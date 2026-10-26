import unittest,json,copy
from pathlib import Path
from scripts.surname_from_father import validate
R=Path(__file__).resolve().parents[1]
class XieHuanSurname(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=json.loads((R/'corpus/songshu/067-xielingyun.json').read_text());cls.names=json.loads((R/'corpus/songshu/067-huan-surname-name-components.json').read_text())['records'];cls.aa=json.loads((R/'corpus/songshu/067-xielingyun-assertions.json').read_text())['assertions']
 def check(self,n=None,c=None,aa=None,names=None):
  c=c or self.c;validate(n or self.names[1],names or self.names,{c['id']:c},aa or self.aa,root=R)
 def test_real_same_paragraph_father(self):self.check()
 def test_wrong_ming_surname_and_subject(self):
  for k,v in [('ming','奐'),('surname','王'),('person_id',self.names[0]['person_id'])]:
   n=copy.deepcopy(self.names[1]);n[k]=v
   with self.assertRaises(ValueError):self.check(n=n)
 def test_not_mother_adoption_or_grandfather(self):
  for pred in ['mother','adoptive_father','grandfather']:
   aa=copy.deepcopy(self.aa);next(a for a in aa if a['id']=='a-song067-lingyun-001')['predicate']=pred
   with self.assertRaises(ValueError):self.check(aa=aa)
 def test_fixed_source_raw_and_text(self):
  for what in ['revision_id','raw_sha256']:
   c=copy.deepcopy(self.c);c['source'][what]='wrong'
   with self.assertRaises(ValueError):self.check(c=c)
  c=copy.deepcopy(self.c);c['paragraphs'][0]['text']='甲'+c['paragraphs'][0]['text']
  for m in c['paragraphs'][0]['mentions']:m['start']+=1;m['end']+=1
  with self.assertRaises(ValueError):self.check(c=c)
 def test_complete_rekey(self):
  mapping={n['person_id']:'new_'+str(i)for i,n in enumerate(self.names)}
  def remap(v):
   if isinstance(v,dict):return{k:remap(x)for k,x in v.items()}
   if isinstance(v,list):return[remap(x)for x in v]
   return mapping.get(v,v)if isinstance(v,str)else v
  self.check(n=remap(self.names[1]),c=remap(self.c),aa=remap(self.aa),names=remap(self.names))
if __name__=='__main__':unittest.main()
