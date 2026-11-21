import copy
import json
from pathlib import Path
import unittest

from scripts.nanshi019_dialogue import age_anchor, collateral_valid


ROOT = Path(__file__).resolve().parents[1]


class Nanshi019DialogueTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        base = ROOT / 'corpus/nanshi'
        cls.chapter = json.loads((base / '019-dan19.json').read_text())
        cls.ages = cls.chapter['annotation']['age_assertions']
        cls.relations = [a for a in json.loads((base / '019-dan19-assertions.json').read_text())['assertions']
                         if 'nanshi019_role' in a['qualifiers']]
        cls.paragraphs = {p['id']: (cls.chapter['id'], p) for p in cls.chapter['paragraphs']}

    def test_answer_and_recollection_keep_their_sources(self):
        answer, earlier = self.ages
        self.assertEqual([35,29], [a['value'] for a in self.ages])
        self.assertEqual('晦', age_anchor(answer, self.chapter)['surface'])
        self.assertEqual('荀中郎', age_anchor(earlier, self.chapter)['surface'])
        shifted = copy.deepcopy(earlier)
        shifted['person_id'] = answer['person_id']
        self.assertIsNone(age_anchor(shifted, self.chapter))
        shifted = copy.deepcopy(answer)
        shifted.update(source_number='三十三', value=33, source_term='答曰三十三')
        self.assertIsNone(age_anchor(shifted, self.chapter))

    def test_named_junior_and_senior_stay_with_the_clause(self):
        self.assertEqual(3, len(self.relations))
        for assertion in self.relations:
            self.assertTrue(collateral_valid(assertion, self.paragraphs))
            shifted = copy.deepcopy(assertion)
            shifted['subject_person_id'], shifted['object_person_id'] = (
                shifted['object_person_id'], shifted['subject_person_id'])
            self.assertFalse(collateral_valid(shifted, self.paragraphs))
            shifted = copy.deepcopy(assertion)
            shifted['qualifiers']['kinship_structure']['distance'] = 2
            self.assertFalse(collateral_valid(shifted, self.paragraphs))
