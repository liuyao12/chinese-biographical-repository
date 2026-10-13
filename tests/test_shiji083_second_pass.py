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
        self.assertEqual({m['person_id'] for m in p15['mentions'] if m['surface'] == '勝'}, {'ssv_spo_859'})
        self.assertNotEqual(next(m['person_id'] for m in p3['mentions'] if m['surface'] == '勝'), next(m['person_id'] for m in p15['mentions'] if m['surface'] == '勝'))

    def test_qin_king_and_letter_recipient_keep_separate_scope(self):
        c = self.chapter()
        p2 = c['paragraphs'][1]
        self.assertEqual({m['person_id'] for m in p2['mentions'] if m['surface'] in ('秦王', '秦昭王')}, {'ao3_0fy_d45'})
        self.assertEqual({m['person_id'] for m in p2['mentions'] if m['surface'] == '白起'}, {'2bk_fz6_icl'})
        p16 = c['paragraphs'][15]
        self.assertEqual({m['person_id'] for m in p16['mentions'] if m['surface'] == '大王'}, {'4qt_ofp_ysv'})
        self.assertEqual({m['person_id'] for m in p16['mentions'] if m['surface'] == '昭王'}, {'ao3_0fy_d45'})

    def test_unidentified_yan_king_does_not_gain_named_identity(self):
        c = self.chapter()
        p12 = c['paragraphs'][11]
        self.assertEqual({m['person_id'] for m in p12['mentions'] if m['surface'] == '燕王'}, {'nhk_xgq_7qk'})
        self.assertEqual({m['person_id'] for m in p12['mentions'] if m['surface'] == '栗腹'}, {'fo2_the_x22'})
