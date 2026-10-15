# coding: utf-8
import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RETIRED={'1ia_b4v_w14','0lb_ygj_t93','z5h_0si_ndg','qlm_m3s_f3b_A','pdn_whf_crz','anh_fih_n7i','j8g_yef_isr','gau_cq7_7g1','0sl_eh8_yhw','h69_ln7_f94','llf_tvb_j2l','qlm_m3s_f3b','iob_qd9_w2s','61g_cr5_n52','o2m_km9_b1w','qlm_m3s_f3b_B','zu4_zoq_n1q','gau_cq7_7g1_A','cxt_wg1_9qm','h69_ln7_f94_A','mpz_80p_uhj','a43_p6o_o49'}
def read(p):return json.loads((ROOT/p).read_text())
def para(n,key):return next(p for p in read('corpus/shiji/'+n+'.json')['paragraphs'] if p['id'].endswith(':'+key))
class JibuCoreFamilyTests(unittest.TestCase):
 def test_twelve_chapter_groups_and_five_family_groups_keep_source_evidence(self):
  ds=[d for n in ['040','100'] for d in read('corpus/shiji/'+n+'-equivalences.json')['decisions'] if d['id'].startswith('eq-shiji100-core-')]
  self.assertEqual(len(ds),17)
  for d in ds:
   self.assertTrue(d['identity_materialized']);self.assertFalse(d['human_reviewed']);self.assertGreaterEqual(len(d['chapter_ids']),2)
   self.assertTrue(all(e['quote'] and e['mention_ids'] for e in d['evidence']))
 def test_maodun_letter_is_not_an_arbitrary_chanyu_match(self):
  m=next(m for m in para('100','p002')['mentions'] if m['surface']=='單于');self.assertEqual(m['person_id'],'wjt_htu_081_A')
  d=next(d for d in read('corpus/shiji/100-equivalences.json')['decisions'] if d['id']=='eq-shiji100-core-maodun')
  self.assertTrue(any('冒頓乃爲書遺高后' in e['quote'] for e in d['evidence']))
 def test_chu_paternal_path_includes_jian_and_baigong_sheng(self):
  people={p['id']:p for p in read('registry/persons.json')['persons']}
  for pid,parent in [('q8m_d0c_kq3_AE','q8m_d0c_kq3_A'),('q8m_d0c_kq3_AEB','q8m_d0c_kq3_AE'),('q8m_d0c_kq3_AEBA','q8m_d0c_kq3_AEB'),('q8m_d0c_kq3_AEA','q8m_d0c_kq3_AE')]:
   self.assertEqual(people[pid]['family_path']['parent_person_id'],parent)
  self.assertEqual(people['q8m_d0c_kq3_AEBA']['label'],'白公勝')
 def test_identified_mothers_merge_only_the_matched_sons_contexts(self):
  expected={'a-shiji031-032':'fbw_boe_fyu','a-shiji040-050':'fbw_boe_fyu','a-shiji066-007':'fbw_boe_fyu','a-shiji040-047':'hil_pvv_3c6','a-shiji066-006':'hil_pvv_3c6'}
  for n in ['031','040','066']:
   for a in read('corpus/shiji/'+n+'-assertions.json')['assertions']:
    if a['id'] in expected:self.assertEqual(a['object_person_id'],expected[a['id']])
  self.assertNotEqual(expected['a-shiji040-050'],expected['a-shiji040-047'])
 def test_zhao_wang_names_and_return_accounts_are_not_silently_rewritten(self):
  self.assertIn('生熊珍',para('040','p041')['text']);self.assertIn('生子軫',para('066','p002')['text'])
  self.assertIn('巣大夫',para('040','p055')['text']);self.assertIn('邊邑鄢',para('066','p021')['text'])
  self.assertEqual(next(m['person_id'] for m in para('040','p045')['mentions'] if m['surface']=='昭王'),'q8m_d0c_kq3_AEA')
  self.assertEqual(next(m['person_id'] for m in para('066','p008')['mentions'] if m['surface']=='昭王'),'q8m_d0c_kq3_AEA')
 def test_all_twenty_two_retired_ids_and_jsons_are_gone(self):
  people={p['id'] for p in read('registry/persons.json')['persons']};self.assertFalse(people & RETIRED)
  for pid in RETIRED:
   for folder in ['data/corpus/profiles','exports/persons']:self.assertFalse((ROOT/folder/(pid+'.json')).exists())
 def test_remaining_candidates_are_not_merged_by_name_only(self):
  p=para('100','p005');ids={m['surface']:m['person_id'] for m in p['mentions']}
  self.assertEqual(ids['灌夫'],'o7j_zzq_frd');self.assertEqual(ids['籍福'],'j9f_i2u_283')
  self.assertEqual(next(m['person_id'] for m in para('100','p004')['mentions'] if m['surface']=='趙同'),'m0d_n8x_pj8')
 def test_kinship_interpretation_and_social_metaphors_remain_separate(self):
  case=read('corpus/shiji/100.json')['annotation']['kinship_interpretation_cases'][0]
  self.assertEqual(case['default_alternative_id'],'shigu-maternal-half-brother');self.assertEqual(len(case['alternatives']),2)
  social={'cte_yao_v47','j32_wtj_khz_A','o7j_zzq_frd','j9f_i2u_283'}
  self.assertFalse(any(a['subject_person_id'] in social and a['object_person_id'] in social for a in read('corpus/shiji/100-assertions.json')['assertions']))
