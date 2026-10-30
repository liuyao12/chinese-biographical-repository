"""Coverage is proved from executed IDs, not eight successful process exits."""
import copy
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import types
import unittest
from unittest import mock
import uuid
from scripts import python_test_shards as shards

COMMIT = 'a' * 40

class CompleteUnittestShards(unittest.TestCase):
    def fixture(self, body, policy=None):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        (root / 'tests').mkdir()
        module = 'test_shard_fixture_' + uuid.uuid4().hex
        source = root / 'tests' / (module + '.py')
        source.write_text('import unittest\n' + body)
        if policy:
            value = {'schema_version': 1, 'static_skips': [], 'dynamic_skips': [], 'expected_failures': [], **policy(module)}
            (root / shards.POLICY).write_text(json.dumps(value))
        return root, module, source

    def run_all(self, root, plan=None):
        plan = plan or shards.make_plan(root, COMMIT, 8)
        digest = shards.digest(shards.canonical(plan))
        reports = [shards.run_shard(root, plan, i, digest, COMMIT, stream=io.StringIO()) for i in range(8)]
        return plan, digest, reports

    def complete_fixture(self):
        methods = ''.join(f' def test_{i:02}(self): self.assertEqual({i}, {i})\n' for i in range(12))
        body = ('class Sample(unittest.TestCase):\n' + methods
                + ' @unittest.skip("existing decorated skip")\n def test_static_skip(self): pass\n'
                + ' def test_dynamic_skip(self): self.skipTest("optional fixture absent")\n'
                + ' @unittest.expectedFailure\n def test_expected_failure(self): self.assertTrue(False)\n')
        policy = lambda module: {
            'static_skips': [{'test_id': module + '.Sample.test_static_skip', 'reason': 'existing decorated skip', 'condition': {'platform_not': 'win32' if sys.platform != 'win32' else 'darwin'}}],
            'dynamic_skips': [{'test_id': module + '.Sample.test_dynamic_skip', 'reason': 'optional fixture absent', 'condition': {'path_missing': 'optional.json'}}],
            'expected_failures': [{'test_id': module + '.Sample.test_expected_failure', 'reason': 'explicit synthetic existing expected failure'}]}
        return self.fixture(body, policy)

    def test_eight_round_robin_shards_execute_every_discovered_id_once(self):
        root, _, _ = self.complete_fixture()
        plan, digest, reports = self.run_all(root)
        self.assertEqual(len(plan['execution_keys']), 15)
        for i, report in enumerate(reports):
            self.assertEqual(report['assigned_execution_keys'], plan['execution_keys'][i::8])
            self.assertEqual(report['assigned_test_ids'], plan['original_discovery_test_ids'][i::8])
            self.assertEqual(report['exit_code'], 0)
        result = shards.aggregate(plan, reports, digest, COMMIT)
        self.assertEqual(result['covered_execution_keys'], plan['execution_keys'])
        self.assertEqual(len(result['skipped']), 2)
        self.assertEqual(len(result['expected_failures']), 1)
        self.assertTrue(result['successful'])

    def test_empty_shards_have_explicit_successful_ledgers(self):
        root, _, _ = self.fixture('class Sample(unittest.TestCase):\n def test_only(self): pass\n')
        plan, digest, reports = self.run_all(root)
        self.assertEqual(sum(bool(r['assigned_test_ids']) for r in reports), 1)
        self.assertEqual(shards.aggregate(plan, reports, digest, COMMIT)['tests'], 1)

    def test_missing_duplicate_and_extra_reports_cannot_pass(self):
        root, _, _ = self.complete_fixture()
        plan, digest, reports = self.run_all(root)
        for altered in [reports[:-1], reports + [reports[0]], [reports[0]] + reports[:-1]]:
            with self.subTest(count=len(altered)), self.assertRaises(shards.CoverageError):
                shards.aggregate(plan, altered, digest, COMMIT)

    def test_missing_duplicate_and_extra_started_or_result_ids_cannot_pass(self):
        root, _, _ = self.complete_fixture()
        plan, digest, reports = self.run_all(root)
        mutations = [lambda r: r['started_execution_keys'].pop(),
                     lambda r: r['started_execution_keys'].append(r['started_execution_keys'][0]),
                     lambda r: r['started_execution_keys'].append('foreign.Test.test_extra'),
                     lambda r: r['started_test_ids'].pop(),
                     lambda r: r['results'].pop(),
                     lambda r: r['results'].append(copy.deepcopy(r['results'][0]))]
        for change in mutations:
            altered = copy.deepcopy(reports)
            change(altered[0])
            with self.assertRaises(shards.CoverageError):
                shards.aggregate(plan, altered, digest, COMMIT)

    def test_mixed_commit_plan_sources_runtime_and_incomplete_reports_rejected(self):
        root, _, _ = self.complete_fixture()
        plan, digest, reports = self.run_all(root)
        for field, value in [('source_commit', 'b' * 40), ('plan_sha256', 'bad'),
                             ('test_sources_sha256', 'bad'), ('python_major_minor', [0, 0]),
                             ('complete', False), ('exit_code', 1)]:
            altered = copy.deepcopy(reports)
            altered[0][field] = value
            with self.subTest(field=field), self.assertRaises(shards.CoverageError):
                shards.aggregate(plan, altered, digest, COMMIT)

    def test_unexpected_skip_is_a_failure_even_though_unittest_allows_it(self):
        root, _, _ = self.fixture('class Sample(unittest.TestCase):\n def test_skip(self): self.skipTest("new unapproved skip")\n')
        plan, digest, reports = self.run_all(root)
        report = next(r for r in reports if r['tests_run'])
        self.assertTrue(report['unittest_successful'])
        self.assertEqual(report['exit_code'], 1)
        with self.assertRaises(shards.CoverageError):
            shards.aggregate(plan, reports, digest, COMMIT)

    def test_known_dynamic_skip_only_allowed_for_exact_reason_and_condition(self):
        root, module, _ = self.complete_fixture()
        plan = shards.make_plan(root, COMMIT, 8)
        key = next(row['execution_key'] for row in plan['test_instances'] if row['test_id'] == module + '.Sample.test_dynamic_skip')
        self.assertEqual(plan['allowed_skips'][key], 'optional fixture absent')
        (root / 'optional.json').write_text('{}')
        with self.assertRaises(shards.CoverageError):
            shards.run_shard(root, plan, 0, shards.digest(shards.canonical(plan)), COMMIT, stream=io.StringIO())

    def test_failed_error_and_unexpected_success_tests_remain_failed(self):
        bodies = ['def test_failure(self): self.assertTrue(False)',
                  'def test_error(self): raise RuntimeError("actual fixture failure")',
                  '@unittest.expectedFailure\n def test_unexpected_success(self): pass']
        for body in bodies:
            policy = (lambda module: {'expected_failures': [{'test_id': module + '.Sample.test_unexpected_success', 'reason': 'synthetic expected failure must not become an unexpected success'}]}) if '@unittest.expectedFailure' in body else None
            root, _, _ = self.fixture('class Sample(unittest.TestCase):\n ' + body + '\n', policy)
            plan, digest, reports = self.run_all(root)
            report = next(r for r in reports if r['tests_run'])
            self.assertEqual(report['exit_code'], 1)
            with self.assertRaises(shards.CoverageError):
                shards.aggregate(plan, reports, digest, COMMIT)

    def test_subtest_failure_and_skip_cannot_be_hidden_by_parent_success(self):
        for content in ['self.assertTrue(False)', 'self.skipTest("new subtest skip")']:
            root, _, _ = self.fixture('class Sample(unittest.TestCase):\n def test_sub(self):\n  with self.subTest(case=1): ' + content + '\n')
            plan, digest, reports = self.run_all(root)
            self.assertTrue(any(r['exit_code'] == 1 for r in reports))
            with self.assertRaises(shards.CoverageError):
                shards.aggregate(plan, reports, digest, COMMIT)

    def test_setup_class_error_does_not_count_unstarted_tests_as_covered(self):
        root, _, _ = self.fixture('class Sample(unittest.TestCase):\n @classmethod\n def setUpClass(cls): raise RuntimeError("fixture setup failure")\n def test_one(self): pass\n def test_two(self): pass\n')
        plan, digest, reports = self.run_all(root)
        self.assertTrue(any(r['errors'] for r in reports))
        with self.assertRaises(shards.CoverageError):
            shards.aggregate(plan, reports, digest, COMMIT)

    def test_loader_import_and_load_tests_errors_never_become_a_successful_plan(self):
        for body in ['raise ImportError("broken discovery fixture")\n',
                     'def load_tests(loader, tests, pattern): raise RuntimeError("load_tests failed")\n']:
            root, _, _ = self.fixture(body)
            with self.assertRaisesRegex(shards.CoverageError, 'discovery errors'):
                shards.make_plan(root, COMMIT, 8)

    def test_duplicate_original_ids_preserve_every_serial_occurrence_even_for_one_object(self):
        body = ('class Sample(unittest.TestCase):\n def test_one(self): pass\n'
                'def load_tests(loader, tests, pattern):\n case=Sample("test_one")\n return unittest.TestSuite([case]*9)\n')
        root, _, _ = self.fixture(body)
        plan, digest, reports = self.run_all(root)
        self.assertEqual(len(plan['original_discovery_test_ids']), 9)
        self.assertEqual(len(set(plan['original_discovery_test_ids'])), 1)
        self.assertEqual([row['occurrence_ordinal'] for row in plan['test_instances']], list(range(1,10)))
        self.assertEqual(reports[0]['tests_run'], 2)
        self.assertEqual(len(set(reports[0]['started_execution_keys'])), 2)
        self.assertEqual(shards.aggregate(plan, reports, digest, COMMIT)['tests'], 9)

    def test_foreign_loader_failure_sentinel_fails_even_without_own_loader_errors(self):
        body = 'def load_tests(loader, tests, pattern):\n return unittest.TestLoader().loadTestsFromName("missing_shard_fixture_module_123")\n'
        root, _, _ = self.fixture(body)
        with self.assertRaisesRegex(shards.CoverageError, 'failed-loader sentinel'):
            shards.make_plan(root, COMMIT, 8)

    def test_setup_class_skip_does_not_fabricate_execution_of_selected_methods(self):
        root, _, _ = self.fixture('class Sample(unittest.TestCase):\n @classmethod\n def setUpClass(cls): raise unittest.SkipTest("new fixture-level skip")\n def test_one(self): pass\n')
        plan, digest, reports = self.run_all(root)
        report = next(r for r in reports if r['assigned_test_ids'])
        self.assertEqual(report['tests_run'], 0)
        self.assertEqual(report['exit_code'], 1)
        with self.assertRaises(shards.CoverageError):
            shards.aggregate(plan, reports, digest, COMMIT)

    def test_stale_plan_rejects_changed_source_or_new_test_instead_of_running_subset(self):
        for extra in [False, True]:
            root, _, source = self.fixture('class Sample(unittest.TestCase):\n def test_one(self): pass\n')
            plan = shards.make_plan(root, COMMIT, 8)
            if extra:
                (root / 'tests' / ('test_extra_' + uuid.uuid4().hex + '.py')).write_text('import unittest\nclass Extra(unittest.TestCase):\n def test_new(self): pass\n')
            else:
                source.write_text(source.read_text() + '\n# changed input at same nominal commit\n')
            with self.assertRaises(shards.CoverageError):
                shards.run_shard(root, plan, 0, shards.digest(shards.canonical(plan)), COMMIT, stream=io.StringIO())

    def test_commit_guard_rejects_wrong_head_or_dirty_tracked_tree(self):
        with mock.patch.object(shards.subprocess, 'check_output', return_value='b' * 40):
            with self.assertRaisesRegex(shards.CoverageError, 'checkout commit'):
                shards.check_commit(Path('.'), COMMIT, True)
        with mock.patch.object(shards.subprocess, 'check_output', return_value=COMMIT), mock.patch.object(shards.subprocess, 'run', return_value=types.SimpleNamespace(returncode=1)):
            with self.assertRaisesRegex(shards.CoverageError, 'tracked checkout'):
                shards.check_commit(Path('.'), COMMIT, True)

    def test_source_fingerprint_and_commit_guard_include_untracked_corpus_inputs(self):
        root, _, _ = self.fixture('class Sample(unittest.TestCase):\n def test_one(self): pass\n')
        plan = shards.make_plan(root, COMMIT, 8)
        (root / 'corpus').mkdir()
        (root / 'corpus' / 'untracked.json').write_text('{}')
        with self.assertRaises(shards.CoverageError):
            shards.run_shard(root, plan, 0, shards.digest(shards.canonical(plan)), COMMIT, stream=io.StringIO())
        with mock.patch.object(shards.subprocess, 'check_output', side_effect=[COMMIT, b'corpus/untracked.json\0']), mock.patch.object(shards.subprocess, 'run', return_value=types.SimpleNamespace(returncode=0)):
            with self.assertRaisesRegex(shards.CoverageError, 'untracked source'):
                shards.check_commit(root, COMMIT, True)
        with mock.patch.object(shards.subprocess, 'check_output', side_effect=[COMMIT, b'.ci-results/plan.json\0build/output.sqlite\0scripts/__pycache__/cache.pyc\0']), mock.patch.object(shards.subprocess, 'run', return_value=types.SimpleNamespace(returncode=0)):
            shards.check_commit(root, COMMIT, True)

    def test_new_skip_or_expected_failure_decorator_cannot_authorize_itself(self):
        for decorator, line in [('@unittest.skip("new unapproved skip")', 'pass'),
                                ('@unittest.expectedFailure', 'self.assertTrue(False)')]:
            root, _, _ = self.fixture('class Sample(unittest.TestCase):\n ' + decorator + '\n def test_new(self): ' + line + '\n')
            with self.assertRaisesRegex(shards.CoverageError, 'unapproved'):
                shards.make_plan(root, COMMIT, 8)

    def test_known_static_skip_id_and_reason_still_need_the_original_capability_condition(self):
        policy = lambda module: {'static_skips': [{'test_id': module + '.Sample.test_skip', 'reason': 'same existing reason', 'condition': {'platform_not': sys.platform}}]}
        root, _, _ = self.fixture('class Sample(unittest.TestCase):\n @unittest.skip("same existing reason")\n def test_skip(self): pass\n', policy)
        with self.assertRaisesRegex(shards.CoverageError, 'unapproved decorator skip'):
            shards.make_plan(root, COMMIT, 8)

    def test_cli_end_to_end_manifests_cover_every_id_and_missing_artifact_fails(self):
        root, _, _ = self.complete_fixture()
        out = root / '.ci-results'
        plan_path = out / 'plan.json'
        def command(*args, expected=0):
            run = subprocess.run([sys.executable, shards.__file__, *args, '--root', str(root), '--commit', COMMIT], capture_output=True, text=True)
            self.assertEqual(run.returncode, expected, run.stdout + run.stderr)
        command('plan', '--shards', '8', '--output', str(plan_path))
        for i in range(8):
            command('run', '--plan', str(plan_path), '--index', str(i), '--output', str(out / f'shard-{i}.json'))
        coverage = out / 'coverage.json'
        command('aggregate', '--plan', str(plan_path), '--reports', str(out), '--output', str(coverage))
        value = json.loads(coverage.read_text())
        self.assertEqual(value['covered_execution_keys'], json.loads(plan_path.read_text())['execution_keys'])
        (out / 'shard-3.json').unlink()
        command('aggregate', '--plan', str(plan_path), '--reports', str(out), '--output', str(coverage), expected=1)
        self.assertFalse(json.loads(coverage.read_text())['complete'])

if __name__ == '__main__':
    unittest.main(verbosity=2)
