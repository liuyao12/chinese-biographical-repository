"""Per-validation memo of bounded readonly WYD proof construction.

No data survive the owning call. The original proof runs on every cache miss;
caller-owned values are never retained or returned by reference.
"""
from contextvars import ContextVar
from contextlib import contextmanager
from functools import wraps
from pathlib import Path
import copy
import hashlib
import json
import sys

# Package and direct-script imports must use the same handle, including mixed use.
_THIS = sys.modules[__name__]
_OTHER = 'validation_context' if __name__ == 'scripts.validation_context' else 'scripts.validation_context'
sys.modules.setdefault(_OTHER, _THIS)
_ACTIVE = ContextVar('cbr_single_validation_context', default=None)
DEPENDENCIES = ('corpus', 'registry', 'source-evidence', 'sources',
                'data/historical-tables', 'data/corpus', 'docs', 'schema', 'scripts')
DRIFT_ERROR = '驗證期間來源依賴內容或檔案集合變動；本次結果不可採信'


def fingerprint(root):
    """Fresh bytes and membership; never consult the proof memo."""
    root = Path(root).resolve()
    result = {}
    for rel in DEPENDENCIES:
        base = root / rel
        paths = [base] if base.is_file() else sorted(base.rglob('*')) if base.exists() else []
        for path in paths:
            if not path.is_file():
                continue
            # Lazy imports may create bytecode during ordinary Python runs.
            # The executable source files remain part of this fingerprint.
            if rel == 'scripts' and ('__pycache__' in path.relative_to(base).parts
                                     or path.suffix in ('.pyc', '.pyo')):
                continue
            before = path.stat()
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            after = path.stat()
            attrs = lambda st: (st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns, st.st_ctime_ns)
            if attrs(before) != attrs(after):
                raise ValueError(DRIFT_ERROR)
            result[path.relative_to(root).as_posix()] = (digest, attrs(after))
    return result


@contextmanager
def scope(root, enabled=True):
    """Fresh even when nested; finally disables and destroys the private memo."""
    state = {'root': Path(root).resolve(), 'memo': {}, 'closed': False} if enabled else None
    token = _ACTIVE.set(state)
    try:
        yield state
    finally:
        if state is not None:
            state['closed'] = True
            state['memo'].clear()
        _ACTIVE.reset(token)


def _json_tree(value):
    # JSON encoding must not collapse unsupported Python shapes (tuple/list,
    # integer/string keys, subclasses) onto an earlier valid proof key.
    if type(value) in (str, int, float, bool) or value is None:
        return True
    if type(value) is list:
        return all(_json_tree(item) for item in value)
    if type(value) is dict:
        return all(type(key) is str and _json_tree(item) for key, item in value.items())
    return False


def memoized(root_index):
    def decorate(function):
        @wraps(function)
        def call(*args, **kwargs):
            state = _ACTIVE.get()
            if state is None or state['closed'] or kwargs or len(args) <= root_index:
                return function(*args, **kwargs)
            try:
                root = Path(args[root_index]).resolve()
                if root != state['root']:
                    return function(*args, **kwargs)
                values = list(args)
                values[root_index] = str(root)
                if not _json_tree(values):
                    return function(*args, **kwargs)
                # All in-memory fields participate, not IDs or selected qualifiers.
                key = (function.__module__, function.__qualname__, json.dumps(values, ensure_ascii=False, sort_keys=True, allow_nan=False))
            except (TypeError, ValueError, OSError):
                return function(*args, **kwargs)
            if key not in state['memo']:
                # Exceptions remain uncached and retain their original type/message.
                state['memo'][key] = copy.deepcopy(function(*args, **kwargs))
            return copy.deepcopy(state['memo'][key])
        return call
    return decorate
