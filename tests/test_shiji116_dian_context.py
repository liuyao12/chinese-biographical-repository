import json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
TARGET={f'c-shiji-116-xinanyi:m009-{n}' for n in ['0016','0021','0089','0100','0127']}
PID='h0h_wsl_1nf'
def read(p):return json.loads((R/p).read_text())
class DianContext(unittest.TestCase):
 def test_exact_five_contextual_mentions_and_dynasty_exclusion(self):
  c=read('corpus/shiji/116.json');ms={m['id']:m for p in c['paragraphs']for m in p['mentions']}
  for mid in TARGET:self.assertEqual((ms[mid]['person_id'],ms[mid]['surface'],ms[mid]['status']),(PID,'滇王','contextual_provisional'))
  self.assertIsNone(ms['c-shiji-116-xinanyi:m011-0041']['person_id'])
  self.assertIsNone(ms['c-shiji-116-xinanyi:m006-0018']['person_id'])
 def test_decision_keeps_named_anchor_continuity_and_succession_uncertainty(self):
  d=read('corpus/shiji/116-identities.json')['decisions'][0];b=d['identification_basis'];self.assertEqual(d['person_id'],PID);self.assertEqual(set(b['target_mention_ids']),TARGET);self.assertEqual(b['source_named_person_mention_ids'],['c-shiji-116-xinanyi:m005-0145']);self.assertFalse(b['explicit_name_in_target_passage']);self.assertTrue(b['possible_unrecorded_succession']);self.assertEqual(b['witness_independence'],'not_assumed');self.assertFalse(d['human_reviewed']);self.assertEqual(d['confidence_level'],'moderate');self.assertIn('始首善',d['evidence'][-1]['quote']);self.assertIn('常有善意',d['references'][0]['quote'])
 def test_kingship_mentions_do_not_make_seal_gift_an_accession(self):
  h=next(h for h in read('corpus/shiji/116-titles.json')['holdings']if h['id']=='th-shiji116-020');self.assertEqual(h['mode'],'attestation');self.assertEqual(h['person_id'],PID);self.assertEqual({a['person_mention_id']for a in h['attestations']},TARGET)
  for a in h['attestations']:
   if a['start']<70:self.assertIsNone(a['date_expression']);self.assertNotIn('normalized_date_range',a)
   else:self.assertEqual(a['date_expression'],'元封二年');self.assertEqual([a['normalized_date_range'][k]['era_year']for k in ['earliest','latest']],[110,109])
  for endpoint in h['effective_period'].values():self.assertEqual(endpoint['status'],'unknown');self.assertIsNone(endpoint['date_expression'])
 def test_registry_links_every_new_mention_and_displays_uncertainty(self):
  p=next(p for p in read('registry/persons.json')['persons']if p['id']==PID);self.assertTrue(TARGET.issubset({e['mention_id']for e in p['evidence']}));self.assertTrue(TARGET.issubset(set(next(a for a in p['aliases']if a['surface']=='滇王')['mention_ids'])));self.assertIn('不能排除',p['identity_note'])
if __name__=='__main__':unittest.main()
