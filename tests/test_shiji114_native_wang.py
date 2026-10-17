# coding:utf-8
import copy,json,unittest
from pathlib import Path
from unittest.mock import patch
from scripts.table_evidence import load_tables,table_person_evidence_errors,table_name_component_errors
from scripts.table_title_holdings import table_title_errors
from scripts.validate_corpus import validate
from scripts.person_bundle import bundle
R=Path(__file__).resolve().parents[1]
PID='r5s_lra_wfi';CELL='shiji-022-t1-r069-c02';MID=CELL+'-m000'
def load(p):return json.loads((R/p).read_text())
class NativeWangProfile(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.tables=load_tables(R);cls.registry=load('registry/persons.json');cls.people={p['id']for p in cls.registry['persons']};cls.person=next(p for p in cls.registry['persons']if p['id']==PID);cls.e=cls.person['evidence'][0];cls.holdings=load('corpus/shiji/022-table-title-events.json')['holdings']
 def test_native_registry_evidence_is_exact_name_and_full_cell(self):
  self.assertEqual(table_person_evidence_errors(self.e,self.tables,PID),[]);self.assertEqual(self.e['quote'],'望');self.assertEqual(self.e['source_quote'],'東甌王廣武侯望率其眾四萬餘人來降，處廬江郡。');self.assertNotIn('paragraph_id',self.e)
 def test_wrong_cell_revision_person_and_surface_are_rejected(self):
  for key,value in [('table_cell_id','shiji-022-t1-r069-c01'),('source_revision','0'),('mention_id','missing'),('source_quote','望'),('quote','東甌王'),('chapter_id','c-shiji-114-dongyue')]:
   e=dict(self.e,**{key:value});self.assertTrue(table_person_evidence_errors(e,self.tables,PID),key)
  self.assertTrue(table_person_evidence_errors(self.e,self.tables,'ub6_g9c_hvb'))
 def test_offspan_and_fake_paragraph_are_rejected(self):
  tables=copy.deepcopy(self.tables);cell=next(c for f in tables['shiji-022']['fragments']for r in f['rows']for c in r['cells']if c['id']==CELL);cell['person_mentions'][0]['start']-=1;self.assertTrue(table_person_evidence_errors(self.e,tables,PID));self.assertTrue(table_person_evidence_errors(dict(self.e,paragraph_id='fabricated'),self.tables,PID))
 def test_registry_scope_and_bidirectional_evidence_are_checked(self):
  original=Path.read_text
  for kind in ['scope','missing_evidence','bad_alias']:
   registry=copy.deepcopy(self.registry);person=next(p for p in registry['persons']if p['id']==PID)
   if kind=='scope':person.pop('evidence_scope')
   elif kind=='missing_evidence':person['evidence']=[]
   else:person['aliases'][0]['surface']='搖'
   def read(path,*args,**kwargs):
    if path==R/'registry/persons.json':return json.dumps(registry,ensure_ascii=False)
    return original(path,*args,**kwargs)
   with patch.object(Path,'read_text',read):errors=validate(R)
   self.assertTrue(errors,kind);self.assertTrue(any('人物' in x or '異稱' in x for x in errors),errors[:3])
 def test_two_source_titles_are_attestations_with_unknown_periods(self):
  self.assertEqual({h['title']for h in self.holdings},{'東甌王','廣武侯'})
  for h in self.holdings:
   self.assertEqual(table_title_errors(h,self.tables,self.people),[]);self.assertEqual(h['mode'],'attestation');self.assertTrue(all(x==dict(status='unknown',date_expression=None,evidence=[])for x in h['effective_period'].values()))
 def test_surrender_cannot_be_changed_to_grant_or_accession(self):
  for mode in ['grant','accession','self_proclamation']:
   h=copy.deepcopy(self.holdings[0]);h['mode']=mode;self.assertTrue(table_title_errors(h,self.tables,self.people))
 def test_inline_title_cannot_use_wrong_name_or_title_span(self):
  for kind in ['person','span','revision','cell']:
   h=copy.deepcopy(self.holdings[0])
   if kind=='person':h['person_id']='ub6_g9c_hvb'
   elif kind=='span':h['attestations'][0]['source_parts'][0]['start']=1
   elif kind=='revision':h['evidence'][0]['source_revision']='0'
   else:h['table_title_basis']['event']['table_cell_id']='shiji-022-t1-r068-c02'
   self.assertTrue(table_title_errors(h,self.tables,self.people),kind)
 def test_inline_title_cannot_invent_start_end_or_event_year(self):
  for endpoint in ['start','end']:
   h=copy.deepcopy(self.holdings[0]);h['effective_period'][endpoint].update(status='source_event',date_expression='建元三年');self.assertTrue(table_title_errors(h,self.tables,self.people))
  h=copy.deepcopy(self.holdings[0]);h['attestations'][0]['normalized_date']=dict(year=-137);self.assertTrue(table_title_errors(h,self.tables,self.people))
 def test_surname_and_paternal_family_are_not_invented(self):
  n=next(n for n in load('data/corpus/profile-names.json')['records']if n['person_id']==PID);self.assertEqual(table_name_component_errors(n,self.tables),[]);self.assertEqual((n['surname'],n['ming'],n['title']),(None,'望','東甌王'));self.assertNotIn('family_path',self.person)
 def test_commentary_is_a_quotation_of_the_table_not_independent_event(self):
  ref=self.person['references'][0];self.assertIn('徐廣曰年表曰',ref['raw_quote']);self.assertIn('L37-L39',ref['url']);self.assertFalse(ref['image_verified']);self.assertEqual(ref['scope'],'commentary_quotes_year_table_not_independent_event')
 def test_full_bundle_has_native_occurrence_sources_titles_and_no_fake_prose(self):
  b=bundle(PID,R);self.assertEqual(b['mentions'],[]);self.assertEqual(len(b['table_occurrences']),1);self.assertEqual(b['table_occurrences'][0]['id'],MID);self.assertEqual(b['most_mentioned_source_ids'],['table-witness-shiji-022']);self.assertEqual(len(b['title_holdings']),2);self.assertEqual(b['relations'],[]);self.assertEqual(b.get('life_events',[]),[]);self.assertTrue(any(c['id']==CELL for c in b['table_passages']));self.assertTrue(any(s['source_id']=='table-witness-shiji-022'for s in b['sources']))
 def test_distinct_wang_and_unnamed_kings_remain_separate(self):
  b=bundle(PID,R,include_provisional=True);self.assertEqual(b['person_ids'],[PID]);self.assertTrue({'c19_xxo_r8f_*A','xzr_i9s_mnp','ub6_g9c_hvb'}.issubset(self.people))
 def test_export_and_reader_profile_are_complete_not_candidate_fallback(self):
  b=load('exports/persons/'+PID+'.json');p=load('data/corpus/profiles/'+PID+'.json');self.assertEqual(b['record_type'],'person_source_bundle');self.assertEqual(len(p['titles']),2);self.assertEqual(p['review'],'ai_provisional');self.assertEqual(p['name_components'][0]['ming'],'望');self.assertEqual(p['occurrences'],[]);self.assertEqual(len(p['table_occurrences']),1);self.assertEqual(p['relations'],[])
if __name__=='__main__':unittest.main()
