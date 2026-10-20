# coding: utf-8
import copy,json,unittest
from pathlib import Path
from scripts.table_evidence import load_tables,table_title_range_errors
from scripts.date_ranges import year_range_errors
R=Path(__file__).resolve().parents[1]
def load(f):return json.loads((R/f).read_text())
def holding(hid):return next(h for h in load('corpus/shiji/112-titles.json')['holdings']if h['id']==hid)
def check(h,endpoint):
 b=h['effective_period'][endpoint];v=b['normalized_date_range'];return table_title_range_errors(v,h,endpoint,load_tables(R),b)+year_range_errors(v,b['evidence'],v['parallel_event']['source_event_quote'])
class PingjinTableDates(unittest.TestCase):
 def test_four_endpoints_bind_people_source_events_and_separate_year_rows(self):
  for hid,end,years in [('th-shiji112-010','start',(125,124)),('th-shiji112-011','start',(125,124)),('th-shiji112-015','start',(121,120)),('th-shiji112-015','end',(108,107))]:
   h=holding(hid);b=h['effective_period'][end];v=b['normalized_date_range'];self.assertEqual(check(h,end),[]);self.assertEqual(tuple(v[k]['era_year']for k in ['earliest','latest']),years);self.assertIsNone(b['date_expression']);self.assertNotIn('normalized_date',b)
 def test_previous_office_and_wrong_title_are_not_new_grants(self):
  for hid,title in [('th-shiji112-010','御史大夫'),('th-shiji112-011','冠軍侯')]:
   h=copy.deepcopy(holding(hid));h['title']=title;event=h['effective_period']['start']['normalized_date_range']['table_event'];event['title_source_term']=('為'if h['kind']=='office'else'封')+title;self.assertTrue(check(h,'start'))
  h=copy.deepcopy(holding('th-shiji112-010'));h['mode']='attestation';self.assertTrue(check(h,'start'))
 def test_fathers_grant_cannot_be_attached_to_son(self):
  h=copy.deepcopy(holding('th-shiji112-011'));h['person_id']='q69_35n_f3h_A';self.assertTrue(check(h,'start'))
 def test_child_accession_uses_explicit_table_year_not_father_death_header(self):
  h=holding('th-shiji112-015');b=h['effective_period']['start'];self.assertIn('元狩二年，弘病',b['normalized_date_range']['original_quote']);self.assertEqual(b['normalized_date_range']['table_event']['source_year_term'],'三年');self.assertTrue(all(a['date_expression']is None and 'normalized_date'not in a for a in h['attestations']));death=next(e for e in load('corpus/shiji/112-life-events.json')['events']if e['person_id']=='q69_35n_f3h');self.assertEqual(death['date_expression'],'元狩二年')
 def test_hou_first_year_is_not_an_era_first_year(self):
  h=copy.deepcopy(holding('th-shiji112-015'));v=h['effective_period']['start']['normalized_date_range'];v['table_event'].update(source_year_term='元年',event_source_term='侯慶元年');self.assertTrue(check(h,'start'))
 def test_same_numeral_in_different_era_cannot_supply_the_date(self):
  h=copy.deepcopy(holding('th-shiji112-015'));v=h['effective_period']['start']['normalized_date_range'];v['table_event']['year_mapping'].update(regnal_year_cell_id='shiji-022-t1-r099-c01',digital_year_cell_id='shiji-022-t1-r099-c00');v['earliest'].update(era_year=109,year=-108);v['latest'].update(era_year=108,year=-107);self.assertTrue(check(h,'start'))
 def test_wrong_column_or_row_and_missing_fixed_source_are_rejected(self):
  for key,value in [('era_column_id','shiji-020-t1-column-6'),('noble_name_cell_id','shiji-020-t1-r009-c00')]:
   h=copy.deepcopy(holding('th-shiji112-015'));h['effective_period']['start']['normalized_date_range']['table_event'][key]=value;self.assertTrue(check(h,'start'))
  h=copy.deepcopy(holding('th-shiji112-015'));h['effective_period']['start']['normalized_date_range']['table_event']['year_mapping']['source_revision']='1';self.assertTrue(check(h,'start'))
  h=copy.deepcopy(holding('th-shiji112-010'));h['effective_period']['start']['normalized_date_range']['table_event']['digital_year_cell_id']='shiji-022-t1-r084-c00';self.assertTrue(check(h,'start'))
 def test_calendar_and_received_column_heading_are_required(self):
  for scope in ['received_calendar_rule','column']:
   h=copy.deepcopy(holding('th-shiji112-015'));v=h['effective_period']['start']['normalized_date_range'];v['references']=[r for r in v['references']if (not r.get('table_column_id')if scope=='column'else r['scope']!=scope)];self.assertTrue(check(h,'start'))
 def test_loss_of_one_fief_does_not_end_other_offices_or_follow_death(self):
  h=holding('th-shiji112-015');self.assertEqual(h['effective_period']['end']['event_type'],'deposition');self.assertIn('國除',h['effective_period']['end']['normalized_date_range']['table_event']['event_source_term']);h=copy.deepcopy(h);h['effective_period']['end']['event_type']='death';h['effective_period']['end']['normalized_date_range']['table_event']['event_type']='death';self.assertTrue(check(h,'end'))
  self.assertEqual(holding('th-shiji112-011')['effective_period']['end']['status'],'unknown')
  office=holding('th-shiji112-016');self.assertNotIn('normalized_date_range',office['effective_period']['start']);self.assertNotIn('normalized_date_range',office['effective_period']['end'])
 def test_bundle_cites_year_cells_and_headers_without_extra_person_mentions(self):
  from scripts.person_bundle import bundle
  p=bundle('q69_35n_f3h_A',R);points={c['id']for c in p['table_passages']};needed={'shiji-022-t1-r087-c00','shiji-022-t1-r087-c01','shiji-022-t1-r100-c00','shiji-022-t1-r100-c01'};self.assertTrue(needed.issubset(points));self.assertFalse(any(m['table_cell_id']in needed for m in p['table_occurrences']));self.assertTrue(any(s['source_id']=='table-witness-shiji-022'for s in p['sources']));cols={c['id']:c for c in p['table_column_references']};self.assertEqual(cols['shiji-020-t1-column-4']['text'],'元狩');self.assertEqual(cols['shiji-020-t1-column-6']['text'],'元封');self.assertFalse(any(p['id']in needed for p in p['passages']))
