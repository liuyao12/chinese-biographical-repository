import json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
class CaoxiuWorkReferences(unittest.TestCase):
 def setUp(self):
  self.d=json.loads((R/'corpus/sanguozhi/009-caoxiu.json').read_text());self.ms=[m for p in self.d['paragraphs']for m in p['mentions']if m.get('kind')=='work'];self.ws={w['id']:w for w in json.loads((R/'registry/works.json').read_text())['works']}
 def test_four_titles(self):
  self.assertEqual([m['surface']for m in self.ms],['魏書','魏書','世語','文士傳'])
  for p in self.d['paragraphs']:
   for m in p['mentions']:
    if m.get('kind')=='work':self.assertEqual(p['text'][m['start']:m['end']],m['surface']);self.assertNotIn('work_reference_resolution',m)
 def test_source_scope_except_source_proven_shiyu(self):
  for m in self.ms:
   if m['surface']=='世語':
    self.assertEqual(m['work_id'],'w-shiyu-sgz027-reference');self.assertEqual(self.ws[m['work_id']]['author'],'郭頒');self.assertEqual(self.ws[m['work_id']]['citation_title'],'魏晉世語')
   elif m['surface']=='魏書':
    self.assertEqual(m['work_id'],'w-weishu-wangshen');self.assertIn('王沈',self.ws[m['work_id']]['author']);self.assertEqual(self.d['annotation']['weishu_identity_review']['status'],'contextual_provisional')
   else:self.assertIn('sgz009-caoxiu-reference',m['work_id']);self.assertIsNone(self.ws[m['work_id']]['author'])
 def test_duplicate_work_removed_from_every_public_index(self):
  old='w-shiyu-sgz009-caoxiu-reference';self.assertNotIn(old,self.ws)
  for path in ('registry/work-provenance.json','data/corpus/work-provenance.json'):
   self.assertNotIn(old,json.loads((R/path).read_text())['works'])
  self.assertNotIn(old,{w['id']for w in json.loads((R/'data/corpus/work-titles.json').read_text())['works']})
 def test_review_points_to_resolvable_primary_authority(self):
  review=self.d['annotation']['work_reference_reviews'][0];case=next(x for x in review['cross_work_identity_evidence']if x['id']=='work-identity-caoxiu-shiyu');proof=json.loads((R/case['authority_path']).read_text());self.assertEqual(case['work_id'],'w-shiyu-sgz027-reference');self.assertTrue(set(case['evidence_ids'])<={e['id']for e in proof['evidence']});self.assertEqual(next(a for a in proof['authorities']if a['id']==case['bibliographic_authority_id'])['work_id'],case['work_id'])
 def test_author_person_kept(self):
  p=self.d['paragraphs'][-1];self.assertTrue(any(m['kind']=='person' and m['surface']=='張隠'for m in p['mentions']));self.assertEqual(next(m['start']for m in p['mentions']if m['kind']=='work'),2)
 def test_reciprocal(self):
  for p in self.d['paragraphs']:
   for m in p['mentions']:
    if m.get('kind')=='work':self.assertIn({'chapter_id':self.d['id'],'source_id':self.d['source_id'],'paragraph_id':p['id'],'mention_id':m['id'],'quote':p['text']},self.ws[m['work_id']]['reference_attestations'])
