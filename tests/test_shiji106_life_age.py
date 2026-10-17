import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class LifeAge(unittest.TestCase):
 def setUp(self):
  self.c=json.loads((ROOT/'corpus/shiji/106.json').read_text());self.events=json.loads((ROOT/'corpus/shiji/106-life-events.json').read_text())['events']
 def test_each_actual_death_has_same_person_anchor(self):
  self.assertEqual(len(self.events),15)
  ps={p['id']:p for p in self.c['paragraphs']}
  for e in self.events:
   ev=e['evidence'][0];p=ps[ev['paragraph_id']];self.assertEqual(ev['quote'],p['text']);m=next(m for m in p['mentions']if m['id']==ev['person_mention_id']);self.assertEqual(m['person_id'],e['person_id']);self.assertIn(e['source_term'],p['text'])
 def test_unknown_prince_year_and_collective_cause_remain_unknown(self):
  prince=self.events[1];self.assertEqual(prince['date_expression'],'孝文時');self.assertNotIn('normalized_date_range',prince)
  for e in self.events[9:11]:self.assertEqual(e['source_term'],'太后、太子皆死');self.assertNotIn('自殺',e['source_term'])
 def test_source_ages_never_infer_birth(self):
  a=self.c['annotation']['age_assertions'];self.assertEqual([x['value']for x in a],[20,62,14]);self.assertEqual(a[2]['person_id'],'yqp_nlb_p1p_CAB')
  self.assertTrue(all(x['birth_year']is None and x['counting']=='unspecified_source_age'for x in a));self.assertEqual(a[0]['normalized_date_range']['earliest']['era_year'],197)
 def test_duration_and_chronology_are_not_exact_months(self):
  z=self.events[-1];self.assertEqual(z['date_expression'],'圍趙十月而下之');self.assertNotIn('normalized_date',z)
  for e in self.events:
   if 'normalized_date_range'in e:self.assertEqual(e['normalized_date_range']['precision'],'year_range');self.assertNotIn('month',e['normalized_date_range'])
