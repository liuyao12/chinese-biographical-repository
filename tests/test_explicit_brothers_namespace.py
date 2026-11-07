import copy,json,unittest
from pathlib import Path
from unittest.mock import patch
from scripts.person_bundle import load_catalog
from scripts.personless_namespace import namespace_members,namespace_index_root
from scripts import wyd_song045_roles as m
ROOT=Path(__file__).resolve().parents[1]
class ExplicitBrothersNamespace(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.people,records=load_catalog(ROOT);cls.assertions={a['id']:a for r in records if r.get('record_type')=='person_assertion_set'for a in r['assertions']};cls.chapters={r['id']:r for r in records if r.get('record_type')=='marked_chapter'};cls.assembly=next(a for a in json.loads((ROOT/'registry/family-assemblies.json').read_bytes())['assemblies']if a['id']=='family-song045-cheng-brothers')
 def reject(self,assembly=None,people=None,assertions=None,chapters=None):
  with self.assertRaises(ValueError):namespace_members(assembly or self.assembly,people or self.people,self.assertions if assertions is None else assertions,chapters or self.chapters,root=ROOT)
 def test_two_real_brothers_without_parent_profile(self):
  out=namespace_members(self.assembly,self.people,self.assertions,self.chapters,root=ROOT);self.assertEqual(len(out),2);self.assertNotIn(self.assembly['namespace_id'],self.people);self.assertTrue(all(x['parent_person_id']is None and x['root_person_id']is None for x in out.values()))
 def test_parent_name_id_or_root_cannot_be_fabricated(self):
  for key,value in [('common_parent_name','某'),('common_parent_person_id',self.assembly['entry_person_id']),('common_parent_registered',True)]:
   a=copy.deepcopy(self.assembly);a['collateral_root_group'][key]=value;self.reject(a)
  a=copy.deepcopy(self.assembly);a['root_person_id']=a['entry_person_id'];self.reject(a)
 def test_reverse_and_impostor_endpoints_reject(self):
  aid=self.assembly['collateral_root_group']['brother_assertion_id']
  for mode in ['reverse','impostor']:
   aa=copy.deepcopy(self.assertions);a=aa[aid]
   if mode=='reverse':a['subject_person_id'],a['object_person_id']=a['object_person_id'],a['subject_person_id']
   else:a['object_person_id']=m.resolve_roles(self.chapters[m.CID],ROOT)['real_feilong']
   self.reject(assertions=aa)
 def test_missing_proof_wrong_term_and_relative_order_reject(self):
  aa=copy.deepcopy(self.assertions);del aa[self.assembly['collateral_root_group']['brother_assertion_id']];self.reject(assertions=aa)
  for key,value in [('source_term','從弟'),('relative_age','unknown'),('name_record_ids',[])]:
   a=copy.deepcopy(self.assembly);a['collateral_root_group'][key]=value;self.reject(a)
 def test_wrong_layer_and_nested_annotation_reject(self):
  for target,key,value in [('p','text_layer','witness_appended_pei_songzhi_note'),('p','annotator','裴松之'),('position','text_layer','witness_appended_pei_songzhi_note'),('position','attached_note_to_paragraph_id','other')]:
   cc=copy.deepcopy(self.chapters);p=next(p for p in cc[m.CID]['paragraphs']if p['id'].endswith('p008'));(p if target=='p'else p['source_position'])[key]=value;self.reject(chapters=cc)
 def test_other_generation_or_parent_edge_reject(self):
  for mode in ['generation','parent']:
   a=copy.deepcopy(self.assembly)
   if mode=='generation':a['members'][1]['person_id']+='A'
   else:a['members'][1]['parent_person_id']=a['members'][0]['person_id']
   self.reject(a)
 def test_quote_co_shift_and_short_ref_reject(self):
  a=copy.deepcopy(self.assembly);a['collateral_root_group']['references'][0]['quote']='道養弟道助';self.reject(a)
  cc=copy.deepcopy(self.chapters);p=next(p for p in cc[m.CID]['paragraphs']if p['id'].endswith('p008'));p['text']='甲'+p['text']
  for mark in p['mentions']:mark['start']+=1;mark['end']+=1
  self.reject(chapters=cc)
 def test_consistent_branch_rekey_not_letter_whitelist(self):
  ns=self.assembly['namespace_id'];mapping={self.assembly['collateral_root_group']['root_person_ids'][0]:ns+'_C',self.assembly['collateral_root_group']['root_person_ids'][1]:ns+'_D'}
  def remap(x):
   if isinstance(x,dict):return {k:remap(v)for k,v in x.items()}
   if isinstance(x,list):return [remap(v)for v in x]
   if isinstance(x,str):
    for old,new in mapping.items():x=x.replace(old,new)
   return x
  original=Path.read_bytes
  def read(p):
   b=original(p)
   if p.suffix=='.json'and(p.is_relative_to(ROOT/'corpus')or p.is_relative_to(ROOT/'registry')):return json.dumps(remap(json.loads(b)),ensure_ascii=False).encode()
   return b
  with patch.object(Path,'read_bytes',read):
   pp={mapping.get(k,k):remap(v)for k,v in self.people.items()};out=namespace_members(remap(self.assembly),pp,remap(self.assertions),remap(self.chapters),root=ROOT);self.assertEqual(set(out),set(mapping.values()))
 def test_index_label_distinguishes_explicit_brothers(self):
  rows=namespace_members(self.assembly,self.people,self.assertions,self.chapters,root=ROOT);items=[{'person_id':pid,'label':'程氏真人','assembled_identity':row}for pid,row in rows.items()];label=namespace_index_root(self.assembly['namespace_id'],items)['label'];self.assertIn('弟兄（原文明記；父未名）',label);self.assertNotIn('兩支',label)
 def test_new_type_cannot_enter_old_cousin_mode(self):
  a=copy.deepcopy(self.assembly);a['collateral_root_group']['type']='unknown_shared_father_from_qualified_first_cousins';self.reject(a)
if __name__=='__main__':unittest.main()
