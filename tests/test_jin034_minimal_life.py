"""Portable finite minimal-life tests; no source clone or hardcoded current PID."""
import copy,json
from contextlib import contextmanager
from scripts import fixed_jin034_yanghu_ner as core,fixed_jin034_minimal_life as m
from tests.test_jin034_yanghu_ner import YangHuNER
class MinimalLife(YangHuNER):
 def reject(self):
  with self.assertRaises((ValueError,KeyError,TypeError,OSError)):core.accepted_state(self.T)
 def test_exact_death_age_origin(self):
  b,r,people,ch=core.accepted_state(self.T);phase=m.documents(self.T,r,ch)
  life=core.read(self.T,m.LP)['events'];address=core.read(self.T,m.AP)['assertions'];age=next(x for x in ch['annotation']['age_assertions']if x['id']=='age-jin034-yanghu-death58')
  self.assertEqual(len(life),1);self.assertEqual(life[0]['event_type'],'death');self.assertIsNone(life[0]['date_expression']);self.assertNotIn('normalized_date',life[0]);self.assertEqual(life[0]['person_id'],r['yang_hu'])
  self.assertEqual(age['value'],58);self.assertEqual(age['source_number'],'五十八');self.assertIsNone(age['birth_year']);self.assertEqual(age['age_context'],{'kind':'at_death','life_event_id':life[0]['id']});self.assertEqual(age['evidence'],life[0]['evidence'])
  self.assertEqual(address[0]['relation'],'biographical_origin');self.assertEqual(address[0]['place'],{'source_name':'泰山南城','place_id':None,'modern_identification':None});self.assertEqual(set(phase['expected_documents']),{m.LP,m.AP})
 def test_wrong_death_owner(self):
  self.change(m.LP,lambda d:d['events'][0].update(person_id=self.r['du_yu']));self.reject()
 def test_wrong_quote(self):
  self.change(m.LP,lambda d:d['events'][0]['evidence'][0].update(quote='尋卒，時年五十八。'));self.reject()
 def test_fake_278(self):
  self.change(m.LP,lambda d:d['events'][0].update(date_expression='咸寧四年',normalized_date={'year':278}));self.reject()
 def test_age_cannot_be_birth_or_other_person(self):
  def f(ch):
   a=next(a for a in ch['annotation']['age_assertions']if a['id']=='age-jin034-yanghu-death58');a.update(birth_year=221,person_id=self.r['du_yu'])
  self.change(core.CH,f);self.reject()
 def test_missing_reverse(self):
  mid=core.CID+':p028:m0053'
  def f(d):next(p for p in d['persons']if p['id']==self.r['yang_hu'])['evidence']=[e for e in next(p for p in d['persons']if p['id']==self.r['yang_hu'])['evidence']if e.get('mention_id')!=mid]
  self.change('registry/persons.json',f);self.reject()
 def test_same_pid_bad_anchor(self):
  def f(ch):
   p,=[p for p in ch['paragraphs']if p['id']==core.CID+':p028'];mm,=[mm for mm in p['mentions']if mm['id']==core.CID+':p028:m0053'];mm['end']+=1
  self.change(core.CH,f);self.reject()
 def test_missing_stage_and_orphan(self):
  target=self.T/m.EP;data=target.read_bytes();target.unlink()
  try:self.reject()
  finally:target.write_bytes(data)
 def test_caller_closure_and_unrelated(self):
  records=self.records();core.guard_bundle(self.T,self.r['yang_hu'],self.people,records)
  partial=[d for d in records if d.get('record_type')!='person_life_event_assertion_set']
  with self.assertRaises(ValueError):core.guard_bundle(self.T,self.r['yang_hu'],self.people,partial)
  people=copy.deepcopy(self.people);people[self.r['yang_hu']]['evidence']=[]
  with self.assertRaises(ValueError):core.guard_bundle(self.T,self.r['yang_hu'],people,records)
  # Unrelated caller retains the original early return without demanding this source.
  core.guard_bundle(self.T,'unrelated-not-a-034-role',{},[])
 def test_caller_wrong_same_person_span(self):
  records=copy.deepcopy(self.records());ch=next(d for d in records if d.get('id')==core.CID);p,=[p for p in ch['paragraphs']if p['id']==core.CID+':p028'];p['mentions'][0]['start']+=1
  with self.assertRaises(ValueError):core.guard_bundle(self.T,self.r['yang_hu'],self.people,records)
 def test_complete_role_rekey_and_single_endpoint_reject(self):
  old=self.r['yang_hu'];all_people=core.read(self.T,'registry/persons.json')['persons'];new='z9q_s8w_v7n';self.assertNotIn(new,{p['id']for p in all_people})
  def walk(v):
   if isinstance(v,str):return new if v==old else v
   if isinstance(v,list):return[walk(x)for x in v]
   if isinstance(v,dict):return{k:walk(x)for k,x in v.items()}
   return v
  # Exact person-valued scalars only; no opaque MID/event/assertion ID rewriting, no historical proof changes.
  for rel in self.original:
   if rel.endswith('.json')and(rel.startswith('corpus/')or rel.startswith('registry/')):
    path=self.T/rel;d=json.loads(path.read_bytes());nd=walk(d)
    if nd!=d:path.write_text(json.dumps(nd,ensure_ascii=False)+'\n')
  b,r,people,ch=core.accepted_state(self.T);self.assertEqual(r['yang_hu'],new);self.assertNotIn(old,people);self.assertEqual(core.read(self.T,m.LP)['events'][0]['person_id'],new)
  m.guard_bundle(self.T,new,people,[ch]+[core.read(self.T,b[k])for k in('names_path','identities_path','groups_path')]+[core.read(self.T,m.LP),core.read(self.T,m.AP)],r,people,ch)
  self.change(m.AP,lambda d:d['assertions'][0].update(person_id=old));self.reject()
