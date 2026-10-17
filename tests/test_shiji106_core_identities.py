import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(path):return json.loads((ROOT/path).read_text())
class CoreIdentities(unittest.TestCase):
 def test_letter_kings_match_same_event_named_edict(self):
  d=read('corpus/shiji/106-equivalences.json');expected=['yqp_nlb_p1p_ABE','yqp_nlb_p1p_ABG','yqp_nlb_p1p_ABD','yqp_nlb_p1p_AEA','yqp_nlb_p1p_DCA']
  for i,pid in enumerate(expected,1):
   a=next(a for a in d['decisions']if a['id']==f'eq-shiji106-internal-royal-{i:03d}');self.assertEqual(a['canonical_person_id'],pid);self.assertEqual(a['scope'],'same_chapter');self.assertTrue(a['identity_materialized']);self.assertTrue(any(e['paragraph_id'].endswith('p009')for e in a['evidence']));self.assertTrue(any(e['paragraph_id'].endswith('p016')for e in a['evidence']))
 def test_zhou_yafu_and_child_share_attested_zhoubo_root(self):
  rows=read('corpus/shiji/057-assertions.json')['assertions'];a=next(a for a in rows if a['id']=='a-shiji057-002');self.assertEqual(a['object_person_id'],'koy_6jg_gcc');self.assertTrue(a['subject_person_id'].startswith('koy_6jg_gcc_'));b=next(b for b in rows if b['id']=='a-shiji057-008');self.assertEqual(b['object_person_id'],a['subject_person_id']);self.assertTrue(b['subject_person_id'].startswith(a['subject_person_id']));self.assertEqual(len(b['subject_person_id']),len(a['subject_person_id'])+1);person=next(p for p in read('registry/persons.json')['persons']if p['id']==b['subject_person_id']);self.assertEqual(person['family_path']['parent_person_id'],a['subject_person_id']);self.assertNotIn('birth_order',a['qualifiers'])
 def test_retired_candidates_have_no_registry_or_public_alias_files(self):
  retired=['lbk_uyq_t6e','xx0_5ue_hl1','6zw_vkw_sxz','xky_ebm_pdy','syn_6p6_j5m','t3i_l5f_u0p','68g_980_mer','v4x_3qx_dy7','ddd_32x_k8h','i37_l7b_6n8','iv3_1c9_df4','fn4_s0b_4jd','y1q_rxv_87u','nwx_f88_xfu','nwx_f88_xfu_A','u6m_zsb_0ps'];ids={p['id']for p in read('registry/persons.json')['persons']}
  for pid in retired:self.assertNotIn(pid,ids);self.assertFalse((ROOT/'data/corpus/profiles'/f'{pid}.json').exists());self.assertFalse((ROOT/'exports/persons'/f'{pid}.json').exists())
