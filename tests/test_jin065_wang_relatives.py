from pathlib import Path
import copy,hashlib,json,unittest
from scripts.jin065_relatives import gift_valid,succession_valid
from scripts.validate_corpus import source_age_number
from scripts.liuxiaobiao_layers import valid as comment_valid
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads((R/p).read_text())
class WangRelatives(unittest.TestCase):
 def setUp(self):
  self.ch=read('corpus/jinshu/065.json');self.para={p['id']:(self.ch['id'],p)for p in self.ch['paragraphs']};self.ms={m['id']:(self.ch['id'],p['id'],m)for _,p in self.para.values()for m in p['mentions']};self.proof=read('source-evidence/jin065-wang-descendants/reading.json')
 def test_ranges_and_sources(self):
  q=self.proof
  for w in q['source_layers'].values():self.assertEqual(hashlib.sha256((R/w['raw_path']).read_bytes()).hexdigest(),w['raw_sha256'])
  for x in q['printed_witness']['pages']:
   self.assertEqual(x['source_url'], f"{q['printed_witness']['url']}#page={x['pdf_page']}")
   self.assertRegex(x['capture_sha256'],r'^[0-9a-f]{64}$')
  for x in q['comparisons']:
   a=x['source'];self.assertEqual(self.para[a['paragraph_id']][1]['text'][a['start']:a['end']],a['quote'])
   for s in x['witnesses']:
    t=(R/q['source_layers'][s['witness']]['raw_path']).read_text();self.assertEqual(t[s['raw_start']:s['raw_end']],s['quote'])
  self.assertEqual(len(q['item_boundaries']),7)
  for n in q['reused_native_sources']:
   c=read(n['path']);self.assertEqual(c['id'],n['chapter_id']);self.assertTrue(n['paragraph_ids']);self.assertTrue(set(n['paragraph_ids'])<={p['id']for p in c['paragraphs']})
 def test_existing_ids_and_quotations(self):
  q=self.proof
  for row in q['graphic_variants']:
   a=self.ms[row['mention_id']][2];self.assertEqual((a['surface'],a['person_id']),(row['source_surface'],row['recorded_person_id']))
  pin=read('corpus/shishuoxinyu/009-wangdao-relatives.json');ya=read('corpus/shishuoxinyu/006-wangdao-relatives.json')
  for ch in (pin,ya):
   for p in ch['paragraphs']:
    if p['text_layer']=='received_chapter':continue
    self.assertTrue(comment_valid(p,ch,R));bad=copy.deepcopy(p);bad['source_quote']['raw_end']-=1;self.assertFalse(comment_valid(bad,ch,R))
  self.assertEqual([x['value']for x in pin['annotation']['age_assertions']],[20,22])
  self.assertEqual(source_age_number('二十有二'),22);self.assertIsNone(source_age_number('二十有'))
  self.assertEqual(q['chronology_disagreement']['modern_annal_year'],400);self.assertIsNone(q['chronology_disagreement']['inferred_biography_year'])
  decision,=q['identity_decisions']
  review=read(decision['review'])
  self.assertEqual(decision['person_id'],'ra9_tie_fu4')
  self.assertEqual(len(review['canonical_mentions']),3)
  for mention in review['canonical_mentions']:
   if mention['chapter_id']==self.ch['id']:
    self.assertEqual(self.ms[mention['mention_id']][2]['person_id'],decision['person_id'])
  for witness in review['name_witnesses']:
   line=(R/witness['path']).read_text().splitlines()[witness['line']-1]
   self.assertEqual(line[witness['start']:witness['end']],witness['quote'])
 def test_succession_cousins_and_gifts(self):
  old='th-wangdao4-100-30-111';events=read('corpus/jinshu/065-events.json')['events'];succ=next(x for x in events if x['id']==old);self.assertTrue(succession_valid(succ,self.para));self.assertFalse(succession_valid(dict(succ,title='爵'),self.para))
  hol=read('corpus/jinshu/065-titles.json')['holdings'];self.assertNotIn(old,[x['id']for x in hol]);self.assertEqual(read('corpus/shishuoxinyu/009-wangdao-relatives-titles.json')['holdings'][0]['title'],'武岡侯')
  ds={x['id']:x for x in read('corpus/jinshu/065-life-events.json')['events']};g=[x for x in hol if x['id'].startswith('th-jin065-relatives-')];self.assertEqual(len(g),4)
  for x in g:
   self.assertTrue(gift_valid(x,self.para,self.ms,ds));bad=copy.deepcopy(x);bad['posthumous_basis']['death_event_id']='unrelated';self.assertFalse(gift_valid(bad,self.para,self.ms,ds))
  kin=next(x for x in read('corpus/jinshu/065-assertions.json')['assertions']if x['id']=='a-jin065-mi-hua-elder');self.assertEqual(kin['subject_person_id'],'3c9_d1d_870');self.assertEqual(kin['object_person_id'],'7r6_k52_qji_ABAAFAB')
