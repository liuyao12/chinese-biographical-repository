import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OLD=['ttc_nht_1ih', 'trv_ybp_bes', 'jgl_hok_5v6', 'tod_lbz_fbe', '7l9_yz7_nwv', 'n9g_zzh_3ss', 'wai_hue_j42', 'ugq_ldt_klj', 'kxl_a6t_r9a', 'kru_906_knc', 'a82_krd_hlg', '8dm_xw2_ci8', '253_2n7_qs7', 'q29_h9w_sah', '31b_36a_313', 'eep_7t4_31w', 'orq_rdx_tgp', '052_eu1_tdb', 'onk_jwj_o75']
def read(f):return json.loads((ROOT/f).read_text())
def para(n,key):return next(p for p in read('corpus/shiji/'+n+'.json')['paragraphs'] if p['id'].endswith(':'+key))
class YuanChaoCoreIdentityTests(unittest.TestCase):
 def test_contextual_titles_and_emperor_change_are_specific(self):
  for key,surface,pid in [('p002','絳侯','koy_6jg_gcc'),('p009','吳王','yqp_nlb_p1p_CA'),('p015','梁王','yqp_nlb_p1p_ACG'),('p021','上','yqp_nlb_p1p_ACAA')]:
   self.assertEqual({m['person_id'] for m in para('101',key)['mentions'] if m['surface']==surface},{pid})
  self.assertEqual({m['person_id'] for m in para('101','p020')['mentions'] if m['surface']=='上'},{'yqp_nlb_p1p_ACA'})
 def test_fifteen_decisions_and_nineteen_retired_ids(self):
  ds=[d for d in read('corpus/shiji/101-equivalences.json')['decisions'] if d['id'].startswith('eq-shiji101-core-')];self.assertEqual(len(ds),15)
  for d in ds:self.assertTrue(d['identity_materialized']);self.assertEqual(d['person_ids'],[d['canonical_person_id']]);self.assertFalse(d['human_reviewed']);self.assertEqual(d['status'],'contextual_provisional')
  self.assertFalse(set(OLD)&{p['id'] for p in read('registry/persons.json')['persons']})
  for pid in OLD:
   for folder in ['data/corpus/profiles','exports/persons']:self.assertFalse((ROOT/folder/(pid+'.json')).exists())
 def test_mothers_merge_by_same_child_and_event_not_by_title(self):
  for n,key,surface,pid in [('101','p005','太后','9zj_vf7_86a_A'),('057','p010','薄太后','9zj_vf7_86a_A'),('118','p002','薄太后','9zj_vf7_86a_A'),('101','p008','皇后','ixk_6fg_v6f_A'),('058','p001','竇太后','ixk_6fg_v6f_A')]:
   self.assertEqual({m['person_id'] for m in para(n,key)['mentions'] if m['surface']==surface},{pid})
  self.assertNotEqual('9zj_vf7_86a_A','ixk_6fg_v6f_A')
  for n,key,surface in [('101','p014','母'),('124','p007','劇孟母')]:self.assertEqual(next(m['person_id'] for m in para(n,key)['mentions'] if m['surface']==surface),'qel_t1a_itz')
 def test_liu_li_homonyms_and_yuan_family_remain_distinct(self):
  self.assertEqual(next(m['person_id'] for m in para('101','p016')['mentions'] if m['surface']=='劉禮'),'6ds_5ek_8sw')
  self.assertEqual(next(m['person_id'] for m in para('101','p014')['mentions'] if m['surface']=='禮'),'yqp_nlb_p1p_DB')
  self.assertEqual(next(m['person_id'] for m in para('101','p001')['mentions'] if m['surface']=='噲'),'vv0_3wv_i18')
  self.assertFalse(any(a['predicate']=='father' and a['subject_person_id']=='c6v_07v_vxz' and a['object_person_id']=='vv0_3wv_i18' for a in read('corpus/shiji/101-assertions.json')['assertions']))
 def test_benyu_decomposition_preserves_old_start_and_adds_second_person(self):
  ms=para('101','p005')['mentions'];a=next(m for m in ms if m['id']=='c-shiji-101-yuanchao:m005-0182');b=next(m for m in ms if m['id']=='c-shiji-101-yuanchao:m005-0183')
  self.assertEqual((a['surface'],a['person_id'],a['start'],a['end']),('賁','dwv_5hn_680',182,183));self.assertEqual((b['surface'],b['person_id'],b['start'],b['end']),('育','66l_m67_5ie',183,184))
  ds=[d for d in read('corpus/shiji/101-identities.json')['decisions'] if d['id'].startswith('d-shiji101-benyu-')];self.assertEqual(len(ds),2)
  for d in ds:self.assertEqual(d['references'][0]['quote'],'孟賁、夏育，皆古勇者也。');self.assertEqual(d['references'][0]['revision_id'],2514771);self.assertFalse(d['references'][0]['image_verified'])
 def test_commentary_and_reported_variant_do_not_rewrite_names(self):
  ids=read('corpus/shiji/101-identities.json')['decisions']
  for pid,quote in [('epn_7nx_g1b','先即先生。'),('w2n_7g1_30z','棓，姓也。')]:
   d=next(d for d in ids if d['person_id']==pid);self.assertTrue(any(r['quote']==quote and r['revision_id']==2514771 for r in d['references']))
  v=next(v for v in read('corpus/shiji/101.json')['annotation']['reported_variants'] if v['source_term']=='棓生');self.assertFalse(v['adopted']);self.assertEqual((v['received_reading'],v['reported_reading']),('棓','服'))
  p=next(p for p in read('registry/persons.json')['persons'] if p['id']=='w2n_7g1_30z');self.assertNotIn('服生',{a['surface'] for a in p['aliases']})
 def test_received_spelling_and_fixed_witness_are_preserved(self):
  c=read('corpus/shiji/101.json');self.assertEqual(c['source']['revision_id'],368092);self.assertEqual(len(c['paragraphs']),23)
  self.assertIn('清室',para('101','p003')['text']);self.assertIn('張恢先所',para('101','p016')['text']);self.assertIn('棓生',para('101','p015')['text']);self.assertIn('朝錯',para('101','p023')['text'])
