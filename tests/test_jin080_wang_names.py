import unittest,json,copy
from pathlib import Path
from scripts.fixed_biography_names import component_valid,validate_surname
R=Path(__file__).resolve().parents[1]
class Names(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=json.loads((R/'corpus/jinshu/080-wangxizhi.json').read_bytes());cls.rows=json.loads((R/'corpus/jinshu/080-wangxizhi-name-components.json').read_bytes())['records'];cls.aa=json.loads((R/'corpus/jinshu/080-wangxizhi-assertions.json').read_bytes())['assertions']
 def check(self,n,aa=None,c=None):
  c=c or self.c;aa=self.aa if aa is None else aa
  if not component_valid(n,c,R,aa):raise ValueError('Invalid component')
  if n.get('surname_basis'):validate_surname(n,self.rows,{c['id']:c},aa,R)
 def test_ten_and_five_zi(self):
  self.assertEqual(len(self.rows),10);self.assertEqual(sum('zi'in n for n in self.rows),5)
  for n in self.rows:self.check(n)
 def test_unknown_father_stays_null(self):
  n=self.rows[-1];a=next(a for a in self.aa if a['id']==n['surname_basis']['steps'][-1]['assertion_id']);self.assertEqual(a['predicate'],'paternal_uncle');self.assertIsNone(a['qualifiers']['father_person_id']);self.check(n)
 def test_wrong_courtesy(self):
  n=copy.deepcopy(self.rows[5]);n['zi']='子敬'
  with self.assertRaises(ValueError):self.check(n)
 def test_courtesy_not_ming(self):
  n=copy.deepcopy(self.rows[5]);n['ming']='子猷'
  with self.assertRaises(ValueError):self.check(n)
 def test_wrong_surname(self):
  n=copy.deepcopy(self.rows[5]);n['surname']='謝'
  with self.assertRaises(ValueError):self.check(n)
 def test_heir_not_father(self):
  n=copy.deepcopy(self.rows[-1]);n['surname_basis']['steps'][-1]['assertion_id']='a-jin080-wangxizhi-kin_032'
  with self.assertRaises(ValueError):self.check(n)
 def test_mutated_relation(self):
  aa=copy.deepcopy(self.aa);aa[16]['predicate']='adoptive_father'
  with self.assertRaises(ValueError):self.check(self.rows[5],aa)
 def test_wrong_person_consistent_record(self):
  n=copy.deepcopy(self.rows[5]);n['person_id']=self.rows[6]['person_id']
  with self.assertRaises(ValueError):self.check(n)
 def test_raw_shift_even_retained_text(self):
  c=copy.deepcopy(self.c);p=c['paragraphs'][36];pos=p['source_position'];self.assertIn('raw_start',pos);pos['raw_start']+=1;pos['raw_end']+=1
  with self.assertRaises(ValueError):self.check(self.rows[5],c=c)
if __name__=='__main__':unittest.main()
