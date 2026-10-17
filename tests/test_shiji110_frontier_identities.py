# coding: utf-8
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text())
def paragraph(book,n):return next(p for p in load('corpus/shiji/'+book+'.json')['paragraphs']if p['id'].endswith(':p'+str(n).zfill(3)))
def person(book,n,surface):return next(m['person_id']for m in paragraph(book,n)['mentions']if m['surface']==surface)
class XiongnuFrontierIdentities(unittest.TestCase):
 def test_four_officials_connect_to_specific_profiles(self):
  self.assertEqual(person('110',54,'韓說'),'l9e_fbr_36a_*AB*B');self.assertEqual(person('110',54,'衛伉'),'5dd_l1c_6g8_D');self.assertEqual(person('110',54,'路博德'),'vib_10x_51n');self.assertEqual(person('110',35,'右將軍建'),'ior_a2u_f1c')
 def test_hanshuo_case_is_resolved_without_erasing_other_cases(self):
  a=load('corpus/shiji/110.json')['annotation'];self.assertEqual(len(a['unresolved_identity_cases']),3);case=next(c for c in a['resolved_identity_cases']if c['id']=='u-shiji110-hanshuo-hanyan');self.assertEqual(case['person_id'],'l9e_fbr_36a_*AB*B');self.assertTrue(case['identity_equivalence_decision_ids'])
 def test_hanshuo_kinship_and_specific_posts_support_identity(self):
  self.assertEqual(person('111',39,'韓說'),'l9e_fbr_36a_*AB*B');self.assertEqual(person('114',8,'韓說'),'l9e_fbr_36a_*AB*B');self.assertIn('以太初三年為游擊將軍，屯於五原外列城',paragraph('111',39)['text']);self.assertIn('穨當孽孫韓嫣',paragraph('093',7)['text'])
 def test_weikang_is_eldest_even_though_id_ends_d(self):
  a=next(a for a in load('corpus/shiji/111-assertions.json')['assertions']if a['id']=='a-shiji111-012');self.assertEqual(a['subject_person_id'],'5dd_l1c_6g8_D');self.assertEqual(a['object_person_id'],'5dd_l1c_6g8');self.assertEqual(a['qualifiers']['birth_order']['ordinal'],1);self.assertIn('宜春侯伉',paragraph('111',23)['text']);self.assertIn('子伉代為長平侯',paragraph('111',23)['text'])
 def test_lubode_biography_and_campaign_keep_same_person(self):
  for book,n in [('111',44),('113',7),('113',10)]:self.assertEqual(person(book,n,'路博德'),'vib_10x_51n')
  self.assertIn('平州人',paragraph('111',44)['text']);self.assertIn('屯居延',paragraph('111',44)['text']);self.assertIn('衛尉路博德為伏波將軍',paragraph('113',10)['text'])
 def test_chronology_difference_stays_in_source(self):
  self.assertTrue(paragraph('110',60)['text'].startswith('後二歳'));self.assertIn('以巫蠱族滅',paragraph('110',60)['text']);self.assertIn('元鼎六年',paragraph('111',39)['text']);self.assertIn('元封元年冬',paragraph('114',8)['text'])
 def test_building_is_not_sujian_name_and_defeat_not_death(self):
  p=paragraph('111',5);i=p['text'].index('建筑');self.assertFalse(any(m['start']<=i<m['end']for m in p['mentions']));self.assertIn('右將軍建得以身脫',paragraph('110',35)['text']);self.assertIn('贖為庶人',paragraph('111',8)['text'])
 def test_six_retired_ids_have_no_registry_or_public_entry(self):
  ids={p['id']for p in load('registry/persons.json')['persons']}
  for pid in ['tvo_aez_7nt','3u0_w7q_w9q','haa_dor_26n','1n0_bu8_jv2','wxg_pg3_wk0','0nh_j0e_l31']:
   self.assertNotIn(pid,ids)
   for folder in ['exports/persons','data/corpus/profiles']:self.assertFalse((ROOT/folder/(pid+'.json')).exists())
