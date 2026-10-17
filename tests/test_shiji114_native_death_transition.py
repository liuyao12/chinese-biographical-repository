import copy,json,unittest
from pathlib import Path
from scripts.table_evidence import load_tables,table_regnal_range_errors
from scripts.table_life_events import native_death_errors
from scripts.date_ranges import year_range_errors
from scripts.person_bundle import bundle
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads((R/p).read_text())
class NativeDeathTransition(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.record=read('corpus/shiji/020-table-life-events.json');cls.event=cls.record['events'][0];cls.tables=load_tables(R);cls.people={p['id']for p in read('registry/persons.json')['persons']}
 def test_native_death_keeps_actual_person_and_received_year(self):
  e=self.event;self.assertEqual(native_death_errors(self.record,e,self.tables,self.people),[]);self.assertEqual((e['person_id'],e['source_term'],e['date_expression']),('08e_bwz_ync','終古死','太初元年'));self.assertNotIn('paragraph_id',e['evidence'][0])
 def test_fixed_transition_preserves_three_ce_years(self):
  d=self.event['normalized_date_range'];self.assertEqual([d[k]['era_year']for k in ['earliest','latest']],[105,103]);self.assertEqual(year_range_errors(d,self.event['evidence'],'太初元年'),[]);self.assertEqual(table_regnal_range_errors(d,'太初元年',self.tables),[])
 def test_wrong_person_revision_quote_or_year_rejected(self):
  for kind in ['person','revision','quote','year','term','fake_paragraph']:
   e=copy.deepcopy(self.event)
   if kind=='person':e['person_id']='bxw_vv0_1t3'
   elif kind=='revision':e['evidence'][0]['source_revision']='0'
   elif kind=='quote':e['evidence'][0]['quote']='無後，國除。'
   elif kind=='year':e['date_expression']='太初二年'
   elif kind=='term':e['source_term']='國除'
   else:e['evidence'][0]['paragraph_id']='fake'
   self.assertTrue(native_death_errors(self.record,e,self.tables,self.people),kind)
 def test_negated_conditional_and_legal_death_rejected(self):
  for phrase in ['終古未死','終古當死','終古死罪']:
   ts=copy.deepcopy(self.tables);e=copy.deepcopy(self.event);c=next(c for f in ts['shiji-020']['fragments']for row in f['rows']for c in row['cells']if c['id']==e['evidence'][0]['table_cell_id']);c['text']=c['text'].replace('終古死',phrase);e['evidence'][0]['quote']=c['text'];self.assertTrue(any('明記' in x for x in native_death_errors(self.record,e,ts,self.people)),phrase)
 def test_conversion_cannot_use_other_year_or_fake_event_month(self):
  for field,value in [('astronomical_table_year',-102),('event_month','五月'),('last_month_date','12-12')]:
   d=copy.deepcopy(self.event['normalized_date_range']);d['calendar_reform'][field]=value;self.assertTrue(year_range_errors(d,self.event['evidence'],'太初元年'))
 def test_all_boundary_rule_references_required(self):
  original=self.event['normalized_date_range']
  for i in range(5):
   d=copy.deepcopy(original);d['references'].pop(i);self.assertTrue(year_range_errors(d,self.event['evidence'],'太初元年'),i)
 def test_unfixed_reconstruction_reference_rejected(self):
  d=copy.deepcopy(self.event['normalized_date_range']);d['references'][1]['url']=d['references'][1]['url'].replace('719e02ff011ab122aad5fb29084e3f6ee8b65390','main');self.assertTrue(year_range_errors(d,self.event['evidence'],'太初元年'))
 def test_editorial_104_is_not_exact_death_year(self):
  d=copy.deepcopy(self.event['normalized_date_range']);d['earliest']=d['latest']=dict(era='BCE',era_year=104,year=-103);self.assertTrue(year_range_errors(d,self.event['evidence'],'太初元年'))
 def test_original_year_table_and_source_revision_checked(self):
  d=copy.deepcopy(self.event['normalized_date_range']);d['references'][-1]['quote']='103';self.assertTrue(table_regnal_range_errors(d,'太初元年',self.tables));d=copy.deepcopy(self.event['normalized_date_range']);d['references'][-1]['url']='https://example.org';self.assertTrue(table_regnal_range_errors(d,'太初元年',self.tables))
 def test_general_year_model_still_rejects_three_years(self):
  d=copy.deepcopy(self.event['normalized_date_range']);d['basis']='regnal_year_crosses_ce_year';self.assertTrue(any('相鄰兩年'in x for x in year_range_errors(d,self.event['evidence'],'太初元年')))
 def test_bundle_collects_native_event_year_cells_and_study_refs(self):
  p=bundle('08e_bwz_ync',R);e=next(e for e in p['life_events']if e['id']==self.event['id']);self.assertEqual(e['study_references'][0]['opinion_validation'],'not_attempted');self.assertTrue(any(c['id']=='shiji-022-t1-r103-c00'for c in p['table_passages']));self.assertTrue(any(d['record_id']==e['id']and d['basis']=='calendar_reform_transition_year'for d in p['date_range_normalizations']))
 def test_death_does_not_end_title_or_count_children(self):
  p=bundle('08e_bwz_ync',R);self.assertTrue(all(h['effective_period']['end']['status']=='unknown'for h in p['title_holdings']));self.assertNotIn('biological_children_count',self.event)
if __name__=='__main__':unittest.main()
