# coding: utf-8
import copy
import json
import unittest
from pathlib import Path
from scripts.title_chronology_preference import title_chronology_preference_valid
from scripts.validate_corpus import normalized_date_errors

ROOT = Path(__file__).resolve().parents[1]


class TitleChronologyPreference(unittest.TestCase):
    def setUp(self):
        self.holdings = {h['id']: h for p in (ROOT / 'corpus').glob('*/*-titles.json')
                         for h in json.loads(p.read_text())['holdings']}
        self.preferred = [h for h in self.holdings.values() if 'chronology_preference' in h]

    def test_two_local_preferences_preserve_all_source_dates(self):
        self.assertEqual(len(self.preferred), 2)
        years = []
        for h in self.preferred:
            self.assertTrue(title_chronology_preference_valid(h, self.holdings))
            candidates = [self.holdings[i] for i in h['chronology_preference']['candidate_holding_ids']]
            years.append(sorted(c['effective_period']['start']['normalized_date']['year'] for c in candidates))
            for c in candidates:
                self.assertEqual(c['effective_period']['end']['status'], 'unknown')
                self.assertEqual(normalized_date_errors(c['effective_period']['start']['normalized_date']), [])
        self.assertEqual(sorted(years), [[478, 479], [479, 480]])

    def test_unknown_candidate_wrong_person_or_other_title_cannot_be_preferred(self):
        h = copy.deepcopy(self.preferred[0])
        h['chronology_preference']['candidate_holding_ids'].append('missing')
        self.assertFalse(title_chronology_preference_valid(h, self.holdings))
        for field, value in [('person_id', 'another-person'), ('title', '無關官職')]:
            holdings = copy.deepcopy(self.holdings)
            alternate_id = self.preferred[0]['chronology_preference']['candidate_holding_ids'][1]
            holdings[alternate_id][field] = value
            self.assertFalse(title_chronology_preference_valid(self.preferred[0], holdings))

    def test_shengming_source_spelling_and_death_year_are_not_rewritten(self):
        h = self.holdings['th-nan-wang-wenzhen']
        self.assertEqual(h['effective_period']['start']['date_expression'], '升明三年')
        self.assertIn('薨', h['evidence'][0]['quote'])
        self.assertEqual(h['effective_period']['start']['normalized_date']['year'], 479)
        self.assertNotEqual(h['effective_period']['start']['normalized_date']['year'], 447)
        self.assertEqual(self.holdings['th-nan-wang-zhennan']['title'], '鎭南將軍')


if __name__ == '__main__':
    unittest.main()
