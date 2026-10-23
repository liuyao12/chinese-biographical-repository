import json,hashlib,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1];PREFIX='source-evidence/pei-weishu-author-identity/'
OLD={'w-weishu-sgz028-reference','w-weishu-sgz009-caoxiu-reference','w-weishu-sgz009-caozhen-reference','w-weishu-sgz010-reference','w-weishu-sgz022-reference'};NEW='w-weishu-wangshen'
ORIGINAL_CHAPTERS={'c-sanguozhi-009-caoxiu','c-sanguozhi-009-caozhen','c-sanguozhi-010-xunyu-xunyou-jiaxu','c-sanguozhi-022-chenqun-chentai','c-sanguozhi-028-wangling'}
class PeiWeishuIdentity(unittest.TestCase):
 def test_canonical_and_unchanged_separate_books(self):
  w={w['id']:w for w in json.loads((R/'registry/works.json').read_text())['works']};self.assertTrue(OLD.isdisjoint(w));self.assertIn('w-weishu-weishou',w);self.assertIn('w-sanguozhi',w);self.assertEqual(len([e for e in w[NEW]['reference_attestations']if e['chapter_id'] in ORIGINAL_CHAPTERS]),14);self.assertIn('上下文',w[NEW]['citation_qualification'])
 def test_five_raws_resolve_and_hash(self):
  e=json.loads((R/PREFIX/'review.json').read_text())['evidence'];self.assertEqual(len(e['sources.json']['sources']),5)
  for s in e['sources.json']['sources']:self.assertEqual(hashlib.sha256((R/s['path']).read_bytes()).hexdigest(),s['raw_sha256'])
  for a in e['anchors.json']:self.assertEqual((R/a['raw_path']).read_text()[a['raw_start']:a['raw_end']],a['quote'])
 def test_volume_variants_and_no_composition_year(self):
  e=json.loads((R/PREFIX/'review.json').read_text())['evidence']['audit_before_identity_proposal'];self.assertEqual([x['volumes']for x in e['catalogue_extents']],[48,44,47]);m=json.loads((R/'registry/work-provenance.json').read_text());self.assertTrue(OLD.isdisjoint(m['works']))
 def test_reciprocal_literal_marks_contextual_review(self):
  ws={w['id']:w for w in json.loads((R/'registry/works.json').read_text())['works']};n=0
  for p in(R/'corpus/sanguozhi').glob('*.json'):
   c=json.loads(p.read_text())
   for para in c.get('paragraphs',[]):
    for m in para['mentions']:
     self.assertNotIn(m.get('work_id'),OLD)
     if m.get('work_id')==NEW:
      n+=1;self.assertEqual(para['text'][m['start']:m['end']],m['surface']);self.assertEqual(m['surface'],'魏書')
      if c['id'] in ORIGINAL_CHAPTERS:
       self.assertEqual(c['annotation']['weishu_identity_review']['status'],'contextual_provisional')
      else:
       ref=Path(c['annotation']['work_reference_review_path']);self.assertFalse(ref.is_absolute());self.assertNotIn('..',ref.parts)
       review=json.loads((R/ref).read_text());self.assertIs(review['human_reviewed'],False)
       decision,=[x for x in review['decisions'] if x['work_id']==NEW]
       self.assertTrue(decision['qualification'].strip())
       self.assertIn('魏收',decision['qualification'])
      self.assertIn({'chapter_id':c['id'],'source_id':c['source_id'],'paragraph_id':para['id'],'mention_id':m['id'],'quote':para['text']},ws[NEW]['reference_attestations'])
  self.assertEqual(n,len([e for e in ws[NEW]['reference_attestations'] if e['chapter_id'].startswith('c-sanguozhi')]))
