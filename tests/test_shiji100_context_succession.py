import copy
import json
import unittest
from pathlib import Path
from scripts.title_successions import succession_valid
ROOT=Path(__file__).resolve().parents[1]
def read(f):return json.loads((ROOT/f).read_text())
class JibuContextSuccessionTests(unittest.TestCase):
 def setUp(self):
  c=read('corpus/shiji/100.json');self.ps={p['id']:(c['id'],copy.deepcopy(p)) for p in c['paragraphs']};self.hs={h['id']:h for h in read('corpus/shiji/100-titles.json')['holdings']};self.a=copy.deepcopy(next(a for a in read('corpus/shiji/100-assertions.json')['assertions'] if a['id']=='a-shiji100-003'))
 def test_adjacent_quoted_parent_and_child_support_succession(self):
  self.assertTrue(succession_valid(self.a,self.hs,self.ps));self.assertEqual(self.a['qualifiers']['succession']['predecessor_holding_id'],'th-shiji100-020');self.assertEqual(self.a['qualifiers']['succession']['source_term'],'子賁嗣')
 def test_wrong_parent_anchor_does_not_pass(self):
  p=self.ps['c-shiji-100-jibu:p009'][1]
  for m in p['mentions']:
   if m.get('person_id')=='jx9_cov_qe0':m['person_id']='yqp_nlb_p1p_A'
  self.assertFalse(succession_valid(self.a,self.hs,self.ps))
 def test_parent_must_be_inside_its_actual_quote(self):
  self.a['evidence'][0]['quote']='孝文時，爲燕相';self.assertFalse(succession_valid(self.a,self.hs,self.ps))
 def test_inserted_intervening_paragraph_cannot_be_skipped(self):
  ps={}
  for pid,hit in self.ps.items():
   ps[pid]=hit
   if pid.endswith(':p009'):ps['c-shiji-100-jibu:inserted']=(hit[0],{'id':'c-shiji-100-jibu:inserted','text':'插入敘事','mentions':[]})
  self.assertFalse(succession_valid(self.a,self.hs,ps))
 def test_same_address_changes_referent_with_dialogue(self):
  p=self.ps['c-shiji-100-jibu:p004'][1];ms=[m for m in p['mentions'] if m['surface']=='足下'];self.assertEqual([m['person_id'] for m in ms],['tnc_ag2_eej']*2+['udu_dyy_4wd']*4)
  self.assertEqual({m['person_id'] for m in self.ps['c-shiji-100-jibu:p001'][1]['mentions'] if m['surface']=='君'},{'li9_cmb_8ci'});self.assertEqual({m['person_id'] for m in self.ps['c-shiji-100-jibu:p003'][1]['mentions'] if m['surface']=='君'},{'udu_dyy_4wd'})
 def test_specific_grant_year_keeps_received_context_and_other_dates(self):
  h=self.hs['th-shiji100-020'];s=h['effective_period']['start'];self.assertEqual(s['date_expression'],'呉（軍）［楚］反時');self.assertEqual(s['normalized_date_range']['earliest']['year'],-151);self.assertEqual(s['normalized_date_range']['latest']['year'],-150);self.assertEqual(h['title'],'兪侯');self.assertEqual(h['effective_period']['end']['status'],'unknown')
  refs=s['normalized_date_range']['references'];self.assertTrue(any(r.get('revision_id')==9458843 for r in refs));self.assertTrue(any(r.get('table_cell_id')=='shiji-019-t4-r008-c02' for r in refs));death=next(e for e in read('corpus/shiji/100-life-events.json')['events'] if e['person_id']=='jx9_cov_qe0');self.assertEqual(death['normalized_date_range']['latest']['year'],-144)
 def test_commentary_short_name_is_peng_yue(self):
  p=self.ps['c-shiji-100-jibu:p012'][1];self.assertEqual(next(m['person_id'] for m in p['mentions'] if m['surface']=='越'),'9qt_orl_5f2')

 def test_adjacent_context_is_explicit_and_cannot_cross_chapters(self):
  for value in [None,{}, {'kind':'adjacent_paragraphs','paragraph_ids':None}, {'kind':'adjacent_paragraphs','paragraph_ids':['c-shiji-100-jibu:p010','c-shiji-100-jibu:p009']}]:
   a=copy.deepcopy(self.a);a['context']=value;self.assertFalse(succession_valid(a,self.hs,self.ps))
  prior=self.ps['c-shiji-100-jibu:p009'];self.ps['c-shiji-100-jibu:p009']=('another-chapter',prior[1]);self.assertFalse(succession_valid(self.a,self.hs,self.ps))
