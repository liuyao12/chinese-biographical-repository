"""Independent regular-file fixture copies; APFS CoW when available.

Linux keeps shutil.copy2 behavior. Darwin accepts OS parent aliases (including
/var -> /private/var), but never copies through a final symlink. Intended for
controlled temporary fixtures, not adversarial concurrent path mutation.
"""
import ctypes
import functools
import os
from pathlib import Path
import shutil
import stat
import sys

_platform = sys.platform


@functools.lru_cache(maxsize=1)
def _clone_function():
    library = ctypes.CDLL('/usr/lib/libSystem.B.dylib', use_errno=True)
    function = library.clonefile
    function.argtypes = (ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int)
    function.restype = ctypes.c_int
    return library, function


def _clonefile(src, dst):
    _, function = _clone_function()
    if function(os.fsencode(src), os.fsencode(dst), 0):
        number = ctypes.get_errno()
        raise OSError(number, os.strerror(number), os.fspath(dst))


def _regular(path, *, absent=False):
    try:
        mode = path.lstat().st_mode
    except FileNotFoundError:
        if absent:
            return
        raise
    if not stat.S_ISREG(mode):
        raise ValueError('fixture copy requires a regular file, not a final symlink')


def copy_fixture_file(src, dst, *, follow_symlinks=True):
    """copy2-compatible result/metadata for this regular-file fixture scope.

    No hardlinks. Clone failures use real copy2; copy/metadata errors propagate.
    Directory metadata is still handled by ordinary shutil.copytree. Parent
    aliases are canonicalized only for the Darwin operation, not its return.
    """
    if _platform != 'darwin':
        return shutil.copy2(src, dst, follow_symlinks=follow_symlinks)
    source = Path(src)
    _regular(source)
    destination = Path(dst)
    if destination.is_symlink():
        raise ValueError('fixture destination must not be a final symlink')
    result = dst
    if destination.is_dir():
        result = os.path.join(dst, os.path.basename(src))
        destination = Path(result)
    _regular(destination, absent=True)
    source = source.parent.resolve(strict=True) / source.name
    destination = destination.parent.resolve(strict=True) / destination.name
    # Detect a repeated/same-file path before a clone attempt or fallback write.
    if destination.exists() and os.path.samestat(source.stat(), destination.stat()):
        raise shutil.SameFileError(src, result, 'are the same file')
    try:
        _clonefile(source, destination)
    except (OSError, AttributeError):
        shutil.copy2(source, destination, follow_symlinks=follow_symlinks)
        return result
    if os.path.samestat(source.stat(), destination.stat()):
        raise RuntimeError('clone unexpectedly shares the source inode')
    shutil.copystat(source, destination, follow_symlinks=follow_symlinks)
    return result
