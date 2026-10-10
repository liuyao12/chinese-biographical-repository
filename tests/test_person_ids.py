import unittest
from unittest.mock import patch
from scripts.person_ids import allocate_person_id, allocate_child_id, allocate_descendant_id, valid_person_id, family_path_errors


class PersonIdTests(unittest.TestCase):
    def test_old_and_opaque_ids_are_valid(self):
        self.assertTrue(valid_person_id('cbr-p000001'))
        self.assertTrue(valid_person_id('cbr-p-a7k2_m9x4_q6n8'))
        for value in ('cbr-p00001', 'cbr-p-A7k2_m9x4_q6n8', None):
            self.assertFalse(valid_person_id(value))

    def test_collision_is_retried(self):
        with patch('scripts.person_ids.secrets.choice', side_effect=list('a'*9 + 'b'*9)):
            self.assertEqual(allocate_person_id({'aaa_aaa_aaa_A'}), 'bbb_bbb_bbb')

    def test_family_child_generation_and_reserved_branch(self):
        self.assertTrue(valid_person_id('abc_def_123_AB'))
        self.assertFalse(valid_person_id('abc_def_123ab'))
        self.assertEqual(allocate_child_id('abc_def_123', {'abc_def_123_AA'}), 'abc_def_123_B')
        self.assertEqual(allocate_child_id('abc_def_123_A', set()), 'abc_def_123_AA')
        with self.assertRaises(ValueError):
            allocate_child_id('cbr-p000001', set())

    def test_missing_father_has_star_without_placeholder_person(self):
        child = allocate_descendant_id('abc_def_123', 2, set())
        self.assertEqual(child, 'abc_def_123_*A')
        self.assertTrue(valid_person_id(child))
        self.assertFalse(valid_person_id('abc_def_123_*'))
        self.assertEqual(allocate_descendant_id('abc_def_123', 2, {child}), 'abc_def_123_*B')
        path = {'ancestor_person_id': 'abc_def_123', 'parent_person_id': None,
                'connection': 'grandfather', 'generation_distance': 2,
                'intermediate_person_ids': [None]}
        self.assertEqual(family_path_errors(child, path), [])
        self.assertTrue(family_path_errors('abc_def_123_AA', path))
        self.assertTrue(family_path_errors(child, dict(path, parent_person_id='abc_def_123_A')))
        self.assertEqual(allocate_child_id(child, set()), 'abc_def_123_*AA')
