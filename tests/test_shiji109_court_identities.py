# coding: utf-8
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text())
def paragraph(book,n):return next(p for p in load('corpus/shiji/'+book+'.json')['paragraphs']if p['id'].endswith(':p'+str(n).zfill(3)))
def person(book,n,surface):return next(m['person_id']for m in paragraph(book,n)['mentions']if m['surface']==surface)
class LiGuangCourtIdentities(unittest.TestCase):
 def test_three_shanyus_are_distinct_by_event(self):
  self.assertEqual({m['person_id']for m in paragraph('109',5)['mentions']if m['surface']=='單于'},{'wjt_htu_081_AAA'})
  self.assertEqual({m['person_id']for m in paragraph('109',13)['mentions']if m['surface']=='單于'},{'wjt_htu_081_AAB'})
  self.assertEqual(person('109',17,'單于'),'wjt_htu_081_AABC')
 def test_transient_shanyu_does_not_become_yizhixie(self):
  p=paragraph('110',39);ids={m['person_id']for m in p['mentions']if m.get('person_id')};self.assertGreaterEqual(len(ids),2);self.assertIn('wjt_htu_081_AAB',ids)
 def test_liling_marriage_reuses_one_daughter_and_preserves_both_assertions(self):
  self.assertEqual(person('109',18,'女'),'wjt_htu_081_AABCA');self.assertEqual(person('110',59,'其女'),'wjt_htu_081_AABCA')
  for book,aid in [('109','a-shiji109-011'),('110','a-shiji110-025')]:
   a=next(a for a in load('corpus/shiji/'+book+'-assertions.json')['assertions']if a['id']==aid);self.assertEqual({a['subject_person_id'],a['object_person_id']},{'wjt_htu_081_AABCA','wjt_htu_081_AABC'})
  assemblies=load('registry/family-assemblies.json')['assemblies'];self.assertNotIn('family-shanyu-shiji109-tianhan',{a['id']for a in assemblies});a=next(a for a in assemblies if a['id']=='family-touman-shiji110');m=next(m for m in a['members']if m['person_id']=='wjt_htu_081_AABCA');self.assertEqual(m['parent_person_id'],'wjt_htu_081_AABC')
 def test_year_disagreements_are_not_normalized_by_identity(self):
  self.assertIn('其後四歳',paragraph('109',5)['text']);self.assertIn('自馬邑軍後五年',paragraph('110',31)['text'])
  self.assertIn('後二歳',paragraph('109',10)['text']);self.assertIn('其明年',paragraph('123',16)['text']);self.assertIn('後三歲',paragraph('111',36)['text'])
 def test_hanyan_chu_note_and_zhangqian_bangu_note_keep_layers(self):
  self.assertEqual(paragraph('049',35)['text_layer'],'witness_appended_chu_note');self.assertEqual(person('049',35,'韓王孫名嫣'),'l9e_fbr_36a_*AB*A')
  self.assertEqual(paragraph('112',30)['text_layer'],'witness_appended_bangu_note');self.assertEqual(person('112',30,'張騫'),'gqj_xdu_8rf')
 def test_taizi_ju_does_not_invent_a_mother_for_ligan_children(self):
  self.assertEqual({m['person_id']for m in paragraph('109',15)['mentions']if m['surface']=='太子'},{'yqp_nlb_p1p_ACAAD'})
  assertions=load('corpus/shiji/109-assertions.json')['assertions']
  self.assertFalse(any(a['predicate']=='mother'and a['subject_person_id']in ['27j_f4p_jwp_AA','27j_f4p_jwp_AB']for a in assertions))
 def test_weiqing_identity_preserves_appointment_sequence(self):
  self.assertEqual(person('109',10,'大將軍'),'5dd_l1c_6g8');self.assertEqual(person('109',11,'大將軍'),'5dd_l1c_6g8');self.assertIn('即軍中拜車騎將軍青為大將軍',paragraph('111',6)['text'])
 def test_right_kings_remain_event_specific(self):
  self.assertEqual(person('109',11,'右賢王'),'cs1_ann_ert');self.assertNotEqual(person('109',17,'右賢王'),'cs1_ann_ert')
