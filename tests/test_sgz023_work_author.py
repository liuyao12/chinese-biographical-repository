import unittest,copy,json
from collections import Counter
from tests.test_sgz023_four_biographies_ner import FourBiographiesNER,ROOT,CH
from scripts.fixed_sgz023_works import state,author_valid
from scripts.fixed_sgz023_four_biographies import guard_bundle
from scripts.fixed_sgz023_peiqian import errors
class TypedWorks(unittest.TestCase):
 setUpClass=classmethod(FourBiographiesNER.setUpClass.__func__)
 altered=FourBiographiesNER.altered
 def test_exact_source_and_person_endpoint_conservation(self):
  c,ch,old,r,w=state(ROOT)
  self.assertEqual(Counter(m['kind']for p in ch['paragraphs']for m in p['mentions']),{'person':225,'work':26,'unresolved':12})
  a={m['id']:(m['start'],m['end'],m['surface'],m['person_id'])for p in ch['paragraphs']for m in p['mentions']}
  b={m['id']:(m['start'],m['end'],m['surface'],m['person_id'])for p in old['paragraphs']for m in p['mentions']}
  self.assertEqual(a,b);self.assertEqual(ch['text_sha256'],old['text_sha256'])
 def test_wrong_work_not_hidden_by_parent_source_view(self):
  ch=copy.deepcopy(self.ch);m=next(m for p in ch['paragraphs']for m in p['mentions']if m['surface']=='《惠帝起居注》');m['work_id']='w-jinji-ganbao-sgz028-reference'
  with self.altered({CH:ch}):self.assertTrue(errors(ch,ROOT))
 def test_wrong_author_rejected(self):
  reg=json.loads((ROOT/'registry/works.json').read_text());w=next(w for w in reg['works']if w['id']=='w-sgz023-reference-huidi-qijuzhu');w['source_author_attributions'][0]['author_person_id']='kbq_kjc_n2f_B'
  with self.altered({'registry/works.json':reg}):self.assertTrue(errors(self.ch,ROOT))
 def test_unknown_author_not_inferred(self):
  c,ch,old,r,works=state(ROOT)
  for wid in ['w-sgz023-reference-wenzhangxulu','w-jinzhugongzan-sgz022-luyu-reference']:
   self.assertFalse(works[wid].get('source_author_attributions'))
  self.assertEqual(len(c['expected_new_provenance']),7)
 def test_directory_navigation_does_not_invent_chapters(self):
  self.assertEqual(len(self.ch['cross_chapter_references']),7)
  for r in self.ch['cross_chapter_references']:
   self.assertEqual(r['target']['work_id'],'w-sanguozhi');self.assertIsNone(r['target']['chapter_id']);self.assertIsNone(r['target']['paragraph_id'])
  ch=copy.deepcopy(self.ch);ch['cross_chapter_references'][0]['target']['chapter_id']='c-invented'
  with self.altered({CH:ch}):self.assertTrue(errors(ch,ROOT))
 def test_author_finite_owner_rejects_parent_caller(self):
  c,ch,old,r,works=state(ROOT)
  ws=[w for w in works.values()if any(a.get('authorship_syntax',{}).get('kind')=='source_bound_fixed_sgz023_work_context'for a in w.get('source_author_attributions',[]))]
  self.assertEqual(len(ws),3)
  for w in ws:
   a=next(a for a in w['source_author_attributions']if a.get('authorship_syntax',{}).get('kind')=='source_bound_fixed_sgz023_work_context')
   self.assertTrue(author_valid(a,w,ch,ROOT));self.assertFalse(author_valid(a,w,old,ROOT))
 def test_bundle_cannot_substitute_untyped_parent_view(self):
  c,ch,old,r,w=state(ROOT);records=[old if x.get('id')==ch['id']else x for x in self.records]
  with self.assertRaises(AssertionError):guard_bundle(ROOT,'kbq_kjc_n2f_B',self.people,records)
