import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class ContextualEmperors(unittest.TestCase):
    def setUp(self):
        c=json.loads((ROOT/'corpus/shiji/103.json').read_text())
        self.ps={p['id'].rsplit(':',1)[-1]:p for p in c['paragraphs']}
    def person(self,para,start):
        return next(m['person_id'] for m in self.ps[para]['mentions'] if m['start']==start)
    def test_prince_and_current_emperor_are_distinct(self):
        self.assertEqual(self.person('p014',40),'yqp_nlb_p1p_ACA')
        self.assertEqual(self.person('p014',45),'yqp_nlb_p1p_AC')
        self.assertEqual(self.person('p015',61),'yqp_nlb_p1p_ACA')
        self.assertEqual(self.person('p015',96),'yqp_nlb_p1p_AC')
    def test_retrospective_after_death_does_not_switch_emperor(self):
        for start in [61,70,97]:self.assertEqual(self.person('p022',start),'yqp_nlb_p1p_ACA')
        self.assertEqual(self.person('p023',6),'yqp_nlb_p1p_ACA')
        self.assertEqual(self.person('p011',22),'yqp_nlb_p1p_ACA')
        for para,start in [('p010',5),('p011',78),('p011',164),('p016',49)]:self.assertEqual(self.person(para,start),'yqp_nlb_p1p_ACAA')
    def test_office_verb_and_place_are_excluded(self):
        for para,start in [('p010',23),('p011',86),('p015',3),('p016',57),('p024',110)]:
            self.assertFalse(any(m['start']<=start<m['end'] and m.get('person_id') for m in self.ps[para]['mentions']))
