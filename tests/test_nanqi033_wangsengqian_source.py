import unittest,json,re,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];J=lambda p:json.loads(p.read_text());C=J(ROOT/'corpus/nanqishu/033-wangsengqian.json');N=J(ROOT/'corpus/nanshi/022-wangzhi.json');A=J(ROOT/'corpus/nanqishu/033-wangsengqian-assertions.json')['assertions'];B=J(ROOT/'corpus/nanshi/022-wangzhi-assertions.json')['assertions'];I=J(ROOT/'tests/fixtures/nanqi033-wangsengqian/person-ids.json')
def at(i,term,off=0):
 p=C['paragraphs'][i-1];a=p['text'].index(term)+off;return next(m for m in p['mentions']if m['start']==a)
class Nanqi033WangsengqianSource(unittest.TestCase):
 def test_fixed_complete_units_not_heading_or_apparatus(self):
  for c,name,start,end,size in [(C,'KR2a0017_033.txt',13,215,3772),(N,'KR2a0024_022.txt',469,498,560)]:
   b=(ROOT/'tests/fixtures/nanqi033-wangsengqian'/name).read_bytes();self.assertEqual(hashlib.sha256(b).hexdigest(),c['source']['response_sha256']);self.assertEqual(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),c['source']['source_blob_sha']);text=''.join(re.sub(r'<pb:[^>]+>|¶','',l)for l in b.decode().splitlines()[start-1:end]);self.assertEqual(text,''.join(p['text']for p in c['paragraphs']));self.assertEqual(len(text),size);self.assertFalse(c['source']['image_verified']);self.assertFalse(c['annotation']['human_reviewed'])
  self.assertTrue(N['paragraphs'][0]['text'].endswith('志弟揖位太中大夫揖子筠'));self.assertNotIn('筠字元禮',N['paragraphs'][0]['text']);self.assertNotIn('考證',''.join(p['text']for p in C['paragraphs']))
 def test_all_anchors_exact_nonoverlap(self):
  for c in [C,N]:
   for p in c['paragraphs']:
    end=0
    for m in p['mentions']:self.assertGreaterEqual(m['start'],end);self.assertEqual(p['text'][m['start']:m['end']],m['surface']);end=m['end']
 def test_three_letters_different_speakers(self):
  self.assertEqual(at(7,'僕一門')['person_id'],I['tan']);self.assertEqual(at(7,'吾與足下')['person_id'],I['sq']);self.assertEqual(at(7,'吾與足下',2)['person_id'],I['tan']);self.assertEqual(at(7,'使僕就此職',1)['person_id'],I['tan']);self.assertEqual(at(7,'尚書婦是')['person_id'],I['sq'])
 def test_nested_quotes_do_not_use_nearest_person(self):
  self.assertEqual(at(14,'弟書遂不減')['person_id'],I['qia']);self.assertEqual(at(14,'不減吾',2)['person_id'],I['xizhi']);self.assertEqual(at(14,'弟書如騎')['person_id'],I['min']);self.assertEqual(at(14,'緊媚其父',2)['person_id'],I['xichao']);self.assertEqual(at(14,'緊媚其父',3)['person_id'],I['xiyin']);self.assertEqual(at(15,'客多歸之',3)['person_id'],I['ji'])
 def test_care_allusions_are_not_adoption(self):
  self.assertFalse(any(a['predicate']in['adoptive_father','ritual_successor_of']for a in A+B));self.assertTrue(any(a['predicate']=='paternal_uncle'and a['subject_person_id']==I['jian']and a['object_person_id']==I['sq']for a in A));self.assertIsNone(at(3,'弟子更逾')['person_id']);self.assertIsNone(at(7,'二子勲䕃')['person_id'])
 def test_ninth_son_and_relative_older_brother(self):
  a=next(a for a in A if a['predicate']=='father'and a['subject_person_id']==I['ji']);self.assertEqual(a['qualifiers']['birth_order']['ordinal'],9);self.assertEqual(a['context']['kind'],'adjacent_paragraphs');self.assertEqual(len(a['evidence']),2);self.assertEqual(a['object_person_id'],I['sq']);self.assertFalse(any('birth_order'in a['qualifiers']for a in A+B if a['subject_person_id']==I['zhi']))
 def test_zhi_father_belongs_to_independent_nanshi(self):
  self.assertFalse(any(a['predicate']=='father'and a['subject_person_id']==I['zhi']for a in A));a=next(a for a in B if a['predicate']=='father'and a['subject_person_id']==I['zhi']);self.assertEqual(a['object_person_id'],I['sq']);self.assertEqual(a['status'],'source_attested');self.assertEqual(a['evidence'][0]['source_id'],N['source_id']);self.assertIn('謂其父僧虔',a['evidence'][0]['quote'])
 def test_mothers_wives_and_five_sons_not_inferred(self):
  mothers=[a for a in A+B if a['predicate']=='mother'];self.assertEqual(len(mothers),1);self.assertEqual(mothers[0]['subject_person_id'],I['zhi']);self.assertEqual(mothers[0]['object_person_id'],I['mother']);self.assertNotEqual(I['mother'],I['wife']);children=[a for a in B if a['predicate']=='father'and a['object_person_id']==I['zhi']];self.assertEqual(len(children),5);self.assertFalse(any('birth_order'in a['qualifiers']for a in children));self.assertFalse(any(a['predicate']=='mother'and a['object_person_id']==I['princess']for a in A+B))
 def test_same_names_and_uncertain_addressee(self):
  self.assertNotEqual(I['masong'],'50b_399_d54');self.assertNotEqual(I['rong'],'7r6_k52_qji_A');self.assertNotEqual(I['xiyin'],'215_e1c_3e3');self.assertEqual(at(16,'阿越')['person_id'],I['sq']);self.assertIsNone(at(16,'張吳興')['person_id']);self.assertTrue(all(m['person_id']is None for m in C['paragraphs'][15]['mentions']if m['surface']=='汝'));self.assertIn('郗惜',C['paragraphs'][13]['text']);self.assertTrue(all(m.get('candidate_set_complete')is False for m in C['paragraphs'][15]['mentions']if m['surface']=='汝'))
if __name__=='__main__':unittest.main()
