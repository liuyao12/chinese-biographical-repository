import copy,json,unittest
from pathlib import Path
from scripts.table_evidence import load_tables
from scripts.table_title_holdings import table_title_errors
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads((R/p).read_text())
class DongyueNativeGrants(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.tables=load_tables(R);cls.people={p['id'] for p in read('registry/persons.json')['persons']};cls.hs={h['id']:h for h in read('corpus/shiji/020-table-title-events.json')['holdings']}
 def holding(self,n):return self.hs[f'th-table-shiji020-r{n:03}-founding-grant']
 def test_four_grants_keep_native_person_cells(self):
  for n,pid,title in [(57,'bxw_vv0_1t3','北石侯'),(61,'43i_62q_gf6','開陵侯'),(63,'1bh_uew_js1','東成侯'),(64,'7ty_ab1_ab9','無錫侯')]:
   h=self.holding(n);self.assertEqual((h['person_id'],h['title']),(pid,title));self.assertEqual(table_title_errors(h,self.tables,self.people),[]);self.assertEqual(h['effective_period']['end']['status'],'unknown');self.assertTrue(all('paragraph_id'not in e for e in h['evidence']))
 def test_first_month_has_year_only_conversion_and_original_day(self):
  s=self.holding(57)['effective_period']['start'];self.assertEqual(s['date_expression'],'元封元年正月壬午');self.assertEqual(s['normalized_date']['era_year'],110);self.assertEqual(s['normalized_date']['precision'],'year');self.assertNotIn('normalized_date_range',s)
 def test_intercalary_months_remain_ranges(self):
  for n in [61,63]:
   s=self.holding(n)['effective_period']['start'];self.assertEqual(s['date_expression'],'元封元年閏月癸卯');self.assertEqual([s['normalized_date_range'][k]['era_year'] for k in ['earliest','latest']],[111,110])
 def test_year_only_never_invents_month_and_uses_range(self):
  h=self.holding(64);s=h['effective_period']['start'];self.assertEqual(s['date_expression'],'元封元年');self.assertEqual(h['table_title_basis']['date_parts'][1]['text'],'元年');self.assertEqual([s['normalized_date_range'][k]['era_year'] for k in ['earliest','latest']],[111,110]);self.assertNotIn('normalized_date',s)
 def test_unknown_month_cannot_collapse_to_scalar(self):
  h=copy.deepcopy(self.holding(64));s=h['effective_period']['start'];d=s.pop('normalized_date_range');d.pop('earliest');d.pop('latest');d.update(era='BCE',era_year=110,year=-109,precision='year');s['normalized_date']=d;self.assertTrue(table_title_errors(h,self.tables,self.people))
 def test_successor_cannot_become_founding_holder(self):
  h=copy.deepcopy(self.holding(57));h['person_id']='76z_zdc_38o';self.assertTrue(table_title_errors(h,self.tables,self.people))
 def test_source_households_are_retained_without_residence_inference(self):
  h=self.holding(63);self.assertEqual(h['table_title_basis']['merit']['quote'],'以故東越繇王斬東越王餘善功侯，萬戶。');self.assertNotIn('residence',h)
 def test_qiantang_is_source_designation_not_invented_birthplace(self):
  a=next(a for a in read('corpus/shiji/114-addresses.json')['assertions'] if a['id']=='pa-shiji114-002');self.assertEqual((a['person_id'],a['relation'],a['place']['source_name']),('08e_bwz_ync','source_locality_designation','錢唐'));self.assertIsNone(a['place']['modern_identification']);self.assertIsNone(a['qualifiers']['origin_or_residence']);self.assertTrue(all(a['source_term']in e['quote']for e in a['evidence']))
if __name__=='__main__':unittest.main()
