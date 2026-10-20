import copy,unittest
from test_biography_ritual_succession import A,PS,AS
from scripts.biography_ritual_succession import valid
class ReviewQualification(unittest.TestCase):
 def test_source_false(self):
  a=copy.deepcopy(A);a['human_reviewed']=False;self.assertTrue(valid(a,PS,AS))
 def test_source_true(self):
  a=copy.deepcopy(A);a['human_reviewed']=True;self.assertTrue(valid(a,PS,AS))
 def test_invalid_false(self):
  a=copy.deepcopy(A);a.update(human_reviewed=False,predicate='adoptive_father');self.assertFalse(valid(a,PS,AS))
 def test_invalid_true(self):
  a=copy.deepcopy(A);a.update(human_reviewed=True,predicate='adoptive_father');self.assertFalse(valid(a,PS,AS))

 def test_review_none_rejected(self):
  a=copy.deepcopy(A);a['human_reviewed']=None;self.assertFalse(valid(a,PS,AS))
 def test_review_string_rejected(self):
  a=copy.deepcopy(A);a['human_reviewed']='false';self.assertFalse(valid(a,PS,AS))
 def test_review_integer_zero_rejected(self):
  a=copy.deepcopy(A);a['human_reviewed']=0;self.assertFalse(valid(a,PS,AS))
 def test_review_integer_one_rejected(self):
  a=copy.deepcopy(A);a['human_reviewed']=1;self.assertFalse(valid(a,PS,AS))
