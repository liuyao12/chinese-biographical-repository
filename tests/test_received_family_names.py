import json,copy,unittest,sys,tempfile,shutil,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R))
from scripts.received_family_names import validate,source_component_valid,clan_valid
from scripts.person_bundle import load_catalog,bundle,validate_clan_style
C=json.loads((R/'corpus/sanguozhi/026-guohuai.json').read_text());CH={C['id']:C};A=json.loads((R/'corpus/sanguozhi/026-guohuai-assertions.json').read_text())['assertions'];N=json.loads((R/'corpus/sanguozhi/026-guohuai-name-components.json').read_text())['records'];G=json.loads((R/'corpus/jinshu/043-wangyan-wife-name-components.json').read_text())['records'][0]
def name(ming):return copy.deepcopy(next(n for n in N if n['ming']==ming))
def valid(n,aa=A,names=N):
 try:validate(n,names,CH,aa,R);return True
 except ValueError:return False
class ReceivedFamilyNames(unittest.TestCase):
 def test_all_twelve_received_and_thirteen_including_exact_clan(self):
  self.assertEqual(len(N)+1,13)
  for n in N:
   self.assertTrue(source_component_valid(n,C,R),n['id'])
   if'surname_basis'in n:self.assertTrue(valid(n),n['id'])
  self.assertIsNone(G['ming']);self.assertEqual(G['surname'],'郭')
 def test_courtesy_names_bind_their_own_adjacent_subject(self):
  self.assertEqual({n['ming']:n.get('zi')for n in N if n['ming']in('淮','配','展','豫','鎮','奕')},{'淮':'伯濟','配':'仲南','展':'泰舒','豫':'泰寧','鎮':'季南','奕':'泰業'})
  x=name('配');x['zi']='泰舒';p=next(p for p in C['paragraphs']if p['id']==x['paragraph_id']);start=p['text'].index('字泰舒')+1;x['component_source_binding']['courtesy_anchor']=dict(paragraph_id=p['id'],start=start,end=start+2,surface='泰舒');self.assertFalse(source_component_valid(x,C,R))
 def test_zi_is_source_scoped_not_global_preferred(self):
  x=name('奕');self.assertEqual(x['zi'],'泰業');self.assertNotIn('preferred',x);self.assertIn('未設global preferred',x['note'])
 def test_grandfather_remains_grandfather(self):
  x=name('全');self.assertEqual(x['surname_basis']['steps'][0]['traversal'],'child_to_grandfather');self.assertEqual(x['surname_basis']['steps'][0]['generation_after'],-2);x['surname_basis']['steps'][0]['traversal']='child_to_father';self.assertFalse(valid(x))
 def test_younger_brother_path_does_not_invent_father(self):
  x=name('豫');steps=x['surname_basis']['steps'];self.assertEqual(steps[-1]['traversal'],'older_to_younger');self.assertEqual([s['generation_after']for s in steps],[0,1,1]);self.assertFalse(any(a['predicate']=='father'and a['subject_person_id']==x['person_id']for a in A))
 def test_source_sister_clan_only_no_marital_surname(self):
  x=copy.deepcopy(next(n for n in N if n.get('clan_style')));p=next(p for p in C['paragraphs']if p['id']==x['paragraph_id']);self.assertTrue(clan_valid(x,p,A));self.assertIsNone(x['ming']);self.assertEqual(x['surname'],'王');x['surname']='郭';self.assertFalse(valid(x));self.assertFalse(clan_valid(x,p,A))
 def test_clan_value_mismatch_is_rejected_at_native_surname_layer(self):
  x=copy.deepcopy(next(n for n in N if n.get('clan_style')));x['clan_style']['value']='郭氏';self.assertFalse(valid(x));self.assertFalse(source_component_valid(x,C,R))
 def test_no_woman_given_name_invented(self):
  x=copy.deepcopy(next(n for n in N if n.get('clan_style')));x['ming']='妹';self.assertFalse(valid(x));self.assertFalse(source_component_valid(x,C,R))
 def test_no_spouse_or_affine_surname_path(self):
  x=name('配');x['surname_basis']['steps'][0]['assertion_id']=next(a['id']for a in A if a['predicate']=='spouse');self.assertFalse(valid(x))
 def test_no_maternal_adoptive_sworn_or_denied_shared_father(self):
  x=name('配');id=x['surname_basis']['steps'][0]['assertion_id']
  for key,val in [('lineage','maternal'),('adoptive',True),('sworn',True),('same_mother_only',True),('shared_father',False)]:
   aa=copy.deepcopy(A);a=next(a for a in aa if a['id']==id);a['qualifiers'][key]=val;self.assertFalse(valid(x,aa),key)
 def test_no_unknown_common_father_or_assembly_edge(self):
  x=name('配');aa=copy.deepcopy(A);a=next(a for a in aa if a['id']==x['surname_basis']['steps'][0]['assertion_id']);a['predicate']='father';self.assertFalse(valid(x,aa))
 def test_no_cycle_repeat_or_wrong_generation(self):
  for mutation in ('repeat','cycle','generation'):
   x=name('奕');s=x['surname_basis']['steps']
   if mutation=='repeat':s[1]=copy.deepcopy(s[0])
   if mutation=='cycle':s[1]['to_person_id']=s[0]['from_person_id']
   if mutation=='generation':s[0]['generation_after']=1
   self.assertFalse(valid(x),mutation)
 def test_no_label_or_structural_id_inference(self):
  x=name('配');x['surname_basis']['steps']=[];self.assertFalse(valid(x));x=name('配');x['person_id']='郭配';self.assertFalse(source_component_valid(x,C,R));self.assertFalse(valid(x))
 def test_full_name_not_claimed_literal_for_short_source_name(self):
  x=name('緼');x['component_source_binding']['name_form']='full_name';self.assertFalse(source_component_valid(x,C,R));self.assertEqual(x['ming'],'緼')
 def test_synthetic_identity_ids_are_not_whitelist(self):
  cc=copy.deepcopy(C);nn=copy.deepcopy(N);aa=copy.deepcopy(A);old={m['person_id']for p in cc['paragraphs']for m in p['mentions']if m['kind']=='person'};mp={x:'synthetic'+str(i)for i,x in enumerate(sorted(old))}
  def remap(v):
   if isinstance(v,dict):return{k:remap(x)for k,x in v.items()}
   if isinstance(v,list):return[remap(x)for x in v]
   return mp.get(v,v)if isinstance(v,str)else v
  cc=remap(cc);nn=remap(nn);aa=remap(aa)
  for x in nn:
   if'surname_basis'in x:validate(x,nn,{cc['id']:cc},aa,R)
 def test_production_bundles_have_readable_components_without_label_mutation(self):
  cat=load_catalog(R)
  for n in N+[G]:
   b=bundle(n['person_id'],root=R,catalog=cat);self.assertTrue(any(x.get('id')==n['id']for x in b.get('name_components',[])),n['id'])
if __name__=='__main__':unittest.main()
