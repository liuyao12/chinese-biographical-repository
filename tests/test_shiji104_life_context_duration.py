import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class LifeContextDuration(unittest.TestCase):
 def test_six_deaths_keep_parallel_years_and_source_layers(self):
  d=json.loads((ROOT/'corpus/shiji/104-life-events.json').read_text());self.assertEqual(len(d['events']),6)
  ren=[e for e in d['events']if e['person_id']=='6bn_yfc_lzi_A'];self.assertEqual(len(ren),2)
  self.assertEqual({e['evidence'][0]['paragraph_id']for e in ren},{'c-shiji-104-tianshu:p008','c-shiji-104-tianshu:p015'})
  for e in d['events']:
   if e['person_id']in ['6bn_yfc_lzi_A','y9g_gi6_sn7']:
    self.assertEqual(e['normalized_date']['year'],-90);self.assertEqual(e['normalized_date']['era_year'],91)
    self.assertEqual(e['normalized_date']['basis']['kind'],'parallel_event');self.assertIsNone(e['date_expression'])
   if e['person_id']=='6bn_yfc_lzi':self.assertNotIn('normalized_date',e)
 def test_duration_bounds_do_not_invent_values_or_endpoints(self):
  d=json.loads((ROOT/'corpus/shiji/104-titles.json').read_text())
  for hid,lower,unit in [('th-shiji104-005',10,'title_year'),('th-shiji104-013',1,'title_month')]:
   h=next(h for h in d['holdings']if h['id']==hid);r=h['reported_duration'];self.assertIsNone(r['value']);self.assertEqual(r['unit'],unit)
   self.assertEqual(r['bounds'],{'lower':lower,'lower_inclusive':False,'upper':None,'upper_inclusive':None})
 def test_contextual_mentions_and_non_person_exclusions(self):
  d=json.loads((ROOT/'corpus/shiji/104-identities.json').read_text());rows=[r for r in d['decisions']if r['id'].startswith('d-shiji104-context-')]
  self.assertEqual(sum(len(e['mention_ids'])for r in rows for e in r['evidence']),6)
  c=json.loads((ROOT/'corpus/shiji/104.json').read_text());p=next(p for p in c['paragraphs']if p['id'].endswith('p012'))
  self.assertEqual(next(m['person_id']for m in p['mentions']if m['start']==91),'vkr_lkp_dme')
  self.assertFalse(any(m['start']==312 for m in p['mentions']))
