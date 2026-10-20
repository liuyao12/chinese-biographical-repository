# coding: utf-8
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class BashuEnvoyIdentityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c=json.loads((ROOT/'corpus/shiji/117.json').read_text())
        cls.m={m['id'].split(':')[-1]:m for p in cls.c['paragraphs'] for m in p['mentions']}
        cls.d={x['id']:x for x in json.loads((ROOT/'corpus/shiji/117-identities.json').read_text())['decisions']}
    def test_nanyue_prince_is_not_han_prince(self):
        self.assertEqual(self.m['m032-0100']['person_id'],'bvb_d1z_fd0_*AA')
        d=self.d['d-shiji117-bashu-yingqi']
        self.assertEqual(d['scope'],'cross_chapter')
        self.assertTrue(any(e['quote']=='遣太子嬰齊入宿衛。' for e in d['evidence']))
    def test_missions_do_not_collapse_into_one_envoy(self):
        for mid in ['m032-0174','m032-0197']:
            self.assertEqual(self.m[mid]['person_id'],'a62_lwv_9ui')
        self.assertEqual(self.m['m034-0022']['person_id'],'usb_lgr_ksa')
        self.assertIsNone(self.m['m034-0003']['person_id'])
        d=self.d['d-shiji117-bashu-tangmeng']
        self.assertTrue(any('郎中將' in e['quote']for e in d['evidence']))
        self.assertEqual(self.m['m032-0174']['surface'],'中郎將')
    def test_literary_voice_is_explicitly_not_an_attended_event(self):
        d=self.d['d-shiji117-bashu-xiangru-literary-voice']
        self.assertEqual(d['identification_basis']['source_actor_scope'],'literary_authorial_voice')
        self.assertTrue(d['identification_basis']['historical_event_attendance_not_inferred'])
        for mid in ['m038-0101','m039-0000']:
            self.assertEqual(self.m[mid]['person_id'],'usb_lgr_ksa')
        self.assertIsNone(self.m['m038-0000']['person_id'])
    def test_generic_chanyu_and_unselected_emperor_stay_unresolved(self):
        for mid in ['m032-0055','m038-0031']:
            self.assertIsNone(self.m[mid]['person_id'])
    def test_new_anchors_cover_only_attested_names(self):
        for mid,surface in [('m032-0197','使者'),('m034-0022','信使')]:
            m=self.m[mid];p=next(p for p in self.c['paragraphs']if m in p['mentions'])
            self.assertEqual(p['text'][m['start']:m['end']],surface)
if __name__=='__main__':unittest.main()
