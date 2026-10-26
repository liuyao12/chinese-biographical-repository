import copy,json,unittest
from pathlib import Path
from scripts.wyd_song044_nobles import records,holding_valid,proposal_errors
from scripts.received_career_roles import holding_valid as career_valid
from scripts.validate_corpus import title_proposal_errors
from scripts.wyd_song044_formal_roles import source_errors
ROOT=Path(__file__).resolve().parents[1]
class NobleTests(unittest.TestCase):
 def setUp(self):
  self.ch=json.loads((ROOT/'corpus/songshu/044-wyd1739.json').read_text());self.h,self.q=records(self.ch);self.pids={self.h['person_id']}
 def test_actual_grant_and_unknown_acceptance(self):
  self.assertTrue(career_valid(self.h,self.ch));self.assertEqual(title_proposal_errors(self.q,self.ch,self.pids),[])
  self.assertEqual(self.h['reported_households']['value'],2000);self.assertEqual(self.q['reported_households']['value'],4000)
  self.assertFalse(holding_valid(self.q,self.ch));self.assertEqual(source_errors(self.ch,ROOT),[])
 def test_no_invented_dates_or_termination(self):
  self.assertEqual(self.h['effective_period']['start']['date_expression'],'永初元年');self.assertEqual(self.h['effective_period']['end'],{'status':'unknown','date_expression':None,'evidence':[]})
  for path,value in [('date_expression','426'),('outcome','not_assumed'),('acceptance_status','accepted'),('appointment_issued',False),('effective_service_attested',True),('human_reviewed',True)]:
   q=copy.deepcopy(self.q);q[path]=value;self.assertTrue(title_proposal_errors(q,self.ch,self.pids),path)
  h=copy.deepcopy(self.h);h['effective_period']['end']['date_expression']='426';self.assertFalse(career_valid(h,self.ch))
 def test_count_role_and_offered_status_not_interchangeable(self):
  for value in [4000,0,None]:
   h=copy.deepcopy(self.h);h['reported_households']['value']=value;self.assertFalse(career_valid(h,self.ch))
  q=copy.deepcopy(self.q);q['reported_households']['scope']='actual_enfeoffment_allotment';self.assertTrue(proposal_errors(q,self.ch,self.pids))
 def test_not_borrow_other_advancement(self):
  q=copy.deepcopy(self.q);q['appointment_anchor']['surface']='進號';self.assertTrue(title_proposal_errors(q,self.ch,self.pids))
  q=copy.deepcopy(self.q);q['reported_declination']['source_term']='固讓';self.assertTrue(proposal_errors(q,self.ch,self.pids))
 def test_subject_and_source_fail_closed(self):
  for field,value in [('person_id','wrong'),('person_mention_id','wrong')]:
   q=copy.deepcopy(self.q);q[field]=value;self.assertTrue(proposal_errors(q,self.ch,self.pids))
  for mutate in [lambda c:c['source'].update(revision='wrong'),lambda c:c['paragraphs'][1].update(text='異'+c['paragraphs'][1]['text'])]:
   c=copy.deepcopy(self.ch);mutate(c)
   if c!=self.ch:self.assertFalse(holding_valid(self.h,c))
 def test_exact_role_kind_and_co_shift_rejected(self):
  c=copy.deepcopy(self.ch);p=next(p for p in c['paragraphs'] if p['id'].endswith('p002'));m=next(m for m in p['mentions'] if m['id'].endswith('m0269'));m['kind']='unresolved';self.assertFalse(holding_valid(self.h,c))
  c=copy.deepcopy(self.ch);p=c['paragraphs'][1];p['text']='字'+p['text']
  for m in p['mentions']:m['start']+=1;m['end']+=1
  self.assertFalse(holding_valid(self.h,c))
 def test_legal_all_reference_rekey(self):
  c=copy.deepcopy(self.ch);old=self.h['person_id'];new='abc_def_123'
  for p in c['paragraphs']:
   for m in p['mentions']:
    if m.get('person_id')==old:m['person_id']=new
  h,q=records(c);self.assertEqual(h['person_id'],new);self.assertTrue(career_valid(h,c));self.assertEqual(title_proposal_errors(q,c,{new}),[])
 def test_proposal_stripped_only_after_strict_validation(self):
  c=copy.deepcopy(self.ch);c['annotation']['title_proposals'][0]['reported_households']['value']=2000;self.assertTrue(source_errors(c,ROOT))
  c=copy.deepcopy(self.ch);c['annotation']['unknown_extra']=True;self.assertTrue(source_errors(c,ROOT))
 def test_malformed_direct_records(self):
  for c in [None,[],{},'bad']:
   self.assertFalse(holding_valid(self.h,c));self.assertTrue(proposal_errors(self.q,c,self.pids))
if __name__=='__main__':unittest.main()
