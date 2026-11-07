from pathlib import Path
import sys,json,copy,unittest
F=Path(__file__).resolve().parents[1];sys.path.insert(0,str(F))
from scripts.fixed_jin080_wangxizhi_comparison import source_errors,family_valid,validate_surname
from scripts.biography_family_clause import valid
from scripts.directed_uncle_roles import paternal_uncle_direction_valid
from scripts.non_parental_family import non_parental_relation_valid
C=json.loads((F/'corpus/jinshu/080-wangxizhi-comparison.json').read_text());PP={p['id']:(C['id'],p)for p in C['paragraphs']};A=json.loads((F/'corpus/jinshu/080-wangxizhi-comparison-assertions.json').read_text())['assertions'];N=json.loads((F/'corpus/jinshu/080-wangxizhi-comparison-names.json').read_text())['records']
class Tests(unittest.TestCase):
 def test_complete_47_331(self):self.assertEqual([],source_errors(C,F));self.assertEqual(47,len(C['paragraphs']));self.assertEqual(331,sum(len(p['mentions'])for p in C['paragraphs']))
 def test_all19_actual_general_gate(self):
  self.assertEqual(19,len(A))
  for a in A:self.assertTrue(valid(a,PP,A,{C['id']:C},F),a['id'])
 def test_uncle_direction(self):
  a=next(a for a in A if a['predicate']=='paternal_uncle');self.assertTrue(paternal_uncle_direction_valid(a,PP));b=copy.deepcopy(a);b['subject_person_id'],b['object_person_id']=b['object_person_id'],b['subject_person_id'];self.assertFalse(paternal_uncle_direction_valid(b,PP))
 def test_ritual_not_father(self):
  a=next(a for a in A if a['predicate']=='ritual_successor_of');self.assertTrue(non_parental_relation_valid(a,PP,A));b=copy.deepcopy(a);b['predicate']='father';self.assertFalse(family_valid(b,PP,F))
 def test_wrong_subject(self):
  a=copy.deepcopy(A[0]);a['subject_person_id']=A[0]['object_person_id'];self.assertFalse(family_valid(a,PP,F))
 def test_cross_paragraph(self):
  a=copy.deepcopy(A[0]);a['evidence'][0]['paragraph_id']=C['paragraphs'][1]['id'];self.assertFalse(family_valid(a,PP,F))
 def test_fake_absolute_order(self):
  a=copy.deepcopy(A[-1]);a['qualifiers']['relative_birth_order']['older_ordinal']=1;self.assertFalse(family_valid(a,PP,F))
 def test_all_inferred_names(self):
  for n in N:
   if 'surname_basis'in n:validate_surname(n,N,{C['id']:C},A,F)
 def test_unknown_ming_clan_style(self):
  from scripts.person_bundle import validate_clan_style
  for n in N:
   if 'clan_style'in n:
    self.assertIsNone(n['ming']);validate_clan_style(n,PP[n['paragraph_id']][1],A)
 def test_clan_wrong_father(self):
  from scripts.person_bundle import validate_clan_style
  n=copy.deepcopy(next(n for n in N if 'clan_style'in n));n['clan_style_basis']['father_assertion_id']='a-jin080-zhenzhi-father-huizhi'
  with self.assertRaises(ValueError):validate_clan_style(n,PP[n['paragraph_id']][1],A)
 def test_wrong_surname(self):
  n=copy.deepcopy(next(n for n in N if 'surname_basis'in n));n['surname']='謝'
  with self.assertRaises(ValueError):validate_surname(n,N,{C['id']:C},A,F)
 def test_missing_name_seed(self):
  n=next(n for n in N if 'surname_basis'in n)
  with self.assertRaises(ValueError):validate_surname(n,[n],{C['id']:C},A,F)
 def test_false_wyd(self):
  c=copy.deepcopy(C);c['source']['edition']='武英殿';self.assertTrue(source_errors(c,F))
 def test_transferred_role(self):
  c=copy.deepcopy(C);c['paragraphs'][0]['mentions'][0]['person_id']=next(m['person_id']for m in C['paragraphs'][0]['mentions']if m['person_id']!=c['paragraphs'][0]['mentions'][0]['person_id']);self.assertTrue(source_errors(c,F))
 def test_shifted_whole_text(self):
  c=copy.deepcopy(C);p=c['paragraphs'][0];p['text']='甲'+p['text'];
  for m in p['mentions']:m['start']+=1;m['end']+=1
  self.assertTrue(source_errors(c,F))
 def test_malformed_qualifiers_fail_closed(self):
  for q in [None,[],{'source_clause_binding':[]}]:
   a=copy.deepcopy(A[0]);a['qualifiers']=q;self.assertFalse(valid(a,PP,A,{C['id']:C},F))
 def test_no_common_father_on_brother(self):
  a=copy.deepcopy(next(a for a in A if a['id']=='a-jin080-xizhi-unnamed-older-brother'));a['qualifiers']['shared_father']=True;self.assertFalse(family_valid(a,PP,F))
 def test_false_human_review_type(self):
  a=copy.deepcopy(A[0]);a['human_reviewed']=0;self.assertFalse(family_valid(a,PP,F))
 def test_false_offset_bool(self):
  c=copy.deepcopy(C);c['paragraphs'][0]['mentions'][0]['start']=False;self.assertTrue(source_errors(c,F))
 def test_bad_name_path(self):
  n=copy.deepcopy(next(n for n in N if 'surname_basis'in n));n['surname_basis']['steps'][0]['traversal']='mother_to_child'
  with self.assertRaises(ValueError):validate_surname(n,N,{C['id']:C},A,F)
 def test_note_layer_cannot_be_body(self):
  c=copy.deepcopy(C);c['paragraphs'][0]['text_layer']='witness_appended_pei_songzhi_note';self.assertTrue(source_errors(c,F))
 def test_unknown_malformed(self):
  for x in [None,[],{'id':C['id'],'paragraphs':None}]:self.assertTrue(source_errors(x,F))
if __name__=='__main__':unittest.main()
