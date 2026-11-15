import unittest,json
from pathlib import Path
from scripts.retired_person_ids import retired_person_ids,assert_not_retired

class Final37IdentityTests(unittest.TestCase):
 def setUp(self):
  self.root=Path(__file__).resolve().parents[1]
  self.people={x['id']:x for x in json.loads((self.root/'registry/persons.json').read_text())['persons']}
  self.decisions=[x for x in json.loads((self.root/'corpus/shiji/130-identities.json').read_text())['decisions']if x['id'].startswith('d-shiji130-final37-')]
 def test_exact_37_decisions_and_37_reservations(self):
  self.assertEqual(len(self.decisions),37)
  retired=retired_person_ids(self.root);old=[]
  for d in self.decisions:
   r=json.loads((self.root/('source-evidence/shiji130-final37-'+d['id'].rsplit('-',1)[1]+'/annotation-chain.json')).read_text());self.assertEqual(r['identity_decision_id'],d['id']);self.assertFalse(r['person_aliases_created']);old+=r['retired_person_ids']
  self.assertEqual(len(set(old)),37);self.assertTrue(set(old)<=retired);self.assertFalse(set(old)&self.people.keys())
  for p in old:
   with self.assertRaises(ValueError):assert_not_retired(p,self.root)
 def test_full_source_quotes_and_reversed_endpoints(self):
  chapters={}
  for f in(self.root/'corpus').glob('*/*.json'):
   v=json.loads(f.read_text())
   if isinstance(v,dict)and v.get('record_type')=='marked_chapter':chapters[v['id']]=v
  for d in self.decisions:
   self.assertEqual(d['status'],'contextual_provisional');self.assertFalse(d['human_reviewed']);self.assertFalse(self.people[d['person_id']].get('id_aliases'))
   for ev in d['evidence']:
    p=next(p for p in chapters[ev['chapter_id']]['paragraphs']if p['id']==ev['paragraph_id']);self.assertEqual(ev['quote'],p['text'])
   for mid in d['identification_basis']['target_mention_ids']:
    m=next(m for c in chapters.values()for p in c['paragraphs']for m in p['mentions']if m['id']==mid);self.assertEqual(m['person_id'],d['person_id']);self.assertEqual(m['kind'],'person');self.assertTrue(any(mid in a['mention_ids']for a in self.people[d['person_id']]['aliases']));self.assertTrue(any(e.get('mention_id')==mid for e in self.people[d['person_id']]['evidence']))
 def test_prior_qualifications_and_no_invented_names(self):
  for d in self.decisions:
   self.assertEqual(len(d['prior_source_qualifications']),1);q=d['prior_source_qualifications'][0];self.assertTrue(q['metadata']['label']);self.assertEqual(len(q['original_registry_record_sha256']),64);self.assertEqual(set(q['source_mention_ids']),set(d['identification_basis']['target_mention_ids']))
 def test_yandan_outside_transaction(self):
  chapter=json.loads((self.root/'corpus/shiji/130.json').read_text());mid=next(m['id']for p in chapter['paragraphs']for m in p['mentions']if m['surface']=='燕丹');self.assertFalse(any(mid in d['identification_basis']['target_mention_ids']for d in self.decisions))

 def test_candidate_pool_deduplicated_after_identity_union(self):
  chapter=json.loads((self.root/'corpus/jinshu/039.json').read_text());mention=next(m for p in chapter['paragraphs']for m in p['mentions']if m['id']=='c-jinshu-039-wangxun-feng:appraisal:l146:m0445');self.assertEqual(mention['surface'],'爰絲');self.assertEqual(mention['kind'],'unresolved');self.assertEqual(len(mention['candidate_person_ids']),len(set(mention['candidate_person_ids'])))
