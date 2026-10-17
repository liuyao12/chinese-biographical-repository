# coding: utf-8
import copy,json,unittest
from pathlib import Path
from scripts.table_evidence import load_tables,table_regnal_range_errors
from scripts.date_ranges import year_range_errors
from scripts.validate_corpus import named_office_end_valid
R=Path(__file__).resolve().parents[1]
def load(f):return json.loads((R/f).read_text())
def h(n):return next(h for h in load('corpus/shiji/112-titles.json')['holdings']if h['id']=='th-shiji112-'+str(n).zfill(3))
def life():return next(e for e in load('corpus/shiji/112-life-events.json')['events']if e['person_id']=='q69_35n_f3h')
def check(v,expr):return table_regnal_range_errors(v,expr,load_tables(R))
def anchors():
 c=load('corpus/shiji/112.json');p={p['id']:(c['id'],p)for p in c['paragraphs']};m={m['id']:(c['id'],q['id'],m)for q in c['paragraphs']for m in q['mentions']};return p,m
class LifeOfficeDates(unittest.TestCase):
 def test_four_grants_preserve_dates_as_conservative_windows(self):
  for n,years in [(3,(141,140)),(4,(131,130)),(7,(127,126)),(26,(128,127))]:
   b=h(n)['effective_period']['start'];v=b['normalized_date_range'];self.assertEqual(tuple(v[k]['era_year']for k in ['earliest','latest']),years);self.assertEqual(check(v,b['date_expression']),[]);self.assertEqual(year_range_errors(v,b['evidence'],b['date_expression']),[]);self.assertNotIn('normalized_date',b)
 def test_two_deaths_preserve_regnal_expression_and_unknown_month(self):
  es=[e for e in load('corpus/shiji/112-life-events.json')['events']if 'normalized_date_range'in e];self.assertEqual(len(es),2)
  for e,years in zip(es,[(122,121),(128,127)]):
   v=e['normalized_date_range'];self.assertEqual(tuple(v[k]['era_year']for k in ['earliest','latest']),years);self.assertEqual(check(v,e['date_expression']),[]);self.assertNotIn('normalized_date',e);self.assertNotIn('month',v)
 def test_source_ages_do_not_become_births_or_exact_civil_years(self):
  a,b=load('corpus/shiji/112.json')['annotation']['age_assertions'];self.assertEqual(a['source_term'],'年四十餘');self.assertNotIn('normalized_date_range',a);self.assertEqual(b['value'],60);self.assertIsNone(b['birth_year']);self.assertEqual(b['counting'],'unspecified_source_age');v=b['normalized_date_range'];self.assertEqual((v['earliest']['era_year'],v['latest']['era_year']),(141,140));self.assertNotIn('normalized_date',b);self.assertEqual(check(v,b['date_expression']),[])
 def test_five_source_attestations_are_not_five_grants(self):
  allh=load('corpus/shiji/112-titles.json')['holdings'];a=[(h,a)for h in allh for a in h['attestations']if 'normalized_date_range'in a];self.assertEqual(len(a),5)
  for holding,z in a:self.assertEqual(check(z['normalized_date_range'],z['date_expression']),[]);self.assertEqual(z['surface'],holding['title']);self.assertNotIn('normalized_date',z)
  self.assertEqual(h(14)['mode'],'attestation');self.assertEqual(h(14)['effective_period']['start']['status'],'unknown');self.assertEqual(h(14)['effective_period']['end']['status'],'unknown')
 def test_explicit_office_end_binds_named_office_and_holder(self):
  t=h(10);p,m=anchors();self.assertTrue(named_office_end_valid(t,p,m));self.assertEqual(t['effective_period']['end']['event_type'],'explicit_end');self.assertEqual(t['end_basis']['source_term'],'竟以丞相終');self.assertEqual(h(11)['effective_period']['end']['status'],'unknown')
  for key,value in [('kind','noble_rank'),('title','平津侯'),('person_id','q69_35n_f3h_A')]:
   bad=copy.deepcopy(t);bad[key]=value;self.assertFalse(named_office_end_valid(bad,p,m))
 def test_generic_death_cannot_be_end_of_named_office(self):
  t=copy.deepcopy(h(10));p,m=anchors();t['end_basis']['source_term']='弘病';self.assertFalse(named_office_end_valid(t,p,m));t=copy.deepcopy(h(10));t['effective_period']['end']['event_type']='death';self.assertFalse(named_office_end_valid(t,p,m))
 def test_same_year_numeral_from_another_era_is_rejected(self):
  v=copy.deepcopy(life()['normalized_date_range']);proof=v['regnal_year_table'];proof.update(era_anchor_cell_id='shiji-022-t1-r079-c01',regnal_year_cell_id='shiji-022-t1-r080-c01',digital_year_cell_id='shiji-022-t1-r080-c00');self.assertTrue(check(v,'元狩二年'))
 def test_wrong_row_revision_and_missing_original_year_ref_rejected(self):
  for key,val in [('digital_year_cell_id','shiji-022-t1-r087-c00'),('source_revision','1'),('year_source_term','三年')]:
   v=copy.deepcopy(life()['normalized_date_range']);v['regnal_year_table'][key]=val;self.assertTrue(check(v,'元狩二年'))
  v=copy.deepcopy(life()['normalized_date_range']);v['references']=[r for r in v['references']if r.get('table_cell_id')!='shiji-022-t1-r086-c01'];self.assertTrue(check(v,'元狩二年'))
 def test_taichu_direction_and_current_birth_window_are_both_checked(self):
  v=load('corpus/hanshu/098-life-events.json')['events'][0]['normalized_date_range'];self.assertEqual(check(v,'本始三年'),[]);self.assertEqual((v['earliest']['era_year'],v['latest']['era_year']),(71,70))
  for base,expr in [(v,'本始三年'),(life()['normalized_date_range'],'元狩二年')]:
   bad=copy.deepcopy(base);old=bad['regnal_year_table']['calendar_rule'];bad['regnal_year_table']['calendar_rule']='han_tenth_month_before_taichu'if old=='han_first_month_after_taichu'else'han_first_month_after_taichu';self.assertTrue(check(bad,expr))
 def test_other_title_periods_duration_and_conflicting_source_date_preserved(self):
  self.assertEqual(h(7)['effective_period']['start']['date_expression'],'元朔三年');self.assertIn('張歐免',h(7)['evidence'][0]['quote']);self.assertEqual(h(15)['effective_period']['start']['normalized_date_range']['latest']['era_year'],120);self.assertEqual(h(16)['reported_duration']['source_term'],'十餘歲');self.assertEqual(h(5)['effective_period']['start']['date_expression'],'二歲中');self.assertNotIn('normalized_date_range',h(5)['effective_period']['start'])
 def test_bundle_separates_period_attestation_age_and_death_roles(self):
  from scripts.person_bundle import bundle
  b=bundle('q69_35n_f3h',R);rs=b['date_range_normalizations'];uses=[d for d in rs if d['date_role']=='title_attestation'];self.assertEqual(len(uses),4);self.assertTrue(all('attestation_id'in x and 'endpoint'not in x for x in uses));age=next(d for d in rs if d['date_role']=='age_attestation'and d['record_id']=='age-shiji112-002');self.assertNotIn('event_type',age);end=next(d for d in rs if d['date_role']=='title_period'and d['record_id']=='th-shiji112-010'and d['endpoint']=='end');self.assertNotIn('event_type',end);self.assertTrue(any(d['date_role']=='life_event'and d['event_type']=='death'for d in rs))
 def test_cited_year_cells_do_not_create_person_mentions_or_new_sons(self):
  from scripts.person_bundle import bundle
  b=bundle('q69_35n_f3h',R);points={p['id']for p in b['table_passages']};wanted={'shiji-022-t1-r067-c00','shiji-022-t1-r077-c00','shiji-022-t1-r086-c00'};self.assertTrue(wanted.issubset(points));self.assertFalse(any(m['table_cell_id']in wanted for m in b['table_occurrences']));z=bundle('4w5_b4e_vf5_AB',R);self.assertIn('shiji-022-t1-r136-c00',{p['id']for p in z['table_passages']});self.assertTrue(any(s['source_id']=='table-witness-shiji-022'for s in z['sources']))
