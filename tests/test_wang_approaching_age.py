# coding: utf-8
import copy
import json
import unittest
from pathlib import Path
from scripts.age_approximations import age_approximation_errors
from scripts.validate_corpus import normalized_date_errors

ROOT = Path(__file__).resolve().parents[1]


class ApproachingAge(unittest.TestCase):
    def setUp(self):
        self.c = json.loads((ROOT / 'corpus/songshu/066.json').read_text())
        self.a = next(a for a in self.c['annotation']['age_assertions']
                      if a.get('approximation', {}).get('kind') == 'approaching_age')
        self.p = next(p for p in self.c['paragraphs'] if p['source_position']['first_line'] == 20)
        self.refs = self.c['annotation']['person_reference_occurrences']

    def test_approaching90_and_death88_are_independent_source_reports(self):
        self.assertEqual(age_approximation_errors(self.a, self.p, self.refs), [])
        self.assertEqual(self.a['approximation']['target'], 90)
        self.assertIsNone(self.a['value'])
        self.assertIsNone(self.a['birth_year'])
        self.assertEqual(self.a['normalized_date']['year'], 446)
        self.assertEqual(normalized_date_errors(self.a['normalized_date']), [])
        other = next(a for a in self.c['annotation']['age_assertions'] if a['value'] == 88)
        self.assertEqual(other['normalized_date']['year'], 447)
        self.assertNotIn(70, [a['value'] for a in self.c['annotation']['age_assertions']])

    def test_exact_age_strict_bound_and_wrong_speaker_are_rejected(self):
        for key, value in [('value', 90), ('bounds', {'upper': 90}), ('birth_year', 357)]:
            a = copy.deepcopy(self.a)
            a[key] = value
            self.assertTrue(age_approximation_errors(a, self.p, self.refs))
        a = copy.deepcopy(self.a)
        speech_start = a['speaker_scope']['speech_start_anchor']['end']
        addressee = next(r for r in self.refs if r['paragraph_id'] == self.p['id']
                        and r['start'] >= speech_start and r['surface'] == '陛下')
        a['speaker_scope']['speaker_person_reference_id'] = addressee['id']
        self.assertTrue(age_approximation_errors(a, self.p, self.refs))

    def test_plain_regnal_year_requires_explicit_omitted_era_context(self):
        date = copy.deepcopy(self.a['normalized_date'])
        date['relative_year_reference'].pop('kind')
        self.assertTrue(normalized_date_errors(date))


if __name__ == '__main__':
    unittest.main()
