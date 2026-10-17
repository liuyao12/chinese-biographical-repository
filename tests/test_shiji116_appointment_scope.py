import copy,json,unittest
from pathlib import Path
from scripts import validate_corpus as module
from scripts.person_bundle import bundle
from scripts.table_evidence import load_tables,table_regnal_range_errors
R=Path(__file__).resolve().parents[1]
C=json.loads((R/'corpus/shiji/116.json').read_text());P=next(p for p in C['annotation']['title_proposals']if p['id']=='tp-shiji116-duotong-son');PEOPLE={p['id']for p in json.loads((R/'registry/persons.json').read_text())['persons']}
class AppointmentScope(unittest.TestCase):
 def test_actual_received_agreement_is_accepted_as_not_reported(self):self.assertEqual(module.title_proposal_errors(P,C,PEOPLE),[])
 def test_outcome_cannot_turn_into_actual_grant_or_false_non_enactment(self):
  for outcome in ['grant','not_enacted']:
   p=copy.deepcopy(P);p['outcome']=outcome;self.assertIn('任官約定須保存實行情況未載',module.title_proposal_errors(p,C,PEOPLE))
 def test_forged_or_missing_role_anchor_is_rejected(self):
  for value in [None,dict(P['role_anchor'],start=1),dict(P['role_anchor'],surface='王')]:
   p=copy.deepcopy(P);p['role_anchor']=value;self.assertTrue(module.title_proposal_errors(p,C,PEOPLE))
 def test_person_cannot_be_swapped_to_father(self):
  p=copy.deepcopy(P);p['person_id']='98i_dd4_aof';self.assertIn('稱號提議人物錨點不符',module.title_proposal_errors(p,C,PEOPLE))
 def test_agreement_cannot_be_omitted_or_borrowed_outside_quoted_scope(self):
  for variant in ['missing','short_quote','wrong_term']:
   p=copy.deepcopy(P)
   if variant=='missing':p.pop('agreement_anchor')
   elif variant=='short_quote':p['evidence'][0]['quote']='使其子為令'
   else:p['agreement_anchor']['surface']='拜'
   self.assertTrue(module.title_proposal_errors(p,C,PEOPLE))
 def test_existing_explicit_unenacted_proposals_remain_valid(self):
  total=0
  for path in (R/'corpus').glob('*/*.json'):
   if not path.stem.isdigit():continue
   chapter=json.loads(path.read_text())
   for p in chapter['annotation'].get('title_proposals',[]):self.assertEqual(module.title_proposal_errors(p,chapter,PEOPLE),[],p['id']);total+=1
  self.assertGreater(total,0)
 def test_arrangement_is_not_exported_as_a_held_title(self):
  p=bundle('98i_dd4_aof_A',R);self.assertFalse(any(h['title']=='令'for h in p['title_holdings']));self.assertTrue(any(x['id']==P['id']and x['outcome']=='not_reported'for x in p['title_proposals']));self.assertTrue(any(a['predicate']=='father'and a['object_person_id']=='98i_dd4_aof'for a in p['relations']))
 def test_xiangru_usage_does_not_inherit_tangmeng_background_year(self):
  h=next(h for h in json.loads((R/'corpus/shiji/116-titles.json').read_text())['holdings']if h['id']=='th-shiji116-010');self.assertEqual(h['effective_period']['start']['status'],'unknown');self.assertTrue(all(a['date_expression']is None for a in h['attestations']));self.assertIn('使相如以郎中將往喻',h['evidence'][0]['quote'])
 def test_tangmeng_actual_grant_preserves_tenth_month_year_window(self):
  h=next(h for h in json.loads((R/'corpus/shiji/116-titles.json').read_text())['holdings']if h['id']=='th-shiji116-007');s=h['effective_period']['start'];self.assertEqual(h['mode'],'grant');self.assertNotIn('normalized_date',s);self.assertEqual([s['normalized_date_range'][k]['era_year']for k in ['earliest','latest']],[136,135]);self.assertEqual(table_regnal_range_errors(s['normalized_date_range'],s['date_expression'],load_tables(R)),[])
 def test_missing_title_does_not_crash_or_validate_arrangement(self):
  p=copy.deepcopy(P);p['title']=None;self.assertTrue(module.title_proposal_errors(p,C,PEOPLE))
if __name__=='__main__':unittest.main()
