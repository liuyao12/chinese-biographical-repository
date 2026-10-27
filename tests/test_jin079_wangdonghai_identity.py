import hashlib,json,unittest
from pathlib import Path
from scripts.person_bundle import bundle
from scripts.retired_person_ids import retired_person_ids
ROOT=Path(__file__).resolve().parents[1]
SOURCE='c-jinshu-079-xielang-family:p001:m0046'
SEED='c-jinshu-075-taiyuan-wang:line018:m0000'
class WangDonghaiIdentityTests(unittest.TestCase):
 def setUp(self):
  self.source=json.loads((ROOT/'corpus/jinshu/079.json').read_text());self.target=json.loads((ROOT/'corpus/jinshu/075-taiyuan-wang.json').read_text())
  self.people={p['id']:p for p in json.loads((ROOT/'registry/persons.json').read_text())['persons']}
  self.review=json.loads((ROOT/'source-evidence/wangdonghai-wangcheng-identity/review.json').read_text())
 def mark(self,c,mid):return next(m for p in c['paragraphs']for m in p['mentions']if m['id']==mid)
 def test_same_person_by_fixed_source_roles_not_pid_constant(self):
  person=self.mark(self.target,SEED)['person_id'];self.assertEqual(self.mark(self.source,SOURCE)['person_id'],person)
  for mid in [SOURCE,SEED]:self.assertEqual([p['id']for p in self.people.values()if any(e.get('mention_id')==mid for e in p['evidence'])],[person])
  self.assertFalse(any(c['id']=='u-jinshu079-wangdonghai'for c in self.source['annotation']['unresolved_identity_cases']))
 def test_full_units_and_source_positions_preserved(self):
  for pin in self.review['source_binding']['source_pins']:
   chapter=self.source if pin['chapter_id']==self.source['id']else self.target
   for pp in pin['paragraphs']:
    p=next(p for p in chapter['paragraphs']if p['id']==pp['id']);self.assertEqual(p['text'],pp['text']);self.assertEqual(hashlib.sha256(p['text'].encode()).hexdigest(),pp['sha256'])
  m=self.mark(self.source,SOURCE);self.assertEqual((m['start'],m['end'],m['surface']),(46,49,'王東海'))
 def test_retired_is_reservation_never_alias_or_query(self):
  receipt=json.loads((ROOT/'source-evidence/wangdonghai-wangcheng-identity/annotation-chain.json').read_text());retired=retired_person_ids(ROOT)
  aliases={a for p in self.people.values()for a in p.get('id_aliases',[])}
  for pid in receipt['retired_person_ids']:
   self.assertIn(pid,retired);self.assertNotIn(pid,self.people);self.assertNotIn(pid,aliases)
   with self.assertRaises(ValueError):bundle(pid,root=ROOT,catalog=(self.people,[]))
 def test_rendered_annotation_does_not_claim_fixed_raw_or_presence(self):
  self.assertIn('cache miss',self.review['external_reading_reference']['access_scope']);self.assertIn('No raw',self.review['external_reading_reference']['access_scope'])
  self.assertIn('非親讀散佚原書',self.review['external_reading_reference']['layers'][1]);self.assertIn('不新造CE',self.review['chronology'])
