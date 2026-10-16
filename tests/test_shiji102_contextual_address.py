import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class ContextualAddress(unittest.TestCase):
    def setUp(self):
        c=json.loads((ROOT/'corpus/shiji/102.json').read_text())
        self.ps={p['id'].rsplit(':',1)[-1]:p for p in c['paragraphs']}
    def test_biography_audiences_are_specific_wendi(self):
        allms=[m for p in self.ps.values() for m in p['mentions'] if m['surface']=='陛下']
        self.assertEqual(len(allms),8)
        self.assertTrue(all(m['person_id']=='yqp_nlb_p1p_AC' for m in allms))
        for para,start in [('p002',42),('p006',177)]:
            m=next(m for m in self.ps[para]['mentions'] if m['start']==start)
            self.assertEqual(m['person_id'],'yqp_nlb_p1p_AC')
    def test_predecessor_and_addressees_keep_separate_subjects(self):
        for para,start,pid in [('p007',56,'yqp_nlb_p1p_A'),('p007',73,'dq6_ovk_58c'),('p011',273,'rl6_a40_3hj_AA'),('p012',35,'rl6_a40_3hj_AA')]:
            m=next(m for m in self.ps[para]['mentions'] if m['start']==start)
            self.assertEqual(m['person_id'],pid)
    def test_offices_groups_and_verbs_not_marked_as_people(self):
        for para,starts in [('p002',[89,278]),('p003',[33]),('p004',[40]),('p006',[151]),('p009',[21,135]),('p012',[372,427])]:
            for start in starts:
                self.assertFalse(any(m['start']<=start<m['end'] and m.get('person_id') for m in self.ps[para]['mentions']))
