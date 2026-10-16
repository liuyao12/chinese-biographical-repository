# coding: utf-8
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(f):return json.loads((ROOT/f).read_text())
class MengWuPreferredReading(unittest.TestCase):
 def test_three_chu_mentions_keep_literal_mengtian_but_link_mengwu(self):
  p=next(p for p in load('corpus/shiji/073.json')['paragraphs']if p['id'].endswith(':p010'));ms=[m for m in p['mentions']if m['surface']=='蒙恬'];self.assertEqual(len(ms),3);self.assertEqual({m['person_id']for m in ms},{'k2p_5ol_dwh_A'});self.assertIn('李信及蒙恬將二十萬南伐荊',p['text']);self.assertIn('蒙恬攻寢',p['text']);self.assertIn('與蒙恬會城父',p['text'])
 def test_every_literal_occurrence_has_qualified_preferred_reading(self):
  decisions=load('corpus/shiji/073-identities.json')['decisions'];ds=[d for d in decisions if d.get('preferred_reading',{}).get('variant_id')=='rv-shiji073-mengwu-study'];self.assertEqual(len(ds),3);self.assertEqual(len({d['preferred_reading']['person_mention_id']for d in ds}),3)
  for d in ds:
   self.assertEqual(d['person_id'],'k2p_5ol_dwh_A');self.assertEqual(d['preferred_reading']['preferred_surface'],'蒙武');self.assertTrue(d['preferred_reading']['source_spelling_is_not_alias']);self.assertFalse(d['human_reviewed']);self.assertFalse(d['references'][0]['image_verified']);self.assertIn('第194頁',d['references'][0]['title']);self.assertIn('轉引',d['references'][0]['note'])
 def test_mengwu_profile_does_not_offer_mengtian_as_ordinary_alias(self):
  p=load('data/corpus/profiles/k2p_5ol_dwh_A.json');self.assertNotIn('蒙恬',p['names']);self.assertEqual(len([d for d in p['preferred_readings']if d['variant_id']=='rv-shiji073-mengwu-study']),3)
 def test_northern_campaign_and_father_son_stay_distinct(self):
  p=next(p for p in load('corpus/shiji/110.json')['paragraphs']if p['id'].endswith(':p004'));self.assertEqual(next(m['person_id']for m in p['mentions']if m['surface']=='蒙恬'),'k2p_5ol_dwh_AA');p=next(p for p in load('corpus/shiji/088.json')['paragraphs']if p['id'].endswith(':p001'));self.assertIn('武子曰恬',p['text']);self.assertNotEqual('k2p_5ol_dwh_A','k2p_5ol_dwh_AA')
 def test_old_local_candidate_is_retired_after_all_reference_updates(self):
  self.assertNotIn('eal_ozl_urh',{p['id']for p in load('registry/persons.json')['persons']})
  for folder in ['exports/persons','data/corpus/profiles']:self.assertFalse((ROOT/folder/'eal_ozl_urh.json').exists())
 def test_guochang_kunming_campaign_connects_to_bahu_general(self):
  p=next(p for p in load('corpus/shiji/123.json')['paragraphs']if p['id'].endswith(':p023'));self.assertEqual(next(m['person_id']for m in p['mentions']if m['surface']=='郭昌'),'ey5_pne_opn');p=next(p for p in load('corpus/shiji/111.json')['paragraphs']if p['id'].endswith(':p040'));self.assertIn('還擊昆明，毋功，奪印',p['text'])
 def test_xuziwei_same_name_and_office_without_guozong_merge(self):
  p=next(p for p in load('corpus/shiji/122.json')['paragraphs']if p['id'].endswith(':p035'));self.assertEqual(next(m['person_id']for m in p['mentions']if m['surface']=='徐自爲'),'3jt_wmb_7c3');p=next(p for p in load('corpus/shiji/110.json')['paragraphs']if p['id'].endswith(':p052'));a=next(m['person_id']for m in p['mentions']if m['surface']=='郭縱');p=next(p for p in load('corpus/shiji/129.json')['paragraphs']if p['id'].endswith(':p010'));b=next(m['person_id']for m in p['mentions']if m['surface']=='郭縱');self.assertNotEqual(a,b)
