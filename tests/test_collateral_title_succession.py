# coding: utf-8
from pathlib import Path
import json,copy,unittest
from scripts.collateral_title_succession import valid
R=Path(__file__).resolve().parents[1]
class CollateralTitleSuccessionTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=json.loads((R/'corpus/songshu/047-liuhuaisu.json').read_text());cls.ps={p['id']:(cls.c['id'],p)for p in cls.c['paragraphs']}
  cls.h={h['id']:h for h in json.loads((R/'corpus/songshu/047-liuhuaisu-titles.json').read_text())['holdings']};cls.rels=json.loads((R/'corpus/songshu/047-liuhuaisu-assertions.json').read_text())['assertions']
 def test_two_source_chain_links_no_dates_or_parent_invention(self):
  a=self.h['th-song047-weizu-succession'];b=self.h['th-song047-daocun-succession'];self.assertTrue(valid(a,self.h,self.ps,self.rels))
  self.assertEqual(a['inheritance']['predecessor_holding_id'],'th-song047-020');self.assertEqual(b['inheritance']['predecessor_holding_id'],a['id'])
  for x in(a,b):
   self.assertEqual(x['inheritance']['resolved_title'],'東興縣侯');self.assertIsNone(x['effective_period']['start']['date_expression']);self.assertNotIn('normalized_date',x['effective_period']['start']);self.assertEqual(x['effective_period']['end'],{'status':'unknown','date_expression':None,'evidence':[]})
  self.assertFalse(any(r['subject_person_id']=='myg_cco_ng6'and r['object_person_id']=='olf_c6j_hmg'and r['predicate']in('father','adoptive_father')for r in self.rels))
 def test_collateral_clause_wrong_source_binding_and_dates_rejected(self):
  a=self.h['th-song047-weizu-succession']
  for kind in('predecessor','role','term','position','father','brother','title','year','end','quote','revision'):
   h=copy.deepcopy(a);i=h['inheritance'];b=i['source_chain_binding']
   if kind=='predecessor':i['predecessor_person_id']='tyh_fzo_pb6'
   if kind=='role':i['predecessor_relation']='father'
   if kind=='term':i['source_term']='子蔚祖嗣封'
   if kind=='position':b['clause_anchor']['start']+=1
   if kind=='father':b['father_assertion_id']='a-song047-liuhuaisu-004'
   if kind=='brother':b['brother_assertion_id']='a-song047-liuhuaisu-003'
   if kind=='title':i['resolved_title']='左將軍'
   if kind=='year':h['effective_period']['start']['date_expression']='三年'
   if kind=='end':h['effective_period']['end']['date_expression']='卒'
   if kind=='quote':h['evidence'][0]['quote']+='改'
   if kind=='revision':b['source_revision']='wrong'
   self.assertFalse(valid(h,self.h,self.ps,self.rels),kind)
  self.assertFalse(valid(a,self.h,self.ps,[]))
 def test_distinct_second_link_is_explicit_father_not_collateral(self):
  b=self.h['th-song047-daocun-succession'];self.assertEqual(b['inheritance']['source_term'],'蔚祖卒子道存嗣')
  self.assertFalse(valid(b,self.h,self.ps,self.rels))
  self.assertTrue(any(r['subject_person_id']==b['person_id']and r['object_person_id']==b['inheritance']['predecessor_person_id']and r['predicate']=='father'for r in self.rels))
if __name__=='__main__':unittest.main()
