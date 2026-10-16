import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def row():
 d=json.loads((ROOT/'data/historical-tables/shiji-019.json').read_text())
 return next(r for f in d['fragments'] for r in f['rows'] if r['id']=='shiji-019-t4-r008')
class LuanBuHouTableTests(unittest.TestCase):
 def test_luan_bu_short_forms_do_not_swallow_qing_bu(self):
  c=row()['cells'][1];ms=c['person_mentions']
  self.assertEqual({m['person_id'] for m in ms if m['surface']=='布'},{'jx9_cov_qe0'});self.assertEqual(len([m for m in ms if m['surface']=='布']),4)
  q=next(m for m in ms if m['surface']=='黥布');self.assertEqual(q['person_id'],'zxd_afr_2xg');self.assertFalse(any(m['start']>q['start'] and m['start']<q['end'] for m in ms))
 def test_peng_yue_and_gaozu_short_forms_follow_the_same_event(self):
  ms=row()['cells'][1]['person_mentions'];self.assertEqual(len([m for m in ms if m['surface']=='越']),2)
  self.assertEqual({m['person_id'] for m in ms if m['surface'] in ['越','彭越']},{'9qt_orl_5f2'});self.assertEqual(next(m['person_id'] for m in ms if m['surface']=='高祖'),'yqp_nlb_p1p_A')
 def test_death_holder_and_succeeding_hou_ben_remain_distinct(self):
  a,b=row()['cells'][2:4];self.assertEqual(next(m['person_id'] for m in a['person_mentions'] if m['surface']=='布'),'jx9_cov_qe0');self.assertEqual(next(m['person_id'] for m in b['person_mentions'] if m['surface']=='賁'),'jx9_cov_qe0_A')
  self.assertIn('亖月丁卯',a['text']);self.assertIn('元狩六年',b['text'])
