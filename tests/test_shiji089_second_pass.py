# coding: utf-8
import json
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
class ZhangerIdentityTests(unittest.TestCase):
    def paragraph(self, number, ending):
        data = json.loads((ROOT / f'corpus/shiji/{number}.json').read_text())
        return next(p for p in data['paragraphs'] if p['id'].endswith(':'+ending))
    def test_jingxing_hanxin_identity_preserves_capture_death_difference(self):
        local=self.paragraph('089','p023'); parallel=self.paragraph('092','p010')
        ids={m['person_id'] for p in [local,parallel] for m in p['mentions'] if m['surface']=='韓信'}
        self.assertEqual(ids,{'ofc_8ei_jb7'})
        self.assertIn('追殺趙王歇襄國',local['text'])
        self.assertIn('禽趙王歇',parallel['text'])
    def test_wuji_glyph_and_jizha_title_are_not_rewritten(self):
        p=self.paragraph('089','p001')
        self.assertTrue(any(m['surface']=='魏公子毋忌' and m['person_id']=='h8u_hld_5su' for m in p['mentions']))
        p=self.paragraph('089','p030')
        self.assertTrue(any(m['surface']=='延陵季子' and m['person_id']=='5dm_e40_rqh_AAAAAAAAAAAAAAAAAAD' for m in p['mentions']))
        self.assertIn('大伯',p['text'])
        self.assertIn('季札封於延陵，故號曰延陵季子',self.paragraph('031','p008')['text'])
