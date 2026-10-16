# coding: utf-8
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(f):return json.loads((ROOT/f).read_text())
def para(n,k):return next(p for p in load('corpus/shiji/'+n+'.json')['paragraphs']if p['id'].endswith(':p'+str(k).zfill(3)))
def who(n,k,s):return next(m['person_id']for m in para(n,k)['mentions']if m['surface']==s)
class XiongnuWesternIdentities(unittest.TestCase):
 def test_nanyue_king_is_last_king_not_his_predecessor(self):
  self.assertEqual(who('110',45,'南越王'),'f4l_jyl_oqv_C');self.assertEqual(who('113',9,'建德'),'f4l_jyl_oqv_C');self.assertNotEqual(who('113',7,'王'),'f4l_jyl_oqv_C');self.assertIn('蘇弘得建德',para('113',11)['text']);self.assertIn('頭已懸',para('110',45)['text'])
 def test_mugua_is_not_successors_and_death_agents_stay_distinct(self):
  self.assertEqual(who('110',55,'其王'),'2l2_58b_q4i');self.assertIn('共殺其王毋寡',para('123',33)['text']);self.assertIn('斬其王而還',para('110',55)['text']);self.assertNotEqual(who('123',36,'昧蔡'),'2l2_58b_q4i');self.assertNotEqual(who('123',36,'蟬封'),'2l2_58b_q4i')
 def test_marriage_connects_specific_woman_and_king_without_naming_them(self):
  self.assertEqual(who('110',47,'公主'),'6f5_70o_6w4');self.assertEqual(who('110',47,'烏孫王'),'3jf_ce1_jy2_A');self.assertEqual(who('123',25,'翁主'),'6f5_70o_6w4');self.assertNotEqual(who('123',25,'岑娶'),'3jf_ce1_jy2_A');self.assertIsNone(who('110',47,'翁主'))
  people={p['id']:p for p in load('registry/persons.json')['persons']};self.assertEqual(people['6f5_70o_6w4']['label'],'江都翁主');self.assertEqual(people['3jf_ce1_jy2_A']['label'],'昆莫');self.assertNotIn('細君',[a['surface']for a in people['6f5_70o_6w4']['aliases']])
 def test_liguangli_campaigns_and_kinship_are_same_person(self):
  self.assertEqual(who('123',30,'李廣利'),'pez_8dn_r76');self.assertEqual(who('109',17,'李廣利'),'pez_8dn_r76');self.assertEqual(who('049',32,'廣利'),'pez_8dn_r76');self.assertEqual(who('110',55,'貳師將軍'),'pez_8dn_r76');self.assertEqual(who('110',60,'廣利'),'pez_8dn_r76');self.assertTrue(para('110',60)['text'].startswith('後二歳'));self.assertIn('以巫蠱族滅',para('110',60)['text'])
 def test_unresolved_cases_and_wusun_grandson_remain(self):
  self.assertEqual(len(load('corpus/shiji/110.json')['annotation']['unresolved_identity_cases']),3);self.assertIn('乃令其孫岑娶妻翁主',para('123',25)['text']);self.assertIn('先王',para('113',9)['text'])
 def test_retired_ids_have_no_registry_or_public_entry(self):
  ids={p['id']for p in load('registry/persons.json')['persons']}
  for p in ['9w0_e8e_sdf','oe4_3q9_y4m','s79_jb8_yix','k8g_wo9_ejj','fyv_cvv_y5b']:
   self.assertNotIn(p,ids)
   for folder in ['exports/persons','data/corpus/profiles']:self.assertFalse((ROOT/folder/(p+'.json')).exists())
