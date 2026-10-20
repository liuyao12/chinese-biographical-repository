"""Source-bound regression: ancestor, not biography head, owns the sibling list."""
from pathlib import Path
import json,copy,unittest
from scripts.reported_ancestor_siblings import reported_ancestor_siblings_valid
from scripts.validate_corpus import source_age_number
F=json.loads((Path(__file__).parent/'fixtures/liang030-ancestor-siblings.json').read_text());C=F['chapter'];A=F['assertions'];PARAS={p['id']:(C['id'],p)for p in C['paragraphs']};BROTHERS=A[4:]
def valid(a,records=A,paras=PARAS):return reported_ancestor_siblings_valid(a,paras,records,source_age_number)
class SourceBoundSiblings(unittest.TestCase):
 def test_actual_three_siblings(self):
  for a in BROTHERS:self.assertTrue(valid(a))
 def test_biography_subject_cannot_replace_ancestor(self):
  a=copy.deepcopy(BROTHERS[0]);a['subject_person_id']=A[0]['subject_person_id'];a['evidence'][0]['subject_person_mention_id']=A[0]['evidence'][0]['subject_person_mention_id'];self.assertFalse(valid(a))
 def test_reverse_age_or_absolute_ordinal_rejected(self):
  for a in BROTHERS:
   q=copy.deepcopy(a);o=q['qualifiers']['relative_birth_order'];o['older_person_id'],o['younger_person_id']=o['younger_person_id'],o['older_person_id'];self.assertFalse(valid(q))
   q=copy.deepcopy(a);q['qualifiers']['relative_birth_order']['older_ordinal']=1;self.assertFalse(valid(q))
 def test_invented_shared_parent_rejected(self):
  for key in ['shared_father','shared_mother']:
   a=copy.deepcopy(BROTHERS[0]);a['qualifiers'][key]=True;self.assertFalse(valid(a))
 def test_source_distance_must_remain_unadopted(self):
  for key,value in [('generation_distance',8),('adopted_for_family_tree',True),('reported_generation_number',9)]:
   records=copy.deepcopy(A);records[3]['qualifiers'][key]=value;self.assertFalse(valid(records[4],records))
 def test_bad_anchor_position_and_nonperson_rejected(self):
  for kind,value in [('start',0),('kind','unresolved')]:
   paras=copy.deepcopy(PARAS);p=next(iter(paras.values()))[1];m=next(m for m in p['mentions']if m['id']==BROTHERS[0]['evidence'][0]['subject_person_mention_id']);m[kind]=value;self.assertFalse(valid(BROTHERS[0],paras=paras))
 def test_missing_ancestry_or_wrong_evidence_rejected(self):
  self.assertFalse(valid(BROTHERS[0],A[:3]+A[4:]))
  a=copy.deepcopy(BROTHERS[0]);a['evidence'][0]['quote']='partial unrelated';self.assertFalse(valid(a))
 def test_review_state_is_boolean_not_semantic_override(self):
  a=copy.deepcopy(BROTHERS[0]);a['human_reviewed']=True;self.assertTrue(valid(a))
  a['human_reviewed']='true';self.assertFalse(valid(a))
 def test_annotation_layer_rejected_without_top_level_layer(self):
  for target in ['paragraph','source_position']:
   for key,value in [('source_layer','commentary'),('text_layer','attached_note'),('annotator','裴松之'),('attached_note_to_paragraph_id','another')]:
    paras=copy.deepcopy(PARAS);p=next(iter(paras.values()))[1];p.pop('source_layer',None)
    metadata=p if target=='paragraph' else p['source_position'];metadata[key]=value
    self.assertFalse(valid(BROTHERS[0],paras=paras),(target,key))
 def test_explicit_body_layer_remains_valid(self):
  paras=copy.deepcopy(PARAS);p=next(iter(paras.values()))[1];p['source_position']['source_layer']='received_biography';p['source_position']['text_layer']='received_chapter'
  self.assertTrue(valid(BROTHERS[0],paras=paras))
if __name__=='__main__':unittest.main()
