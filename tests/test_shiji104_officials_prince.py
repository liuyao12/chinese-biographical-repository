import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class OfficialsPrince(unittest.TestCase):
 def test_royal_and_du_identities_are_materialized(self):
  c=json.loads((ROOT/'corpus/shiji/104.json').read_text());ms=[m for p in c['paragraphs'] for m in p['mentions']]
  for surface,pid in [('魯王','yqp_nlb_p1p_ACAL'),('御史大夫杜','dxx_6m8_7o6'),('太子','yqp_nlb_p1p_ACAAD')]:
   self.assertTrue(any(m['surface']==surface and m.get('person_id')==pid for m in ms))
  self.assertFalse({m.get('person_id')for m in ms}&{'ebi_jr2_aky','w8i_dhi_044','64t_pmo_3d4'})
 def test_bao_and_left_prime_keep_ids_with_commentary_names(self):
  reg=json.loads((ROOT/'registry/persons.json').read_text());labels={p['id']:p['label']for p in reg['persons']}
  self.assertIn('劉屈氂',labels['x8h_4i8_xwm']);self.assertIn('暴勝之',labels['qlq_xq2_1sm'])
  d=json.loads((ROOT/'corpus/shiji/104-identities.json').read_text())
  for pid in ['x8h_4i8_xwm','qlq_xq2_1sm']:
   r=next(r for r in d['decisions']if r.get('person_id')==pid)
   self.assertTrue(any(ref.get('revision_id')==2514774 for ref in r['references']))
   self.assertFalse(r['human_reviewed'])
 def test_disagreeing_actions_and_text_layers_remain(self):
  c=json.loads((ROOT/'corpus/shiji/104.json').read_text());p=next(p for p in c['paragraphs']if p['id'].endswith('p015'))
  self.assertIn('使御史大夫暴君下責丞相',p['text']);self.assertEqual(p['text_layer'],'witness_appended_chu_note')
  d=json.loads((ROOT/'corpus/shiji/104-identities.json').read_text());r=next(r for r in d['decisions']if r.get('person_id')=='qlq_xq2_1sm')
  self.assertTrue(any('御史大夫暴勝之謂丞相曰' in ref['quote']for ref in r['references']))
  self.assertIn('行動敘述不同',r['rationale'])
