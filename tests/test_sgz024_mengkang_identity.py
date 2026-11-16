# coding:utf-8
import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class MengKangSourceIdentity(unittest.TestCase):
 def setUp(self):
  self.review=json.loads((ROOT/'source-evidence/sgz024-cuilin/mengkang-identity-qualification.json').read_text())
  self.chapters={d['id']:d for p in (ROOT/'corpus/sanguozhi').glob('*.json')if(d:=json.loads(p.read_text())).get('record_type')=='marked_chapter'}
 def anchor(self,which):
  pid=self.review['paragraph_id_'+which];q=next(q for c in self.chapters.values()for q in c['paragraphs']if q['id']==pid);m=next(m for m in q['mentions']if m['id']==self.review['mention_id_'+which]);return q,m
 def test_two_exact_source_anchors_same_current_person(self):
  q,a=self.anchor('016');r,b=self.anchor('024');self.assertEqual(a['surface'],'孟康');self.assertEqual(b['surface'],'孟康');self.assertEqual(a['person_id'],b['person_id']);self.assertEqual(b['person_id'],self.review['person_id'])
 def test_full_context_and_qualification_not_source_explicit_zi(self):
  q,a=self.anchor('016');r,b=self.anchor('024');self.assertEqual(q['text'],self.review['quote_016']);self.assertEqual(r['text'],self.review['quote_024']);self.assertIn('康字公休安平人',q['text']);self.assertIn('散騎侍郎孟康薦林',r['text']);self.assertNotIn('公休',r['text']);self.assertEqual(self.review['status'],'contextual_provisional');self.assertIs(self.review['human_reviewed'],False)
 def test_one_inverse_registry_owner_for_each_mid(self):
  people=json.loads((ROOT/'registry/persons.json').read_text())['persons']
  for which in ['016','024']:
   owners=[p['id']for p in people if any(e.get('mention_id')==self.review['mention_id_'+which]for e in p['evidence'])];self.assertEqual(owners,[self.review['person_id']])
if __name__=='__main__':unittest.main()
