# coding: utf-8
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text())
def paragraph(book,n):return next(p for p in load('corpus/shiji/'+book+'.json')['paragraphs']if p['id'].endswith(':p'+str(n).zfill(3)))
def person(book,n,surface):return next(m['person_id']for m in paragraph(book,n)['mentions']if m['surface']==surface)
RETIRED=['2af_4tx_pil', '2sy_6a4_j5k', '3qx_bkv_c0r', '4ub_gne_e2e', '514_qwu_eaa', '67k_3wh_j8c', '6dx_6sh_873', '7w8_il9_9fv', '81n_sfg_u64', '87t_j04_qp3', '8sb_2ue_1nf', 'acv_096_kwf', 'd31_kms_f7h', 'dba_sl3_c31', 'ddf_jql_z0y', 'dg5_xe0_sdd', 'dwm_kwy_53u', 'f4j_73i_aup', 'fbp_g9d_1zu', 'gcj_0vc_72s', 'h8h_gjb_mb9', 'hae_ws1_2ad', 'hev_jdd_l90', 'i45_w2y_9x9', 'jio_w3a_ic4', 'lvl_qjo_kig', 'ma3_01e_ip2', 'msj_ltn_6fg', 'n79_j93_xiu', 'nit_fmb_fqz', 'nls_m5j_z5z', 'o85_onv_slc', 'oz1_e5f_8q1', 'q3n_t18_zql', 'qah_j22_ega', 'r2c_l17_1q6', 'rzr_o54_u0d', 'tdz_63e_0nm', 'tf3_lxa_cj1', 'thx_toi_m04', 'wqs_z6j_lz7', 'wtu_vqy_2dq']
class XiongnuAncientIdentities(unittest.TestCase):
 def test_gongliu_does_not_become_buzhu_by_shared_office_story(self):
  self.assertEqual(person('110',2,'公劉'),'ubt_idy_jr8');self.assertIn('公劉失其稷官',paragraph('110',2)['text']);self.assertIn('不窋以失其官',paragraph('004',3)['text']);self.assertNotEqual(person('004',3,'不窋'),'ubt_idy_jr8')
 def test_conquest_numbers_and_army_sizes_are_not_normalized(self):
  self.assertIn('西戎八國',paragraph('110',3)['text']);self.assertIn('益國十二',paragraph('005',38)['text']);self.assertIn('十萬之眾北擊胡',paragraph('110',4)['text']);self.assertIn('三十萬眾北逐戎狄',paragraph('088',2)['text'])
 def test_state_and_event_disambiguate_royal_titles(self):
  self.assertEqual(person('110',2,'武王'),'y4i_pjk_4gn_AA');self.assertEqual(person('110',2,'穆王'),'sx2_wyn_nhr');self.assertEqual(person('110',2,'齊桓公'),'9w2_c77_53m');self.assertEqual(person('110',4,'惠王'),'y97_huh_vuz_AAAAAAAAAAAAABAAAAAA')
 def test_huihou_is_stepmother_not_birth_mother_of_xiangwang(self):
  aa=load('corpus/shiji/110-assertions.json')['assertions'];a=next(a for a in aa if a['id']=='a-shiji110-010');self.assertEqual((a['subject_person_id'],a['predicate'],a['object_person_id']),('gt1_z7d_s3u','stepmother','rft_1rm_8b4'));self.assertFalse(any(a['subject_person_id']=='gt1_z7d_s3u'and a['predicate']=='mother'and a['object_person_id']=='rft_1rm_8b4'for a in aa))
 def test_xuantaihou_has_one_zhaowang_identity_across_mother_assertions(self):
  subjects=[]
  for book in ['005','071','072']:
   subjects.extend(a['subject_person_id']for a in load('corpus/shiji/'+book+'-assertions.json')['assertions']if a['predicate']=='mother'and a['object_person_id']=='pvp_ebv_zcb')
  self.assertEqual(len(subjects),3);self.assertEqual(set(subjects),{'ao3_0fy_d45'})
 def test_qinwuyang_preserves_qinkai_grandfather_without_filling_father(self):
  self.assertEqual(person('086',32,'秦舞陽'),'505_n4y_p39_*A');a=next(a for a in load('corpus/shiji/110-assertions.json')['assertions']if a['id']=='a-shiji110-003');self.assertEqual((a['subject_person_id'],a['predicate'],a['object_person_id']),('505_n4y_p39_*A','grandfather','505_n4y_p39'));family=next(a for a in load('registry/family-assemblies.json')['assemblies']if a['id']=='family-qinkai-shiji110');m=next(m for m in family['members']if m['person_id']=='505_n4y_p39_*A');self.assertIsNone(m['parent_person_id']);self.assertEqual(m['intermediate_person_ids'],[None])
 def test_three_huiwang_subjects_do_not_identify_liangwang(self):
  for n,start in [(64,27),(66,43),(66,215)]:
   p=paragraph('005',n);m=next(m for m in p['mentions']if m['start']==start);self.assertEqual(m['surface'],'王');self.assertEqual(m['person_id'],'y97_huh_vuz_AAAAAAAAAAAAABAAAAAA')
  m=next(m for m in paragraph('005',66)['mentions']if m['surface']=='梁王');self.assertIsNone(m.get('person_id'))
 def test_qinwang_and_shihuang_in_specific_events_share_identity(self):
  self.assertEqual(person('110',4,'秦王'),'ao3_0fy_d45_AAA');self.assertEqual(person('110',4,'始皇帝'),'ao3_0fy_d45_AAA');self.assertEqual(person('073',10,'秦始皇'),'ao3_0fy_d45_AAA');self.assertIn('朕為始皇帝',paragraph('006',21)['text'])
 def test_chu_campaign_mengtian_is_not_merged_without_note_review(self):
  self.assertEqual(person('073',10,'蒙恬'),'k2p_5ol_dwh_A');self.assertEqual(person('110',4,'蒙恬'),'k2p_5ol_dwh_AA');self.assertNotEqual(person('073',10,'蒙恬'),person('110',4,'蒙恬'))
 def test_42_retired_entries_removed_after_reference_migration(self):
  ids={p['id']for p in load('registry/persons.json')['persons']};self.assertEqual(len(RETIRED),42)
  for pid in RETIRED:
   self.assertNotIn(pid,ids)
   for folder in ['data/corpus/profiles','exports/persons']:self.assertFalse((ROOT/folder/(pid+'.json')).exists())
  ds=[d for d in load('corpus/shiji/110-equivalences.json')['decisions']if d['id'].startswith('eq-shiji110-ancient-')];self.assertEqual(len(ds),33);self.assertTrue(all(d.get('identity_materialized')and not d['human_reviewed']for d in ds))
