# coding: utf-8
import copy,json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def load(f):return json.loads((R/f).read_text())
def chapter():return load('corpus/shiji/113.json')
def para(k):return next(p for p in chapter()['paragraphs']if p['id'].endswith(k))
def names(pid):return next(n for n in load('data/corpus/profile-names.json')['records']if n['person_id']==pid)
class NanyueCoreIdentities(unittest.TestCase):
 def test_shared_events_reconcile_twelve_groups(self):
  ds=[d for d in load('corpus/shiji/113-equivalences.json')['decisions']if d['id'].startswith('eq-shiji113-core-')];self.assertEqual(len(ds),12)
  self.assertEqual({d['canonical_person_id']for d in ds},{'ao3_0fy_d45_AAAA','pom_ycp_ha5','ob7_g6i_7pp','yqp_nlb_p1p_A','h2h_z86_a3d','i30_mjq_6q8_A','yqp_nlb_p1p_AC','yqp_nlb_p1p_ACA','i3f_9l9_g53','yqp_nlb_p1p_ACAA','71j_ydc_ly7','b77_ulm_otk'})
  for d in ds:self.assertTrue(d['evidence']);self.assertFalse(d['human_reviewed'])
 def test_local_wudi_is_not_han_wudi(self):
  self.assertEqual(next(m for m in para('p006')['mentions']if m['surface']=='武帝')['person_id'],'bvb_d1z_fd0')
  self.assertEqual(next(m for m in para('p007')['mentions']if m['surface']=='天子')['person_id'],'yqp_nlb_p1p_ACAA')
 def test_cangwu_qinwang_and_zhaoguang_have_explicit_commentary(self):
  a=next(d for d in load('corpus/shiji/113-equivalences.json')['decisions']if d['id'].endswith('cangwuqinwang'));self.assertIn('秦王即下趙光也',a['references'][0]['quote']);self.assertEqual(next(m for m in para('p008')['mentions']if m['surface']=='蒼梧秦王')['person_id'],'b77_ulm_otk');self.assertEqual(names('b77_ulm_otk')['ming'],'光')
 def test_compound_surname_courtesy_name_and_unknown_given_name(self):
  n=names('u20_r6q_88g');self.assertEqual((n['surname'],n['ming'],n['zi']),('安國',None,'少季'));self.assertIn('字少季',n['additional_names']);self.assertIn('姓安國字少季',n['references'][0]['quote'])
 def test_sister_direction_preserves_age_order_without_new_parents(self):
  a=next(a for a in load('corpus/shiji/113-assertions.json')['assertions']if a['id']=='a-shiji113-011');self.assertEqual((a['subject_person_id'],a['object_person_id']),('3q4_zsp_jwy','tz9_dhl_ifo'));self.assertEqual(a['predicate'],'sister');order=a['qualifiers']['relative_birth_order'];self.assertEqual((order['older_person_id'],order['younger_person_id']),('3q4_zsp_jwy','tz9_dhl_ifo'))
 def test_table_zhouzao_is_same_fief_not_xiahouzao(self):
  t=load('data/historical-tables/shiji-018.json');c=next(c for f in t['fragments']for r in f['rows']for c in r['cells']if c['id']=='shiji-018-t1-r026-c02');self.assertEqual(c['text'],'七。六年正月丁未，哀侯周灶元年。');self.assertEqual(c['person_mentions'][0]['person_id'],'cnz_t0f_oaz');self.assertEqual(names('cnz_t0f_oaz')['surname'],'周');d=load('corpus/shiji/113-distinctions.json')['distinctions'][0];self.assertEqual(set(d['person_ids']),{'cnz_t0f_oaz','li9_cmb_8ci_A'})
 def test_primary_glyphs_and_parallel_glyphs_remain_separate(self):
  vs={v['id']:v for v in chapter()['annotation']['reported_variants']};self.assertEqual((vs['v-shiji113-zao-glyph']['received_reading'],vs['v-shiji113-zao-glyph']['reported_reading']),('灶','竈'));self.assertEqual((vs['v-shiji113-jiu-surname-glyph']['received_reading'],vs['v-shiji113-jiu-surname-glyph']['reported_reading']),('樛','摎'));self.assertIn('樛氏女',para('p006')['text'])
  for v in vs.values():self.assertFalse(v['adopted']);self.assertFalse(v['image_verified'])
 def test_zhuang_yan_not_fabricated_lifetime_name_change(self):
  n=names('71j_ydc_ly7');self.assertEqual((n['surname'],n['ming']),('莊','助'));self.assertIn('嚴助',n['additional_names']);d=next(d for d in load('corpus/shiji/113-equivalences.json')['decisions']if d['id'].endswith('zhuangzhu'));self.assertIn('天子使嚴助徃諭意南粤王胡',d['references'][0]['quote'])
 def test_retired_ids_removed_from_all_active_sources_and_exports(self):
  olds=['ntz_hml_tl6','hav_xw6_5np','67a_vl4_hwv','jhm_171_fem','hu0_8um_byp','bmn_s2c_y7n','ow5_ebp_tr8','bi1_trt_8y1','dtr_0a5_e27','vj4_k9i_17d','g0x_vmx_2lg','8eg_ctq_fxg','8m2_avf_zfe','yhn_qyw_eq0']
  paths=[R/'registry/persons.json',R/'data/corpus/profile-names.json']+list((R/'corpus').rglob('*.json'))+list((R/'data/historical-tables').glob('*.json'))
  for p in paths:
   text=p.read_text()
   for old in olds:self.assertNotIn(old,text,str(p))
  for old in olds:
   for folder in ['exports/persons','data/corpus/profiles']:self.assertFalse((R/folder/(old+'.json')).exists())
 def test_api_courtesy_name_and_table_links_are_parseable(self):
  b=load('exports/persons/u20_r6q_88g.json');self.assertEqual(b['name_components'][0]['zi'],'少季');b=load('exports/persons/cnz_t0f_oaz.json');self.assertTrue(any(x['table_id']=='shiji-018'for x in b['table_occurrences']))
 def test_courtesy_name_validation_rejects_unsupported_or_mislabelled_name(self):
  from scripts.person_bundle import validate_courtesy_name
  n=names('u20_r6q_88g');validate_courtesy_name(n)
  for change in [{'zi':''},{'zi':3},{'zi':'未見'},{'ming':'少季'},{'references':[]}]:
   with self.subTest(change=change):
    with self.assertRaises(ValueError):validate_courtesy_name(dict(n,**change))
if __name__=='__main__':unittest.main()
