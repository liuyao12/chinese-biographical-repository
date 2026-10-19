# coding: utf-8
import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
J=lambda rel:json.loads((ROOT/rel).read_text())
class Jin037CollationPending(unittest.TestCase):
 def test_fixed_digital_source_not_silently_emended(self):
  rows=J('data/research/early-medieval-family-pending.json');r=next(r for r in rows['records'] if r['id']=='pending-jin037-pengcheng-fan-xin');a=r['proposal']['source_anchor'];ch=J('corpus/jinshu/037.json');p=next(p for p in ch['paragraphs'] if p['id']==a['paragraph_id'])
  self.assertEqual(p['text'][a['start']:a['end']],a['surface']);self.assertEqual(a['surface'],'心二萬三千戶');self.assertFalse(ch['source']['image_verified']);self.assertEqual(r['person_ids'],['dkn_ge4_286_AAADAAA'])
 def test_pending_bidirectional_index(self):
  d=J('data/research/early-medieval-family-pending.json');pid='dkn_ge4_286_AAADAAA';rid='pending-jin037-pengcheng-fan-xin';self.assertEqual(d['person_index'][pid].count(rid),1);self.assertIn(pid,next(r for r in d['records'] if r['id']==rid)['person_ids'])
