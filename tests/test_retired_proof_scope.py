"""A full retirement proof is reused only inside its owning validation scope."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from scripts import retired_person_ids as retired
from scripts import source_non_person_retirement as negative
from scripts import validation_context as context

ROOT=Path(__file__).resolve().parents[1]
class RetiredProofScopeTests(unittest.TestCase):
 def source(self):
  temporary=tempfile.TemporaryDirectory();self.addCleanup(temporary.cleanup);root=Path(temporary.name)
  for rel in ['registry/persons.json','corpus/shiji/130.json','corpus/shiji/037.json',negative.REVIEW_PATH,negative.RECEIPT_PATH,*negative.MIRRORS,'data/historical-tables/shiji-015.json']:
   target=root/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes((ROOT/rel).read_bytes())
  return root
 def old(self,root):return json.loads((root/negative.RECEIPT_PATH).read_text())['retired_person_ids'][0]
 def test_complete_negative_proof_once_inside_twice_outside(self):
  root=self.source()
  with patch.object(negative,'_review',wraps=negative._review) as proof:
   with context.scope(root):
    self.assertIn(self.old(root),retired.retired_person_ids(root));self.assertEqual(retired.retired_person_ids(root),retired.retired_person_ids(root))
   self.assertEqual(proof.call_count,1)
   retired.retired_person_ids(root);retired.retired_person_ids(root)
   self.assertEqual(proof.call_count,3)
   with context.scope(root):retired.retired_person_ids(root)
   self.assertEqual(proof.call_count,4)
 def test_cross_root_nested_and_disabled_scopes_are_fresh(self):
  root=self.source();other=self.source()
  with patch.object(negative,'_review',wraps=negative._review) as proof:
   with context.scope(root) as outer:
    retired.retired_person_ids(root)
    retired.retired_person_ids(other);retired.retired_person_ids(other)
    with context.scope(root):retired.retired_person_ids(root)
    with context.scope(root,enabled=False):retired.retired_person_ids(root);retired.retired_person_ids(root)
    self.assertIs(context._ACTIVE.get(),outer);retired.retired_person_ids(root)
   self.assertEqual(proof.call_count,6);self.assertTrue(outer['closed']);self.assertEqual(outer['memo'],{})
 def test_exception_uncached_and_caller_cannot_poison_set(self):
  root=self.source();path=root/'corpus/current-ledger.json';path.write_text(json.dumps({'person_id':self.old(root)}))
  with context.scope(root),patch.object(negative,'_review',wraps=negative._review) as proof:
   for _ in range(2):
    with self.assertRaisesRegex(ValueError,'current-ledger'):retired.retired_person_ids(root)
   self.assertEqual(proof.call_count,2);path.unlink();result=retired.retired_person_ids(root)
   self.assertIsInstance(result,frozenset)
   with self.assertRaises(AttributeError):result.add('bad')
   local=set(result);local.clear();self.assertIn(self.old(root),retired.retired_person_ids(root))
  self.assertIsNone(context._ACTIVE.get())
 def test_full_unknown_receipt_fields_not_ignored_outside_scope(self):
  root=self.source();retired.retired_person_ids(root);p=root/negative.RECEIPT_PATH;data=json.loads(p.read_text());data['unknown_metadata']={'human_reviewed':True};p.write_text(json.dumps(data))
  with self.assertRaisesRegex(ValueError,'exact negative source review'):retired.retired_person_ids(root)
 def test_unknown_receipt_change_inside_scope_rejected_by_normal_end_guard(self):
  from scripts import validate_corpus
  root=self.source()
  def mutate(root):
   retired.retired_person_ids(root);p=root/negative.RECEIPT_PATH;data=json.loads(p.read_text());data['unknown_metadata']={'extra':[1]};p.write_text(json.dumps(data));retired.retired_person_ids(root);return []
  with patch.object(validate_corpus,'_validate_uncached',mutate):self.assertIn(context.DRIFT_ERROR,validate_corpus.validate(root))
  with self.assertRaises(ValueError):retired.retired_person_ids(root)
 def test_new_hidden_endpoint_file_cannot_survive_end_guard(self):
  from scripts import validate_corpus
  root=self.source()
  def mutate(root):
   retired.retired_person_ids(root);(root/'corpus/hidden-current.json').write_text(json.dumps({'nested':{self.old(root):'endpoint'}}));retired.retired_person_ids(root);return []
  with patch.object(validate_corpus,'_validate_uncached',mutate):self.assertIn(context.DRIFT_ERROR,validate_corpus.validate(root))
  with self.assertRaisesRegex(ValueError,'hidden-current'):retired.retired_person_ids(root)
 def test_no_cached_api_can_bypass_missing_receipt_on_next_call(self):
  root=self.source();retired.retired_person_ids(root);(root/negative.RECEIPT_PATH).unlink()
  with self.assertRaisesRegex(ValueError,'requires both'):retired.retired_person_ids(root)
 def test_full_negative_checks_remain_inside_scope(self):
  for mode in ['source','quote','registry','descendant','table','ledger','receipt']:
   with self.subTest(mode=mode):
    root=self.source();old=self.old(root)
    if mode in ['source','quote']:
     p=root/'corpus/shiji/130.json';d=json.loads(p.read_text())
     if mode=='source':d['source']['revision_id']=0
     else:next(x for x in d['paragraphs']if x['id']=='c-shiji-130-taishigong:p049')['text']='wrong'
    elif mode in ['registry','descendant']:
     p=root/'registry/persons.json';d=json.loads(p.read_text());d['persons'].append({'id':old if mode=='registry'else old+'_A'})
    elif mode=='table':p=root/'data/historical-tables/hidden.json';d={'person_id':old}
    elif mode=='ledger':p=root/'source-evidence/hidden.json';d={'unexpected':{old:'endpoint'}}
    else:p=root/negative.RECEIPT_PATH;d=json.loads(p.read_text());d['review_sha256']='0'*64
    p.write_text(json.dumps(d))
    with context.scope(root),self.assertRaises(ValueError):retired.retired_person_ids(root)
