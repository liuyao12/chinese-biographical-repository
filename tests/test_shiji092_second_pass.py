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

    def test_chenping_uses_the_same_yunmeng_arrest_account(self):
        p = self.paragraph('092', 'p023')
        self.assertEqual(self.ids(p, '陳平'), {'i3f_9l9_g53'})
        q = self.paragraph('056', 'p011')
        self.assertIn('僞遊雲夢', q['text'])
        self.assertIn('赦信以爲淮陰侯', q['text'])

    def test_jiang_guan_keep_distinct_people_and_temporal_evidence(self):
        p = self.paragraph('092', 'p024')
        self.assertEqual(self.ids(p, '絳'), {'koy_6jg_gcc'})
        self.assertEqual(self.ids(p, '灌'), {'sj9_pfu_fwh'})
        self.assertEqual(self.ids(p, '樊將軍噲'), {'b1r_inb_fts'})
        self.assertIn('號絳侯', self.paragraph('057', 'p003')['text'])
        q = self.paragraph('057', 'p011')
        self.assertIn('孝文帝十一年卒', q['text'])
        self.assertIn('子勝之代侯', q['text'])
        self.assertIn('潁陰侯灌嬰', self.paragraph('095', 'p022')['text'])
        records = json.loads((ROOT / 'corpus/shiji/092-equivalences.json').read_text())['decisions']
        guan = next(x for x in records if x['id'] == 'eq-shiji092-review-guanying')
        self.assertEqual(guan['status'], 'contextual_provisional')
        self.assertIn('較弱', guan['rationale'])
        self.assertFalse(guan['human_reviewed'])

    def test_zhangliang_grant_and_julu_dispute_keep_parallel_accounts(self):
        p = self.paragraph('092', 'p016')
        self.assertEqual(self.ids(p, '張良'), {'ea5_zvr_hlp'})
        self.assertIn('語在淮陰事中', self.paragraph('055', 'p016')['text'])
        p = self.paragraph('092', 'p019')
        self.assertEqual(self.ids(p, '張黶'), {'h1w_580_5oa'})
        self.assertEqual(self.ids(p, '陳澤'), {'hnx_2zc_ixj'})
        q = self.paragraph('089', 'p017')
        self.assertIn('張耳不信，以爲殺之', q['text'])
        self.assertIn('皆沒不出', q['text'])

    def test_yue_quotation_identity_does_not_erase_death_and_departure_difference(self):
        p = self.paragraph('092', 'p019')
        self.assertEqual(self.ids(p, '大夫種'), {'gu2_fde_5bw'})
        self.assertEqual(self.ids(p, '范蠡'), {'yhm_h9f_8p0'})
        self.assertEqual(self.ids(p, '句踐'), {'i7a_22p_qda'})
        self.assertIn('身死亡', p['text'])
        self.assertIn('種遂自殺', self.paragraph('041', 'p013')['text'])
        self.assertIn('范蠡浮海出齊', self.paragraph('041', 'p020')['text'])
        self.assertIn('卒老死于陶', self.paragraph('041', 'p027')['text'])
        rows = json.loads((ROOT / 'corpus/shiji/092-equivalences.json').read_text())['decisions']
        decision = next(x for x in rows if x['id'] == 'eq-shiji092-review-fanli')
        self.assertIn('同案被殺', decision['rationale'])
        self.assertFalse(decision['human_reviewed'])

    def test_prince_is_lvhou_son_and_baili_variant_keeps_received_glyph(self):
        p = self.paragraph('092', 'p025')
        self.assertEqual(self.ids(p, '太子'), {'yqp_nlb_p1p_AA'})
        self.assertIn('生孝惠帝', self.paragraph('009', 'p001')['text'])
        p = self.paragraph('092', 'p012')
        self.assertEqual(self.ids(p, '百里奚'), {'ylb_ttg_8dr'})
        self.assertIn('虞君不用子，故亡', self.paragraph('005', 'p022')['text'])
        self.assertIn('百里傒', self.paragraph('005', 'p022')['text'])

    def test_ancient_allusions_and_zhou_founders_have_scoped_identities(self):
        p = self.paragraph('092', 'p020')
        self.assertEqual(self.ids(p, '舜'), {'ddb_l4j_4j2'})
        self.assertEqual(self.ids(p, '禹'), {'6ip_dr3_fbl'})
        self.assertEqual(self.ids(p, '孟賁'), {'dwv_5hn_680'})
        self.assertEqual(self.ids(self.paragraph('092', 'p026'), '堯'), {'oho_r3f_c6y'})
        p = self.paragraph('092', 'p027')
        self.assertEqual(self.ids(p, '周'), {'y4i_pjk_4gn_AD'})
        self.assertEqual(self.ids(p, '召'), {'7m7_qvm_4oj'})
        self.assertEqual(self.ids(p, '太公'), {'1g3_02y_oor'})
        self.assertIn('太公望呂尚', self.paragraph('032', 'p001')['text'])
        self.assertIn('召公奭', self.paragraph('034', 'p001')['text'])
        rows = json.loads((ROOT / 'corpus/shiji/092-equivalences.json').read_text())['decisions']
        meng = next(x for x in rows if x['id'] == 'eq-shiji092-review-mengben')
        self.assertIn('比同事件弱', meng['rationale'])
        self.assertFalse(meng['human_reviewed'])

    def test_hanxin_commentary_author_does_not_replace_father_tan(self):
        p = self.paragraph('092', 'p027')
        self.assertEqual(self.ids(p, '太史公'), {'pme_eis_xqi_*A*AAAAA'})
        self.assertEqual(self.ids(self.paragraph('130', 'p004'), '太史公'), {'pme_eis_xqi_*A*AAAA'})
        self.assertIn('余視其母冢', p['text'])
