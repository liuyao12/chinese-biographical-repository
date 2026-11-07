import unittest,json,copy
from pathlib import Path
from unittest.mock import patch
import received_sima_family_sources as owner53
import jin064_wudi_family_sources as owner64
from validate_corpus import normalized_date_errors,direct_source_age_valid
from age_context import age_context_valid
from posthumous_enfeoffments import valid as enfeoffment_valid
ROOT=Path(__file__).resolve().parents[1]
class ReceivedSimaDatedProfiles(unittest.TestCase):
 def fixture(self):
  raw=lambda p:(ROOT/p).read_bytes();return ROOT,raw,{p['id']:p for p in json.loads(raw('registry/persons.json'))['persons']}
 def setup(self):
  root,raw,people=self.fixture();c53,r53,d53=owner53._proof(raw,people);c64,r64,d64=owner64._proof(raw,people);docs={**d53,**d64};chapters={d['id']:d for d in docs.values()if d.get('record_type')=='marked_chapter'};events={e['id']:e for d in docs.values()for e in d.get('events',[])};return root,raw,people,docs,chapters,events,r53,r64
 def test_01_current_both_owners_and_exact_scope(self):
  _,_,_,docs,chs,events,_,_=self.setup();self.assertEqual(len(events),8);self.assertTrue(all(e['event_type']=='death'for e in events.values()));self.assertEqual(sum(len(d.get('holdings',[]))for d in docs.values()),1);self.assertEqual(sum(len(c['annotation'].get('age_assertions',[]))for c in chs.values()),6)
 def test_02_normal_regnal_years_all_nine(self):
  _,_,_,docs,chs,events,_,_=self.setup();dates=[(e,e['normalized_date'],'life_event')for e in events.values()]
  dates +=[(h,h['effective_period']['start']['normalized_date'],'start')for d in docs.values()for h in d.get('holdings',[])]
  for record,date,role in dates:self.assertEqual(normalized_date_errors(date,chs,bound_record=record,bound_role=role),[])
 def test_03_wrong_year_even_coherent_era_year_rejected(self):
  _,_,_,_,chs,events,_,_=self.setup()
  for e in events.values():
   d=copy.deepcopy(e['normalized_date']);d['year']+=1;d['era_year']+=1;self.assertTrue(normalized_date_errors(d,chs,bound_record=e,bound_role='life_event'))
 def test_04_omitted_era_and_same_year_remain_literal(self):
  _,_,_,_,_,events,_,_=self.setup();j=events['le-jin064-jing-death'];z=events['le-jin064-zhi-death'];y=events['le-jin064-yu_wudi_son-death'];self.assertEqual(j['date_expression'],'六年');self.assertEqual(j['normalized_date']['year'],270);self.assertEqual(z['date_expression'],'其年');self.assertEqual(z['normalized_date']['year'],273);self.assertEqual(y['normalized_date']['year'],277)
 def test_05_normal_age_context_and_no_derived_birth(self):
  _,_,_,_,chs,events,_,_=self.setup()
  for ch in chs.values():
   for a in ch['annotation'].get('age_assertions',[]):self.assertTrue(direct_source_age_valid(a));self.assertTrue(age_context_valid(a,events));self.assertIsNone(a['birth_year']);self.assertEqual(a['counting'],'unspecified_source_age')
 def test_06_age_cannot_borrow_another_death(self):
  _,_,_,_,chs,events,_,_=self.setup();a=copy.deepcopy(next(a for c in chs.values()for a in c['annotation'].get('age_assertions',[])));a['age_context']['life_event_id']=next(eid for eid,e in events.items()if e['person_id']!=a['person_id']);self.assertFalse(age_context_valid(a,events))
 def test_07_normal_posthumous_enfeoffment_and_wrong_death(self):
  _,_,_,docs,chs,events,_,_=self.setup();h=next(h for d in docs.values()for h in d.get('holdings',[]));ps={p['id']:(c['id'],p)for c in chs.values()for p in c['paragraphs']};ms={m['id']:(c['id'],p['id'],m)for c in chs.values()for p in c['paragraphs']for m in p['mentions']};self.assertTrue(enfeoffment_valid(h,ps,ms,events));self.assertEqual(h['effective_period']['start']['date_expression'],'四月');self.assertEqual(h['effective_period']['start']['normalized_date']['year'],300);bad=copy.deepcopy(h);bad['enfeoffment_basis']['death_event_id']=next(eid for eid,e in events.items()if e['person_id']!=h['person_id']);self.assertFalse(enfeoffment_valid(bad,ps,ms,events));self.assertEqual(h['effective_period']['end']['status'],'unknown')
 def test_08_age_value_and_human_type_drift_rejected(self):
  root,raw,people,docs,chs,events,_,_=self.setup();c=next(c for c in chs.values()if c['id']==owner64.CID);path=next(p for p,d in docs.items()if d is c)
  for key,value in [('value',999),('human_reviewed',0)]:
   bad=copy.deepcopy(c);bad['annotation']['age_assertions'][0][key]=value;b=json.dumps(bad,ensure_ascii=False).encode()
   with self.assertRaises(AssertionError):owner64._proof(lambda p:b if p==path else raw(p),people)
 def test_09_death_cannot_move_to_different_source_person(self):
  _,raw,people,docs,_,events,_,r64=self.setup();path=next(p for p,d in docs.items()if d.get('record_type')=='person_life_event_assertion_set'and d.get('chapter_id')==owner64.CID);bad=copy.deepcopy(docs[path]);bad['events'][0]['person_id']=r64['qin'];b=json.dumps(bad,ensure_ascii=False).encode()
  with self.assertRaises(AssertionError):owner64._proof(lambda p:b if p==path else raw(p),people)
 def test_10_caller_only_new_life_owner_rejected_at_entry(self):
  root,raw,people,docs,_,_,_,_=self.setup();c=json.loads(raw(owner53.REF));records=[copy.deepcopy(docs[p])for p in c['expected_documents']];life=next(d for d in records if d.get('record_type')=='person_life_event_assertion_set');fake='q1q_q1q_q1q';life['events'][0]['person_id']=fake
  with patch.object(owner53,'_raw',lambda r,p:raw(p)),patch.object(owner64,'_raw',lambda r,p:raw(p)):
   with self.assertRaisesRegex(ValueError,'caller/physical'):owner53.guard_bundle(root,fake,people,records)
 def test_11_caller_only_new_holding_owner_rejected_at_entry(self):
  root,raw,people,docs,_,_,_,_=self.setup();c=json.loads(raw(owner53.REF));records=[copy.deepcopy(docs[p])for p in c['expected_documents']];holding=next(d for d in records if d.get('record_type')=='title_holding_assertion_set');fake='q1q_q1q_q1q';holding['holdings'][0]['person_id']=fake
  with patch.object(owner53,'_raw',lambda r,p:raw(p)),patch.object(owner64,'_raw',lambda r,p:raw(p)):
   with self.assertRaisesRegex(ValueError,'caller/physical'):owner53.guard_bundle(root,fake,people,records)
 def test_12_source_raw_mids_and_xml_are_conserved(self):
  _,_,_,docs,chs,_,_,_=self.setup()
  from render_corpus import render
  for ch in chs.values():
   xml=render(ch);self.assertEqual(xml.count('<p '),len(ch['paragraphs']));self.assertNotIn('時年三歲</persName>',xml)
 def test_13_legitimate_current_endpoint_rekey_preserves_dates_and_opaque_ids(self):
  _,raw,people,docs,_,_,r53,_=self.setup();old=r53['bin'];new='q2q_q2q_q2q';self.assertNotIn(new,people);c=json.loads(raw(owner53.REF));paths=set(c['expected_documents'])
  def move(x):
   if isinstance(x,dict):return{k:move(v)for k,v in x.items()}
   if isinstance(x,list):return[move(v)for v in x]
   return new if x==old else x
  p=copy.deepcopy(people);p[new]=p.pop(old);p[new]['id']=new
  changed=lambda rel:json.dumps(move(json.loads(raw(rel))),ensure_ascii=False).encode()if rel in paths else raw(rel)
  _,roles,after=owner53._proof(changed,p);self.assertEqual(roles['bin'],new)
  for path in paths:
   original=docs[path];current=after[path]
   for key in('events','holdings','assertions'):
    if key in original:self.assertEqual([x['id']for x in original[key]],[x['id']for x in current[key]])
if __name__=='__main__':unittest.main()
