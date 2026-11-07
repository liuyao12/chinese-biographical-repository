"""Independent test copies: APFS clones when available, ordinary copy2 everywhere else."""
import ctypes
import errno
import os
import shutil
import sys
from functools import lru_cache

_UNSUPPORTED = {errno.EXDEV, errno.ENOSYS, errno.EINVAL, errno.ENOTSUP, errno.EOPNOTSUPP}

@lru_cache(maxsize=1)
def _clone_function():
    library = ctypes.CDLL(None, use_errno=True)
    function = library.clonefile
    function.argtypes = (ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int)
    function.restype = ctypes.c_int
    # Retain the library along with its callable; no file contents are cached.
    return library, function

def _clonefile(source, destination):
    try:
        _, function = _clone_function()
    except (AttributeError, OSError):
        raise OSError(errno.ENOSYS, 'clonefile unavailable')
    if function(os.fsencode(source), os.fsencode(destination), 0) != 0:
        code = ctypes.get_errno()
        raise OSError(code, os.strerror(code), os.fspath(destination))

def fixture_copy2(source, destination, *, follow_symlinks=True):
    """copytree-compatible copy2; never hardlink or alter the source file.

    Existing destinations and symlinks use copy2's own semantics. Clone errors
    other than unsupported/cross-filesystem propagate, including ENOSPC.
    """
    if os.path.isdir(destination):
        destination = os.path.join(destination, os.path.basename(source))
    if (sys.platform != 'darwin' or not follow_symlinks
            or os.path.islink(source) or os.path.lexists(destination)):
        return shutil.copy2(source, destination, follow_symlinks=follow_symlinks)
    try:
        _clonefile(source, destination)
    except OSError as error:
        if error.errno not in _UNSUPPORTED:
            raise
        return shutil.copy2(source, destination, follow_symlinks=follow_symlinks)
    shutil.copystat(source, destination, follow_symlinks=follow_symlinks)
    return destination


def copy_required_native_source_fixtures(source_root, destination_root):
    """Copy the two declared physical inputs required by native source proofs."""
    from pathlib import Path
    source_root, destination_root = Path(source_root), Path(destination_root)
    # Pei immutable occurrence capture and Liang's current source-role fixture.
    paths = (
        'tests/fixtures/occurrence-concordance/original-anchors.json',
        'tests/fixtures/nanqi033-wangsengqian/person-ids.json',
    )
    for relative in paths:
        source, destination = source_root / relative, destination_root / relative
        if not source.is_file():
            raise FileNotFoundError(source)
        destination.parent.mkdir(parents=True, exist_ok=True)
        fixture_copy2(source, destination)
        if os.path.samefile(source, destination):
            raise ValueError('native source fixture must be an independent copy')
        if source.read_bytes() != destination.read_bytes():
            raise ValueError('native source fixture copy differs from current source')
