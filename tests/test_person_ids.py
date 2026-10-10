import unittest
from unittest.mock import patch
from scripts.person_ids import allocate_person_id, allocate_child_id, valid_person_id


class PersonIdTests(unittest.TestCase):
    def test_old_and_opaque_ids_are_valid(self):
        self.assertTrue(valid_person_id('cbr-p000001'))
        self.assertTrue(valid_person_id('cbr-p-a7k2_m9x4_q6n8'))
        for value in ('cbr-p00001', 'cbr-p-A7k2_m9x4_q6n8', None):
            self.assertFalse(valid_person_id(value))

    def test_collision_is_retried(self):
        with patch('scripts.person_ids.secrets.choice', side_effect=list('a'*9 + 'b'*9)):
            self.assertEqual(allocate_person_id({'aaa_aaa_aaa-A'}), 'bbb_bbb_bbb-')

    def test_family_child_generation_and_reserved_branch(self):
        self.assertTrue(valid_person_id('abc_def_123-AB'))
        self.assertFalse(valid_person_id('abc_def_123-ab'))
        self.assertEqual(allocate_child_id('abc_def_123-', {'abc_def_123-AA'}), 'abc_def_123-B')
        self.assertEqual(allocate_child_id('abc_def_123-A', set()), 'abc_def_123-AA')
        with self.assertRaises(ValueError):
            allocate_child_id('cbr-p000001', set())
