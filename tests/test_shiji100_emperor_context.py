import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(f):return json.loads((ROOT/f).read_text())
def para(n):return next(p for p in read('corpus/shiji/100.json')['paragraphs'] if p['id'].endswith(f':p{n:03d}'))
class JibuEmperorContextTests(unittest.TestCase):
 def test_wen_emperor_in_jibu_summons_is_not_gaozu(self):
  ms=[m for m in para(3)['mentions'] if m['surface'] in {'上','陛下'}]
  self.assertEqual(len(ms),5);self.assertEqual({m['person_id'] for m in ms},{'yqp_nlb_p1p_AC'})
 def test_gaozu_in_pardon_and_luan_bu_speech(self):
  ms=[m for n in [1,7,8] for m in para(n)['mentions'] if m['surface'] in {'上','陛下'}]
  self.assertEqual(len(ms),14);self.assertEqual({m['person_id'] for m in ms},{'yqp_nlb_p1p_A'})
 def test_office_location_and_guest_words_are_not_emperor_mentions(self):
  for n,term in [(2,'上將軍'),(2,'殿上'),(4,'上客')]:
   p=para(n);pos=p['text'].index(term)
   self.assertFalse(any(m['start']<=pos+term.index('上')<m['end'] and m.get('person_id') in {'yqp_nlb_p1p_A','yqp_nlb_p1p_AC'} for m in p['mentions']))
 def test_context_decisions_point_to_actual_occurrences(self):
  ds=[d for d in read('corpus/shiji/100-identities.json')['decisions'] if d['id'].startswith('d-shiji100-emperor-')]
  self.assertEqual(len(ds),2);seen=[]
  for d in ds:
   self.assertFalse(d['human_reviewed']);self.assertEqual(d['status'],'contextual_provisional')
   for e in d['evidence']:
    p=next(p for p in read('corpus/shiji/100.json')['paragraphs'] if p['id']==e['paragraph_id']);self.assertEqual(e['quote'],p['text'])
    for mid in e['mention_ids']:
     m=next(m for m in p['mentions'] if m['id']==mid);self.assertEqual(m['person_id'],d['person_id']);seen.append(mid)
  self.assertEqual(len(set(seen)),19)
