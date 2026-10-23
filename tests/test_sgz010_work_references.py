import json,unittest
from pathlib import Path
from scripts.source_author_prefix import source_author_errors
R=Path(__file__).resolve().parents[1]
class XunWorkReferences(unittest.TestCase):
 def setUp(self):
  self.d=json.loads((R/'corpus/sanguozhi/010.json').read_text());self.ps={p['id']:p for p in self.d['paragraphs']};self.ms=[m for p in self.d['paragraphs']for m in p['mentions']if m['kind']=='work'];self.ws={w['id']:w for w in json.loads((R/'registry/works.json').read_text())['works']}
 def test_all55_and46_titles(self):
  self.assertEqual(len(self.d['paragraphs']),55);self.assertEqual(len(self.ms),46)
  for p in self.d['paragraphs']:
   for m in p['mentions']:
    if m['kind']=='work':self.assertEqual(p['text'][m['start']:m['end']],m['surface']);self.assertNotIn('work_reference_resolution',m)
 def test_ui_citation_title_not_qualified_registry_label(self):
  for m in self.ms:
   w=self.ws[m['work_id']];self.assertTrue(w['citation_title']);self.assertNotIn('（',w['citation_title']);self.assertTrue(w['citation_qualification'])
 def test_two_hanji_authors_not_conflated(self):
  ms=[m for m in self.ms if m['surface']=='漢紀'];self.assertEqual({m['work_id']for m in ms},{'w-hanji-zhangfan-sgz010-reference','w-hanji-xunyue-sgz010-reference'})
 def test_narrow_title_correction_keeps_mid(self):
  p=self.ps[self.d['id']+':full:u012'];m=next(m for m in p['mentions']if m['id'].endswith('m0011'));self.assertEqual((m['kind'],m['surface'],m['work_id']),('work','平原禰衡傳','w-pingyuan-ni-heng-zhuan'));person=next(p for p in json.loads((R/'registry/persons.json').read_text())['persons']if p['id']=='727_51c_19b');self.assertFalse(any(m['id']in a['mention_ids']for a in person['aliases']));self.assertFalse(any(e.get('mention_id')==m['id']for e in person['evidence']))
 def test_curved_ritual_is_not_book(self):
  p=self.ps[self.d['id']+':descendants:p001'];i=p['text'].index('曲禮');self.assertFalse(any(m['kind']=='work'and max(m['start'],i)<min(m['end'],i+2)for m in p['mentions']))
 def test_reused_specific_bridges(self):
  self.assertEqual({m['work_id']for m in self.ms if m['surface']=='傅子'},{'w-fuzi-pei-reference'});self.assertEqual({m['work_id']for m in self.ms if m['surface']=='世語'},{'w-shiyu-sgz027-reference'});self.assertEqual({m['work_id']for m in self.ms if m['surface']=='晉紀'},{'w-jinji-ganbao-sgz028-reference'})
 def test_seven_source_author_anchors(self):
  ws={k:dict(v,source_author_attributions=[e for e in v.get('source_author_attributions',[])if e['chapter_id']==self.d['id']])for k,v in self.ws.items()};self.assertEqual(sum(len(w['source_author_attributions'])for w in ws.values()),7);self.assertEqual(source_author_errors(ws,{self.d['id']:self.d}),[])
 def test_full_reverse_quotes(self):
  for p in self.d['paragraphs']:
   for m in p['mentions']:
    if m['kind']=='work':self.assertIn({'chapter_id':self.d['id'],'source_id':self.d['source_id'],'paragraph_id':p['id'],'mention_id':m['id'],'quote':p['text']},self.ws[m['work_id']]['reference_attestations'])
