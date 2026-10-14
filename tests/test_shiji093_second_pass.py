# coding: utf-8
import json
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

class HanLuIdentityTests(unittest.TestCase):
    def paragraph(self, book, suffix):
        c = json.loads((ROOT / f'corpus/shiji/{book}.json').read_text())
        return next(p for p in c['paragraphs'] if p['id'].endswith(':' + suffix))
    def ids(self, p, surface):
        return {m['person_id'] for m in p['mentions'] if m['surface'] == surface}
    def test_kings_and_two_hanxin_people_stay_distinct(self):
        p = self.paragraph('093', 'p001')
        self.assertEqual(self.ids(p, '韓王信'), {'hm1_rqr_l9u'})
        self.assertEqual(self.ids(p, '橫陽君成'), {'8i3_5vf_iu9'})
        q = self.paragraph('093', 'p003')
        self.assertEqual(self.ids(q, '鄭昌'), {'vxt_uj1_8ym'})
        self.assertEqual(self.ids(q, '韓王昌'), {'vxt_uj1_8ym'})
        self.assertEqual(self.ids(self.paragraph('092', 'p001'), '淮陰侯韓信'), {'ofc_8ei_jb7'})
        self.assertIn('故吳令鄭昌', self.paragraph('007', 'p024')['text'])
    def test_new_huaiwang_is_not_earlier_captive_king(self):
        p = self.paragraph('093', 'p001')
        self.assertEqual(self.ids(p, '項梁'), {'5xt_rg8_7zs_A'})
        self.assertEqual(self.ids(p, '懷王'), {'c2w_s7g_en0_*A'})
        q = self.paragraph('007', 'p006')
        self.assertIn('自懷王入秦不反', q['text'])
        self.assertIn('求楚懷王孫心', q['text'])
        self.assertEqual(self.ids(q, '懷王'), {'c2w_s7g_en0', 'c2w_s7g_en0_*A'})
    def test_baideng_people_and_short_names_use_scoped_evidence(self):
        p = self.paragraph('093', 'p005')
        self.assertEqual(self.ids(p, '冒頓'), {'wjt_htu_081_A'})
        self.assertEqual(self.ids(p, '陳平'), {'i3f_9l9_g53'})
        self.assertIn('白登', self.paragraph('110', 'p012')['text'])
        self.assertIn('高帝用陳平奇計', self.paragraph('056', 'p012')['text'])
        p = self.paragraph('093', 'p008')
        self.assertEqual(self.ids(p, '蕭'), {'xd8_uww_5ok'})
        self.assertEqual(self.ids(p, '曹'), {'37j_16p_7n8'})
        rows = json.loads((ROOT / 'corpus/shiji/093-equivalences.json').read_text())['decisions']
        for key in ['xiao', 'cao']:
            row = next(x for x in rows if x['id'] == 'eq-shiji093-review-' + key)
            self.assertIn('較弱', row['rationale'])
            self.assertFalse(row['human_reviewed'])
