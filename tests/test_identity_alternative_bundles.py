# coding: utf-8
import copy
import json
import unittest
from pathlib import Path
from scripts.identity_alternatives import identity_alternative_errors, identity_participant_ids
from scripts.person_bundle import bundle, load_catalog
ROOT = Path(__file__).resolve().parents[1]

class IdentityAlternativeBundles(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = load_catalog(ROOT)
        d = json.loads((ROOT / 'corpus/jinshu/093-chupou-identities.json').read_text())
        cls.case = next(d for d in d['decisions'] if d['id'].endswith('regency-addressee'))
    def test_valid_case_preserves_two_distinct_candidates(self):
        self.assertEqual(identity_alternative_errors(self.case, self.catalog[0]), [])
        self.assertEqual(identity_participant_ids(self.case), {'xke_dj3_6ba_AAB', '84i_4jp_gmc'})
        self.assertEqual(self.case['confidence_level'], 'medium')
    def test_unknown_duplicate_empty_or_equated_alternative_is_rejected(self):
        for value in ['unknown-person', self.case['person_id'], []]:
            d = copy.deepcopy(self.case); d['alternatives'][0]['person_id'] = value
            self.assertTrue(identity_alternative_errors(d, self.catalog[0]))
        for key,value in [('status','equivalent'), ('rationale','')]:
            d = copy.deepcopy(self.case); d['alternatives'][0][key] = value
            self.assertTrue(identity_alternative_errors(d, self.catalog[0]))
        d = copy.deepcopy(self.case); d['status'] = 'source_explicit'
        self.assertTrue(identity_alternative_errors(d, self.catalog[0]))
    def test_both_source_bundles_include_case_without_merging_persons(self):
        mid = self.case['identification_basis']['target_mention_ids'][0]
        paragraph = self.case['evidence'][0]['paragraph_id']
        queen, emperor = self.case['person_id'], self.case['alternatives'][0]['person_id']
        for pid in [queen, emperor]:
            b = bundle(pid, catalog=self.catalog)
            self.assertEqual(b['person_ids'], [pid])
            self.assertIn(self.case['id'], {d['id'] for d in b['identity_decisions']})
            self.assertIn(paragraph, {p['id'] for p in b['passages']})
            self.assertTrue({queen, emperor}.issubset({p['id'] for p in b['persons']}))
            self.assertEqual(mid in {m['id'] for m in b['mentions']}, pid == queen)
            self.assertEqual(b['id_aliases'], [])
if __name__ == '__main__':
    unittest.main()
