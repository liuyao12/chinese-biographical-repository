# coding: utf-8
import copy
import json
import unittest
from pathlib import Path
from scripts.maternal_roles import maternal_role_valid
ROOT = Path(__file__).resolve().parents[1]

class MaternalRoles(unittest.TestCase):
    def setUp(self):
        c = json.loads((ROOT / 'corpus/jinshu/032-chu-suanzi.json').read_text())
        self.ps = {p['id']: (c['id'], p) for p in c['paragraphs']}
        self.rows = [a for a in json.loads((ROOT / 'corpus/jinshu/032-chu-suanzi-assertions.json').read_text())['assertions'] if a['predicate'] == 'maternal_role']
    def test_received_mother_and_two_prior_mothers_remain_non_biological(self):
        self.assertEqual(len(self.rows), 3)
        self.assertTrue(all(maternal_role_valid(a, self.ps) for a in self.rows))
        self.assertEqual([a['qualifiers']['role'] for a in self.rows], ['mother_unspecified', 'prior_mother', 'prior_mother'])
    def test_rejects_invented_birth_or_father(self):
        for key, value in [('biological_mother', True), ('father_person_id', 'xke_dj3_6ba_AA')]:
            a = copy.deepcopy(self.rows[0]); a['qualifiers'][key] = value
            self.assertFalse(maternal_role_valid(a, self.ps))
    def test_rejects_swapped_object_and_relabelled_stepmother(self):
        a = copy.deepcopy(self.rows[1]); a['object_person_id'] = 'mpc_jpz_86r'
        self.assertFalse(maternal_role_valid(a, self.ps))
        a = copy.deepcopy(self.rows[1]); a['qualifiers']['role'] = 'stepmother'
        self.assertFalse(maternal_role_valid(a, self.ps))
