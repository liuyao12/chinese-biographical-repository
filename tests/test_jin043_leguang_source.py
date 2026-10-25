# coding:utf-8
from pathlib import Path
import unittest,json,copy,hashlib
R=Path(__file__).resolve().parents[1];CID='c-jinshu-043-leguang'
def load():return json.loads((R/'corpus/jinshu/043-leguang.json').read_bytes())
def linked(c,surface):return[m for p in c['paragraphs']for m in p['mentions']if m['surface']==surface]
class LeguangSourceTests(unittest.TestCase):
 def test_complete_eleven_paragraphs_fixed_raw_and_truncation_rejection(self):
  from scripts.fixed_wikisource_units import source_errors
  c=load();self.assertEqual(len(c['paragraphs']),11);self.assertEqual(sum(len(p['text'])for p in c['paragraphs']),1382);self.assertEqual(source_errors(c,R),[])
  bad=copy.deepcopy(c);p=bad['paragraphs'][-1];p['text']=p['text'][:-1];p['source_position']['raw_character_offsets']=p['source_position']['raw_character_offsets'][:-1];self.assertTrue(source_errors(bad,R))
 def test_contextual_surname_short_forms_not_ordinary_le_or_yun(self):
  c=load();wang=next(m['person_id']for m in c['paragraphs'][0]['mentions']if m['surface']=='王衍');guang=linked(c,'樂廣')[0]['person_id'];pei=linked(c,'裴頠')[0]['person_id']
  self.assertEqual([(m['surface'],m['person_id'])for m in c['paragraphs'][3]['mentions']if m['surface']in('王','樂')],[('王',wang),('樂',guang)])
  self.assertEqual([(m['surface'],m['person_id'])for m in c['paragraphs'][4]['mentions']if m['surface']in('裴','樂')],[('裴',pei),('樂',guang),('樂',guang)])
  for i,word in [(2,'廣雲'),(5,'樂地')]:
   p=c['paragraphs'][i];start=p['text'].index(word)+(1 if word=='廣雲'else 0);self.assertFalse(any(m['start']<=start<m['end']for m in p['mentions']))
  self.assertIn('神姿郎徹',c['paragraphs'][0]['text']);self.assertIn('潘嶽',c['paragraphs'][1]['text'])
 def test_sons_are_not_five_fabricated_names_and_kai_candidate_remains_explicit(self):
  c=load();cases=c['annotation']['source_reading_cases'];case=next(x for x in cases if x['id'].endswith('-kai'));self.assertEqual(case['status'],'unresolved');self.assertNotIn(case['person_id'],case['candidate_person_ids']);self.assertEqual(len(linked(c,'五男')),1);self.assertEqual(linked(c,'五男')[0]['kind'],'unresolved')
  rows=json.loads((R/'source-evidence/jin043-leguang-source/identity-records.json').read_bytes());self.assertEqual(len([r for r in rows if r['is_new']]),7);self.assertEqual(len([r for r in rows if r['key']in('kai','zhao','mo')]),3)
  girl=next(r for r in rows if r['key']=='daughter');self.assertIn('未名',girl['label']);self.assertNotIn('name_components',girl)
 def test_yang_same_event_distinguishes_reading_from_text_correction(self):
  c=load();parallel=json.loads((R/'corpus/sanguozhi/019-yangxiu.json').read_bytes());m=next(m for p in parallel['paragraphs']for m in p['mentions']if m['id']=='c-sanguozhi-019-yangxiu:p006:m0082');self.assertEqual(m['surface'],'嶠');self.assertTrue(all(x['person_id']==m['person_id']for x in linked(c,'喬')));self.assertIn('楊准',c['paragraphs'][4]['text']);self.assertNotIn('楊準',c['paragraphs'][4]['text'])
if __name__=='__main__':unittest.main()
