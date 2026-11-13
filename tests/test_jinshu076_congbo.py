import copy
import json
import unittest
from pathlib import Path

from scripts.jinshu076_congbo import valid

ROOT = Path(__file__).resolve().parents[1]


class Jinshu076CongboTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        chapter = json.loads((ROOT / 'corpus/jinshu/076-wangbiaozhi.json').read_text())
        cls.paragraphs = {p['id']: (chapter['id'], p) for p in chapter['paragraphs']}
        record = json.loads((ROOT / 'corpus/jinshu/076-wangbiaozhi-assertions.json').read_text())
        cls.assertion = next(a for a in record['assertions']
                             if a['id'] == 'a-jinshu076-wangbiaozhi-congbo-wangdao')

    def test_exact_source_clause_and_generation(self):
        self.assertTrue(valid(self.assertion, self.paragraphs))
        q = self.assertion['qualifiers']
        self.assertEqual(q['source_term'], '從伯導')
        self.assertEqual(q['kinship_structure']['generation_difference'], -1)
        self.assertIsNone(q['kinship_structure']['distance'])
        self.assertIsNone(q['kinship_structure']['common_ancestor_person_id'])

    def test_wrong_subject_object_term_direction_and_invented_ancestor_rejected(self):
        mutations = [
            lambda a: a.update(subject_person_id='7r6_k52_qji_ABAA'),
            lambda a: a.update(object_person_id='7r6_k52_qji_ABDBB'),
            lambda a: a['qualifiers'].update(source_term='從弟導'),
            lambda a: a['qualifiers']['source_clause_binding'].update(surface='從叔導'),
            lambda a: a['qualifiers']['kinship_structure'].update(generation_difference=0),
            lambda a: a['qualifiers']['kinship_structure'].update(common_ancestor_person_id='invented'),
            lambda a: a['evidence'][0].update(subject_person_mention_id='c-jinshu-076-wangbiaozhi:line055:m0038'),
        ]
        for mutate in mutations:
            candidate = copy.deepcopy(self.assertion)
            mutate(candidate)
            self.assertFalse(valid(candidate, self.paragraphs))


if __name__ == '__main__':
    unittest.main()
