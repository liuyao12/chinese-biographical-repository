# coding: utf-8
import unittest,copy,json
from pathlib import Path
from scripts.name_xiaoming import validate_xiaoming
class XiaomingNames(unittest.TestCase):
 def setUp(self):
  d=json.loads((Path(__file__).parent/'fixtures/song046_xiaoming.json').read_text());self.names=d['names'];self.p=d['paragraph']
 def fails(self,n=None):self.assertRaises(ValueError,validate_xiaoming,n or self.names[0],self.p)
 def test_both_persons(self):
  for n in self.names:self.assertIsNone(validate_xiaoming(n,self.p))
 def test_child_father_reversal(self):
  self.names[0]['person_id']=self.names[1]['person_id'];self.fails()
 def test_role_reversal(self):
  self.names[0]['xiaoming_basis']['subject_role']='father';self.fails()
 def test_wrong_value(self):self.names[0]['xiaoming']='梨';self.fails()
 def test_same_surface_different_person_id(self):
  mid=self.names[0]['xiaoming_basis']['child_value_anchor']['person_mention_id'];next(m for m in self.p['mentions']if m['id']==mid)['person_id']='other_same_name';self.fails()
 def test_wrong_offset(self):self.names[0]['xiaoming_basis']['child_value_anchor']['start']+=1;self.fails()
 def test_crop_quote(self):self.names[0]['quote']='敷小名查父邵小名梨';self.fails()
 def test_courtesy_marker_is_not_xiaoming(self):
  self.p['text']=self.p['text'].replace('敷小名查父邵小名梨','敷字也查父邵字也梨');self.names[0]['quote']=self.p['text'];self.fails()
 def test_xiaozhi_marker_is_not_xiaoming(self):
  self.p['text']=self.p['text'].replace('敷小名查父邵小名梨','敷小字查父邵小字梨');self.names[0]['quote']=self.p['text'];self.fails()
 def test_fruit_comparison_not_declaration(self):
  b=self.names[0]['xiaoming_basis'];at=self.p['text'].index('查何如梨');b['child_value_anchor'].update(start=at,end=at+1,surface='查');self.fails()
 def test_generic_fruit_without_basis(self):self.fails({'person_id':self.names[0]['person_id'],'xiaoming':'梨','quote':self.p['text']})
 def test_unknown_kind(self):self.names[0]['xiaoming_basis']['kind']='generic_fruit';self.fails()
 def test_missing_paired_parent_anchor(self):del self.names[0]['xiaoming_basis']['father_name_anchor'];self.fails()
 def test_clause_truncation(self):self.names[0]['xiaoming_basis']['clause_anchor']['end']-=1;self.fails()
 def test_wrong_marker_position(self):self.names[0]['xiaoming_basis']['father_marker_anchor']['start']-=1;self.fails()
 def test_zi_misclassification_with_xiaoming_evidence(self):
  n=self.names[0];n['zi']=n.pop('xiaoming');self.fails()
 def test_xiaozhi_misclassification_with_xiaoming_evidence(self):
  n=self.names[0];n['xiaozhi']=n.pop('xiaoming');self.fails()
 def test_generic_alias_stays_untyped(self):self.assertIsNone(validate_xiaoming({'additional_names':['查','梨']},None))
 def test_empty_value(self):self.names[0]['xiaoming']='';self.fails()
 def test_false_human_review(self):self.names[0]['xiaoming_basis']['human_reviewed']=True;self.fails()

 def test_insert_negation_with_all_offsets_rebased(self):
  at=self.names[0]['xiaoming_basis']['clause_anchor']['start'];self.p['text']=self.p['text'][:at]+'非'+self.p['text'][at:]
  for m in self.p['mentions']:
   if m['start']>=at:m['start']+=1;m['end']+=1
  for n in self.names:
   n['quote']=self.p['text']
   for key,a in n['xiaoming_basis'].items():
    if isinstance(a,dict)and'start'in a:a['start']+=1;a['end']+=1
  self.fails()
 def test_generic_pronoun_not_named_child(self):
  b=self.names[0]['xiaoming_basis'];at=b['child_name_anchor']['start'];self.p['text']=self.p['text'][:at]+'其'+self.p['text'][at+1:];self.names[0]['quote']=self.p['text'];b['child_name_anchor']['surface']='其';b['clause_anchor']['surface']=b['clause_anchor']['surface'].replace('敷','其',1);next(m for m in self.p['mentions']if m['id']==b['child_name_anchor']['person_mention_id'])['surface']='其';self.fails()
