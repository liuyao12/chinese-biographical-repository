# coding: utf-8
import copy
import json
import unittest
from pathlib import Path
from scripts.marriage_termination import marriage_termination_valid

ROOT = Path(__file__).resolve().parents[1]


class MarriageTermination(unittest.TestCase):
    def setUp(self):
        c = json.loads((ROOT / 'corpus/nanshi/024.json').read_text())
        self.paragraphs = {p['id']: (c['id'], p) for p in c['paragraphs']}
        self.a = next(a for a in json.loads((ROOT / 'corpus/nanshi/024-assertions.json').read_text())['assertions']
                      if a['id'] == 'a-nanshi024-cong-marriage')

    def test_marriage_is_retained_with_explicit_undated_divorce(self):
        self.assertTrue(marriage_termination_valid(self.a, self.paragraphs))
        self.assertIsNone(self.a['qualifiers']['marriage_termination']['date'])

    def test_invented_year_or_wrong_spouse_is_rejected(self):
        a = copy.deepcopy(self.a)
        a['qualifiers']['marriage_termination']['date'] = {'year': 510}
        self.assertFalse(marriage_termination_valid(a, self.paragraphs))
        a = copy.deepcopy(self.a)
        a['object_person_id'] = a['subject_person_id']
        self.assertFalse(marriage_termination_valid(a, self.paragraphs))

    def test_unrelated_or_absent_divorce_does_not_terminate_marriage(self):
        paragraphs = copy.deepcopy(self.paragraphs)
        pid = self.a['evidence'][0]['paragraph_id']
        paragraphs[pid][1]['text'] = paragraphs[pid][1]['text'].replace('遂離婚', '未離婚')
        a = copy.deepcopy(self.a)
        a['evidence'][0]['quote'] = paragraphs[pid][1]['text']
        self.assertFalse(marriage_termination_valid(a, paragraphs))
        a = copy.deepcopy(self.a)
        a['qualifiers']['source_term'] = '始興王女繁昌主'
        self.assertFalse(marriage_termination_valid(a, self.paragraphs))


if __name__ == '__main__':
    unittest.main()
