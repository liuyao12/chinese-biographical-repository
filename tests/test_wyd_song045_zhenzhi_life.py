from pathlib import Path
import unittest,sys,copy,json,importlib.util
ROOT=Path(__file__).resolve().parents[1] if Path(__file__).parent.name=='tests' else Path('/Users/liuyao/.codex/visualizations/2026/10/08/01a1196e-92f4-7fd1-a99c-8be9123187ca/cbr-song045-wyd-ner-candidate/native-fixture')
sys.path[:0]=[str(ROOT),str(ROOT/'scripts')]
from scripts import wyd_song045_zhenzhi_life as z
from scripts import wyd_song045_lifecycle as life
class Zhenzhi(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.e,cls.age,cls.a=z.records(ROOT);cls.ch=json.loads((ROOT/z.SOURCE).read_bytes())
 def test_date_and_scope(self):
  self.assertEqual(self.e['normalized_date']['year'],425);self.assertEqual(self.e['normalized_date']['precision'],'year');self.assertNotIn('month',self.e['normalized_date']);self.assertEqual(len(self.e['source_zhenzhi_subject_scope']['full_paragraphs']),2);self.assertTrue(z.death_valid(self.e,ROOT))
 def test_age_is_open_lower_bound(self):
  self.assertIsNone(self.age['value']);self.assertIsNone(self.age['birth_year']);self.assertEqual(self.age['bounds'],{'lower':90,'lower_inclusive':False,'upper':None,'upper_inclusive':None});self.assertEqual(self.age['source_term'],'年九十餘');self.assertEqual(self.age['age_context']['life_event_id'],z.LE)
 def test_age_exact_and_inclusive_refused(self):
  for k,v in [('value',90),('value',91),('birth_year',335),('source_number','九十一')]:
   ch=copy.deepcopy(self.ch);a=next(x for x in ch['annotation']['age_assertions']if x['id']==z.AGE);a[k]=v
   with self.assertRaises(ValueError):life.base_annotation(ch)
  for k,v in [('lower_inclusive',True),('upper',99),('lower',90.5)]:
   ch=copy.deepcopy(self.ch);next(x for x in ch['annotation']['age_assertions']if x['id']==z.AGE)['bounds'][k]=v
   with self.assertRaises(ValueError):life.base_annotation(ch)
 def test_wrong_date_role_and_location_refused(self):
  for k,v in [('person_id','wrong'),('date_expression','元嘉中')]:
   e=copy.deepcopy(self.e);e[k]=v;self.assertFalse(z.death_valid(e,ROOT))
  for k,v in [('year',426),('month',1),('day',1)]:
   e=copy.deepcopy(self.e);e['normalized_date'][k]=v;self.assertFalse(z.death_valid(e,ROOT))
  a=copy.deepcopy(self.a);a['place']['source_name']='京口';self.assertFalse(z.address_valid(a,self.ch,ROOT))
 def test_full_named_scope_not_nearest_name(self):
  for suffix in ['p014','p015']:
   ch=copy.deepcopy(self.ch);p=next(p for p in ch['paragraphs']if p['id'].endswith(suffix));m=next(m for m in p['mentions']if m['surface']=='鎮之');m['person_id']='another'
   with self.assertRaises(AssertionError):z.subject(ch)
 def test_existing_53_retained(self):
  ages=self.ch['annotation']['age_assertions'];self.assertEqual([a['id']for a in ages],['age-song045-wyd-cui-death',z.AGE]);self.assertEqual(ages[0]['value'],53)
 def test_malformed_inputs_failclosed(self):
  for bad in [None,[],1,'x',{},True]:self.assertFalse(z.death_valid(bad,ROOT));self.assertFalse(z.address_valid(bad,self.ch,ROOT))
 def test_relative_home_not_geocoded(self):
  self.assertEqual(self.a['place'],{'source_name':'家','place_id':None,'modern_identification':None});self.assertTrue(z.address_valid(self.a,self.ch,ROOT))
if __name__=='__main__':unittest.main()
