import copy,json,unittest
from pathlib import Path
from scripts.source_office_reports import holding_role_valid,qualified_office_valid,detail_valid,succession_valid
ROOT=Path(__file__).resolve().parents[1]
class ChentaiOffices(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=json.loads((ROOT/'corpus/sanguozhi/022-chenqun-chentai.json').read_text());cls.ps={p['id']:(cls.c['id'],p)for p in cls.c['paragraphs']};cls.hs={h['id']:h for h in json.loads((ROOT/'corpus/sanguozhi/022-chenqun-chentai-titles.json').read_text())['holdings']};cls.new=[h for h in cls.hs.values()if h['id'].startswith('th-sgz022-chentai-')];cls.ds=json.loads((ROOT/'corpus/sanguozhi/022-chentai-source-details.json').read_text())['records'];cls.es=json.loads((ROOT/'corpus/sanguozhi/022-chentai-person-events.json').read_text())['events']
 def test_complete_ledger_resolves_every_nonexcluded_candidate(self):
  ledger=json.loads((ROOT/'source-evidence/sanguozhi022-chentai-offices/coverage.json').read_text());self.assertEqual(len(ledger['rows']),42);known=set(self.hs)|{d['id']for d in self.ds}|{e['id']for e in self.es}
  for row in ledger['rows']:
   p=self.ps[row['paragraph_id']][1];a=row['source_anchor'];self.assertEqual(p['text'][a['start']:a['end']],a['surface'])
   if row['disposition']=='consumed':self.assertTrue(row['runtime_record_ids']);self.assertTrue(set(row['runtime_record_ids'])<=known)
   else:self.assertEqual(row['disposition'],'excluded');self.assertEqual(row['runtime_record_ids'],[])
 def test_all_new_source_roles_or_qualified_reports_validate(self):
  self.assertEqual(len(self.new),25)
  for h in self.new:
   with self.subTest(h=h['id']):self.assertTrue(qualified_office_valid(h,self.c)if 'source_qualification'in h else holding_role_valid(h,self.c,self.hs))
 def test_five_nonoffice_details_are_runtime_typed(self):
  self.assertEqual(len(self.ds),5)
  for d in self.ds:self.assertTrue(detail_valid(d,self.c,self.hs),d['id'])
 def test_three_unknown_title_successions_are_runtime_events(self):
  self.assertEqual(len(self.es),3)
  for e in self.es:self.assertTrue(succession_valid(e,self.ps));self.assertIsNone(e['title']);self.assertIsNone(e['holding_id'])
 def test_wrong_consistent_recipient_does_not_pass_same_paragraph(self):
  h=copy.deepcopy(self.hs['th-sgz022-chentai-office-23']);h['person_id']='9w8_tqh_ysn_AAA';h['attestations'][0]['person_mention_id']=self.c['id']+':p010:m1526';h['evidence'][0]['person_mention_id']=h['attestations'][0]['person_mention_id'];self.assertFalse(holding_role_valid(h,self.c,self.hs))
 def test_cannot_end_office_at_death(self):
  h=copy.deepcopy(self.hs['th-sgz022-chentai-office-10']);h['effective_period']['end']=dict(status='source_event',event_type='explicit_end',date_expression='景元元年',evidence=h['evidence']);self.assertFalse(holding_role_valid(h,self.c,self.hs))
 def test_posthumous_appointment_year_not_copied_from_death(self):
  h=copy.deepcopy(self.hs['th-sgz022-chentai-office-21']);h['effective_period']['start']['date_expression']='景元元年';self.assertFalse(holding_role_valid(h,self.c,self.hs))
 def test_taichang_not_preferred_real_office(self):
  h=copy.deepcopy(self.hs['th-sgz022-chentai-ganbao-taichang-report']);h['source_qualification']['preferred_historical_office_assertion_id']=h['id'];self.assertFalse(qualified_office_valid(h,self.c))
 def test_taichang_objection_cannot_point_to_other_person(self):
  h=copy.deepcopy(self.hs['th-sgz022-chentai-ganbao-taichang-report']);h['source_qualification']['objection_evidence']['person_mention_id']=h['source_qualification']['objection_author_mention_id'];self.assertFalse(qualified_office_valid(h,self.c))
 def test_taichang_cannot_turn_report_into_grant(self):
  h=copy.deepcopy(self.hs['th-sgz022-chentai-ganbao-taichang-report']);h['mode']='grant';self.assertFalse(qualified_office_valid(h,self.c))
 def test_count_no_people_invented_or_biological_children_assumed(self):
  d=next(x for x in self.ds if x['kind']=='unnamed_family_title_grants');self.assertEqual([x['recipient_count']for x in d['values']['grants']],[1,2]);self.assertEqual(d['values']['recipient_person_ids'],[])
  d=copy.deepcopy(d);d['values']['biological_children_only']=True;self.assertFalse(detail_valid(d,self.c,self.hs))
 def test_aggregate_increase_not_total_or_revenue(self):
  d=copy.deepcopy(next(x for x in self.ds if x['kind']=='fief_household_count'));self.assertEqual(d['values']['increase'],2600);self.assertEqual(d['values']['unit_source_name'],'尸');d['values']['total']=2600;self.assertFalse(detail_valid(d,self.c,self.hs))
 def test_count_anchor_shift_to_same_numeral_elsewhere_rejected(self):
  d=copy.deepcopy(next(x for x in self.ds if x['kind']=='unnamed_family_title_grants'));a=d['source_detail_pattern']['fields']['count2'];a['start']=1477;a['end']=1478;self.assertFalse(detail_valid(d,self.c,self.hs))
 def test_selection_duty_link_to_another_office_rejected(self):
  d=copy.deepcopy(next(x for x in self.ds if x['source_term']=='典選舉'));d['values']['office_title_holding_id']='th-sgz022-chentai-office-15';self.assertFalse(detail_valid(d,self.c,self.hs))
 def test_command_supervision_not_appointment_to_subordinate_office(self):
  d=copy.deepcopy(next(x for x in self.ds if x['kind']=='command_authority'));d['values']['new_office_appointment']=True;self.assertFalse(detail_valid(d,self.c,self.hs))
 def test_succession_does_not_resolve_rank_from_posthumous_name(self):
  e=copy.deepcopy(self.es[1]);e['title']='穆侯';self.assertFalse(succession_valid(e,self.ps))
 def test_son_succession_local_parent_must_match_dead_biographical_subject(self):
  e=copy.deepcopy(self.es[1]);e['source_clause_binding']['resumed_predecessor_mention_id']=self.c['id']+':p010:m1436';self.assertFalse(succession_valid(e,self.ps))
 def test_brother_successor_cannot_be_predecessor(self):
  e=copy.deepcopy(self.es[2]);e['predecessor_person_id']=e['person_id'];self.assertFalse(succession_valid(e,self.ps))
 def test_grant_stages_and_short_reference_remain_distinct(self):
  self.assertEqual(len([h for h in self.new if h['title']=='假節']),2);self.assertEqual(len([h for h in self.new if h['title']=='尚書右僕射']),2)
  right=self.hs['th-sgz022-chentai-office-14'];left=self.hs['th-sgz022-chentai-office-20'];report=self.hs['th-sgz022-chentai-weishichunqiu-right-pushe-report'];self.assertEqual(left['mode'],'transfer');self.assertEqual(report['mode'],'attestation');self.assertNotEqual(right['evidence'][0]['paragraph_id'],report['evidence'][0]['paragraph_id'])
 def test_authorization_role_and_command_scope_are_machine_readable(self):
  h=copy.deepcopy(self.hs['th-sgz022-chentai-office-11']);h['appointment_role']='additional_office';self.assertFalse(holding_role_valid(h,self.c,self.hs))
  command=copy.deepcopy(self.hs['th-sgz022-chentai-office-12']);self.assertEqual(command['jurisdictions'][0]['source_name'],'雍涼');command['jurisdictions'][0]['source_name']='淮北';self.assertFalse(holding_role_valid(command,self.c,self.hs))
 def test_generic_role_frame_works_with_synthetic_subject(self):
  c=copy.deepcopy(self.c);p=next(p for p in c['paragraphs']if p['id'].endswith('p010'));old=self.hs['th-sgz022-chentai-office-01']['person_id'];p['text']='甲'+p['text'][1:]
  for m in p['mentions']:
   if m.get('person_id')==old:m['person_id']='synthetic_subject'
   if m['start']==0:m['surface']='甲'
  h=copy.deepcopy(self.hs['th-sgz022-chentai-office-01']);h['person_id']='synthetic_subject';h['evidence'][0]['quote']=p['text'];h['effective_period']['start']['evidence'][0]['quote']=p['text'];h['source_office_role']['scope_anchor']['surface']='甲'+h['source_office_role']['scope_anchor']['surface'][1:];h.pop('source_office_date_binding',None);h['effective_period']['start'].pop('normalized_date_range',None);self.assertTrue(holding_role_valid(h,c,{h['id']:h}))
if __name__=='__main__':unittest.main()
