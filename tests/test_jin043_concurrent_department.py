import unittest,json,copy
from pathlib import Path
from scripts import fixed_wuyingdian_jin043_shantao as g
from scripts.source_office_reports import detail_valid
from scripts.person_bundle import load_catalog,bundle
ROOT=Path(__file__).resolve().parents[1];DETAIL='corpus/jinshu/043-wyd1739-shantao-source-details.json';TITLE='corpus/jinshu/043-wyd1739-shantao-titles.json'
class ConcurrentDepartment(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.people,cls.records=load_catalog(ROOT);cls.ch=next(r for r in cls.records if r.get('id')==g.CID);cls.roles,cls.ct=g.formal_state(cls.ch,ROOT,cls.people,cls.records);cls.details=json.loads((ROOT/DETAIL).read_bytes())['records'];cls.holdings={h['id']:h for r in cls.records for h in r.get('holdings',[])}
 def test_exact_positions_and_no_standalone_rank(self):
  self.assertEqual([(d['source_anchor']['start'],d['source_anchor']['end'])for d in self.details],[(83,86),(23,26)])
  for d in self.details:self.assertTrue(detail_valid(d,self.ch,self.holdings,ROOT));self.assertEqual(d['values']['appointment_role'],'concurrent');self.assertIsNone(d['values']['office_title'])
  hs=json.loads((ROOT/TITLE).read_bytes())['holdings'];self.assertEqual(len(hs),53);self.assertNotIn('吏部',[h['title']for h in hs]);self.assertEqual(next(h for h in hs if h['id'].endswith('-022'))['attestations'][0]['start'],18)
 def test_wrong_first_match_and_without_ling(self):
  d=copy.deepcopy(self.details[0]);d['source_anchor'].update(start=18,end=20,surface='吏部');self.assertFalse(detail_valid(d,self.ch,self.holdings,ROOT))
  d=copy.deepcopy(self.details[0]);d['source_detail_pattern']['fields']['verb'].update(start=17,end=18,surface='為');self.assertFalse(detail_valid(d,self.ch,self.holdings,ROOT))
 def test_wrong_owner_or_main_office(self):
  d=copy.deepcopy(self.details[0]);d['person_id']=self.roles['shanjian'];self.assertFalse(detail_valid(d,self.ch,self.holdings,ROOT))
  d=copy.deepcopy(self.details[0]);d['values']['linked_holding_id']='th-jin043-wyd-shan-022';self.assertFalse(detail_valid(d,self.ch,self.holdings,ROOT))
  hs=copy.deepcopy(self.holdings);hs[self.details[0]['values']['linked_holding_id']]['person_id']=self.roles['shanjian'];self.assertFalse(detail_valid(self.details[0],self.ch,hs,ROOT))
 def test_fake_title_or_year_or_tenure(self):
  for key,value in [('office_title','吏部尚書'),('appointment_role','acting'),('duty_code','unknown')]:
   d=copy.deepcopy(self.details[0]);d['values'][key]=value;self.assertFalse(detail_valid(d,self.ch,self.holdings,ROOT))
  d=copy.deepcopy(self.details[1]);d['date_expression']='永嘉初';self.assertFalse(detail_valid(d,self.ch,self.holdings,ROOT))
  d=copy.deepcopy(self.details[0]);d['reported_duration']={'value':10};self.assertFalse(detail_valid(d,self.ch,self.holdings,ROOT))
 def test_later_service_not_earlier_appointment(self):
  d=copy.deepcopy(self.details[0]);d['source_detail_pattern']['later_service_context']['source_anchor'].update(start=0,end=4,surface='自力就職');self.assertFalse(detail_valid(d,self.ch,self.holdings,ROOT));self.assertEqual(len(self.details[0]['evidence']),2);self.assertIn('乃起視事',self.details[0]['evidence'][1]['quote'])
 def test_reserved_old_record_cannot_reappear(self):
  rs=copy.deepcopy(self.records);extra={'record_type':'title_holding_assertion_set','chapter_id':g.CID,'holdings':[dict(self.holdings['th-jin043-wyd-shan-025'],id='th-jin043-wyd-shan-027')]};rs.append(extra)
  with self.assertRaises(ValueError):g.formal_state(self.ch,ROOT,self.people,rs)
 def test_local_clause_checks_even_if_expected_row_is_rebuilt_wrong(self):
  from unittest.mock import patch
  for scenario in ['first_match','missing_ling','invented_full_title','borrowed_year','individual_duration','wrong_kind']:
   d=copy.deepcopy(self.details[0])
   if scenario=='first_match':d['source_anchor'].update(start=18,end=20,surface='吏部');d['source_term']='吏部'
   if scenario=='missing_ling':d['source_detail_pattern']['fields']['verb'].update(start=17,end=18,surface='為')
   if scenario=='invented_full_title':d['values']['office_title']='吏部尚書'
   if scenario=='borrowed_year':d['date_expression']='咸寧初'
   if scenario=='individual_duration':d['reported_duration']={'value':10}
   if scenario=='wrong_kind':d['kind']='office_duration'
   ct=copy.deepcopy(self.ct);ct['sidecars'][DETAIL]['records']=[d if x['id']==d['id']else x for x in ct['sidecars'][DETAIL]['records']]
   with patch.object(g,'formal_state',lambda *args,**kwargs:(self.roles,ct)):self.assertFalse(g.concurrent_department_function_valid(d,self.ch,self.holdings,ROOT),scenario)
 def test_wrong_main_link_even_if_expected_slot_rebuilt_wrong(self):
  from unittest.mock import patch
  d=copy.deepcopy(self.details[0]);d['values']['linked_holding_id']='th-jin043-wyd-shan-022';ct=copy.deepcopy(self.ct);ct['sidecars'][DETAIL]['records'][0]=d;ct['concurrent_department_functions'][0]['linked_holding_id']=d['values']['linked_holding_id']
  with patch.object(g,'formal_state',lambda *args,**kwargs:(self.roles,ct)):self.assertFalse(g.concurrent_department_function_valid(d,self.ch,self.holdings,ROOT))
 def test_real_bundles(self):
  for role in ['shantao','shanjian']:
   b=bundle(self.roles[role],ROOT,include_provisional=True,catalog=(self.people,self.records));self.assertTrue(any(d['source_term']=='領吏部'for d in b['source_details']));self.assertFalse(any(h['title']=='吏部'and h['id'].startswith('th-jin043-wyd-shan-')for h in b['title_holdings']))
if __name__=='__main__':unittest.main()
