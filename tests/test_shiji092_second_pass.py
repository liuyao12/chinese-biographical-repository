# coding: utf-8
import json
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

class HanxinIdentityTests(unittest.TestCase):
    def paragraph(self, book, suffix):
        c = json.loads((ROOT / f'corpus/shiji/{book}.json').read_text())
        return next(p for p in c['paragraphs'] if p['id'].endswith(':' + suffix))
    def ids(self, paragraph, surface):
        return {m['person_id'] for m in paragraph['mentions'] if m['surface'] == surface}
    def test_three_qin_kings_are_distinct_and_follow_full_titles(self):
        p = self.paragraph('092', 'p006')
        q = self.paragraph('092', 'p008')
        self.assertEqual(self.ids(p, '邯'), {'4jv_qte_5p4'})
        self.assertEqual(self.ids(p, '欣'), {'o8z_o5j_2e8'})
        self.assertEqual(self.ids(p, '翳'), {'3j2_4x7_nzr'})
        self.assertTrue(any(m['person_id'] == 'o8z_o5j_2e8' and '欣' in m['surface'] for m in q['mentions']))
        self.assertTrue(any(m['person_id'] == '3j2_4x7_nzr' and '翳' in m['surface'] for m in q['mentions']))
        self.assertIn('司馬欣為塞王', self.paragraph('007', 'p021')['text'])
        self.assertIn('董翳為翟王', self.paragraph('007', 'p021')['text'])
    def test_xiao_recommendation_uses_explicit_parallel_account(self):
        p = self.paragraph('092', 'p005')
        self.assertEqual(self.ids(p, '蕭何'), {'xd8_uww_5ok'})
        self.assertIn('何進言韓信', self.paragraph('053', 'p004')['text'])
        self.assertIn('語在淮陰侯事中', self.paragraph('053', 'p004')['text'])
    def test_qi_king_guang_is_not_later_qi_king_hanxin(self):
        p = self.paragraph('092', 'p014')
        self.assertEqual(self.ids(p, '齊王田廣'), {'0hs_fg6_1qj_A'})
        self.assertNotEqual(self.ids(p, '齊王田廣'), self.ids(p, '韓信'))
        self.assertIn('田廣', self.paragraph('008', 'p044')['text'])
    def test_wushe_origin_and_longju_death_accounts_keep_source_wording(self):
        p = self.paragraph('092', 'p017')
        self.assertEqual(self.ids(p, '武涉'), {'3la_fcr_q0l'})
        self.assertIn('盱眙人武涉', p['text'])
        self.assertIn('盱臺人武涉', self.paragraph('008', 'p047')['text'])
        p = self.paragraph('092', 'p015')
        self.assertEqual(self.ids(p, '龍且'), {'sr6_5zr_1f3'})
        self.assertIn('騎將灌嬰擊', self.paragraph('008', 'p044')['text'])
        self.assertIn('殺龍且', p['text'])
