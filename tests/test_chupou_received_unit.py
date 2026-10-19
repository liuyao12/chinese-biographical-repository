# coding: utf-8
import json
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

class ChuPouReceivedUnit(unittest.TestCase):
    def setUp(self):
        self.c = json.loads((ROOT / 'corpus/jinshu/093-chupou.json').read_text())
    def test_all_six_source_paragraphs_keep_received_spans(self):
        self.assertEqual([p['source_position']['first_line'] for p in self.c['paragraphs']], [49, 51, 53, 55, 57, 59])
        self.assertEqual(sum(len(p['mentions']) for p in self.c['paragraphs']), 79)
        for p in self.c['paragraphs']:
            for m in p['mentions']:
                self.assertEqual(p['text'][m['start']:m['end']], m['surface'])
    def test_yonghe_era_does_not_become_gu_he_person_reference(self):
        p = next(p for p in self.c['paragraphs'] if p['source_position']['first_line'] == 55)
        self.assertTrue(p['text'].startswith('永和初'))
        self.assertFalse(any(m['start'] == 1 for m in p['mentions']))
        self.assertTrue(any(m['surface'] == '和' for m in p['mentions']))
    def test_patron_identification_uses_annal_not_title_alone(self):
        unresolved = [m for p in self.c['paragraphs'] for m in p['mentions'] if m['kind'] == 'unresolved']
        self.assertEqual({m['surface'] for m in unresolved}, {'西陽王'})
        self.assertTrue(all(m['person_id'] is None for m in unresolved))
        patron = next(m for p in self.c['paragraphs'] for m in p['mentions'] if m['surface'] == '吳王')
        self.assertEqual(patron['person_id'], 'qpk_4pt_y6r')
        decisions = json.loads((ROOT / 'corpus/jinshu/093-chupou-identities.json').read_text())
        decision = next(d for d in decisions['decisions'] if d['id'] == 'd-jinshu093-chupou-wuwang-yue')
        self.assertEqual(decision['identification_basis']['target_mention_ids'], [patron['id']])
        self.assertTrue(all(r['source_revision'] == 2582704 for r in decision['references']))
        self.assertIn('吳王岳爲琅邪王', decision['references'][1]['quote'])
    def test_variants_remain_source_and_reported_notes_in_separate_layers(self):
        text = '\n'.join(p['text'] for p in self.c['paragraphs'])
        self.assertIn('左將卦', text)
        self.assertIn('督護徐龕', text)
        self.assertIn('李菟', text)
        notes = [n for x in self.c['source']['normalization']['excerpts'] for n in x.get('removed_digital_editorial_notes', [])]
        self.assertTrue(any('王龕' in n['text'] for n in notes))
        self.assertTrue(any('李農' in n['text'] for n in notes))
        self.assertTrue(all(n['text_layer'] == 'modern_digital_apparatus' and n['independently_verified'] is False for n in notes))
if __name__ == '__main__':
    unittest.main()
