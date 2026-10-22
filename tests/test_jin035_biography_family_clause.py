import unittest,json,copy
from pathlib import Path
from scripts.biography_family_clause import valid
from scripts.non_parental_family import non_parental_relation_valid
ROOT=Path(__file__).resolve().parents[1]
class Jin035FamilyClause(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  c=json.loads((ROOT/'corpus/jinshu/035-pei-family.json').read_text());cls.ps={p['id']:(c['id'],p)for p in c['paragraphs']};cls.aa=json.loads((ROOT/'corpus/jinshu/035-pei-family-assertions.json').read_text())['assertions'];cls.aa=[a for a in cls.aa if a.get('qualifiers',{}).get('source_clause_binding',{}).get('kind')=='biography_family_clause']
 def test_all_source_clauses(self):
  self.assertEqual(len(self.aa),36)
  for a in self.aa:self.assertTrue(valid(a,self.ps,self.aa),a['id'])
 def test_ritual_production_dispatch(self):
  a=next(a for a in self.aa if a['predicate']=='ritual_successor_of');self.assertTrue(non_parental_relation_valid(a,self.ps,self.aa));self.assertFalse(non_parental_relation_valid(a,self.ps,[]))
 def test_reversed_and_truncated(self):
  for original in self.aa:
   a=copy.deepcopy(original);a['subject_person_id'],a['object_person_id']=a['object_person_id'],a['subject_person_id'];self.assertFalse(valid(a,self.ps,self.aa))
   a=copy.deepcopy(original);a['evidence'][0]['quote']=a['evidence'][0]['quote'][:-1];self.assertFalse(valid(a,self.ps,self.aa))
 def test_unknown_cousin_distance(self):
  a=copy.deepcopy(next(a for a in self.aa if a['predicate']=='agnatic_cousin'));a['qualifiers']['kinship_structure']['distance']=1;self.assertFalse(valid(a,self.ps,self.aa))
 def test_no_birth_mother_or_list_ordinal(self):
  for original in self.aa:
   a=copy.deepcopy(original);a['qualifiers']['biological_mother_person_id']='invented';self.assertFalse(valid(a,self.ps,self.aa))
   if a['qualifiers']['source_clause_binding']['rule']=='named_children_list':
    a=copy.deepcopy(original);a['qualifiers']['birth_order']={'ordinal':1};self.assertFalse(valid(a,self.ps,self.aa))
