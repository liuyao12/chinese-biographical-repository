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
