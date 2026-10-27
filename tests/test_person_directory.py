import copy,json,tempfile,unittest
from pathlib import Path
from scripts.person_directory import metadata,outputs,period_assignments

def date(dynasty='晉',era='CE',value=300):
 return {'era':era,'era_year':value,'year':value if era=='CE'else 1-value,'year_numbering':'astronomical','references':[{'columns':{'dynasty':dynasty,'era_name':'原年號'}}]}
def holding(mode='grant',person='p',**kw):
 return {'id':'h','person_id':person,'mode':mode,'title':'官','effective_period':{'start':{'status':'source_event','normalized_date':date()}},'attestations':[],**kw}
class PersonDirectoryTests(unittest.TestCase):
 def test_names_and_preferences_keep_needed_locator_without_guessing(self):
  p={'id':'p','label':'謝朏','name_components':[]};self.assertEqual(metadata(p)['name_components'],[])
  p['name_components']=[{'id':'n','person_id':'p','surname':'裴','ming':'顗','quote':'完整原句','surname_basis':{'huge':'not needed'}}]
  p['preferred_name_component_readings']=[{'records':[{'record':{'id':'n','quote':'完整原句'}}]}]
  m=metadata(p);self.assertEqual(m['name_components'][0]['quote'],'完整原句');self.assertNotIn('surname_basis',m['name_components'][0]);self.assertEqual(p['name_components'][0]['ming'],'顗')
 def test_jiguan_only_two_relations_and_owner(self):
  p={'id':'p','addresses':[{'id':str(i),'person_id':'p','relation':r,'place':{'source_name':r}}for i,r in enumerate(['biographical_origin','native_place','birth_place','residence','burial_place','ancestral_origin'])]}
  p['addresses'].append({'person_id':'other','relation':'native_place','place':{'source_name':'他人'}})
  self.assertEqual([x['value']for x in metadata(p)['jiguan']],['biographical_origin','native_place'])
 def test_owned_live_title_dates_and_source_slots(self):
  h=holding();h['attestations']=[{'normalized_date':date(),'usage':'narrative'}]
  result=period_assignments({'id':'p','titles':[h,holding(person='other')]});self.assertEqual(len(result),1);self.assertEqual(result[0]['record_ids'],['h']);self.assertEqual({x['slot']for x in result[0]['record_refs']},{'start','attestation'});self.assertEqual(result[0]['record_refs'][0]['era_year'],300)
 def test_posthumous_unassumed_and_proposal_not_activity(self):
  for h in [holding('posthumous_grant'),holding(assumed=False),holding(appointment_basis={'assumed':False}),holding(service_status='not_assumed')]:self.assertEqual(period_assignments({'id':'p','titles':[h]}),[])
  self.assertEqual(period_assignments({'id':'p','titles':[holding()],'title_proposals':[{'person_id':'p','title':'官','outcome':'not_assumed'}]}),[])
 def test_selected_life_date_not_competing_or_parent(self):
  events=[{'id':'a','person_id':'p','event_type':'death','normalized_date':date('宋')},{'id':'b','person_id':'p','event_type':'death','normalized_date':date('魏')},{'id':'parent','person_id':'other','event_type':'death','normalized_date':date('唐')}]
  dec={'person_ids':['p'],'event_type':'death','candidate_event_ids':['a','b'],'preferred_event_id':'a','status':'editorial_provisional'}
  self.assertEqual([x['value']for x in period_assignments({'id':'p','life_events':events,'life_event_date_decisions':[dec]})],['宋']);dec['preferred_event_id']=None;self.assertEqual(period_assignments({'id':'p','life_events':events,'life_event_date_decisions':[dec]}),[])
 def test_bce_not_positive_ce_and_bad_numbers_rejected(self):
  e={'id':'e','person_id':'p','event_type':'death','normalized_date':date('秦','BCE',210)}
  result=period_assignments({'id':'p','life_events':[e]});self.assertEqual(result[0]['record_refs'][0]['year'],-209);self.assertEqual(result[0]['record_refs'][0]['era'],'BCE')
  for v in [True,-210,0]:e['normalized_date']['era_year']=v;self.assertEqual(period_assignments({'id':'p','life_events':[e]}),[])
 def test_unknown_and_full_profile_coverage_fail_closed(self):
  with tempfile.TemporaryDirectory()as td:
   r=Path(td);(r/'registry').mkdir();(r/'data/corpus/profiles').mkdir(parents=True);(r/'registry/persons.json').write_text(json.dumps({'persons':[{'id':'p'}]}));(r/'data/corpus/profiles/index.json').write_text(json.dumps({'profiles':[{'id':'p'}]}))
   with self.assertRaises(ValueError):outputs(r)
   (r/'data/corpus/profiles/p.json').write_text(json.dumps({'id':'p','canonical_person_id':'p','label':'不拆姓'}));a=outputs(r);self.assertEqual(a,outputs(r));row=json.loads(next(iter(a.values())))['persons']['p'];self.assertEqual(row['name_components'],[]);self.assertEqual(row['period_assignments'],[]);self.assertNotIn('default_title',row)
if __name__=='__main__':unittest.main()
