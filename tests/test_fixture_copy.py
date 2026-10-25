import errno
import os
from pathlib import Path
import shutil
import stat
import sys
import tempfile
import unittest
from unittest.mock import patch
import importlib.util
_spec = importlib.util.spec_from_file_location('fixture_copy', Path(__file__).with_name('fixture_copy.py'))
f = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(f)


class FixtureCopyTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)  # Deliberately retain macOS /var alias.
        self.src = self.root / 'source'
        self.dst = self.root / 'destination'
        self.src.write_bytes(b'original\x00content' * 100)
        self.src.chmod(0o640)
        os.utime(self.src, ns=(1700000000123456789, 1700000000987654321))

    def isolated(self, dst):
        dst = Path(dst)
        original = self.src.read_bytes()
        self.assertEqual(dst.read_bytes(), original)
        self.assertFalse(os.path.samestat(self.src.stat(), dst.stat()))
        self.assertEqual(self.src.stat().st_nlink, 1)
        self.assertEqual(dst.stat().st_nlink, 1)
        dst.write_bytes(b'clone edit')
        self.assertEqual(self.src.read_bytes(), original)
        self.src.write_bytes(b'source edit')
        self.assertEqual(dst.read_bytes(), b'clone edit')

    def test_real_tempfile_alias_metadata_and_two_way_isolation(self):
        before = self.src.stat()
        self.assertEqual(f.copy_fixture_file(self.src, self.dst), self.dst)
        after = self.dst.stat()
        self.assertEqual(stat.S_IMODE(after.st_mode), stat.S_IMODE(before.st_mode))
        self.assertEqual(after.st_mtime_ns, before.st_mtime_ns)
        self.assertEqual(after.st_atime_ns, self.src.stat().st_atime_ns)
        self.isolated(self.dst)

    def test_real_relative_paths_preserve_string_return(self):
        # Avoid process-global chdir: relative paths from the existing cwd suffice.
        src = os.path.relpath(self.src)
        dst = os.path.relpath(self.dst)
        self.assertEqual(f.copy_fixture_file(src, dst), dst)
        self.isolated(self.dst)

    def test_path_and_string_return_match_copy2(self):
        for index, kind in enumerate((str, Path)):
            dst = kind(self.root / ('target' + str(index)))
            result = f.copy_fixture_file(self.src, dst)
            self.assertEqual(type(result), type(dst))
            self.assertEqual(result, dst)

    def test_directory_destination_return_matches_copy2(self):
        directory = self.root / 'folder'; directory.mkdir()
        ordinary = self.root / 'ordinary'; ordinary.mkdir()
        result = f.copy_fixture_file(self.src, directory)
        reference = shutil.copy2(self.src, ordinary)
        self.assertEqual(type(result), type(reference))
        self.assertEqual(result, os.path.join(directory, self.src.name))
        self.isolated(result)

    def test_real_overwrite_fallback_is_independent(self):
        self.dst.write_bytes(b'old longer data' * 1000)
        self.assertEqual(f.copy_fixture_file(self.src, self.dst), self.dst)
        self.isolated(self.dst)

    def test_same_file_rejected_without_mutation(self):
        original = self.src.read_bytes()
        with self.assertRaises(shutil.SameFileError):
            f.copy_fixture_file(self.src, self.src)
        self.assertEqual(self.src.read_bytes(), original)

    @unittest.skipUnless(sys.platform == 'darwin', 'Darwin-specific rejection contract')
    def test_final_symlinks_and_nonregular_rejected(self):
        link = self.root / 'link'; link.symlink_to(self.src)
        original = self.src.read_bytes()
        for src, dst in ((link, self.dst), (self.src, link)):
            with self.assertRaises(ValueError): f.copy_fixture_file(src, dst)
        directory = self.root / 'source-directory'; directory.mkdir()
        with self.assertRaises(ValueError): f.copy_fixture_file(directory, self.dst)
        self.assertEqual(self.src.read_bytes(), original)
        self.assertFalse(self.dst.exists())

    def test_forced_linux_is_exact_copy2_dispatch(self):
        with patch.object(f, '_platform', 'linux'), patch.object(f, '_clonefile', side_effect=AssertionError('must not clone')):
            self.assertEqual(f.copy_fixture_file(self.src, self.dst), self.dst)
        self.isolated(self.dst)

    def test_clone_failure_falls_back_to_real_copy2(self):
        for number in (errno.ENOTSUP, errno.EXDEV, errno.ENOSYS, errno.ENOSPC):
            with self.subTest(errno=number):
                self.dst.unlink(missing_ok=True)
                with patch.object(f, '_platform', 'darwin'), patch.object(f, '_clonefile', side_effect=OSError(number, 'injected clone failure')):
                    self.assertEqual(f.copy_fixture_file(self.src, self.dst), self.dst)
                self.assertEqual(self.dst.read_bytes(), self.src.read_bytes())
                self.assertFalse(os.path.samestat(self.src.stat(), self.dst.stat()))

    def test_partial_clone_failure_copies_complete_bytes(self):
        def partial(src, dst):
            Path(dst).write_bytes(b'partial'); raise OSError(errno.EIO, 'injected')
        with patch.object(f, '_platform', 'darwin'), patch.object(f, '_clonefile', side_effect=partial):
            f.copy_fixture_file(self.src, self.dst)
        self.isolated(self.dst)

    def test_real_copy_failure_propagates(self):
        # Patch only this helper's dependency binding, never global shutil.
        class FailedCopy:
            @staticmethod
            def copy2(*args, **kwargs): raise OSError(errno.ENOSPC, 'injected full disk')
        original = self.src.read_bytes()
        with patch.object(f, '_platform', 'darwin'), patch.object(f, '_clonefile', side_effect=OSError(errno.ENOTSUP, 'injected')), patch.object(f, 'shutil', FailedCopy):
            with self.assertRaises(OSError) as error: f.copy_fixture_file(self.src, self.dst)
        self.assertEqual(error.exception.errno, errno.ENOSPC)
        self.assertEqual(self.src.read_bytes(), original)

    @unittest.skipUnless(sys.platform == 'darwin', 'real clone then injected metadata failure')
    def test_metadata_failure_propagates(self):
        class FailedMetadata:
            @staticmethod
            def copystat(*args, **kwargs): raise OSError(errno.EPERM, 'injected metadata error')
        with patch.object(f, 'shutil', FailedMetadata):
            with self.assertRaises(OSError) as error: f.copy_fixture_file(self.src, self.dst)
        self.assertEqual(error.exception.errno, errno.EPERM)
        self.assertEqual(self.dst.read_bytes(), self.src.read_bytes())

    def test_actual_setup_like_layout_and_cleanup(self):
        source = self.root / 'repo'; fixture = self.root / 'fixture'
        folders = ('registry', 'corpus', 'source-evidence', 'data/historical-tables', 'sources', 'data/works')
        for folder in folders:
            p = source / folder; p.mkdir(parents=True)
            (p / 'record.json').write_bytes(b'{"record": "unchanged"}')
            p.chmod(0o750); os.utime(p, ns=(1700000000000000000, 1700000001000000000))
            shutil.copytree(p, fixture / folder, copy_function=f.copy_fixture_file)
            self.assertEqual((fixture / folder / 'record.json').read_bytes(), (p / 'record.json').read_bytes())
            self.assertEqual(stat.S_IMODE((fixture / folder).stat().st_mode), 0o750)
            self.assertEqual((fixture / folder).stat().st_mtime_ns, p.stat().st_mtime_ns)
        (fixture / 'corpus/record.json').write_bytes(b'fixture mutation')
        self.assertEqual((source / 'corpus/record.json').read_bytes(), b'{"record": "unchanged"}')
        shutil.rmtree(fixture)
        self.assertTrue((source / 'sources/record.json').exists())


if __name__ == '__main__': unittest.main()
