# coding: utf-8
"""Real source roles, not name-based validation exceptions."""
import copy,json,unittest
from pathlib import Path
from scripts.literal_family_reports import kinship_valid,count_valid,death_valid
from scripts.validate_corpus import source_age_number
ROOT=Path(__file__).resolve().parents[1]
class LuSourceFamily(unittest.TestCase):
 def setUp(self):
  self.ch=json.loads((ROOT/'corpus/sanguozhi/022-luyu.json').read_text());self.cs={self.ch['id']:self.ch};self.ps={p['id']:(self.ch['id'],p)for p in self.ch['paragraphs']}
  self.kin=json.loads((ROOT/'corpus/sanguozhi/022-luyu-assertions.json').read_text())['assertions'];self.deaths=json.loads((ROOT/'corpus/sanguozhi/022-luyu-life-events.json').read_text())['events'];self.count=self.ch['annotation']['family_count_reports'][0]
 def k(self,a):return kinship_valid(a,self.ps,self.cs,ROOT)
 def d(self,a):return death_valid(a,self.ps,self.cs,ROOT)
 def c(self,a):return count_valid(a,self.ps,self.cs,ROOT,source_age_number)
 def test_all_actual_source_roles(self):
  self.assertEqual(len(self.kin),10);self.assertTrue(all(self.k(a)for a in self.kin));self.assertTrue(all(self.d(a)for a in self.deaths));self.assertTrue(self.c(self.count))
 def test_wrong_parent_endpoint_even_with_evidence_rewritten(self):
  a=copy.deepcopy(self.kin[0]);a['object_person_id']=a['subject_person_id'];a['evidence'][0]['object_person_mention_id']=a['evidence'][0]['subject_person_mention_id'];self.assertFalse(self.k(a))
 def test_reverse_parent_child(self):
  a=copy.deepcopy(self.kin[0]);a['subject_person_id'],a['object_person_id']=a['object_person_id'],a['subject_person_id'];e=a['evidence'][0];e['subject_person_mention_id'],e['object_person_mention_id']=e['object_person_mention_id'],e['subject_person_mention_id'];self.assertFalse(self.k(a))
 def test_youngest_is_not_fourth(self):
  a=copy.deepcopy(next(a for a in self.kin if 'birth_order'in a['qualifiers']));a['qualifiers']['birth_order']['ordinal']=4;self.assertFalse(self.k(a))
 def test_list_order_addition_rejected(self):
  a=copy.deepcopy(next(a for a in self.kin if a['qualifiers']['literal_source_binding']['rule']=='named_sons'));a['qualifiers']['birth_order']={'ordinal':1};self.assertFalse(self.k(a))
 def test_missing_generations_remain_unknown(self):
  for a in self.kin:
   if 'intermediate_person_ids'in a['qualifiers']:
    self.assertTrue(all(x is None for x in a['qualifiers']['intermediate_person_ids']));b=copy.deepcopy(a);b['qualifiers']['intermediate_person_ids'][0]=a['object_person_id'];self.assertFalse(self.k(b));b=copy.deepcopy(a);b['qualifiers']['parent_person_id']=a['object_person_id'];self.assertFalse(self.k(b))
 def test_report_count_not_complete_named_list(self):
  for field,value in [('reported_count',3),('reported_count','4'),('complete_named_list',True),('source_number','三'),('named_member_person_ids',[])]:
   a=copy.deepcopy(self.count);a[field]=value;self.assertFalse(self.c(a),(field,value))
 def test_layer_cannot_be_relabelled_consistently_without_projection(self):
  a=copy.deepcopy(self.count);pid=a['evidence'][0]['paragraph_id'];p=self.ps[pid][1];p['text_layer']='received_chapter';p['source_position']['source_layer']='received_body';a['literal_source_binding']['source_layer']='received_chapter';self.assertFalse(self.c(a))
 def test_attached_note_cannot_be_main_source(self):
  a=copy.deepcopy(self.kin[0]);self.ps[a['evidence'][0]['paragraph_id']][1]['attached_note_to_paragraph_id']='other';self.assertFalse(self.k(a))
 def test_candidate_official_cannot_be_death_subject(self):
  a=copy.deepcopy(next(a for a in self.deaths if 'candidate_1'in a['literal_source_binding']['roles']));r=a['literal_source_binding']['roles'];r['subject']=r['candidate_3'];p=self.ps[a['evidence'][0]['paragraph_id']][1];m=next(m for m in p['mentions']if m['id']==r['subject']);a['person_id']=m['person_id'];a['evidence'][0]['person_mention_id']=m['id'];self.assertFalse(self.d(a))
 def test_patron_cannot_be_death_subject(self):
  a=copy.deepcopy(next(a for a in self.deaths if 'patron'in a['literal_source_binding']['roles']));r=a['literal_source_binding']['roles'];r['subject']=r['patron'];p=self.ps[a['evidence'][0]['paragraph_id']][1];m=next(m for m in p['mentions']if m['id']==r['subject']);a['person_id']=m['person_id'];a['evidence'][0]['person_mention_id']=m['id'];self.assertFalse(self.d(a))
 def test_calendar_and_orphan_age_not_birth_or_own_death(self):
  self.assertEqual(sorted(a['normalized_date']['year'] for a in self.deaths),[192,257,278,350]);a=self.ch['annotation']['age_assertions'][0];self.assertEqual(a['value'],10);self.assertIsNone(a['birth_year']);self.assertEqual(a['age_context'],{'kind':'during_life'});self.assertEqual(a['counting'],'unspecified_source_age')
if __name__=='__main__':unittest.main()
