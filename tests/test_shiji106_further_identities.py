import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text())
class FurtherIdentities(unittest.TestCase):
 def test_eight_cross_chapter_decisions_are_materialized(self):
  rows=read('corpus/shiji/106-equivalences.json')['decisions'];rows=[a for a in rows if a['id'].startswith('eq-shiji106-further-')];self.assertEqual(len(rows),8)
  for a in rows:self.assertTrue(a['identity_materialized']);self.assertEqual(a['person_ids'],[a['canonical_person_id']]);self.assertGreaterEqual(len({e['chapter_id']for e in a['evidence']}),2)
 def test_qixiao_parent_is_explicit_and_shares_liu_root(self):
  a=next(a for a in read('corpus/shiji/052-assertions.json')['assertions']if a['id']=='a-shiji052-040');self.assertEqual(a['object_person_id'],'yqp_nlb_p1p_AB');self.assertTrue(a['subject_person_id'].startswith('yqp_nlb_p1p_AB'));self.assertIn('悼惠王子',a['qualifiers']['source_term']);p=next(p for p in read('registry/persons.json')['persons']if p['id']==a['subject_person_id']);self.assertEqual(p['family_path']['source_assertion_id'],a['id']);self.assertNotIn('birth_order',a['qualifiers'])
 def test_jingwang_is_ancestral_reference_not_current_xi(self):
  c=read('corpus/shiji/106.json');p=next(p for p in c['paragraphs']if p['id'].endswith('p006'));m=next(m for m in p['mentions']if m['surface']=='城陽景王');self.assertEqual(m['person_id'],'yqp_nlb_p1p_ABF');self.assertIn('城陽景王有義，攻諸呂',p['text'])
 def test_retired_candidates_and_old_qixiao_files_are_removed(self):
  retired=['1iv_bo2_ode','59b_c0s_5il','k2v_k0j_chh','hfn_aif_jww','doj_zhx_nm1','fwu_nkh_9qr','s3a_ah3_epn','l9w_b0y_aow','qa2_bme_epc','mvv_bou_spk','jc7_nxq_532'];ids={p['id']for p in read('registry/persons.json')['persons']}
  for pid in retired:self.assertNotIn(pid,ids);self.assertFalse((ROOT/'data/corpus/profiles'/f'{pid}.json').exists());self.assertFalse((ROOT/'exports/persons'/f'{pid}.json').exists())
