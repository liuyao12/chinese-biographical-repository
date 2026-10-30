"""Normal core-loop orchestration with synthetic catalog transport, not historical evidence."""
import json,tempfile,unittest,copy
from pathlib import Path
from unittest.mock import patch
from scripts import export_person_bundles as e,calendar_wiring,validate_corpus,reading_catalog,table_person_profiles,formal_source_citations

class FlowTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
  self.base=Path(self.temp.name);self.root=self.base/'source';self.root.mkdir();self.cp=self.base/'checkpoint'
  (self.root/'registry').mkdir();(self.root/'registry/persons.json').write_text('{}')
  self.ids=['aaa_aaa_aaa','bbb_bbb_bbb','ccc_ccc_ccc','ddd_ddd_ddd']
  self.people={pid:{'id':pid,'label':'明確測試人物'+pid,'aliases':[],'evidence':[]}for pid in self.ids}
  self.people[self.ids[0]]['id_aliases']=['eee_eee_eee'];self.calls=[]
 def result(self,pid):return {'record_type':'person_source_bundle','requested_person_id':pid,'person_ids':[pid],'identity_policy':{},'family_tree_decisions':[],'source_mention_summary':[],'mentions':[],'table_occurrences':[],'sources':[],'most_mentioned_source_ids':[]}
 def run_export(self,checkpoint=False,resume=False,interrupt=None,downstream=False):
  def bundle(pid,**kwargs):
   self.calls.append(pid)
   if interrupt is not None and len(self.calls)==interrupt:raise RuntimeError('simulated interrupt before bundle completion')
   return self.result(pid)
  if downstream:
   path=self.root/'data/historical-tables/person-candidates.json';path.parent.mkdir(parents=True,exist_ok=True);path.write_text('{}')
  with patch.object(e,'load_catalog',return_value=(self.people,[])),patch.object(e,'load_assemblies',return_value=({},{})),patch.object(e,'bundle',side_effect=bundle),patch.object(formal_source_citations,'load_citation_index',return_value={}),patch.object(calendar_wiring,'export_calendar_contexts')as cal,patch.object(validate_corpus,'validate',return_value=[])as validator,patch.object(reading_catalog,'run')as reader,patch.object(table_person_profiles,'build')as profiles:
   e.export(self.root,**({'checkpoint_dir':self.cp,'resume':resume,'checkpoint_batch_size':2}if checkpoint else {}))
   return {'validate':validator.call_count,'calendar':cal.call_count,'reader':reader.call_count,'profiles':profiles.call_count}
 def outputs(self):return {p.name:p.read_bytes()for p in (self.root/'exports/persons').iterdir()}
 def test_interrupted_resume_matches_complete_core_index_alias_and_rebuilds_alias(self):
  self.run_export();expected=self.outputs();self.calls=[]
  with self.assertRaises(RuntimeError):self.run_export(True,interrupt=4)
  self.calls=[];counts=self.run_export(True,True)
  self.assertEqual(self.outputs(),expected)
  self.assertEqual(self.calls,self.ids[2:]+[self.ids[0]]) # aliases always freshly bundled
  self.assertEqual(counts['validate'],1)
 def test_default_skips_new_validation_and_checkpoint_rebuilds_downstream(self):
  self.assertEqual(self.run_export(downstream=True),{'validate':0,'calendar':1,'reader':1,'profiles':1})
  self.calls=[];self.assertEqual(self.run_export(True,downstream=True),{'validate':1,'calendar':1,'reader':1,'profiles':1})
  self.calls=[];self.assertEqual(self.run_export(True,True,downstream=True),{'validate':1,'calendar':1,'reader':1,'profiles':1})
  self.assertEqual(self.calls,[self.ids[0]])
 def test_invalid_options_rejected_before_calendar_or_source_writes(self):
  for value in (True,0,65,32.0):
   with patch.object(calendar_wiring,'export_calendar_contexts')as cal:
    with self.assertRaises(ValueError):e.export(self.root,checkpoint_batch_size=value)
    cal.assert_not_called()
 def test_source_validation_failure_cannot_reuse_completed_outputs(self):
  self.run_export(True);self.calls=[]
  with patch.object(calendar_wiring,'export_calendar_contexts'),patch.object(validate_corpus,'validate',return_value=['real source guard rejected']):
   with self.assertRaisesRegex(ValueError,'real source guard rejected'):e.export(self.root,checkpoint_dir=self.cp,resume=True,checkpoint_batch_size=2)
  self.assertEqual(self.calls,[])

 def test_live_source_content_change_refuses_resume_before_any_bundle(self):
  self.run_export(True);self.calls=[]
  (self.root/'registry/persons.json').write_text('{"changed_source":true}')
  with self.assertRaises(ValueError):self.run_export(True,True)
  self.assertEqual(self.calls,[])
 def test_complete_uid_rekey_never_resurrects_previous_checkpoint_people(self):
  self.run_export(True);old=list(self.ids);self.calls=[]
  self.ids=['fff_fff_fff','ggg_ggg_ggg','hhh_hhh_hhh','iii_iii_iii']
  self.people={pid:{'id':pid,'label':'明確改號測試人物'+pid,'aliases':[],'evidence':[]}for pid in self.ids}
  self.people[self.ids[0]]['id_aliases']=['jjj_jjj_jjj']
  (self.root/'registry/persons.json').write_text(json.dumps({'persons':list(self.people.values())}))
  with self.assertRaises(ValueError):self.run_export(True,True)
  self.assertEqual(self.calls,[])
  self.cp=self.base/'new-checkpoint-after-rekey';self.run_export(True)
  actual=self.outputs();index=json.loads(actual['index.json'])
  self.assertEqual({r['person_id']for r in index['persons']},set(self.ids))
  for pid in old:self.assertNotIn(pid+'.json',actual)
  for pid in self.ids:self.assertEqual(json.loads(actual[pid+'.json'])['person_ids'],[pid])

if __name__=='__main__':unittest.main()
