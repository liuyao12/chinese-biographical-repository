# coding: utf-8
import json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def load(f):return json.loads((R/f).read_text())
def para(n,k):return next(p for p in load('corpus/shiji/'+n+'.json')['paragraphs']if p['id'].endswith(':p'+str(k).zfill(3)))
def pid(n,k,s):return next(m['person_id']for m in para(n,k)['mentions']if m['surface']==s)
class PingjinCore(unittest.TestCase):
 def test_sunwu_adjacent_persons_not_whole_work(self):
  p=para('111',21);a=next(m for m in p['mentions']if m['id'].endswith('m021-0022'));b=next(m for m in p['mentions']if m['id'].endswith('m021-0023'));self.assertEqual((a['surface'],a['start'],a['end'],a['person_id']),('孫',22,23,'vax_w2r_0za'));self.assertEqual((b['surface'],b['start'],b['end'],b['person_id']),('吳',23,24,'61h_0sk_4pb'));self.assertIn('孫吳兵法',p['text']);self.assertFalse(any(m['start']<26and m['end']>24for m in p['mentions']))
 def test_author_reference_does_not_create_wudi_life_or_office(self):
  hs=load('corpus/shiji/111-titles.json')['holdings'];self.assertFalse(any(h['person_id']in ['vax_w2r_0za','61h_0sk_4pb']for h in hs));ds=[d for d in load('corpus/shiji/111-identities.json')['decisions']if d['id'].startswith('d-shiji111-sunwu-')];self.assertEqual(len(ds),2)
  for d in ds:
   r=d['references'][0];self.assertEqual(r['quote'],'師古曰呉呉起也孫孫武也');self.assertFalse(r['image_verified']);self.assertIn('/blob/',r['url']);self.assertIn('不宣稱',d['rationale'])
 def test_emperor_and_family_titles_by_context(self):
  self.assertEqual(pid('112',2,'天子'),'yqp_nlb_p1p_ACAA');self.assertEqual(pid('112',10,'衛將軍'),'5dd_l1c_6g8');self.assertEqual(pid('112',30,'衛青'),'5dd_l1c_6g8');self.assertEqual(pid('112',30,'霍去病'),'3tw_nq2_gyn');self.assertEqual(pid('112',23,'衛皇后'),'l5c_h8i_d5q')
 def test_zhufu_different_accounts_join_with_evidence(self):
  for n,k in [('011',18),('052',29),('080',20),('121',19),('122',38),('112',10)]:self.assertEqual(pid(n,k,'主父偃'),'vbr_ff1_yc4')
  d=next(d for d in load('corpus/shiji/112-equivalences.json')['decisions']if d['id']=='eq-shiji112-core-zhufu');self.assertIn('篇末追評',d['rationale']);self.assertEqual(len(d['chapter_ids']),6)
 def test_zhangou_identity_preserves_conflicting_years(self):
  self.assertEqual(pid('112',5,'張歐'),'afj_vl8_7fu_A');self.assertIn('元朔三年，張歐免',para('112',5)['text']);self.assertIn('元朔四年，韓安國免',para('103',24)['text']);d=next(d for d in load('corpus/shiji/112-equivalences.json')['decisions']if d['id']=='eq-shiji112-core-zhangou');self.assertFalse(d['references'][0]['image_verified']);self.assertIn('不裁成同一年',d['rationale'])
 def test_zhumaichen_and_appended_layers(self):
  self.assertEqual(pid('112',5,'朱買臣'),'gni_7gn_c4a');self.assertEqual(pid('122',23,'朱買臣'),'gni_7gn_c4a');self.assertNotEqual(pid('112',29,'太皇太后'),'yqp_nlb_p1p_ACAA');self.assertNotEqual(pid('112',30,'孝宣'),'yqp_nlb_p1p_ACAA');self.assertNotEqual(para('112',30)['text_layer'],'received_chapter');self.assertNotEqual(para('112',29)['text_layer'],'received_chapter')
 def test_twelve_retired_ids_are_removed(self):
  old=['ukp_lkb_cb5','aec_cp5_x6d','jj8_r26_ani','65g_b5h_fvh','h37_ncd_om5','a05_brz_8xe','sg8_94p_jik','ges_7zm_vut','kcl_nyd_kou','ez5_fp5_uga','0ad_530_yth','bvn_k2n_f84'];ids={p['id']for p in load('registry/persons.json')['persons']}
  for p in old:
   self.assertNotIn(p,ids)
   for folder in ['exports/persons','data/corpus/profiles']:self.assertFalse((R/folder/(p+'.json')).exists())
