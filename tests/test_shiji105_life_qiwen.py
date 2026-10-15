import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class LifeQiWen(unittest.TestCase):
 def test_actual_deaths_exclude_failed_predictions(self):
  d=json.loads((ROOT/'corpus/shiji/105-life-events.json').read_text());self.assertEqual(len(d['events']),13)
  terms={e['source_term']for e in d['events']};self.assertIn('即後十一日，溲血而死',terms);self.assertIn('後二十餘日，溲血死',terms)
  self.assertFalse(any(e['person_id']=='9pv_or9_2r6'for e in d['events']))
  self.assertFalse(any('p038' in e['evidence'][0]['paragraph_id']for e in d['events']))
 def test_qiwen_identity_and_parallel_range_keep_source_date_unknown(self):
  d=json.loads((ROOT/'corpus/shiji/105-life-events.json').read_text());e=d['events'][-1];self.assertEqual(e['person_id'],'ycr_d4w_b0x');self.assertIsNone(e['date_expression']);self.assertIn('轉聞',e['interpretation_note'])
  w=e['normalized_date_range'];self.assertEqual((w['earliest']['year'],w['latest']['year']),(-165,-164));self.assertEqual(w['parallel_event']['source_event_quote'],'以故死');self.assertEqual(w['parallel_event']['reference_year_quote'],'165')
  self.assertNotIn('normalized_date',e)
 def test_fengxin_existing_span_is_preserved_and_reference_is_separate(self):
  c=json.loads((ROOT/'corpus/shiji/105.json').read_text());p=next(p for p in c['paragraphs']if p['id'].endswith('p047'));m=next(m for m in p['mentions']if m['id']=='c-shiji-105-bianque:m047-0120');self.assertEqual(m['surface'],'馮信');self.assertEqual(m['end']-m['start'],2)
  d=json.loads((ROOT/'corpus/shiji/105-identities.json').read_text());r=next(r for r in d['decisions']if r.get('person_id')=='qot_kkm_wa4');self.assertTrue(any(ref.get('year')==2023 for ref in r['references']))
