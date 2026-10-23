import unittest,json,copy
from pathlib import Path
from scripts.role_event_year_bridge import valid,range_errors
from scripts.biographical_appointment_sequence import holding_valid
from scripts.validate_corpus import normalized_date_errors
R=Path(__file__).resolve().parents[1];CH='corpus/sanguozhi/022-chenqun-chentai.json';TIT='corpus/sanguozhi/022-chenqun-chentai-titles.json'
C=json.loads((R/CH).read_text());HS=json.loads((R/TIT).read_text())['holdings']
def select(rule,slot):return copy.deepcopy(next(h for h in HS if h.get('source_role_sequence',{}).get('rule')==rule and h.get('source_role_slot')==slot))
class RoleEventBridge(unittest.TestCase):
 def test_all_nine_production_role_contracts(self):
  hs=[h for h in HS if 'source_role_year_bridge'in h];self.assertEqual(len(hs),9)
  for h in hs:
   self.assertTrue(valid(h,C,R),h['id']);self.assertTrue(holding_valid(h,C,R),h['id']);s=h['effective_period']['start']
   if 'normalized_date'in s:self.assertEqual(normalized_date_errors(s['normalized_date'],{C['id']:C},R,h,'start'),[],h['id'])
   else:self.assertEqual(range_errors(s['normalized_date_range'],h['evidence'],None,R),[])
 def test_expected_exact_years_and_ranges(self):
  self.assertEqual(sorted(h['effective_period']['start']['normalized_date']['year']for h in HS if 'source_role_year_bridge'in h and 'normalized_date'in h['effective_period']['start']),[220,220,220,220,225,226,226])
  for slot in ('office4','rank2'):
   r=select('accession_office_series',slot)['effective_period']['start']['normalized_date_range'];self.assertEqual((r['earliest']['year'],r['latest']['year']),(220,225));self.assertNotIn('year',r)
 def test_taihe_227_not_accession_year(self):
  h=select('testamentary_successor_office_series','rank');h['effective_period']['start']['normalized_date'].update(year=227,era_year=227);h['source_time_scope']['normalized_start_year']=227;self.assertFalse(valid(h,C,R))
 def test_accession_day_not_appointment_day(self):
  h=select('accession_office_series','rank1');h['effective_period']['start']['normalized_date']['month']=10;self.assertFalse(valid(h,C,R))
 def test_no_death_as_all_tenure_ends(self):
  for h in [copy.deepcopy(h)for h in HS if 'source_role_year_bridge'in h]:h['effective_period']['end']={'status':'source_event','event_type':'explicit_end','date_expression':'青龍四年','evidence':h['evidence']};self.assertFalse(valid(h,C,R))
 def test_following_office_cannot_be_exact220(self):
  h=select('accession_office_series','office4');h['effective_period']['start']['normalized_date']=select('accession_office_series','office2')['effective_period']['start']['normalized_date'];self.assertFalse(valid(h,C,R))
 def test_stale_fixed_source_hash_rejected(self):
  h=select('campaign_office_series','office3');h['source_role_year_bridge']['proofs'][0]['sha256']='0'*64;self.assertFalse(valid(h,C,R))
 def test_different_person_or_ruler_rejected(self):
  h=select('accession_office_series','office2');h['source_role_year_bridge']['person_id']='wrong';self.assertFalse(valid(h,C,R));h=select('accession_office_series','office2');h['source_role_year_bridge']['ruler_person_id']='wrong';self.assertFalse(valid(h,C,R))
 def test_unanchored_roles_remain_undated(self):
  for rule,slot in [('testamentary_successor_office_series','duty'),('campaign_office_series','duty'),('testamentary_successor_office_series','privilege'),('campaign_office_series','office4')]:
   h=select(rule,slot);self.assertNotIn('source_role_year_bridge',h);self.assertNotIn('normalized_date',h['effective_period']['start']);self.assertNotIn('normalized_date_range',h['effective_period']['start'])
 def test_wrong_external_offset_or_six_to_five_rejected(self):
  h=select('campaign_office_series','office3');h['source_role_year_bridge']['proofs'][0]['event']['start']+=1;self.assertFalse(valid(h,C,R));h=select('campaign_office_series','office3');h['source_role_year_bridge']['proofs'][0]['mapping']['source_number']='五';self.assertFalse(valid(h,C,R))
 def test_archived_raw_and_full_units_are_locally_resolvable(self):
  import hashlib
  j=json.loads((R/'source-evidence/chenqun-title-date-bridges/review.json').read_text())
  for s in j['sources']:self.assertEqual(hashlib.sha256((R/s['path']).read_bytes()).hexdigest(),s['sha256'])
  for u in j['complete_units']:self.assertEqual((R/u['raw_path']).read_text()[u['start']:u['end']],u['text'])
  for a in j['raw_anchors']:self.assertEqual((R/a['raw_path']).read_text()[a['start']:a['end']],a['quote'])
