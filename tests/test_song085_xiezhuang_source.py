# coding: utf-8
import unittest,json,sys,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.person_bundle import load_catalog,bundle
from scripts.render_corpus import render
J=lambda p:json.loads(p.read_text());F=ROOT/'tests/fixtures/song085-xiezhuang';D=J(ROOT/'corpus/songshu/085-xiezhuang.json');IDS=J(F/'ids.json');I={**IDS['existing'],**IDS['new']}
class XiezhuangSource(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.cat=load_catalog(ROOT);cls.rows=J(ROOT/'corpus/songshu/085-xiezhuang-assertions.json')['assertions']
 def test_actual_volume_and_full_biography(self):
  raw=(F/'KR2a0016_085.txt').read_text().splitlines();self.assertEqual(raw[5],'#+PROPERTY: JUAN 卷八十五');self.assertTrue(raw[252].startswith('王景文'));u=J(F/'units.json');self.assertEqual((len(u),sum(len(p['text']) for p in D['paragraphs'])),(15,4455));self.assertTrue(u[0]['text'].startswith('謝莊字希逸'));self.assertTrue(u[-1]['text'].endswith('追贈金紫光禄大夫'))
  for x,p in zip(u,D['paragraphs']):self.assertEqual(x['text'],p['text']);self.assertEqual(''.join(f['selected_text'] for f in x['source_fragments']),p['text'])
 def test_fixed_receipt_and_xml(self):
  self.assertEqual(D['source']['source_commit'],'e80c057667e3c8684f11d5088251e10244d5a264');self.assertEqual(D['source']['response_sha256'],hashlib.sha256((F/'KR2a0016_085.txt').read_bytes()).hexdigest());self.assertFalse(D['source']['image_verified']);self.assertEqual((ROOT/'corpus/songshu/085-xiezhuang.xml').read_text(),render(D))
 def test_exact_anchors_and_raw_glyphs(self):
  self.assertEqual(sum(len(p['mentions']) for p in D['paragraphs']),193)
  for p in D['paragraphs']:
   end=0
   for m in p['mentions']:self.assertGreaterEqual(m['start'],end);self.assertEqual(p['text'][m['start']:m['end']],m['surface']);end=m['end']
  text=''.join(p['text'] for p in D['paragraphs'])
  for s in ['宏微','王徽','張㪍','張竒','颺','獯檢','已心']:self.assertIn(s,text)
 def test_existing_zhuang_and_hongwei_not_duplicated(self):
  self.assertEqual(I['謝莊'],'aa6_83c_juy_DBABA');self.assertEqual(I['謝弘微'],'aa6_83c_juy_DBAB');a=next(a for a in self.rows if a['subject_person_id']==I['謝莊']);self.assertEqual((a['predicate'],a['object_person_id']),('father',I['謝弘微']));self.assertFalse(any(p['label']=='宏微' for p in self.cat[0].values()))
 def test_issued_duji_reused(self):self.assertEqual(I['杜畿'],'56f_8f7_e9f');self.assertIn('56f_8f7_e9f',self.cat[0]);self.assertNotIn('杜畿',IDS['new'])
 def test_eldest_son_explicit_not_id_order(self):
  a=next(a for a in self.rows if a['subject_person_id']==I['謝颺']);self.assertEqual(a['object_person_id'],I['謝莊']);self.assertEqual(a['qualifiers']['birth_order']['ordinal'],1)
 def test_empress_is_yang_daughter_not_zhuang_daughter(self):
  aa=[a for a in self.rows if a['subject_person_id']==I['順帝皇后（颺女，未名）']];self.assertEqual(next(a for a in aa if a['predicate']=='father')['object_person_id'],I['謝颺']);self.assertEqual(next(a for a in aa if a['predicate']=='spouse')['object_person_id'],I['宋順帝']);self.assertFalse(any(a['predicate']=='mother' for a in aa))
 def test_quoted_han_mother_not_song_consort(self):
  a=next(a for a in self.rows if a['predicate']=='mother');self.assertEqual((a['subject_person_id'],a['object_person_id']),(I['漢昭帝'],I['趙婕妤']));self.assertNotEqual(a['object_person_id'],I['殷貴妃'])
 def test_wanghui_and_yuankai_unresolved(self):
  for s in ['王徽','元凱']:
   m=next(m for p in D['paragraphs'] for m in p['mentions'] if m['surface']==s);self.assertIsNone(m['person_id'])
  self.assertEqual(next(m for p in D['paragraphs'] for m in p['mentions'] if m['surface']=='王徽')['candidate_person_ids'],['d8d_ced_96e'])
 def test_song_suiwang_not_nanqi_suiwang(self):self.assertNotEqual(I['隨王誕'],'4tg_ud8_zdy');self.assertTrue(any(m['surface']=='竟陵王誕' and m['person_id']==I['隨王誕'] for p in D['paragraphs'] for m in p['mentions']))
 def test_quoted_and_narrative_emperors_separate(self):
  ms=[m for p in D['paragraphs'] for m in p['mentions']];self.assertTrue(any(m['surface']=='武帝' and m['person_id']==I['漢武帝'] for m in ms));self.assertTrue(any(m['surface']=='世祖' and m['person_id']==I['宋世祖'] for m in ms));self.assertNotEqual(I['前廢帝'],I['宋太宗'])
 def test_no_age_inferred_birth_or_title_end_dates(self):
  self.assertFalse(any(k in D['annotation'] for k in ['birth_year','life_events','title_holdings']));self.assertTrue(any('年四十六' in p['text'] for p in D['paragraphs']));self.assertFalse(any(a['predicate']=='mother' and a['subject_person_id']==I['謝莊'] for a in self.rows))
 def test_all_new_bundle_in_memory(self):
  for pid in IDS['new'].values():
   x=bundle(pid,root=ROOT,catalog=self.cat,include_provisional=True);self.assertEqual(x['canonical_person_id'],pid);self.assertTrue(x['mentions'])
 def test_human_review_flags_not_claimed(self):
  self.assertFalse(D['annotation']['human_reviewed']);self.assertTrue(all(a['human_reviewed'] is False for a in self.rows));fs=J(ROOT/'registry/family-assemblies.json');self.assertFalse(next(m for f in fs['assemblies'] for m in f['members'] if m['person_id']=='4qr_wrk_3vd_DDBB')['parent_connection']['human_reviewed'])
if __name__=='__main__':unittest.main()
