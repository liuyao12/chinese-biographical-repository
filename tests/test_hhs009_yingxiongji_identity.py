import json,hashlib,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1];W='w-hanmo-yingxiongji';PRE='source-evidence/yingxiongji-native-identity/'
class HeroIdentity(unittest.TestCase):
 def setUp(self):
  self.c=json.loads((R/'corpus/houhanshu/009.json').read_text());self.p=next(p for p in self.c['paragraphs']if p['id'].endswith('chuping01-note-06-1'));self.w=next(w for w in json.loads((R/'registry/works.json').read_text())['works']if w['id']==W);self.review=json.loads((R/PRE/'review.json').read_text())
 def test_precise_lixian_marker(self):
  m=next(m for m in self.p['mentions']if m.get('work_id')==W);self.assertEqual((m['start'],m['end'],m['surface']),(0,3,'英雄記'));self.assertEqual(m['status'],'contextual_provisional');self.assertEqual(self.p['text_layer'],'witness_appended_lixian_note');self.assertEqual(self.p['layer_attribution']['attributed_author'],'李賢');self.assertNotIn('source_author_attributions',self.w)
 def test_reciprocal_attestation(self):
  m=next(m for m in self.p['mentions']if m.get('work_id')==W);self.assertIn({'chapter_id':self.c['id'],'source_id':self.c['source_id'],'paragraph_id':self.p['id'],'mention_id':m['id'],'quote':self.p['text']},self.w['reference_attestations']);self.assertEqual(self.w['status'],'referenced_only')
 def test_raws_hashes_and_exact_catalogue_entries(self):
  for s in self.review['bibliographic_sources']:self.assertEqual(hashlib.sha256((R/s['path']).read_bytes()).hexdigest(),s['raw_sha256'])
  for a in self.review['catalogue_proofs']:self.assertEqual((R/a['file']).read_text()[a['start']:a['end']],a['quote'])
  u=self.review['pei_parallel_full_unit'];self.assertEqual((R/u['file']).read_text()[u['start']:u['end']],u['text']);self.assertIn('匡字公節',u['text'])
 def test_variants_and_unknown_years(self):
  self.assertEqual(self.w['citation_title'],'漢末英雄記');a=self.review['research_snapshot_before_adoption'];self.assertEqual([x['title']for x in a['received_titles']],['英雄記','漢末英雄記','漢書英雄記']);self.assertIn('等',self.w['author']);m=json.loads((R/'registry/work-provenance.json').read_text())['works'][W]
  for k in ['composition','earliest_extant_edition']:self.assertEqual(m[k],{'status':'not_researched','assertions':[]})
 def test_no_unimported_pei_marking(self):
  chapters=[]
  for p in(R/'corpus').glob('*/*.json'):
   c=json.loads(p.read_text())
   if any(m.get('work_id')==W for pa in c.get('paragraphs',[])for m in pa['mentions']):chapters.append(c['id'])
  self.assertEqual(chapters,[self.c['id']])
