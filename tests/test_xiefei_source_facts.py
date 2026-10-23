import copy,json,unittest
from pathlib import Path
from scripts.biography_source_details import valid,holding_valid
from scripts.biography_offered_offices import errors as offer_errors
from scripts.continued_biography_family import valid as family_valid,children_errors
from scripts.fixed_primary_biography_dates import valid as date_valid
from scripts.lifecycle_offered_biography import end_valid,gift_valid
from scripts.current_office_death import current_office_death_valid
from scripts.person_bundle import load_catalog,bundle
R=Path(__file__).resolve().parents[1]
L=lambda n:json.loads((R/'corpus/liangshu'/n).read_text())
C=L('015-xiefei.json');CH={C['id']:C};PS={p['id']:(C['id'],p)for p in C['paragraphs']};MS={m['id']:(C['id'],p['id'],m)for p in C['paragraphs']for m in p['mentions']};HS={h['id']:h for h in L('015-xiefei-titles.json')['holdings']};QS={q['id']:q for q in C['annotation']['title_proposals']};DS=L('015-xiefei-details.json')['records'];AS=L('015-xiefei-assertions.json')['assertions'];PIDS={m[2]['person_id']for m in MS.values()if m[2].get('person_id')}
D=lambda kind:copy.deepcopy(next(d for d in DS if d['kind']==kind))
class XieFeiFactsTests(unittest.TestCase):
 def test_all_details_anchored(self):
  for d in DS:self.assertTrue(valid(d,C,HS,QS),d['id'])
 def test_salary_grade_is_not_payment(self):
  for key in ('actual_payment_value','annual_payment_value'):
   d=D('office_emolument');d['values'][key]=2000;self.assertFalse(valid(d,C,HS,QS))
 def test_unknown_gift_count_not_one(self):
  d=D('gift');d['values']['items'][0]['value']=1;self.assertFalse(valid(d,C,HS,QS))
 def test_funeral_money_has_no_invented_unit(self):
  d=copy.deepcopy(next(d for d in DS if d['id'].endswith('funeral-gifts')));d['values']['items'][3]['unit_source_name']='文';self.assertFalse(valid(d,C,HS,QS))
 def test_gift_wrong_recipient(self):
  d=D('gift');d['values']['recipient_person_id']=d['person_id'];self.assertFalse(valid(d,C,HS,QS))
 def test_unrecognized_claim_fields_rejected(self):
  d=D('official_duty');d['birth_year']=441;self.assertFalse(valid(d,C,HS,QS));d=D('official_duty');d['kind']='invented';self.assertFalse(valid(d,C,HS,QS))
 def test_visit_not_origin(self):
  d=D('recorded_presence');d['values']['origin_or_residence']='origin';self.assertFalse(valid(d,C,HS,QS))
 def test_detail_wrong_anchor_or_subject(self):
  d=D('official_duty');d['source_anchor']['start']+=1;self.assertFalse(valid(d,C,HS,QS));d=D('official_duty');d['person_id']='wrong';self.assertFalse(valid(d,C,HS,QS))
 def test_duty_does_not_create_office(self):
  d=D('official_duty');d['values']['linked_holding_id']=next(h['id']for h in HS.values()if h['title']=='中書郎');self.assertFalse(valid(d,C,HS,QS))
 def test_unassumed_and_unreported_all_valid(self):
  for q in QS.values():self.assertEqual([],offer_errors(q,C,PIDS),q['id'])
 def test_unreported_cannot_be_refusal_or_holding(self):
  q=copy.deepcopy(next(q for q in QS.values()if q['proposal_kind']=='appointment_service_unreported'));q['proposal_kind']='unassumed_appointment';q['outcome']='not_assumed';self.assertTrue(offer_errors(q,C,PIDS));self.assertFalse(any(h['title']=='都官尚書'for h in HS.values()))
 def test_collective_offer_recipient_bound(self):
  q=copy.deepcopy(next(q for q in QS.values()if '-yongyuan2-yin-'in q['id']and q['title']=='散騎常侍'));q['role_anchor']=copy.deepcopy(next(x['role_anchor']for x in QS.values()if '-yongyuan2-fei-'in x['id']and x['title']=='散騎常侍'));self.assertTrue(offer_errors(q,C,PIDS))
 def test_refusal_cannot_be_removed(self):
  q=copy.deepcopy(next(q for q in QS.values()if q['proposal_kind']=='unassumed_appointment'));q.pop('non_assumption_anchor');self.assertTrue(offer_errors(q,C,PIDS))
 def test_family_source_roles_and_uncertain_mother(self):
  for a in AS[:4]:self.assertTrue(family_valid(a,PS),a['id'])
  a=copy.deepcopy(AS[3]);a['qualifiers']['biological_mother']=True;self.assertFalse(family_valid(a,PS))
 def test_second_son_without_invented_first_or_mother(self):
  for a in AS[-2:]:self.assertEqual([],children_errors(a,C))
  a=copy.deepcopy(AS[-2]);a['qualifiers']['birth_order']={'ordinal':1};self.assertTrue(children_errors(a,C));a=copy.deepcopy(AS[-1]);a['qualifiers']['birth_order']['ordinal']=1;self.assertTrue(children_errors(a,C))
 def test_local_end_only_actual_office(self):
  for h in HS.values():
   if h.get('end_basis',{}).get('kind')in('named_last_office_mourning_leave','named_son_office_removed_for_slaughtering_cattle'):self.assertTrue(end_valid(h,PS,MS),h['id'])
  h=copy.deepcopy(next(h for h in HS.values()if h['id'].endswith('sheren-before-mourning')));h['title']='中書郎';self.assertFalse(end_valid(h,PS,MS))
 def test_comma_death_does_not_end_other_offices(self):
  h=copy.deepcopy(next(h for h in HS.values()if h['id'].endswith('zhuan-taishou')));self.assertTrue(current_office_death_valid(h,PS,MS));h['title']='司徒右長史';self.assertFalse(current_office_death_valid(h,PS,MS))
 def test_posthumous_gift_not_to_mourning_emperor(self):
  h=copy.deepcopy(next(h for h in HS.values()if h.get('posthumous_basis')));self.assertTrue(gift_valid(h,PS,MS,{}));h['person_id']=MS[h['posthumous_basis']['sovereign_person_mention_id']][2]['person_id'];self.assertFalse(gift_valid(h,PS,MS,{}))
 def test_collective_count_and_distinct_members(self):
  h=copy.deepcopy(next(h for h in HS.values()if h.get('collective_designation')));self.assertTrue(holding_valid(h,C,HS));h['collective_designation']['count']=3;self.assertFalse(holding_valid(h,C,HS))
 def test_acceptance_not_generic_refusal(self):
  h=copy.deepcopy(next(h for h in HS.values()if h.get('assumption_basis',{}).get('kind')=='initial_refusal_then_explicit_acceptance'));self.assertTrue(holding_valid(h,C,HS));h['assumption_basis']['source_term']='並固讓不受';self.assertFalse(holding_valid(h,C,HS))
 def test_death506_requires_both_parallel_events(self):
  d=copy.deepcopy(next(x for x in L('015-xiefei-life-events.json')['events']if x['id'].endswith('-fei'))['normalized_date']);self.assertTrue(date_valid(d,CH,R,next(x for x in L('015-xiefei-life-events.json')['events']if x['id'].endswith('-fei')),'life_event'));d['fixed_primary_binding']['corroborating_appointment_anchor']['quote']='';self.assertFalse(date_valid(d,CH,R,next(x for x in L('015-xiefei-life-events.json')['events']if x['id'].endswith('-fei')),'life_event'))
 def test_date_year_or_raw_offsets_failclosed(self):
  d=copy.deepcopy(next(x for x in L('015-xiefei-life-events.json')['events']if x['id'].endswith('-fei'))['normalized_date']);d['year']=508;d['era_year']=508;self.assertFalse(date_valid(d,CH,R,next(x for x in L('015-xiefei-life-events.json')['events']if x['id'].endswith('-fei')),'life_event'));d['year']=506;d['era_year']=506;d['fixed_primary_binding']['event_anchor']['raw_start']+=1;self.assertFalse(date_valid(d,CH,R,next(x for x in L('015-xiefei-life-events.json')['events']if x['id'].endswith('-fei')),'life_event'))
 def test_profile_bundle_includes_details_without_fake_offices(self):
  cat=load_catalog(R);pid=AS[0]['subject_person_id'];b=bundle(pid,catalog=cat);self.assertTrue(b['source_details']);self.assertEqual(2,len([q for q in b['title_proposals']if q['proposal_kind']=='appointment_service_unreported']));self.assertFalse(any(t['title']=='中二千石'for t in b['title_holdings']));self.assertTrue(any(x['kind']=='parallel_chronology_qualification'for x in bundle(AS[3]['object_person_id'],catalog=cat)['source_reading_cases']))
if __name__=='__main__':unittest.main()
