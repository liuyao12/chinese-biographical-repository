# coding:utf-8
import copy,json,unittest
from pathlib import Path
from scripts.table_evidence import load_tables,table_regnal_range_errors
R=Path(__file__).resolve().parents[1]
def load(f):return json.loads((R/f).read_text())
class ReignDesignations(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.tables=load_tables(R);cls.mentions={m['id']:(c['id'],p['id'],m)for f in (R/'corpus').glob('*/*.json')for c in [json.loads(f.read_text())]if c.get('record_type')=='marked_chapter'for p in c['paragraphs']for m in p['mentions']}
 def item(self,hid='th-shiji113-005'):
  h=next(h for h in load('corpus/shiji/113-titles.json')['holdings']if h['id']==hid);b=h['effective_period']['start'];return copy.deepcopy(b['normalized_date_range']),b['date_expression']
 def errors(self,w,e,mentions=None):return table_regnal_range_errors(w,e,self.tables,self.mentions if mentions is None else mentions)
 def test_two_original_designations_keep_source_text_and_civil_year_windows(self):
  for hid,expr,pair,years in [('th-shiji113-005','漢十一年',('漢','高皇帝'),(197,196)),('th-shiji113-011','孝文帝元年',('孝文帝','孝文'),(180,179))]:
   w,e=self.item(hid);self.assertEqual(e,expr);proof=w['regnal_year_table'];self.assertEqual((proof['source_era_name'],proof['era_name']),pair);self.assertEqual((w['earliest']['era_year'],w['latest']['era_year']),years);self.assertEqual(self.errors(w,e),[])
 def test_autumn_appointment_references_use_fixed_year_cells(self):
  for hid in ['th-shiji113-022','th-shiji113-024']:
   h=next(h for h in load('corpus/shiji/113-titles.json')['holdings']if h['id']==hid);b=h['effective_period']['start'];self.assertEqual(b['date_expression'],'元鼎五年秋');d=b['normalized_date'];self.assertEqual(d['era_year'],112);refs=d['references'];self.assertTrue(any(r.get('table_cell_id')=='shiji-022-t1-r095-c00'and r['quote']=='112'for r in refs));self.assertTrue(any(r.get('scope')=='received_calendar_rule'for r in refs));self.assertTrue(all('oldid='in r['url'] or r.get('scope')=='received_calendar_rule'for r in refs))
 def test_han006_parallel_dates_keep_original_date_blank(self):
  from scripts.date_ranges import parallel_event_date
  hs=load('corpus/hanshu/006-titles.json')['holdings'];self.assertEqual(len(hs),6)
  for h in hs:
   a=h['attestations'][0];self.assertIsNone(a['date_expression']);d=a['normalized_date'];self.assertTrue(parallel_event_date(d));self.assertEqual(d['era_year'],112);self.assertEqual(d['basis']['reference_year_quote'],'元鼎五年秋');r=next(r for r in d['references']if r['scope']=='received_parallel_event');m=self.mentions[r['person_mention_id']];self.assertEqual(m[2]['person_id'],h['person_id']);self.assertEqual(m[0],'c-shiji-113-nanyue');self.assertIn('oldid=',r['url'])
 def test_only_explicit_han006_grants_receive_start_date(self):
  hs=load('corpus/hanshu/006-titles.json')['holdings'];dated=[h for h in hs if 'normalized_date'in h['effective_period']['start']];self.assertEqual([h['title']for h in dated],['戈船將軍','下瀨將軍'])
  for h in hs:
   b=h['effective_period']['start'];self.assertIsNone(b['date_expression']);self.assertEqual(h['effective_period']['end']['status'],'unknown')
   if h['mode']=='attestation':self.assertEqual(b['status'],'unknown');self.assertNotIn('normalized_date',b)
 def test_person_bundle_preserves_source_designation_and_validates_anchor(self):
  from scripts.person_bundle import bundle
  for pid,hid,expr in [('bvb_d1z_fd0','th-shiji113-005','漢十一年'),('fpv_2sb_uay','th-shiji113-011','孝文帝元年')]:
   b=bundle(pid,root=R);h=next(h for h in b['title_holdings']if h['id']==hid);self.assertEqual(h['effective_period']['start']['date_expression'],expr);self.assertIn('reign_designation',h['effective_period']['start']['normalized_date_range']['regnal_year_table']);self.assertTrue(any(c.get('id')=='shiji-022-t1-r001-c01'if hid.endswith('005')else c.get('id')=='shiji-022-t1-r028-c01'for c in b['table_passages']))
 def test_person_bundle_rejects_wrong_reign_person(self):
  from scripts.person_bundle import bundle,load_catalog
  catalog=load_catalog(R)
  h=next(h for record in catalog[1]for h in record.get('holdings',[])if h['id']=='th-shiji113-005');h['effective_period']['start']['normalized_date_range']['regnal_year_table']['reign_designation']['person_id']='yqp_nlb_p1p_AC'
  with self.assertRaises(ValueError):bundle('bvb_d1z_fd0',root=R,catalog=catalog)
 def test_missing_designation_proof_is_rejected(self):
  w,e=self.item();w['regnal_year_table'].pop('reign_designation');self.assertTrue(self.errors(w,e))
 def test_unknown_designation_is_not_a_global_year_alias(self):
  w,e=self.item();p=w['regnal_year_table'];p['source_era_name']='魏';p['reign_designation']['source_era_name']='魏';self.assertTrue(self.errors(w,'魏十一年'))
 def test_wrong_person_or_wrong_source_anchor_rejected(self):
  for key,value in [('person_id','yqp_nlb_p1p_AC'),('person_mention_id','c-shiji-113-nanyue:m003-0001')]:
   w,e=self.item();w['regnal_year_table']['reign_designation'][key]=value;self.assertTrue(self.errors(w,e))
 def test_anchor_must_exist_in_actual_corpus(self):
  w,e=self.item();self.assertTrue(self.errors(w,e,{}))
 def test_context_cannot_come_from_unrelated_paragraph(self):
  w,e=self.item();w['evidence'][0]['paragraph_id']='c-shiji-113-nanyue:p003';self.assertTrue(self.errors(w,e))
 def test_source_context_quote_cannot_be_arbitrary(self):
  w,e=self.item();w['regnal_year_table']['reign_designation']['source_context_quote']='漢人皆曰';self.assertTrue(self.errors(w,e))
 def test_human_review_cannot_be_invented(self):
  w,e=self.item();w['regnal_year_table']['reign_designation']['human_reviewed']=True;self.assertTrue(self.errors(w,e))
 def test_malformed_source_era_name_returns_errors_not_exception(self):
  for value in [None,[],{},1]:
   w,e=self.item();w['regnal_year_table']['source_era_name']=value;self.assertTrue(self.errors(w,e))
 def test_wrong_calendar_range_is_rejected(self):
  w,e=self.item();w['earliest']=dict(w['latest']);self.assertTrue(self.errors(w,e))
 def test_exact_designation_does_not_accept_unneeded_claim(self):
  w,e=self.item();p=w['regnal_year_table'];p.pop('source_era_name');self.assertTrue(self.errors(w,'高皇帝十一年'))
if __name__=='__main__':unittest.main()
