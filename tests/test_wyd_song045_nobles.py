from pathlib import Path
import sys,json,copy,unittest
from unittest.mock import patch
P=Path(__file__).resolve().parent;F=P.parent;sys.path.insert(0,str(F))
from scripts.wyd_song045_nobles import records,holding_valid,holding_dispatch_valid,event_record,event_valid,extra_deaths,death_valid,proposal,proposal_valid,base_annotation,CID,ROW
from scripts.received_career_roles import holding_valid as role_valid,event_valid as career_event_valid
from scripts.noble_transfers import noble_transfer_errors
from scripts.unassumed_appointments import unassumed_appointment_valid
from scripts.validate_corpus import normalized_date_errors
from scripts.person_bundle import load_catalog,bundle
class Cases(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.ch=json.loads((F/'corpus/songshu/045-wyd1739-liucui.json').read_bytes());cls.hs,cls.q=records(F);cls.by={h['id']:h for h in cls.hs};cls.ps={p['id']:(CID,p)for p in cls.ch['paragraphs']};cls.ms={m['id']:(CID,p['id'],m)for p in cls.ch['paragraphs']for m in p['mentions']};cls.relations=json.loads((F/'corpus/songshu/045-wyd1739-liucui-assertions.json').read_bytes())['assertions']
 def test_all_seven_holding_dispatch(self):
  self.assertEqual(len(self.hs),7)
  for h in self.hs:self.assertTrue(holding_valid(h,self.ch,self.by,F));self.assertTrue(role_valid(h,self.ch,F))
 def test_actual_fief_numbers_and_types(self):
  for slot,value,number in [('cui-she',500,'五百'),('cui-jianan',1000,'千')]:
   h=self.by['th-song045-wyd-'+slot];self.assertEqual(h['reported_households']['value'],value);self.assertEqual(h['reported_households']['source_number'],number);self.assertIsNone(h['reported_households']['actual_revenue'])
   for wrong in [True,float(value),value+1]:
    b=copy.deepcopy(h);b['reported_households']['value']=wrong;self.assertFalse(holding_valid(b,self.ch,self.by,F))
 def test_transfer_and_year420(self):
  j=self.by['th-song045-wyd-cui-jianan'];self.assertEqual(noble_transfer_errors(j,self.by,self.ps,self.ms,{CID:self.ch}),[]);self.assertEqual(normalized_date_errors(j['effective_period']['start']['normalized_date'],{CID:self.ch},F,j,'start'),[])
  self.assertEqual(j['effective_period']['start']['normalized_date']['year'],420);self.assertEqual(self.by['th-song045-wyd-cui-she']['effective_period']['end']['event_type'],'explicit_end');self.assertEqual(self.by['th-song045-wyd-cui-xian']['effective_period']['end']['status'],'unknown')
  b=copy.deepcopy(j);b['transfer_basis']['previous_holding_id']='th-song045-wyd-cui-xian';self.assertFalse(holding_valid(b,self.ch,self.by,F))
 def test_succession_surface_full_chain_and_unknown_dates(self):
  for slot in ['kuang-jianan','chen-jianan']:
   h=self.by['th-song045-wyd-'+slot];self.assertEqual(h['attestations'][0]['surface'],'嗣');self.assertEqual(h['title'],'嗣');self.assertTrue(holding_valid(h,self.ch,self.by,F));self.assertIsNone(h['effective_period']['start']['date_expression']);self.assertEqual(h['effective_period']['end']['status'],'unknown')
   b=copy.deepcopy(h);b['effective_period']['start']['date_expression']='明年';self.assertFalse(holding_valid(b,self.ch,self.by,F))
   b=copy.deepcopy(h);b['source_succession_binding']['father_assertion_id']='a-song045-wyd-huai-father';self.assertFalse(holding_valid(b,self.ch,self.by,F))
 def test_wrong_predecessor_or_missing_holding(self):
  h=self.by['th-song045-wyd-chen-jianan'];by=copy.deepcopy(self.by);del by['th-song045-wyd-kuang-jianan'];self.assertFalse(holding_valid(h,self.ch,by,F))
  b=copy.deepcopy(h);b['inheritance']['predecessor_person_id']=self.by['th-song045-wyd-cui-jianan']['person_id'];self.assertFalse(holding_valid(b,self.ch,self.by,F))
 def test_posthumous_not_active_and_not_dated_by_death(self):
  for slot in ['cui-anbei','sun-taichang']:
   h=self.by['th-song045-wyd-'+slot];self.assertEqual(h['mode'],'posthumous_grant');self.assertIsNone(h['effective_period']['start']['date_expression']);b=copy.deepcopy(h);b['mode']='grant';self.assertFalse(holding_valid(b,self.ch,self.by,F))
 def test_unassumed_not_holding_and_existing_generic(self):
  self.assertTrue(unassumed_appointment_valid(self.q,self.ch));self.assertTrue(proposal_valid(self.q,self.ch,F));self.assertEqual(self.q['outcome'],'not_assumed');self.assertNotIn(self.q['person_id'],[h['person_id']for h in self.hs]);base_annotation(self.ch)
  for key,value in [('outcome','not_reported'),('person_id','abc_def_123'),('title','太常'),('date_expression','元嘉二年')]:
   q=copy.deepcopy(self.q);q[key]=value;self.assertFalse(proposal_valid(q,self.ch,F));c=copy.deepcopy(self.ch);c['annotation']['title_proposals']=[q]
   with self.assertRaises(ValueError):base_annotation(c)
 def test_heir_deaths_and_abolition(self):
  self.assertEqual(len(extra_deaths(F)),2)
  for e in extra_deaths(F):self.assertTrue(death_valid(e,F));self.assertIsNone(e['date_expression']);self.assertNotIn('normalized_date',e)
  e=event_record(F);self.assertTrue(event_valid(e,self.ch,F));self.assertTrue(career_event_valid(e,self.ch,F));b=copy.deepcopy(e);b['holding_id']='th-song045-wyd-cui-xian';self.assertFalse(event_valid(b,self.ch,F))
 def test_malformed_no_exceptions(self):
  for x in [None,True,[],str('bad'),{},dict(source_career_role=None),dict(source_career_role=[]),dict(source_inherited_title_binding=None)]:
   self.assertFalse(holding_valid(x,self.ch,self.by,F));self.assertFalse(role_valid(x,self.ch,F));self.assertFalse(event_valid(x,self.ch,F));self.assertFalse(career_event_valid(x,self.ch,F))
 def test_wrong_person_quote_and_date(self):
  h=self.hs[0]
  for key,val in [('person_id','abc_def_123'),('title','建安縣侯')]:
   b=copy.deepcopy(h);b[key]=val;self.assertFalse(holding_valid(b,self.ch,self.by,F))
  ch=copy.deepcopy(self.ch);ch['paragraphs'][0]['text']='錯'+ch['paragraphs'][0]['text'];self.assertFalse(holding_valid(h,ch,self.by,F))
  j=copy.deepcopy(self.by['th-song045-wyd-cui-jianan']);j['effective_period']['start']['normalized_date']['year']=421;self.assertFalse(holding_valid(j,self.ch,self.by,F))
 def test_source_raw_calendar_and_father_proof_drift(self):
  rb=Path.read_bytes
  for path in [F/ROW,F/'source-evidence/song045-wyd1739-liucui/transcription-columns.txt']:
   with patch.object(Path,'read_bytes',lambda p:rb(p)+b' 'if p==path else rb(p)):self.assertFalse(holding_valid(self.hs[0],self.ch,self.by,F))
  path=F/'corpus/songshu/045-wyd1739-liucui-assertions.json';d=json.loads(rb(path));next(a for a in d['assertions']if a['id']=='a-song045-wyd-chen-father')['evidence'][0]['quote']='假引文'
  with patch.object(Path,'read_bytes',lambda p:json.dumps(d,ensure_ascii=False).encode()if p==path else rb(p)):self.assertFalse(holding_valid(self.by['th-song045-wyd-chen-jianan'],self.ch,self.by,F))
 def test_missing_marker_actual_api_rejected(self):
  catalog=load_catalog(F)
  for record_type,key,record_id,marker in [('title_holding_assertion_set','holdings','th-song045-wyd-cui-xian','source_career_role'),('person_life_event_assertion_set','events','le-song045-wyd-kuangzhi','source_wyd045_noble_death_scope')]:
   altered=copy.deepcopy(catalog);r=next(r for r in altered[1]if r.get('record_type')==record_type and r.get('chapter_id')==CID);x=next(x for x in r[key]if x['id']==record_id);pid=x['person_id'];x.pop(marker)
   with self.assertRaises(ValueError):bundle(pid,F,include_provisional=True,catalog=altered)
 def test_prior_seven_facts_preserved(self):
  ch=self.ch;self.assertEqual(ch['annotation']['age_assertions'][0]['value'],53)
  hs=json.loads((F/'corpus/songshu/045-wyd1739-liucui-titles.json').read_bytes())['holdings'];self.assertEqual(len(hs),9);self.assertEqual(len([h for h in hs if h['mode']=='attestation']),2)
  events=json.loads((F/'corpus/songshu/045-wyd1739-liucui-life-events.json').read_bytes())['events'];self.assertEqual({e['id'] for e in events if e['id'] in {'le-song045-wyd-cui','le-song045-wyd-daoji','le-song045-wyd-huai'}},{'le-song045-wyd-cui','le-song045-wyd-daoji','le-song045-wyd-huai'});self.assertEqual([e['normalized_date']['year']for e in events if e['id'] in {'le-song045-wyd-cui','le-song045-wyd-daoji','le-song045-wyd-huai'} and 'normalized_date'in e],[427,433])
if __name__=='__main__':unittest.main()
