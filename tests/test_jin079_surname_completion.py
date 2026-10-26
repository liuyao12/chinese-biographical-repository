import unittest,json,copy,hashlib
from pathlib import Path
from scripts.surname_from_father import validate
ROOT=Path(__file__).resolve().parents[1]
class SurnameCompletion(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=json.loads((ROOT/'corpus/jinshu/079.json').read_text());cls.nn=json.loads((ROOT/'corpus/jinshu/079-name-completion.json').read_text())['records'];cls.names=json.loads((ROOT/'data/corpus/profile-names.json').read_text())['records']+cls.nn;cls.aa=[]
  for f in(ROOT/'corpus').glob('*/*.json'):
   d=json.loads(f.read_text())
   if d.get('record_type')=='person_assertion_set':cls.aa+=d['assertions']
 def check(self,n,aa=None,c=None,names=None):
  c=c or self.c;return validate(n,names or self.names,{c['id']:c},self.aa if aa is None else aa,root=ROOT)
 def test_four_inferences_and_one_original_full_name(self):
  self.assertEqual([n['ming']for n in self.nn],['瑤','該','模','澹'])
  for n in self.nn:self.check(n);self.assertEqual(n['surname'],'謝')
  self.assertEqual(len([n for n in self.names if n.get('id')=='name-jin079-xiean-explicit']),1)
 def test_wrong_surname_person_and_ming(self):
  for key,value in [('surname','王'),('person_id',self.nn[1]['person_id']),('ming','曜')]:
   n=copy.deepcopy(self.nn[0]);n[key]=value
   with self.assertRaises(ValueError):self.check(n)
 def test_mother_adoption_and_ritual_not_father(self):
  for predicate in ['mother','adoptive_father','ritual_successor_of']:
   aa=copy.deepcopy(self.aa);next(a for a in aa if a['id']=='a-jin079-xieyao-an-yao')['predicate']=predicate
   with self.assertRaises(ValueError):self.check(self.nn[0],aa=aa)
 def test_brother_never_creates_father_generation(self):
  for key,value in [('traversal','father_to_child'),('generation_after',3)]:
   n=copy.deepcopy(self.nn[-1]);n['surname_basis']['steps'][-1][key]=value
   with self.assertRaises(ValueError):self.check(n)
 def test_raw_sha_and_revision(self):
  for key,value in [('wikitext_sha256','0'*64),('revision_id',0)]:
   c=copy.deepcopy(self.c);c['source'][key]=value
   with self.assertRaises(ValueError):self.check(self.nn[0],c=c)
 def test_independent_full_source_rejects_co_shift(self):
  c=copy.deepcopy(self.c);n=copy.deepcopy(self.nn[0]);p=next(p for p in c['paragraphs']if p['id']==n['paragraph_id']);p['text']='甲'+p['text']
  for m in p['mentions']:m['start']+=1;m['end']+=1
  n['quote']=p['text'];step=n['surname_basis']['steps'][0];step['evidence'][0]['quote']=p['text'];step['source_frames'][0]['paragraph_sha256']=hashlib.sha256(p['text'].encode()).hexdigest();aa=copy.deepcopy(self.aa);a=next(a for a in aa if a['id']==step['assertion_id']);a['evidence'][0]['quote']=p['text'];b=a['qualifiers']['source_clause_binding'];b['clause_start']+=1;b['clause_end']+=1;b['paragraph_sha256']=step['source_frames'][0]['paragraph_sha256']
  with self.assertRaises(ValueError):self.check(n,aa=aa,c=c)
 def test_complete_canonical_rekey(self):
  ids={n['person_id']for n in self.nn};seed=next(n for n in self.names if n.get('id')=='name-jin079-xiean-explicit');ids.add(seed['person_id']);mapping={pid:'replacement_'+str(i)for i,pid in enumerate(sorted(ids))}
  def remap(x):
   if isinstance(x,dict):return{k:remap(v)for k,v in x.items()}
   if isinstance(x,list):return[remap(v)for v in x]
   return mapping.get(x,x)if isinstance(x,str)else x
  for n in remap(self.nn):self.check(n,aa=remap(self.aa),c=remap(self.c),names=remap(self.names))
 def test_all_legacy_source_rows_remain_available(self):
  # Legal legacy rows without id coexist with the single located full-name seed.
  self.assertTrue(any('id'not in n for n in self.names));self.check(self.nn[0])
if __name__=='__main__':unittest.main()
