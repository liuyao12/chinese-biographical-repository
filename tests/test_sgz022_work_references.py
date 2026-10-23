import json,unittest
from pathlib import Path
from scripts.source_author_prefix import source_author_errors
R=Path(__file__).resolve().parents[1]
class ChenWorkReferences(unittest.TestCase):
 def setUp(self):
  self.d=json.loads((R/'corpus/sanguozhi/022-chenqun-chentai.json').read_text());self.ps={p['id']:p for p in self.d['paragraphs']};self.ms=[m for p in self.d['paragraphs']for m in p['mentions']if m['kind']=='work'];self.ws={w['id']:w for w in json.loads((R/'registry/works.json').read_text())['works']}
 def test_complete16_and19_titles(self):
  self.assertEqual(len(self.ps),16);self.assertEqual(len(self.ms),19)
  for p in self.ps.values():
   for m in p['mentions']:
    if m['kind']=='work':self.assertEqual(p['text'][m['start']:m['end']],m['surface']);self.assertNotIn('work_reference_resolution',m)
 def test_ui_title_and_qualification(self):
  for m in self.ms:
   w=self.ws[m['work_id']];self.assertNotIn('（',w['citation_title']);self.assertTrue(w['citation_qualification'])
 def test_chenzi_is_work_not_chengji_alias(self):
  m=next(m for m in self.ms if m['surface']=='陳子');self.assertEqual(m['id'],self.d['id']+':p003:m0085');self.assertEqual(m['work_id'],'w-chenzi');self.assertIsNone(m['person_id']);p=next(x for x in json.loads((R/'registry/persons.json').read_text())['persons']if x['id']=='9w8_tqh_ysn_A');self.assertFalse(any(m['id']in a['mention_ids']for a in p['aliases']));self.assertFalse(any(e.get('mention_id')==m['id']for e in p['evidence']))
 def test_sunzi_is_provisional_not_expanded_or_person_merge(self):
  m=next(m for m in self.ms if m['surface']=='孫子');self.assertEqual((m['work_id'],m['status']),('w-sunzi-sgz022-reference','contextual_provisional'));review=next(x for x in self.d['annotation']['work_reference_reviews']if x['id']=='work-review-sanguozhi022-chenqun-chentai');prior=next(x['before']for x in review['role_corrections']if x['before']['surface']=='孫子');self.assertEqual(prior['kind'],'unresolved');self.assertIn('candidate_person_ids',prior)
 def test_hanshu_subdivision_not_false_full_title(self):
  m=next(m for m in self.ms if m['surface']=='漢書地理志');self.assertEqual(self.ws[m['work_id']]['citation_title'],'漢書');self.assertIn('地理志',self.ws[m['work_id']]['citation_qualification'])
 def test_bowuji_not_automatically_bowuzhi(self):
  m=next(m for m in self.ms if m['surface']=='博物記');self.assertEqual(m['work_id'],'w-bowuji-sgz022-reference');self.assertIsNone(self.ws[m['work_id']]['author'])
 def test_actual_ganbao_prefix(self):
  ws={k:dict(v,source_author_attributions=[e for e in v.get('source_author_attributions',[])if e['chapter_id']==self.d['id']])for k,v in self.ws.items()};es=[e for w in ws.values()for e in w['source_author_attributions']];self.assertEqual(len(es),1);self.assertEqual(es[0]['author_surface'],'干寶');self.assertEqual(source_author_errors(ws,{self.d['id']:self.d}),[])
 def test_full_reverse_citations(self):
  for p in self.ps.values():
   for m in p['mentions']:
    if m['kind']=='work':self.assertIn({'chapter_id':self.d['id'],'source_id':self.d['source_id'],'paragraph_id':p['id'],'mention_id':m['id'],'quote':p['text']},self.ws[m['work_id']]['reference_attestations'])

 def test_chenzi_comparison_roles_and_original_quantities(self):
  p=self.ps[self.d['id']+':p003'];m=next(m for m in p['mentions']if m['surface']=='陳子');h=json.loads((R/'corpus/houhanshu/062.json').read_text());hp=next(p for p in h['paragraphs']if p['id'].endswith(':chen:chen-ji-body'));hm=next(m for m in hp['mentions']if m['surface']=='陳子');self.assertEqual(m['work_id'],hm['work_id']);self.assertEqual(m['kind'],hm['kind']);self.assertEqual(m['status'],'contextual_provisional');self.assertIn('著書數十篇世謂之陳子',p['text']);self.assertIn('發憤著書數萬言號曰陳子',hp['text']);authors={m['person_id']for m in p['mentions']if m['surface']=='紀'};self.assertIn(hp['mentions'][0]['person_id'],authors);review=next(x for x in self.d['annotation']['work_reference_reviews']if x['id']=='work-review-sanguozhi022-chenqun-chentai')['chenzi_role_review'];self.assertEqual(review['status'],'editorial_provisional');self.assertEqual(review['alternative_readings'][0]['kind'],'person_honorific');self.assertIn('022世謂之陳子仍為人物稱呼',review['alternative_readings'][0]['prior_registry_note'])
