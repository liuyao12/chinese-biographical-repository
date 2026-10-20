import json,copy,unittest
from pathlib import Path
from scripts.directed_uncle_roles import paternal_uncle_direction_valid
class ResumedUncle(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.f=json.loads((Path(__file__).parent/'fixtures/resumed_paternal_uncle.json').read_text())
 def valid(self,a=None,p=None):
  return paternal_uncle_direction_valid(a or self.f['assertion'],{self.f['paragraph']['id']:(self.f['chapter_id'],p or self.f['paragraph'])})
 def test_actual_resumed_subject(self):self.assertTrue(self.valid())
 def test_reversed_endpoints(self):
  a=copy.deepcopy(self.f['assertion']);a['subject_person_id'],a['object_person_id']=a['object_person_id'],a['subject_person_id'];self.assertFalse(self.valid(a))
 def test_wrong_named_uncle(self):
  a=copy.deepcopy(self.f['assertion']);a['object_person_id']='wrong-person';self.assertFalse(self.valid(a))
 def test_wrong_role_term(self):
  a=copy.deepcopy(self.f['assertion']);a['qualifiers']['source_term']='伯父融';self.assertFalse(self.valid(a))
 def test_same_person_rejected(self):
  a=copy.deepcopy(self.f['assertion']);a['object_person_id']=a['subject_person_id'];self.assertFalse(self.valid(a))
 def inserted(self,text,person=False):
  p=copy.deepcopy(self.f['paragraph']);a=copy.deepcopy(self.f['assertion']);pos=p['text'].index('與叔父');p['text']=p['text'][:pos]+text+p['text'][pos:]
  for m in p['mentions']:
   if m['start']>=pos:m['start']+=len(text);m['end']+=len(text)
  if person:p['mentions'].append({'id':'intervening-person','kind':'person','person_id':'another-person','surface':text,'start':pos,'end':pos+len(text)})
  for e in a['evidence']:e['quote']=p['text']
  return a,p
 def test_intervening_person_rejected(self):
  a,p=self.inserted('某甲',True);self.assertFalse(self.valid(a,p))
 def test_quotation_boundary_rejected(self):
  a,p=self.inserted('「曰」');self.assertFalse(self.valid(a,p))
if __name__=='__main__':unittest.main()
