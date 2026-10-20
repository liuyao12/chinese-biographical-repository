# coding:utf-8
"""完整固定單元的任官、報齡、追復及連續年段反例；無私有檔案依賴。"""
import unittest,json,copy,hashlib
from pathlib import Path
from scripts.validate_corpus import direct_source_age_valid,source_age_number
from scripts.unassumed_appointments import unassumed_appointment_valid
from scripts.jin_facts_boundaries import posthumous_restoration_valid,continuous_annal_valid,continuous_annal_binding_valid
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads((R/p).read_text())
class CompleteFactsTests(unittest.TestCase):
 def setUp(self):
  self.c=read('corpus/jinshu/077-yinhao.json');self.a=read('corpus/jinshu/008-yonghe5.json');self.age=next(x for x in self.c['annotation']['age_assertions']if x['id']=='age-jin077-f51-001');self.ps=[x for x in self.c['annotation']['title_proposals']if x['id']in ['tp-jin077-f51-002','tp-jin077-f51-003']];self.deaths=read('corpus/jinshu/077-yinhao-life-events.json')['events'];self.events={x['id']:x for x in self.deaths};self.restore=next(x for x in read('corpus/jinshu/077-yinhao-events.json')['events']if x['id']=='pe-jin077-f51-001');self.date=next(x for x in read('corpus/jinshu/008-yonghe5-titles.json')['holdings']if x['person_id']=='9w8_tqh_ysn_B*AA*A')['attestations'][0]['normalized_date']
 def test_living_seventy(self):
  self.assertTrue(direct_source_age_valid(self.age));self.assertEqual(self.age['age_context'],{'kind':'during_life'});self.assertIsNone(self.age['birth_year'])
 def test_age_number_unchanged(self):
  self.assertIsNone(source_age_number('元'));x=copy.deepcopy(self.age);x['value']=69;self.assertFalse(direct_source_age_valid(x));x.update(source_number='元',value=1,source_term='年登元');self.assertFalse(direct_source_age_valid(x))
 def test_both_unassumed(self):
  self.assertEqual({x['title']for x in self.ps},{'侍中','安西軍司'});self.assertTrue(all(unassumed_appointment_valid(x,self.c)for x in self.ps))
 def test_wrong_refusal_recipient(self):
  x=copy.deepcopy(self.ps[0]);x['person_id']='ali_hbb_4bn';self.assertFalse(unassumed_appointment_valid(x,self.c))
 def test_wrong_role_and_offset(self):
  for key,value in [('surface','尚書令'),('start',0)]:
   x=copy.deepcopy(self.ps[0]);x['role_anchor'][key]=value;self.assertFalse(unassumed_appointment_valid(x,self.c))
 def test_wrong_appointment(self):
  x=copy.deepcopy(self.ps[0]);x['appointment_anchor']['surface']='請為';self.assertFalse(unassumed_appointment_valid(x,self.c))
 def test_quote_switch_rejected(self):
  c=copy.deepcopy(self.c);x=copy.deepcopy(self.ps[0]);p=next(p for p in c['paragraphs']if p['id']==x['role_anchor']['paragraph_id']);p['mentions'].append({'id':'test-switch','kind':'person','person_id':'ali_hbb_4bn','surface':'侍','start':x['role_anchor']['start'],'end':x['role_anchor']['start']+1});self.assertFalse(unassumed_appointment_valid(x,c))
 def test_resumed_invitation_refusal(self):
  x=next(x for x in self.c['annotation']['title_proposals']if x['id']=='tp-jin077-f51-004');self.assertTrue(unassumed_appointment_valid(x,self.c));bad=copy.deepcopy(x);bad['appointment_stage']='appointment';self.assertFalse(unassumed_appointment_valid(bad,self.c))
 def test_wrong_resumed_decliner(self):
  x=next(x for x in self.c['annotation']['title_proposals']if x['id']=='tp-jin077-f51-004');c=copy.deepcopy(self.c);p=next(p for p in c['paragraphs']if p['id']==x['role_anchor']['paragraph_id']);m=next(m for m in p['mentions']if m['end']==x['non_assumption_anchor']['start']);m['person_id']='ali_hbb_4bn';self.assertFalse(unassumed_appointment_valid(x,c))
 def test_restoration_one_death(self):
  self.assertTrue(posthumous_restoration_valid(self.restore,{self.c['id']:self.c},self.events));self.assertIsNone(self.restore['office_title']);self.assertIsNone(self.restore['title_holding_id'])
 def test_restoration_not_petition(self):
  x=copy.deepcopy(self.restore);x['source_term']='崇復本官';self.assertFalse(posthumous_restoration_valid(x,{self.c['id']:self.c},self.events))
 def test_wrong_death_person(self):
  es=copy.deepcopy(self.events);es[self.restore['death_event_id']]['person_id']='ali_hbb_4bn';self.assertFalse(posthumous_restoration_valid(self.restore,{self.c['id']:self.c},es));self.assertFalse(posthumous_restoration_valid(self.restore,{self.c['id']:self.c},{}))
 def test_no_restoration_year_invented(self):
  x=copy.deepcopy(self.restore);x['date_expression']='永和十二年';self.assertFalse(posthumous_restoration_valid(x,{self.c['id']:self.c},self.events))
 def test_annal_complete_year(self):
  self.assertTrue(continuous_annal_valid(self.date,source_age_number));self.assertTrue(continuous_annal_binding_valid(self.date,self.a));self.assertEqual(self.date['year'],349)
 def test_wrong_annal_year(self):
  x=copy.deepcopy(self.date);x['year']=350;self.assertFalse(continuous_annal_valid(x,source_age_number))
 def test_skipped_raw_line_even_rehashed(self):
  x=copy.deepcopy(self.date);s=x['references'][1]['section'];ls=s['raw_quote'].splitlines();ls.pop(4);s['raw_quote']='\n'.join(ls);s['raw_quote_sha256']=hashlib.sha256(s['raw_quote'].encode()).hexdigest();self.assertFalse(continuous_annal_valid(x,source_age_number))
 def test_changed_era_or_revision(self):
  x=copy.deepcopy(self.date);x['regnal_year_mapping']['era_name']='建元';self.assertFalse(continuous_annal_valid(x,source_age_number));x=copy.deepcopy(self.date);x['references'][1]['source_revision']='another';self.assertFalse(continuous_annal_binding_valid(x,self.a))
 def test_subject_and_paragraph_binding(self):
  x=copy.deepcopy(self.date);x['annal_year_reference']['event_paragraph_id']='other';self.assertFalse(continuous_annal_valid(x,source_age_number));self.assertFalse(continuous_annal_binding_valid(x,self.a))
 def test_attestation_not_appointment_start(self):
  h=next(h for h in read('corpus/jinshu/008-yonghe5-titles.json')['holdings']if h['person_id']=='9w8_tqh_ysn_B*AA*A');self.assertEqual(h['mode'],'attestation');self.assertEqual(h['effective_period']['start']['status'],'unknown');self.assertNotIn('normalized_date',h['effective_period']['start'])
 def test_death_boundaries(self):
  self.assertFalse(any(x['person_id']=='u61_ylg_6av'for x in self.deaths));self.assertFalse(any(x['person_id']=='dkn_ge4_286_AAAAAAAD'for x in self.deaths));x=next(x for x in self.deaths if x['person_id']=='djo_u3b_i9w');self.assertIsNone(x['date_expression']);self.assertNotIn('normalized_date',x)
 def test_all_original_ledgers_retained(self):
  d=read('source-evidence/jin008077/facts51-consumption-ledger.json');self.assertEqual(len(d['records']),145);self.assertEqual(len({x['proposal']['id']for x in d['records']}),145);self.assertTrue(all(x['remaining_typed_qualification']for x in d['records']))
 def test_unknown_relatives_not_invented(self):
  d=read('source-evidence/jin008077/facts51-kinship-boundaries.json');self.assertIsNone(d[0]['unnamed_father']);self.assertIsNone(d[1]['unnamed_brother']);self.assertEqual(d[1]['relationship'],'same_mother_younger_brother')
if __name__=='__main__':unittest.main()
