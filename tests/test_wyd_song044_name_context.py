import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CID='c-songshu-044-wyd1739-xiehui'
class WydNameContextTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.chapter=json.loads((ROOT/'corpus/songshu/044-wyd1739.json').read_text())
  cls.people={p['id']:p for p in json.loads((ROOT/'registry/persons.json').read_text())['persons']}
  cls.readings={r['source_role_key']:r for r in json.loads((ROOT/'source-evidence/song044-wyd1739-xiehui/name-context-review.json').read_text())['readings']}
 def role(self,key):
  hits=[(p,m)for p in self.chapter['paragraphs']for m in p['mentions']if m.get('source_role_key')==key]
  self.assertTrue(hits);self.assertEqual(len({m['person_id']for _,m in hits}),1)
  return hits
 def test_relationship_words_are_outside_the_name_span(self):
  p,m=self.role('zongshuxian')[0]
  self.assertEqual(p['text'][:7],'上手答示宗叔獻')
  self.assertEqual(p['text'][m['start']:m['end']],'獻')
  self.assertEqual(p['text'][m['start']-2:m['start']],'宗叔')
  self.assertIsNone(self.readings['zongshuxian']['surname'])
  self.assertTrue(self.people[m['person_id']]['label'].startswith('獻（'))
 def test_later_explicit_full_names_restore_surnames(self):
  for key,full in [('xiedun','謝遯'),('shiyou','謝世猷')]:
   hits=self.role(key);self.assertTrue(any(m['surface']==full and p['text'][m['start']:m['end']]==full for p,m in hits))
   self.assertEqual(self.readings[key]['label'],full)
   self.assertTrue(self.people[hits[0][1]['person_id']]['label'].startswith('謝'))
 def test_contextual_readings_keep_their_relationship_evidence(self):
  facts=json.loads((ROOT/'corpus/songshu/044-wyd1739-assertions.json').read_text())['assertions'];byid={a['id']:a for a in facts}
  for key,surname in [('shixiu','謝'),('shiji','謝'),('shao','謝'),('huaifu','商')]:
   reading=self.readings[key];p,m=self.role(key)[0]
   self.assertEqual(reading['name_form'],'contextual_family_surname');self.assertEqual(reading['surname'],surname)
   self.assertTrue(self.people[m['person_id']]['label'].startswith(surname))
   self.assertTrue(reading['relationship_assertion_ids'])
   for aid in reading['relationship_assertion_ids']:
    self.assertIn(aid,byid);self.assertTrue(byid[aid]['evidence'])
   self.assertEqual(reading['status'],'contextual_provisional');self.assertFalse(reading['human_reviewed'])
 def test_registered_source_roles_do_not_claim_unallocated_ids(self):
  person_mentions=[m for p in self.chapter['paragraphs']for m in p['mentions']if m['kind']=='person']
  self.assertEqual(len(person_mentions),438)
  for m in person_mentions:
   self.assertIn(m['person_id'],self.people)
   self.assertNotIn('尚未正式分配全庫ID',m.get('interpretation_note',''))
   self.assertTrue(any(e.get('mention_id')==m['id']for e in self.people[m['person_id']]['evidence']))
 def test_original_witness_and_review_limits_remain(self):
  from scripts.fixed_wuyingdian_song044 import validate_source
  validate_source(self.chapter,ROOT)
  self.assertEqual(sum(m['kind']=='unresolved'for p in self.chapter['paragraphs']for m in p['mentions']),19)
  self.assertFalse(self.chapter['source']['image_verified'])
  self.assertFalse(self.chapter['annotation']['human_reviewed'])
if __name__=='__main__':unittest.main()
