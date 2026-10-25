"""Actual received-source pair scope; no synthetic historical claims are saved."""
import copy,json,unittest
from pathlib import Path
from scripts.source_pair_order_preference import validate,preferred_relation,NEW,OLD,CID
ROOT=Path(__file__).resolve().parents[1]
class FixedSourcePairOrderTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.record=json.loads((ROOT/'corpus/shishuoxinyu/yanyu-071-order-decisions.json').read_text())
  cls.chapters={}
  for rel in('corpus/shishuoxinyu/yanyu-071.json','corpus/songshu/052-xiejingren.json'):
   c=json.loads((ROOT/rel).read_text());cls.chapters[c['id']]=c
  cls.assertions={}
  for rel in('corpus/shishuoxinyu/yanyu-071-assertions.json','corpus/songshu/052-xiejingren-assertions.json'):
   cls.assertions.update({a['id']:a for a in json.loads((ROOT/rel).read_text())['assertions']})
  cls.people={p['id']:p for p in json.loads((ROOT/'registry/persons.json').read_text())['persons']}
  cls.ju,cls.an=cls.record['decisions'][0]['person_ids']
 def test_actual_received_pair(self):self.assertTrue(validate(self.record,ROOT,self.chapters,self.assertions,self.people))
 def test_bad_types_fail_with_value_error(self):
  for bad in(None,[],'bad',0):
   with self.subTest(type=type(bad).__name__),self.assertRaises(ValueError):validate(bad,ROOT,self.chapters,self.assertions,self.people)
 def test_other_pair_rejected(self):
  d=copy.deepcopy(self.record);d['decisions'][0]['person_ids'][1]=next(p for p in self.people if p not in(self.ju,self.an))
  with self.assertRaises(ValueError):validate(d,ROOT,self.chapters,self.assertions,self.people)
 def test_commentary_must_not_be_body(self):
  c=copy.deepcopy(self.chapters);c[CID]['paragraphs'][1]['text_layer']='received_chapter'
  with self.assertRaises(ValueError):validate(self.record,ROOT,c,self.assertions,self.people)
 def test_wrong_preference_rejected(self):
  d=copy.deepcopy(self.record);d['decisions'][0]['preferred_assertion_id']=OLD
  with self.assertRaises(ValueError):validate(d,ROOT,self.chapters,self.assertions,self.people)
 def test_raw_assertions_retained_only_one_preferred_direction(self):
  d=self.record['decisions'];before=copy.deepcopy(self.assertions);old=preferred_relation(self.assertions[OLD],d);new=preferred_relation(self.assertions[NEW],d)
  self.assertEqual(self.assertions,before);self.assertEqual(old['qualifiers']['source_term'],'太傅安第二弟');self.assertNotIn('relative_birth_order',old['qualifiers']);self.assertEqual(new['qualifiers']['relative_birth_order']['older_person_id'],self.ju)
 def test_unrelated_relation_unchanged(self):
  a=self.assertions['a-shishuo071-daoyun-father'];self.assertEqual(preferred_relation(a,self.record['decisions']),a)
 def test_legal_all_reference_rekey(self):
  source_root='_'.join(self.ju.split('_')[:3]);new_root='rky_tst_001'
  mapping={p:new_root+p[len(source_root):]for p in self.people if p==source_root or p.startswith(source_root+'_')}
  self.assertFalse(set(mapping.values()).intersection(self.people))
  def rebind(v):
   if isinstance(v,dict):return{mapping.get(k,k):rebind(x)for k,x in v.items()}
   if isinstance(v,list):return[rebind(x)for x in v]
   return mapping.get(v,v)if isinstance(v,str)else v
  people={rebind(v)['id']:rebind(v)for v in self.people.values()};chapters=rebind(self.chapters);assertions=rebind(self.assertions);record=rebind(self.record)
  self.assertTrue(validate(record,ROOT,chapters,assertions,people))
  with self.assertRaises(ValueError):validate(record,ROOT,chapters,assertions,self.people)

if __name__=='__main__':unittest.main()
