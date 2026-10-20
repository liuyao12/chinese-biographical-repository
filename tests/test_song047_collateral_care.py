from pathlib import Path
import json,copy,unittest
from scripts.song047_collateral_care import valid,chronology_caution_valid,preferred_relation
R=Path(__file__).resolve().parents[1]
class Song047CollateralCareTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=json.loads((R/'corpus/songshu/047-liuhuaisu.json').read_text());cls.ps={p['id']:(cls.c['id'],p)for p in cls.c['paragraphs']};cls.rows={a['id'][-3:]:a for a in json.loads((R/'corpus/songshu/047-liuhuaisu-assertions.json').read_text())['assertions']if a['id'][-3:]in('001','008','009','013')}
 def test_actual_four_clauses_and_unknowns(self):
  self.assertEqual(len(self.rows),4)
  for a in self.rows.values():self.assertTrue(valid(a,self.ps),a['id'])
  self.assertTrue(chronology_caution_valid(self.rows['001'],R))
  self.assertEqual(self.rows['008']['subject_person_id'],'3dv_ken_w58');self.assertEqual(self.rows['009']['subject_person_id'],'3dv_ken_w58')
  self.assertIsNone(self.rows['008']['qualifiers']['mother_person_id'])
  self.assertEqual(self.rows['013']['qualifiers']['kinship_structure']['generation_difference'],-1)
 def test_wrong_direction_parentage_distance_and_source_rejected(self):
  for n,a in self.rows.items():
   for what in('reverse','term','position','revision','quote','predicate'):
    x=copy.deepcopy(a)
    if what=='reverse':x['subject_person_id'],x['object_person_id']=x['object_person_id'],x['subject_person_id']
    if what=='term':x['qualifiers']['source_term']+='改'
    if what=='position':x['qualifiers']['source_clause_binding']['start']+=1
    if what=='revision':x['qualifiers']['source_clause_binding']['source_revision']='wrong'
    if what=='quote':x['evidence'][0]['quote']+='改'
    if what=='predicate':x['predicate']='father'
    self.assertFalse(valid(x,self.ps),(n,what))
  for n in('001','013'):
   for key,value in(('distance',2),('common_ancestor_person_id','someone'),('generation_difference',0 if n=='013'else-1)):
    x=copy.deepcopy(self.rows[n]);x['qualifiers']['kinship_structure'][key]=value;self.assertFalse(valid(x,self.ps))
  x=copy.deepcopy(self.rows['008']);x['qualifiers']['mother_person_id']='vke_n1n_e2q';self.assertFalse(valid(x,self.ps))
  for key,value in(('legal_adoption_status','adopted'),('biological_parentage_inference','birth_mother')):
   x=copy.deepcopy(self.rows['009']);x['qualifiers'][key]=value;self.assertFalse(valid(x,self.ps))
 def test_preferred_unknown_preserves_raw_older(self):
  a=copy.deepcopy(self.rows['001']);p=preferred_relation(a)
  self.assertEqual(a,self.rows['001']);self.assertEqual(a['qualifiers']['kinship_structure']['subject_relative_age'],'older');self.assertIn('relative_birth_order',a['qualifiers'])
  self.assertEqual(p['qualifiers']['kinship_structure']['subject_relative_age'],'unknown');self.assertNotIn('relative_birth_order',p['qualifiers'])
  self.assertEqual(p['qualifiers']['relative_age_interpretation']['preferred_subject_relative_age'],None)
 def test_chronology_case_hash_and_preference_guard(self):
  for key,value in(('case_sha256','0'*64),('case_id','fake'),('case_path','../private.json')):
   x=copy.deepcopy(self.rows['001']);x['qualifiers']['relative_age_interpretation'][key]=value;self.assertFalse(chronology_caution_valid(x,R))
  x=copy.deepcopy(self.rows['001']);x['qualifiers']['relative_age_interpretation']['preferred_subject_relative_age']='older';self.assertFalse(valid(x,self.ps))
if __name__=='__main__':unittest.main()
