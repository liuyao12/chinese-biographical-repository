import unittest,json,copy
from pathlib import Path
from unittest.mock import patch
from scripts.fixed_witness_fact_slots import valid,records,recipes
R=Path(__file__).resolve().parents[1]
class Qualification(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=json.loads((R/'corpus/jinshu/031-jingxian-yanghou.json').read_bytes());cls.a=next(x for x in json.loads((R/'corpus/jinshu/031-jingxian-yanghou-assertions.json').read_bytes())['assertions']if x['id'].endswith('queen-mother'))
 def test_current_contextual_not_explicit(self):
  self.assertTrue(valid(self.a,self.c,R));mi=self.a['qualifiers']['maternal_interpretation'];self.assertEqual(mi['status'],'contextual_preferred');self.assertIs(mi['source_explicit_birth'],False);self.assertEqual(len(mi['supporting_source_references']),3)
 def test_explicit_birth_rejected(self):
  a=copy.deepcopy(self.a);a['qualifiers']['maternal_interpretation']['status']='source_explicit_birth';self.assertFalse(valid(a,self.c,R))
 def test_missing_qualification_rejected(self):
  a=copy.deepcopy(self.a);del a['qualifiers']['maternal_interpretation'];self.assertFalse(valid(a,self.c,R))
 def test_prior_mother_not_birth_mother(self):
  a=copy.deepcopy(self.a);c=json.loads((R/'corpus/jinshu/034-yanghu.json').read_bytes());a['object_person_id']=next(m['person_id']for m in c['paragraphs'][39]['mentions']if m['surface']=='前母');self.assertFalse(valid(a,self.c,R))
 def test_same_word_cannot_replace_source_reference(self):
  a=copy.deepcopy(self.a);a['qualifiers']['maternal_interpretation']['supporting_source_references'][-1]['quote']='祜母';self.assertFalse(valid(a,self.c,R))
 def test_proof_omission_even_consistent_recipe_rejected(self):
  cfg=copy.deepcopy(recipes());del cfg['jin031-jingxian-yanghou']['maternal_context_proofs']
  with patch('scripts.fixed_witness_fact_slots.recipes',return_value=cfg):self.assertFalse(valid(self.a,self.c,R))
 def test_wrong_role_in_trusted_reference_rejected(self):
  cfg=copy.deepcopy(recipes());w=cfg['jin031-jingxian-yanghou']['maternal_context_proofs'][0]['witnesses'][2];w['role_bindings']['mother']=copy.deepcopy(w['role_bindings']['prior_mother'])
  with patch('scripts.fixed_witness_fact_slots.recipes',return_value=cfg):self.assertFalse(valid(self.a,self.c,R))
 def test_raw_hash_reference_rejected(self):
  cfg=copy.deepcopy(recipes());cfg['jin031-jingxian-yanghou']['maternal_context_proofs'][0]['witnesses'][1]['raw_sha256']='0'*64
  with patch('scripts.fixed_witness_fact_slots.recipes',return_value=cfg):self.assertFalse(valid(self.a,self.c,R))
if __name__=='__main__':unittest.main()
