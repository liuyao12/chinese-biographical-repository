import copy,json,unittest
from pathlib import Path
from scripts.song047_title_semantics import imperial_gift_valid,elided_decline_valid,unresolved_title_errors
from scripts.posthumous_gifts import posthumous_gift_valid
R=Path(__file__).resolve().parents[1]
class Song047TitleTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=json.loads((R/'corpus/songshu/047-liuhuaisu.json').read_text());cls.h={h['id']:h for h in json.loads((R/'corpus/songshu/047-liuhuaisu-titles.json').read_text())['holdings']}
  cls.ps={p['id']:(cls.c['id'],p)for p in cls.c['paragraphs']};cls.ms={m['id']:(cls.c['id'],p['id'],m)for p in cls.c['paragraphs']for m in p['mentions']}
  cls.life={e['id']:e for e in json.loads((R/'corpus/songshu/047-liuhuaisu-life-events.json').read_text())['events']}
 def test_all_seventy_two_are_accounted_and_never_invent_tenure(self):
  receipt=json.loads((R/'source-evidence/song047-liuhuaisu-recovery/title-native-consumption.json').read_text())
  self.assertEqual(len(receipt['records']),72);self.assertEqual(len({r['proposal_id']for r in receipt['records']}),72)
  source_titles=[h for h in self.h.values()if h.get('source_proposal_id')]
  self.assertEqual(len(source_titles),69);self.assertEqual(sum(len(h['attestations'])for h in source_titles),70)
  self.assertEqual(len(self.c['annotation']['title_proposals']),2)
  for h in self.h.values():self.assertEqual(h['effective_period']['end'],{'status':'unknown','date_expression':None,'evidence':[]})
  for n in(54,55,62,63,70):self.assertIsNone(self.h[f'th-song047-{n:03d}']['effective_period']['start']['date_expression'])
  self.assertNotIn('th-song047-056',self.h);self.assertNotIn('th-song047-057',self.h);self.assertNotIn('th-song047-008',self.h)
 def test_declined_both_roles_and_negative_recipient_role_quote(self):
  for row in self.c['annotation']['title_proposals']:
   self.assertTrue(elided_decline_valid(row,self.c))
   for mutation in('person','role','refuser','quote'):
    a=copy.deepcopy(row)
    if mutation=='person':a['person_id']='olf_c6j_hmg'
    if mutation=='role':a['role_anchor']=a['elided_appointment_context']['first_title_anchors'][0]
    if mutation=='refuser':a['elided_appointment_context']['refusing_mention_id']=a['elided_appointment_context']['first_recipient_mention_id']
    if mutation=='quote':a['evidence'][0]['quote']+='改'
    self.assertFalse(elided_decline_valid(a,self.c),mutation)
 def test_unresolved_not_assigned_and_negative_cases(self):
  pids={m.get('person_id')for _,_,m in self.ms.values()}|{'q7q_j3y_nhj'}
  self.assertEqual(unresolved_title_errors(self.c,pids),[])
  for mutation in('person','candidate','case','position'):
   c=copy.deepcopy(self.c);a=c['annotation']['unresolved_title_attestations'][0]
   if mutation=='person':a['person_id']='q7q_j3y_nhj'
   if mutation=='candidate':a['candidate_person_ids']=[]
   if mutation=='case':a['identity_case_id']='missing'
   if mutation=='position':a['title_anchor']['end']+=1
   self.assertTrue(unresolved_title_errors(c,pids),mutation)
 def test_posthumous_actual_source_and_negative_contracts(self):
  for n in(62,63,70):
   h=self.h[f'th-song047-{n:03d}'];self.assertTrue(posthumous_gift_valid(h,self.ps,self.ms,self.life),n)
   for mutation in('person','quote','grant','date','revision'):
    x=copy.deepcopy(h)
    if mutation=='person':x['person_id']='olf_c6j_hmg'
    if mutation=='quote':x['posthumous_basis']['source_term']+='改'
    if mutation=='grant':x['posthumous_basis']['grant_anchor']['start']+=1
    if mutation=='date':x['effective_period']['start']['date_expression']='十九年'
    if mutation=='revision':x['posthumous_basis']['source_revision']='wrong'
    self.assertFalse(imperial_gift_valid(x,self.ps,self.ms,self.life),(n,mutation))
  x=copy.deepcopy(self.h['th-song047-062']);x['posthumous_basis']['recipient_pairs'].reverse();self.assertFalse(imperial_gift_valid(x,self.ps,self.ms,self.life))
  x=self.h['th-song047-070'];self.assertFalse(imperial_gift_valid(x,self.ps,self.ms,{}))
  life=copy.deepcopy(self.life);life['le-song047-jiangdaosheng-death']['person_id']='olf_c6j_hmg';self.assertFalse(imperial_gift_valid(x,self.ps,self.ms,life))
 def test_date_scope_is_narrow(self):
  self.assertEqual(self.h['th-song047-035']['effective_period']['start']['normalized_date']['year'],437)
  for n in range(37,46):self.assertEqual(self.h[f'th-song047-{n:03d}']['attestations'][0]['normalized_date']['year'],442)
  for n in range(46,56):self.assertNotIn('normalized_date',self.h[f'th-song047-{n:03d}']['attestations'][0])
  for n in(26,27):
   a=self.h[f'th-song047-{n:03d}']['attestations'][0];self.assertEqual(a['normalized_date_range']['earliest']['year'],465);self.assertNotIn('normalized_date',a)
if __name__=='__main__':unittest.main()
