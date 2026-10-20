# coding: utf-8
from pathlib import Path
import unittest,copy,json,importlib.util,sys
from scripts import directed_uncle_roles as mod
D=Path(__file__).resolve().parents[1]
C=json.loads((D/'corpus/songshu/046-zhangshao.json').read_bytes());A=json.loads((D/'corpus/songshu/046-zhangshao-assertions.json').read_bytes())['assertions'][3];P=C['paragraphs'][1]
class SourceUncleBinding(unittest.TestCase):
 def valid(self,p,a=None):return mod.paternal_uncle_direction_valid(a or A,{p['id']:(C['id'],p)})
 def test_complete_actual_paragraph(self):
  self.assertEqual(len(P['text']),463);self.assertTrue(self.valid(P));self.assertEqual(A['qualifiers']['father_sibling_role'],'elder_brother');self.assertEqual(A['qualifiers']['object_generation_relative_to_subject'],-1)
 def test_different_resumed_child(self):
  p=copy.deepcopy(P);m=next(m for m in p['mentions']if m['start']==413);m['person_id']='other_person';self.assertFalse(self.valid(p))
 def test_other_named_subject_in_mourning_scope(self):
  p=copy.deepcopy(P);i=p['text'].index('未拜父在');p['mentions'].append({'id':'negative-only','kind':'person','start':i,'end':i+2,'surface':p['text'][i:i+2],'person_id':'other_person'});self.assertFalse(self.valid(p))
 def test_no_biographical_head(self):
  p=copy.deepcopy(P);m=next(m for m in p['mentions']if m['start']==8);m['person_id']='other_person';self.assertFalse(self.valid(p))
 def test_from_mother_not_paternal_uncle(self):
  p=copy.deepcopy(P);a=copy.deepcopy(A);p['text']=p['text'].replace('伯父茂度','從母茂度');a['qualifiers']['source_term']='從母茂度每譬止之';a['evidence'][0]['quote']=p['text'];self.assertFalse(self.valid(p,a))
 def test_swapped_uncle_and_nephew(self):
  a=copy.deepcopy(A);a['subject_person_id'],a['object_person_id']=a['object_person_id'],a['subject_person_id'];self.assertFalse(self.valid(P,a))
 def test_same_surface_different_person_anchor(self):
  a=copy.deepcopy(A);a['object_person_id']='other_person';self.assertFalse(self.valid(P,a))
 def test_missing_raw_relation(self):
  a=copy.deepcopy(A);a['qualifiers']['source_term']='叔父茂度每譬止之';self.assertFalse(self.valid(P,a))
 def test_quoted_transfer_of_subject(self):
  p=copy.deepcopy(P);p['text']=p['text'][:399]+'曰'+p['text'][400:];a=copy.deepcopy(A);a['evidence'][0]['quote']=p['text'];self.assertFalse(self.valid(p,a))
 def test_longer_unanchored_prefix_not_allowed(self):
  p=copy.deepcopy(P);p['text']=p['text'][:4]+'曰'+p['text'][5:];a=copy.deepcopy(A);a['evidence'][0]['quote']=p['text'];self.assertFalse(self.valid(p,a))
if __name__=='__main__':unittest.main(verbosity=2)
