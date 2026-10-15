# coding: utf-8
import json,hashlib,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OLD={'c4o_fny_0vd','mq3_lev_w2t','71k_260_g1p','ggi_5lp_87e','xu3_wem_5h3','9wx_3fi_zk2','r5o_rck_hff','c56_xgh_owp','01m_8vn_zqy','vnm_ppc_xjm','ilz_9fs_tfm','jvl_f6r_3bd','otl_2v4_mdf','wl3_jss_lix','nzi_rg8_uik','6in_5g6_f6d','krx_d9v_3wv'}
def read(p):return json.loads((ROOT/p).read_text())
def para(n):return next(p for p in read('corpus/shiji/099.json')['paragraphs'] if p['id'].endswith(':p'+f'{n:03d}'))
class LiushuContextTests(unittest.TestCase):
 def test_generation_comparison_remains_unresolved_after_huhai_merge(self):
  p=para(3);m=next(m for m in p['mentions'] if m['surface']=='秦二世')
  self.assertEqual((m['kind'],m['person_id'],m['status']),('unresolved',None,'unresolved'))
  case=next(x for x in read('corpus/shiji/099.json')['annotation']['unresolved_identity_cases'] if x['id']=='ic-shiji099-qin-two-generations')
  self.assertEqual(case['candidate_person_ids'],['ao3_0fy_d45_AAAA']);self.assertTrue(case['unknown_identity_possible']);self.assertFalse(case['candidate_list_exhaustive'])
 def test_explicit_emperor_and_huhai_are_same_person(self):
  self.assertEqual({m['person_id'] for m in para(8)['mentions'] if m['surface']=='二世'},{'ao3_0fy_d45_AAAA'})
  self.assertEqual({m['person_id'] for m in para(16)['mentions'] if m['surface']=='胡亥'},{'ao3_0fy_d45_AAAA'})
  p=next(p for p in read('registry/persons.json')['persons'] if p['id']=='ao3_0fy_d45_AAAA')
  self.assertFalse(any(e.get('mention_id')=='c-shiji-099-liushu:m003-0021' for e in p['evidence']))
 def test_chu_huai_is_xin_not_the_grandfather(self):
  self.assertEqual({m['person_id'] for m in para(8)['mentions'] if m['surface'] in ['懷王','義帝']},{'c2w_s7g_en0_*A'})
 def test_nested_jin_prince_is_not_han_prince_or_office_component(self):
  ms=[m for m in para(16)['mentions'] if m['surface']=='太子']
  self.assertIsNone(ms[0]['person_id']);self.assertIn('職名',ms[0]['note'])
  self.assertEqual(ms[2]['person_id'],'6di_ywz_ju4_AAB')
  self.assertTrue(all(m['person_id']=='yqp_nlb_p1p_AA' for i,m in enumerate(ms) if i not in [0,2]))
 def test_maodun_father_is_touman_and_hypothetical_children_stay_unknown(self):
  p=para(6);self.assertEqual({m['person_id'] for m in p['mentions'] if m['surface']=='父'},{'wjt_htu_081'})
  self.assertTrue(all(m.get('person_id') is None for m in p['mentions'] if m['surface'] in ['外孫','群母']))
 def test_sixteen_groups_retain_individual_source_evidence(self):
  ds=[d for d in read('corpus/shiji/099-equivalences.json')['decisions'] if d['id'].startswith('eq-shiji099-context-')]
  self.assertEqual(len(ds),16)
  for d in ds:
   self.assertTrue(d['identity_materialized']);self.assertGreaterEqual(len(d['chapter_ids']),2);self.assertFalse(d['human_reviewed'])
   self.assertTrue(all(e['quote'] and e['mention_ids'] for e in d['evidence']))
 def test_retired_candidates_are_absent(self):
  ids={p['id'] for p in read('registry/persons.json')['persons']};self.assertFalse(ids & OLD)
  for pid in OLD:
   for folder in ['data/corpus/profiles','exports/persons']:self.assertFalse((ROOT/folder/(pid+'.json')).exists())
