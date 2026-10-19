# coding: utf-8
import copy
import json
import unittest
from pathlib import Path
from scripts.chuji_parentage import chuji_parentage_valid

ROOT = Path(__file__).resolve().parents[1]


class ChujiParentage(unittest.TestCase):
    def setUp(self):
        chapter = json.loads((ROOT / 'corpus/nanqishu/032.json').read_text())
        self.paragraphs = {p['id']: (chapter['id'], p)
                           for p in chapter['paragraphs']}
        self.relations = json.loads(
            (ROOT / 'corpus/nanqishu/032-assertions.json').read_text())['assertions']
        self.a = next(a for a in self.relations if a['predicate'] == 'adoptive_father')

    def valid(self, a=None, relations=None):
        return chuji_parentage_valid(a or self.a, self.paragraphs,
                                     relations or self.relations)

    def test_explicit_chuji_retains_different_birth_father(self):
        self.assertTrue(self.valid())
        father = next(a for a in self.relations if a['id'] ==
                      self.a['qualifiers']['biological_father_assertion_id'])
        self.assertNotEqual(father['object_person_id'], self.a['object_person_id'])

    def test_uncle_alone_cannot_establish_adoption(self):
        a = copy.deepcopy(self.a)
        a['qualifiers']['source_term'] = '伯父秀才粲之'
        self.assertFalse(self.valid(a))

    def test_wrong_person_and_detached_anchors_are_rejected(self):
        for field, value in [('object_person_id', self.a['subject_person_id']),
                             ('subject_person_id', self.a['object_person_id'])]:
            a = copy.deepcopy(self.a)
            a[field] = value
            self.assertFalse(self.valid(a))
        a = copy.deepcopy(self.a)
        a['evidence'][0]['object_person_mention_id'] = 'missing'
        self.assertFalse(self.valid(a))

    def test_absent_or_overwritten_biological_father_is_rejected(self):
        key = self.a['qualifiers']['biological_father_assertion_id']
        self.assertFalse(self.valid(relations=[r for r in self.relations if r['id'] != key]))
        relations = copy.deepcopy(self.relations)
        next(r for r in relations if r['id'] == key)['object_person_id'] = self.a['object_person_id']
        self.assertFalse(self.valid(relations=relations))

    def test_unrelated_uncle_evidence_and_legal_inference_are_rejected(self):
        a = copy.deepcopy(self.a)
        a['qualifiers']['paternal_uncle_assertion_id'] = a['qualifiers']['biological_father_assertion_id']
        self.assertFalse(self.valid(a))
        a = copy.deepcopy(self.a)
        a['qualifiers']['modern_legal_status'] = 'established'
        self.assertFalse(self.valid(a))


if __name__ == '__main__':
    unittest.main()
