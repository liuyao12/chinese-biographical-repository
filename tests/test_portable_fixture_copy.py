"""Portable fixture-copy behavior; all source and destination files are disposable."""
import errno
import os
from pathlib import Path
import shutil
import stat
import sys
import tempfile
import unittest
from unittest.mock import patch
from tests import portable_fixture_copy as h

class PortableFixtureCopy(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
        self.source=self.root/'source';self.source.write_bytes(b'fixture source\x00\xff');self.source.chmod(0o640);os.utime(self.source,ns=(1300000000000000000,1300000000123456789));self.destination=self.root/'destination'
    def attributes(self,path):
        s=path.stat();return(s.st_dev,s.st_ino,s.st_size,stat.S_IMODE(s.st_mode),s.st_mtime_ns,s.st_ctime_ns,s.st_nlink)
    def check_independent(self,before):
        self.assertEqual(self.destination.read_bytes(),self.source.read_bytes());a=self.source.stat();b=self.destination.stat();self.assertNotEqual((a.st_dev,a.st_ino),(b.st_dev,b.st_ino));self.assertEqual((a.st_nlink,b.st_nlink),(1,1));self.assertEqual((a.st_size,stat.S_IMODE(a.st_mode),a.st_mtime_ns),(b.st_size,stat.S_IMODE(b.st_mode),b.st_mtime_ns));self.assertEqual(self.attributes(self.source),before)
        self.destination.write_bytes(b'destination changed');self.assertEqual(self.source.read_bytes(),b'fixture source\x00\xff');self.assertEqual(self.attributes(self.source),before)
    @unittest.skipUnless(sys.platform=='darwin','actual Darwin clonefile only')
    def test_actual_clone_independent_bytes_and_metadata(self):
        before=self.attributes(self.source)
        with patch.object(h,'_clonefile',wraps=h._clonefile)as clone,patch.object(h.shutil,'copy2',side_effect=AssertionError('actual APFS clone must not fall back')):
            self.assertEqual(h.fixture_copy2(self.source,self.destination),self.destination);self.assertEqual(clone.call_count,1)
        self.check_independent(before)
    def test_non_darwin_uses_copy2_without_loading_clone(self):
        before=self.attributes(self.source)
        with patch.object(h.sys,'platform','linux'),patch.object(h,'_clonefile',side_effect=AssertionError('Linux cannot invoke Darwin clone')),patch.object(h.shutil,'copy2',wraps=shutil.copy2)as cp:
            h.fixture_copy2(self.source,self.destination);self.assertEqual(cp.call_count,1)
        self.check_independent(before)
    def test_unsupported_and_cross_filesystem_fallback(self):
        for number in sorted(h._UNSUPPORTED):
            with self.subTest(errno=number):
                before=self.attributes(self.source)
                with patch.object(h.sys,'platform','darwin'),patch.object(h,'_clonefile',side_effect=OSError(number,'simulated unsupported')),patch.object(h.shutil,'copy2',wraps=shutil.copy2)as cp:
                    h.fixture_copy2(self.source,self.destination);self.assertEqual(cp.call_count,1)
                self.check_independent(before);self.destination.unlink()
    def test_real_io_errors_propagate_without_copy_or_success(self):
        for number in [errno.ENOSPC,errno.EACCES,errno.EIO]:
            with self.subTest(errno=number),patch.object(h.sys,'platform','darwin'),patch.object(h,'_clonefile',side_effect=OSError(number,'simulated true error')),patch.object(h.shutil,'copy2',side_effect=AssertionError('must not swallow real I/O failure')):
                with self.assertRaises(OSError)as error:h.fixture_copy2(self.source,self.destination)
                self.assertEqual(error.exception.errno,number);self.assertFalse(self.destination.exists())
    def test_existing_destination_retains_copy2_semantics(self):
        self.destination.write_bytes(b'old destination');before=self.attributes(self.source)
        with patch.object(h.sys,'platform','darwin'),patch.object(h,'_clonefile',side_effect=AssertionError('existing destination must use copy2')):h.fixture_copy2(self.source,self.destination)
        self.check_independent(before)
    def test_directory_destination_matches_copy2(self):
        directory=self.root/'directory';directory.mkdir();h.fixture_copy2(self.source,directory);self.destination=directory/self.source.name;self.check_independent(self.attributes(self.source))
    @unittest.skipUnless(hasattr(os,'symlink'),'symlinks required')
    def test_symlink_source_follow_and_no_follow_match_copy2(self):
        link=self.root/'source-link';link.symlink_to(self.source)
        with patch.object(h.sys,'platform','darwin'),patch.object(h,'_clonefile',side_effect=AssertionError('symlinks must use copy2')):
            h.fixture_copy2(link,self.destination);self.assertFalse(self.destination.is_symlink());self.assertEqual(self.destination.read_bytes(),self.source.read_bytes());self.destination.unlink()
            h.fixture_copy2(link,self.destination,follow_symlinks=False);self.assertTrue(self.destination.is_symlink());self.assertEqual(os.readlink(self.destination),os.readlink(link));self.assertNotEqual(link.lstat().st_ino,self.destination.lstat().st_ino)
    @unittest.skipUnless(hasattr(os,'symlink'),'symlinks required')
    def test_existing_destination_symlink_matches_copy2(self):
        target=self.root/'other-target';target.write_bytes(b'previous');self.destination.symlink_to(target)
        with patch.object(h.sys,'platform','darwin'),patch.object(h,'_clonefile',side_effect=AssertionError('existing symlink must use copy2')):h.fixture_copy2(self.source,self.destination)
        self.assertTrue(self.destination.is_symlink());self.assertEqual(target.read_bytes(),self.source.read_bytes());self.assertEqual(self.source.read_bytes(),b'fixture source\x00\xff')
    def test_same_file_is_rejected_like_copy2(self):
        before=self.attributes(self.source)
        with self.assertRaises(shutil.SameFileError):h.fixture_copy2(self.source,self.source)
        self.assertEqual(self.attributes(self.source),before)
if __name__=='__main__':unittest.main(verbosity=2)
