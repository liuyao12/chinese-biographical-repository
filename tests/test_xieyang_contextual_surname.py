import unittest,json,copy
from pathlib import Path
from scripts.surname_from_father import validate
R=Path(__file__).resolve().parents[1]
class ContextualSurname(unittest.TestCase):
 def setUp(self):
  self.ns=json.loads((R/'data/corpus/profile-names.json').read_text())['records'];self.n=copy.deepcopy(next(x for x in self.ns if x.get('id')=='name-song085-f13-027'));c=json.loads((R/'corpus/songshu/085-xiezhuang.json').read_text());self.cs={c['id']:c};self.aa=json.loads((R/'corpus/songshu/085-xiezhuang-assertions.json').read_text())['assertions']
 def bad(self,f):
  f();self.assertRaises(ValueError,validate,self.n,self.ns,self.cs,self.aa)
 def test_contextual_pass(self):validate(self.n,self.ns,self.cs,self.aa);self.assertEqual(self.n['surname'],'謝');self.assertEqual(self.n['status'],'contextual_provisional')
 def test_source_explicit_rejected(self):self.bad(lambda:self.n.update(status='source_explicit'))
 def test_wrong_father(self):self.bad(lambda:self.n['surname_basis'].update(father_person_id='wrong'))
 def test_wrong_surname(self):self.bad(lambda:self.n.update(surname='王'))
 def test_truncated_quote(self):self.bad(lambda:self.n['surname_basis'].update(child_context_quote=self.n['quote'][:-1]))
 def test_wrong_anchor(self):self.bad(lambda:self.n['surname_basis'].update(father_full_mention_id=self.n['person_mention_id']))
 def test_adoptive_instead_of_explicit_father(self):
  self.bad(lambda:next(a for a in self.aa if a['id']==self.n['surname_basis']['father_assertion_id']).update(predicate='adoptive_father'))
 def test_ordinary_unknown_unmodified(self):
  n={'surname':None,'ming':None};validate(n,[],{},[]);self.assertEqual(n,{'surname':None,'ming':None})
