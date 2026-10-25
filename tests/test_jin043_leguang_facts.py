# coding:utf-8
from pathlib import Path
import unittest,json,copy
R=Path(__file__).resolve().parents[1]
class LeguangFactsTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  from scripts.fixed_witness_fact_slots import records
  cls.ch=json.loads((R/'corpus/jinshu/043-leguang.json').read_bytes());cls.rs=records(cls.ch,R);cls.v={v['fixed_source_fact_binding']['slot']:v for v in cls.rs};cls.ids={r['key']:r['person_id']for r in json.loads((R/'source-evidence/jin043-leguang-source/identity-records.json').read_bytes())}
 def reject(self,value):
  from scripts.fixed_witness_fact_slots import valid
  self.assertFalse(valid(value,self.ch,R))
 def test_parentage_and_marriage_are_machine_readable_in_source_direction(self):
  for child,parent in [('guang','fang'),('kai','guang'),('zhao','guang'),('mo','guang'),('daughter','guang'),('yangqiao','yangzhun'),('yangmao','yangzhun')]:
   v=self.v[child+'-father'];self.assertEqual((v['predicate'],v['subject_person_id'],v['object_person_id']),('father',self.ids[child],self.ids[parent]));self.assertNotIn('birth_order',v['qualifiers']);bad=copy.deepcopy(v);bad['subject_person_id'],bad['object_person_id']=bad['object_person_id'],bad['subject_person_id'];self.reject(bad)
  v=self.v['daughter-spouse'];self.assertEqual((v['predicate'],v['subject_person_id'],v['object_person_id']),('spouse',self.ids['daughter'],self.ids['simaying']));self.assertFalse(any(v.get('predicate')=='mother'for v in self.rs))
 def test_five_sons_and_three_named_sons_neither_fill_gaps_nor_create_ordinals(self):
  a=self.v['five-sons']['values'];b=self.v['named-three-sons']['values'];self.assertEqual(a['sons_count'],5);self.assertIsNone(a['all_daughters_count']);self.assertEqual(b['listed_sons_count'],3);self.assertEqual(set(b['listed_person_ids']),{self.ids[k]for k in ['kai','zhao','mo']});self.assertIsNone(b['all_sons_count']);self.assertFalse(b['absolute_sibling_order_asserted'])
  bad=copy.deepcopy(self.v['kai-father']);bad['qualifiers']['birth_order']={'ordinal':1};self.reject(bad)
 def test_reported_eight_and_undated_deaths_do_not_invent_birth_or_304(self):
  age=self.v['age-eight'];self.assertEqual((age['source_number'],age['source_term'],age['value']),('八','八歲',8));self.assertIsNone(age['birth_year']);self.assertEqual(age['counting'],'unspecified_source_age');self.assertIn('廣時年八歲',age['evidence'][0]['quote'])
  for slot in ['guang-death','fang-death']:
   v=self.v[slot];self.assertIsNone(v['date_expression']);self.assertNotIn('normalized_date',v);bad=copy.deepcopy(v);bad['normalized_date']={'year':304};self.reject(bad)
  bad=copy.deepcopy(age);bad['birth_year']=252;self.reject(bad)
 def test_office_report_does_not_expand_title_or_complete_resignation(self):
  self.assertIsNone(self.v['fang-staff']['values']['formal_office_title']);self.assertIsNone(self.v['kai-staff']['values']['leader_person_id']);self.assertFalse(self.v['resignation-intent']['values']['departure_completed']);self.assertIsNone(self.v['unpunctuated-career']['values']['concurrency']);self.assertIsNone(self.v['unpunctuated-career']['values']['relative_order']);self.assertEqual(self.v['career-11']['title'],'吏部');self.assertEqual(self.v['career-11']['appointment_role'],'concurrent')
  bad=copy.deepcopy(self.v['resignation-intent']);bad['values']['departure_completed']=True;self.reject(bad)
  for slot,title in [('you-rank','東安王'),('ying-rank','成都王'),('yi-rank','長沙王'),('jiong-rank','齊王'),('yue-rank','東海王'),('minhuai-designation','湣懷太子')]:
   v=self.v[slot];self.assertEqual(v['title'],title);self.assertEqual(v['mode'],'attestation');self.assertEqual(v['effective_period']['start']['status'],'unknown');self.assertEqual(v['effective_period']['end']['status'],'unknown')
  titles=[v['title']for v in self.rs if'title'in v];self.assertNotIn('參魏征西將軍軍事',titles);self.assertNotIn('吏部尚書左僕射',titles)
 def test_names_keep_received_characters_and_surname_inference_separate(self):
  self.assertEqual(self.v['name-panyue']['ming'],'嶽');self.assertEqual(self.v['name-yangqiao']['ming'],'喬');self.assertEqual(self.v['name-yangzhun']['ming'],'准');self.assertEqual(self.v['name-xunfan']['ming'],'籓')
  for key,surname in [('fang','樂'),('kai','樂'),('zhao','樂'),('mo','樂'),('yangqiao','楊'),('yangmao','楊')]:
   v=self.v['name-'+key];self.assertEqual(v['surname'],surname);self.assertEqual(v['status'],'contextual_provisional');self.assertEqual(v['surname_basis']['kind'],'contextual_surname_from_fixed_biography_family')
if __name__=='__main__':unittest.main()
