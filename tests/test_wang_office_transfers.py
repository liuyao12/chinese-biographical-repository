# coding: utf-8
import copy
import json
import unittest
from pathlib import Path
from scripts.office_transfers import office_transfer_valid
from scripts.current_office_death import current_office_death_valid
from scripts.unassumed_appointments import unassumed_appointment_valid

ROOT = Path(__file__).resolve().parents[1]
def read(path):
    return json.loads((ROOT / path).read_text())

class WangOfficeTransfers(unittest.TestCase):
    def setUp(self):
        self.chapters = {stem: read('corpus/jinshu/076-' + stem + '.json')
                         for stem in ['wangbin', 'wangleng', 'wangbiaozhi']}
        self.paragraphs = {p['id']: (c['id'], p) for c in self.chapters.values() for p in c['paragraphs']}
        self.mentions = {m['id']: (c['id'], p['id'], m) for c in self.chapters.values()
                         for p in c['paragraphs'] for m in p['mentions']}
        self.holdings = [h for stem in self.chapters for h in read('corpus/jinshu/076-' + stem + '-titles.json')['holdings']]
        self.transfers = [h for h in self.holdings if h['mode'] == 'transfer']

    def test_eleven_office_transfers_keep_source_phrases_and_unknown_years(self):
        self.assertEqual(len(self.transfers), 11)
        for h in self.transfers:
            self.assertTrue(office_transfer_valid(h, self.paragraphs, self.mentions), h['id'])
            self.assertIsNone(h['effective_period']['start']['date_expression'])
            self.assertNotIn('normalized_date', h['effective_period']['start'])

    def test_joint_transfer_cannot_manufacture_a_separate_source_phrase(self):
        h = copy.deepcopy(next(h for h in self.transfers if h['title'] == '江州刺史'))
        self.assertEqual(h['office_transfer_basis']['source_term'], '遷前將軍、江州刺史')
        h['office_transfer_basis']['source_term'] = '遷江州刺史'
        h['office_transfer_basis']['titles'] = ['江州刺史']
        self.assertFalse(office_transfer_valid(h, self.paragraphs, self.mentions))

    def test_transfer_cannot_change_recipient_or_replace_royal_transfer_basis(self):
        h = copy.deepcopy(self.transfers[0])
        h['person_id'] = 'someone-else'
        self.assertFalse(office_transfer_valid(h, self.paragraphs, self.mentions))
        h = copy.deepcopy(self.transfers[0])
        h['kind'] = 'royal_rank'
        self.assertFalse(office_transfer_valid(h, self.paragraphs, self.mentions))

    def test_local_zu_guan_ends_only_the_last_named_office_without_inventing_year(self):
        h = next(h for h in self.holdings if h['title'] == '尚書右僕射')
        self.assertTrue(current_office_death_valid(h, self.paragraphs, self.mentions))
        self.assertIsNone(h['effective_period']['end']['date_expression'])
        other = copy.deepcopy(next(h for h in self.holdings if h['title'] == '關內侯'))
        other['end_basis'] = copy.deepcopy(h['end_basis'])
        other['effective_period']['end'] = copy.deepcopy(h['effective_period']['end'])
        self.assertFalse(current_office_death_valid(other, self.paragraphs, self.mentions))
        self.assertEqual(next(h for h in self.holdings if h['title'] == '度支尚書')['effective_period']['end']['status'], 'unknown')

    def test_five_unassumed_appointments_are_not_held_offices(self):
        proposals = [(c, p) for c in self.chapters.values() for p in c['annotation'].get('title_proposals', [])]
        self.assertEqual(len(proposals), 5)
        for c, p in proposals:
            self.assertTrue(unassumed_appointment_valid(p, c), p['id'])
        records = [h for h in self.holdings if h['person_id'] == '7r6_k52_qji_ABDBB' and h['title'] == '尚書僕射']
        self.assertEqual(len(records), 1)
        self.assertTrue(records[0]['attestations'][0]['paragraph_id'].endswith('line075'))
        self.assertFalse(any(h['title'] == '義興內史' and h['person_id'] == '7r6_k52_qji_ABDB' for h in self.holdings))
        self.assertFalse(any(h['title'] in ['儀同三司', '光祿大夫'] and h['person_id'] == '7r6_k52_qji_ABDBB'
                             and h['mode'] in ['grant', 'transfer', 'demotion'] for h in self.holdings))
        self.assertTrue(any(h['title'] == '光祿大夫' and h['person_id'] != '7r6_k52_qji_ABDBB' for h in self.holdings))

    def test_source_eight_years_is_not_a_calendar_range_or_second_office_duration(self):
        h = next(h for h in self.holdings if h['title'] == '會稽內史' and h['person_id'] == '7r6_k52_qji_ABDBB')
        self.assertEqual(h['reported_duration']['value'], 8)
        self.assertEqual(h['reported_duration']['source_term'], '居郡八年')
        self.assertNotIn('reported_duration', next(h for h in self.holdings if h['title'] == '鎮軍將軍'))

if __name__ == '__main__':
    unittest.main()
