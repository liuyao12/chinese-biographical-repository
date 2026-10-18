# coding: utf-8
import json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def load(f):return json.loads((R/f).read_text())
def para(n,k):return next(p for p in load('corpus/shiji/'+n+'.json')['paragraphs']if p['id'].endswith(':p'+str(k).zfill(3)))
def pid(n,k,s):return next(m['person_id']for m in para(n,k)['mentions']if m['surface']==s)
class RebelIdentities(unittest.TestCase):
 def test_peace_envoy_shared_event(self):
  self.assertEqual(pid('112',13,'劉敬'),pid('099',6,'劉敬'));self.assertIn('使劉敬往結和親約',para('099',6)['text'])
 def test_southern_commander_and_grandson_gap(self):
  self.assertEqual(pid('112',13,'尉佗'),pid('113',1,'尉佗'));self.assertEqual(pid('112',19,'尉佗'),'bvb_d1z_fd0');p=next(p for p in load('registry/persons.json')['persons']if p['id']=='bvb_d1z_fd0_*A');f=p['family_path'];self.assertEqual(f['ancestor_person_id'],'bvb_d1z_fd0');self.assertIsNone(f['parent_person_id']);self.assertEqual(f['intermediate_person_ids'],[None]);self.assertIn('佗孫胡',para('113',4)['text'])
 def test_rebels_match_their_distinct_theatres(self):
  expected={'吳廣':'h2h_z86_a3d','武臣':'yu4_0gm_gje','張耳':'agx_sqm_4ou','項梁':'5xt_rg8_7zs_A','田儋':'u87_cc1_7vm','景駒':'nw9_lle_9jg','周市':'i8y_6lu_30h','韓廣':'neh_wop_6sz'}
  for s,p in expected.items():self.assertEqual(pid('112',19,s),p)
  self.assertEqual(pid('112',13,'章邯'),'4jv_qte_5p4')
 def test_same_name_and_short_name_collisions_stay_separate(self):
  self.assertNotEqual(pid('112',19,'吳廣'),pid('043',64,'吳廣'));self.assertNotEqual(pid('112',19,'周市'),pid('094',4,'市'));self.assertNotEqual(pid('112',19,'項梁'),pid('007',1,'項籍'))
 def test_unresolved_and_source_spelling_unchanged(self):
  self.assertEqual(pid('112',13,'成進'),'lve_fqh_8v6');self.assertEqual(pid('112',19,'屠睢'),'5ep_xih_trk');self.assertEqual(pid('112',19,'監祿'),'a1r_v0c_ghw');self.assertIsNone(pid('112',19,'尉[佗]'));self.assertIn('景駒舉郢',para('112',19)['text']);self.assertIn('軍彭城東',para('007',5)['text'])
 def test_fourteen_old_identity_and_path_ids_retired(self):
  old=['5vm_33p_472','qig_axh_3z6','rxf_qqr_to2','8a8_f4u_it7','kd6_4zt_f4n','7qu_l07_81s','5el_35a_36r','0qb_3yw_sge','mbg_5br_536','zeu_gxt_4pn','2kl_5xk_hld','r3c_eue_cqn','k8p_ptb_xa1','r3c_eue_cqn_*A'];ids={p['id']for p in load('registry/persons.json')['persons']}
  for p in old:
   self.assertNotIn(p,ids)
   for folder in ['exports/persons','data/corpus/profiles']:self.assertFalse((R/folder/(p+'.json')).exists())
