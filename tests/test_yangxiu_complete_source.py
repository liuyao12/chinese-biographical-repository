# coding:utf-8
import unittest,json,copy,tempfile,hashlib
from pathlib import Path
from scripts.fixed_wikisource_units import source_errors
from scripts.punctuated_family_frames import valid
from scripts.biography_congfudi import biography_congfudi_valid as cousin_valid
R=Path(__file__).resolve().parents[1];C=json.loads((R/'corpus/jinshu/093-yangxiu.json').read_bytes());PS=C['paragraphs'];A=json.loads((R/'corpus/jinshu/093-yangxiu-assertions.json').read_bytes())['assertions'];P={p['id']:(C['id'],p)for p in PS}
class Yangxiu(unittest.TestCase):
 def test_complete_three_source(self):
  self.assertEqual(len(PS),3);self.assertEqual(sum(len(p['text'])for p in PS),652);self.assertFalse(source_errors(C,R));self.assertIn('諡曰威',PS[-1]['text']);self.assertFalse(C['source']['image_verified']);self.assertIsNone(C['source']['edition'])
 def test_all_three_frames(self):
  self.assertEqual({a['predicate']for a in A},{'father','brother','agnatic_cousin'})
  for a in A:self.assertTrue(cousin_valid(a,P)if a['predicate']=='agnatic_cousin'else valid(a,P,{C['id']:C},R))
 def test_role_swap_rejected(self):
  for a in [a for a in A if a['predicate']!='agnatic_cousin']:
   b=copy.deepcopy(a);r=b['qualifiers']['received_family_frame']['roles'];r['father'],r['brother']=r['brother'],r['father'];self.assertFalse(valid(b,P,{C['id']:C},R))
 def test_courtesy_same_person_guard(self):
  a=copy.deepcopy(A[0]);p=copy.deepcopy(PS[0]);m=next(m for m in p['mentions']if m['surface']=='稚舒');m['person_id']='synthetic_other';self.assertFalse(valid(a,{p['id']:(C['id'],p)}))
 def test_quotation_not_narrative(self):
  for a in [a for a in A if a['predicate']!='agnatic_cousin']:
   p=copy.deepcopy(PS[0]);a=copy.deepcopy(a);p['text']='「'+p['text']+'」';b=a['qualifiers']['received_family_frame'];b['clause_start']+=1;b['clause_end']+=1;b['paragraph_sha256']=hashlib.sha256(p['text'].encode()).hexdigest();a['evidence'][0]['quote']=p['text']
   for m in p['mentions']:m['start']+=1;m['end']+=1
   self.assertFalse(valid(a,{p['id']:(C['id'],p)}))
 def test_distinct_father_brother_roles(self):
  a=copy.deepcopy(A[0]);p=copy.deepcopy(PS[0]);father=next(m for m in p['mentions']if m['surface']=='耽');brother=next(m for m in p['mentions']if m['surface']=='瑾');brother['person_id']=father['person_id'];self.assertFalse(valid(a,{p['id']:(C['id'],p)}))
 def test_collateral_no_parent_invention(self):
  a=next(a for a in A if a['predicate']=='agnatic_cousin');self.assertIsNone(a['qualifiers']['kinship_structure']['common_ancestor_person_id']);self.assertEqual(a['qualifiers']['kinship_structure']['generation_difference'],0);self.assertEqual(len(A),3);self.assertFalse(any(a['subject_person_id']==next(m['person_id']for m in PS[0]['mentions']if m['surface']=='瑾')for a in A))
 def test_cousin_qualified_not_genetic(self):
  a=next(a for a in A if a['predicate']=='agnatic_cousin');self.assertEqual(a['qualifiers']['literary_usage']['qualification'],'preferred_normal_classical_usage_not_genetic_verification');self.assertEqual(a['qualifiers']['kinship_structure']['subject_relative_age'],'younger');b=copy.deepcopy(a);b['qualifiers']['kinship_structure']['distance']['common_ancestor_depth']['subject']=3;self.assertFalse(cousin_valid(b,P))
 def test_same_025_subject_and_explicit_093_fullname(self):
  other=json.loads((R/'corpus/sanguozhi/025-xinpi.json').read_bytes());pid=next(m['person_id']for p in other['paragraphs']for m in p['mentions']if m['surface']=='琇');self.assertEqual(pid,next(m['person_id']for m in PS[0]['mentions']if m['surface']=='羊琇'))
 def test_queen_reuses_existing_hongxun_via_complete_primary(self):
  import hashlib
  bridge=json.loads((R/'source-evidence/jin093-yangxiu/queen-identity-bridge.json').read_bytes());pr=bridge['prior_reference'];other=json.loads((R/pr['native_path']).read_bytes());p=next(p for p in other['paragraphs']if p['id']==pr['paragraph_id']);m=next(m for m in p['mentions']if m['id']==pr['mention_id']);local=next(m for m in PS[0]['mentions']if m['surface']=='景獻皇后');self.assertEqual(local['person_id'],m['person_id']);self.assertEqual(m['surface'],'弘訓太后');self.assertEqual(p['text'],pr['quote']);parallel=bridge['parallel_source'];raw=(R/parallel['raw_file']).read_bytes();self.assertEqual(hashlib.sha256(raw).hexdigest(),parallel['raw_sha256']);t=raw.decode();u=parallel['selection'];self.assertEqual(t[u['start']:u['end']],u['raw']);self.assertEqual(len(parallel['complete_projected_paragraphs']),2)
  for a in parallel['role_anchors']:self.assertEqual(t[a['start']:a['end']],a['quote'])
  self.assertIn('號弘訓太后',u['raw']);self.assertIn('合食於景皇帝',pr['quote'])
 def test_no_typed_dates_or_office_in_this_source_batch(self):
  for p in PS:
   for m in p['mentions']:self.assertEqual(p['text'][m['start']:m['end']],m['surface'])
  self.assertIn('任領護各十年',PS[0]['text']);self.assertIn('在職十三年',PS[0]['text']);self.assertFalse(C['annotation'].get('death_dates'));self.assertFalse(C['annotation'].get('title_tenures'))
if __name__=='__main__':unittest.main()
