import unittest,json,copy
from pathlib import Path
from unittest.mock import patch
from scripts.person_bundle import validate_clan_style
R=Path(__file__).resolve().parents[1]
class PaternalClans(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.nn=json.loads((R/'corpus/name-context/xie-women-paternal-clans.json').read_text())['records'];cls.cases=json.loads((R/'source-evidence/name-context/xie-women-paternal-clans.json').read_text());cls.chs={};cls.aa=[]
  for f in(R/'corpus').glob('*/*.json'):
   d=json.loads(f.read_text())
   if d.get('record_type')=='marked_chapter':cls.chs[d['id']]=d
   if d.get('record_type')=='person_assertion_set':cls.aa+=d['assertions']
 def p(self,n):return next(p for p in self.chs[n['chapter_id']]['paragraphs']if p['id']==n['paragraph_id'])
 def test_all_five_true_father_clan_styles(self):
  self.assertEqual(len(self.nn),5)
  for n in self.nn:validate_clan_style(n,self.p(n),self.aa);self.assertIsNone(n['ming'])
 def test_no_invented_ming_or_wrong_surname(self):
  for original in self.nn:
   for k,v in [('ming','某'),('surname','趙'),('person_id','other')]:
    n=copy.deepcopy(original);n[k]=v
    with self.assertRaises(ValueError):validate_clan_style(n,self.p(n),self.aa)
 def test_not_mother_adoptive_spouse_or_wrong_parent(self):
  for n in self.nn:
   aid=n['clan_style']['assertion_ids'][0]
   for pred in ['mother','adoptive_father','spouse']:
    aa=copy.deepcopy(self.aa);next(a for a in aa if a['id']==aid)['predicate']=pred
    with self.assertRaises(ValueError):validate_clan_style(n,self.p(n),aa)
   aa=copy.deepcopy(self.aa);next(a for a in aa if a['id']==aid)['object_person_id']='other'
   with self.assertRaises(ValueError):validate_clan_style(n,self.p(n),aa)
 def test_wrong_fullname_basis_person(self):
  for original in self.nn:
   n=copy.deepcopy(original);n['clan_style_basis']['parent_full_name_source']['parent_person_id']='other'
   with self.assertRaises(ValueError):validate_clan_style(n,self.p(n),self.aa)
 def test_whole_source_coshift_rejected_without_writing_root(self):
  n=copy.deepcopy(self.nn[0]);case=self.cases[0];path=R/case['source']['native_path'];data=json.loads(path.read_bytes());p=next(p for p in data['paragraphs']if p['id']==n['paragraph_id']);p['text']='甲'+p['text']
  for m in p['mentions']:m['start']+=1;m['end']+=1
  n['quote']=p['text'];original=Path.read_bytes
  def read(f):return json.dumps(data,ensure_ascii=False).encode()if f==path else original(f)
  with patch.object(Path,'read_bytes',read):
   with self.assertRaises(ValueError):validate_clan_style(n,p,self.aa)
 def test_source_fullname_cannot_be_replaced_by_label(self):
  n=self.nn[2];case=self.cases[2];path=R/case['seed']['native_path'];d=json.loads(path.read_bytes());p=next(p for p in d['paragraphs']if p['id']==case['seed']['paragraph_id']);m=next(m for m in p['mentions']if m['id']==case['seed_mention_id']);m['kind']='unresolved';original=Path.read_bytes
  def read(f):return json.dumps(d,ensure_ascii=False).encode()if f==path else original(f)
  with patch.object(Path,'read_bytes',read):
   with self.assertRaises(ValueError):validate_clan_style(n,self.p(n),self.aa)
 def test_all_reference_rekey(self):
  ids={n['person_id']for n in self.nn}|{n['clan_style_basis']['parent_full_name_source']['parent_person_id']for n in self.nn};mapping={pid:'new_person_'+str(i)for i,pid in enumerate(sorted(ids))}
  def remap(v):
   if isinstance(v,dict):return{k:remap(x)for k,x in v.items()}
   if isinstance(v,list):return[remap(x)for x in v]
   return mapping.get(v,v)if isinstance(v,str)else v
  original=Path.read_bytes;paths={R/f['native_path']for case in self.cases for f in(case['source'],case['seed'])}
  def read(f):return json.dumps(remap(json.loads(original(f))),ensure_ascii=False).encode()if f in paths else original(f)
  with patch.object(Path,'read_bytes',read):
   for n in self.nn:validate_clan_style(remap(n),remap(self.p(n)),remap(self.aa))
if __name__=='__main__':unittest.main()
