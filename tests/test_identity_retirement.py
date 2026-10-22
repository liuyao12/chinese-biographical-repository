import json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from scripts import retired_person_ids as h,person_ids as p
RECEIPT=dict(record_type='editorial_annotation_rekey_receipt',identity_decision_id='d-synthetic-identity',retired_person_ids=['old_abc_123'],retirement_policy='audit_only_not_canonical_not_alias_not_reusable',person_aliases_created=False)
DECISION=dict(id='d-synthetic-identity',person_id='new_abc_123',scope='cross_chapter',status='contextual_provisional',evidence=[{'paragraph_id':'synthetic:p1','quote':'synthetic'}],rationale='Synthetic explicit identity bridge.')
class IdentityRetirement(unittest.TestCase):
 def root(self,receipt=None,decision=None):
  t=tempfile.TemporaryDirectory();self.addCleanup(t.cleanup);r=Path(t.name)
  f=r/'source-evidence/synthetic/annotation-chain.json';f.parent.mkdir(parents=True);f.write_text(json.dumps(RECEIPT if receipt is None else receipt))
  f=r/'corpus/synthetic/001-identities.json';f.parent.mkdir(parents=True);f.write_text(json.dumps({'record_type':'person_identity_decision_set','decisions':[DECISION if decision is None else decision]}))
  f=r/'registry/persons.json';f.parent.mkdir(parents=True);f.write_text(json.dumps({'persons':[{'id':'new_abc_123'}]}))
  return r
 def test_positive_binds_identity_without_family(self):
  r=self.root();self.assertEqual(h.retired_person_ids(r),{'old_abc_123'});self.assertNotIn('new_abc_123',h.retired_person_ids(r))
 def test_new_decision_no_whitelist(self):
  self.assertEqual(h.retired_person_ids(self.root(dict(RECEIPT,identity_decision_id='d-another'),dict(DECISION,id='d-another'))),{'old_abc_123'})
 def test_missing_decision_rejected(self):
  r=self.root();(r/'corpus/synthetic/001-identities.json').unlink()
  with self.assertRaises(ValueError):h.retired_person_ids(r)
 def test_wrong_decision_set_type_rejected(self):
  r=self.root();f=r/'corpus/synthetic/001-identities.json';d=json.loads(f.read_text());d['record_type']='not_identity';f.write_text(json.dumps(d))
  with self.assertRaises(ValueError):h.retired_person_ids(r)
 def test_duplicate_decision_rejected(self):
  r=self.root();(r/'corpus/synthetic/002-identities.json').write_text(json.dumps({'decisions':[DECISION]}))
  with self.assertRaises(ValueError):h.retired_person_ids(r)
 def test_mixed_namespace_family_rejected(self):
  for fields in [dict(family_id='family-synthetic'),dict(namespace_id='new_abc_123'),dict(historical_rekey_mapping={'old_abc_123':'new_abc_123_A'}),dict(mapping_role='audit_only_not_alias_or_current_person_endpoint')]:
   with self.subTest(fields=fields),self.assertRaises(ValueError):h.retired_person_ids(self.root(dict(RECEIPT,**fields)))
 def test_malformed_owner_and_ids_rejected(self):
  for fields in [dict(identity_decision_id=None),dict(identity_decision_id='../../bad'),dict(retired_person_ids=[]),dict(retired_person_ids=['bad']),dict(retired_person_ids=['old_abc_123']*2),dict(retired_person_ids=[{}]),dict(retired_person_ids=None)]:
   with self.subTest(fields=fields),self.assertRaises(ValueError):h.retired_person_ids(self.root(dict(RECEIPT,**fields)))
 def test_bound_decision_mismatch_rejected(self):
  for fields in [dict(person_id='not_abc_123'),dict(person_id='old_abc_123'),dict(person_id='bad'),dict(scope='same_chapter'),dict(evidence=[]),dict(rationale=''),dict(status='approved')]:
   with self.subTest(fields=fields),self.assertRaises(ValueError):h.retired_person_ids(self.root(decision=dict(DECISION,**fields)))
 def test_alias_and_policy_shortcut_rejected(self):
  for fields in [dict(person_aliases_created=True),dict(retirement_policy='approved'),dict(human_reviewed=True)]:
   with self.subTest(fields=fields),self.assertRaises(ValueError):h.retired_person_ids(self.root(dict(RECEIPT,**fields)))
 def test_missing_registry_or_live_retired_person_rejected(self):
  r=self.root();(r/'registry/persons.json').unlink()
  with self.assertRaises(ValueError):h.retired_person_ids(r)
  r=self.root();(r/'registry/persons.json').write_text(json.dumps({'persons':[{'id':'new_abc_123'},{'id':'old_abc_123'}]}))
  with self.assertRaises(ValueError):h.retired_person_ids(r)
 def test_registration_and_allocator_reject_retired(self):
  r=self.root()
  with self.assertRaises(ValueError):h.assert_not_retired('old_abc_123',r)
  with patch.object(p.secrets,'choice',side_effect=list('oldabc123newabc456')):self.assertEqual(p.allocate_person_id([],root=r),'new_abc_456')
  with self.assertRaises(ValueError):p.allocate_child_id('old_abc_123',[],root=r)
 def test_root_scoped_no_cache(self):
  r=self.root();self.assertEqual(h.retired_person_ids(r),{'old_abc_123'});(r/'source-evidence/synthetic/annotation-chain.json').unlink();self.assertFalse(h.retired_person_ids(r))
if __name__=='__main__':unittest.main()
