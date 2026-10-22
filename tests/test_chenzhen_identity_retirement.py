"""Permanent public-ID retirement regressions. All negative mutations are memory/temp only."""
from pathlib import Path
import unittest,json,copy,tempfile
from unittest.mock import patch
from scripts.retired_person_ids import retired_person_ids,allocation_conflicts,assert_not_retired
from scripts.person_ids import allocate_person_id,allocate_child_id
from scripts.person_bundle import load_catalog,bundle
R=Path(__file__).resolve().parents[1];KEEP='bvi_h86_vk1';RETIRED=('jdl_lhw_qs9','aon_o1a_cxi','fyf_enn_4w8','cwr_47k_5ds');LOCAL='qaa_xph_cck';DID='d-shiji070-018'
class ChenZhenRetirement(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.catalog=load_catalog(R);cls.reg=json.loads((R/'registry/persons.json').read_text());cls.receipt=json.loads((R/'source-evidence/chenzhen-identity-merge/annotation-chain.json').read_text());cls.decision=next(x for x in json.loads((R/'corpus/shiji/070-identities.json').read_text())['decisions']if x['id']==DID)
 def test_actual_four_retired_no_registry_or_alias(self):
  ids={p['id']for p in self.reg['persons']};self.assertTrue(set(RETIRED)<=retired_person_ids(R));self.assertTrue(set(RETIRED).isdisjoint(ids));self.assertIn(LOCAL,ids)
  for p in self.reg['persons']:self.assertTrue(set(RETIRED).isdisjoint(p.get('id_aliases',[])))
  for old in RETIRED:
   with self.assertRaises(ValueError):assert_not_retired(old,R)
   with self.assertRaises((KeyError,ValueError)):bundle(old,root=R,catalog=self.catalog)
 def test_actual_all_42_source_anchors_same_ids_and_text(self):
  expected=[]
  for f in sorted((R/'corpus/shiji').glob('*.json')):
   c=json.loads(f.read_text())
   if c.get('record_type')=='marked_chapter':
    for p in c['paragraphs']:
     for m in p['mentions']:
      if m.get('person_id')==KEEP:expected.append(m['id']);self.assertEqual(m['surface'],p['text'][m['start']:m['end']])
  self.assertEqual(len(expected),42);person=next(p for p in self.reg['persons']if p['id']==KEEP);self.assertEqual(person['label'],'陳軫');self.assertEqual({m for a in person['aliases']for m in a['mention_ids']},set(expected));self.assertEqual({e['mention_id']for e in person['evidence']},set(expected));self.assertIn('source_identity_notes',person)
 def test_no_old_current_corpus_endpoints(self):
  for f in (R/'corpus').glob('*/*.json'):
   c=json.loads(f.read_text());self.assertFalse(any(old in json.dumps(c,ensure_ascii=False)for old in RETIRED),str(f))
 def test_tang_single_external_candidate_stays_unresolved(self):
  c=json.loads((R/'corpus/xintangshu/071xia-chen-preface.json').read_text());case=next(x for x in c['annotation']['unresolved_identity_cases']if x['id']=='case-xts071xia-chen-zhen');self.assertEqual(case['candidate_person_ids'],[LOCAL,KEEP]);self.assertEqual(case['status'],'unresolved');self.assertFalse(case['candidate_list_exhaustive']);self.assertEqual(case['preferred_identity_hypothesis']['person_id'],KEEP)
  self.assertEqual({m['person_id']for p in c['paragraphs']for m in p['mentions']if m['surface']=='軫'},{LOCAL})
  for pid in [LOCAL,KEEP]:self.assertTrue(any(x['id']==case['id']for x in bundle(pid,root=R,catalog=self.catalog)['unresolved_identity_cases']))
 def test_retirement_allocator_root_and_prefix_no_reuse(self):
  ids=set(self.catalog[0]);retired=retired_person_ids(R)
  for old in RETIRED:
   self.assertTrue(allocation_conflicts(old,retired));self.assertTrue(allocation_conflicts(old+'_A',retired));self.assertTrue(allocation_conflicts(old[:3],retired))
   with self.assertRaises(ValueError):allocate_child_id(old,ids,root=R)
   safe=allocate_person_id(ids,root=R);stream=list(old.replace('_','')+safe.replace('_',''))
   with patch('scripts.person_ids.secrets.choice',side_effect=stream):self.assertEqual(allocate_person_id(ids,root=R),safe)
 def synthetic(self,receipt=None,decision=None,current=None):
  t=tempfile.TemporaryDirectory();self.addCleanup(t.cleanup);r=Path(t.name)
  for rel,x in [('source-evidence/synthetic/annotation-chain.json',receipt if receipt is not None else self.receipt),('corpus/synthetic/case-identities.json',{'record_type':'person_identity_decision_set','decisions':[decision if decision is not None else self.decision]}),('registry/persons.json',{'persons':current if current is not None else[{'id':KEEP}]})]:
   f=r/rel;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(json.dumps(x))
  return r
 def test_receipt_binds_actual_cross_chapter_owner(self):self.assertEqual(retired_person_ids(self.synthetic()),frozenset(RETIRED))
 def test_reject_reintroduced_current_old_id(self):
  with self.assertRaises(ValueError):retired_person_ids(self.synthetic(current=[{'id':KEEP},{'id':RETIRED[0]}]))
 def test_reject_missing_wrong_or_unsupported_owner(self):
  for field,value in [('id','d-not-owner'),('person_id',RETIRED[0]),('scope','same_chapter'),('evidence',[]),('rationale','')]:
   d=copy.deepcopy(self.decision);d[field]=value
   with self.assertRaises(ValueError):retired_person_ids(self.synthetic(decision=d))
 def test_reject_mixed_namespace_family_alias_unknown_receipts(self):
  for field,value in [('family_id','family-synthetic'),('historical_rekey_mapping',{}),('namespace_id','abc_def_123'),('person_aliases_created',True),('extra',1)]:
   x=copy.deepcopy(self.receipt);x[field]=value
   with self.assertRaises(ValueError):retired_person_ids(self.synthetic(receipt=x))
if __name__=='__main__':unittest.main()
