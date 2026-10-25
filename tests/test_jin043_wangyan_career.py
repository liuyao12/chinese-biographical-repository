"""Finite career source roles and nonservice boundaries, no mutations of native files."""
import copy,json,unittest
from pathlib import Path
from scripts.fixed_witness_fact_slots import records,valid
R=Path(__file__).resolve().parents[1]
class WangyanCareerTests(unittest.TestCase):
 def setUp(self):
  self.c=json.loads((R/'corpus/jinshu/043-wangyan.json').read_text());self.v={x['id']:x for x in records(self.c,R)}
 def test_refused_and_omitted_roles_never_become_holdings(self):
  hs=json.loads((R/'corpus/jinshu/043-wangyan-titles.json').read_text())['holdings'];self.assertEqual(len(hs),25)
  self.assertFalse({'遼東太守','武陵侯','元帥','荊州','青州','持節','假黃鉞'}&{h['title']for h in hs})
  self.assertEqual(next(h for h in hs if h['id'].endswith('career_19'))['title'],'吏部')
  self.assertTrue(all(h['effective_period']['end']['status']=='unknown'for h in hs))
 def test_consistent_wrong_recipient_in_same_paragraph_rejected(self):
  h=copy.deepcopy(self.v['th-jin043-wangyan-career_17']);p=self.c['paragraphs'][5];other=next(m for m in p['mentions']if m['surface']=='成都王穎');h['person_id']=other['person_id']
  for e in h['evidence']+h['effective_period']['start']['evidence']:e['person_mention_id']=other['id']
  for a in h['attestations']:a['person_mention_id']=other['id']
  self.assertFalse(valid(h,self.c,R))
 def test_272_only_nomination_not_later_service_or_death(self):
  q=self.v['sd-jin043-wangyan-career_03'];self.assertEqual(q['normalized_date']['year'],272);self.assertFalse(q['values']['holding_created']);self.assertEqual(q['values']['appointment_stage'],'recommendation')
  h=copy.deepcopy(self.v['th-jin043-wangyan-career_04']);h['effective_period']['start']['normalized_date']=copy.deepcopy(q['normalized_date']);h['effective_period']['start']['date_expression']='泰始八年';self.assertFalse(valid(h,self.c,R))
  q=copy.deepcopy(q);q['normalized_date']['year']=273;self.assertFalse(valid(q,self.c,R))
 def test_refusal_cannot_be_relabelled_grant_and_old22_remain(self):
  v=copy.deepcopy(self.v['sd-jin043-wangyan-career_30']);v.update(title='武陵侯',kind='noble_rank',mode='grant');v['values']['holding_created']=True;self.assertFalse(valid(v,self.c,R))
  self.assertEqual(len([v for v in self.v.values()if v.get('age_context')]),2)
  self.assertTrue(all('normalized_date'not in v for v in self.v.values()if v.get('event_type')=='death'))
if __name__=='__main__':unittest.main()
