"""Checkpoint transport tests; synthetic outputs are explicitly not source proofs."""
import importlib.util,json,os,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from scripts import validation_context as context
from scripts import person_export_checkpoint as c

class CheckpointTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
  self.base=Path(self.temp.name);self.root=self.base/'root';self.root.mkdir()
  for rel in ('registry/persons.json','data/works/index.json','data/corpus/input.json','scripts/code.py'):
   p=self.root/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('{}')
  (self.root/'exports/persons').mkdir(parents=True)
  self.ids=['aaa_aaa_aaa','bbb_bbb_bbb','ccc_ccc_ccc'];self.cp=self.base/'checkpoint'
 def source(self):return c.SourceSnapshot(self.root,context.fingerprint(self.root),[self.root/'scripts'])
 def checkpoint(self,resume=False,**kw):return c.PersonExportCheckpoint(self.root,self.cp,self.source(),self.ids,self.ids,resume=resume,batch_size=kw.pop('batch_size',2),**kw)
 def text(self,pid):return json.dumps({'record_type':'person_source_bundle','requested_person_id':pid,'person_ids':[pid],'value':'測試'})+'\n'
 def put(self,cp,pid):cp.write_output(pid,self.text(pid));cp.mark(pid)
 def test_bounded_commit_interruption_tail_and_exact_reuse(self):
  cp=self.checkpoint();self.put(cp,self.ids[0]);self.assertEqual(list((self.cp/'batches').iterdir()),[])
  self.put(cp,self.ids[1]);self.put(cp,self.ids[2]) # final pending batch is deliberately interrupted
  resumed=self.checkpoint(True)
  self.assertEqual(set(resumed.completed),set(self.ids[:2]))
  for pid in self.ids[:2]:self.assertEqual(resumed.reuse(pid),json.loads(self.text(pid)))
  self.assertIsNone(resumed.reuse(self.ids[2]));self.put(resumed,self.ids[2]);resumed.finish()
  self.assertEqual(set(self.checkpoint(True).completed),set(self.ids))
 def test_content_code_and_membership_drift_reject_resume(self):
  for kind in ('source','code','membership','dataworks'):
   with self.subTest(kind=kind):
    cp=self.checkpoint();self.put(cp,self.ids[0]);cp.finish()
    p={'source':'registry/persons.json','code':'scripts/code.py','membership':'registry/new.json','dataworks':'data/works/index.json'}[kind]
    target=self.root/p;old=target.read_bytes()if target.exists()else None;target.write_text('{"changed":1}')
    with self.assertRaises(ValueError):self.checkpoint(True)
    if old is None:target.unlink()
    else:target.write_bytes(old)
    import shutil;shutil.rmtree(self.cp)
 def test_same_content_rewrite_mtime_is_not_durable_identity(self):
  cp=self.checkpoint();self.put(cp,self.ids[0]);cp.finish()
  p=self.root/'registry/persons.json';p.write_bytes(p.read_bytes())
  self.assertIsNotNone(self.checkpoint(True).reuse(self.ids[0]))
 def test_in_run_change_and_restore_detected_no_pending_commit(self):
  cp=self.checkpoint();self.put(cp,self.ids[0]);p=self.root/'registry/persons.json';old=p.read_bytes();p.write_text('changed');p.write_bytes(old)
  with self.assertRaises(ValueError):cp.finish()
  self.assertEqual(list((self.cp/'batches').iterdir()),[])
 def test_corrupt_missing_and_wrong_owner_output_recompute(self):
  cp=self.checkpoint();self.put(cp,self.ids[0]);cp.finish();p=cp.output_path(self.ids[0])
  for raw in (b'{',self.text(self.ids[1]).encode()):
   p.write_bytes(raw);self.assertIsNone(self.checkpoint(True).reuse(self.ids[0]))
  p.unlink();self.assertIsNone(self.checkpoint(True).reuse(self.ids[0]))
  resumed=self.checkpoint(True);self.put(resumed,self.ids[0]);resumed.finish()
  self.assertIsNotNone(self.checkpoint(True).reuse(self.ids[0]))
 def test_truncated_header_and_batch_are_explicit_errors(self):
  cp=self.checkpoint();self.put(cp,self.ids[0]);cp.finish()
  for p in [self.cp/'header.json',next((self.cp/'batches').glob('batch-*.json'))]:
   raw=p.read_bytes();p.write_bytes(b'{')
   with self.assertRaises(ValueError):self.checkpoint(True)
   p.write_bytes(raw)
 def test_unowned_legacy_outputs_never_form_checkpoint(self):
  (self.root/'exports/persons'/f'{self.ids[0]}.json').write_text(self.text(self.ids[0]))
  with self.assertRaises(ValueError):self.checkpoint(True)
  cp=self.checkpoint();self.assertIsNone(cp.reuse(self.ids[0]))
 def test_atomic_replace_failure_preserves_receipt_and_recomputes_batch(self):
  cp=self.checkpoint();self.put(cp,self.ids[0]);header=(self.cp/'header.json').read_bytes()
  with patch.object(c.os,'replace',side_effect=OSError('injected interruption')):
   with self.assertRaises(OSError):cp.finish()
  self.assertEqual((self.cp/'header.json').read_bytes(),header);self.assertEqual(list((self.cp/'batches').iterdir()),[])
  self.assertIsNone(self.checkpoint(True).reuse(self.ids[0]));cp.finish()
 def test_paths_owner_membership_and_batch_bounds(self):
  for v in (True,False,0,-1,65,1.5):
   with self.assertRaises(ValueError):self.checkpoint(batch_size=v)
  with self.assertRaises(ValueError):c.validate_options(self.root,self.root/'inside',False,32)
  cp=self.checkpoint()
  for pid in ('../escape','zzz_zzz_zzz'):
   with self.assertRaises(ValueError):cp.write_output(pid,'{}')
  p=self.root/'exports/persons'/f'{self.ids[0]}.json';p.symlink_to(self.root/'registry/persons.json')
  with self.assertRaises(ValueError):cp.write_output(self.ids[0],self.text(self.ids[0]))
  p.unlink();self.put(cp,self.ids[0]);cp.finish()
  batch=next((self.cp/'batches').glob('batch-*.json'));d=json.loads(batch.read_text());d['owner_token']='0'*32;batch.write_text(json.dumps(d))
  with self.assertRaises(ValueError):self.checkpoint(True)
 def test_wrong_root_membership_and_symlink_checkpoint_refused(self):
  source=self.source();other=self.base/'other';(other/'exports/persons').mkdir(parents=True)
  with self.assertRaises(ValueError):c.PersonExportCheckpoint(other,self.cp,source,self.ids,self.ids)
  cp=self.checkpoint();self.put(cp,self.ids[0]);cp.finish()
  with self.assertRaises(ValueError):c.PersonExportCheckpoint(self.root,self.cp,self.source(),self.ids[:2],self.ids,resume=True,batch_size=2)
  link=self.base/'link';link.symlink_to(self.cp,target_is_directory=True)
  with self.assertRaises(ValueError):c.validate_options(self.root,link,True,2)
 def test_late_dependency_change_safely_rejects_core_checkpoint(self):
  cp=self.checkpoint();self.put(cp,self.ids[0]);cp.finish()
  (self.root/'data/corpus/profile.json').write_text('{}')
  with self.assertRaises(ValueError):self.checkpoint(True)

if __name__=='__main__':unittest.main()
