# coding: utf-8
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(f):return json.loads((ROOT/f).read_text())
def para(n,k):return next(p for p in load('corpus/shiji/'+n+'.json')['paragraphs']if p['id'].endswith(':p'+str(k).zfill(3)))
def person(n,k,s):return next(m['person_id']for m in para(n,k)['mentions']if m['surface']==s)
class WeiHouseholdIdentities(unittest.TestCase):
 def test_weifuren_only_son_is_ju_without_ordinal(self):
  self.assertEqual(person('111',5,'男'),'yqp_nlb_p1p_ACAAD');self.assertEqual(person('049',26,'據'),'yqp_nlb_p1p_ACAAD');a=next(a for a in load('corpus/shiji/111-assertions.json')['assertions']if a['id']=='a-shiji111-011');self.assertEqual(a['subject_person_id'],'yqp_nlb_p1p_ACAAD');self.assertNotIn('birth_order',a['qualifiers'])
 def test_wang_furen_links_by_specific_qi_mother_story(self):
  for n,k in [('111',9),('049',30),('060',20),('126',20)]:self.assertEqual(person(n,k,'王夫人'),'3eo_u7e_pxx')
  self.assertNotEqual(person('049',18,'王夫人'),'3eo_u7e_pxx');self.assertIn('趙人也',para('060',20)['text']);self.assertIn('生子閎',para('060',20)['text'])
 def test_hong_and_changyi_children_use_exact_anaphor_anchors(self):
  self.assertEqual(person('126',20,'子'),'yqp_nlb_p1p_ACAAA');self.assertEqual(person('049',30,'子'),'yqp_nlb_p1p_ACAAA');self.assertEqual(person('049',30,'齊王'),'yqp_nlb_p1p_ACAAA');self.assertEqual(person('049',31,'男一人'),'yqp_nlb_p1p_ACAAF');self.assertEqual(person('049',31,'昌邑王'),'yqp_nlb_p1p_ACAAF');self.assertNotEqual(person('049',30,'子'),person('049',31,'男一人'))
 def test_advisors_stay_separate_and_layers_and_money_stay_literal(self):
  self.assertNotEqual(person('111',9,'甯乘'),person('126',19,'東郭先生'));self.assertIn('五百金',para('111',9)['text']);self.assertIn('五百金',para('126',19)['text']);self.assertEqual(para('111',9)['text_layer'],'received_chapter');self.assertEqual(para('126',19)['text_layer'],'witness_appended_chu_note');self.assertEqual(para('060',20)['text_layer'],'witness_appended_chu_note')
 def test_weihou_same_person_but_conflicting_sibling_order_preserved(self):
  self.assertEqual(person('126',19,'衛后'),'l5c_h8i_d5q');self.assertEqual(person('060',20,'衛夫人'),'l5c_h8i_d5q');a=next(a for a in load('corpus/shiji/111-assertions.json')['assertions']if a['id']=='a-shiji111-008');b=next(a for a in load('corpus/shiji/126-assertions.json')['assertions']if a['id']=='a-shiji126-005');self.assertEqual(a['qualifiers']['relative_birth_order']['older_person_id'],'l5c_h8i_d5q');self.assertEqual(b['qualifiers']['relative_birth_order']['older_person_id'],'5dd_l1c_6g8');self.assertIn('而姊衛子夫',para('111',1)['text']);self.assertIn('衛后兄也',para('126',19)['text'])
 def test_emperor_stays_wudi_through_scoped_story_but_prior_emperor_unknown(self):
  for k in [14,15,17,19,22]:self.assertEqual(person('126',k,'武帝'),'yqp_nlb_p1p_ACAA')
  self.assertIsNone(person('126',20,'先帝'))
 def test_nine_retired_ids_are_removed_without_redirects(self):
  ids={p['id']for p in load('registry/persons.json')['persons']}
  for p in ['apn_ec5_yqm','77o_my6_sxt','op9_u99_9x5','dak_kea_wep','2wt_drt_ii8','dw3_19c_euu','sdj_vte_hhn','udi_l0u_sbn','kq8_9zr_p86']:
   self.assertNotIn(p,ids)
   for folder in ['exports/persons','data/corpus/profiles']:self.assertFalse((ROOT/folder/(p+'.json')).exists())
