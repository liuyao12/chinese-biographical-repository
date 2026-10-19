# coding: utf-8
import copy
import hashlib
import json
import unittest
from pathlib import Path

from scripts.annal_year_context import annal_regnal_year_valid, annal_year_binding_valid
from scripts.life_event_dates import date_decision_errors, selected_dates
from scripts.validate_corpus import normalized_date_errors, source_age_number

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads((ROOT / path).read_text())


class AnnalYearContext(unittest.TestCase):
    def setUp(self):
        self.chapter = read('corpus/songshu/005.json')
        self.event = read('corpus/songshu/005-life-events.json')['events'][0]
        self.date = self.event['normalized_date']
        self.chapters = {self.chapter['id']: self.chapter}

    def test_annal_year_is_bound_to_raw_section_and_exact_entry(self):
        self.assertEqual(normalized_date_errors(self.date, self.chapters), [])
        self.assertEqual(self.date['year'], 448)
        self.assertEqual(self.event['date_expression'], '秋七月壬午')
        self.assertEqual(self.chapter['paragraphs'][0]['text'], '秋七月壬午，左光祿大夫王敬弘薨。')
        self.assertNotIn('元嘉', self.chapter['paragraphs'][0]['text'])
        self.assertEqual(self.date['precision'], 'year')
        self.assertNotIn('gregorian_date', self.date)

    def test_an_arithmetically_valid_reference_still_requires_registered_source(self):
        self.assertTrue(annal_regnal_year_valid(self.date, source_age_number))
        self.assertTrue(normalized_date_errors(self.date))
        chapter = copy.deepcopy(self.chapter)
        chapter['source']['annal_year_sections'] = []
        self.assertFalse(annal_year_binding_valid(self.date, chapter))
        chapter = copy.deepcopy(self.chapter)
        chapter['source']['revision_id'] += 1
        self.assertFalse(annal_year_binding_valid(self.date, chapter))

    def test_different_line_or_paragraph_cannot_borrow_the_year_section(self):
        for key, value in [('event_source_line', 420), ('event_paragraph_id', 'synthetic:other')]:
            bad = copy.deepcopy(self.date)
            bad['annal_year_reference'][key] = value
            self.assertFalse(annal_regnal_year_valid(bad, source_age_number))
        chapter = copy.deepcopy(self.chapter)
        chapter['paragraphs'][0]['source_position']['first_line'] = 420
        self.assertFalse(annal_year_binding_valid(self.date, chapter))

    def test_wrong_year_or_era_cannot_be_satisfied_by_a_correct_sum(self):
        bad = copy.deepcopy(self.date)
        bad.update(year=449, era_year=449)
        bad['regnal_year_mapping'].update(regnal_year=26, target_regnal_year=26, source_number='二十六')
        self.assertFalse(annal_regnal_year_valid(bad, source_age_number))
        bad = copy.deepcopy(self.date)
        bad['regnal_year_mapping']['era_name'] = '永明'
        self.assertFalse(annal_regnal_year_valid(bad, source_age_number))

    def test_a_rehashed_inserted_year_boundary_is_rejected(self):
        bad = copy.deepcopy(self.date)
        ref = bad['references'][1]
        section = ref['section']
        section['raw_quote'] = section['raw_quote'].replace('五月己卯，', '==元嘉二十六年==五月己卯，')
        # A standalone boundary must also fail, even with adjusted line counts.
        section['raw_quote'] = section['raw_quote'].replace('==元嘉二十六年==五月', '==元嘉二十六年==\n五月')
        section['source_lines'][1] += 1
        section['raw_quote_sha256'] = hashlib.sha256(section['raw_quote'].encode()).hexdigest()
        ref['quote'] = section['raw_quote']
        self.assertFalse(annal_regnal_year_valid(bad, source_age_number))

    def test_changed_original_year_body_and_section_digest_are_rejected(self):
        for change in ['body', 'digest']:
            bad = copy.deepcopy(self.date)
            section = bad['references'][1]['section']
            if change == 'body':
                section['raw_quote'] = section['raw_quote'].replace('二十五年春', '二十六年春')
                section['raw_quote_sha256'] = hashlib.sha256(section['raw_quote'].encode()).hexdigest()
                bad['references'][1]['quote'] = section['raw_quote']
            else:
                section['raw_quote_sha256'] = '0' * 64
            self.assertFalse(annal_regnal_year_valid(bad, source_age_number))

    def test_preference_keeps_both_biographies_and_does_not_move_reported_age(self):
        song = read('corpus/songshu/066-life-events.json')['events'][0]
        south = next(e for e in read('corpus/nanshi/024-life-events.json')['events']
                     if e['person_id'] == self.event['person_id'])
        self.assertEqual([e['normalized_date']['year'] for e in [song, south]], [447, 447])
        decision = read('corpus/songshu/005-date-decisions.json')['decisions'][0]
        events = {e['id']: e for e in [self.event, song, south]}
        self.assertEqual(date_decision_errors(decision, events, [], {self.event['person_id']}), [])
        self.assertEqual(selected_dates(list(events.values()), [decision])[0]['year'], 448)
        ages = read('corpus/songshu/066.json')['annotation']['age_assertions']
        age = next(a for a in ages if a.get('value') == 88)
        self.assertEqual(age['normalized_date']['year'], 447)
        self.assertFalse(any(e['event_type'] == 'birth' for e in events.values()))

    def test_dated_style_is_not_an_appointment_or_a_general_office_end(self):
        holding = read('corpus/songshu/005-titles.json')['holdings'][0]
        self.assertEqual(holding['mode'], 'attestation')
        self.assertEqual(holding['title'], '左光祿大夫')
        self.assertEqual(holding['attestations'][0]['normalized_date']['year'], 448)
        for side in ['start', 'end']:
            self.assertEqual(holding['effective_period'][side]['status'], 'unknown')
            self.assertIsNone(holding['effective_period'][side]['date_expression'])


if __name__ == '__main__':
    unittest.main()
