import copy,json,unittest
from pathlib import Path
from scripts.table_evidence import load_tables,table_title_range_errors
from scripts.date_ranges import year_range_errors
from scripts.person_bundle import bundle,load_catalog
ROOT=Path(__file__).resolve().parents[1]
class WuGrant(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.tables=load_tables(ROOT);cls.h=next(h for h in json.loads((ROOT/'corpus/shiji/106-titles.json').read_text())['holdings']if h['id']=='th-shiji106-005');cls.v=cls.h['effective_period']['start']['normalized_date_range'];cls.catalog=load_catalog()
 def errors(self,v,endpoint='start'):return table_title_range_errors(v,self.h,endpoint,self.tables)
 def test_explicit_table_grant_is_not_earlier_campaign_date(self):
  s=self.h['effective_period']['start'];self.assertIsNone(s['date_expression']);self.assertEqual(self.v['earliest']['era_year'],196);self.assertEqual(self.v['latest']['era_year'],195);self.assertIn('高帝十一年秋',self.v['original_quote']);self.assertIn('十月辛丑',self.v['table_event']['quote']);self.assertEqual(self.h['effective_period']['end']['status'],'unknown')
 def test_fixed_same_person_table_range_is_valid(self):
  self.assertEqual(self.errors(self.v),[]);self.assertEqual(year_range_errors(self.v,self.h['effective_period']['start']['evidence'],self.v['parallel_event']['source_event_quote']),[])
 def test_wrong_person_and_revision_are_rejected(self):
  for k,value in [('person_mention_id','shiji-017-t1-r012-c12-review-018'),('source_revision','1')]:
   with self.subTest(k=k):v=copy.deepcopy(self.v);v['table_event'][k]=value;self.assertTrue(self.errors(v))
 def test_neighbor_row_and_partial_quote_are_rejected(self):
  for k,value in [('regnal_year_cell_id','shiji-017-t1-r011-c01'),('quote','初王濞元年')]:
   with self.subTest(k=k):v=copy.deepcopy(self.v);v['table_event'][k]=value;self.assertTrue(self.errors(v))
 def test_unmatched_parallel_reference_and_year_are_rejected(self):
  v=copy.deepcopy(self.v);v['parallel_event']['reference_event_quote']='another event';self.assertTrue(self.errors(v));v=copy.deepcopy(self.v);v['latest']['era_year']=196;self.assertTrue(self.errors(v))
 def test_grant_range_does_not_supply_title_end(self):self.assertTrue(self.errors(self.v,'end'))
 def test_bundle_exposes_range_and_its_actual_source_cell(self):
  b=bundle('yqp_nlb_p1p_CA',catalog=self.catalog);d=next(d for d in b['date_range_normalizations']if d['record_id']=='th-shiji106-005');self.assertEqual(d['date_role'],'title_period');self.assertEqual(d['endpoint'],'start');self.assertEqual(d['table_event'],self.v['table_event']);self.assertTrue(any(p['id']==d['table_event']['table_cell_id']and p['text']==d['table_event']['quote']for p in b['table_passages']))
