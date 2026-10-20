# coding: utf-8
"""Unresolved identity slots preserve sources without asserting two spouses."""
import copy,json,unittest
from pathlib import Path
from scripts.unresolved_relation_identity import group_errors
ROOT=Path(__file__).resolve().parents[1]
class UnresolvedSpouseIdentity(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=json.loads((ROOT/'corpus/weishu-weishou/038-wanghuilong.json').read_text());cls.assertions={a['id']:a for a in json.loads((ROOT/'corpus/weishu-weishou/038-wanghuilong-assertions.json').read_text())['assertions']};cls.pids={p['id']for p in json.loads((ROOT/'registry/persons.json').read_text())['persons']}
 def test_real_case(self):self.assertEqual(group_errors(self.c,self.assertions,self.pids),[])
 def bad(self,edit):
  c=copy.deepcopy(self.c);edit(c['annotation']['unresolved_relation_identity_groups'][0]);self.assertTrue(group_errors(c,self.assertions,self.pids))
 def test_wrong_assertion(self):self.bad(lambda g:g['assertion_ids'].__setitem__(0,'missing'))
 def test_wrong_candidate(self):self.bad(lambda g:g['candidate_person_ids'].__setitem__(0,g['common_person_id']))
 def test_wrong_common_spouse(self):self.bad(lambda g:g.__setitem__('common_person_id',g['candidate_person_ids'][0]))
 def test_wrong_source(self):self.bad(lambda g:g['references'][0].__setitem__('source_id','other-source'))
 def test_wrong_witness(self):self.bad(lambda g:g['source_fingerprint'].__setitem__('source_commit','other-revision'))
 def test_wrong_span(self):self.bad(lambda g:g['references'][0]['span'].__setitem__('start',0))
 def test_no_migration_alias(self):
  g=self.c['annotation']['unresolved_relation_identity_groups'][0];self.assertIsNone(g['same_person']);self.assertIsNone(g['distinct_people']);self.assertNotIn('alias',g)
 def test_resolved_same_not_unresolved(self):self.bad(lambda g:g.__setitem__('same_person',True))
 def test_resolved_distinct_not_unresolved(self):self.bad(lambda g:g.__setitem__('distinct_people',True))
 def test_null_must_be_explicit(self):self.bad(lambda g:g.pop('same_person'))
 def test_not_parentage_model(self):self.bad(lambda g:g.__setitem__('predicate','father'))
 def test_no_case_unchanged(self):
  c=copy.deepcopy(self.c);c['annotation'].pop('unresolved_relation_identity_groups');self.assertEqual(group_errors(c,self.assertions,self.pids),[])
 def test_original_assertions_keep_both(self):
  g=self.c['annotation']['unresolved_relation_identity_groups'][0];self.assertEqual(len(g['assertion_ids']),2)
  for aid in g['assertion_ids']:self.assertEqual(self.assertions[aid]['status'],'source_attested');self.assertTrue(self.assertions[aid]['evidence'][0]['quote'])
