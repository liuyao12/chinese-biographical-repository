"""Run in-process mutation tests against real inputs with private per-test edits."""
import builtins
from contextlib import ExitStack, contextmanager
import io
import os
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
from unittest.mock import patch


@contextmanager
def edited_inputs(root):
    """Overlay Python file opens and Path.stat on an existing directory layout.

    Intended for synchronous validator tests editing named input files. Directory
    enumeration, OS-level file mutations and subprocesses use the real filesystem.
    """
    entered_root = Path(os.path.abspath(root))
    root = entered_root.resolve()
    with TemporaryDirectory(prefix='cbr-edits-') as directory, ExitStack() as stack:
        changed = {}
        def key(file):
            path = Path(os.path.abspath(os.fsdecode(file)))
            if entered_root != root and path.is_relative_to(entered_root):
                path = root / path.relative_to(entered_root)
            if path.is_relative_to(root) and os.path.islink(path):
                return Path(os.path.realpath(path))
            return path
        def redirect(original):
            def routed(file, mode='r', *args, **kwargs):
                if isinstance(file, int):
                    return original(file, mode, *args, **kwargs)
                path = key(file)
                if not path.is_relative_to(root):
                    return original(file, mode, *args, **kwargs)
                if any(flag in mode for flag in 'wax+') and path not in changed:
                    target = Path(directory) / str(len(changed))
                    if 'x' in mode and path.exists():
                        raise FileExistsError(path)
                    if not path.parent.is_dir() or mode.startswith('r') and not path.exists():
                        raise FileNotFoundError(path)
                    if path.is_dir():
                        raise IsADirectoryError(path)
                    if ('a' in mode or mode.startswith('r')) and path.exists():
                        with original(path, 'rb') as src, original(target, 'wb') as dst:
                            shutil.copyfileobj(src, dst)
                    changed[path] = target
                return original(changed.get(path, file), mode, *args, **kwargs)
            return routed
        original_stat = Path.stat
        def routed_stat(path, *args, **kwargs):
            private = changed.get(key(path)) if kwargs.get('follow_symlinks', True) else None
            return original_stat(private if private is not None else path, *args, **kwargs)
        stack.enter_context(patch.object(Path, 'stat', routed_stat))
        stack.enter_context(patch.object(builtins, 'open', redirect(builtins.open)))
        stack.enter_context(patch.object(io, 'open', redirect(io.open)))
        yield changed
