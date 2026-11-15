from pathlib import Path
import unittest,sys,json,copy,hashlib
P=Path(__file__).resolve().parent;F=P.parent;sys.path.insert(0,str(F));from scripts.wyd_song045_lifecycle import records,valid,date_valid,CID
from scripts.layered_biography_titles import holding_valid,address_valid
from scripts.validate_corpus import normalized_date_errors
from scripts.local_death_date_evidence import local_death_date_evidence_valid
from scripts.validate_corpus import source_age_number
from scripts.person_bundle import load_catalog,bundle
SOURCE='corpus/songshu/045-wyd1739-liucui.json'
class Cases(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.ch=json.loads((F/SOURCE).read_bytes());cls.events=records(F)
 def test_three_deaths(self):
  self.assertEqual([x['normalized_date']['year']if'normalized_date'in x else None for x in self.events],[427,433,None])
  for x in self.events:self.assertTrue(valid(x,F))
 def test_actual_date_dispatch(self):
  for x in self.events[:2]:
   d=x['normalized_date'];self.assertEqual(normalized_date_errors(d,{CID:self.ch},F,x,'life_event'),[]);self.assertTrue(local_death_date_evidence_valid(d,x,{CID:self.ch},source_age_number,F))
 def test_wrong_person_direction_and_year(self):
  for key,value in [('person_id','abc_def_123'),('date_expression','元嘉三年'),('source_term','薨')]:
   x=copy.deepcopy(self.events[0]);x[key]=value;self.assertFalse(valid(x,F))
  for key,value in [('year',428),('year',427.0),('precision','month'),('month',1),('day',1),('human_reviewed',True)]:
   x=copy.deepcopy(self.events[0]);x['normalized_date'][key]=value;self.assertFalse(valid(x,F));self.assertFalse(date_valid(x['normalized_date'],x,{CID:self.ch},F))
 def test_scope_chain_and_era_mutations(self):
  for i in [0,1]:
   x=copy.deepcopy(self.events[i]);x['normalized_date']['event_evidence_binding']['chain'][0]['anchor']['start']+=1;self.assertFalse(valid(x,F))
   x=copy.deepcopy(self.events[i]);x['normalized_date']['regnal_year_mapping']['era_name']='元嘉偽';self.assertFalse(valid(x,F))
 def test_unreported_huai_year_not_borrowed(self):
  x=copy.deepcopy(self.events[2]);x['normalized_date']=copy.deepcopy(self.events[0]['normalized_date']);self.assertFalse(valid(x,F))
 def test_malformed_fail_closed(self):
  for x in [None,[],True,'x',{},dict(source_wyd045_death_scope=[])]:self.assertFalse(valid(x,F));self.assertFalse(date_valid(None,x,{},F))
 def test_fixed_row_and_raw_drift_rejected(self):
  from unittest.mock import patch
  from scripts.wyd_song045_lifecycle import ROW
  rb=Path.read_bytes;rowpath=F/ROW;rawpath=F/'source-evidence/song045-wyd1739-liucui/transcription-columns.txt'
  for path in [rowpath,rawpath]:
   if not path.exists():
    self.fail('fixture缺實際來源檔：'+str(path))
   with patch.object(Path,'read_bytes',lambda p:rb(p)+b' 'if p==path else rb(p)):
    self.assertFalse(valid(self.events[0],F))
 def test_reported_53_at_same_death(self):
  from scripts.wyd_song045_lifecycle import age_record,base_annotation
  from scripts.age_context import age_context_valid
  age=age_record(self.ch);self.assertEqual(age['value'],53);self.assertIsNone(age['birth_year']);self.assertEqual(age['counting'],'unspecified_source_age');self.assertTrue(age_context_valid(age,{e['id']:e for e in self.events}));base_annotation(self.ch)
  for key,value in [('value',True),('value',53.0),('value',54),('person_id','abc_def_123'),('birth_year',375),('counting','source_explicit_xusui')]:
   c=copy.deepcopy(self.ch);c['annotation']['age_assertions'][0][key]=value
   with self.assertRaises(ValueError):base_annotation(c)
 def test_existing_grammar_holdings(self):
  d=json.loads((F/'corpus/songshu/045-wyd1739-liucui-titles.json').read_bytes())
  own=[h for h in d['holdings']if h['id']in ('th-song045-wyd-huaizhi-reported','th-song045-wyd-kuangzhi-reported')]
  self.assertEqual(len(own),2)
  for h in own:
   self.assertTrue(holding_valid(h,self.ch));self.assertEqual(h['mode'],'attestation');self.assertEqual(h['effective_period']['start']['status'],'unknown');self.assertEqual(h['effective_period']['end']['status'],'unknown')
   for key,value in [('person_id','abc_def_123'),('mode','grant'),('title','太常')]:
    b=copy.deepcopy(h);b[key]=value;self.assertFalse(holding_valid(b,self.ch))
 def test_origin(self):
  d=json.loads((F/'corpus/songshu/045-wyd1739-liucui-addresses.json').read_bytes());self.assertTrue(address_valid(d['assertions'][0],self.ch))
 def test_real_bundle_dates_and_reports(self):
  cat=load_catalog(F)
  for e in self.events:
   b=bundle(e['person_id'],F,include_provisional=True,catalog=cat)
   def walk(x):
    if isinstance(x,dict):
     if x.get('id')==e['id']:return True
     return any(walk(v)for v in x.values())
    return isinstance(x,list)and any(walk(v)for v in x)
   self.assertTrue(walk(b))
if __name__=='__main__':unittest.main()
