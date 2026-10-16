import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class ContextualTitles(unittest.TestCase):
    def setUp(self):
        c=json.loads((ROOT/'corpus/shiji/101.json').read_text())
        self.ps={p['id'].rsplit(':',1)[-1]:p for p in c['paragraphs']}
    def test_prince_in_wen_reign_is_jing(self):
        p=self.ps['p017']; ms={m['start']:m for m in p['mentions']}
        for start in (100,103,159):
            self.assertEqual(ms[start]['surface'],'太子')
            self.assertEqual(ms[start]['person_id'],'yqp_nlb_p1p_ACA')
        for start in (70,83,114,137): self.assertNotIn(start,ms)
    def test_jia_retains_subject_through_death(self):
        ms={m['start']:m for m in self.ps['p018']['mentions']}
        for start in (113,154,188):
            self.assertEqual(ms[start]['person_id'],'yph_dkb_w4w')
            self.assertEqual(ms[start]['surface'],'丞相')
        self.assertIsNone(ms[163].get('person_id'))
        self.assertNotIn(55,ms)
    def test_addressee_and_emperors_do_not_bleed_across_reigns(self):
        ms={m['start']:m for m in self.ps['p020']['mentions']}
        for start in (32,171): self.assertEqual(ms[start]['person_id'],'yqp_nlb_p1p_ACA')
        self.assertEqual(ms[190]['person_id'],'ktk_wbg_wnm')
        self.assertNotIn(24,ms)
        ms={m['start']:m for m in self.ps['p021']['mentions']}
        self.assertEqual(ms[16]['person_id'],'yqp_nlb_p1p_ACAA')
        for start in (21,58): self.assertNotIn(start,ms)
