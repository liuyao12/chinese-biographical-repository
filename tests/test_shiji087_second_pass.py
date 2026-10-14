import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class LisiEvidenceTests(unittest.TestCase):
    def read(self, suffix, key):
        return json.loads((ROOT / ('corpus/shiji/087-' + suffix + '.json')).read_text())[key]

    def test_qin_king_scopes_distinguish_departure_from_successor(self):
        chapter = json.loads((ROOT / 'corpus/shiji/087.json').read_text())
        paragraphs = {p['id'].rsplit(':', 1)[1]: p for p in chapter['paragraphs']}
        for m in paragraphs['p002']['mentions']:
            if m['surface'] == '秦王':
                self.assertEqual(m['person_id'], 'jik_qff_1cj')
        for key in ['p003', 'p004', 'p009']:
            for m in paragraphs[key]['mentions']:
                if m['surface'] == '秦王':
                    self.assertEqual(m['person_id'], 'ao3_0fy_d45_AAA')
        self.assertTrue(any(m.get('person_id') == 'ao3_0fy_d45_AA' for m in paragraphs['p003']['mentions']))

    def test_custody_and_requested_burial_do_not_become_death(self):
        events = self.read('life-events', 'events')
        self.assertFalse(any(e['person_id'] == 'yad_hp5_rax' and e['evidence'][0]['paragraph_id'].endswith(':p017') for e in events))
        self.assertFalse(any(e['person_id'] == '172_ij7_8yf' for e in events))
        child = next(e for e in events if e['person_id'] == '49g_7az_e4i_B')
        self.assertNotIn('normalized_date', child)
        self.assertIn('夷三族', child['source_term'])
        self.assertNotIn('腰斬', child['source_term'])

    def test_death_year_preserves_source_month_and_precision(self):
        events = self.read('life-events', 'events')
        for pid, year, phrase in [('49g_7az_e4i', 208, '二世二年七月'), ('ao3_0fy_d45_AAA', 210, '其年七月')]:
            event = next(e for e in events if e['person_id'] == pid)
            self.assertEqual(event['date_expression'], phrase)
            date = event['normalized_date']
            self.assertEqual(date['era_year'], year)
            self.assertEqual(date['year'], 1 - year)
            self.assertEqual(date['precision'], 'year')
            self.assertFalse(date['human_reviewed'])
            self.assertNotIn('month', date)

    def test_origin_service_and_quoted_legend_keep_distinct_roles(self):
        addresses = self.read('addresses', 'assertions')
        own = [a for a in addresses if a['person_id'] == '49g_7az_e4i']
        self.assertEqual({(a['relation'], a['place']['source_name']) for a in own}, {('biographical_origin', '楚上蔡'), ('death_place', '咸陽市')})
        self.assertFalse(any(a['person_id'] == '172_ij7_8yf' and a['relation'] == 'burial_place' for a in addresses))
        legend = next(a for a in addresses if a['person_id'] == 'z9y_ry1_zee')
        self.assertIn('二世引韓子', legend['interpretation_note'])
        self.assertIsNone(legend['place']['modern_identification'])
