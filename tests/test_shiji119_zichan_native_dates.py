import copy,json,unittest
from pathlib import Path
from scripts.life_event_dates import date_decision_errors,selected_dates
ROOT=Path(__file__).resolve().parents[1]
CHILD='qjs_3hl_6ck_A'
def read(path):return json.loads((ROOT/path).read_text())
class ZichanNativeTableAndDatesTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.table=read('data/historical-tables/shiji-014.json')
  cls.cells={c['id']:c for f in cls.table['fragments'] for row in f['rows'] for c in row['cells']}
  cls.people={p['id']:p for p in read('registry/persons.json')['persons']}
  cls.events={e['id']:e for n in ['042','119'] for e in read(f'corpus/shiji/{n}-life-events.json')['events']}
  cls.choice=next(d for d in read('corpus/shiji/119-date-decisions.json')['decisions'] if d['id']=='ld-shiji119-zichan-death')
 def test_seven_received_name_occurrences_are_individual_person_markers(self):
  for row,start in [(279,17),(288,2),(298,7),(299,14),(304,3),(317,7),(346,1)]:
   cell=self.cells[f'shiji-014-r{row}-c13']
   name=[m for m in cell['person_mentions'] if m['surface']=='子產']
   self.assertEqual(len(name),1);m=name[0]
   self.assertEqual((m['start'],m['end'],m['person_id']),(start,start+2,CHILD))
   self.assertEqual(cell['text'][m['start']:m['end']],m['surface'])
 def test_two_addressed_zi_are_scoped_to_the_same_speaker_unit(self):
  cell=self.cells['shiji-014-r298-c13'];marks=cell['person_mentions']
  self.assertEqual([(m['start'],m['person_id']) for m in marks if m['surface']=='子'],[(15,CHILD),(17,CHILD)])
  old=next(m for m in marks if m['surface']=='季札')
  self.assertEqual(old['id'],'shiji-014-r298-c13-m000')
  self.assertEqual(old['person_id'],'5dm_e40_rqh_AAAAAAAAAAAAAAAAAAD')
 def test_zikong_and_zheng_zicheng_are_distinct_source_roles(self):
  rebel=next(m for m in self.cells['shiji-014-r279-c13']['person_mentions'] if m['surface']=='子孔')
  self.assertEqual(rebel['person_id'],'b5q_cso_92n')
  adviser=next(m for m in self.cells['shiji-014-r299-c13']['person_mentions'] if m['surface']=='子成')
  self.assertNotEqual(adviser['person_id'],'xgd_r31_cmr_A')
  person=self.people[adviser['person_id']]
  self.assertNotIn('family_path',person)
  self.assertEqual({a['surface'] for a in person['aliases']},{'子成'})
  self.assertTrue(all(e['kind']=='table_cell' for e in person['evidence']))
 def test_promoted_people_have_complete_native_evidence_across_all_tables(self):
  adviser=next(m['person_id'] for m in self.cells['shiji-014-r299-c13']['person_mentions'] if m['surface']=='子成')
  expected={pid:set() for pid in [CHILD,'b5q_cso_92n',adviser]}
  for path in (ROOT/'data/historical-tables').glob('*.json'):
   table=json.loads(path.read_text())
   for fragment in table.get('fragments',[]):
    for row in fragment['rows']:
     for cell in row['cells']:
      for m in cell.get('person_mentions',[]):
       if m['person_id'] in expected:expected[m['person_id']].add(m['id'])
  for pid,mids in expected.items():
   self.assertEqual(self.people[pid]['evidence_scope'],'corpus_and_native_table_mentions')
   self.assertEqual({e['mention_id'] for e in self.people[pid]['evidence'] if e.get('kind')=='table_cell'},mids)
 def test_preferred_year_retains_the_other_source_date_and_exact_received_term(self):
  source=self.events['le-shiji042-040'];preferred=self.events['le-shiji119-001']
  self.assertEqual(source['date_expression'],'聲公五年')
  self.assertEqual((source['normalized_date']['era_year'],source['normalized_date']['year']),(496,-495))
  self.assertIsNone(preferred['date_expression'])
  self.assertEqual((preferred['normalized_date']['era_year'],preferred['normalized_date']['year']),(522,-521))
  self.assertEqual(date_decision_errors(self.choice,self.events,[],self.people),[])
  selected=selected_dates(list(self.events.values()),[self.choice])
  self.assertEqual(len(selected),1);self.assertEqual(selected[0]['record_id'],preferred['id'])
  self.assertEqual(selected[0]['selection_decision_id'],self.choice['id'])
 def test_undated_alternative_cannot_be_used_for_a_numeric_choice(self):
  changed=copy.deepcopy(self.events);del changed['le-shiji042-040']['normalized_date']
  self.assertTrue(date_decision_errors(self.choice,changed,[],self.people))
 def test_year_precision_does_not_invent_death_month_or_day(self):
  for eid in self.choice['candidate_event_ids']:
   date=self.events[eid]['normalized_date'];self.assertEqual(date['precision'],'year')
   self.assertNotIn('month',date);self.assertNotIn('day',date)
  refs=self.events['le-shiji119-001']['normalized_date']['references']
  self.assertTrue(any(r.get('source_commit')=='dc3dc18e0039e05679d98bc650c2f980f8dcabac' for r in refs))
  self.assertTrue(any(r.get('scope')=='digital_editorial_regnal_year_equivalence_only' and r['quote']=='522' for r in refs))
 def test_machine_profile_keeps_both_claims_and_exposes_one_preference(self):
  p=read('data/corpus/profiles/'+CHILD+'.json')
  selected=next(d for d in p['selected_life_event_dates'] if d.get('selection_decision_id')==self.choice['id'])
  self.assertEqual(selected['era_year'],522)
  self.assertEqual({e['normalized_date']['era_year'] for e in p['life_events'] if e['id'] in self.choice['candidate_event_ids']},{496,522})
 def test_qing_grant_has_its_own_year_without_inferred_end_or_xiang_start(self):
  holdings=read('corpus/shiji/042-titles.json')['holdings']
  qing=next(h for h in holdings if h['id']=='th-shiji042-018')
  self.assertEqual(qing['effective_period']['start']['date_expression'],'十二年')
  date=qing['effective_period']['start']['normalized_date']
  self.assertEqual((date['era_year'],date['year']),(554,-553))
  self.assertTrue(any(r.get('table_cell_id')=='shiji-014-r288-c13' for r in date['references']))
  self.assertEqual(qing['effective_period']['end']['status'],'unknown')
  xiang=next(h for h in read('corpus/shiji/119-titles.json')['holdings'] if h['id']=='th-shiji119-005')
  self.assertNotIn('normalized_date',xiang['effective_period']['start'])
  self.assertEqual(xiang['reported_duration']['value'],26)
 def test_liedafu_explanation_does_not_import_other_biographies(self):
  h=next(h for h in read('corpus/shiji/119-titles.json')['holdings'] if h['id']=='th-shiji119-003')
  self.assertEqual(h['effective_period']['start']['status'],'unknown')
  self.assertNotIn('三得相三去相',h['interpretation_note'])
  self.assertNotIn('三月為相',h['interpretation_note'])
 def test_addressed_zi_is_not_promoted_to_a_courtesy_name(self):
  name=next(n for n in read('data/corpus/profile-names.json')['records'] if n['person_id']==CHILD)
  self.assertIsNone(name['surname']);self.assertIsNone(name['ming'])
  self.assertNotIn('子',name['additional_names'])
  self.assertEqual(name['additional_names'],['子産'])
  chapter=read('corpus/shiji/119.json')
  para=next(p for p in chapter['paragraphs'] if p['id']==name['paragraph_id'])
  self.assertIn(name['quote'],para['text'])
if __name__=='__main__':unittest.main()
