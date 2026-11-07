"""One literal full name, not a surname/given-name inference."""
from pathlib import Path
import unittest,json,copy
from scripts.fixed_song067_wenzhong_literal_name import state,valid
from scripts.person_bundle import validate_full_name
R=Path(__file__).resolve().parents[1]
class Song067WenzhongLiteralName(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.c,cls.p,cls.n=state(R)
 def test_actual_full_literal_name_and_unsegmented_fields(self):
  self.assertEqual(self.n['full_name'],'文種');self.assertIsNone(self.n['surname']);self.assertIsNone(self.n['ming']);self.assertTrue(valid(self.n,self.p,self.c,R));validate_full_name(self.n,self.p,chapter=self.c,root=R)
 def test_literal_exact_source_marker(self):
  m=next(m for m in self.p['mentions']if m['id']==self.n['person_mention_id']);self.assertEqual(m['surface'],'文種');self.assertEqual(m['person_id'],self.n['person_id']);self.assertEqual((m['start'],m['end']),(242,244));self.assertEqual(self.p['text'][242:244],'文種')
 def test_reject_invented_surname_or_given_name_split(self):
  for k,v in [('surname','文'),('ming','種'),('full_name','種')]:
   n=copy.deepcopy(self.n);n[k]=v;self.assertFalse(valid(n,self.p,self.c,R));self.assertRaises(ValueError,validate_full_name,n,self.p,chapter=self.c,root=R)
 def test_reject_borrowed_short_name_or_other_person(self):
  for k,v in [('person_mention_id',self.p['id']+':m00094'),('person_id','49g_7az_e4i')]:
   n=copy.deepcopy(self.n);n[k]=v;self.assertFalse(valid(n,self.p,self.c,R))
 def test_reject_wrong_caller_source_or_commentary_text(self):
  c=copy.deepcopy(self.c);c['source_id']='wrong';self.assertFalse(valid(self.n,self.p,c,R));p=copy.deepcopy(self.p);p['text']=p['text'].replace('文種','文中',1);self.assertFalse(valid(self.n,p,self.c,R))
 def test_existing_parallel_spelling_branch_still_rejects_fake_qualification(self):
  n=copy.deepcopy(self.n);n['full_name_basis']['kind']='received_parallel_spelling';self.assertRaises(ValueError,validate_full_name,n,self.p,chapter=self.c,root=R)
if __name__=='__main__':unittest.main()
