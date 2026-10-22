# coding: utf-8
"""Source-specific regression: quoted old histories are not title-string merges."""
from pathlib import Path
import json,unittest,hashlib
ROOT=Path(__file__).resolve().parents[1]
class WangchangWorkTests(unittest.TestCase):
 def setUp(self):
  self.d=json.loads((ROOT/'corpus/sanguozhi/027-wangchang.json').read_text());self.ms={m['surface']:m for p in self.d['paragraphs']for m in p['mentions']if m['kind']=='work'};self.ws={w['id']:w for w in json.loads((ROOT/'registry/works.json').read_text())['works']}
 def test_complete_twenty_paragraph_unit_and_raw(self):
  self.assertEqual(len(self.d['paragraphs']),20);raw=(ROOT/self.d['source']['raw_path']).read_bytes();self.assertEqual(hashlib.sha256(raw).hexdigest(),self.d['source']['raw_file_sha256'])
 def test_all_seven_explicit_titles_marked(self):
  self.assertEqual(set(self.ms),{'孫子兵法','王氏譜','郭林宗傳','治論','國語','世語','晉書','晉陽秋'})
 def test_original_sunzi_anchor_preserved(self):
  m=self.ms['孫子兵法'];self.assertEqual((m['id'],m['start'],m['end'],m['work_id']),('c-sanguozhi-027-wangchang:unit004:m0000',0,4,'w-sunzi-bingfa'))
 def test_quoted_jinshu_is_not_tang_compilation(self):
  self.assertNotEqual(self.ms['晉書']['work_id'],'w-jinshu');self.assertIsNone(self.ws[self.ms['晉書']['work_id']]['author'])
 def test_received_short_title_with_source_proven_bibliography(self):
  m=self.ms['世語'];w=self.ws[m['work_id']];self.assertEqual(m['surface'],'世語');self.assertEqual(m['work_id'],'w-shiyu-sgz027-reference');self.assertNotIn('魏晉世語',w['title']);self.assertEqual(w['author'],'郭頒');self.assertEqual(w['citation_title'],'魏晉世語');self.assertEqual(w['bibliographic_authority_id'],'authority-pei-shiyu')
 def test_only_attested_zhilun_title_not_generic_binshu(self):
  self.assertEqual(self.ws[self.ms['治論']['work_id']]['author'],'王昶');self.assertNotIn('兵書',self.ms)
 def test_unnamed_biezhuan_has_qualification_not_invented_title(self):
  reviews=self.d['annotation']['work_reference_reviews'];self.assertTrue(any(x['surface']=='别傳'for r in reviews for x in r['boundaries']));self.assertNotIn('别傳',self.ms)
 def test_registry_both_ends_exact(self):
  ps={p['id']:p for p in self.d['paragraphs']}
  for m in self.ms.values():
   w=self.ws[m['work_id']];a=next(a for a in w['reference_attestations']if a['mention_id']==m['id']);self.assertEqual(ps[a['paragraph_id']]['text'],a['quote']);self.assertIsNone(m['person_id'])
if __name__=='__main__':unittest.main()
