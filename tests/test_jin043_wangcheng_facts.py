import unittest,json,copy
from pathlib import Path
try:from scripts.fixed_witness_fact_slots import records,valid,errors
except ImportError:from fixed_witness_fact_slots import records,valid,errors
ROOT=Path(__file__).resolve().parents[1]
class LimitedWangChengFacts(unittest.TestCase):
 def setUp(self):
  self.ch=json.loads((ROOT/'corpus/jinshu/043-wangcheng.json').read_text());self.rs=records(self.ch,ROOT);self.by={r['id']:r for r in self.rs}
 def test_nine_source_slots_only(self):
  self.assertEqual(len(self.rs),9);self.assertTrue(all(valid(r,self.ch,ROOT)for r in self.rs));self.assertTrue(all('normalized_date'not in r for r in self.rs));self.assertEqual([r['qualifiers']['birth_order']['ordinal']for r in self.rs if r.get('predicate')=='father'],[1,2])
 def test_father_direction_and_son_order_not_interchangeable(self):
  r=copy.deepcopy(self.by['a-jin043-wangcheng-zhan-father']);r['subject_person_id'],r['object_person_id']=r['object_person_id'],r['subject_person_id'];self.assertFalse(valid(r,self.ch,ROOT));r=copy.deepcopy(self.by['a-jin043-wangcheng-hui-father']);r['qualifiers']['birth_order']['ordinal']=1;self.assertFalse(valid(r,self.ch,ROOT));r=copy.deepcopy(self.by['a-jin043-wangcheng-zhan-father']);r['predicate']='mother';self.assertFalse(valid(r,self.ch,ROOT))
 def test_age_44_is_same_person_at_death_not_birth_or_calendar(self):
  r=self.by['age-jin043-wangcheng-fortyfour'];self.assertEqual(r['age_context'],{'kind':'at_death','life_event_id':'le-jin043-wangcheng-cheng'});self.assertIsNone(r['birth_year'])
  for key,value in [('value',14),('birth_year',269),('age_context',{'kind':'at_death','life_event_id':'le-jin043-wangcheng-zhan'}),('normalized_date',{'year':312})]:
   x=copy.deepcopy(r);x[key]=value;self.assertFalse(valid(x,self.ch,ROOT))
 def test_names_do_not_invent_surnames_or_courtesy_for_sons(self):
  for r in self.rs:
   if r['id'].startswith('nc-'):
    self.assertIsNone(r['surname']);x=copy.deepcopy(r);x['surname']='王';self.assertFalse(valid(x,self.ch,ROOT))
  r=self.by['nc-jin043-wangcheng-cheng'];self.assertEqual(r['zi'],'平子');x=copy.deepcopy(r);x['zi']='大業';self.assertFalse(valid(x,self.ch,ROOT))
 def test_death_subject_and_early_death_not_chronology(self):
  r=self.by['le-jin043-wangcheng-zhan'];self.assertEqual(r['source_term'],'長子詹，早卒');self.assertIsNone(r['date_expression']);x=copy.deepcopy(r);x['person_id']=self.by['le-jin043-wangcheng-cheng']['person_id'];self.assertFalse(valid(x,self.ch,ROOT));x=copy.deepcopy(r);x['before_father_death']=True;self.assertFalse(valid(x,self.ch,ROOT))
 def test_source_role_changes_cannot_shift_all_facts(self):
  c=copy.deepcopy(self.ch);ms=[m for m in c['paragraphs'][6]['mentions']if m['kind']=='person'];a=next(m for m in ms if m['surface']=='詹');b=next(m for m in ms if m['surface']=='徽');a['person_id'],b['person_id']=b['person_id'],a['person_id'];self.assertFalse(valid(self.by['a-jin043-wangcheng-zhan-father'],c,ROOT))
