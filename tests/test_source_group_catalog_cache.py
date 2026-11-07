import copy,hashlib,json,os,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from scripts import source_group_catalog_cache as c
from scripts.validation_context import scope
from scripts.profile_title_preferences import PreferenceCatalog
from scripts.liang_xiao_close_family import same

class SourceGroupCatalogCache(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name).resolve();(self.root/'corpus').mkdir();(self.root/'scripts').mkdir();self.raw=self.root/'corpus/raw.txt';self.raw.write_text('received');self.current=self.root/'corpus/current.json';self.current.write_text(json.dumps({'roles':['a','b']}));self.code=self.root/'scripts/proof.py';self.code.write_text('x=1\n');self.calls=0
  reviewed={'scripts/proof.py':hashlib.sha256(self.code.read_bytes()).hexdigest()};digest=hashlib.sha256(json.dumps(reviewed,sort_keys=True,separators=(',',':')).encode()).hexdigest();review=patch.object(c,'_REVIEWED_GUARD_CODE_SHA256',digest);review.start();self.addCleanup(review.stop)
  self.people={p:{'id':p,'evidence':[{'mid':'mid-'+p}]}for p in ['a','b']}
  self.doc={'record_type':'source_person_reference_group_set','owner':'fixture','chapter_id':'chapter','groups':[{'id':'g1','members':[{'person_id':'a'},{'person_id':'b'}],'number':1}],'unresolved_readings':[{'id':'r1','candidate_person_ids':['a'],'subject_person_id':'b'}]};self.records=[copy.deepcopy(self.doc)]
 def builder(self,records=None,people=None):
  records=self.records if records is None else records;people=self.people if people is None else people
  def build():
   self.calls+=1;assert self.raw.read_bytes()==b'received'and self.raw.read_text()=='received';roles=json.loads(self.current.read_bytes())['roles'];expected=copy.deepcopy(self.doc)
   for m,p in zip(expected['groups'][0]['members'],roles):m['person_id']=p
   expected['unresolved_readings'][0].update(candidate_person_ids=[roles[0]],subject_person_id=roles[1]);assert same(list(records),[expected]);assert set(people)==set(roles)
   for p in roles:assert people[p]=={'id':p,'evidence':[{'mid':'mid-'+p}]}
   return list(records)
  return build
 def run_cache(self,records=None,people=None,ids=None):
  records=self.records if records is None else records;people=self.people if people is None else people
  return c.run(self.root,records,people,self.builder(records,people),ids=ids)
 def test_real_internal_class_is_supported_but_distinct_from_list(self):
  pc=PreferenceCatalog(self.records,self.people,self.root)
  with scope(self.root)as state:
   self.run_cache();self.run_cache();self.run_cache(pc);self.run_cache(pc)
   stats=c.statistics(self.root);self.assertEqual(stats['cold_proofs'],2);self.assertEqual(stats['hits'],2);self.assertEqual(len(c.dependencies(self.root)),2)
  self.assertEqual(state['memo'],{});self.assertTrue(state['closed'])
 def test_extra_references_do_not_change_the_ordered_content_key(self):
  with scope(self.root):
   self.run_cache();held=self.records[0]['groups'][0];also_held=self.people['a']
   self.run_cache();self.assertEqual(c.statistics(self.root)['hits'],1);self.assertEqual(self.calls,1)
 def test_cold_certificate_does_not_inherit_legacy_memo(self):
  from scripts.validation_context import _ACTIVE
  old=self.builder()
  def builder():
   self.assertIsNone(_ACTIVE.get());return old()
  with scope(self.root):c.run(self.root,self.records,self.people,builder)
 def test_cold_builder_caller_sideeffect_cannot_issue_certificate(self):
  old=self.builder()
  def builder():
   docs=old();self.people['a']['evidence'].clear();return docs
  with scope(self.root):
   with self.assertRaisesRegex(ValueError,'caller catalog changed'):c.run(self.root,self.records,self.people,builder)
   self.assertEqual(c.dependencies(self.root),{})
 def test_cold_detached_docs_must_match_complete_caller_projection(self):
  old=self.builder()
  def builder():
   docs=copy.deepcopy(old());docs[0]['groups'][0]['number']=2;return docs
  with scope(self.root):
   with self.assertRaisesRegex(ValueError,'result differs'):c.run(self.root,self.records,self.people,builder)
   self.assertEqual(c.dependencies(self.root),{})
 def test_cold_closure_time_caller_change_is_not_certified(self):
  original=c._hash_files
  def changed(root,paths):
   result=original(root,paths);self.records[0]['groups'][0]['id']='g2';return result
  with scope(self.root),patch.object(c,'_hash_files',changed):
   with self.assertRaisesRegex(ValueError,'caller catalog changed'):self.run_cache()
   self.assertEqual(c.dependencies(self.root),{})
 def test_warm_closure_time_caller_change_is_not_a_hit(self):
  original=c._hash_files
  def changed(root,paths):
   result=original(root,paths);self.people['a']['evidence'].clear();return result
  with scope(self.root):
   self.run_cache()
   with patch.object(c,'_hash_files',changed),self.assertRaisesRegex(ValueError,'caller catalog changed'):self.run_cache()
   self.assertEqual(c.statistics(self.root)['hits'],0)
 def test_selected_return_cannot_pollute_private_index(self):
  with scope(self.root):
   groups,readings,related=self.run_cache(ids={'a'});groups[0]['id']='polluted';readings.clear();related.clear()
   groups,readings,related=self.run_cache(ids={'a'});self.assertEqual(groups[0]['id'],'g1');self.assertEqual(len(readings),1);self.assertEqual(related,{'a','b'});self.assertEqual(self.calls,1)
 def test_mutated_caller_same_object_and_unrelated_query_are_not_hits(self):
  with scope(self.root):
   self.run_cache(ids={'unrelated'})
   for kind in ['missing-group','wrong-member','wrong-reverse','bool-int','tuple-list','unknown-owner']:
    records=copy.deepcopy(self.records);people=copy.deepcopy(self.people)
    if kind=='missing-group':records=[]
    elif kind=='wrong-member':records[0]['groups'][0]['members'][0]['person_id']='b'
    elif kind=='wrong-reverse':people['a']['evidence']=[]
    elif kind=='bool-int':records[0]['groups'][0]['number']=True
    elif kind=='tuple-list':records[0]['groups']=tuple(records[0]['groups'])
    else:records[0]['owner']='unknown'
    with self.subTest(kind=kind),self.assertRaises(AssertionError):self.run_cache(records,people,ids={'unrelated'})
   self.records[0]['groups'][0]['id']='g2'
   with self.assertRaises(AssertionError):self.run_cache(ids={'unrelated'})
 def test_reordered_dict_retains_current_observable_output_order(self):
  with scope(self.root):
   self.run_cache();records=copy.deepcopy(self.records);g=records[0]['groups'][0];records[0]['groups'][0]={k:g[k]for k in reversed(g)}
   got=self.run_cache(records,ids={'a'})[0][0];self.assertEqual(list(got),list(records[0]['groups'][0]));self.assertEqual(c.statistics(self.root)['hits'],0)
 def test_same_size_raw_edit_and_restored_mtime_fail(self):
  with scope(self.root):
   self.run_cache();s=self.raw.stat();self.raw.write_text('bad-text');os.utime(self.raw,ns=(s.st_atime_ns,s.st_mtime_ns))
   with self.assertRaises(AssertionError):self.run_cache()
 def test_both_reader_overlays_are_uncached_and_not_old_memo_hits(self):
  for reader in ['read_bytes','read_text']:
   with self.subTest(reader=reader),scope(self.root):
    self.run_cache();original=getattr(Path,reader)
    def injected(p,*a,**k):return(b'bad-text'if reader=='read_bytes'else'bad-text')if p==self.raw else original(p,*a,**k)
    with patch.object(Path,reader,injected),self.assertRaises(AssertionError):self.run_cache(ids={'unrelated'})
 def test_code_and_membership_changes_invalidate(self):
  with scope(self.root):
   self.run_cache();self.code.write_text('x=2\n');self.run_cache();self.assertEqual(self.calls,2);self.assertEqual(c.statistics(self.root)['hits'],0)
  with scope(self.root):
   self.run_cache();(self.root/'corpus/new.json').write_text('{}');self.run_cache();self.assertEqual(c.statistics(self.root)['hits'],0)
 def test_arbitrary_subclass_falls_back_and_keeps_original_behaviour(self):
  class Other(list):pass
  with scope(self.root):
   self.run_cache(Other(self.records));self.run_cache(Other(self.records));self.assertEqual(self.calls,2);self.assertEqual(c.statistics(self.root)['hits'],0)
 def test_coherent_rekey_then_endpoint_or_reverse_loss(self):
  with scope(self.root):
   self.run_cache();before=hashlib.sha256(self.raw.read_bytes()).hexdigest();records=copy.deepcopy(self.records);people={p:{'id':p,'evidence':[{'mid':'mid-'+p}]}for p in ['x','y']};self.current.write_text(json.dumps({'roles':['x','y']}))
   for m,p in zip(records[0]['groups'][0]['members'],['x','y']):m['person_id']=p
   records[0]['unresolved_readings'][0].update(candidate_person_ids=['x'],subject_person_id='y');got=self.run_cache(records,people,ids={'x'});self.assertEqual(got[2],{'x','y'});self.assertEqual(hashlib.sha256(self.raw.read_bytes()).hexdigest(),before)
   bad=copy.deepcopy(records);bad[0]['groups'][0]['members'][0]['person_id']='a'
   with self.assertRaises(AssertionError):self.run_cache(bad,people,ids={'unrelated'})
   people['x']['evidence']=[]
   with self.assertRaises(AssertionError):self.run_cache(records,people,ids={'unrelated'})
 def test_unproved_external_read_does_not_create_cache(self):
  with tempfile.NamedTemporaryFile()as external,scope(self.root):
   old=self.builder()
   def builder():Path(external.name).read_bytes();return old()
   for _ in range(2):c.run(self.root,self.records,self.people,builder)
   self.assertEqual(c.dependencies(self.root),{});self.assertEqual(self.calls,2)

class ActualPreferenceCatalogCallerDrift(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  from scripts.person_bundle import load_catalog
  cls.root=Path(__file__).resolve().parents[1];cls.people,cls.records=load_catalog(cls.root);cls.pid='8jz_o3s_obt'
  assert type(cls.records)is PreferenceCatalog
 def test_actual_PC_cold_callback_sideeffect_rejects_without_certificate(self):
  from scripts import source_person_reference_groups as groups
  original=groups._validated_sets_uncached;label=self.people[self.pid]['label']
  def changed(records,people,root):
   result=original(records,people,root);people[self.pid]['label']=label+' changed';return result
  try:
   with scope(self.root),patch.object(groups,'_validated_sets_uncached',changed):
    with self.assertRaisesRegex(ValueError,'caller catalog changed'):groups.validated_sets(self.records,self.people,self.root)
    self.assertEqual(c.dependencies(self.root),{})
  finally:self.people[self.pid]['label']=label
 def test_actual_PC_cold_closure_sideeffect_rejects_without_certificate(self):
  from scripts import source_person_reference_groups as groups
  original=c._hash_files;label=self.people[self.pid]['label']
  def changed(root,paths):
   result=original(root,paths);self.people[self.pid]['label']=label+' changed';return result
  try:
   with scope(self.root),patch.object(c,'_hash_files',changed):
    with self.assertRaisesRegex(ValueError,'caller catalog changed'):groups.validated_sets(self.records,self.people,self.root)
    self.assertEqual(c.dependencies(self.root),{})
  finally:self.people[self.pid]['label']=label
 def test_actual_PC_warm_closure_sideeffect_rejects_instead_of_hit(self):
  from scripts import source_person_reference_groups as groups
  original=c._hash_files;label=self.people[self.pid]['label']
  def changed(root,paths):
   result=original(root,paths);self.people[self.pid]['label']=label+' changed';return result
  try:
   with scope(self.root):
    groups.validated_sets(self.records,self.people,self.root)
    with patch.object(c,'_hash_files',changed),self.assertRaisesRegex(ValueError,'caller catalog changed'):groups.for_people(self.records,self.people,self.root,{self.pid})
    self.assertEqual(c.statistics(self.root)['hits'],0)
  finally:self.people[self.pid]['label']=label

if __name__=='__main__':unittest.main()
