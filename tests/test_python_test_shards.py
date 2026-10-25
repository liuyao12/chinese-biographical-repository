"""Small subprocess fixtures only; never discover the production suite here."""
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/python_test_shards.py'
SPEC = importlib.util.spec_from_file_location('shard_driver_under_test', SCRIPT)
s = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(s)
SHA = 'a' * 40


class Shards(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.tests = self.root / 'tests'
        self.tests.mkdir()
        self.addCleanup(self.tmp.cleanup)

    def fixture(self, failure=False):
        text = '''import unittest
from pathlib import Path
LOG = Path(__file__).with_name('lifecycle.txt')
def log(x):
    with LOG.open('a') as f: f.write(x + '\\n')
class A(unittest.TestCase):
    @classmethod
    def setUpClass(cls): log('class_setup')
    @classmethod
    def tearDownClass(cls): log('class_teardown')
    def setUp(self): log('setup:' + self.id())
    def tearDown(self): log('teardown:' + self.id())
'''
        for i in range(12):
            text += f'    def test_{i:02}(self):\n        self.assertTrue({not failure or i != 0!r})\n'
        (self.tests / 'test_tiny.py').write_text(text)

    def command(self, *args):
        if args and args[0] == 'verify':
            args = (args[0], '--start-directory', self.tests, *args[1:])
        return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], cwd=self.root,
                              env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'),
                              capture_output=True, text=True, timeout=30)

    def run_piece(self, index, extra=()):
        path = self.root / f'{index}.json'
        result = self.command('run', '--start-directory', self.tests, '--index', index,
                              '--count', 2, '--revision', SHA, '--manifest', path, *extra)
        return result, path

    def successful(self):
        self.fixture()
        paths = []
        for index in range(2):
            result, path = self.run_piece(index)
            self.assertEqual(result.returncode, 0, result.stderr)
            paths.append(path)
        self.assertEqual(s.verify(paths, SHA, 2, [f'test_tiny.A.test_{i:02}' for i in range(12)]), 12)
        gate = self.command('verify', '--revision', SHA, '--count', 2, *paths)
        self.assertEqual(gate.returncode, 0, gate.stderr)
        return paths

    def test_real_subprocess_union_and_lifecycle(self):
        paths = self.successful()
        rows = [json.loads(p.read_text()) for p in paths]
        self.assertEqual(rows[0]['all_ids'], rows[1]['all_ids'])
        lines = (self.tests / 'lifecycle.txt').read_text().splitlines()
        self.assertEqual(lines.count('class_setup'), 2)
        self.assertEqual(lines.count('class_teardown'), 2)
        self.assertEqual(len([x for x in lines if x.startswith('setup:')]), 12)
        self.assertEqual(len([x for x in lines if x.startswith('teardown:')]), 12)
        self.assertEqual(set(rows[0]['selected_ids']) & set(rows[1]['selected_ids']), set())

    def test_failure_is_nonzero(self):
        self.fixture(failure=True)
        index = int.from_bytes(hashlib.sha256(b'test_tiny.A.test_00').digest(), 'big') % 2
        result, path = self.run_piece(index)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(json.loads(path.read_text())['success'])

    def test_import_error_is_nonzero(self):
        (self.tests / 'test_bad.py').write_text('raise RuntimeError("import broke")\n')
        result, path = self.run_piece(0)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(json.loads(path.read_text())['complete'])

    def test_list_rejects_import_errors_and_failed_test_objects(self):
        (self.tests/'test_bad.py').write_text('raise ImportError("missing dependency")\n')
        result, path = self.run_piece(0, ('--list',))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('discovery/import error', json.loads(path.read_text())['exception'])
        (self.tests/'test_bad.py').unlink()
        (self.tests/'test_failed.py').write_text("import unittest\ndef load_tests(loader, tests, pattern):\n return unittest.TestSuite([unittest.loader._FailedTest('missing', ImportError('hidden'))])\n")
        result, path = self.run_piece(0, ('--list',))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('discovery/import error', json.loads(path.read_text())['exception'])

    def test_process_exit_leaves_incomplete_receipt(self):
        (self.tests / 'test_exit.py').write_text('import os,unittest\nclass X(unittest.TestCase):\n def test_exit(self): os._exit(7)\n')
        index = int.from_bytes(hashlib.sha256(b'test_exit.X.test_exit').digest(), 'big') % 2
        result, path = self.run_piece(index)
        self.assertEqual(result.returncode, 7)
        row = json.loads(path.read_text())
        self.assertFalse(row['complete'])
        self.assertFalse(row['success'])

    def test_bad_receipts_rejected(self):
        paths = self.successful()
        originals = [json.loads(p.read_text()) for p in paths]
        mutations = {
            'overlap': lambda rows: rows[1].update(selected_ids=rows[0]['selected_ids']),
            'wrong_sha': lambda rows: rows[1].update(revision='b' * 40),
            'incomplete': lambda rows: rows[1].update(complete=False),
            'wrong_count': lambda rows: rows[1].update(tests_run=0),
            'different_universe': lambda rows: rows[1]['all_ids'].pop(),
            'duplicate_index': lambda rows: rows[1].update(shard_index=0),
            'failed': lambda rows: rows[1].update(success=False),
            'hidden_error': lambda rows: rows[1].update(errors=1),
        }
        for name, mutate in mutations.items():
            with self.subTest(name=name):
                rows = copy.deepcopy(originals)
                mutate(rows)
                for p, row in zip(paths, rows): p.write_text(json.dumps(row))
                self.assertNotEqual(self.command('verify', '--revision', SHA, '--count', 2, *paths).returncode, 0)
        for p, row in zip(paths, originals): p.write_text(json.dumps(row))
        self.assertNotEqual(self.command('verify', '--revision', SHA, '--count', 2, paths[0]).returncode, 0)
        paths[1].write_text('{"truncated":')
        self.assertNotEqual(self.command('verify', '--revision', SHA, '--count', 2, *paths).returncode, 0)

    def test_duplicate_ids_empty_and_parameters_rejected(self):
        with self.assertRaises(ValueError): s.selection(['same', 'same'], 0, 2)
        with self.assertRaises(ValueError): s.selection([], 0, 2)
        self.fixture()
        for index, count in ((-1, 2), (2, 2), (0, 0)):
            self.assertNotEqual(self.command('run', '--start-directory', self.tests, '--index', index,
                                            '--count', count, '--revision', SHA, '--manifest', self.root/'bad.json').returncode, 0)
        self.assertNotEqual(self.command('run', '--index', 'x', '--count', 2, '--manifest', self.root/'bad.json').returncode, 0)
        # One discovered case, two shards: the unassigned shard is rejected.
        (self.tests/'test_tiny.py').write_text('import unittest\nclass X(unittest.TestCase):\n def test_one(self): pass\n')
        index = 1 - int.from_bytes(hashlib.sha256(b'test_tiny.X.test_one').digest(), 'big') % 2
        result, _ = self.run_piece(index)
        self.assertNotEqual(result.returncode, 0)

    def test_discovered_duplicate_and_class_setup_error_fail(self):
        (self.tests/'test_dup.py').write_text("import unittest\nclass X(unittest.TestCase):\n def test_one(self): pass\ndef load_tests(loader, tests, pattern):\n case=X('test_one')\n return unittest.TestSuite([case,case])\n")
        result, path = self.run_piece(0)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('duplicate', json.loads(path.read_text())['exception'])
        (self.tests/'test_dup.py').unlink()
        (self.tests/'test_setup.py').write_text("import unittest\nclass X(unittest.TestCase):\n @classmethod\n def setUpClass(cls): raise RuntimeError('broken setup')\n def test_one(self): pass\n")
        index = int.from_bytes(hashlib.sha256(b'test_setup.X.test_one').digest(), 'big') % 2
        result, path = self.run_piece(index)
        self.assertNotEqual(result.returncode, 0)
        row = json.loads(path.read_text())
        self.assertEqual(row['tests_run'], 0)
        self.assertFalse(row['complete'])

    def test_coordinated_omission_rejected_against_checkout(self):
        paths = self.successful()
        rows = [json.loads(p.read_text()) for p in paths]
        # Both shards falsely agree on a smaller universe with coherent success.
        smaller = rows[0]['all_ids'][1:]
        for row, path in zip(rows, paths):
            row['all_ids'] = smaller
            row['selected_ids'] = s.selection(smaller, row['shard_index'], 2)
            row['tests_run'] = len(row['selected_ids'])
            self.assertTrue(row['complete'] and row['success'])
            path.write_text(json.dumps(row))
        result = self.command('verify', '--revision', SHA, '--count', 2, *paths)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('inconsistent', result.stderr)

    def test_new_checkout_case_after_shard_run_is_rejected(self):
        paths = self.successful()
        (self.tests/'test_added.py').write_text('import unittest\nclass Added(unittest.TestCase):\n def test_new(self): pass\n')
        result = self.command('verify', '--revision', SHA, '--count', 2, *paths)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('inconsistent', result.stderr)

    def test_fresh_verify_import_error_is_rejected(self):
        paths = self.successful()
        (self.tests/'test_broken.py').write_text('raise ImportError("new error")\n')
        result = self.command('verify', '--revision', SHA, '--count', 2, *paths)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('discovery/import error', result.stderr)

    def test_list_is_not_execution_success(self):
        self.fixture()
        result, path = self.run_piece(0, ('--list',))
        self.assertEqual(result.returncode, 0)
        row = json.loads(path.read_text())
        self.assertTrue(row['discovery_complete'])
        self.assertFalse(row['complete'])
        self.assertFalse((self.tests/'lifecycle.txt').exists())
        with self.assertRaises(ValueError): s.verify([path], SHA, 1, [f'test_tiny.A.test_{i:02}' for i in range(12)])


if __name__ == '__main__':
    unittest.main()
