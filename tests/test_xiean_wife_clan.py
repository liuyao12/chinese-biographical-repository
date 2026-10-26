import json,copy,unittest
from pathlib import Path
from scripts.person_bundle import validate_clan_style
R=Path(__file__).resolve().parents[1]
class WifeClan(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.n=json.loads((R/'corpus/jinshu/079-xiean-wife-name-components.json').read_text())['records'][0];c=json.loads((R/'corpus/jinshu/079.json').read_text());cls.p=next(p for p in c['paragraphs']if p['id']==cls.n['paragraph_id']);cls.aa=json.loads((R/'corpus/jinshu/079-assertions.json').read_text())['assertions']
 def test_real_source_sister_clan(self):validate_clan_style(self.n,self.p,self.aa);self.assertIsNone(self.n['ming'])
 def test_no_invented_ming_or_wrong_surname(self):
  for k,v in [('ming','氏'),('surname','謝'),('person_id','other')]:
   n=copy.deepcopy(self.n);n[k]=v
   with self.assertRaises(ValueError):validate_clan_style(n,self.p,self.aa)
 def test_no_spouse_as_sister_and_no_wrong_brother(self):
  for pred in ['spouse','mother']:
   aa=copy.deepcopy(self.aa);next(a for a in aa if a['id']=='a-phase6-079-29-6')['predicate']=pred
   with self.assertRaises(ValueError):validate_clan_style(self.n,self.p,aa)
  aa=copy.deepcopy(self.aa);next(a for a in aa if a['id']=='a-phase6-079-29-6')['object_person_id']='other'
  with self.assertRaises(ValueError):validate_clan_style(self.n,self.p,aa)
 def test_full_fixed_source_and_revision(self):
  p=copy.deepcopy(self.p);p['text']='甲'+p['text'];n=copy.deepcopy(self.n);n['quote']=p['text']
  for m in p['mentions']:m['start']+=1;m['end']+=1
  aa=copy.deepcopy(self.aa)
  for a in aa:
   for e in a['evidence']:
    if e['paragraph_id']==p['id']:e['quote']=p['text']
  with self.assertRaises(ValueError):validate_clan_style(n,p,aa)
  n=copy.deepcopy(self.n);n['source_revision']=0
  with self.assertRaises(ValueError):validate_clan_style(n,self.p,self.aa)
 def test_legal_pid_rekey(self):
  mapping={self.n['person_id']:'new_wife',next(a for a in self.aa if a['id']=='a-phase6-079-29-6')['object_person_id']:'new_brother'}
  def remap(v):
   if isinstance(v,dict):return{k:remap(x)for k,x in v.items()}
   if isinstance(v,list):return[remap(x)for x in v]
   return mapping.get(v,v)if isinstance(v,str)else v
  validate_clan_style(remap(self.n),remap(self.p),remap(self.aa))
 def test_original_legacy_sibling_clan_still_valid(self):
  p={'id':'legacy:p','text':'王導之妹也','mentions':[{'kind':'person','person_id':'brother','surface':'王導'}]};n={'paragraph_id':p['id'],'surname':'王','ming':None,'quote':p['text'],'person_id':'sister','clan_style':{'kind':'sibling_clan_appellation','value':'王氏','source_term':p['text'],'assertion_ids':['legacy'],'status':'editorial_provisional','rationale':'source','human_reviewed':False}};a={'id':'legacy','predicate':'sister','subject_person_id':'sister','object_person_id':'brother','qualifiers':{'source_term':p['text']},'evidence':[{'paragraph_id':p['id'],'quote':p['text']}]};validate_clan_style(n,p,[a])
if __name__=='__main__':unittest.main()
