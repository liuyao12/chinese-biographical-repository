"""First bounded source-facts layer, without inferring births or tenures."""
import copy,json,unittest
from pathlib import Path
from scripts import fixed_wuyingdian_jin043_shantao as g
from scripts.person_bundle import load_catalog,bundle
ROOT=Path(__file__).resolve().parents[1]
class ShanBasicFactsTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.people,cls.records=load_catalog(ROOT);cls.ch=next(r for r in cls.records if r.get('id')==g.CID);cls.roles,cls.ct=g.formal_state(cls.ch,ROOT,cls.people,cls.records)
 def test_exact_ages_do_not_supply_birth(self):
  rows=self.ch['annotation']['age_assertions'];self.assertEqual([a['value']for a in rows],[40,79,60]);self.assertTrue(all(a['birth_year']is None for a in rows));self.assertEqual([a['person_id']for a in rows],[self.roles['shantao'],self.roles['shantao'],self.roles['shanjian']])
 def test_wrong_age_owner_or_birth_rejected(self):
  for key,value in [('value',78),('birth_year',205),('person_id',self.roles['shanjian'])]:
   x=copy.deepcopy(self.ch);x['annotation']['age_assertions'][1][key]=value
   with self.assertRaises(ValueError):g.formal_state(x,ROOT,self.people,self.records)
 def test_wrong_fact_owner_or_borrowed_year_rejected(self):
  rows=copy.deepcopy(self.records);record=next(r for r in rows if r.get('record_type')=='title_holding_assertion_set'and r.get('chapter_id')==g.CID);record['holdings'][0]['person_id']=self.roles['shanjian']
  with self.assertRaises(ValueError):g.formal_state(self.ch,ROOT,self.people,rows)
  rows=copy.deepcopy(self.records);record=next(r for r in rows if r.get('record_type')=='person_life_event_assertion_set'and r.get('chapter_id')==g.CID);record['events'][1]['date_expression']='永嘉三年'
  with self.assertRaises(ValueError):g.formal_state(self.ch,ROOT,self.people,rows)
 def test_actual_bundle_death_origin_and_posthumous(self):
  b=bundle(self.roles['shantao'],ROOT,include_provisional=True,catalog=(self.people,self.records));self.assertTrue(any(x['place']['source_name']=='河內懷'for x in b['address_assertions']));e=next(x for x in b['life_events']if x['id']=='le-jin043-wyd-shantao-death');self.assertEqual(e['normalized_date']['year'],283)
  self.assertTrue(any(x['title']=='康'and x['mode']=='posthumous_naming'for x in b['title_holdings']))
if __name__=='__main__':unittest.main()
