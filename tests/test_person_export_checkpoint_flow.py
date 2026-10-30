"""Normal core-loop orchestration with synthetic catalog transport, not historical evidence."""
import json,tempfile,unittest,copy
from pathlib import Path
from unittest.mock import patch
from scripts import export_person_bundles as e,calendar_wiring,validate_corpus,reading_catalog,table_person_profiles,formal_source_citations

class FlowTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
  self.base=Path(self.temp.name);self.root=self.base/'source';self.root.mkdir();self.cp=self.base/'checkpoint'
  # Real pure reader preflight needs a valid empty catalog, even in this
  # explicitly synthetic checkpoint-transport fixture. Do not mock the reader.
  minimal={'registry/persons.json':{'persons':[]},'registry/works.json':{'works':[]},
   'corpus/progress.json':{'books':[]},'data/corpus/shiji-contents.json':{'chapters':[],'source':'synthetic transport only'},
   'data/corpus/chapter-directory.json':{'works':[]},'data/historical-tables/index.json':{'tables':[]}}
  for rel,value in minimal.items():
   path=self.root/rel;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(value))
  self.ids=['aaa_aaa_aaa','bbb_bbb_bbb','ccc_ccc_ccc','ddd_ddd_ddd']
  self.people={pid:{'id':pid,'label':'明確測試人物'+pid,'status':'source_attested','aliases':[],'evidence':[]}for pid in self.ids}
  self.people[self.ids[0]]['id_aliases']=['eee_eee_eee'];self.calls=[]
 def result(self,pid):return {'record_type':'person_source_bundle','requested_person_id':pid,'person_ids':[pid],'identity_policy':{},'family_tree_decisions':[],'source_mention_summary':[],'mentions':[],'table_occurrences':[],'sources':[],'most_mentioned_source_ids':[]}
 def run_export(self,checkpoint=False,resume=False,interrupt=None,downstream=False):
  def bundle(pid,**kwargs):
   self.calls.append(pid)
   if interrupt is not None and len(self.calls)==interrupt:raise RuntimeError('simulated interrupt before bundle completion')
   return self.result(pid)
  if downstream:
   path=self.root/'data/historical-tables/person-candidates.json';path.parent.mkdir(parents=True,exist_ok=True);path.write_text('{}')
  with patch.object(e,'load_catalog',return_value=(self.people,[])),patch.object(e,'load_assemblies',return_value=({},{})),patch.object(e,'bundle',side_effect=bundle),patch.object(formal_source_citations,'load_citation_index',return_value={}),patch.object(calendar_wiring,'export_calendar_contexts')as cal,patch.object(validate_corpus,'validate',return_value=[])as validator,patch.object(reading_catalog,'run')as reader,patch.object(table_person_profiles,'build')as profiles:
   e.export(self.root,**({'checkpoint_dir':self.cp,'resume':resume,'checkpoint_batch_size':2}if checkpoint else {}))
   return {'validate':validator.call_count,'calendar':cal.call_count,'reader':reader.call_count,'profiles':profiles.call_count}
 def outputs(self):return {p.name:p.read_bytes()for p in (self.root/'exports/persons').iterdir()}
 def test_interrupted_resume_matches_complete_core_index_alias_and_rebuilds_alias(self):
  self.run_export();expected=self.outputs();self.calls=[]
  with self.assertRaises(RuntimeError):self.run_export(True,interrupt=4)
  self.calls=[];counts=self.run_export(True,True)
  self.assertEqual(self.outputs(),expected)
  self.assertEqual(self.calls,self.ids[2:]+[self.ids[0]]) # aliases always freshly bundled
  self.assertEqual(counts['validate'],1)
 def test_default_skips_new_validation_and_checkpoint_rebuilds_downstream(self):
  self.assertEqual(self.run_export(downstream=True),{'validate':0,'calendar':1,'reader':1,'profiles':1})
  self.calls=[];self.assertEqual(self.run_export(True,downstream=True),{'validate':1,'calendar':1,'reader':1,'profiles':1})
  self.calls=[];self.assertEqual(self.run_export(True,True,downstream=True),{'validate':1,'calendar':1,'reader':1,'profiles':1})
  self.assertEqual(self.calls,[self.ids[0]])
 def test_core_only_repository_does_not_request_reader_inputs(self):
  with tempfile.TemporaryDirectory()as tmp:
   root=Path(tmp)
   self.assertFalse((root/'data/historical-tables/person-candidates.json').exists())
   with patch.object(calendar_wiring,'export_calendar_contexts')as calendar,patch.object(e,'_export_person_outputs',return_value=[])as core,patch.object(reading_catalog,'outputs',side_effect=AssertionError('disabled reader must not be requested'))as preflight,patch.object(reading_catalog,'run')as reader,patch.object(table_person_profiles,'build')as profiles:
    e.export(root)
   calendar.assert_called_once_with(root);core.assert_called_once_with(root);preflight.assert_not_called();reader.assert_not_called();profiles.assert_not_called()
 def test_invalid_options_rejected_before_calendar_or_source_writes(self):
  for value in (True,0,65,32.0):
   with patch.object(calendar_wiring,'export_calendar_contexts')as cal:
    with self.assertRaises(ValueError):e.export(self.root,checkpoint_batch_size=value)
    cal.assert_not_called()
 def test_source_validation_failure_cannot_reuse_completed_outputs(self):
  self.run_export(True);self.calls=[]
  with patch.object(calendar_wiring,'export_calendar_contexts'),patch.object(validate_corpus,'validate',return_value=['real source guard rejected']):
   with self.assertRaisesRegex(ValueError,'real source guard rejected'):e.export(self.root,checkpoint_dir=self.cp,resume=True,checkpoint_batch_size=2)
  self.assertEqual(self.calls,[])

 def test_live_source_content_change_refuses_resume_before_any_bundle(self):
  self.run_export(True);self.calls=[]
  (self.root/'registry/persons.json').write_text('{"persons":[],"changed_source":true}')
  with self.assertRaises(ValueError):self.run_export(True,True)
  self.assertEqual(self.calls,[])
 def test_complete_uid_rekey_never_resurrects_previous_checkpoint_people(self):
  self.run_export(True);old=list(self.ids);self.calls=[]
  self.ids=['fff_fff_fff','ggg_ggg_ggg','hhh_hhh_hhh','iii_iii_iii']
  self.people={pid:{'id':pid,'label':'明確改號測試人物'+pid,'status':'source_attested','aliases':[],'evidence':[]}for pid in self.ids}
  self.people[self.ids[0]]['id_aliases']=['jjj_jjj_jjj']
  (self.root/'registry/persons.json').write_text(json.dumps({'persons':list(self.people.values())}))
  with self.assertRaises(ValueError):self.run_export(True,True)
  self.assertEqual(self.calls,[])
  self.cp=self.base/'new-checkpoint-after-rekey';self.run_export(True)
  actual=self.outputs();index=json.loads(actual['index.json'])
  self.assertEqual({r['person_id']for r in index['persons']},set(self.ids))
  for pid in old:self.assertNotIn(pid+'.json',actual)
  for pid in self.ids:self.assertEqual(json.loads(actual[pid+'.json'])['person_ids'],[pid])

class ActualReaderPreflightTests(unittest.TestCase):
 """Actual received corpus, readonly overlays; only writers/core are stubbed."""
 @classmethod
 def setUpClass(cls):
  import hashlib
  cls.root=Path(__file__).resolve().parents[1]
  cls.progress_path=cls.root/'corpus/progress.json'
  cls.progress_bytes=cls.progress_path.read_bytes()
  cls.progress=json.loads(cls.progress_bytes)
  cls.chapter_path=cls.root/'corpus/liangshu/041-wanggui-ws1512987.json'
  cls.chapter_bytes=cls.chapter_path.read_bytes()
  cls.source_sha=hashlib.sha256(cls.chapter_bytes).hexdigest()
  cls.generic_id=json.loads(cls.chapter_bytes)['id']
  cls.shiji_id=json.loads((cls.root/'corpus/shiji/001.json').read_bytes())['id']
 def exercise(self,*,missing=None,checkpoint=False,shared=True):
  import hashlib,contextlib
  from scripts import validation_context as context
  events=[];core_states=[]
  data=copy.deepcopy(self.progress)
  if missing is not None:
   data['books']=[row for row in data['books']if row['chapter_id']!=missing]
   self.assertEqual(len(data['books']),len(self.progress['books'])-1)
  original=Path.read_text
  def readonly_read(path,*args,**kwargs):
   if path.resolve()==self.progress_path.resolve():
    events.append('reader_inputs');self.assertIsNone(context._ACTIVE.get())
    return json.dumps(data,ensure_ascii=False)
   return original(path,*args,**kwargs)
  def calendar(root):self.assertEqual(root,self.root);events.append('calendar');self.assertIsNone(context._ACTIVE.get())
  def core(root,**kwargs):
   self.assertEqual(root,self.root);events.append('core');state=context._ACTIVE.get();core_states.append(state)
   self.assertEqual(state is not None,shared);return []
  def post_reader(*,root):self.assertEqual(root,self.root);events.append('post_reader');self.assertIsNone(context._ACTIVE.get())
  def post_profiles(root):self.assertEqual(root,self.root);events.append('post_profiles');self.assertIsNone(context._ACTIVE.get())
  self.assertTrue((self.root/'data/historical-tables/person-candidates.json').is_file())
  with tempfile.TemporaryDirectory()as tmp,contextlib.ExitStack()as stack:
   cp=Path(tmp)/'not-created-checkpoint'
   stack.enter_context(patch.object(Path,'read_text',readonly_read))
   stack.enter_context(patch.object(Path,'write_text',side_effect=AssertionError('reader preflight wrote a file')))
   stack.enter_context(patch.object(Path,'write_bytes',side_effect=AssertionError('reader preflight wrote a file')))
   stack.enter_context(patch.object(calendar_wiring,'export_calendar_contexts',side_effect=calendar))
   core_spy=stack.enter_context(patch.object(e,'_export_person_outputs',side_effect=core))
   reader_spy=stack.enter_context(patch.object(reading_catalog,'run',side_effect=post_reader))
   profile_spy=stack.enter_context(patch.object(table_person_profiles,'build',side_effect=post_profiles))
   # Wrap, never fake, the actual fingerprint: failure must precede it entirely.
   fingerprint=stack.enter_context(patch.object(context,'fingerprint',wraps=context.fingerprint))
   if missing is not None:
    with self.assertRaises(KeyError)as failure:e.export(self.root,shared_context=shared,**({'checkpoint_dir':cp}if checkpoint else{}))
    self.assertEqual(failure.exception.args,(missing,));core_spy.assert_not_called();reader_spy.assert_not_called();profile_spy.assert_not_called();fingerprint.assert_not_called();self.assertFalse(cp.exists());self.assertEqual(events,['calendar','reader_inputs'])
   else:
    e.export(self.root,shared_context=shared);self.assertEqual(events,['calendar','reader_inputs','core','post_reader','post_profiles']);self.assertEqual(fingerprint.call_count,2)
    self.assertEqual(core_spy.call_count,1);self.assertEqual(reader_spy.call_count,1);self.assertEqual(profile_spy.call_count,1)
  self.assertIsNone(context._ACTIVE.get())
  for state in core_states:
   if state is not None:self.assertTrue(state['closed']);self.assertEqual(state['memo'],{})
  self.assertEqual(self.progress_path.read_bytes(),self.progress_bytes);self.assertEqual(self.chapter_path.read_bytes(),self.chapter_bytes);self.assertEqual(hashlib.sha256(self.chapter_path.read_bytes()).hexdigest(),self.source_sha)
 def test_actual_generic_missing_progress_fails_before_core_or_checkpoint(self):
  self.exercise(missing=self.generic_id,checkpoint=True)
 def test_actual_shiji_missing_progress_fails_before_core(self):
  self.exercise(missing=self.shiji_id)
 def test_actual_valid_reader_input_keeps_core_and_postwriters_order(self):
  self.exercise()
 def test_actual_valid_reader_input_preserves_disabled_shared_context(self):
  self.exercise(shared=False)

if __name__=='__main__':unittest.main()
