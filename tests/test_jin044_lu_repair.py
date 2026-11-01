"""Source semantics and caller consistency, separately from source capture integrity."""
import copy,json,os,unittest
from pathlib import Path
from tests.test_jin044_lu_native import Jin044LuTests,ROOT
from scripts.fixed_jin044_lu_rendered import CH,REF,proof,guard_bundle,errors
from scripts.person_bundle import load_catalog,bundle
class IdentityRepairTests(unittest.TestCase):
 setUp=Jin044LuTests.setUp
 read=Jin044LuTests.read
 write=Jin044LuTests.write
 def test_song_actor_is_not_jin_captor_even_with_complete_new_reverse(self):
  c,r=proof(self.root);new=r['$liucan'];b=self.read(REF);s=b['identity_exclusion_seeds']['liucan'];oldch=self.read(s['path']);old=next(m['person_id']for p in oldch['paragraphs']for m in p['mentions']if m['id']==s['marker']['id']);people=self.read('registry/persons.json');fresh=next(p for p in people['persons']if p['id']==new);actor=next(p for p in people['persons']if p['id']==old);actor['evidence']+=fresh['evidence']
  for a in fresh['aliases']:
   target=next((x for x in actor['aliases']if x['surface']==a['surface']),None)
   if target:target['mention_ids']+=a['mention_ids']
   else:actor['aliases'].append(a)
  people['persons']=[p for p in people['persons']if p['id']!=new];self.write('registry/persons.json',people)
  def relink(x):
   if isinstance(x,str):return old if x==new else x
   if isinstance(x,list):return[relink(v)for v in x]
   if isinstance(x,dict):return{k:relink(v)for k,v in x.items()}
   return x
  for f in self.root.rglob('*.json'):
   if f==self.root/REF:continue
   self.write(str(f.relative_to(self.root)),relink(json.loads(f.read_text())))
  fixed=self.read(CH);self.assertEqual(sum(m['person_id']==old for p in fixed['paragraphs']for m in p['mentions']),5)
  self.assertTrue(errors(fixed,self.root))
 def test_lin_is_qualified_inference_not_literal_grandfather(self):
  c,r=proof(self.root);families=self.read('registry/family-assemblies.json');row=next(m for f in families['assemblies']for m in f['members']if m['person_id']==r['$lin']);con=row['ancestor_connection'];self.assertIs(row['parent_person_id'],None);self.assertFalse(con['same_father_independently_attested']);self.assertFalse(con['literal_grandfather_assertion']);self.assertFalse(con['father_is_hao_asserted']);self.assertEqual(len(con['references']),2)
  con['same_father_independently_attested']=True;self.write('registry/family-assemblies.json',families);self.assertTrue(errors(c,self.root))
class CallerConsistencyTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.catalog=load_catalog(ROOT);cls.chapter,cls.roles=proof(ROOT)
 def setUp(self):self.people=copy.deepcopy(self.catalog[0]);self.records=copy.deepcopy(list(self.catalog[1]))
 def call(self,pid=None):return guard_bundle(ROOT,pid or self.roles['$fu'],self.people,self.records)
 def test_normal_caller_passes(self):self.call()
 def test_single_caller_endpoint_rejected_for_original_person(self):
  ch=next(r for r in self.records if r.get('id')==self.__class__.chapter['id']);ch['paragraphs'][2]['mentions'][0]['person_id']=self.roles['$qin'];self.assertRaises(ValueError,self.call)
 def test_single_caller_endpoint_rejected_for_foreign_query_person(self):
  physical=self.__class__.chapter;b=json.loads((ROOT/REF).read_text());seed=b['identity_exclusion_seeds']['liucan'];source=json.loads((ROOT/seed['path']).read_text());old=next(m['person_id']for p in source['paragraphs']for m in p['mentions']if m['id']==seed['marker']['id']);ch=next(r for r in self.records if r.get('id')==physical['id']);ch['paragraphs'][2]['mentions'][0]['person_id']=old;self.assertRaises(ValueError,self.call,old)
 def test_missing_current_reverse_rejected(self):
  pid=self.roles['$fu'];actor=self.people[pid];actor['evidence']=[e for e in actor['evidence']if e.get('chapter_id')!=self.__class__.chapter['id']];self.assertRaises(ValueError,self.call)
 def test_missing_caller_sidecar_rejected(self):
  self.records=[r for r in self.records if not(r.get('chapter_id')==self.__class__.chapter['id']and r.get('record_type')=='title_holding_assertion_set')];self.assertRaises(ValueError,self.call)
 def test_unknown_owner_rejected(self):
  ch=next(r for r in self.records if r.get('id')==self.__class__.chapter['id']);ch['id']='c-foreign-owner';self.assertRaises(ValueError,self.call)
 def test_bool_number_coercion_rejected(self):
  ch=next(r for r in self.records if r.get('id')==self.__class__.chapter['id']);ch['source']['image_verified']=0;self.assertRaises(ValueError,self.call)
