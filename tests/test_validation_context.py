import copy
import importlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
from scripts import validation_context as c

class ValidationContextTests(unittest.TestCase):
 def test_copy_full_argument_key_and_separate_roots(self):
  calls=[]
  @c.memoized(0)
  def proof(root,ch):
   calls.append((str(root),copy.deepcopy(ch)));return {'nested':[ch]}
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);other=root/'other';other.mkdir()
   with c.scope(root):
    a=proof(root,{'id':'x','human_reviewed':False});a['nested'].clear()
    self.assertEqual(proof(root,{'id':'x','human_reviewed':False}),{'nested':[{'id':'x','human_reviewed':False}]})
    proof(root,{'id':'x','human_reviewed':True});proof(other,{'id':'x'})
   self.assertEqual(len(calls),3)
   with c.scope(root):proof(root,{'id':'x','human_reviewed':False})
   self.assertEqual(len(calls),4)
 def test_unsupported_shapes_preserve_original_and_exceptions_release(self):
  @c.memoized(0)
  def proof(root,ch):
   if not isinstance(ch,dict):raise ValueError('original shape')
   return ch
  with tempfile.TemporaryDirectory() as d:
   for bad in [None,[], 'bad', object(), ('tuple',)]:
    with self.assertRaisesRegex(ValueError,'original shape'):
     with c.scope(d):proof(d,bad)
    self.assertIsNone(c._ACTIVE.get())
 def test_tuple_and_list_do_not_collide(self):
  @c.memoized(0)
  def proof(root,ch):return type(ch['items']).__name__
  with c.scope('.'):
   self.assertEqual(proof('.',{'items':[]}), 'list')
   self.assertEqual(proof('.',{'items':()}), 'tuple')
 def test_nested_disabled_and_flat_import_share_handle(self):
  sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
  self.assertIs(importlib.import_module('validation_context'),c)
  with c.scope('.') as outer:
   with c.scope('.',enabled=False):self.assertIsNone(c._ACTIVE.get())
   self.assertIs(c._ACTIVE.get(),outer)
  self.assertTrue(outer['closed']);self.assertEqual(outer['memo'],{})
 def test_fresh_content_membership_and_stat(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);p=root/'registry/persons.json';p.parent.mkdir();p.write_text('{}')
   before=c.fingerprint(root);p.write_text('{"new":true}')
   self.assertNotEqual(before,c.fingerprint(root));p.write_text('{}')
   self.assertNotEqual(before,c.fingerprint(root))
   p2=root/'registry/new.json';p2.write_text('{}');added=c.fingerprint(root);p2.unlink()
   self.assertNotEqual(added,c.fingerprint(root))
 def test_validate_drift_and_uncached_exception_release(self):
  from scripts import validate_corpus as v
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);p=root/'corpus/raw.txt';p.parent.mkdir();p.write_text('before')
   def mutate(root):p.write_text('after');return []
   with patch.object(v,'_validate_uncached',mutate):self.assertIn(c.DRIFT_ERROR,v.validate(root))
   with patch.object(v,'_validate_uncached',side_effect=ValueError('original')):
    for enabled in [True,False]:
     with self.assertRaisesRegex(ValueError,'original'):v.validate(root,shared_context=enabled)
     self.assertIsNone(c._ACTIVE.get())
 def test_dynamic_seed_script_mutation_is_dependency_drift(self):
  from scripts import validate_corpus as v
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);p=root/'scripts/wyd_song044_role_seed.py';p.parent.mkdir();p.write_text('original dynamic seed')
   def mutate(root):p.write_text('changed dynamic seed');return []
   with patch.object(v,'_validate_uncached',mutate):self.assertIn(c.DRIFT_ERROR,v.validate(root))
 def test_generated_bytecode_is_not_a_source_dependency(self):
  from scripts import validate_corpus as v
  import py_compile
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);p=root/'scripts/seed.py';p.parent.mkdir();p.write_text('value = 1\n')
   def compile_source(root):py_compile.compile(str(p),doraise=True);return []
   with patch.object(v,'_validate_uncached',compile_source):self.assertEqual(v.validate(root),[])
   def change_source(root):p.write_text('value = 2\n');return []
   with patch.object(v,'_validate_uncached',change_source):self.assertIn(c.DRIFT_ERROR,v.validate(root))
 def test_real_source_full_in_memory_and_cached_result_pollution(self):
  from scripts.wyd_song044_formal_roles import source_errors
  from scripts.wyd_song044_names import records
  root=Path(__file__).resolve().parents[1]
  ch=json.loads((root/'corpus/songshu/044-wyd1739.json').read_text())
  with c.scope(root):
   self.assertEqual(source_errors(ch,root),[])
   bad=copy.deepcopy(ch);bad['annotation']['human_reviewed']=True
   self.assertTrue(source_errors(bad,root))
   rows=records(root);original=copy.deepcopy(rows);rows[0]['surname']='wrong'
   self.assertEqual(records(root),original)
if __name__=='__main__':unittest.main()
