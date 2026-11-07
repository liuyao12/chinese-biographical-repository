"""Actual-root finite date successor tests; no thin root or candidate API substitution."""
import copy,json,unittest
from pathlib import Path
from scripts import fixed_jin098_wangdun_career as owner
from scripts import fixed_jin098_wangdun_comparison as core
from scripts import fixed_jin098_wangdun_career_dates as bridge
from scripts.received_career_roles import holding_valid,detail_valid
from scripts.validate_corpus import title_proposal_errors,normalized_date_errors
ROOT=Path(__file__).resolve().parents[1]
class CareerDates(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.ch=owner.read(ROOT,owner.CH);cls.roles,cls.t=owner.prepared(cls.ch,ROOT);cls.hs=cls.t['title_record']['holdings'];cls.ds=cls.t['detail_record']['records'];cls.qs=cls.t['annotation']['title_proposals'];cls.pids={p['id']for p in owner.read(ROOT,'registry/persons.json')['persons']}
 def test_two_initial_outer_ranges_not_tenures(self):
  rows={h['id']:h for h in self.hs}
  for rid,expr,a,z in [('th-jin098-career-p002-10','永嘉初',307,313),('th-jin098-career-p004-25','建武初',317,317)]:
   h=rows[rid];self.assertTrue(holding_valid(h,self.ch,ROOT));s=h['effective_period']['start'];r=s['normalized_date_range'];self.assertEqual(s['date_expression'],expr);self.assertEqual(r['source_stage'],'初');self.assertEqual((r['earliest']['year'],r['latest']['year']),(a,z));self.assertNotIn('normalized_date',s);self.assertEqual(h['effective_period']['end'],{'status':'unknown','date_expression':None,'evidence':[]})
 def test_all_five_p018_events_322_dispatch(self):
  rows=[r for r in self.qs+self.ds if r['id']in bridge.TARGETS];self.assertEqual({r['id']for r in rows},set(bridge.TARGETS))
  for r in rows:
   role='title_proposal'if r['id'].startswith('tp-')else'source_detail';d=r['normalized_date'];self.assertEqual(d['year'],322);self.assertEqual(d['source_expression'],'永昌元年');self.assertEqual(d['event_evidence_binding']['date_anchor']['paragraph_id'],core.CID+':p011');self.assertEqual(d['event_evidence_binding']['target_anchor']['paragraph_id'],core.CID+':p018');self.assertEqual(normalized_date_errors(d,{self.ch['id']:self.ch},ROOT,r,role),[])
   if role=='title_proposal':self.assertEqual(title_proposal_errors(r,self.ch,self.pids,{},ROOT),[]);self.assertFalse(r['effective_service_attested']);self.assertFalse(holding_valid(r,self.ch,ROOT))
   else:self.assertTrue(detail_valid(r,self.ch,{},ROOT));self.assertFalse(r['values']['court_appointment_attested'])
 def test_prior_p011_privilege_no_backward_year(self):
  rows=[r for r in self.ds if r.get('source_career_role',{}).get('paragraph_id')==core.CID+':p011'];self.assertTrue(rows)
  for r in rows:
   self.assertNotIn('normalized_date',r);self.assertIsNone(r['date_expression']);x=copy.deepcopy(r);x['normalized_date']=copy.deepcopy(next(r for r in self.ds if r['id']==bridge.TARGETS[-1])['normalized_date']);x['date_expression']='永昌元年';self.assertFalse(detail_valid(x,self.ch,{},ROOT))
 def test_wrong_year_era_and_subject_rejected(self):
  r=next(r for r in self.ds if r['id']==bridge.TARGETS[-1])
  for key,value in [('year',324),('year',323),('year',True),('source_expression','太甯元年')]:
   n=copy.deepcopy(r['normalized_date']);n[key]=value;self.assertTrue(normalized_date_errors(n,{self.ch['id']:self.ch},ROOT,r,'source_detail'))
  x=copy.deepcopy(r);x['person_id']=self.roles['dao'];self.assertFalse(detail_valid(x,self.ch,{},ROOT));self.assertTrue(normalized_date_errors(x['normalized_date'],{self.ch['id']:self.ch},ROOT,x,'source_detail'))
 def test_wrong_chain_and_missing_quotation_rejected(self):
  r=next(r for r in self.ds if r['id']==bridge.TARGETS[-1])
  for kind in ['date_anchor','chain','quote']:
   x=copy.deepcopy(r);d=x['normalized_date']
   if kind=='date_anchor':d['event_evidence_binding']['date_anchor']['paragraph_id']=core.CID+':p019'
   elif kind=='chain':d['event_evidence_binding']['complete_chain_paragraph_ids'].pop(2)
   else:d['evidence'].pop(0)
   self.assertFalse(detail_valid(x,self.ch,{},ROOT));self.assertTrue(normalized_date_errors(d,{self.ch['id']:self.ch},ROOT,x,'source_detail'))
 def test_ranges_cannot_be_changed_or_confirmed_dates(self):
  for h in self.hs:
   if 'normalized_date_range'not in h['effective_period']['start']:continue
   for kind in ['range','exact','end']:
    x=copy.deepcopy(h)
    if kind=='range':x['effective_period']['start']['normalized_date_range']['latest']['year']+=1
    elif kind=='exact':x['effective_period']['start']['normalized_date']={'year':317}
    else:x['effective_period']['end']={'status':'source_event','normalized_date':{'year':324}}
    self.assertFalse(holding_valid(x,self.ch,ROOT))
 def test_same_source_catalog_drift_rejected(self):
  r=next(r for r in self.ds if r['id']==bridge.TARGETS[-1]);bad=copy.deepcopy(self.ch);next(p for p in bad['paragraphs']if p['id']==core.CID+':p012')['text']+='改';self.assertTrue(normalized_date_errors(r['normalized_date'],{bad['id']:bad},ROOT,r,'source_detail'))
 def test_original_local_six_still_323(self):
  rows=[r for r in self.ds if r.get('normalized_date',{}).get('event_evidence_binding',{}).get('kind')=='fixed_jin098_career_local_year'];self.assertEqual(len(rows),6)
  for r in rows:self.assertEqual(r['normalized_date']['year'],323);self.assertEqual(normalized_date_errors(r['normalized_date'],{self.ch['id']:self.ch},ROOT,r,'source_detail'),[])
if __name__=='__main__':unittest.main()
