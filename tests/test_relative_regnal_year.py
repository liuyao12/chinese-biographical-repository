# coding: utf-8
import copy
import json
import unittest
from pathlib import Path
from scripts.relative_regnal_year import relative_regnal_year_valid
from scripts.validate_corpus import normalized_date_errors, source_age_number

ROOT = Path(__file__).resolve().parents[1]


class RelativeRegnalYear(unittest.TestCase):
    def setUp(self):
        self.dates = []
        for f in ['songshu/066', 'nanqishu/032', 'nanshi/024']:
            self.dates += [e['normalized_date'] for e in json.loads(
                (ROOT / ('corpus/' + f + '-life-events.json')).read_text())['events']
                           if 'relative_year_reference' in e.get('normalized_date', {})]

    def test_source_relative_words_preserved_with_numeric_years(self):
        self.assertEqual(sorted(d['year'] for d in self.dates), [447, 447, 484])
        for d in self.dates:
            self.assertTrue(relative_regnal_year_valid(d, source_age_number))
            self.assertEqual(normalized_date_errors(d), [])
            self.assertIn(d['source_expression'], ['明年', '其年'])

    def test_explicit_regnal_year_remains_distinct_from_relative_years(self):
        events = json.loads((ROOT / 'corpus/nanshi/024-life-events.json').read_text())['events']
        date = next(e['normalized_date'] for e in events
                    if e['id'] == 'le-nanshi-024-81-wang-received')
        self.assertEqual(date['source_expression'], '元嘉四年')
        self.assertEqual(date['year'], 427)
        self.assertEqual(normalized_date_errors(date), [])
        self.assertFalse(relative_regnal_year_valid(date, source_age_number))

    def test_wrong_offset_wrong_era_and_missing_antecedent_fail(self):
        for date in self.dates:
            d = copy.deepcopy(date)
            d['regnal_year_mapping']['year_offset'] = 9
            self.assertFalse(relative_regnal_year_valid(d, source_age_number))
            d = copy.deepcopy(date)
            d['regnal_year_mapping']['era_name'] = '錯置年號'
            self.assertFalse(relative_regnal_year_valid(d, source_age_number))
            d = copy.deepcopy(date)
            d['relative_year_reference']['antecedent_expression'] = '九十九年'
            self.assertFalse(relative_regnal_year_valid(d, source_age_number))

    def test_no_backdating_or_reordering_evidence(self):
        d = copy.deepcopy(self.dates[0])
        d['year'] += 1
        self.assertFalse(relative_regnal_year_valid(d, source_age_number))
        d = copy.deepcopy(self.dates[0])
        d['relative_year_reference']['era_evidence_index'] = 2
        self.assertFalse(relative_regnal_year_valid(d, source_age_number))

    def test_age_and_places_remain_source_qualified(self):
        for f, value in [('songshu/066', 88), ('nanqishu/032', 64), ('nanshi/024', 88)]:
            chapter = json.loads((ROOT / ('corpus/' + f + '.json')).read_text())
            age = chapter['annotation']['age_assertions'][0]
            self.assertEqual(age['value'], value)
            self.assertIsNone(age['birth_year'])
            self.assertEqual(age['counting'], 'unspecified_source_age')
            addresses = json.loads((ROOT / ('corpus/' + f + '-addresses.json')).read_text())['assertions']
            for a in addresses:
                self.assertIsNone(a['place']['modern_identification'])
                self.assertNotEqual(a['relation'], 'birth_place')
        qi = json.loads((ROOT / 'corpus/nanqishu/032-life-events.json').read_text())
        lun = next(e for e in qi['events'] if e['id'] == 'le-qi-wang-lunzhi')
        self.assertIsNone(lun['date_expression'])
        self.assertNotIn('normalized_date', lun)


if __name__ == '__main__':
    unittest.main()
