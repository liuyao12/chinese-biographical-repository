import json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
class WanglingWorkReferences(unittest.TestCase):
 def setUp(self):
  self.d=json.loads((R/'corpus/sanguozhi/028-wangling.json').read_text());self.ms=[m for p in self.d['paragraphs'] for m in p['mentions'] if m.get('kind')=='work'];self.ws={w['id']:w for w in json.loads((R/'registry/works.json').read_text())['works']}
 def test_thirteen_literal_titles(self):
  self.assertEqual(len(self.ms),13)
  for p in self.d['paragraphs']:
   for m in p['mentions']:
    if m.get('kind')=='work':self.assertEqual(p['text'][m['start']:m['end']],m['surface']);self.assertIsNone(m['person_id']);self.assertNotIn('work_reference_resolution',m)
 def test_weishu_not_later_or_unproved_author(self):
  ms=[m for m in self.ms if m['surface']=='魏書'];self.assertEqual([m['work_id']for m in ms],['w-weishu-wangshen']);self.assertNotEqual(ms[0]['work_id'],'w-weishu-weishou');self.assertIn('上下文',self.ws[ms[0]['work_id']]['citation_qualification'])
 def test_author_and_scope(self):
  self.assertEqual(self.ws['w-jinji-ganbao-sgz028-reference']['author'],'干寳');self.assertEqual(self.ws['w-hanjinchunqiu-sgz028-reference']['author'],'習鑿齒');self.assertEqual([m['work_id']for m in self.ms if m['surface']=='春秋'],['w-chunqiu-sgz028-reference'])
 def test_shiji_source_bridge(self):
  review=next(v for v in self.d['annotation']['work_reference_reviews']if v['id']=='work-review-sanguozhi028-wangling');ev=review['cross_work_identity_evidence'][0];self.assertEqual(ev['work_id'],'w-shiji');self.assertIn('目論',ev['quote']);self.assertIn('無彊',ev['quote']);self.assertEqual([m['work_id']for m in self.ms if m['surface']=='史記'],['w-shiji'])
 def test_reciprocal_attestations(self):
  for p in self.d['paragraphs']:
   for m in p['mentions']:
    if m.get('kind')=='work':self.assertIn({'chapter_id':self.d['id'],'source_id':self.d['source_id'],'paragraph_id':p['id'],'mention_id':m['id'],'quote':p['text']},self.ws[m['work_id']]['reference_attestations'])
