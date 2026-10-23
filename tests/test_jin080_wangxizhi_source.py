from pathlib import Path
import json,unittest
ROOT=Path(__file__).resolve().parents[1]
class WangXizhiSource(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.c=json.loads((ROOT/'corpus/jinshu/080-wangxizhi.json').read_text());cls.p={p['id'].rsplit(':',1)[-1]:p for p in cls.c['paragraphs']}
 def test_selected_complete_unit_not_whole_book(self):
  self.assertEqual(len(self.p),47);self.assertEqual(self.c['source']['text_scope'],'partial_chapter');self.assertFalse(self.c['source']['image_verified']);self.assertIn('始羲之所與共游者許邁',self.p['p047']['text'])
 def test_quote_recipient_not_all_subjects(self):
  p=self.p['p002'];ms=p['mentions'];x=next(m['person_id']for m in ms if m['surface']=='羲之');yin=next(m['person_id']for m in ms if m['surface']=='殷浩');a=p['text'].index('吾等');self.assertEqual(next(m['person_id']for m in ms if m['start']==a),yin);a=p['text'].index('公卿')+1;self.assertFalse(any(m['start']==a for m in ms));self.assertNotEqual(x,yin)
 def test_two_oldwomen_are_not_one_person(self):
  ms=self.p['p026']['mentions'];self.assertNotEqual(next(m['person_id']for m in ms if m['surface']=='孤居姥'),next(m['person_id']for m in ms if m['surface']=='老姥'))
 def test_bamboo_is_not_person(self):
  p=self.p['p038'];a=p['text'].index('此君');self.assertFalse(any(m['start']==a and m['person_id']for m in p['mentions']))
 def test_wangcheng_reading_is_reversible_not_text_replacement(self):
  m=next(m for m in self.p['p001']['mentions']if m['surface']=='王承');ds=json.loads((ROOT/'corpus/jinshu/080-wangxizhi-identities.json').read_text())['decisions'];d=next(d for d in ds if d['person_id']==m['person_id']);self.assertEqual(d['preferred_reading']['person_mention_id'],m['id']);self.assertEqual(d['preferred_reading']['received_surface'],'王承');self.assertEqual(d['preferred_reading']['preferred_surface'],'王應');self.assertTrue(d['preferred_reading']['source_spelling_is_not_alias']);self.assertFalse(d['human_reviewed']);v=self.c['annotation']['reported_variants'][0];self.assertFalse(v['adopted']);self.assertEqual(v['status'],'reported_not_collated')
 def test_earlier_wangkuang_not_huan_rebellion_guard(self):
  k=next(m['person_id']for m in self.p['p001']['mentions']if m['surface']=='曠');c=json.loads((ROOT/'corpus/jinshu/099-huanxuan.json').read_text());old=[m['person_id']for p in c['paragraphs']for m in p['mentions']if m['surface']=='王曠'];self.assertTrue(old);self.assertNotIn(k,old)
 def test_exact_original_characters(self):
  self.assertIn('氈青',self.p['p042']['text']);self.assertIn('懸橙',self.p['p045']['text']);self.assertEqual(self.p['p040']['text'][:6],'楨之字公幹，')
if __name__=='__main__':unittest.main()
