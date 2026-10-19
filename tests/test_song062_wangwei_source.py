import unittest,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];J=lambda p:json.loads(p.read_text());C=J(ROOT/'corpus/songshu/062-wangwei.json');A=J(ROOT/'corpus/songshu/062-wangwei-assertions.json')['assertions'];I=J(ROOT/'tests/fixtures/song062-wangwei/person-ids.json')
def at(i,phrase,off=0):
 p=C['paragraphs'][i-1];a=p['text'].index(phrase)+off;return next(m for m in p['mentions']if m['start']==a)
class Song062WangweiSource(unittest.TestCase):
 def test_fixed_complete_body(self):
  b=(ROOT/'tests/fixtures/song062-wangwei/KR2a0016_062.txt').read_bytes();ls=b.decode().splitlines();self.assertEqual(hashlib.sha256(b).hexdigest(),C['source']['response_sha256']);self.assertEqual(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),C['source']['source_blob_sha']);self.assertEqual(C['source']['source_commit'],'e80c057667e3c8684f11d5088251e10244d5a264');t=''.join(p['text']for p in C['paragraphs']);self.assertEqual(t,''.join(l[:-1]for l in ls[82:264]if not l.startswith('<pb:')));self.assertEqual(len(t),3401);self.assertTrue(ls[264].startswith('史臣曰'));self.assertIn('可追贈祕書監',t)
 def test_no_emendment_or_apparatus_in_body(self):
  t=''.join(p['text']for p in C['paragraphs']);self.assertIn('(闕/)',t);self.assertIn('&KR0008;',t);self.assertIn('二十年卒時年二十九',t);self.assertIn('僧謙卒後四句',t);self.assertNotIn('四旬',t);self.assertNotIn('臣承蒼',t);self.assertNotIn('史臣曰',t);self.assertTrue(C['paragraphs'][3]['text'].endswith('且當笑'));self.assertTrue(C['paragraphs'][4]['text'].startswith('微常住'))
 def test_original_fragments_and_anchors(self):
  for p,u in zip(C['paragraphs'],C['source']['normalization']['selected_source_line_units']):
   self.assertEqual(p['text'],''.join(f['selected_text']for f in u['source_fragments']));end=0
   for f in u['source_fragments']:self.assertEqual(f['selected_text'],f['source_text'][f['source_start']:f['source_end']]);self.assertEqual(hashlib.sha256(f['source_text'].encode()).hexdigest(),f['source_line_sha256'])
   for m in p['mentions']:self.assertGreaterEqual(m['start'],end);self.assertEqual(p['text'][m['start']:m['end']],m['surface']);end=m['end']
  self.assertEqual(sum(len(p['mentions'])for p in C['paragraphs']),241)
 def test_three_letter_addressees_not_one_nearest_name(self):
  self.assertEqual(at(2,'弟心病亂')['person_id'],I['wei']);self.assertEqual(at(2,'君多識')['person_id'],I['jiang']);self.assertEqual(at(3,'吾雖')['person_id'],I['wei']);self.assertEqual(at(3,'弟每共')['person_id'],I['sc']);self.assertEqual(at(4,'卿昔')['person_id'],I['he']);self.assertEqual(at(5,'弟年十五')['person_id'],I['qian']);self.assertEqual(at(5,'又兄為人',1)['person_id'],I['wei']);self.assertEqual(at(2,'兄守金城')['person_id'],I['olderbro']);self.assertNotEqual(I['olderbro'],I['wei'])
 def test_nested_ancient_quote_and_collective(self):
  self.assertEqual(at(2,'生我名者',1)['person_id'],I['junping']);self.assertEqual(at(2,'殺我身',1)['person_id'],I['junping']);self.assertIsNone(at(3,'兄弟尤為')['person_id']);self.assertIsNone(at(4,'王樂')['person_id']);self.assertEqual(at(5,'誰復視我',3)['person_id'],I['wei']);self.assertFalse(any(m['surface']=='操'for p in C['paragraphs']for m in p['mentions']))
 def test_corrupt_allusions_not_forced_into_names(self):
  for i,x in [(2,'管叔'),(2,'衞賜'),(5,'謝能思之'),(5,'左率'),(5,'第五兒'),(5,'劉新婦'),(5,'殷太妃')]:self.assertIsNone(at(i,x)['person_id'])
  self.assertEqual(at(2,'山公')['person_id'],I['shan']);self.assertEqual(at(2,'仲容')['person_id'],I['ruanxian']);self.assertEqual(at(2,'中散')['person_id'],I['jikang']);self.assertEqual(at(3,'林宗')['person_id'],I['linzong'])
 def test_direct_six_relations_and_no_invented_parent(self):
  self.assertEqual(len(A),6);father=[a for a in A if a['predicate']=='father'];self.assertEqual([(a['subject_person_id'],a['object_person_id'])for a in father],[(I['wei'],I['ru'])]);self.assertFalse(any(a['predicate']in ['mother','spouse','adoptive_father','ritual_successor_of']for a in A));self.assertFalse(any(a['predicate']=='father'and a['subject_person_id']==I['qian']for a in A));self.assertTrue(all(not a['human_reviewed']for a in A))
 def test_071_identity_and_qian_distinction(self):
  d=J(ROOT/'corpus/songshu/062-wangwei-identities.json')['decisions'][0];self.assertEqual(d['person_id'],'7r6_k52_qji_ABAAAADA');self.assertIn('c-songshu-071-wangsengchuo',d['chapter_ids']);dd=J(ROOT/'corpus/songshu/062-wangwei-distinctions.json')['distinctions'][0];self.assertIn(I['qian'],dd['person_ids']);self.assertEqual(len(set(dd['person_ids'])),2);self.assertNotEqual(I['wei'],'d8d_ced_96e')
 def test_no_fact_or_rekey_side_effect(self):
  r=J(ROOT/'registry/persons.json');p=next(p for p in r['persons']if p['id']==I['wei']);self.assertEqual(p['id'],'7r6_k52_qji_ABAAAADA');self.assertFalse(C['source']['image_verified']);self.assertFalse(C['annotation']['human_reviewed']);self.assertTrue(all(a['human_reviewed']is False for a in A));self.assertFalse(any(x.get('predicate')=='father'and x['subject_person_id']in[I['olderbro'],I['oldersis'],I['qian']]for x in A))
if __name__=='__main__':unittest.main()
