"""A source-bound local year chain preserves the received stage and exact dates."""
import copy
import json
from pathlib import Path
import unittest
from scripts.validate_corpus import normalized_date_errors

DATA = json.loads((Path(__file__).parent/'fixtures/source-bound-local-era-chain.json').read_text())

class LocalEraChainTests(unittest.TestCase):
    def setUp(self):
        self.chapter = copy.deepcopy(DATA['chapter'])
        self.date = copy.deepcopy(DATA['dates'][0])
    def errors(self):
        return normalized_date_errors(self.date, {self.chapter['id']: self.chapter})
    def test_explicit_fifth_year_after_stage(self):
        self.assertEqual(self.errors(), [])
        self.assertEqual(self.date['year'], 539)
        self.assertEqual(self.date['source_expression'], '五年')
    def test_next_year_binds_its_exact_later_anchor(self):
        self.date = copy.deepcopy(DATA['dates'][1])
        self.assertEqual(self.errors(), [])
        self.assertEqual(self.date['year'], 540)
    def test_wrong_year_rejected(self):
        self.date['year'] += 1
        self.assertTrue(self.errors())
    def test_missing_context_rejected(self):
        del self.date['narrative_era_scope']
        self.assertTrue(self.errors())
    def test_source_metadata_change_rejected(self):
        self.chapter['source']['revision_id'] = 'different'
        self.assertTrue(self.errors())
    def test_paragraph_text_change_rejected(self):
        self.chapter['paragraphs'][4]['text'] += '改'
        self.assertTrue(self.errors())
    def test_other_subject_rejected(self):
        self.date['narrative_era_scope']['subject_person_id'] = 'other'
        self.assertTrue(self.errors())
    def test_wrong_local_antecedent_rejected(self):
        a = self.date['narrative_era_scope']['antecedent_anchor']
        a.update(start=30, end=32, surface='六年')
        self.assertTrue(self.errors())
    def test_quote_anchor_cannot_be_borrowed(self):
        self.date['evidence'][2]['source_quote_anchor']['start'] = 30
        self.assertTrue(self.errors())
    def test_stage_not_first_year(self):
        self.date['source_expression'] = '大同元年'
        self.date['year'] = self.date['era_year'] = 535
        self.assertTrue(self.errors())
    def test_fabricated_image_qualification_rejected(self):
        self.date['narrative_era_scope']['source_metadata']['image_verified'] = True
        self.assertTrue(self.errors())

if __name__ == '__main__':
    unittest.main()
