"""Source-specific regressions; only repository native files, no private helper paths."""
import unittest,json,hashlib
from pathlib import Path
from scripts.houhan_text_layers import layer_errors
R=Path(__file__).resolve().parents[1]
class Sanguozhi027WangchangSource(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=json.loads((R/'corpus/sanguozhi/027-wangchang.json').read_text());cls.ps={p['id'].split(':')[-1]:p for p in cls.c['paragraphs']};cls.aset=json.loads((R/'corpus/sanguozhi/027-wangchang-assertions.json').read_text())['assertions']
 def test_full_eighteen_ordered_layers(self):
  self.assertEqual([p['id'].split(':')[-1]for p in self.c['paragraphs'][:18]],[f'unit{i:03}'for i in range(1,19)]);self.assertEqual(sum(len(p['text'])for p in self.c['paragraphs'][:18]),3245)
 def test_nine_pei_not_chen_body(self):
  self.assertEqual(sum(p['text_layer']=='witness_appended_pei_songzhi_note'for p in self.c['paragraphs']),9)
 def test_all_anchors_unicode_exact(self):
  for p in self.c['paragraphs']:
   last=0
   for m in p['mentions']:self.assertEqual(p['text'][m['start']:m['end']],m['surface']);self.assertGreaterEqual(m['start'],last);last=m['end']
 def test_qing_independent_not_pei(self):
  p=self.ps['qing-collation'];self.assertEqual(p['text_layer'],'witness_appended_qing_siku_collation');self.assertEqual(layer_errors(p),[]);self.assertIn('苑疑作宛',p['text'])
 def test_qing_wrong_author_rejected(self):
  import copy
  p=copy.deepcopy(self.ps['qing-collation']);p['layer_attribution']['attributed_author']='裴松之';self.assertTrue(layer_errors(p))
 def test_raw_unchanged_and_fragments_exact(self):
  raw=(R/self.c['source']['raw_path']).read_bytes();self.assertEqual(hashlib.sha256(raw).hexdigest(),'022fc5dba059f0b330510848ef58d10b96ce10fc09a466c73cf45aaf52139998');lines=raw.decode().splitlines()
  for p in self.c['paragraphs'][:18]:self.assertEqual(''.join(lines[f['line']-1][f['raw_start']:f['raw_end']]for f in p['source_position']['source_fragments']),p['text'])
 def test_shen_variant_same_id_not_new_father(self):
  self.assertTrue(any(m['surface']=='沉'and m['person_id']=='175_99c_b41_AA'for m in self.ps['unit005']['mentions']));self.assertFalse(any(a['subject_person_id']=='175_99c_b41_AA'and a['predicate']=='father'for a in self.aset))
 def test_wangji_not_langya_shixian(self):
  ms=[m for p in self.c['paragraphs']for m in p['mentions']if m['surface']=='王基'];self.assertTrue(ms);self.assertTrue(all(m['person_id']!='7r6_k52_qji_ABB'for m in ms))
 def test_mo_and_shen_source_local_not_cross_source_identity(self):
  for p in self.c['paragraphs']:
   for m in p['mentions']:
    if m['surface']in ['黙','深']:
     self.assertEqual(m['kind'],'person');self.assertEqual(m['status'],'contextual_provisional');self.assertNotIn(m['person_id'],['566_8c0_c6c','b2a_88b_095','7r6_k52_qji_ABAAAABA'])
 def test_no_brother_assertion_from_xiongshi(self):
  self.assertIn('兄事之',self.ps['unit003']['text']);self.assertFalse(any(a['predicate']=='brother'for a in self.aset))
 def test_guoboyi_source_local_not_unproved_jin_guoyi(self):
  for p in self.c['paragraphs']:
   for m in p['mentions']:
    if m['surface']in ['郭伯益','伯益','奕']:
     self.assertEqual(m['kind'],'person');self.assertEqual(m['status'],'contextual_provisional');self.assertNotEqual(m['person_id'],'r02_hoi_pu7_ACA')
 def test_ordinary_characters_not_people(self):
  p=self.ps['unit017']
  for q in ['治績','節儉']:
   i=p['text'].index(q);self.assertFalse(any(i<=m['start']<i+2 for m in p['mentions']))
  p=self.ps['unit005'];i=p['text'].index('玄黙');self.assertFalse(any(i<=m['start']<i+2 for m in p['mentions']))
 def test_no_titles_dates_or_death_termination(self):
  self.assertNotIn('life_events',self.c['annotation']);self.assertNotIn('title_holdings',self.c['annotation']);self.assertIn('甘露四年薨',self.ps['unit017']['text']);self.assertIn('孫臏佐趙直湊大梁',self.ps['unit017']['text'])
if __name__=='__main__':unittest.main()
