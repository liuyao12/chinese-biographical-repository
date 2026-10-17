import json
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def load(p): return json.loads((ROOT/p).read_text())
class WeiqiContextIdentities(unittest.TestCase):
 def test_eight_materialized_decisions_keep_event_evidence(self):
  ds=[d for d in load('corpus/shiji/107-equivalences.json')['decisions'] if d['id'].startswith('eq-shiji107-context-')]
  self.assertEqual(len(ds),8)
  expected=['nuf_tb9_fjs_A','koy_6jg_gcc_C','ixk_6fg_v6f_A','8dt_22t_v15','wxo_k8i_1it','y6f_9v5_dqg','sj9_pfu_fwh','jo4_4bf_0ra_A']
  self.assertEqual([d['canonical_person_id'] for d in ds],expected)
  for d in ds:
   self.assertEqual(d['person_ids'],[d['canonical_person_id']]);self.assertTrue(d['identity_materialized']);self.assertFalse(d['human_reviewed'])
   self.assertEqual(len(d['evidence']),2);self.assertTrue(all(e['mention_ids'] for e in d['evidence']))
 def test_cousin_endpoint_is_father_not_ying(self):
  a=next(a for a in load('corpus/shiji/107-assertions.json')['assertions']if a['id']=='a-shiji107-016')
  self.assertEqual((a['subject_person_id'],a['predicate'],a['object_person_id']),('nuf_tb9_fjs','agnatic_cousin','ixk_6fg_v6f_A'))
  q=a['qualifiers'];self.assertEqual(q['source_term'],'從兄');self.assertEqual(q['kinship_structure']['generation_difference'],0);self.assertIsNone(q['kinship_structure']['common_ancestor_person_id']);self.assertIsNone(q['kinship_structure']['distance'])
  self.assertEqual(q['relative_birth_order']['older_person_id'],'nuf_tb9_fjs');self.assertEqual(q['relative_birth_order']['younger_person_id'],'ixk_6fg_v6f_A');self.assertIsNone(q['relative_birth_order']['older_ordinal']);self.assertIsNone(q['relative_birth_order']['younger_ordinal'])
 def test_yan_father_is_jia_by_commentary_not_reigning_king(self):
  ds=load('corpus/shiji/107-equivalences.json')['decisions'];d=next(d for d in ds if d['id']=='eq-shiji107-context-008');self.assertEqual(d['references'][0]['quote'],'蚡娶燕王劉澤子康王嘉之女也。');self.assertFalse(d['references'][0]['image_verified'])
  people=load('registry/persons.json')['persons'];daughter=next(p for p in people if p['label']=='田蚡夫人（燕康王女，未名）');self.assertEqual(daughter['family_path']['parent_person_id'],'jo4_4bf_0ra_A');self.assertTrue(daughter['id'].startswith('jo4_4bf_0ra_A'))
  assertions=load('corpus/shiji/107-assertions.json')['assertions'];father=next(a for a in assertions if a['id']=='a-shiji107-011');spouse=next(a for a in assertions if a['id']=='a-shiji107-012');self.assertEqual(father['subject_person_id'],daughter['id']);self.assertEqual(father['object_person_id'],'jo4_4bf_0ra_A');self.assertEqual(spouse['subject_person_id'],daughter['id']);self.assertEqual(spouse['object_person_id'],'7mz_d13_9ka_A')
 def test_dowager_ambiguity_still_has_two_candidates(self):
  c=load('corpus/shiji/107.json');p=next(p for p in c['paragraphs']if p['id'].endswith(':p007'));m=next(m for m in p['mentions']if m['surface']=='太后');self.assertIsNone(m['person_id'])
 def test_no_meng_ying_father_invented(self):
  a=load('corpus/shiji/107-assertions.json')['assertions'];father=next(x for x in a if x['id']=='a-shiji107-007');self.assertEqual(father['object_person_id'],'h1w_44g_vef');self.assertFalse(any(x['predicate']=='father' and x['subject_person_id']=='h1w_44g_vef' and x['object_person_id']=='sj9_pfu_fwh' for x in a))
 def test_nine_retired_ids_have_no_registry_or_exports(self):
  ids={p['id']for p in load('registry/persons.json')['persons']}
  for pid in ['nvf_r2k_j9y','tuo_3kv_ptz','l26_mjw_rwe','btq_wmp_kuw','vi0_7ws_jn8','f4q_d6m_ral','tfu_611_q19','fwk_g2h_l3r','fwk_g2h_l3r_A']:
   self.assertNotIn(pid,ids);self.assertFalse((ROOT/'exports/persons'/f'{pid}.json').exists());self.assertFalse((ROOT/'data/corpus/profiles'/f'{pid}.json').exists())
