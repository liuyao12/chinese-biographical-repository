# coding:utf-8
import unittest,json,pathlib,copy,sys
O=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(O))
from scripts.biography_ritual_succession import valid
from scripts.non_parental_family import non_parental_relation_valid
C=json.load(open(O/'corpus/jinshu/069-zhouyi.json'));AS=json.load(open(O/'corpus/jinshu/069-zhouyi-assertions.json'))['assertions'];A=AS[-1];PS={p['id']:(C['id'],p)for p in C['paragraphs']}
class Ritual(unittest.TestCase):
 def test_actual_full_source(self):self.assertTrue(valid(A,PS,AS));self.assertTrue(non_parental_relation_valid(A,PS,AS))
 def checka(self,mut):
  a=copy.deepcopy(A);mut(a);self.assertFalse(valid(a,PS,AS))
 def test_wrong_head(self):self.checka(lambda a:a['evidence'][0].update(object_person_mention_id=a['qualifiers']['source_clause_binding']['father_person_mention_id']))
 def test_wrong_brother(self):self.checka(lambda a:a['qualifiers']['source_clause_binding'].update(father_person_mention_id=a['evidence'][0]['subject_person_mention_id']))
 def test_no_source_father(self):self.assertFalse(valid(A,PS,[]))
 def test_wrong_father_pair(self):
  aa=copy.deepcopy(AS);aa[4]['object_person_id']=A['object_person_id'];self.assertFalse(valid(A,PS,aa))
 def test_adoptive_father_rejected(self):self.checka(lambda a:a.update(predicate='adoptive_father'))
 def test_bio_father_rejected(self):self.checka(lambda a:a.update(predicate='father'))
 def test_cross_paragraph(self):self.checka(lambda a:a['evidence'][0].update(paragraph_id=C['paragraphs'][8]['id']))
 def test_removed_weisi(self):
  ps=copy.deepcopy(PS);p=ps[A['evidence'][0]['paragraph_id']][1];p['text']=p['text'].replace('為嗣','為官');a=copy.deepcopy(A);a['evidence'][0]['quote']=p['text'];self.assertFalse(valid(a,ps,AS))
 def test_replaced_adopted_word(self):
  ps=copy.deepcopy(PS);p=ps[A['evidence'][0]['paragraph_id']][1];p['text']=p['text'].replace('長子','養子');a=copy.deepcopy(A);a['evidence'][0]['quote']=p['text'];self.assertFalse(valid(a,ps,AS))
 def test_parentage_inferred_rejected(self):self.checka(lambda a:a['qualifiers'].update(parentage_inference='biological'))
 def test_incorrect_bounds(self):self.checka(lambda a:a['qualifiers']['source_clause_binding'].update(start=0))
 def test_head_not_named_start(self):
  ps=copy.deepcopy(PS);p=ps[A['evidence'][0]['paragraph_id']][1];p['text']='某'+p['text'];a=copy.deepcopy(A);a['evidence'][0]['quote']=p['text'];self.assertFalse(valid(a,ps,AS))
 def test_no_legal_adoption_claim(self):self.checka(lambda a:a['qualifiers'].update(legal_adoption_status='adopted'))
if __name__=='__main__':unittest.main(verbosity=2)
