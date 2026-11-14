# coding: utf-8
import copy
import json
import unittest
from pathlib import Path
from scripts.age_context import age_context_valid

ROOT = Path(__file__).resolve().parents[1]

class SourceAgeContext(unittest.TestCase):
    def setUp(self):
        self.chapter = json.loads((ROOT / 'corpus/jinshu/076-wangbiaozhi.json').read_text())
        self.ages = {a['value']: a for a in self.chapter['annotation']['age_assertions']}
        self.events = {e['id']: e for e in json.loads((ROOT / 'corpus/jinshu/076-wangbiaozhi-life-events.json').read_text())['events']}

    def test_twenty_is_lifetime_age_and_seventy_three_links_actual_death(self):
        self.assertEqual(self.ages[20]['age_context'], {'kind': 'during_life'})
        age = self.ages[73]
        self.assertTrue(age_context_valid(age, self.events))
        self.assertEqual(self.events[age['age_context']['life_event_id']]['normalized_date']['year'], 377)
        self.assertIsNone(age['birth_year'])

    def test_lifetime_age_cannot_be_attached_to_a_later_death_paragraph(self):
        age = copy.deepcopy(self.ages[20])
        age['age_context'] = copy.deepcopy(self.ages[73]['age_context'])
        self.assertFalse(age_context_valid(age, self.events))

    def test_another_person_or_changed_quote_cannot_supply_death_age(self):
        age = copy.deepcopy(self.ages[73])
        age['person_id'] = 'other-person'
        self.assertFalse(age_context_valid(age, self.events))
        age = copy.deepcopy(self.ages[73])
        age['evidence'][0]['quote'] = '別段報齡'
        self.assertFalse(age_context_valid(age, self.events))

    def test_missing_event_and_birth_event_are_not_death_anchors(self):
        age = copy.deepcopy(self.ages[73])
        self.assertFalse(age_context_valid(age, {}))
        events = copy.deepcopy(self.events)
        events[age['age_context']['life_event_id']]['event_type'] = 'birth'
        self.assertFalse(age_context_valid(age, events))
        self.assertFalse(age_context_valid(dict(age_context={'kind': 'during_life', 'life_event_id': 'x'}), events))

    def test_over_ten_is_open_bound_and_cannot_supply_a_birth_year(self):
        age = self.ages[None]
        self.assertEqual(age['source_term'], '年出十歲')
        self.assertEqual(age['bounds'], {'lower': 10, 'lower_inclusive': False, 'upper': None, 'upper_inclusive': None})
        self.assertIsNone(age['birth_year'])
        self.assertNotIn('normalized_date', age)

if __name__ == '__main__':
    unittest.main()
