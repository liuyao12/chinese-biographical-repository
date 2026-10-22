"""Real native source operands exercise the production date contracts."""
import copy,json,unittest
from pathlib import Path
from scripts import source_office_reports as o,source_office_dates as d
from scripts.validate_corpus import normalized_date_errors
R=Path(__file__).resolve().parents[1]
class SourceOfficeDates(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.ch=json.loads((R/'corpus/sanguozhi/022-chenqun-chentai.json').read_text());j=json.loads((R/'corpus/sanguozhi/022-chenqun-chentai-titles.json').read_text());cls.hs={h['id']:h for h in j['holdings']};cls.changed=[h for h in j['holdings']if'source_office_date_binding'in h];cls.detail=next(x for x in json.loads((R/'corpus/sanguozhi/022-chentai-source-details.json').read_text())['records']if'date_observation'in x)
 def test_production_eight_holdings(self):
  self.assertEqual(len(self.changed),8)
  for h in self.changed:self.assertTrue(o.holding_role_valid(h,self.ch,self.hs,R),h['id'])
 def test_production_duty(self):self.assertTrue(o.detail_valid(self.detail,self.ch,self.hs,R))
 def test_normalized_dates_production(self):
  for h in self.changed:
   for role,v in [('start',h['effective_period']['start'].get('normalized_date')),('attestation',h['attestations'][0].get('normalized_date'))]:
    if v:self.assertEqual(normalized_date_errors(v,{self.ch['id']:self.ch},R,h,role),[],h['id'])
 def item(self,kind):return copy.deepcopy(next(h for h in self.changed if h['source_office_date_binding']['kind']==kind))
 def invalid(self,h):self.assertFalse(o.holding_role_valid(h,self.ch,self.hs,R))
 def test_era_not_first_or_middle_year(self):
  h=self.item('source_named_era_phase');h['effective_period']['start']['normalized_date_range']['earliest']['year']+=1;self.invalid(h)
 def test_no_phase_carry_to_following_office(self):
  h=copy.deepcopy(next(h for h in self.hs.values()if h['id']=='th-sgz022-chentai-office-03'));h['source_office_date_binding']=copy.deepcopy(self.changed[0]['source_office_date_binding']);self.invalid(h)
 def test_wrong_ruler_or_subject(self):
  h=self.item('dead_predecessor_successor');h['source_office_date_binding']['native_roles']['subject_full']=h['source_office_date_binding']['native_roles']['predecessor_full'];self.invalid(h)
 def test_death_year_not_next_year(self):
  h=self.item('dead_predecessor_successor');h['effective_period']['start']['normalized_date']['year']=256;self.invalid(h)
 def test_death_day_not_appointment_day(self):
  h=self.item('dead_predecessor_successor');h['effective_period']['start']['normalized_date']['day']='癸未';self.invalid(h)
 def test_no_death_tenure_end(self):
  h=self.item('dead_predecessor_successor');h['effective_period']['end']['normalized_date']={'year':260};self.invalid(h)
 def test_wrong_sha(self):
  h=self.item('dead_predecessor_successor');h['source_office_date_binding']['proofs'][0]['sha256']='0'*64;self.invalid(h)
 def test_wrong_event_offset(self):
  h=self.item('dead_predecessor_successor');h['source_office_date_binding']['proofs'][-1]['anchors']['actor']['start']+=1;self.invalid(h)
 def test_249_joint_not_initial_equals_first(self):
  h=self.item('phase_and_in_office_upper');self.assertEqual(h['effective_period']['start']['normalized_date']['year'],249);self.assertEqual(h['source_office_date_binding']['era_phase_range']['latest']['year'],254);h['source_office_date_binding']['joint_inference']['not_equating_phase_with_year_one']=False;self.invalid(h)
 def test_249_wrong_upper_actor(self):
  h=self.item('phase_and_in_office_upper');h['source_office_date_binding']['proofs'][0]['anchors']['actor']['quote']='郭淮';self.invalid(h)
 def test_observed_255_not_tenure_start(self):
  h=self.item('battle_in_office_observation');self.assertEqual(h['effective_period']['start']['status'],'unknown');h['effective_period']['start']=dict(status='source_event',event_type='grant',date_expression=None,evidence=h['evidence'],normalized_date=h['attestations'][0].pop('normalized_date'));self.invalid(h)
 def test_wrong_battle_participant(self):
  h=self.item('battle_in_office_observation');b=h['source_office_date_binding'];b['native_roles']['opponent']=b['native_roles']['defeated'];self.invalid(h)
 def test_huabei_remains_unknown(self):
  for n in(17,18,19):
   h=self.hs['th-sgz022-chentai-office-'+str(n)];self.assertNotIn('normalized_date',h['effective_period']['start']);self.assertNotIn('source_office_date_binding',h)
 def test_duty_not_duration(self):
  x=copy.deepcopy(self.detail);x['date_observation']['duration']=True;self.assertFalse(o.detail_valid(x,self.ch,self.hs,R))
 def test_duty_not_tenure(self):
  x=copy.deepcopy(self.detail);x['date_observation']['tenure_boundary']=True;self.assertFalse(o.detail_valid(x,self.ch,self.hs,R))
 def test_duty_not_all_257(self):
  x=copy.deepcopy(self.detail);x['date_observation']['latest']=257;self.assertFalse(o.detail_valid(x,self.ch,self.hs,R))
 def test_duty_wrong_subject(self):
  x=copy.deepcopy(self.detail);x['date_observation']['native_roles']['subject']=x['date_observation']['native_roles']['rebel'];self.assertFalse(o.detail_valid(x,self.ch,self.hs,R))
 def test_wrong_root_cannot_read_another_tree(self):
  h=self.item('dead_predecessor_successor');self.assertFalse(o.holding_role_valid(h,self.ch,self.hs,R/'missing-root'))
 def test_cut_full_annal_context(self):
  h=self.item('dead_predecessor_successor');b=h['source_office_date_binding'];b['proofs'][-1]['context']['end']=b['proofs'][-1]['anchors']['event']['end'];b['proofs'][-1]['context']['quote']=b['proofs'][-1]['context']['quote'][:b['proofs'][-1]['context']['end']-b['proofs'][-1]['context']['start']];self.invalid(h)
 def test_wrong_predecessor(self):
  h=self.item('dead_predecessor_successor');b=h['source_office_date_binding'];b['native_roles']['predecessor_full']=b['native_roles']['subject_full'];self.invalid(h)
 def test_mixed_exact_and_range(self):
  h=self.item('source_named_era_phase');h['effective_period']['start']['normalized_date']={'year':235};self.invalid(h)
 def test_changed_frame_term(self):
  h=self.item('dead_predecessor_successor');h['source_office_date_binding']['source_term']='代為征西將軍';self.invalid(h)
if __name__=='__main__':unittest.main()
