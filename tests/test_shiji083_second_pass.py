import json
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

class LuZouSecondPassTests(unittest.TestCase):
    def chapter(self):
        return json.loads((ROOT / 'corpus/shiji/083.json').read_text())

    def test_speakers_named_sheng_remain_distinct(self):
        c = self.chapter()
        p3 = c['paragraphs'][2]
        p15 = c['paragraphs'][14]
        self.assertEqual({m['person_id'] for m in p3['mentions'] if m['surface'] == '勝'}, {'03v_bhv_img'})
        self.assertEqual({m['person_id'] for m in p15['mentions'] if m['surface'] == '勝'}, {'fo7_9ev_cht'})
        self.assertNotEqual(next(m['person_id'] for m in p3['mentions'] if m['surface'] == '勝'), next(m['person_id'] for m in p15['mentions'] if m['surface'] == '勝'))

    def test_qin_king_and_letter_recipient_keep_separate_scope(self):
        c = self.chapter()
        p2 = c['paragraphs'][1]
        self.assertEqual({m['person_id'] for m in p2['mentions'] if m['surface'] in ('秦王', '秦昭王')}, {'ao3_0fy_d45'})
        self.assertEqual({m['person_id'] for m in p2['mentions'] if m['surface'] == '白起'}, {'2bk_fz6_icl'})
        p16 = c['paragraphs'][15]
        self.assertEqual({m['person_id'] for m in p16['mentions'] if m['surface'] == '大王'}, {'yqp_nlb_p1p_ACG'})
        self.assertEqual({m['person_id'] for m in p16['mentions'] if m['surface'] == '昭王'}, {'ao3_0fy_d45'})

    def test_unidentified_yan_king_does_not_gain_named_identity(self):
        c = self.chapter()
        p12 = c['paragraphs'][11]
        self.assertEqual({m['person_id'] for m in p12['mentions'] if m['surface'] == '燕王'}, {'nhk_xgq_7qk'})
        self.assertEqual({m['person_id'] for m in p12['mentions'] if m['surface'] == '栗腹'}, {'fo2_the_x22'})

    def test_liang_court_and_lu_ruler_have_specific_parallel_context(self):
        c = self.chapter()
        p15 = c['paragraphs'][14]
        names = {m['surface']:m['person_id'] for m in p15['mentions']}
        self.assertEqual(names['梁孝王'], 'yqp_nlb_p1p_ACG')
        self.assertEqual(names['羊勝'], 'fo7_9ev_cht')
        self.assertEqual(names['公孫詭'], '2bl_b4d_kfg')
        self.assertEqual(names['鄒陽'], '06n_ttw_xgt')
        p13 = c['paragraphs'][12]
        self.assertEqual({m['person_id'] for m in p13['mentions'] if m['surface'] == '魯君'}, {'ngn_suh_k03'})
        self.assertIn('三戰三北', p13['text'])
        parallel = json.loads((ROOT / 'corpus/shiji/086.json').read_text())
        self.assertIn('三敗北', parallel['paragraphs'][0]['text'])
        self.assertIn('曹沫執匕首', parallel['paragraphs'][1]['text'])

    def test_assassination_reference_is_not_changping_king(self):
        c = self.chapter()
        p23 = c['paragraphs'][22]
        self.assertEqual({m['person_id'] for m in p23['mentions'] if m['surface'] == '秦皇帝'}, {'ao3_0fy_d45_AAA'})
        self.assertIn('秦信左右而殺', p23['text'])
        parallel = json.loads((ROOT / 'corpus/shiji/086.json').read_text())['paragraphs'][33]
        self.assertEqual({m['person_id'] for m in parallel['mentions'] if m['surface'] == '秦王'}, {'ao3_0fy_d45_AAA'})
        self.assertEqual({m['person_id'] for m in p23['mentions'] if m['surface'] == '蒙嘉'}, {m['person_id'] for m in parallel['mentions'] if m['surface'] == '中庶子蒙嘉'})
        self.assertIn('未至身', parallel['text'])
        self.assertIn('於是左右既前殺軻', parallel['text'])

    def test_yan_prince_and_unnamed_suqin_patron_are_not_conflated(self):
        c = self.chapter()
        self.assertEqual({m['person_id'] for m in c['paragraphs'][15]['mentions'] if m['surface'] in ('燕丹', '太子')}, {'e3o_2bk_lhm'})
        self.assertEqual({m['person_id'] for m in c['paragraphs'][17]['mentions'] if m['surface'] == '丹'}, {'e3o_2bk_lhm'})
        self.assertEqual({m['person_id'] for m in c['paragraphs'][17]['mentions'] if m['surface'] == '王'}, {'caz_735_cfr'})

    def test_guanyiwu_jailing_and_qi_ruler_keep_event_context(self):
        p = self.chapter()['paragraphs'][12]
        self.assertEqual({m['person_id'] for m in p['mentions'] if m['surface'] in ('管夷吾', '管子')}, {'h1v_8ap_b9y'})
        self.assertEqual({m['person_id'] for m in p['mentions'] if m['surface'] == '桓公'}, {'9w2_c77_53m'})
        self.assertEqual({m['person_id'] for m in p['mentions'] if m['surface'] == '公子糾'}, {'fng_mjp_tdn'})
        self.assertIn('鄉使管子幽囚而不出', p['text'])
        later = self.chapter()['paragraphs'][21]
        self.assertEqual({m['person_id'] for m in later['mentions'] if m['surface'] == '管'}, {'chm_jfj_3y8'})

    def test_three_lords_allusion_retains_literal_child_and_king_scope(self):
        p = self.chapter()['paragraphs'][6]
        expected = {'九侯':'j9n_viq_5o8', '鄂侯':'pzd_z9m_2de', '文王':'y4i_pjk_4gn_A', '紂':'lwx_9yq_ad7', '子':'lse_2ct_dsn'}
        for surface, pid in expected.items():
            self.assertEqual({m['person_id'] for m in p['mentions'] if m['surface']==surface}, {pid})
        self.assertIn('九侯有子而好', p['text'])
        self.assertEqual({m['person_id'] for m in p['mentions'] if m['surface']=='梁王'}, {'nbg_cps_9w9'})

    def test_execution_allusions_do_not_name_unnamed_chu_king(self):
        p = self.chapter()['paragraphs'][16]
        expected = {'李斯':'49g_7az_e4i', '胡亥':'ao3_0fy_d45_AAAA', '箕子':'8a9_tj8_6i7', '比干':'xtq_oi8_w82', '子胥':'g9h_5ih_ug1_A', '楚王':'y9v_xi8_8n3'}
        for surface, pid in expected.items():
            self.assertEqual({m['person_id'] for m in p['mentions'] if m['surface']==surface}, {pid})
        self.assertIn('子胥鴟夷', p['text'])

    def test_service_allusions_keep_distinct_death_accounts(self):
        c = self.chapter()
        p21 = c['paragraphs'][20]
        self.assertEqual({m['person_id'] for m in p21['mentions'] if m['surface']=='商鞅'}, {'2wp_usr_ncd'})
        self.assertEqual({m['person_id'] for m in p21['mentions'] if m['surface']=='大夫種'}, {'gu2_fde_5bw'})
        self.assertIn('而卒車裂之', p21['text'])
        self.assertIn('而卒誅其身', p21['text'])
        p19 = c['paragraphs'][18]
        expected = {'百里奚':'ylb_ttg_8dr','繆公':'y97_huh_vuz_AAAAA','由余':'iig_8e3_qx2','戎人由余':'iig_8e3_qx2'}
        for surface,pid in expected.items():
            self.assertEqual({m['person_id'] for m in p19['mentions'] if m['surface']==surface},{pid})
