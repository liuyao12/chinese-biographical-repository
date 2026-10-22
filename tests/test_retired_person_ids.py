import unittest,tempfile,json,pathlib,copy
from unittest.mock import patch
from scripts import retired_person_ids as h, person_ids as p
Z=dict(record_type='editorial_annotation_rekey_receipt',namespace_id='new_abc_123',historical_rekey_mapping={'old_abc_123':'new_abc_123_A'},mapping_role='audit_only_not_alias_or_current_person_endpoint',person_aliases_created=False)
W=dict(record_type='editorial_annotation_rekey_receipt',family_id='family-synthetic',retired_person_ids=['old_def_456'],retirement_policy='audit_only_not_canonical_not_alias_not_reusable',person_aliases_created=False)
class Reservations(unittest.TestCase):
 def root(self,z=None,w=None):
  t=tempfile.TemporaryDirectory();self.addCleanup(t.cleanup);r=pathlib.Path(t.name)
  for name,d in [('z',z),('w',w)]:
   if d is not None:f=r/'source-evidence'/name/'annotation-chain.json';f.parent.mkdir(parents=True);f.write_text(json.dumps(d))
  return r
 def test_two_shapes_and_root_scope(self):
  self.assertEqual(h.retired_person_ids(self.root(Z,W)),{'old_abc_123','old_def_456'});self.assertEqual(h.retired_person_ids(self.root(Z)),{'old_abc_123'});self.assertFalse(h.retired_person_ids(self.root()))
 def test_future_family_no_whitelist(self):self.assertEqual(h.retired_person_ids(self.root(w=dict(W,family_id='family-new-pei',retired_person_ids=['qaz_qaz_123']))),{'qaz_qaz_123'})
 def test_read_every_call_no_cache(self):
  r=self.root(w=W);self.assertEqual(len(h.retired_person_ids(r)),1);(r/'source-evidence/w/annotation-chain.json').unlink();self.assertFalse(h.retired_person_ids(r))
 def test_non_rekey_ignored(self):self.assertFalse(h.retired_person_ids(self.root(w={'record_type':'age_annotation_revision'})))
 def test_unknown_typed_rejected(self):
  with self.assertRaises(ValueError):h.retired_person_ids(self.root(w={'record_type':W['record_type'],'person_aliases_created':False}))
 def test_mixed_shapes_rejected(self):
  with self.assertRaises(ValueError):h.retired_person_ids(self.root(w=dict(W,historical_rekey_mapping=Z['historical_rekey_mapping'])))
 def test_no_review_shortcut(self):
  with self.assertRaises(ValueError):h.retired_person_ids(self.root(w=dict(W,human_reviewed=True,status='approved',retirement_policy='wrong')))
 def test_aliases_rejected(self):
  with self.assertRaises(ValueError):h.retired_person_ids(self.root(w=dict(W,person_aliases_created=True)))
 def test_malformed_family_ids(self):
  for owner in ['',None,'other','family-../bad']:
   with self.subTest(owner=owner),self.assertRaises(ValueError):h.retired_person_ids(self.root(w=dict(W,family_id=owner)))
 def test_malformed_retired_list(self):
  for ids in [[],['bad'],['abc_def_123']*2,[{}],None]:
   with self.subTest(ids=ids),self.assertRaises(ValueError):h.retired_person_ids(self.root(w=dict(W,retired_person_ids=ids)))
 def test_malformed_namespace(self):
  for change in [dict(namespace_id='bad'),dict(mapping_role='approved'),dict(historical_rekey_mapping={}),dict(historical_rekey_mapping={'old_abc_123':'other_abc_123'}),dict(historical_rekey_mapping={'old_abc_123':'old_abc_123'})]:
   with self.subTest(change=change),self.assertRaises(ValueError):h.retired_person_ids(self.root(z=dict(Z,**change)))
 def test_malformed_json(self):
  r=self.root(w=W);(r/'source-evidence/w/annotation-chain.json').write_text('{')
  with self.assertRaises(ValueError):h.retired_person_ids(r)
 def test_exact_registration_guard(self):
  r=self.root(w=W)
  with self.assertRaises(ValueError):h.assert_not_retired('old_def_456',r)
  self.assertEqual(h.assert_not_retired('abc_def_123',r),'abc_def_123')
 def test_root_allocation_retries_reserved_root(self):
  r=self.root(w=dict(W,retired_person_ids=['abc_def_123']))
  with patch.object(p.secrets,'choice',side_effect=list('abcdef123xyzabc789')):self.assertEqual(p.allocate_person_id([],root=r),'xyz_abc_789')
 def test_root_allocation_reserves_retired_descendant_prefix(self):
  r=self.root(w=dict(W,retired_person_ids=['abc_def_123_A']))
  with patch.object(p.secrets,'choice',side_effect=list('abcdef123xyzabc789')):self.assertEqual(p.allocate_person_id([],root=r),'xyz_abc_789')
 def test_old_api_still_no_root(self):
  with patch.object(p.secrets,'choice',side_effect=list('abcdef123')):self.assertEqual(p.allocate_person_id([]),'abc_def_123')
  self.assertEqual(p.allocate_child_id('abc_def_123',[]),'abc_def_123_A')
 def test_normal_new_allocation(self):
  with patch.object(p.secrets,'choice',side_effect=list('abcdef123')):self.assertEqual(p.allocate_person_id([],root=self.root(w=W)),'abc_def_123')
 def test_retired_root_cannot_allocate_child_or_missing_generation(self):
  r=self.root(w=dict(W,retired_person_ids=['abc_def_123']))
  for generations in [1,2]:
   with self.subTest(generations=generations),self.assertRaises(ValueError):p.allocate_descendant_id('abc_def_123',generations,[],root=r)
 def test_retired_child_and_prefix(self):
  for old in ['abc_def_123_A','abc_def_123_AA']:
   with self.subTest(old=old):self.assertEqual(p.allocate_child_id('abc_def_123',[],root=self.root(w=dict(W,retired_person_ids=[old]))),'abc_def_123_B')
 def test_descendants_below_retired_child_rejected(self):
  r=self.root(w=dict(W,retired_person_ids=['abc_def_123_A']))
  with self.assertRaises(ValueError):p.allocate_child_id('abc_def_123_A',[],root=r)
 def test_no_new_targets_returned(self):self.assertIsInstance(h.retired_person_ids(self.root(z=Z)),frozenset);self.assertNotIn('new_abc_123_A',h.retired_person_ids(self.root(z=Z)))
 def test_consolidate_allocator_hook(self):
  from scripts import consolidate_person_ids as c
  people={'abc_def_123':dict(id='abc_def_123',aliases=[]),'new_xyz_456':dict(id='new_xyz_456',aliases=[],family_path=dict(connection='father',parent_person_id='abc_def_123'))}
  with patch.object(c,'load_catalog',return_value=(people,[])),patch.object(c,'load_assemblies',return_value=({},{})):
   merged,mapping=c.plan(self.root(w=dict(W,retired_person_ids=['abc_def_123_A'])))
  self.assertEqual(mapping,{'new_xyz_456':'abc_def_123_B'})
 def test_consolidate_stage_carries_receipt(self):
  from scripts import consolidate_person_ids as c
  r=self.root(w=W);(r/'registry').mkdir();(r/'corpus').mkdir();d=dict(persons=[dict(id='abc_def_123',aliases=[])]);(r/'registry/persons.json').write_text(json.dumps(d))
  with tempfile.TemporaryDirectory()as tmp,patch.object(c,'plan',return_value=(d['persons'],{})),patch.object(c,'load_catalog',return_value=({},[])):
   dest=pathlib.Path(tmp);c.stage(r,dest);self.assertEqual(h.retired_person_ids(dest),{'old_def_456'});self.assertEqual(json.loads((dest/'registry/persons.json').read_text()),d)
if __name__=='__main__':unittest.main()
