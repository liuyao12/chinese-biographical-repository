from pathlib import Path
import json,hashlib,unittest
R=Path(__file__).resolve().parents[1];MID='c-sanguozhi-024-cuilin:p001:m0194'
class XiangBiejiaAnchor(unittest.TestCase):
 def test_received_phrase_person_span_and_registry_agree(self):
  c=json.loads((R/'corpus/sanguozhi/024-cuilin.json').read_bytes());p=c['paragraphs'][0];m=next(x for x in p['mentions']if x['id']==MID);self.assertEqual(p['text'][191:196],'寧當相累邪');self.assertEqual((m['start'],m['end'],m['surface']),(193,194,'相'));self.assertEqual(p['text'][194],'累');self.assertEqual(m['status'],'contextual_provisional');q=next(x for x in json.loads((R/'registry/persons.json').read_bytes())['persons']if x['id']==m['person_id']);self.assertEqual([a['surface']for a in q['aliases']if MID in a['mention_ids']],['相']);self.assertEqual([(e['quote'],e['source_id'])for e in q['evidence']if e['mention_id']==MID],[('相',c['source_id'])])
 def test_correction_keeps_historical_capture_and_source_wording(self):
  q=json.loads((R/'source-evidence/sgz024-cuilin/xianglei-span-review.json').read_bytes());self.assertFalse(q['wording_changed']);self.assertFalse(q['identity_changed']);self.assertFalse(q['mid_changed']);self.assertFalse(q['human_reviewed']);x=q['historical_capture'];self.assertEqual(hashlib.sha256((R/x['path']).read_bytes()).hexdigest(),x['sha256'])
