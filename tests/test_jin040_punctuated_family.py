# coding: utf-8
import copy,hashlib,json,unittest
from pathlib import Path
from scripts.punctuated_family_frames import valid
R=Path(__file__).resolve().parents[1]
C=json.loads((R/'corpus/jinshu/040-jiachong-family.json').read_text())
P={p['id']:(C['id'],p)for p in C['paragraphs']}
A=json.loads((R/'corpus/jinshu/040-jiachong-family-assertions.json').read_text())['assertions']
class ReceivedFamilyTests(unittest.TestCase):
 def test_all_actual_source_roles(self):
  self.assertEqual(len(A),52)
  for a in A:self.assertTrue(valid(a,P,{C['id']:C},R),a['id'])
 def test_wrong_recipient_even_with_consistent_evidence(self):
  for a in A:
   b=copy.deepcopy(a);e=b['evidence'][0];p=P[e['paragraph_id']][1]
   legitimate={x['subject_person_id']for x in A if x['predicate']==a['predicate']and x['object_person_id']==a['object_person_id']and x['qualifiers']['received_family_frame']==a['qualifiers']['received_family_frame']}
   other=next((m for m in p['mentions']if m.get('person_id')not in(legitimate|{a['object_person_id']})and m.get('kind')=='person'),None)
   if other:
    e['subject_person_mention_id']=other['id'];b['subject_person_id']=other['person_id']
    self.assertFalse(valid(b,P),a['id'])
 def test_fixed_witness_guard_cannot_be_removed(self):
  a=A[0];c=copy.deepcopy(C);c['annotation'].pop('fixed_wikisource_unit_ref');self.assertFalse(valid(a,P,{C['id']:c},R))
 def test_raw_offsets_coshift_and_projection_hash_cannot_hide_change(self):
  a=A[0];c=copy.deepcopy(C);p=next(x for x in c['paragraphs']if x['id']==a['evidence'][0]['paragraph_id']);loc=p['source_position'];loc['raw_character_offsets']=[x+1 for x in loc['raw_character_offsets']];loc['projection_sha256']=hashlib.sha256((json.dumps(loc['raw_character_offsets'],ensure_ascii=False,indent=2)+'\n').encode()).hexdigest();ps=dict(P);ps[p['id']]=(c['id'],p);self.assertFalse(valid(a,ps,{c['id']:c},R))
 def test_unspecified_mothers_not_promoted_to_birth_mother(self):
  rows=[a for a in A if a['predicate']=='maternal_role'];self.assertEqual(len(rows),2)
  for a in rows:
   self.assertIsNone(a['qualifiers']['biological_mother']);self.assertIsNone(a['qualifiers']['father_person_id']);b=copy.deepcopy(a);b['predicate']='mother';self.assertFalse(valid(b,P))
 def test_maternity_qualifications_not_silently_removed(self):
  for a in A:
   if a['predicate']=='mother':
    self.assertIn('birth_mother_interpretation',a['qualifiers']);b=copy.deepcopy(a);b['qualifiers'].pop('birth_mother_interpretation');self.assertFalse(valid(b,P))
 def test_reverse_subject_object_rejected(self):
  for a in A:
   b=copy.deepcopy(a);b['subject_person_id'],b['object_person_id']=b['object_person_id'],b['subject_person_id'];e=b['evidence'][0];e['subject_person_mention_id'],e['object_person_mention_id']=e['object_person_mention_id'],e['subject_person_mention_id']
   self.assertFalse(valid(b,P),a['id'])
 def test_maternal_collateral_no_invented_path(self):
  a=next(a for a in A if a['qualifiers'].get('source_term')=='從舅')
  self.assertEqual(a['subject_person_id'],next(m['person_id']for m in C['paragraphs'][-1]['mentions']if m['surface']=='賈后'))
  self.assertEqual(a['qualifiers']['generation_difference'],-1)
  for field,value in [('generation_difference',-2),('lineage','paternal'),('connecting_person_ids',['invented']),('common_ancestor_person_id','invented')]:
   b=copy.deepcopy(a);b['qualifiers'][field]=value;self.assertFalse(valid(b,P))
 def test_no_collateral_becomes_father(self):
  for a in A:
   if a['predicate']=='kinship_unspecified':
    b=copy.deepcopy(a);b['predicate']='father';self.assertFalse(valid(b,P))
 def test_adoption_is_not_biological_or_rearing(self):
  a=next(a for a in A if a['predicate']=='adoptive_father')
  for pred in('father','raised_by'):
   b=copy.deepcopy(a);b['predicate']=pred;self.assertFalse(valid(b,P))
  for field,value in [('actual_upbringing',True),('modern_legal_status','legal_adoption'),('biological_parentage','replaced')]:
   b=copy.deepcopy(a);b['qualifiers'][field]=value;self.assertFalse(valid(b,P))
 def test_named_biological_parents_retained(self):
  a=next(a for a in A if a['predicate']=='adoptive_father');child=a['subject_person_id']
  self.assertEqual({a['predicate']for a in A if a['subject_person_id']==child and a['predicate']in('father','mother','adoptive_father','ritual_successor_of')},{'father','mother','adoptive_father','ritual_successor_of'})
 def test_queen_mother_not_nested_chong(self):
  a=next(a for a in A if a['qualifiers']['received_family_frame']['rule']=='queen_mother_title');b=copy.deepcopy(a);e=b['evidence'][0];p=P[e['paragraph_id']][1];other=next(m for m in p['mentions']if m['surface']=='充'and m['start']>a['qualifiers']['received_family_frame']['clause_start'])
  b['subject_person_id']=other['person_id'];e['subject_person_mention_id']=other['id'];self.assertFalse(valid(b,P))
 def test_milk_nurse_not_spouse(self):
  a=next(a for a in A if a['qualifiers']['received_family_frame']['rule']=='wife_named');b=copy.deepcopy(a);e=b['evidence'][0];p=P[e['paragraph_id']][1];m=next(m for m in p['mentions']if m['surface']=='乳母');b['subject_person_id']=m['person_id'];e['subject_person_mention_id']=m['id'];self.assertFalse(valid(b,P))
 def test_extra_fields_and_absolute_ordinals_rejected(self):
  for a in A:
   b=copy.deepcopy(a);b['qualifiers']['invented_father']='none';self.assertFalse(valid(b,P))
   if 'relative_birth_order'in a['qualifiers']:
    b=copy.deepcopy(a);b['qualifiers']['relative_birth_order']['younger_ordinal']=2;self.assertFalse(valid(b,P))
 def test_changed_text_hash_not_enough_to_change_family_grammar(self):
  a=next(a for a in A if a['qualifiers']['received_family_frame']['rule']=='brother_named');b=copy.deepcopy(a);ps=copy.deepcopy(P);p=ps[b['evidence'][0]['paragraph_id']][1];p['text']=p['text'].replace('遵弟模','遵母模');b['evidence'][0]['quote']=p['text'];b['qualifiers']['received_family_frame']['paragraph_sha256']=hashlib.sha256(p['text'].encode()).hexdigest();self.assertFalse(valid(b,ps))
 def test_all_roles_remappable_without_id_allowlist(self):
  a=next(a for a in A if a['qualifiers']['received_family_frame']['rule']=='maternal_collateral_head');b=copy.deepcopy(a);ps=copy.deepcopy(P);p=ps[b['evidence'][0]['paragraph_id']][1];mapping={m['person_id']:'synthetic_'+str(i)for i,m in enumerate(p['mentions'])if m.get('person_id')}
  for m in p['mentions']:
   if m.get('person_id')in mapping:m['person_id']=mapping[m['person_id']]
  b['subject_person_id']=mapping[b['subject_person_id']];b['object_person_id']=mapping[b['object_person_id']];self.assertTrue(valid(b,ps))
if __name__=='__main__':unittest.main()
