# coding: utf-8
import copy
import json
import unittest
from pathlib import Path
from scripts.unassumed_appointments import unassumed_appointment_valid

ROOT = Path(__file__).resolve().parents[1]


class WangOfficeInventory(unittest.TestCase):
    def setUp(self):
        self.song = json.loads((ROOT / 'corpus/songshu/066.json').read_text())
        self.qi = json.loads((ROOT / 'corpus/nanqishu/032.json').read_text())
        self.song_h = json.loads((ROOT / 'corpus/songshu/066-titles.json').read_text())['holdings']
        self.qi_h = json.loads((ROOT / 'corpus/nanqishu/032-titles.json').read_text())['holdings']

    def test_source_refusals_all_validate_and_do_not_become_actual_taizi_shaofu(self):
        for c in [self.song, self.qi]:
            for p in c['annotation']['title_proposals']:
                self.assertTrue(unassumed_appointment_valid(p, c), p['id'])
        proposals = [p for p in self.song['annotation']['title_proposals'] if p['title'] == '太子少傅']
        self.assertEqual(len(proposals), 1)
        self.assertFalse(any(h['title'] == '太子少傅' for h in self.song_h))
        self.assertIn('context', proposals[0]['evidence'][0])

    def test_prince_in_teacher_role_is_patron_not_second_recipient(self):
        p = next(p for p in self.song['annotation']['title_proposals'] if p['title'] == '廬陵王師')
        self.assertTrue(unassumed_appointment_valid(p, self.song))
        bad = copy.deepcopy(p)
        bad.pop('patron_person_mention_ids')
        self.assertFalse(unassumed_appointment_valid(bad, self.song))
        bad = copy.deepcopy(p)
        bad['patron_person_mention_ids'] = [p['person_mention_id']]
        self.assertFalse(unassumed_appointment_valid(bad, self.song))
        self.assertTrue(any(h['title'] == '江夏王師' and h['mode'] == 'grant' for h in self.song_h))

    def test_later_actual_appointment_is_distinct_from_first_refused_appointment(self):
        p = next(p for p in self.qi['annotation']['title_proposals'] if p['title'] == '吏部尚書')
        actual = next(h for h in self.qi_h if h['title'] == '吏部尚書' and h['mode'] == 'grant')
        self.assertGreater(actual['attestations'][0]['start'], p['role_anchor']['end'])
        self.assertNotEqual(actual['id'], p['id'])
        self.assertEqual(actual['effective_period']['end']['status'], 'unknown')

    def test_role_span_cannot_be_changed_or_refusal_dropped(self):
        p = next(p for p in self.qi['annotation']['title_proposals'] if p['title'] == '主簿')
        bad = copy.deepcopy(p)
        bad['role_anchor']['start'] += 1
        self.assertFalse(unassumed_appointment_valid(bad, self.qi))
        bad = copy.deepcopy(p)
        bad['non_assumption_anchor']['surface'] = '就職'
        self.assertFalse(unassumed_appointment_valid(bad, self.qi))

    def test_lunzhi_dismissal_and_later_return_are_separate_periods(self):
        holdings = [h for h in self.qi_h if h['title'] == '侍中' and h['person_id'] == '7r6_k52_qji_ABDABAACAA']
        self.assertEqual(len(holdings), 2)
        ended = [h for h in holdings if h['effective_period']['end']['status'] == 'source_event']
        self.assertEqual(len(ended), 1)
        self.assertEqual(ended[0]['effective_period']['end']['event_type'], 'deposition')
        self.assertIsNone(ended[0]['effective_period']['end']['date_expression'])

    def test_posthumous_gift_is_not_lifetime_service(self):
        h = next(h for h in self.qi_h if h['title'] == '散騎常侍' and h['person_id'] == '7r6_k52_qji_ABDABAACA')
        self.assertEqual(h['mode'], 'posthumous_grant')
        self.assertIn('追贈', h['posthumous_basis']['source_term'])
        self.assertEqual(h['effective_period']['end']['status'], 'unknown')


if __name__ == '__main__':
    unittest.main()
