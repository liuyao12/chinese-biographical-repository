# coding: utf-8
import unittest,json,hashlib,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];J=lambda p:json.loads(p.read_text());C=J(ROOT/'corpus/songshu/071-wangsengchuo.json');A=J(ROOT/'corpus/songshu/071-wangsengchuo-assertions.json')['assertions'];I=J(ROOT/'tests/fixtures/song071-wangsengchuo/person-ids.json')
def at(i,phrase,off=0):
 p=C['paragraphs'][i-1];s=p['text'].index(phrase)+off;return next(m for m in p['mentions']if m['start']==s)
class Song071WangsengchuoSource(unittest.TestCase):
 def test_fixed_commit_blob_and_complete_body(self):
  b=(ROOT/'tests/fixtures/song071-wangsengchuo/KR2a0016_071.txt').read_bytes();self.assertEqual(hashlib.sha256(b).hexdigest(),C['source']['response_sha256']);self.assertEqual(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),C['source']['source_blob_sha']);self.assertEqual(C['source']['source_commit'],'e80c057667e3c8684f11d5088251e10244d5a264');lines=b.decode().splitlines();body=''.join(x[:-1]for x in lines[170:216]if not x.startswith('<pb:'));self.assertEqual(''.join(p['text']for p in C['paragraphs']),body);self.assertEqual(len(body),853);self.assertTrue(body.endswith('子儉嗣昇明末為齊國尚書右僕射'));self.assertTrue(lines[216].startswith('史臣曰'));self.assertEqual(lines[240],'#+PROPERTY: JUAN 卷七十一考證')
 def test_every_source_fragment_is_original_and_no_wiki_emendment(self):
  lines=(ROOT/'tests/fixtures/song071-wangsengchuo/KR2a0016_071.txt').read_text().splitlines();units=C['source']['normalization']['selected_source_line_units'];self.assertEqual(len(units),len(C['paragraphs']))
  for u,p in zip(units,C['paragraphs']):
   self.assertEqual(''.join(z['selected_text']for z in u['source_fragments']),p['text'])
   for f in u['source_fragments']:self.assertEqual(f['source_text'],lines[f['line']-1]);self.assertEqual(f['selected_text'],f['source_text'][f['source_start']:f['source_end']]);self.assertEqual(hashlib.sha256(f['source_text'].encode()).hexdigest(),f['source_line_sha256'])
  text=''.join(p['text']for p in C['paragraphs']);self.assertIn('從兄徽',text);self.assertIn('豫章縣侯',text);self.assertIn('臧夀',text);self.assertNotIn('從兄微',text);self.assertNotIn('豫寧縣侯',text);self.assertNotIn('臣承蒼',text);self.assertNotIn('史臣曰',text)
 def test_exact_nonoverlap_mentions(self):
  for p in C['paragraphs']:
   end=0
   for m in p['mentions']:self.assertGreaterEqual(m['start'],end);self.assertEqual(p['text'][m['start']:m['end']],m['surface']);end=m['end']
  self.assertEqual(sum(len(p['mentions'])for p in C['paragraphs']),97)
 def test_speech_humility_not_brothers_and_correct_addressee(self):
  self.assertEqual(at(1,'曰弟名位',1)['person_id'],I['sc']);self.assertEqual(at(3,'曰弟亦恨君',1)['person_id'],I['sc']);self.assertEqual(at(3,'曰弟亦恨君',4)['person_id'],I['jiang']);self.assertFalse(any(a['predicate']in['brother','sister']and I['sc']in[a['subject_person_id'],a['object_person_id']]for a in A))
 def test_collective_princes_and_uncertain_brother_child_not_single(self):
  for i in [3,4]:
   m=at(i,'二凶');self.assertIsNone(m['person_id']);self.assertEqual(set(m['candidate_person_ids']),{I['shao'],I['jun']})
  for ph,off in [('庶人',0),('唯能裁弟',3),('不能裁兒',3)]:self.assertIsNone(at(3,ph,off)['person_id'])
  self.assertEqual(set(at(3,'不能裁兒',3)['candidate_person_ids']),{I['shao'],I['jun']})
 def test_contemporary_king_and_yuan_not_forced(self):
  self.assertIsNone(at(1,'始興王文學')['person_id']);self.assertEqual(at(1,'始興王濬')['person_id'],I['jun']);self.assertIsNone(at(5,'袁悅')['person_id']);self.assertNotEqual(I['wei'],'d8d_ced_96e');self.assertNotEqual(I['jun'],'36c_6b6_4b3');self.assertNotEqual(I['shao'],'9b1_c61_00c')
 def test_two_princes_wives_and_two_fathers_not_mixed(self):
  by={x['id']:x for x in A};self.assertEqual(by['a-song071-sengchuo-007']['subject_person_id'],I['xu_daughter']);self.assertEqual(by['a-song071-sengchuo-007']['object_person_id'],I['xu']);self.assertEqual(by['a-song071-sengchuo-009']['subject_person_id'],I['jiang_sister']);self.assertEqual(by['a-song071-sengchuo-009']['object_person_id'],I['jiang']);self.assertEqual(by['a-song071-sengchuo-008']['object_person_id'],I['dan']);self.assertEqual(by['a-song071-sengchuo-010']['object_person_id'],I['shuo'])
 def test_existing_jian_retained_and_no_biological_mother_invented(self):
  a=next(x for x in A if x['id']=='a-song071-sengchuo-006');self.assertEqual(a['subject_person_id'],'7r6_k52_qji_ABAAAAEAA');self.assertEqual(a['object_person_id'],I['sc']);self.assertIn('僧綽常以正逹',a['evidence'][0]['quote']);self.assertTrue(a['evidence'][0]['quote'].endswith('子儉嗣昇明末為齊國尚書右僕射'));self.assertFalse(any(x['predicate']in['mother','adoptive_father']for x in A))
 def test_cousin_uses_original_hui_and_does_not_assert_unknown_father(self):
  a=next(x for x in A if x['predicate']=='agnatic_cousin');self.assertEqual(a['subject_person_id'],I['wei']);self.assertEqual(a['object_person_id'],I['sc']);self.assertEqual(a['qualifiers']['source_term'],'從兄徽');self.assertIsNone(a['qualifiers']['kinship_structure']['common_ancestor_person_id']);self.assertFalse(any(x['predicate']=='father'and x['subject_person_id']==I['wei']for x in A))
 def test_variant_reading_and_old_jin_hui_are_formally_separated(self):
  d=J(ROOT/'corpus/songshu/071-wangsengchuo-identities.json')['decisions'];v=C['annotation']['reported_variants'][0];self.assertEqual(v['received_reading'],'徽');self.assertEqual(v['reported_reading'],'微');self.assertFalse(v['adopted']);self.assertIn('孺',v['quote']);self.assertTrue(d[0]['preferred_reading']['source_spelling_is_not_alias']);self.assertEqual(d[0]['preferred_reading']['variant_id'],v['id']);self.assertEqual(d[1]['person_id'],'7r6_k52_qji_ABAAAAEAA');self.assertGreaterEqual(len(d[1]['chapter_ids']),3);dist=J(ROOT/'corpus/songshu/071-wangsengchuo-distinctions.json')['distinctions'][0];self.assertEqual(set(dist['person_ids']),{I['wei'],'d8d_ced_96e'})
 def test_three_age_numbers_do_not_create_births_or_title_ends(self):
  text=''.join(p['text']for p in C['paragraphs']);self.assertIn('年十三',text);self.assertIn('時年二十九',text);self.assertIn('時年三十一',text);self.assertFalse(C['source']['image_verified']);self.assertFalse(C['annotation']['human_reviewed']);self.assertTrue(all(x['human_reviewed']is False for x in A))
if __name__=='__main__':unittest.main()
