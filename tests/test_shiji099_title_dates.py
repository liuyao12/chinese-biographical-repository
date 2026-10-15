# coding: utf-8
import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text())
def holdings():return {h['id']:h for h in read('corpus/shiji/099-titles.json')['holdings']}
class LiushuTitleDateTests(unittest.TestCase):
 def test_eight_endpoints_preserve_regnal_year_and_astronomical_ranges(self):
  hs=holdings();spec=[(4,'start',203,202),(5,'start',203,202),(7,'start',201,200),(8,'start',201,200),(19,'start',203,202),(20,'start',201,200),(20,'end',199,198),(21,'start',199,198)]
  for n,side,a,b in spec:
   boundary=hs[f'th-shiji099-{n:03d}']['effective_period'][side];r=boundary['normalized_date_range']
   self.assertEqual((r['earliest']['era_year'],r['latest']['era_year']),(a,b));self.assertEqual((r['earliest']['year'],r['latest']['year']),(1-a,1-b))
   self.assertEqual(r['evidence'],boundary['evidence']);self.assertIn(boundary['date_expression'],r['original_quote']);self.assertEqual(r['precision'],'year_range')
   self.assertTrue(all(e['person_mention_id'] for e in r['evidence']))
 def test_first_and_fourth_paragraphs_support_continuing_appointment_story(self):
  for n in [4,5]:
   b=holdings()[f'th-shiji099-{n:03d}']['effective_period']['start']
   self.assertEqual(b['date_expression'],'漢五年')
   self.assertEqual([e['paragraph_id'] for e in b['evidence']],['c-shiji-099-liushu:p001','c-shiji-099-liushu:p004'])
   self.assertIn('漢五年',b['evidence'][0]['quote']);self.assertNotIn('漢五年',b['evidence'][1]['quote'])
 def test_two_doctor_appointments_do_not_borrow_surrender_year(self):
  for n in [13,17,18]:
   b=holdings()[f'th-shiji099-{n:03d}']['effective_period']['start']
   self.assertIsNone(b['date_expression']);self.assertNotIn('normalized_date',b);self.assertNotIn('normalized_date_range',b)
 def test_transfer_has_relative_start_and_does_not_end_every_title_at_death(self):
  hs=holdings();b=hs['th-shiji099-023']['effective_period']['start']
  self.assertEqual(b['date_expression'],'高帝崩，孝惠即位');self.assertNotIn('normalized_date',b);self.assertNotIn('normalized_date_range',b)
  self.assertEqual(hs['th-shiji099-021']['effective_period']['end']['date_expression'],b['date_expression'])
  self.assertTrue(all(hs[f'th-shiji099-{n:03d}']['effective_period']['end']['status']=='unknown' for n in [4,5,7,8,18,19]))
 def test_longxi_is_service_not_origin_or_a_fabricated_office(self):
  aa=read('corpus/shiji/099-addresses.json')['assertions'];a=next(a for a in aa if a['id']=='pa-shiji099-004')
  self.assertEqual((a['person_id'],a['relation'],a['place']['source_name']),('e5s_bwt_y45','service_location','隴西'));self.assertEqual(a['qualifiers']['source_position'],'戍')
  self.assertEqual(a['date_expression'],'漢五年');self.assertEqual(a['source_term'],'戍隴西');self.assertIsNone(a['place']['modern_identification'])
  self.assertEqual([x['place']['source_name'] for x in aa if x['person_id']==a['person_id'] and x['relation']=='biographical_origin'],['齊'])
 def test_editorial_table_year_column_is_not_treated_as_received_text(self):
  for h in holdings().values():
   for b in h['effective_period'].values():
    if 'normalized_date_range' not in b:continue
    refs=b['normalized_date_range']['references'];digital=[r for r in refs if r.get('scope')=='digital_editorial_regnal_year_equivalence_only']
    self.assertEqual(len(digital),1);self.assertIn('非原文',digital[0]['title']);self.assertFalse(digital[0]['image_verified'])
 def test_export_keeps_title_ranges_out_of_life_dates(self):
  records=[]
  for pid in ['e5s_bwt_y45','dpt_ry7_e1z','yqp_nlb_p1p_A']:
   p=read('exports/persons/'+pid+'.json');records.extend(r for r in p['date_range_normalizations'] if r['record_id'].startswith('th-shiji099-'))
  self.assertEqual(len(records),8);self.assertTrue(all(r['date_role']=='title_period' and r['endpoint'] in ['start','end'] and 'event_type' not in r for r in records))
