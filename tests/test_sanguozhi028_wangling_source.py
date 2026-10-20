# coding: utf-8
import json,unittest,hashlib,xml.etree.ElementTree as ET
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def j(n):return json.loads((R/n).read_text())
class WanglingSource(unittest.TestCase):
 def setUp(self):self.c=j('corpus/sanguozhi/028-wangling.json');self.ps={p['id'].split(':')[-1]:p for p in self.c['paragraphs']}
 def test_full_extent_layers_and_raw(self):
  self.assertEqual(len(self.ps),20);self.assertEqual(sum(len(p['text'])for p in self.ps.values()),2591);self.assertTrue(self.ps['unit001']['text'].startswith('王凌字彦雲'));self.assertTrue(self.ps['unit016']['text'].endswith('親家告吏乃就執之'));self.assertEqual(hashlib.sha256((R/self.c['source']['raw_path']).read_bytes()).hexdigest(),self.c['source']['raw_file_sha256']);self.assertEqual(len([p for p in self.ps.values()if p['text_layer']=='witness_appended_qing_siku_collation']),2)
 def test_xml_text_and_unicode_endpoints(self):
  xp=ET.parse(R/'corpus/sanguozhi/028-wangling.xml').getroot().findall('p');self.assertEqual([''.join(p.itertext())for p in xp],[p['text']for p in self.c['paragraphs']])
  for p in self.c['paragraphs']:
   end=0
   for m in p['mentions']:self.assertGreaterEqual(m['start'],end);self.assertEqual(p['text'][m['start']:m['end']],m['surface']);end=m['end']
 def test_wang_ling_and_yun_no_rekey_or_guessed_father(self):
  a=j('corpus/sanguozhi/028-wangling-assertions.json')['assertions'];self.assertTrue(any(x['subject_person_id']=='f89_ad1_61d'and x['object_person_id']=='8xv_6ak_y28'and x['predicate']=='paternal_uncle'for x in a));self.assertFalse(any(x['subject_person_id']=='f89_ad1_61d'and x['predicate']=='father'for x in a));self.assertEqual(len([x for x in a if x['id'] in ['a-sanguozhi028-wangling-00'+str(i) for i in range(1,6)]]),5);self.assertEqual(len(a),6);self.assertTrue(any(x['predicate']=='maternal_uncle' and x['subject_person_id']=='43d_e5c_69f' and x['object_person_id']=='f89_ad1_61d' for x in a))
 def test_source_variant_and_disputed_speech_preserved(self):
  self.assertIn('郭氾',self.ps['unit001']['text']);self.assertIn('臣松之以為',self.ps['unit004']['text']);self.assertIn('疑悉鑿齒所自造者也',self.ps['unit004']['text']);self.assertIn('令狐及乎',self.ps['unit012']['text']);self.assertIn('及字不可觧疑為反字之誤',self.ps['qing-02']['text'])
 def test_scoped_alias_bridges(self):
  expected={'子師':'8xv_6ak_y28','何平叔':'816_5bc_7b5','賈梁道':'47f_f5a_441'}
  for term,pid in expected.items():self.assertTrue(any(m['surface']==term and m['person_id']==pid for p in self.ps.values()for m in p['mentions']))
 def test_ambiguous_sequence_and_group_not_forced(self):
  for term in ['飛梟金虎','眀山','丁畢桓鄧']:self.assertTrue(any(m['surface']==term and m['kind']=='unresolved'and m['person_id']is None for p in self.ps.values()for m in p['mentions']))
 def test_letter_zi_addresses_taifu_not_biological_son(self):
  p=self.ps['unit010'];st=p['text'].index('活我者子')+3;m=next(m for m in p['mentions']if m['start']==st);self.assertEqual(m['person_id'],'dkn_ge4_286_AAAA')
 def test_wang_yu_distinct_from_song_person(self):
  m=next(m for m in self.ps['unit009']['mentions']if m['surface']=='王彧');self.assertNotEqual(m['person_id'],'1tc_q18_x7v')
 def test_dengai_reflexive_not_nearest_zhugeke(self):
  p=self.ps['appraisal'];st=p['text'].index('不能近自見')+3;m=next(m for m in p['mentions']if m['start']==st);self.assertEqual(m['person_id'],'i24_42d_pzh')
if __name__=='__main__':unittest.main()
