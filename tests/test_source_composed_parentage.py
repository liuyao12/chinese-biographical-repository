import unittest,json,copy,ast,contextlib,importlib
from pathlib import Path
from unittest.mock import patch
from scripts import validate_corpus as native
from scripts import jin064_wudi_family_sources as owner
from scripts.source_composed_parentage import valid as composed_valid
ROOT=Path(__file__).resolve().parents[1]
def native_assertion_prefix(source,record,root,people,assertions):
 """Execute the actual production assertion loop prefix through its status branch."""
 tree=ast.parse(source);loops=[n for n in ast.walk(tree)if isinstance(n,ast.For)and isinstance(n.target,ast.Name)and n.target.id=='a'and ast.unparse(n.iter)=="d['assertions']"and any(isinstance(x,ast.Expr)and isinstance(x.value,ast.Call)and any(isinstance(v,ast.Constant)and v.value=='人物陳述未有來源證據'for v in x.value.args)for x in n.body)]
 assert len(loops)==1;loop=copy.deepcopy(loops[0]);status=next(i for i,x in enumerate(loop.body)if isinstance(x,ast.Expr)and isinstance(x.value,ast.Call)and any(isinstance(v,ast.Constant)and v.value=='人物陳述未有來源證據'for v in x.value.args));stop=status+1
 # Parent code placed the finite received branch after the generic check.
 for i in range(status+1,min(len(loop.body),status+4)):
  x=loop.body[i]
  if isinstance(x,ast.If)and'received_sima_family_roles'in ast.unparse(x.test):stop=i+1
 loop.body=loop.body[:stop];code=ast.fix_missing_locations(ast.Module(body=[loop],type_ignores=[]));errors=[]
 def check(ok,message):
  if not ok:errors.append(message)
 scope=dict(vars(native),d={'assertions':[record]},root=root,family_relations=assertions,pids=set(people),aids=set(),check=check,errors=errors)
 exec(compile(code,'actual-native-assertion-prefix','exec'),scope);return errors
class ZhoufeiDerivedParent(unittest.TestCase):
 def fixture(self):
  raw=lambda p:(ROOT/p).read_bytes();return ROOT,raw,{p['id']:p for p in json.loads(raw('registry/persons.json'))['persons']}
 def setup(self):
  root,raw,people=self.fixture();c,r,docs=owner._proof(raw,people);path=next(p for p,d in docs.items()if d.get('record_type')=='person_assertion_set');aa=docs[path]['assertions'];a=next(a for a in aa if a['id']=='a-jin064-zhou-father-hui');return root,raw,people,c,r,docs,path,aa,a
 @contextlib.contextmanager
 def readers(self,raw):
  with contextlib.ExitStack()as stack:
   for name in('received_sima_family_sources','jin064_wudi_family_sources','scripts.received_sima_family_sources','scripts.jin064_wudi_family_sources'):
    try:mod=importlib.import_module(name)
    except ImportError:continue
    stack.enter_context(patch.object(mod,'_raw',lambda root,path:raw(path)))
   yield
 def prefix(self,a,aa,raw,root,people):
  with self.readers(raw):return native_assertion_prefix(Path(native.__file__).read_text(),a,root,people,aa)
 def test_01_actual_native_status_branch_accepts_qualified_derived(self):
  root,raw,people,c,r,docs,path,aa,a=self.setup();self.assertEqual(a['status'],'contextual_provisional');self.assertTrue(composed_valid(a,aa));self.assertEqual(self.prefix(a,aa,raw,root,people),[])
 def test_02_input_ids_and_same_child_same_mother_maternal_layer_are_typed(self):
  _,_,_,_,r,_,_,aa,a=self.setup();b=a['qualifiers']['source_composed_parent_bridge'];self.assertEqual(b['mother_assertion_id'],'a-jin064-qin-mother-zhou');self.assertEqual(b['maternal_grandfather_assertion_id'],'a-jin064-qin-maternal-grandfather-hui');self.assertTrue(b['same_child']);self.assertTrue(b['same_mother']);self.assertEqual(b['lineage'],'maternal');self.assertFalse(b['literal_father_sentence']);self.assertEqual(b['mother_person_id'],r['m_zhoufei']);self.assertEqual(b['maternal_grandfather_person_id'],r['zhouhui'])
 def reject_input(self,key,field,value_role):
  root,raw,people,c,r,docs,path,aa,a=self.setup();changed=copy.deepcopy(aa);b=a['qualifiers']['source_composed_parent_bridge'];row=next(x for x in changed if x['id']==b[key]);row[field]=r[value_role];self.assertFalse(composed_valid(a,changed));self.assertTrue(self.prefix(a,changed,raw,root,people))
 def test_03_caller_mother_endpoint_cannot_change(self):self.reject_input('mother_assertion_id','object_person_id','m_chenmeiren')
 def test_04_caller_grandfather_endpoint_cannot_change(self):self.reject_input('maternal_grandfather_assertion_id','object_person_id','wu')
 def test_05_caller_child_cannot_change(self):self.reject_input('mother_assertion_id','subject_person_id','yue')
 def test_06_paternal_grandfather_cannot_replace_maternal(self):
  root,raw,people,c,r,docs,path,aa,a=self.setup();changed=copy.deepcopy(aa);g=next(x for x in changed if x['id']==a['qualifiers']['source_composed_parent_bridge']['maternal_grandfather_assertion_id']);g['qualifiers']['lineage']='paternal';self.assertFalse(composed_valid(a,changed));self.assertTrue(self.prefix(a,changed,raw,root,people))
 def test_07_other_mother_link_and_adoptive_mother_rejected(self):
  root,raw,people,c,r,docs,path,aa,a=self.setup()
  for pred in('adoptive_mother','maternal_role'):
   changed=copy.deepcopy(aa);m=next(x for x in changed if x['id']==a['qualifiers']['source_composed_parent_bridge']['mother_assertion_id']);m['predicate']=pred;self.assertTrue(self.prefix(a,changed,raw,root,people))
 def test_08_forged_literal_or_source_attested_status_rejected_by_native(self):
  root,raw,people,c,r,docs,path,aa,a=self.setup()
  for mutate in(lambda x:x.update(status='source_attested'),lambda x:x['qualifiers']['source_composed_parent_bridge'].update(literal_father_sentence=True),lambda x:x['qualifiers']['source_composed_parent_bridge'].update(derived=False)):
   bad=copy.deepcopy(a);mutate(bad);self.assertFalse(composed_valid(bad,aa));self.assertTrue(self.prefix(bad,aa,raw,root,people))
 def test_09_duplicate_or_missing_input_claim_rejected(self):
  root,raw,people,c,r,docs,path,aa,a=self.setup();mid=a['qualifiers']['source_composed_parent_bridge']['mother_assertion_id'];mother=next(x for x in aa if x['id']==mid)
  for changed in([x for x in aa if x['id']!=mid],aa+[copy.deepcopy(mother)]):self.assertTrue(self.prefix(a,changed,raw,root,people))
 def test_10_unrelated_generic_status_requirement_is_unchanged(self):
  root,raw,people,c,r,docs,path,aa,a=self.setup();generic=copy.deepcopy(a);generic['qualifiers']={};generic['status']='contextual_provisional';self.assertIn('人物陳述未有來源證據',self.prefix(generic,aa,raw,root,people));generic['status']='source_attested';generic['evidence']=[];self.assertIn('人物陳述未有來源證據',self.prefix(generic,aa,raw,root,people))
 def test_11_provisional_identity_and_boolean_types_not_erasable(self):
  root,raw,people,c,r,docs,path,aa,a=self.setup()
  for change in(lambda x:x['qualifiers'].update(identity_status='source_attested'),lambda x:x['qualifiers']['source_composed_parent_bridge'].update(same_child=1),lambda x:x.update(human_reviewed=0)):
   bad=copy.deepcopy(a);change(bad);self.assertTrue(self.prefix(bad,aa,raw,root,people))
 def test_12_input_raw_evidence_cannot_belong_to_other_unit(self):
  root,raw,people,c,r,docs,path,aa,a=self.setup();changed=copy.deepcopy(aa);next(x for x in changed if x['id']==a['qualifiers']['source_composed_parent_bridge']['mother_assertion_id'])['evidence'][0]['paragraph_id']='other';self.assertTrue(self.prefix(a,changed,raw,root,people))
 def test_13_legitimate_coherent_mother_rekey_keeps_opaque_source_ids(self):
  root,raw,people,c,r,docs,path,aa,a=self.setup();old=r['m_zhoufei'];new='q3q_q3q_q3q';self.assertNotIn(new,people)
  def move(x):
   if isinstance(x,dict):return{k:move(v)for k,v in x.items()}
   if isinstance(x,list):return[move(v)for v in x]
   return new if x==old else x
  p=copy.deepcopy(people);p[new]=move(p.pop(old));p[new]['id']=new;changedaa=move(aa);changeda=next(x for x in changedaa if x['id']==a['id'])
  def newraw(rel):
   if rel=='registry/persons.json':return json.dumps({'persons':list(p.values())},ensure_ascii=False).encode()
   if rel in c['expected_documents']:return json.dumps(move(json.loads(raw(rel))),ensure_ascii=False).encode()
   return raw(rel)
  self.assertEqual(self.prefix(changeda,changedaa,newraw,root,p),[]);self.assertEqual([x['id']for x in aa],[x['id']for x in changedaa]);self.assertEqual(raw(c['capture_path']),newraw(c['capture_path']))
 def test_14_typed_generation_and_evidence_shape_are_not_coerced(self):
  root,raw,people,c,r,docs,path,aa,a=self.setup()
  for mutate in(lambda g:g['qualifiers'].update(generation_difference=-2.0),lambda g:g.update(evidence=tuple(g['evidence']))):
   changed=copy.deepcopy(aa);g=next(x for x in changed if x['id']==a['qualifiers']['source_composed_parent_bridge']['maternal_grandfather_assertion_id']);mutate(g);self.assertFalse(composed_valid(a,changed));self.assertTrue(self.prefix(a,changed,raw,root,people))
if __name__=='__main__':unittest.main()
