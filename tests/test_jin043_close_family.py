# coding: utf-8
from pathlib import Path
import json,sys,copy,hashlib,unittest
O=Path(__file__).parent;F=O.parent;sys.path.insert(0,str(F));from scripts.biography_family_clause import valid
from scripts.maternal_roles import maternal_role_valid
from scripts.collateral_kinship import agnatic_senior_kin_valid
from scripts.non_parental_family import non_parental_relation_valid
C=json.loads((F/'corpus/jinshu/043-wangrong.json').read_text());P={p['id']:(C['id'],p)for p in C['paragraphs']};A=json.loads((F/'corpus/jinshu/043-wangrong-assertions.json').read_text())['assertions']
def candidate(pred):return copy.deepcopy(next(a for a in A if a['predicate']==pred and a['qualifiers'].get('source_clause_binding',{}).get('rule','').startswith('close_family_')))
def mutate_text(a,old,new):
 p=copy.deepcopy(P);hit=p[a['evidence'][0]['paragraph_id']][1];assert len(old)==len(new);hit['text']=hit['text'].replace(old,new,1);a['evidence'][0]['quote']=hit['text'];a['qualifiers']['source_clause_binding']['paragraph_sha256']=hashlib.sha256(hit['text'].encode()).hexdigest();return p
class Contract(unittest.TestCase):
 def test_actual_12_and_hooks(self):
  for a in A:
   if a['qualifiers']['source_clause_binding']['kind']=='biography_family_clause':self.assertTrue(valid(a,P,A),a['id'])
  self.assertTrue(maternal_role_valid(candidate('maternal_role'),P));self.assertTrue(agnatic_senior_kin_valid(candidate('agnatic_senior_kin'),P));self.assertTrue(non_parental_relation_valid(candidate('ritual_successor_of'),P,A))
 def test_reversed_endpoints(self):
  for a in A[:12]:
   a=copy.deepcopy(a);a['subject_person_id'],a['object_person_id']=a['object_person_id'],a['subject_person_id'];self.assertFalse(valid(a,P,A))
 def test_wrong_role_anchor(self):
  a=candidate('father');a['qualifiers']['source_clause_binding']['roles']['father']=a['qualifiers']['source_clause_binding']['roles']['grandfather'];self.assertFalse(valid(a,P,A))
 def test_wrong_source_term(self):
  for original in A[:12]:
   a=copy.deepcopy(original);a['qualifiers']['source_term']=a['evidence'][0]['quote'][:1];self.assertFalse(valid(a,P,A))
 def test_wrong_offset(self):
  a=candidate('father');a['qualifiers']['source_clause_binding']['clause_start']+=1;self.assertFalse(valid(a,P,A))
 def test_truncated_quote(self):
  a=candidate('father');a['evidence'][0]['quote']=a['qualifiers']['source_term'];self.assertFalse(valid(a,P,A))
 def test_false_mother_and_biological_leak(self):
  a=candidate('maternal_role');p=mutate_text(a,'以母憂','以父憂');self.assertFalse(valid(a,p,A));a=candidate('maternal_role');a['qualifiers']['biological_mother']=True;self.assertFalse(maternal_role_valid(a,P))
 def test_mother_no_father_inference(self):
  a=candidate('maternal_role');a['qualifiers']['father_person_id']='synthetic';self.assertFalse(valid(a,P,A))
 def test_cousin_no_distance_or_common_ancestor(self):
  for field,value in [('distance',1),('common_ancestor_person_id','synthetic')]:
   a=candidate('agnatic_cousin');a['qualifiers']['kinship_structure'][field]=value;self.assertFalse(valid(a,P,A))
 def test_cousin_generation_and_order(self):
  a=candidate('agnatic_cousin');a['qualifiers']['kinship_structure']['generation_difference']=1;self.assertFalse(valid(a,P,A));a=candidate('agnatic_cousin');a['qualifiers']['relative_birth_order']['older_ordinal']=1;self.assertFalse(valid(a,P,A))
 def test_ritual_requires_explicit_father(self):
  a=candidate('ritual_successor_of');self.assertFalse(non_parental_relation_valid(a,P,[]))
 def test_ritual_not_legal_adoption(self):
  a=candidate('ritual_successor_of');a['qualifiers']['legal_adoption_status']='adopted';self.assertFalse(valid(a,P,A))
 def test_negated_or_nested_successor(self):
  for old,new in [('為嗣','非嗣'),('以從弟','曰從弟')]:
   a=candidate('ritual_successor_of');p=mutate_text(a,old,new);self.assertFalse(valid(a,p,A))
 def test_son_not_brother_no_ordinal(self):
  a=candidate('father');a['qualifiers']['birth_order']={'ordinal':1};self.assertFalse(valid(a,P,A));a=copy.deepcopy(A[3]);p=mutate_text(a,'子萬','弟萬');self.assertFalse(valid(a,p,A))
 def test_nephew_not_direct_uncle(self):
  a=candidate('agnatic_senior_kin');a['predicate']='paternal_uncle';self.assertFalse(valid(a,P,A))
 def test_same_surface_different_person_anchor(self):
  a=candidate('father');p=copy.deepcopy(P);hit=p[a['evidence'][0]['paragraph_id']][1];target=next(m for m in hit['mentions']if m['id']==a['evidence'][0]['object_person_mention_id']);target['person_id']='synthetic-other-id';self.assertFalse(valid(a,p,A))
 def test_no_person_id_allowlist(self):
  a=candidate('father');p=copy.deepcopy(P);mapping={a['subject_person_id']:'fixture-child',a['object_person_id']:'fixture-father'}
  a['subject_person_id']=mapping[a['subject_person_id']];a['object_person_id']=mapping[a['object_person_id']]
  for cid,pp in p.values():
   for m in pp['mentions']:m['person_id']=mapping.get(m['person_id'],m['person_id'])
  self.assertTrue(valid(a,p,A))
if __name__=='__main__':unittest.main()
