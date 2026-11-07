"""Attribution/reading limits remain data; no ancient or authorship claim inferred."""
import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class ReferenceIdentityTests(unittest.TestCase):
 def decisions(self):return {d['id']:d for d in json.loads((ROOT/'corpus/shiji/130-identities.json').read_text())['decisions']}
 def test_huangzi_mediated_not_direct_commentary(self):
  d=self.decisions()['d-shiji130-reference-two-001'];self.assertEqual(d['source_context_confidence'],'medium_high_contextual');r=d['references'][0];self.assertFalse(r['reported_ancient_commentary']['directly_read']);self.assertEqual(r['author'],'王國維');self.assertEqual(r['revision_id_reported_in_read_page'],2335248);self.assertIn('徐說殆是也',r['short_quote'])
 def test_zuoqiu_traditional_identity_not_authorship_verdict(self):
  d=self.decisions()['d-shiji130-reference-two-002'];self.assertFalse(d['identity_event_qualification']['authorship_question_resolved']);self.assertEqual(d['references'][0]['revision_id_reported_in_read_page'],7904593);self.assertFalse(d['human_reviewed']);self.assertIsNone(d['model'])
 def test_reference_is_not_native_hanshu_evidence(self):
  for d in self.decisions().values():
   if d['id'].startswith('d-shiji130-reference-two-'):
    self.assertFalse(any(e['chapter_id'].startswith('c-hanshu-062')for e in d['evidence']))
 def test_unknown_bibliography_not_filled(self):
  for d in self.decisions().values():
   if d['id'].startswith('d-shiji130-reference-two-'):
    for r in d['references']:
     for k in ['composition_date','earliest_extant_edition','earliest_extant_edition_date','transcription_base_edition']:
      self.assertIsNone(r.get(k))
if __name__=='__main__':unittest.main()
