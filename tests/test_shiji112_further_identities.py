# coding: utf-8
import json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def load(f):return json.loads((R/f).read_text())
def para(n,k):return next(p for p in load('corpus/shiji/'+n+'.json')['paragraphs']if p['id'].endswith(':p'+str(k).zfill(3)))
def pid(n,k,s):return next(m['person_id']for m in para(n,k)['mentions']if m['surface']==s)
class FurtherExemplars(unittest.TestCase):
 def test_mo_and_zeng_remain_people_in_local_comparison(self):
  self.assertEqual(pid('112',15,'墨'),'tjx_q6x_kc7');self.assertEqual(pid('112',15,'曾子'),'c7w_nyj_95u')
  p=para('112',15);m=next(m for m in p['mentions']if m['surface']=='墨');self.assertEqual(m['end']-m['start'],1);self.assertEqual(m['kind'],'person');self.assertIn('孔、墨、曾子之賢',p['text'])
 def test_taozhu_is_fanli_and_yidun_stays_another_merchant(self):
  self.assertEqual(pid('112',15,'陶朱'),pid('041',20,'范蠡'));self.assertIn('於是自謂陶朱公',para('041',20)['text']);self.assertEqual(pid('112',15,'猗頓'),pid('129',10,'猗頓'));self.assertNotEqual(pid('112',15,'陶朱'),pid('112',15,'猗頓'))
 def test_ancient_royal_names_do_not_use_han_or_yan_kings(self):
  for k in [16,18]:self.assertEqual(pid('112',k,'成'),'qna_m75_pj8');self.assertEqual(pid('112',k,'康'),'nek_dsn_nih')
  self.assertEqual(pid('112',16,'湯'),'tpz_x3m_e0h');self.assertEqual(pid('112',16,'武'),'y4i_pjk_4gn_AA');self.assertNotEqual(pid('112',16,'武'),pid('112',2,'天子'));self.assertNotEqual(pid('112',16,'康'),'jo4_4bf_0ra_A');self.assertEqual(pid('112',29,'夏禹'),'6ip_dr3_fbl')
 def test_literary_xiangru_is_not_lins_or_buyis_son(self):
  self.assertEqual(pid('112',30,'相如'),pid('117',1,'司馬相如'));self.assertNotEqual(pid('112',30,'相如'),pid('117',1,'藺相如'));self.assertNotEqual(pid('112',30,'相如'),pid('103',20,'相如'))
 def test_zhaoyu_law_and_shaofu_are_not_warring_states_adviser(self):
  self.assertEqual(pid('112',30,'趙禹'),pid('104',12,'趙禹'));self.assertEqual(pid('112',30,'趙禹'),pid('122',16,'趙禹'));self.assertNotEqual(pid('112',30,'趙禹'),pid('043',103,'趙禹'))
 def test_meisheng_summons_is_not_meigao(self):
  self.assertEqual(pid('112',30,'枚生'),pid('117',1,'枚乘'));self.assertNotEqual(pid('112',30,'枚生'),pid('112',30,'枚皋'));d=next(d for d in load('corpus/shiji/112-equivalences.json')['decisions']if d['id']=='eq-shiji112-panegyric-meisheng');ref=d['references'][0];self.assertIn('安車蒲輪徴乘',ref['raw_quote']);self.assertIn('683113d4baf6febecaf2ccb7913df87c4d68d454',ref['url']);self.assertEqual(ref['response_extent']['first_line'],520);self.assertFalse(ref['image_verified'])
 def test_liyan_keeps_established_paternal_path_and_literal_music_office(self):
  self.assertEqual(pid('112',30,'李延年'),'qhp_lk5_t1e_A');p=next(p for p in load('registry/persons.json')['persons']if p['id']=='qhp_lk5_t1e_A');self.assertEqual(p['family_path']['parent_person_id'],'qhp_lk5_t1e');self.assertIn('號協聲律',para('125',4)['text'])
 def test_editorial_layers_and_unresolved_emperor_are_preserved(self):
  self.assertEqual(para('112',29)['text_layer'],'witness_appended_edict');self.assertEqual(para('112',30)['text_layer'],'witness_appended_bangu_note');self.assertEqual(para('126',15)['text_layer'],'witness_appended_chu_note');self.assertEqual(pid('112',15,'先帝'),'moo_r04_tz1');self.assertIsNone(pid('112',19,'尉[佗]'))
 def test_distinctions_survive_materialization_and_sang_stays_stable(self):
  rows=load('corpus/shiji/112-distinctions.json')['distinctions'];pairs=[set(r['person_ids'])for r in rows];self.assertIn({'usb_lgr_ksa','c19_xxo_r8f_A'},pairs);self.assertIn({'vkr_lkp_dme','m12_4ic_ro1'},pairs);self.assertIn({'e1m_xt0_8w7','f16_k0n_4q2'},pairs);self.assertEqual(pid('112',30,'桑弘羊'),'fi2_2cl_w22');self.assertEqual(pid('112',30,'弘羊'),'fi2_2cl_w22')

 def test_retired_ids_absent_from_registry_and_public_files(self):
  old=['lni_lzq_7s0', 'ud7_fy7_6vl', 'zvp_ubd_334', '2n9_bsn_ad1', 'dko_o9v_cf7', '3r9_0to_we7', '4ng_2lt_u5u', 'oil_hwe_l58', '9nw_rct_r8j', 'rb8_xqe_j0t', 'rwy_lxz_2cv', 'vvw_4vz_j9e', 'jke_ad4_46c', '9z0_8lu_63q', 'y7w_938_ch8', 'lss_951_wm9', 'f1n_prq_vmh', 'g9i_nw9_5m8', 'upc_vy1_fjk', 'x4a_v9q_unl', 'yng_2ws_4d6', 'tgg_rko_ryw', '4ys_iau_gtb', 'fj6_olv_5t0', 'o0t_u0g_33q', 'xp9_lok_hz4', '3ce_wh3_q9a', 'zb7_1f5_mzb', '9bg_1y9_g83']
  ids={p["id"]for p in load("registry/persons.json")["persons"]}
  for pid in old:
   self.assertNotIn(pid,ids)
   for folder in ["exports/persons","data/corpus/profiles"]:self.assertFalse((R/folder/(pid+".json")).exists())

 def test_huainan_hengshan_case_resolves_kings_without_new_spans(self):
  p=para('112',8)
  for surface,start,pidval in [('淮南',0,'yqp_nlb_p1p_AFA'),('衡山',3,'yqp_nlb_p1p_AFC')]:
   m=next(m for m in p['mentions']if m['surface']==surface);self.assertEqual((m['start'],m['end'],m['person_id']),(start,start+2,pidval));self.assertEqual(m['id'],'c-shiji-112-pingjin:m008-'+str(start).zfill(4))
  self.assertEqual(pid('112',8,'淮南'),pid('118',15,'淮南王安'));self.assertEqual(pid('112',8,'衡山'),pid('118',25,'衡山王賜'));self.assertNotEqual(pid('112',8,'淮南'),pid('118',1,'淮南厲王長'))
