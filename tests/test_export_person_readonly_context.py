import json,unittest,tempfile,os,importlib.util,sys
from pathlib import Path
from unittest.mock import patch
from scripts import validation_context as c
from scripts import calendar_wiring,reading_catalog,table_person_profiles
if os.environ.get('CBR_EXPORTER_CANDIDATE'):
 spec=importlib.util.spec_from_file_location('scripts.export_person_context_candidate',os.environ['CBR_EXPORTER_CANDIDATE']);e=importlib.util.module_from_spec(spec);spec.loader.exec_module(e)
else:
 from scripts import export_person_bundles as e

class ExportReadonlyContextTests(unittest.TestCase):
 def run_export(self,root,shared=True,mutation=None,fail=False):
  calls=[];proof_calls=[]
  @c.memoized(0)
  def proof(r):proof_calls.append(str(r));return {'ok':['original']}
  def calendar(r):
   self.assertIsNone(c._ACTIVE.get());calls.append('calendar');(r/'data/corpus/calendar.json').write_text('{"calendar":true}')
  def core(r):
   calls.append('core');state=c._ACTIVE.get();self.assertEqual(state is not None,shared)
   first=proof(r);first['ok'].append('caller edit');self.assertEqual(proof(r),{'ok':['original']})
   d=r/'exports/persons';d.mkdir(parents=True,exist_ok=True);(d/'one.json').write_text('{"person":true}')
   if mutation:mutation(r)
   if fail:raise ValueError('original core error')
   return [{'person_id':'example'}]
  def reader(root):self.assertIsNone(c._ACTIVE.get());calls.append('reader');(root/'data/corpus/reader.json').write_text('{}')
  def profiles(r):self.assertIsNone(c._ACTIVE.get());calls.append('profiles');(r/'data/corpus/profiles.json').write_text('{}')
  cw,rc,tp=(calendar_wiring,reading_catalog,table_person_profiles)if e.__package__=='scripts'else tuple(importlib.import_module(n)for n in ('calendar_wiring','reading_catalog','table_person_profiles'))
  with patch.object(cw,'export_calendar_contexts',calendar),patch.object(e,'_export_person_outputs',core),patch.object(rc,'run',reader),patch.object(tp,'build',profiles):e.export(root,shared_context=shared)
  return calls,proof_calls
 def fixture(self,root):
  for rel in ['data/corpus/native.json','registry/persons.json','data/historical-tables/person-candidates.json','scripts/dynamic_seed.py']:
   p=root/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('{}')
 def test_writes_are_outside_shared_context_and_new_call_is_fresh(self):
  with tempfile.TemporaryDirectory()as td:
   root=Path(td);self.fixture(root)
   for _ in range(2):
    calls,proofs=self.run_export(root);self.assertEqual(calls,['calendar','core','reader','profiles']);self.assertEqual(len(proofs),1);self.assertIsNone(c._ACTIVE.get())
 def test_disabled_reference_mode_keeps_outputs_and_runs_proof_each_time(self):
  with tempfile.TemporaryDirectory()as td:
   root=Path(td);self.fixture(root);calls,proofs=self.run_export(root,shared=False);self.assertEqual(len(proofs),2);self.assertEqual(calls,['calendar','core','reader','profiles'])
 def test_parent_context_not_inherited_by_write_phases_and_restored(self):
  with tempfile.TemporaryDirectory()as td:
   root=Path(td);self.fixture(root)
   with c.scope(root)as outer:
    self.run_export(root);self.assertIs(c._ACTIVE.get(),outer);self.assertEqual(outer['memo'],{})
   self.assertTrue(outer['closed'])
 def test_registry_byte_drift_rejected_before_downstream(self):
  with tempfile.TemporaryDirectory()as td:
   root=Path(td);self.fixture(root)
   with self.assertRaisesRegex(ValueError,c.DRIFT_ERROR):self.run_export(root,mutation=lambda r:(r/'registry/persons.json').write_text('{"changed":true}'))
   self.assertIsNone(c._ACTIVE.get());self.assertFalse((root/'data/corpus/reader.json').exists())
 def test_membership_addition_and_deletion_are_rejected(self):
  for change in ['add','delete']:
   with tempfile.TemporaryDirectory()as td:
    root=Path(td);self.fixture(root)
    def mutate(r):
     if change=='add':(r/'data/corpus/new.json').write_text('{}')
     else:(r/'data/corpus/native.json').unlink()
    with self.assertRaisesRegex(ValueError,c.DRIFT_ERROR):self.run_export(root,mutation=mutate)
    self.assertIsNone(c._ACTIVE.get())
 def test_dynamic_source_script_drift_rejected(self):
  with tempfile.TemporaryDirectory()as td:
   root=Path(td);self.fixture(root)
   with self.assertRaisesRegex(ValueError,c.DRIFT_ERROR):self.run_export(root,mutation=lambda r:(r/'scripts/dynamic_seed.py').write_text('different'))
 def test_original_exception_preserved_and_memo_released(self):
  with tempfile.TemporaryDirectory()as td:
   root=Path(td);self.fixture(root)
   with self.assertRaisesRegex(ValueError,'original core error'):self.run_export(root,fail=True)
   self.assertIsNone(c._ACTIVE.get());self.assertFalse((root/'data/corpus/reader.json').exists())
 def test_direct_script_import_uses_same_existing_context(self):
  scripts_dir=Path(c.__file__).parent;sys.path.insert(0,str(scripts_dir))
  try:
   spec=importlib.util.spec_from_file_location('export_person_direct_import_test',e.__file__);direct=importlib.util.module_from_spec(spec);spec.loader.exec_module(direct)
   with tempfile.TemporaryDirectory()as td:
    root=Path(td);self.fixture(root)
    with patch.dict(globals(),{'e':direct}):calls,proofs=self.run_export(root)
    self.assertEqual(calls,['calendar','core','reader','profiles']);self.assertEqual(len(proofs),1)
   self.assertIsNone(c._ACTIVE.get())
  finally:sys.path.pop(0)
if __name__=='__main__':unittest.main()
