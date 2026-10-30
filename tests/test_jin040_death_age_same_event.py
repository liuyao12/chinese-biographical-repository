"""Fixed complete C40 source, reported age and exact039/040 same death."""
from pathlib import Path
import copy
import json
import unittest
ROOT=Path(__file__).resolve().parents[1]
class JiaDeathAgeTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  from scripts import fixed_wuyingdian_jin040_jiachong as m
  cls.m=m;cls.ch=m._c40_chapter(ROOT);cls.st=m.complete_unit_state(cls.ch,ROOT);cls.c39=m._c40_read(ROOT,'corpus/jinshu/039.json');cls.event=m._c40_read(ROOT,m.DEATH_LIFE)['events'][0];cls.group=m._c40_read(ROOT,m.DEATH_GROUP)['groups'][0];cls.prior=next(e for e in m._c40_read(ROOT,'corpus/jinshu/039-life-events.json')['events']if e['id']=='le-jin039-xu30-jia');cls.events={cls.prior['id']:cls.prior,cls.event['id']:cls.event};cls.chapters={m.CID:cls.ch,cls.c39['id']:cls.c39}
 def test_actual_complete_source_death_year_month(self):
  self.assertTrue(self.m.validate_source(self.ch,ROOT));self.assertTrue(self.m.death_group_valid(self.group,self.events,self.chapters,self.st['people'],ROOT));self.assertTrue(self.m.death_month_valid(self.event,self.chapters,ROOT));self.assertEqual(self.event['person_id'],self.st['roles']['chong']);self.assertEqual(self.event['normalized_date']['year'],282);self.assertEqual(self.event['source_date_parts']['month'],4);self.assertIsNone(self.event['source_date_parts']['day'])
 def test_age_is_source_report_and_no_birth(self):
  from scripts.age_context import age_context_valid
  a=next(a for a in self.ch['annotation']['age_assertions']if a['id']=='age-jin040-wyd-jiachong-death66');self.assertEqual(a['value'],66);self.assertEqual(a['counting'],'unspecified_source_age');self.assertIsNone(a['birth_year']);self.assertTrue(age_context_valid(a,self.events));bad=copy.deepcopy(a);bad['person_id']=self.st['roles']['limin'];self.assertFalse(age_context_valid(bad,self.events))
 def test_original039_undated_and_group_representative(self):
  self.assertIsNone(self.prior['date_expression']);self.assertNotIn('normalized_date',self.prior);self.assertEqual(self.group['member_event_ids'],[self.prior['id'],self.event['id']]);self.assertEqual(self.group['representative_event_id'],self.event['id']);self.assertEqual(len(self.group['evidence']),2)
 def test_wrong_person_date_month_and_one_end_rejected(self):
  for field,value in [('year',283),('month',3),('day',1),('person',self.st['roles']['limin'])]:
   es=copy.deepcopy(self.events);e=es[self.event['id']]
   if field=='year':e['normalized_date']['year']=value
   elif field=='person':e['person_id']=value
   else:e['source_date_parts'][field]=value
   self.assertFalse(self.m.death_group_valid(self.group,es,self.chapters,self.st['people'],ROOT),field)
 def test_missing_event_wrong_witness_and_prior_mutation_rejected(self):
  es=copy.deepcopy(self.events);del es[self.prior['id']];self.assertFalse(self.m.death_group_valid(self.group,es,self.chapters,self.st['people'],ROOT));g=copy.deepcopy(self.group);g['evidence'][0]['source_id']='wrong';self.assertFalse(self.m.death_group_valid(g,self.events,self.chapters,self.st['people'],ROOT));es=copy.deepcopy(self.events);es[self.prior['id']]['date_expression']='太康三年';self.assertFalse(self.m.death_group_valid(self.group,es,self.chapters,self.st['people'],ROOT))
if __name__=='__main__':unittest.main()
