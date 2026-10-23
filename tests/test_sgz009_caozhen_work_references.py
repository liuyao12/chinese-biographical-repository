import json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
class CaozhenWorkReferences(unittest.TestCase):
 def setUp(self):
  self.d=json.loads((R/'corpus/sanguozhi/009-caozhen.json').read_text());self.ms=[m for p in self.d['paragraphs']for m in p['mentions']if m.get('kind')=='work'];self.ws={w['id']:w for w in json.loads((R/'registry/works.json').read_text())['works']}
 def test_complete_coverage(self):
  self.assertEqual(len(self.d['paragraphs']),45);self.assertEqual(len(self.ms),33)
  for p in self.d['paragraphs']:
   for m in p['mentions']:
    if m.get('kind')=='work':self.assertEqual(p['text'][m['start']:m['end']],m['surface']);self.assertNotIn('work_reference_resolution',m)
 def test_source_scope_unknown_author(self):
  for m in self.ms:self.assertIn(m['work_id'],self.ws)
  self.assertEqual({m['work_id']for m in self.ms if m['surface']in ('魏略','魏畧')},{'w-weilue-sgz028-reference'});self.assertEqual({m['work_id']for m in self.ms if m['surface']=='世語'},{'w-shiyu-sgz027-reference'})
  for slug,author in [('shiyaolun','桓範'),('daodelun','何晏'),('lienvzhuan','皇甫謐'),('jinji','干寳')]:self.assertEqual(self.ws['w-'+slug+'-sgz009-caozhen-reference']['author'],author)
 def test_three_jin_titles_unmerged(self):
  ids={m['work_id']for m in self.ms if m['surface']in ('晉記','晉紀','晉書')};self.assertEqual(len(ids),3);self.assertNotIn('w-jinshu',ids)
 def test_weilue_original_forms(self):
  ms=[m for m in self.ms if m['surface']in ('魏略','魏畧')];self.assertEqual({m['surface']for m in ms},{'魏略','魏畧'});self.assertEqual(len({m['work_id']for m in ms}),1)
 def test_classic_not_commentary(self):
  self.assertEqual({m['work_id']for m in self.ms if m['surface']=='春秋'},{'w-chunqiu-sgz009-caozhen-reference'})
 def test_reciprocal(self):
  for p in self.d['paragraphs']:
   for m in p['mentions']:
    if m.get('kind')=='work':self.assertIn({'chapter_id':self.d['id'],'source_id':self.d['source_id'],'paragraph_id':p['id'],'mention_id':m['id'],'quote':p['text']},self.ws[m['work_id']]['reference_attestations'])

 def test_source_author_anchors(self):
  ps={p['id']:p for p in self.d['paragraphs']};evs=[v for w in self.ws.values()for v in w.get('source_author_attributions',[])if v['chapter_id']==self.d['id']];self.assertEqual(len(evs),7)
  for v in evs:
   p=ps[v['paragraph_id']];a=next(m for m in p['mentions']if m['id']==v['author_mention_id']);w=next(m for m in p['mentions']if m['id']==v['work_mention_id']);self.assertEqual(a['surface'],v['author_surface']);self.assertEqual(a['person_id'],v['author_person_id']);self.assertEqual(w['work_id'],v['referenced_work_id']);self.assertEqual(p['text'],v['quote']);self.assertLessEqual(a['end'],w['start'])
