"""Finite Cao Ren/Cao Chun clauses: source roles, not fixed person identifiers."""
from pathlib import Path
import copy,json,unittest
from scripts.fixed_kanripo_fact_slots import records,valid
from scripts.fixed_kanripo_slot_dates import valid as date_valid
from scripts.age_context import age_context_valid
ROOT=Path(__file__).resolve().parents[1]
class CaorenChunTyped(unittest.TestCase):
 def setUp(self):
  self.ch=json.loads((ROOT/'corpus/sanguozhi/009-caoren-caochun.json').read_text());self.rows=records(self.ch,ROOT);self.by={r['id']:r for r in self.rows}
 def test_source_roles_and_wrong_parent(self):
  a=next(r for r in self.rows if r.get('predicate')=='father');bad=copy.deepcopy(a);bad['subject_person_id'],bad['object_person_id']=bad['object_person_id'],bad['subject_person_id'];self.assertFalse(valid(bad,self.ch,ROOT));self.assertTrue(valid(a,self.ch,ROOT))
 def test_acting_not_permanent_grant(self):
  a=next(r for r in self.rows if r.get('source_career_role',{}).get('role_category')=='acting_appointment');self.assertEqual(a['mode'],'attestation');bad=copy.deepcopy(a);bad['mode']='grant';self.assertFalse(valid(bad,self.ch,ROOT));self.assertIsNone(a['effective_period']['end']['date_expression'])
 def test_two_direct_deaths_and_wrong_year(self):
  for r in self.rows:
   if r.get('normalized_date',{}).get('regnal_year_mapping',{}).get('kind')=='fixed_kanripo_direct_slot_regnal_year':
    self.assertTrue(date_valid(r['normalized_date'],r,self.ch,ROOT));bad=copy.deepcopy(r);bad['normalized_date']['year']+=1;self.assertFalse(date_valid(bad['normalized_date'],bad,self.ch,ROOT))
 def test_death_age_is_not_birth(self):
  ages=[r for r in self.rows if r.get('unit')=='source_age_years'];deaths={r['id']:r for r in self.rows if r.get('event_type')=='death'}
  for a in ages:self.assertIsNone(a['birth_year']);self.assertTrue(age_context_valid(a,deaths))
  a=next(a for a in ages if a.get('age_context',{}).get('kind')=='at_death');bad=copy.deepcopy(a);bad['person_id']='not_the_decedent';self.assertFalse(age_context_valid(bad,deaths))
 def test_unrelated_collective_not_children_of_captor(self):
  a=next(r for r in self.rows if r.get('kind')=='known_collective_event');self.assertIsNone(a['values']['individual_person_ids']);self.assertNotEqual(a['person_id'],a['values']['captor_person_id']);bad=copy.deepcopy(a);bad['values']['individual_person_ids']=['invented'];self.assertFalse(valid(bad,self.ch,ROOT))
if __name__=='__main__':unittest.main()
