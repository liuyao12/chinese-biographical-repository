import unittest,json,copy,hashlib
from pathlib import Path
from scripts.biographical_appointment_sequence import holding_valid,event_valid,proposal_errors,detail_valid,analyse
from scripts.validate_corpus import normalized_date_errors
R=Path(__file__).resolve().parents[1]
D=json.loads((R/'corpus/sanguozhi/022-chenqun-chentai.json').read_text());PID=D['paragraphs'][0]['mentions'][0]['person_id']
HS={h['id']:h for h in json.loads((R/'corpus/sanguozhi/022-chenqun-chentai-titles.json').read_text())['holdings']if 'source_role_sequence'in h}
E=next(e for e in json.loads((R/'corpus/sanguozhi/022-chenqun-chentai-life-events.json').read_text())['events']if 'source_role_sequence'in e)
Q=next(q for q in D['annotation']['title_proposals']if q.get('source_appointment_context',{}).get('kind')=='received_biographical_role_sequence')
DETAILS=json.loads((R/'corpus/sanguozhi/022-chenqun-source-details.json').read_text())['records']
def selected(rule,slot):return copy.deepcopy(next(h for h in HS.values()if h['source_role_sequence']['rule']==rule and h['source_role_slot']==slot))
class BiographyAppointmentSequenceTests(unittest.TestCase):
 def test_complete_native_source_sequence(self):
  self.assertEqual(len(HS),28);self.assertTrue(all(holding_valid(h,D)for h in HS.values()));self.assertTrue(event_valid(E,D));self.assertFalse(proposal_errors(Q,D,{PID}));self.assertTrue(all(detail_valid(x,D,HS)for x in DETAILS))
 def test_omitted_subject_after_accession_and_successor_is_biography_owner(self):
  for rule,slot in [('accession_office_series','office2'),('testamentary_successor_office_series','rank'),('testamentary_successor_office_series','office')]:
   h=selected(rule,slot);self.assertEqual(h['person_id'],PID);self.assertTrue(holding_valid(h,D));self.assertIsNone(h['effective_period']['start']['date_expression'])
 def test_issuer_cannot_replace_recipient_consistently(self):
  h=selected('accession_office_series','office2');g=h['source_role_sequence'];mid=g['roles']['ruler'];who=next(m for m in D['paragraphs'][0]['mentions']if m['id']==mid)['person_id'];h['person_id']=who;h['evidence'][0]['person_mention_id']=mid;h['attestations'][0]['person_mention_id']=mid;g['roles']['subject']=mid;g['roles']['subject_repeat']=mid;self.assertFalse(holding_valid(h,D))
 def test_testamentary_fellow_cannot_be_recipient(self):
  h=selected('testamentary_successor_office_series','rank');g=h['source_role_sequence'];mid=g['roles']['fellow1'];h['person_id']=next(m for m in D['paragraphs'][0]['mentions']if m['id']==mid)['person_id'];h['evidence'][0]['person_mention_id']=mid;h['attestations'][0]['person_mention_id']=mid;g['roles']['subject']=mid;self.assertFalse(holding_valid(h,D))
 def test_embedded_speech_cannot_supply_office_clause(self):
  h=selected('accession_office_series','office2');g=h['source_role_sequence'];i=D['paragraphs'][0]['text'].index('常歎曰');g['scope_anchor'].update(start=i,end=i+4,surface='常歎曰自');self.assertFalse(holding_valid(h,D))
 def test_role_frame_cannot_skip_foreign_person(self):
  h=selected('testamentary_successor_office_series','rank');del h['source_role_sequence']['roles']['fellow1'];self.assertFalse(holding_valid(h,D))
 def test_source_span_coshift_rejected(self):
  h=selected('named_transfer','office1');h['source_role_sequence']['scope_anchor']['start']+=1;h['source_role_sequence']['scope_anchor']['end']+=1;self.assertFalse(holding_valid(h,D))
 def test_death_never_ends_every_office(self):
  for original in HS.values():
   h=copy.deepcopy(original);h['effective_period']['end']={'status':'source_event','event_type':'explicit_end','date_expression':'青龍四年','evidence':E['evidence'],'normalized_date':E['normalized_date']};self.assertFalse(holding_valid(h,D))
 def test_unknown_appointment_year_cannot_be_filled_with_death_year(self):
  h=selected('testamentary_successor_office_series','office');h['source_time_scope']['normalized_start_year']=236;self.assertFalse(holding_valid(h,D))
 def test_shared_suffix_expansion_retains_distinct_source_fragments(self):
  for slot in ['county1','county2','county3']:
   h=selected('early_office_series',slot);self.assertTrue(holding_valid(h,D));self.assertEqual(h['title'],h['attestations'][0]['surface']+'令')
  h=selected('early_office_series','county1');h['shared_title_suffix']['suffix_anchor']['surface']='相';h['title']=h['attestations'][0]['surface']+'相';self.assertFalse(holding_valid(h,D))
 def test_previous_office_attestation_not_new_grant(self):
  h=selected('early_office_series','old_office');self.assertEqual(h['mode'],'attestation');self.assertEqual(h['effective_period']['start']['status'],'unknown');h['mode']='grant';self.assertFalse(holding_valid(h,D))
 def test_unassumed_county_appointment_never_holding(self):
  self.assertFalse(any(h['title']==Q['title']for h in HS.values()));q=copy.deepcopy(Q);q['outcome']='assumed';self.assertTrue(proposal_errors(q,D,{PID}))
 def test_non_assumption_term_cannot_be_dropped(self):
  q=copy.deepcopy(Q);q['non_assumption_anchor']['surface']='行';self.assertTrue(proposal_errors(q,D,{PID}))
 def test_death_owner_not_child_or_retrospective_other_person(self):
  e=copy.deepcopy(E);g=e['source_role_sequence'];mid=g['roles']['child'];e['person_id']=next(m for m in D['paragraphs'][0]['mentions']if m['id']==mid)['person_id'];e['evidence'][0]['person_mention_id']=mid;g['roles']['subject']=mid;self.assertFalse(event_valid(e,D))
 def test_explicit_qinglong_four_maps_only236(self):
  self.assertFalse(normalized_date_errors(E['normalized_date'],{D['id']:D},root=R,bound_record=E,bound_role='life_event'));e=copy.deepcopy(E);e['normalized_date']['year']=237;e['normalized_date']['era_year']=237;self.assertTrue(normalized_date_errors(e['normalized_date'],{D['id']:D},root=R,bound_record=e,bound_role='life_event'))
 def test_death_is_not_death_in_office(self):
  e=copy.deepcopy(E);e['source_term']='卒官';self.assertFalse(event_valid(e,D))
 def test_posthumous_name_does_not_receive236_as_naming_date(self):
  h=selected('death_and_posthumous_name','posthumous_name');self.assertEqual(h['title'],'靖侯');self.assertIsNone(h['effective_period']['start']['date_expression']);h['effective_period']['start']['normalized_date']=E['normalized_date'];self.assertFalse(holding_valid(h,D))
 def test_military_authority_and_institutional_privilege_not_ordinary_office(self):
  for rule,slot in [('campaign_office_series','credential'),('testamentary_successor_office_series','privilege')]:
   h=selected(rule,slot);self.assertEqual(h['kind'],'honorific');self.assertIn(h['appointment_role'],('military_authorization','institutional_privilege'));h['kind']='office';self.assertFalse(holding_valid(h,D))
 def test_fief_count_does_not_become_income(self):
  x=copy.deepcopy(next(x for x in DETAILS if x['kind']=='fief_household_count'));self.assertEqual(x['values']['total'],1300);x['values']['actual_revenue']=1300;self.assertFalse(detail_valid(x,D,HS))
 def test_regency_fellow_ids_bound_to_actual_names(self):
  x=copy.deepcopy(next(x for x in DETAILS if x['kind']=='official_duty'));x['values']['fellow_person_ids'][0]=PID;self.assertFalse(detail_valid(x,D,HS))
 def test_mourning_not_own_death(self):
  x=copy.deepcopy(next(x for x in DETAILS if x['kind']=='office_departure'));x['values']['departure_kind']='died_in_office';self.assertFalse(detail_valid(x,D,HS))
 def test_father_mourning_ends_only_last_county_office_without_a_year(self):
  for slot in ['county1','county2','county3']:
   h=selected('early_office_series',slot);end=h['effective_period']['end'];self.assertEqual(end['status'],'source_event'if slot=='county3'else'unknown');self.assertIsNone(end['date_expression']);self.assertNotIn('normalized_date',end)
  detail=next(x for x in DETAILS if x['kind']=='office_departure');self.assertEqual(detail['values']['linked_holding_ids'],[selected('early_office_series','county3')['id']])
 def test_principal_title_alias_is_issuer_not_staff_recipient(self):
  h=selected('minister_recruitment','office');d=copy.deepcopy(D);field=h['source_role_sequence']['fields']['office'];m=next(m for m in d['paragraphs'][0]['mentions']if m['start']==field['start']);self.assertNotEqual(m['person_id'],PID);m['person_id']=PID;self.assertFalse(holding_valid(h,d))
 def test_fief_source_numerals_do_not_accept_different_count(self):
  d=copy.deepcopy(next(x for x in DETAILS if x['kind']=='fief_household_count'));d['values']['increase']=5000;self.assertFalse(detail_valid(d,D,HS))
 def test_synthetic_names_and_ids_work_without_whitelist(self):
  # A minimal independent synthetic biography has the same recruitment grammar.
  t='乙字丙甲辟乙為軍府西曹掾屬';ms=[dict(id='head',start=0,end=1,surface='乙',kind='person',person_id='synthetic-person'),dict(id='issuer',start=3,end=4,surface='甲',kind='person',person_id='synthetic-issuer'),dict(id='subject',start=5,end=6,surface='乙',kind='person',person_id='synthetic-person'),dict(id='principal',start=7,end=9,surface='軍府',kind='person',person_id='synthetic-issuer')];p=dict(id='p',text=t,text_layer='received_chapter',mentions=ms);ch=dict(source={'source_commit':'synthetic-revision'},paragraphs=[p]);g=dict(kind='received_biographical_role_sequence',rule='minister_recruitment',paragraph_id='p',source_revision='synthetic-revision',paragraph_sha256=hashlib.sha256(t.encode()).hexdigest(),biography_subject_mention_id='head',scope_anchor=dict(paragraph_id='p',start=3,end=len(t),surface=t[3:]),roles={'issuer':'issuer','subject':'subject'},fields={'office':dict(paragraph_id='p',start=7,end=len(t),surface=t[7:])},human_reviewed=False,interpretation_note='synthetic grammar test')
  self.assertEqual(analyse(g,ch,'synthetic-person')[1]['subject']['person_id'],'synthetic-person')
if __name__=='__main__':unittest.main()
