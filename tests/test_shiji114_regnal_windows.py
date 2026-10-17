# coding:utf-8
import copy,json,unittest
from pathlib import Path
from scripts.table_evidence import load_tables,table_regnal_range_errors,regnal_reign_designation_valid
from scripts.table_title_holdings import table_title_errors
from scripts.date_ranges import year_range_errors
from scripts.person_bundle import bundle
R=Path(__file__).resolve().parents[1]
def load(f):return json.loads((R/f).read_text())
class DongyueRegnalWindows(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=load('corpus/shiji/114.json');cls.mentions={m['id']:(cls.c['id'],p['id'],m)for p in cls.c['paragraphs']for m in p['mentions']};cls.tables=load_tables(R);cls.people={p['id']for p in load('registry/persons.json')['persons']};cls.hs={h['id']:h for h in load('corpus/shiji/114-titles.json')['holdings']};cls.lives=load('corpus/shiji/114-life-events.json')['events']
 def title(self,suffix):return self.hs['th-shiji114-'+suffix]
 def test_five_explicit_grants_preserve_two_year_windows_and_literal_years(self):
  for suffix,expr,year in [('001','漢五年',202),('002','孝惠三年',192),('013','建元六年',135),('035','建元六年',135),('036','建元六年',135)]:
   b=self.title(suffix)['effective_period']['start'];self.assertEqual(b['date_expression'],expr);self.assertNotIn('normalized_date',b);d=b['normalized_date_range'];self.assertEqual((d['earliest']['era_year'],d['latest']['era_year']),(year+1,year));self.assertEqual(table_regnal_range_errors(d,expr,self.tables,self.mentions),[]);self.assertEqual(year_range_errors(d,b['evidence'],expr),[])
 def test_han_fifth_year_has_same_person_body_and_native_table_anchors(self):
  b=self.title('001')['effective_period']['start'];d=b['normalized_date_range'];p=d['regnal_year_table'];a=p['reign_designation'];self.assertEqual(a['kind'],'same_person_source_and_table_designations');self.assertEqual(a['source_era_name'],'漢');self.assertEqual(a['table_era_name'],'高皇帝');self.assertEqual(a['person_id'],'yqp_nlb_p1p_A');self.assertTrue(regnal_reign_designation_valid(p,d,self.mentions,self.tables));self.assertIn('高帝',a['source_context_quote']);self.assertIn('漢五年',a['source_context_quote'])
 def test_dual_anchor_claim_rejects_other_body_person_table_person_and_missing_anchor(self):
  original=self.title('001')['effective_period']['start']['normalized_date_range']
  for kind in ['body','table','context','id','review']:
   d=copy.deepcopy(original);p=d['regnal_year_table'];a=p['reign_designation']
   if kind=='body':a['person_mention_id']='c-shiji-114-dongyue:m001-0137'
   elif kind=='table':a['table_person_mention_id']='missing'
   elif kind=='context':a['source_context_quote']='漢五年'
   elif kind=='id':a['person_id']='yqp_nlb_p1p_AA'
   else:a['human_reviewed']=True
   self.assertTrue(table_regnal_range_errors(d,'漢五年',self.tables,self.mentions),kind)
 def test_changed_table_person_cannot_prove_a_body_reign_alias(self):
  ts=copy.deepcopy(self.tables);cell=next(c for f in ts['shiji-022']['fragments']for r in f['rows']for c in r['cells']if c['id']=='shiji-022-t1-r001-c01');cell['person_mentions'][0]['person_id']='yqp_nlb_p1p_AA';d=self.title('001')['effective_period']['start']['normalized_date_range'];self.assertTrue(table_regnal_range_errors(d,'漢五年',ts,self.mentions))
 def test_year_cell_and_source_revision_cannot_be_borrowed_from_another_year(self):
  for field,value in [('regnal_year_cell_id','shiji-022-t1-r006-c01'),('source_revision','0')]:
   d=copy.deepcopy(self.title('001')['effective_period']['start']['normalized_date_range']);d['regnal_year_table'][field]=value;self.assertTrue(table_regnal_range_errors(d,'漢五年',self.tables,self.mentions))
 def test_winter_death_preserves_winter_and_adjacent_common_era_years(self):
  e=next(e for e in self.lives if e['person_id']=='u5g_scl_2bs');self.assertEqual(e['date_expression'],'元封元年冬');d=e['normalized_date_range'];self.assertEqual(d['regnal_year_table']['season_source_term'],'冬');self.assertEqual((d['earliest']['era_year'],d['latest']['era_year']),(111,110));self.assertEqual(table_regnal_range_errors(d,e['date_expression'],self.tables,self.mentions),[])
 def test_winter_proof_cannot_invent_another_season_or_erase_literal_season(self):
  original=next(e['normalized_date_range']for e in self.lives if e['person_id']=='u5g_scl_2bs')
  for season,expr in [('秋','元封元年秋'),('','元封元年'),('冬','元封元年')]:
   d=copy.deepcopy(original);d['regnal_year_table']['season_source_term']=season;self.assertTrue(table_regnal_range_errors(d,expr,self.tables,self.mentions))
 def test_three_unknown_month_deaths_do_not_claim_exact_single_ce_year(self):
  for pid,year in [('yqp_nlb_p1p_CA',154),('tvi_05j_cxc',138),('xp5_39k_w5w',135)]:
   e=next(e for e in self.lives if e['person_id']==pid);self.assertNotIn('normalized_date',e);self.assertEqual((e['normalized_date_range']['earliest']['era_year'],e['normalized_date_range']['latest']['era_year']),(year+1,year))
 def test_autumn_keeps_source_season_and_same_digital_ce_year(self):
  dates=[]
  for suffix in ['016','017','018']:
   h=self.title(suffix)
   for a in h['attestations']:self.assertEqual(a['date_expression'],'元鼎六年秋');dates.append(a['normalized_date'])
  dates.append(self.title('016')['effective_period']['start']['normalized_date'])
  for e in self.lives:
   if e['person_id']in ['yr9_kr5_pfz','yqp_nlb_p1p_ABFAC']:self.assertEqual(e['date_expression'],'元鼎六年秋');dates.append(e['normalized_date'])
  self.assertEqual(len(dates),6)
  for d in dates:self.assertEqual((d['era_year'],d['year']),(111,-110));self.assertIn('元鼎六年秋',d['original_quote']);self.assertTrue(any(r.get('table_cell_id')=='shiji-022-t1-r096-c00'and r['quote']=='111'for r in d['references']))
 def test_dated_title_usage_does_not_become_title_accession(self):
  for suffix in ['006','007','008','009','010','011','012','017','018']:
   h=self.title(suffix);self.assertEqual(h['effective_period']['start']['status'],'unknown');self.assertTrue('normalized_date_range'in h['attestations'][0]or 'normalized_date'in h['attestations'][0]);self.assertEqual(h['effective_period']['end']['status'],'unknown')
 def test_three_former_title_uses_remain_retrospective(self):
  for suffix in ['018','024','032']:self.assertEqual(self.title(suffix)['attestations'][0]['usage'],'retrospective')
 def test_untimed_proclamation_and_dispatch_are_not_filled_from_later_winter(self):
  for suffix in ['019','020','021']:
   h=self.title(suffix)
   for a in h['attestations']:self.assertNotIn('normalized_date_range',a);self.assertNotIn('normalized_date',a)
 def test_prose_winter_campaign_is_not_a_precise_grant_date(self):
  h=self.title('023');b=h['effective_period']['start'];self.assertIsNone(b['date_expression']);self.assertNotIn('normalized_date',b);self.assertNotIn('normalized_date_range',b);self.assertEqual(b['event_type'],'grant');self.assertIn('元封元年冬',b['evidence'][0]['quote'])
 def test_native_intercalary_grant_retains_three_original_cells(self):
  hs=load('corpus/shiji/020-table-title-events.json')['holdings'];self.assertEqual(len(hs),9);h=next(h for h in hs if h['id']=='th-table-shiji020-r060-founding-grant');self.assertEqual(table_title_errors(h,self.tables,self.people),[]);self.assertEqual(h['person_id'],'08e_bwz_ync');self.assertEqual(h['title'],'蘌兒侯');b=h['effective_period']['start'];self.assertEqual(b['date_expression'],'元封元年閏月癸卯');self.assertEqual((b['normalized_date_range']['earliest']['era_year'],b['normalized_date_range']['latest']['era_year']),(111,110));self.assertTrue(all(e['kind']=='table_cell'and 'paragraph_id'not in e for e in h['evidence']));self.assertEqual(h['effective_period']['end']['status'],'unknown')
 def test_bundle_export_can_validate_source_reign_and_winter_without_nlu(self):
  for pid in ['e00_pe1_zri','u5g_scl_2bs','08e_bwz_ync']:
   b=bundle(pid,R);self.assertTrue(b['table_passages']);self.assertTrue(any(s['source_id']=='table-witness-shiji-022'for s in b['sources']))
 def test_received_eleven_paragraphs_and_revision_are_unchanged(self):
  self.assertEqual(self.c['text_sha256'],'b38ea0d040864a0368385740200d92755990ada0d0d3676e768cff945a22fc6f');self.assertEqual(self.c['source']['revision_id'],8735633);self.assertEqual(len(self.c['paragraphs']),11)
if __name__=='__main__':unittest.main()
