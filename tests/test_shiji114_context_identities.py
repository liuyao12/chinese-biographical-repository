# coding:utf-8
import json,unittest
from pathlib import Path
from scripts.consolidate_person_ids import reference_files
R=Path(__file__).resolve().parents[1]
MAPPING={'3jq_7f4_ci2': 'ob7_g6i_7pp', 'ofj_de9_33w': 'yqp_nlb_p1p_A', '8ev_710_2op': 'yqp_nlb_p1p_AA', 'z8w_wsi_81x': 'yqp_nlb_p1p_ACA', 'al0_ke0_9c7': '7mz_d13_9ka_A', 'i7l_4us_u58': '71j_ydc_ly7', 'ksx_r3f_pjy': '6hy_i1z_hu2', 'oj7_6jw_4hs': '6hy_i1z_hu2', '0c3_ttl_f14': '6ym_eva_k4a', 'qfq_48j_lpj': 'yqp_nlb_p1p_CA', 'qfq_48j_lpj_A': 'yqp_nlb_p1p_CAE', '7ly_s1p_rqd': 'i7a_22p_qda', 'zsv_bdr_gyu': '6ip_dr3_fbl', 'r6p_87v_nc8': 'o0l_em5_5v9', 'a8x_0ou_7ud': 'pme_eis_xqi_*A*AAAAA', 'y1h_fo3_brs': 'yqp_nlb_p1p_ACAA', 'gcy_833_xmx': 'yqp_nlb_p1p_ABFA', 'gfy_kw8_8tm': 'yqp_nlb_p1p_ABFA', 'gcy_833_xmx_A': 'yqp_nlb_p1p_ABFAB'}
ROLES={'c-shiji-114-dongyue:m003-0186': '7mz_d13_9ka_A', 'c-shiji-114-dongyue:m004-0081': 'xp5_39k_w5w', 'c-shiji-114-dongyue:m004-0125': 'xp5_39k_w5w', 'c-shiji-114-dongyue:m004-0168': 'xp5_39k_w5w', 'c-shiji-114-dongyue:m004-0189': 'xp5_39k_w5w', 'c-shiji-114-dongyue:m004-0192': 'xp5_39k_w5w', 'c-shiji-114-dongyue:m004-0225': 'xp5_39k_w5w', 'c-shiji-114-dongyue:m004-0176': 'z2v_oh4_mhm', 'c-shiji-114-dongyue:m004-0179': 'z2v_oh4_mhm', 'c-shiji-114-dongyue:m004-0217': '6hy_i1z_hu2', 'c-shiji-114-dongyue:m008-0004': 'ub3_zen_skw'}
TABLE_OLD={'zk4_cdn_dn4','ipu_au8_1uy','1fr_jqc_i3t'}
def load(f):return json.loads((R/f).read_text())
class DongyueContextTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.c=load('corpus/shiji/114.json');cls.people={p['id']:p for p in load('registry/persons.json')['persons']};cls.anchors={m['id']:m for p in cls.c['paragraphs']for m in p['mentions']}
 def test_received_words_revision_and_eleven_paragraphs_preserved(self):
  self.assertEqual(self.c['text_sha256'],'b38ea0d040864a0368385740200d92755990ada0d0d3676e768cff945a22fc6f');self.assertEqual(self.c['source']['revision_id'],8735633);self.assertEqual(len(self.c['paragraphs']),11)
 def test_all_nineteen_source_ids_have_no_registry_or_export_redirects(self):
  self.assertEqual(len(MAPPING),19)
  for old,new in MAPPING.items():
   self.assertNotIn(old,self.people);self.assertIn(new,self.people);self.assertFalse((R/'exports/persons'/(old+'.json')).exists());self.assertFalse((R/'data/corpus/profiles'/(old+'.json')).exists())
 def test_editable_reference_layers_do_not_retain_old_ids(self):
  for f in reference_files(R):
   s=f.read_text()
   for old in MAPPING:self.assertNotIn(old,s,str(f))
 def test_sixteen_new_identity_decisions_have_real_each_book_anchors(self):
  ds=[d for d in load('corpus/shiji/114-equivalences.json')['decisions']if d['id'].startswith('eq-shiji114-core-')or d['id']=='eq-shiji114-chengyang-gongwang'];self.assertEqual(len(ds),16)
  for d in ds:self.assertFalse(d['human_reviewed']);self.assertTrue(all(e['mention_ids']for e in d['evidence']));self.assertEqual(set(d['chapter_ids']),{e['chapter_id']for e in d['evidence']});self.assertEqual(d['person_ids'],[d['canonical_person_id']])
 def test_eleven_exact_role_anchors_resolve_context(self):
  self.assertEqual(len(ROLES),11)
  for mid,pid in ROLES.items():self.assertEqual(self.anchors[mid]['person_id'],pid);self.assertEqual(self.anchors[mid]['status'],'contextual_provisional')
 def test_yushan_self_named_wudi_is_not_han_emperor(self):
  p=next(p for p in self.c['paragraphs']if p['id'].endswith('p008'));self.assertEqual(next(m for m in p['mentions']if m['surface']=='武帝')['person_id'],'ub3_zen_skw');self.assertEqual(next(m for m in p['mentions']if m['surface']=='天子')['person_id'],'yqp_nlb_p1p_ACAA');h=next(h for h in load('corpus/shiji/114-titles.json')['holdings']if h['id']=='th-shiji114-019');self.assertEqual(h['person_id'],'ub3_zen_skw');self.assertEqual(self.anchors[h['attestations'][0]['person_mention_id']]['surface'],'武帝')
 def test_tianfen_chronology_disagreement_not_silently_harmonized(self):
  self.assertIn('建元三年',self.c['paragraphs'][2]['text']);d=next(d for d in load('corpus/shiji/114-equivalences.json')['decisions']if d['id']=='eq-shiji114-core-tianfen');self.assertTrue(any('建元二年'in r['quote']and '免丞相、太尉'in r['quote']for r in d['references']))
 def test_fu_and_ziju_direct_fathers_are_preserved(self):
  a={a['id']:a for a in load('corpus/shiji/114-assertions.json')['assertions']};self.assertEqual((a['a-shiji114-005']['subject_person_id'],a['a-shiji114-005']['object_person_id']),('yqp_nlb_p1p_ABFAB','yqp_nlb_p1p_ABFA'));self.assertEqual((a['a-shiji114-003']['subject_person_id'],a['a-shiji114-003']['object_person_id']),('yqp_nlb_p1p_CAE','yqp_nlb_p1p_CA'));self.assertEqual(self.people['yqp_nlb_p1p_ABFAB']['family_path']['parent_person_id'],'yqp_nlb_p1p_ABFA')
 def test_elder_younger_brother_constraint_has_no_invented_ordinals(self):
  a=next(a for a in load('corpus/shiji/114-assertions.json')['assertions']if a['predicate']=='brother');q=a['qualifiers']['relative_birth_order'];self.assertEqual((q['older_person_id'],q['younger_person_id']),('xp5_39k_w5w','ub3_zen_skw'));self.assertIsNone(q['older_ordinal']);self.assertIsNone(q['younger_ordinal'])
 def test_chou_and_jugu_are_not_merged_by_title(self):
  self.assertIn('e00_pe1_zri_*A',self.people);self.assertIn('1bh_uew_js1',self.people)
  for d in load('corpus/shiji/114-equivalences.json')['decisions']:self.assertFalse({'e00_pe1_zri_*A','1bh_uew_js1'}<=set(d['person_ids']))
 def test_remote_yu_goujian_claims_do_not_create_one_missing_generation(self):
  self.assertIsNone(self.people['e00_pe1_zri'].get('family_path'));self.assertIsNone(self.people['ub6_g9c_hvb'].get('family_path'));a=load('corpus/shiji/114-assertions.json')['assertions'];self.assertEqual({x['object_person_id']for x in a if x['predicate']=='ancestor'},{'i7a_22p_qda'})
 def test_three_table_candidates_retired_and_six_anchors_relinked(self):
  ids={p['id']for p in load('data/historical-tables/person-candidates.json')['persons']};self.assertFalse(ids&TABLE_OLD);found=[]
  for num,rows,pid in [('020',['r059'],'yqp_nlb_p1p_ABFAB'),('021',['r099'],'yqp_nlb_p1p_ABFAB'),('021',['r098'],'yqp_nlb_p1p_ABFAC')]:
   t=load('data/historical-tables/shiji-'+num+'.json')
   for f in t['fragments']:
    for row in f['rows']:
     if row['id'].rsplit('-',1)[-1]in rows:
      for cell in row['cells']:
       # These are the six migrated child-name anchors; the parent-label
       # anchors added later have their own cross-cell relationship tests.
       if cell['column'] == 1:continue
       for m in cell['person_mentions']:self.assertEqual(m['person_id'],pid);self.assertEqual(m['identity_evidence'][0]['person_id'],pid);found.append(m['id'])
  self.assertEqual(len(found),6)
 def test_same_haichang_fief_does_not_merge_su_hong_with_liu_fu(self):
  def person(n,cid):return next(c for f in load('data/historical-tables/shiji-'+n+'.json')['fragments']for r in f['rows']for c in r['cells']if c['id']==cid)['person_mentions'][0]['person_id']
  self.assertEqual(person('020','shiji-020-t1-r056-c05'),'m08_4xt_opo');self.assertEqual(person('021','shiji-021-t1-r099-c03'),'yqp_nlb_p1p_ABFAB')
 def test_name_components_have_actual_sources_and_received_variants(self):
  ns={x['person_id']:x for x in load('data/corpus/profile-names.json')['records']}
  for pid,ming in [('yqp_nlb_p1p_ABFAB','福'),('yqp_nlb_p1p_ABFAC','齒')]:self.assertEqual(ns[pid]['kind'],'table_cell');self.assertEqual(ns[pid]['surname'],'劉');self.assertEqual(ns[pid]['ming'],ming);self.assertIn('劉'+ming,ns[pid]['quote'])
  self.assertIsNone(ns['yqp_nlb_p1p_ABFA']['surname']);self.assertEqual(ns['yqp_nlb_p1p_ABFA']['ming'],'喜');self.assertIn('王温舒',ns['6ym_eva_k4a']['additional_names']);self.assertIn('王溫舒',self.c['paragraphs'][7]['text'])
 def test_old_haichang_loss_does_not_end_liaoying_title(self):
  hs=[h for h in load('corpus/shiji/114-titles.json')['holdings']if h['person_id']=='yqp_nlb_p1p_ABFAB'];old=next(h for h in hs if h['title']=='海常侯');new=next(h for h in hs if h['title']=='繚嫈侯');self.assertEqual(old['effective_period']['end']['event_type'],'deposition');self.assertEqual(new['effective_period']['end']['status'],'unknown')
 def test_digital_witness_odd_phrases_and_incomplete_status_remain(self):
  self.assertIn('樓船將軍率錢唐轅終古',self.c['paragraphs'][7]['text']);self.assertIn('從建成侯敖，與其率，從繇王居股謀',self.c['paragraphs'][8]['text']);row=next(x for x in load('corpus/progress.json')['books']if x['chapter_id']==self.c['id']);self.assertFalse(row['complete']);self.assertEqual(row['person_status'],'in_progress')
if __name__=='__main__':unittest.main()
