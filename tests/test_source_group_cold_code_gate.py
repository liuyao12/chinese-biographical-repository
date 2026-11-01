"""Cold approval must bind the code pins actually entering the certificate."""
import contextvars,hashlib,json,pathlib,sys,tempfile,threading,unittest
from unittest.mock import patch
from scripts import source_group_catalog_cache as c
from scripts.validation_context import scope

class ColdCodeGate(unittest.TestCase):
 def scenario(self,attack=None):
  with tempfile.TemporaryDirectory()as td:
   root=pathlib.Path(td).resolve();(root/'scripts').mkdir();(root/'corpus').mkdir();code=root/'scripts/zzz_guard.py';code.write_text('value=1\n');raw=root/'corpus/received.txt';raw.write_text('received')
   pins={'scripts/zzz_guard.py':hashlib.sha256(code.read_bytes()).hexdigest()};digest=hashlib.sha256(json.dumps(pins,sort_keys=True,separators=(',',':')).encode()).hexdigest();doc={'record_type':'source_person_reference_group_set','owner':'fixture','chapter_id':'fixture','groups':[],'unresolved_readings':[]};records=[doc];people={'abc_def_123':{'id':'abc_def_123'}};calls=[];ready=threading.Event();done=threading.Event();state={'armed':False,'fired':False,'active':True}
   def writer():
    ready.wait()
    if attack=='rewrite-during-build':code.write_text('value=2\n')
    else:(root/'scripts/new_guard.py').write_text('new_guard=1\n')
    done.set()
   worker=threading.Thread(target=lambda:contextvars.Context().run(writer))if attack else None
   if worker:worker.start()
   if attack=='add-after-enumeration':
    def observe(event,args):
     if state['active']and state['armed']and not state['fired']and event=='open'and pathlib.Path(str(args[0]))==code:
      state['fired']=True;ready.set();done.wait()
    sys.addaudithook(observe)
   def builder():
    calls.append(1);assert raw.read_text()=='received'
    if len(calls)==1:
     if attack=='rewrite-during-build':ready.set();done.wait();worker.join()
     if attack=='add-after-enumeration':state['armed']=True
    return records
   try:
    # Test-only approval of this real tiny code set, not a mocked gate/reader.
    with patch.object(c,'_REVIEWED_GUARD_CODE_SHA256',digest),scope(root):
     self.assertTrue(c._reviewed_code_ok(root));first=c.run(root,records,people,builder);deps=c.dependencies(root);after_gate=c._reviewed_code_ok(root);second=c.run(root,records,people,builder);stats=c.statistics(root);self.assertEqual(first,second)
     if attack:
      self.assertFalse(after_gate);self.assertEqual(deps,{});self.assertEqual(stats['hits'],0);self.assertEqual(stats['fallbacks'].get('code_approval_changed_during_cold'),1);self.assertGreaterEqual(len(calls),2)
     else:self.assertTrue(after_gate);self.assertEqual(len(deps),1);self.assertEqual(stats['hits'],1);self.assertEqual(len(calls),1)
   finally:
    state['active']=False
    if worker and worker.is_alive():ready.set();worker.join()
 def test_unchanged_reviewed_code_remains_cold_then_warm(self):self.scenario()
 def test_external_unread_code_rewrite_during_cold_no_certificate(self):self.scenario('rewrite-during-build')
 def test_external_new_code_after_enumeration_no_certificate(self):self.scenario('add-after-enumeration')
 def test_unrelated_data_file_membership_remains_original_invalidation(self):
  # Existing suite owns full membership/output behaviour; this is a control on
  # exact-code pin comparison, not a shortcut around data validation.
  with tempfile.TemporaryDirectory()as td:
   root=pathlib.Path(td).resolve();(root/'scripts').mkdir();file=root/'scripts/proof.py';file.write_text('x=1\n');code=['scripts/proof.py'];pins={'scripts/proof.py':hashlib.sha256(file.read_bytes()).digest()};digest=hashlib.sha256(json.dumps({k:v.hex()for k,v in pins.items()},sort_keys=True,separators=(',',':')).encode()).hexdigest()
   with patch.object(c,'_REVIEWED_GUARD_CODE_SHA256',digest):
    self.assertTrue(c._closed_code_pins_reviewed(root,code,pins));(root/'scripts/another.py').write_text('x=2\n');self.assertFalse(c._closed_code_pins_reviewed(root,code,pins))
if __name__=='__main__':unittest.main(verbosity=2)
