# coding: utf-8
import copy,json,unittest
from pathlib import Path
from scripts.validate_corpus import normalized_date_errors
ROOT=Path(__file__).resolve().parents[1]
class RegnalCivilDates(unittest.TestCase):
 def date(self):
  return copy.deepcopy(json.loads((ROOT/'corpus/houhanshu/062-life-events.json').read_text())['events'][0]['normalized_date'])
 def test_xun_shu_year_keeps_quote_and_does_not_invent_a_day_or_birth(self):
  d=self.date();self.assertEqual(normalized_date_errors(d),[]);self.assertEqual(d['year'],149);self.assertIn('建和三年',d['original_quote']);self.assertEqual(d['calendar'],'chinese_civil');self.assertFalse(any(k in d for k in ['month','day','birth_year']))
 def test_wrong_year_or_unattested_era_number_is_rejected(self):
  for key,value in [('year',150),('source_number','四'),('regnal_year',2),('start_ce_year',146),('end_ce_year',148)]:
   d=self.date()
   if key=='year':d['year']=value;d['era_year']=value
   else:d['regnal_year_mapping'][key]=value
   self.assertTrue(normalized_date_errors(d),key)
 def test_reference_bounds_are_distinct_from_received_date(self):
  for change in ['quote','first','last','expression','calendar','scope']:
   d=self.date()
   if change=='quote':d['references'][0]['quote']='別號'
   if change=='first':d['references'][0]['columns']['first_year']='148'
   if change=='last':d['references'][0]['columns']['last_year']='150'
   if change=='expression':d['source_expression']='建和二年'
   if change=='calendar':d['calendar']='gregorian'
   if change=='scope':d['references'][0]['scope']='received_chapter'
   self.assertTrue(normalized_date_errors(d),change)
 def test_malformed_mapping_and_reference_fail_without_crashing(self):
  for change in ['mapping','columns','quote','url','index']:
   d=self.date()
   if change=='mapping':d['regnal_year_mapping']=None
   if change=='columns':d['references'][0]['columns']=None
   if change=='quote':d['original_quote']=None
   if change=='url':d['references'][0]['url']=None
   if change=='index':d['regnal_year_mapping']['reference_index']=99
   self.assertTrue(normalized_date_errors(d),change)
