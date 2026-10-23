import unittest,json,copy
from pathlib import Path
from scripts.fixed_witness_fact_slots import records,valid,errors,grammar,KIND
ROOT=Path(__file__).resolve().parents[1]
class WitnessFacts(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.ch=json.loads((ROOT/'corpus/jinshu/093-yangxiu.json').read_text());cls.rows=records(cls.ch,ROOT);cls.by={v['fixed_source_fact_binding']['slot']:v for v in cls.rows}
 def test_all_slots_and_source_roles(self):
  self.assertEqual(len(self.rows),36)
  for v in self.rows:self.assertTrue(valid(v,self.ch,ROOT),v['id'])
  self.assertNotEqual(self.by['father-taichang']['person_id'],self.by['zhonghujun-first']['person_id'])
 def reject(self,slot,change):
  x=copy.deepcopy(self.by[slot]);change(x);self.assertFalse(valid(x,self.ch,ROOT))
 def test_wrong_recipient_all_evidence_coherent(self):
  def change(x):
   x['person_id']=self.by['father-taichang']['person_id']
   for e in x['evidence']:e['person_mention_id']=self.by['father-taichang']['evidence'][0]['person_mention_id']
   for a in x['attestations']:a['person_mention_id']=self.by['father-taichang']['evidence'][0]['person_mention_id']
  self.reject('zhonghujun-first',change)
 def test_thirteen_not_episode_or_date(self):
  self.reject('thirteen-years',lambda x:x['values'].update(duration_years=10))
  self.reject('thirteen-years',lambda x:x['values'].update(episode_assignment='first_only'))
  self.reject('thirteen-years',lambda x:x.update(normalized_date={'year':265}))
 def test_playful_request_not_tenure(self):self.reject('playful-future-request',lambda x:x['values'].update(actual_tenure=True))
 def test_unknown_death_not_dated(self):self.reject('death',lambda x:x.update(normalized_date={'year':283}))
 def test_death_not_borrowed_for_all_offices(self):self.reject('zuowei',lambda x:x['effective_period'].update(end={'status':'source_event','event_type':'explicit_end','date_expression':'卒','evidence':self.by['death']['evidence']}))
 def test_gifts_no_burial(self):self.reject('posthumous-gift-order',lambda x:x['values'].update(actual_burial_event=True))
 def test_no_named_affinity(self):self.reject('imperial-kinship-appellation',lambda x:x['values'].update(specified_relation='father_in_law'))
 def test_missing_duplicate_and_moved_slots(self):
  r=dict(record_type='mixed',chapter_id=self.ch['id'],records=self.rows)
  self.assertFalse(errors(ROOT,[self.ch,r]))
  for vs in [self.rows[:-1],self.rows+[self.rows[0]]]:self.assertTrue(errors(ROOT,[self.ch,dict(r,records=vs)]))
 def test_all_roles_can_be_coherently_rekeyed(self):
  c=copy.deepcopy(self.ch);mapping={m['person_id']:'test_'+m['person_id']for p in c['paragraphs']for m in p['mentions']if m['kind']=='person'}
  for p in c['paragraphs']:
   for m in p['mentions']:
    if m['kind']=='person':m['person_id']=mapping[m['person_id']]
  for v in records(c,ROOT):self.assertTrue(valid(v,c,ROOT))
 def test_role_layer_and_marked_span_rejected(self):
  for kind in ['annotator','text_layer','shift']:
   c=copy.deepcopy(self.ch);p=c['paragraphs'][0]
   if kind=='annotator':p['annotator']='裴松之'
   elif kind=='text_layer':p['text_layer']='commentary'
   else:p['mentions'][0]['start']+=1
   with self.assertRaises((AssertionError,ValueError,KeyError)):grammar(c,ROOT)
if __name__=='__main__':unittest.main()
