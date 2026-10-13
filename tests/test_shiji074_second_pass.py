import copy
import json
import unittest
from pathlib import Path
from scripts.validate_corpus import reported_appointment_count_valid

ROOT = Path(__file__).resolve().parents[1]


class MengXunEvidenceTests(unittest.TestCase):
    def test_repeated_appointments_are_not_duration_or_fabricated_intervals(self):
        titles = json.loads((ROOT / 'corpus/shiji/074-titles.json').read_text())['holdings']
        holding = next(h for h in titles if h['id'] == 'th-shiji074-006')
        count = holding['reported_appointment_count']
        self.assertEqual(count['value'], 3)
        self.assertTrue(reported_appointment_count_valid(count, holding['title']))
        self.assertNotIn('reported_duration', holding)
        for boundary in ('start', 'end'):
            self.assertEqual(holding['effective_period'][boundary]['status'], 'unknown')
        for field, value in [('value', True), ('value', 4), ('unit', 'title_year'),
                             ('source_number', None), ('source_term', '三為蘭陵令')]:
            altered = copy.deepcopy(count)
            altered[field] = value
            self.assertFalse(reported_appointment_count_valid(altered, holding['title']))
        altered = copy.deepcopy(count)
        altered['evidence'][0]['quote'] = 'synthetic fixture without appointment statement'
        self.assertFalse(reported_appointment_count_valid(altered, holding['title']))

    def test_burial_and_death_do_not_invent_birthplace_or_year(self):
        addresses = json.loads((ROOT / 'corpus/shiji/074-addresses.json').read_text())['assertions']
        own = [a for a in addresses if a['person_id'] == 'wuo_ghc_ajx']
        self.assertFalse(any(a['relation'] in ('birth_place', 'death_place') for a in own))
        events = json.loads((ROOT / 'corpus/shiji/074-life-events.json').read_text())['events']
        death = next(e for e in events if e['person_id'] == 'wuo_ghc_ajx')
        self.assertIsNone(death['date_expression'])
        self.assertNotIn('normalized_date', death)
