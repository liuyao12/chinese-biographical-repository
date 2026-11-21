import unittest,json
from copy import deepcopy
from pathlib import Path
from scripts.nanshi024_wangyan import errors, ruler_holding, annal_date_valid, proposal_valid
ROOT=Path(__file__).resolve().parents[1]
def read(name):return json.loads((ROOT/name).read_text())
class WangYanCourt(unittest.TestCase):
    def test_prince_official_and_a_declined_post(self):
        ch=read('corpus/nanshi/024-wangyan.json');self.assertFalse(errors(ch,ROOT));rows=read('corpus/nanshi/024-wangyan-titles.json')['holdings'];h=next(h for h in rows if h.get('nanshi024_wangyan_title_reference'));self.assertTrue(ruler_holding(h,ch,ROOT));h['person_id']='i08_s4b_5bb';self.assertFalse(ruler_holding(h,ch,ROOT));p,=ch['annotation']['title_proposals'];self.assertTrue(proposal_valid(p,ch));self.assertNotIn('江州刺史',[h['title']for h in rows]);self.assertNotIn('文獻',[h['title'] for h in rows if h['person_id']=='7r6_k52_qji_ABAAAAEAA']);p['outcome']='accepted';self.assertFalse(proposal_valid(p,ch))
    def test_annal_day_and_son_number(self):
        ch=read('corpus/nanqishu/006-wangyan-jianwu-four.json');ev,=read('corpus/nanqishu/006-wangyan-jianwu-four-life-events.json')['events'];date=ev['normalized_date'];cs={ch['id']:ch};self.assertTrue(annal_date_valid(date,ev,'life_event',cs,ROOT));date['annal_locator']['ganzhi']='庚午';self.assertFalse(annal_date_valid(date,ev,'life_event',cs,ROOT));h=read('corpus/nanqishu/035-hedong-xuan-yan.json');self.assertEqual(h['annotation']['narrative_readings'][0]['ordinal'],19)
