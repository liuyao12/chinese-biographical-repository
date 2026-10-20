# coding: utf-8
"""Source-specific regression; uses only repository-native files."""
import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(n):return json.loads((ROOT/n).read_text())
class WangchangFacts(unittest.TestCase):
 def setUp(self):
  self.c=read('corpus/sanguozhi/027-wangchang.json');self.a=read('source-evidence/sanguozhi027-wang35-consumption.json');self.h=read('corpus/sanguozhi/027-wangchang-titles.json')['holdings'];self.e=read('corpus/sanguozhi/027-wangchang-life-events.json')['events']
 def test_complete_consumption(self):
  self.assertEqual(len(self.a['ledger']),142);self.assertEqual(len(self.a['proposal_records']),142);self.assertEqual({r['id']for r in self.a['proposal_records']},{r['proposal_id']for r in self.a['ledger']})
 def test_literal_full_paragraph_evidence(self):
  ps={p['id']:p for p in self.c['paragraphs']};self.assertEqual(len(self.h),48)
  for h in self.h:
   self.assertFalse(h['human_reviewed'])
   for e in h['evidence']:self.assertEqual(e['quote'],ps[e['paragraph_id']]['text'])
   for a in h['attestations']:self.assertEqual(ps[a['paragraph_id']]['text'][a['start']:a['end']],a['surface'])
 def test_death_not_general_office_termination(self):
  d=[e for e in self.e if e.get('normalized_date',{}).get('year')==259];self.assertEqual(len(d),1);self.assertIn('甘露四年',d[0]['evidence'][0]['quote'])
  for h in self.h:self.assertEqual(h['effective_period']['end']['status'],'unknown')
 def test_236_is_attestation_not_investiture(self):
  h=next(h for h in self.h if h['title']=='太尉');self.assertEqual(h['mode'],'attestation');self.assertEqual(h['effective_period']['start']['status'],'unknown');self.assertEqual(h['attestations'][0]['normalized_date']['year'],236)
 def test_initial_era_is_range(self):
  h=next(h for h in self.h if h['title']=='太傅');d=h['attestations'][0]['normalized_date_range'];self.assertEqual((d['earliest']['year'],d['latest']['year']),(249,254));self.assertEqual(d['source_expression'],'嘉平初')
 def test_age_is_during_life_not_birth_estimate(self):
  aa=self.c['annotation']['age_assertions'];ours=[a for a in aa if a['id'].startswith('age-wang35-')];self.assertEqual(len(ours),2)
  for a in ours:self.assertEqual(a['age_context']['kind'],'during_life')
 def test_unknown_person_not_forced_and_corrections_retained(self):
  unknown=[r for r in self.a['proposal_records']if r['category']=='name_components'and r['person_id']is None];self.assertEqual(len(unknown),3)
  ledger={r['proposal_id']:r for r in self.a['ledger']}
  for r in unknown:self.assertEqual(ledger[r['id']]['state'],'typed')
  self.assertTrue(any(r['category']=='reported_person_identification_correction'for r in self.a['proposal_records']))
if __name__=='__main__':unittest.main()
