# coding:utf-8
import sys,json,pathlib,copy,unittest,importlib.util
V=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(V));sys.dont_write_bytecode=True
from scripts.person_bundle import load_catalog
from scripts.personless_namespace import namespace_members,namespace_index_root,father_bound
from scripts.family_assemblies import load_assemblies
P,RECORDS=load_catalog(V);A={a['id']:a for r in RECORDS if r.get('record_type')=='person_assertion_set'for a in r['assertions']};C={c['id']:c for c in RECORDS if c.get('record_type')=='marked_chapter'}
ASSEMBLY=next(a for a in json.loads((V/'registry/family-assemblies.json').read_bytes())['assemblies']if a.get('id')=='fa-zhou-runan-pei-rui')
class Namespace(unittest.TestCase):
 def setUp(self):self.x=copy.deepcopy(ASSEMBLY);self.a=copy.deepcopy(A);self.c=copy.deepcopy(C);self.p=copy.deepcopy(P)
 def reject(self):
  with self.assertRaises(ValueError):namespace_members(self.x,self.p,self.a,self.c)
 def test_positive15(self):self.assertEqual(len(namespace_members(self.x,self.p,self.a,self.c)),15)
 def test_true_review_equivalent(self):
  self.x['human_reviewed']=True;self.x['collateral_root_group']['human_reviewed']=True;self.assertEqual(len(namespace_members(self.x,self.p,self.a,self.c)),15)
 def test_review_wrong_shape(self):self.x['human_reviewed']='false';self.reject()
 def test_namespace_person(self):self.p[self.x['namespace_id']]={'id':self.x['namespace_id']};self.reject()
 def test_named_common_parent(self):self.x['collateral_root_group']['common_parent_name']='某';self.reject()
 def test_parent_id(self):self.x['collateral_root_group']['common_parent_person_id']='madeup';self.reject()
 def test_hidden_parent(self):self.x['collateral_root_group']['common_parent_birth']=200;self.reject()
 def test_parent_age(self):self.x['collateral_root_group']['relative_age']='older';self.reject()
 def test_metric_unknown(self):self.a['a-jinshu061-congfudi-001']['qualifiers']['kinship_structure']['distance']=None;self.reject()
 def test_wrong_term(self):self.a['a-jinshu061-congfudi-001']['qualifiers']['source_term']='從弟';self.reject()
 def test_missing_father(self):self.x['collateral_root_group']['named_father_assertion_ids'].pop();self.reject()
 def test_wrong_father_subject(self):self.a['a-jin061-fu-father']['subject_person_id']='madeup';self.reject()
 def test_wrong_father_object(self):self.a['a-jin061-fu-father']['object_person_id']='madeup';self.reject()
 def test_father_conflict(self):
  other=copy.deepcopy(self.a['a-jin061-fu-father']);other['object_person_id']='other';self.a['synthetic-conflict']=other;self.reject()
 def test_father_layer(self):self.c['c-jinshu-061-zhou-family']['paragraphs'][0]['source_position']['annotator']='裴松之';self.reject()
 def test_nested_father_layers_both_received_heads(self):
  for index in [0,19]:
   original=copy.deepcopy(self.c)
   self.c['c-jinshu-061-zhou-family']['paragraphs'][index]['source_position']['text_layer']='pei_annotation';self.reject();self.c=original
 def test_each_father_bound_rejects_only_nested_text_layer(self):
  for aid in ['a-jin061-jun-father','a-jin061-fu-father']:
   self.c=copy.deepcopy(C);a=self.a[aid];self.assertTrue(father_bound(a,self.c))
   p=next(p for p in self.c[a['evidence'][0]['chapter_id']]['paragraphs']if p['id']==a['evidence'][0]['paragraph_id'])
   p.pop('source_layer',None);p.pop('text_layer',None);p['source_position'].pop('source_layer',None);p['source_position'].pop('annotator',None)
   p['source_position']['text_layer']='pei_annotation';self.assertFalse(father_bound(a,self.c))
 def test_nested_cousin_layer(self):self.c['c-jinshu-061-zhou-family']['paragraphs'][19]['source_position']['text_layer']='witness_appended_pei_songzhi_note';self.reject()
 def test_member_hidden_ancestor(self):self.x['members'][0]['ancestor_person_id']='madeup';self.reject()
 def test_duplicate_reference(self):self.x['collateral_root_group']['references'].append(copy.deepcopy(self.x['collateral_root_group']['references'][0]));self.reject()
 def test_cousin_layer(self):self.c['c-jinshu-061-zhou-family']['paragraphs'][19]['source_position']['source_layer']='pei_annotation';self.reject()
 def test_wrong_quote(self):self.x['collateral_root_group']['references'][0]['quote']='截短';self.reject()
 def test_fake_root_parent(self):self.x['members'][0]['parent_person_id']=self.x['members'][-1]['person_id'];self.reject()
 def test_extra_root(self):self.x['members'][1]['parent_person_id']=None;self.reject()
 def test_no_alias(self):self.x['members'][0]['source_person_ids'].append('old-id');self.reject()
 def test_bad_generation(self):self.x['members'][1]['person_id']+='A';self.reject()
 def test_root_is_not_person(self):self.x['root_person_id']=self.x['entry_person_id'];self.reject()
 def test_entry_must_real_root(self):self.x['entry_person_id']=self.x['namespace_id'];self.reject()
 def test_index_namespace_heading(self):
  rows=[dict(person_id=r['person_id'],label='真人',assembled_identity=dict(r,namespace_id=self.x['namespace_id'],namespace_entry_person_id=self.x['entry_person_id']))for r in self.x['members']]
  h=namespace_index_root(self.x['namespace_id'],rows);self.assertEqual(h['person_id'],self.x['entry_person_id']);self.assertNotEqual(h['person_id'],self.x['namespace_id'])
 def test_legacy_index_unchanged(self):
  rows=[dict(person_id='abc_def_123',label='原根'),dict(person_id='abc_def_123_A',label='子')];self.assertEqual(namespace_index_root('abc_def_123',rows),rows[0])
if __name__=='__main__':unittest.main(verbosity=2)
