import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(f):return json.loads((ROOT/f).read_text())
def events():return read('corpus/shiji/100-life-events.json')['events']
class JibuLuanLifeTests(unittest.TestCase):
 def test_omitted_death_subject_is_luan_bu_not_jing_emperor(self):
  e=next(e for e in events() if e['date_expression']=='景帝中五年');self.assertEqual(e['person_id'],'jx9_cov_qe0')
  ctx=e['evidence'][0]['context'];self.assertEqual(ctx['kind'],'prior_paragraph_subject');p=next(p for p in read('corpus/shiji/100.json')['paragraphs'] if p['id']==ctx['paragraph_id']);m=next(m for m in p['mentions'] if m['id']==ctx['person_mention_id']);self.assertEqual(m['person_id'],e['person_id']);self.assertEqual(ctx['quote'],p['text'])
  self.assertEqual(e['normalized_date_range']['earliest']['year'],-145);self.assertEqual(e['normalized_date_range']['latest']['year'],-144);self.assertNotIn('normalized_date',e)
 def test_threatened_execution_and_display_place_are_not_death_assertions(self):
  self.assertEqual({e['person_id'] for e in events()},{'7ul_aeb_w4e','9qt_orl_5f2','jx9_cov_qe0'})
  for e in events():
   if e['person_id']!='jx9_cov_qe0':self.assertIsNone(e['date_expression']);self.assertNotIn('normalized_date',e);self.assertNotIn('normalized_date_range',e)
  places=read('corpus/shiji/100-addresses.json')['assertions'];self.assertFalse(any(a['person_id']=='9qt_orl_5f2' and a['relation']=='death_place' for a in places))
 def test_death_does_not_end_all_luan_bu_offices(self):
  for h in read('corpus/shiji/100-titles.json')['holdings']:
   if h['person_id']=='jx9_cov_qe0':self.assertEqual(h['effective_period']['end']['status'],'unknown')
  e=next(e for e in events() if e['person_id']=='jx9_cov_qe0');self.assertEqual(e['normalized_date_range']['precision'],'year_range');self.assertTrue(any(r['scope']=='digital_editorial_regnal_year_equivalence_only' for r in e['normalized_date_range']['references']))
