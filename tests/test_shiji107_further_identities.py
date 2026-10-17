import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text())
class FurtherWeiqiIdentities(unittest.TestCase):
 def decisions(self):return [d for d in load('corpus/shiji/107-equivalences.json')['decisions']if d['id'].startswith('eq-shiji107-further-')]
 def test_eight_event_based_equivalences_materialized(self):
  ds=self.decisions();self.assertEqual(len(ds),8)
  self.assertEqual([d['canonical_person_id']for d in ds],['113_odk_emq','3p2_0dm_6ra','27j_f4p_jwp','fmh_dmt_cql','jws_b08_hob','sj9_pfu_fwh_*A','3p2_0dm_6ra','113_odk_emq'])
  for d in ds:self.assertEqual(d['person_ids'],[d['canonical_person_id']]);self.assertTrue(d['identity_materialized']);self.assertFalse(d['human_reviewed']);self.assertIn('c-shiji-107-weiqi',d['chapter_ids'])
 def test_wei_variant_and_predecessor_kept_in_original_text(self):
  a=load('corpus/shiji/107.json')['paragraphs'][4];b=load('corpus/shiji/103.json')['paragraphs'][13];self.assertIn('建陵侯衛綰',a['text']);self.assertIn('建陵侯衞綰',b['text']);self.assertEqual(next(m['person_id']for m in a['mentions']if m['surface']=='建陵侯衛綰'),'113_odk_emq');self.assertEqual(next(m['person_id']for m in b['mentions']if m['surface']=='建陵侯衞綰'),'113_odk_emq')
  p=load('corpus/shiji/011.json')['paragraphs'][14];self.assertEqual(next(m['person_id']for m in p['mentions']if m['surface']=='劉舍'),'3p2_0dm_6ra');self.assertEqual(next(m['person_id']for m in p['mentions']if m['surface']=='御史大夫綰'),'113_odk_emq')
 def test_li_jiangjun_is_guang_not_guangli(self):
  d=self.decisions()[2];self.assertEqual(d['references'][0]['quote'],'李將軍，李廣也。');self.assertFalse(d['references'][0]['image_verified']);p=load('corpus/shiji/107.json')['paragraphs'][19];self.assertEqual(next(m['person_id']for m in p['mentions']if m['surface']=='李將軍'),'27j_f4p_jwp');self.assertNotEqual(d['canonical_person_id'],'fyv_cvv_y5b')
 def test_linru_keeps_unknown_father_and_attested_grandfather(self):
  d=self.decisions()[5];self.assertEqual(d['references'][0]['quote'],'灌嬰孫，名賢也。');p=next(p for p in load('registry/persons.json')['persons']if p['id']=='sj9_pfu_fwh_*A');self.assertEqual(p['family_path']['ancestor_person_id'],'sj9_pfu_fwh');self.assertEqual(p['family_path']['generation_distance'],2);self.assertIsNone(p['family_path'].get('parent_person_id'))
 def test_tingyi_links_both_named_officials(self):
  p=load('corpus/shiji/107.json')['paragraphs'][21];self.assertEqual(next(m['person_id']for m in p['mentions']if m['surface']=='汲黯'),'fmh_dmt_cql');self.assertEqual(next(m['person_id']for m in p['mentions']if m['surface']=='鄭當時'),'jws_b08_hob');self.assertNotEqual('fmh_dmt_cql','6hy_i1z_hu2')
 def test_eight_old_ids_removed_from_registry_and_exports(self):
  ids={p['id']for p in load('registry/persons.json')['persons']}
  for pid in ['ee1_qga_8bw','xwe_h0r_1x4','9vf_qps_lzv','284_zc9_6fx','00r_qjv_0yg','7ib_rwo_tjs','oie_tl5_yxn','bt3_1wn_4hf']:
   self.assertNotIn(pid,ids);self.assertFalse((ROOT/'exports/persons'/f'{pid}.json').exists());self.assertFalse((ROOT/'data/corpus/profiles'/f'{pid}.json').exists())
