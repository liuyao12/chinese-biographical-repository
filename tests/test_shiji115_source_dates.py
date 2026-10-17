import copy,json,unittest
from pathlib import Path
from scripts.table_evidence import load_tables,table_regnal_range_errors
from scripts.table_title_holdings import table_title_errors
from scripts.table_life_events import native_death_errors
from scripts.person_bundle import bundle
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads((R/p).read_text())
class ChaoxianSourceDates(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.tables=load_tables(R);cls.people={p['id']for p in read('registry/persons.json')['persons']};cls.native={h['id']:h for h in read('corpus/shiji/020-table-title-events.json')['holdings']};cls.prose={h['id']:h for h in read('corpus/shiji/115-titles.json')['holdings']};cls.events=read('corpus/shiji/115-life-events.json')['events'];cls.record=read('corpus/shiji/020-table-life-events.json');cls.zui=next(e for e in cls.record['events']if e['id']=='le-table-shiji020-r073-zui')
 def grant(self,n):return self.native[f'th-table-shiji020-r{n:03}-founding-grant']
 def test_four_native_grants_keep_distinct_original_dates(self):
  for n,expr,year in [(66,'元封三年四月丁卯',108),(67,'元封三年四月',108),(68,'元封三年六月丙辰',108),(73,'元封四年三月壬寅',107)]:
   h=self.grant(n);self.assertEqual(table_title_errors(h,self.tables,self.people),[]);s=h['effective_period']['start'];self.assertEqual(s['date_expression'],expr);self.assertEqual(s['normalized_date']['era_year'],year);self.assertEqual(s['normalized_date']['precision'],'year')
 def test_month_only_never_invents_a_sexagenary_day(self):
  h=self.grant(67);self.assertEqual(h['table_title_basis']['date_parts'][1]['text'],'三年四月');self.assertNotIn('day',h['effective_period']['start']['normalized_date'])
 def test_forged_day_is_rejected_against_actual_cell(self):
  h=copy.deepcopy(self.grant(67));h['table_title_basis']['date_parts'][1]['text']+='丁卯';h['effective_period']['start']['date_expression']+='丁卯';self.assertTrue(table_title_errors(h,self.tables,self.people))
 def test_later_death_occurrence_cannot_be_first_grant_anchor(self):
  h=copy.deepcopy(self.grant(66));h['table_title_basis']['event']['person_mention_id']='shiji-020-t1-r066-c06-m001';self.assertTrue(table_title_errors(h,self.tables,self.people))
 def test_five_prose_grants_do_not_inherit_the_king_death_year(self):
  for i in range(16,21):
   h=self.prose[f'th-shiji115-{i:03}'];s=h['effective_period']['start'];self.assertEqual(s['event_type'],'grant');self.assertIsNone(s['date_expression']);self.assertNotIn('normalized_date',s)
   for a in h['attestations']:self.assertIsNone(a['date_expression']);self.assertNotIn('normalized_date',a)
 def test_two_unknown_month_deaths_keep_adjacent_year_windows(self):
  for pid in ['fa5_rxi_3t4','3rh_ei8_elm']:
   e=next(e for e in self.events if e['person_id']==pid);self.assertNotIn('normalized_date',e);d=e['normalized_date_range'];self.assertEqual([d[k]['era_year']for k in ['earliest','latest']],[110,109]);self.assertEqual(table_regnal_range_errors(d,e['date_expression'],self.tables),[])
 def test_chengsi_date_is_not_silently_copied_from_prior_killing(self):
  e=next(e for e in self.events if e['person_id']=='0hn_hdh_t8n');self.assertEqual(e['source_term'],'誅成巳');self.assertIsNone(e['date_expression']);self.assertNotIn('normalized_date',e)
 def test_rightqu_summer_death_remains_fixed_source_year_108(self):
  e=next(e for e in self.events if e['person_id']=='f41_ulg_3u1_*A');self.assertEqual((e['date_expression'],e['normalized_date']['era_year']),('元封三年夏',108));self.assertTrue(any(r.get('table_cell_id')=='shiji-022-t1-r099-c00'for r in e['normalized_date']['references']))
 def test_zui_death_has_fixed_name_anchor_and_post_reform_window(self):
  e=self.zui;self.assertEqual(native_death_errors(self.record,e,self.tables,self.people),[]);self.assertEqual(e['date_expression'],'太初二年');self.assertEqual([e['normalized_date_range'][k]['era_year']for k in ['earliest','latest']],[103,102]);self.assertEqual(e['evidence'][0]['person_mention_id'],'shiji-020-t1-r073-c07-m000')
 def test_zui_count_and_title_prefix_cannot_be_fabricated_or_omitted(self):
  for kind in ['count','title','omit']:
   e=copy.deepcopy(self.zui)
   if kind=='omit':e.pop('date_layout')
   elif kind=='count':e['date_layout']['cell_count_source_term']='三。'
   else:e['date_layout']['title_source_term']='王'
   self.assertTrue(native_death_errors(self.record,e,self.tables,self.people),kind)
 def test_bundle_contains_explicit_native_grant_and_death_without_forcing_other_titles(self):
  p=bundle('z9d_qn5_wg8_A',R);h=next(h for h in p['title_holdings']if h['id']=='th-table-shiji020-r073-founding-grant');self.assertEqual(h['title'],'涅陽侯');self.assertEqual(h['effective_period']['start']['normalized_date']['era_year'],107);self.assertTrue(any(e['id']==self.zui['id']for e in p['life_events']));self.assertTrue(all(h['effective_period']['end']['status']=='unknown'for h in p['title_holdings']))
 def test_prior_taichu_transition_and_original_prose_are_preserved(self):
  e=self.record['events'][0];self.assertEqual([e['normalized_date_range'][k]['era_year']for k in ['earliest','latest']],[105,103]);c=read('corpus/shiji/115.json');self.assertEqual(c['source']['revision_id'],439220);self.assertIn('長［降］',next(p['text']for p in c['paragraphs']if p['id'].endswith('p008')))
if __name__=='__main__':unittest.main()
