"""Native reader boundary plus synthetic 3.13 definition/delegate controls.

Synthetic module/owner objects exercise classification, not Python 3.13 IO.
The actual interpreter is exercised by the existing CI setup-python job.
"""
import builtins
import functools
import importlib.util
import io
import os
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch
from scripts import source_group_catalog_cache as cache


def fresh_reader_boundary():
    spec = importlib.util.spec_from_file_location('_cbr_pathlib_boundary_test', cache.__file__)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def synthetic_definition(module_name, origin=None):
    # Copy only an existing native stdlib function object; do not execute it or
    # downloaded source. Its genuine code filename is the provenance control.
    native = Path.read_bytes
    value = types.FunctionType(native.__code__, native.__globals__, native.__name__)
    value.__module__ = module_name
    owner = type('SyntheticPathOwner', (), {'__module__': module_name, 'read_bytes': value})
    module = types.ModuleType(module_name)
    module.__spec__ = types.SimpleNamespace(origin=origin or native.__code__.co_filename)
    module.SyntheticPathOwner = owner
    return module, owner, value


class SourceGroupPathlibCompatibility(unittest.TestCase):
    def test_current_native_standard_library_is_accepted(self):
        boundary = fresh_reader_boundary()
        self.assertTrue(boundary._BASE_VALID)
        self.assertTrue(boundary._standard_io())
        self.assertTrue(all(boundary._stdlib_path_definition(owner, value)
                            for owner, name, value in boundary._PATH_MRO_BASE))

    def test_exact_cpython_definition_modules_are_accepted_synthetic(self):
        for name in ('pathlib', 'pathlib._local', 'pathlib._abc'):
            module, owner, value = synthetic_definition(name)
            with self.subTest(module=name), patch.dict(sys.modules, {name: module}):
                self.assertTrue(cache._stdlib_path_definition(owner, value))

    def test_public_class_reexport_need_not_match_definition_module_synthetic(self):
        for name in ('pathlib._local', 'pathlib._abc'):
            module, owner, value = synthetic_definition(name)
            owner.__module__ = 'pathlib'
            with self.subTest(module=name), patch.dict(sys.modules, {name: module}):
                self.assertTrue(cache._stdlib_path_definition(owner, value))

    def test_prefix_lookalike_or_external_module_is_not_trusted(self):
        for name in ('pathlib.fake', 'pathlib._local.fake', 'pathlib._abc.fake',
                     'pathlibevil', 'test_reader_overlay'):
            module, owner, value = synthetic_definition(name)
            with self.subTest(module=name), patch.dict(sys.modules, {name: module}):
                self.assertFalse(cache._stdlib_path_definition(owner, value))

    def test_stdlib_named_module_outside_stdlib_is_rejected(self):
        module, owner, value = synthetic_definition('pathlib._abc', __file__)
        with patch.dict(sys.modules, {'pathlib._abc': module}):
            self.assertFalse(cache._stdlib_path_definition(owner, value))

    def test_forged_module_string_does_not_authenticate_external_code(self):
        original = Path.read_bytes
        @functools.wraps(original)
        def wrapped(self):
            return original(self)
        # wraps copies __module__, but this wrapper's code is in this test file.
        with patch.object(Path, 'read_bytes', wrapped):
            boundary = fresh_reader_boundary()
            self.assertFalse(boundary._BASE_VALID)
            self.assertFalse(boundary._standard_io())

    def test_noncanonical_owner_or_missing_origin_is_rejected(self):
        module, owner, value = synthetic_definition('pathlib._abc')
        with patch.dict(sys.modules, {'pathlib._abc': module}):
            module.SyntheticPathOwner = object()
            self.assertFalse(cache._stdlib_path_definition(owner, value))
            module.SyntheticPathOwner = owner
            module.__spec__ = None
            self.assertFalse(cache._stdlib_path_definition(owner, value))

    def test_post_import_path_wrappers_still_rejected(self):
        boundary = fresh_reader_boundary()
        for name in cache._METHODS:
            original = getattr(Path, name)
            @functools.wraps(original)
            def wrapped(*args, __original=original, **kwargs):
                return __original(*args, **kwargs)
            with self.subTest(method=name), patch.object(Path, name, wrapped):
                self.assertFalse(boundary._standard_io())
        self.assertTrue(boundary._standard_io())

    def test_mro_delegate_replacement_is_rejected_without_top_level_change(self):
        boundary = fresh_reader_boundary()
        class Delegate:
            def read_text(self):
                return 'original'
        original = Delegate.__dict__['read_text']
        top_level = Path.read_text
        extra = boundary._PATH_MRO_BASE + ((Delegate, 'read_text', original),)
        # Synthetic MRO row isolates the inherited delegate identity check on
        # 3.12; 3.13's real PathBase row is captured without a test override.
        with patch.object(boundary, '_PATH_MRO_BASE', extra):
            self.assertTrue(boundary._standard_io())
            with patch.object(Delegate, 'read_text', lambda self: 'changed'):
                self.assertIs(Path.read_text, top_level)
                self.assertFalse(boundary._standard_io())
            with patch.object(Delegate, 'read_text'):
                self.assertFalse(boundary._standard_io())
        self.assertTrue(boundary._standard_io())

    def test_real_inherited_delegate_identity_when_present(self):
        boundary = fresh_reader_boundary()
        rows = [(owner, name, value) for owner, name, value in boundary._PATH_MRO_BASE
                if owner is not Path and name == 'read_text']
        if not rows:
            self.skipTest('Native runtime has no separate inherited read_text delegate')
        owner, name, value = rows[0]
        top_level = Path.read_text
        with patch.object(owner, name, lambda *a, **k: 'changed'):
            self.assertIs(Path.read_text, top_level)
            self.assertFalse(boundary._standard_io())

    def test_post_import_io_replacements_still_rejected(self):
        boundary = fresh_reader_boundary()
        for owner, name in ((io, 'open'), (builtins, 'open'), (os, 'stat'),
                            (os, 'scandir'), (os, 'listdir')):
            original = getattr(owner, name)
            @functools.wraps(original)
            def wrapped(*args, __original=original, **kwargs):
                return __original(*args, **kwargs)
            with self.subTest(owner=owner.__name__, method=name), patch.object(owner, name, wrapped):
                self.assertFalse(boundary._standard_io())
        self.assertTrue(boundary._standard_io())


if __name__ == '__main__':
    unittest.main()
