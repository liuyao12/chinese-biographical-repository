# coding: utf-8
import unittest,json,copy
from pathlib import Path
from scripts.person_bundle import load_catalog
from scripts.surname_received_family_units import validate,KIND
R=Path(__file__).resolve().parents[1]
class YangjinFamilyNames(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.people,cls.records=load_catalog(R);cls.chapters={r['id']:r for r in cls.records if r.get('record_type')=='marked_chapter'};cls.assertions=[a for r in cls.records if r.get('record_type')=='person_assertion_set'for a in r['assertions']];cls.names=[n for r in cls.records if r.get('record_type')=='person_name_component_set'for n in r['records']];cls.selected=[n for n in cls.names if n.get('surname_basis',{}).get('kind')==KIND];cls.by_ming={n['ming']:n['person_id']for n in cls.selected};cls.catalogue=json.loads((R/'registry/family-assemblies.json').read_text())['assemblies'];cls.main=next(f for f in cls.catalogue if f['id']=='family-hongnong-yang-jie-close');cls.jun=next(f for f in cls.catalogue if f['id']=='family-weishu058-yang-jun-close')
 def good(self,n):return validate(n,self.names,self.chapters,self.assertions,R)
 def bad(self,n,names=None,assertions=None,root=R):
  with self.assertRaisesRegex(ValueError,'Received-family surname'):validate(n,names or self.names,self.chapters,assertions or self.assertions,root)
 def test_all_thirteen_routes_read_actual_complete_units(self):
  self.assertEqual(len(self.selected),13)
  for n in self.selected:self.good(n);self.assertEqual(n['surname'],'楊');self.assertFalse(n['human_reviewed']);self.assertLessEqual(len(n['surname_basis']['steps']),5)
 def test_raw_root_is_required_at_real_call_boundary(self):self.bad(copy.deepcopy(self.selected[0]),root=None)
 def test_wrong_work_revision_raw_and_unit_path_rejected(self):
  for key,val in [('work_id','w-wrong'),('source_revision',1),('raw_file_sha256','0'*64),('native_path','../outside.json')]:
   n=copy.deepcopy(self.selected[0]);n['surname_basis']['source_units'][0][key]=val;self.bad(n)
 def test_derived_or_missing_fullname_seed_cannot_bootstrap_surname(self):
  n=copy.deepcopy(self.selected[0]);seedid=n['surname_basis']['source_name_record_id'];names=copy.deepcopy(self.names);seed=next(s for s in names if s.get('id')==seedid);seed['surname_basis']={'kind':'synthetic_inferred_seed'};self.bad(n,names=names)
  n['surname_basis']['source_name_record_id']='unknown';self.bad(n)
 def test_literal_brother_positions_roles_and_order_must_all_match(self):
  n=next(n for n in self.selected if n['ming']=='津')
  for mode in ('offset','reverse','generation','term','boolean_generation'):
   b=copy.deepcopy(n);s=b['surname_basis']['steps'][0]
   if mode=='offset':s['role_binding']['source_anchor']['start']+=1
   elif mode=='reverse':s['from_person_id'],s['to_person_id']=s['to_person_id'],s['from_person_id']
   elif mode=='generation':s['generation_after']=1
   elif mode=='boolean_generation':s['generation_before']=False
   else:s['role_binding']['source_anchor']['surface']='津弟椿'
   self.bad(b)
 def test_same_paragraph_wrong_person_consistent_record_is_rejected(self):
  n=copy.deepcopy(next(n for n in self.selected if n['ming']=='津'));s=n['surname_basis']['steps'][0];claims=copy.deepcopy(self.assertions);a=next(a for a in claims if a['id']==s['assertion_id']);other=self.by_ming['暐'];s['to_person_id']=other;a['subject_person_id']=other;n['person_id']=other
  self.bad(n,assertions=claims)
 def test_no_inferred_father_adoption_cousin_or_generation_jump(self):
  n=next(n for n in self.selected if n['ming']=='逸')
  for mode in ('assembly','adoptive','generation','cycle'):
   b=copy.deepcopy(n);claims=copy.deepcopy(self.assertions);s=b['surname_basis']['steps'][-1];a=next(a for a in claims if a['id']==s['assertion_id'])
   if mode=='assembly':s['traversal']='shared_father_through_sibling'
   elif mode=='adoptive':a['qualifiers']['adoptive']=True
   elif mode=='generation':s['generation_after']+=1
   else:s['to_person_id']=s['from_person_id']
   self.bad(b,assertions=claims)
 def test_ancestor_roles_not_maternal_or_implicit_father(self):
  n=next(n for n in self.selected if n['ming']=='暉');self.good(n)
  for mode in ('maternal','distance','companion','companion_status'):
   b=copy.deepcopy(n);claims=copy.deepcopy(self.assertions);s=b['surname_basis']['steps'][0];a=next(a for a in claims if a['id']==s['assertion_id'])
   if mode=='maternal':a['qualifiers']['lineage']='maternal'
   elif mode=='distance':s['generation_after']=-1
   elif mode=='companion_status':next(x for x in claims if x['id']==s['role_binding']['companion_assertion_id'])['status']='editorial_provisional'
   else:s['role_binding']['companion_assertion_id']=s['assertion_id']
   self.bad(b,assertions=claims)
 def test_source_frames_and_full_quotes_cannot_be_dropped(self):
  for mode in ('frame','quote','empty'):
   n=copy.deepcopy(self.selected[0]);b=n['surname_basis']
   if mode=='frame':b['steps'][0]['source_frames'][0]['paragraph_sha256']='0'*64
   elif mode=='quote':b['steps'][0]['evidence'][0]['quote']='fragment only'
   else:b['steps']=[]
   self.bad(n)
 def test_26_and_7_are_separate_and_old_main_19_are_retained(self):
  extensions=[m for m in self.main['members']if m.get('parent_connection',{}).get('interpretation_basis')=='epitaph_bound_titled_ancestor_sequence'];self.assertEqual(len(self.main['members'])-2*len(extensions),26);self.assertLessEqual(len(extensions),1);self.assertEqual(len(self.jun['members']),7);self.assertEqual(self.main['root_person_id'],'fum_370_iq6');self.assertEqual(self.jun['root_person_id'],self.by_ming['暉']);self.assertFalse({m['person_id']for m in self.main['members']}&{m['person_id']for m in self.jun['members']})
 def test_inferred_parent_edges_are_not_fabricated_source_fathers(self):
  rows={m['person_id']:m for m in self.main['members']+self.jun['members']};source=json.loads((R/'corpus/weishu-weishou/058-yangjin-assertions.json').read_text())['assertions']
  for ming in ('津','暐','謐','遵彥','恩','穆','儉','寬'):
   pid=self.by_ming[ming];self.assertIsNone(rows[pid]['source_assertion_id']);self.assertIsNotNone(rows[pid].get('parent_connection'));self.assertFalse(any(a['predicate']=='father'and a['subject_person_id']==pid for a in source))
 def test_longest_names_preserve_zi_and_former_name_not_labels(self):
  jin=next(n for n in self.selected if n['ming']=='津');self.assertEqual(jin['zi'],'羅漢');self.assertEqual(jin['former_ming'],'延祚');self.assertIn('本名延祚',jin['quote']);self.assertEqual({n['ming']for n in self.selected},{'津','遁','逸','謐','遵彥','暐','元讓','暉','恩','暄','穆','儉','寬'})
