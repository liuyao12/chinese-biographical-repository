import copy,json,unittest
from pathlib import Path
from scripts.maternal_roles import maternal_role_valid
DATA=json.loads((Path(__file__).parent/'fixtures/maternal-role-muyue.json').read_text())
class MotherYueTests(unittest.TestCase):
 def setUp(self):self.p=copy.deepcopy(DATA['paragraph']);self.a=copy.deepcopy(DATA['assertion'])
 def valid(self):return maternal_role_valid(self.a,{self.p['id']:(DATA['chapter_id'],self.p)})
 def insert(self,pos,text):
  self.p['text']=self.p['text'][:pos]+text+self.p['text'][pos:]
  for m in self.p['mentions']:
   if m['start']>=pos:m['start']+=len(text);m['end']+=len(text)
  self.a['evidence'][0]['quote']=self.p['text']
 def test_actual_received_muyue(self):
  self.assertTrue(self.valid());self.assertEqual(self.a['qualifiers']['role'],'mother_unspecified');self.assertIsNone(self.a['qualifiers']['biological_mother']);self.assertIsNone(self.a['qualifiers']['father_person_id'])
 def test_no_birth_inference(self):self.a['qualifiers']['biological_mother']=True;self.assertFalse(self.valid())
 def test_no_father_inference(self):self.a['qualifiers']['father_person_id']=self.a['subject_person_id'];self.assertFalse(self.valid())
 def test_no_mother_predicate(self):self.a['predicate']='mother';self.assertFalse(self.valid())
 def test_no_prior_mother_relabel(self):self.a['qualifiers']['role']='prior_mother';self.assertFalse(self.valid())
 def test_wrong_child(self):
  other=self.p['mentions'][2];self.a['subject_person_id']=other['person_id'];self.a['evidence'][0]['subject_person_mention_id']=other['id'];self.assertFalse(self.valid())
 def test_wrong_mother(self):self.a['object_person_id']=self.a['subject_person_id'];self.assertFalse(self.valid())
 def test_grandmother_not_mother(self):self.insert(15,'祖');self.assertFalse(self.valid())
 def test_other_person_mother_clause(self):self.insert(15,'他人');self.assertFalse(self.valid())
 def test_quoted_mother_clause(self):
  self.insert(15,'「');end=next(m['end']for m in self.p['mentions']if m['id']==self.a['evidence'][0]['object_person_mention_id']);self.insert(end+1,'」');self.assertFalse(self.valid())
 def test_speech_before_mother(self):self.insert(15,'人曰：');self.assertFalse(self.valid())
 def test_source_quote_mismatch(self):self.a['evidence'][0]['quote']='母曰丁貴嬪';self.assertFalse(self.valid())
 def test_exact_wrong_connector(self):
  self.a['qualifiers']['source_term']='母云丁貴嬪';self.assertFalse(self.valid())
 def test_wrong_mother_span(self):
  next(m for m in self.p['mentions']if m['id']==self.a['evidence'][0]['object_person_mention_id'])['start']+=1;self.assertFalse(self.valid())
 def test_no_status_relabel(self):self.a['status']='contextual_provisional';self.assertFalse(self.valid())
 def test_unknown_metadata_preserved(self):
  self.a['editorial_unknown']={'keep':False};self.p['unknown']=[None,0];before=copy.deepcopy((self.a,self.p));self.assertTrue(self.valid());self.assertEqual(before,(self.a,self.p))
if __name__=='__main__':unittest.main()
