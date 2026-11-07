"""Bounded source/guard tests. Fixture is a finite physical source composition,
not a normal-catalogue or complete API/native validation result.
"""
import copy,importlib.util,json,os,pathlib,shutil,tempfile,unittest
HERE=pathlib.Path(__file__).resolve()
ROOT=HERE.parents[1]
MODULE=pathlib.Path(os.environ.get('CBR_JIN059_HELPER',str(ROOT/'scripts/jin059_wei_ying_children.py')))
spec=importlib.util.spec_from_file_location('jin059_bounded_owner',MODULE);owner=importlib.util.module_from_spec(spec);spec.loader.exec_module(owner)
FIXTURE=pathlib.Path(os.environ.get('CBR_JIN059_BOUNDED_FIXTURE',str(ROOT)))
class Jin059FiniteSourceTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=pathlib.Path(self.tmp.name)/'source';self.root.mkdir()
  c=json.loads((FIXTURE/owner.REF).read_text());paths=set(owner.OWNED)|{owner.REF,'registry/persons.json',c['raw_path']}|set(c['expected_documents'])|set(c['expected_reference_documents'])|{s['chapter_path']for s in c['role_seeds'].values()}|{s['path']for s in c['paternal_chain']}
  for rel in paths:
   src=FIXTURE/rel;dst=self.root/rel;self.assertFalse(src.is_symlink());dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
  self.contract=self.read(owner.REF);self.cpath=self.contract['chapter_path'];self.c=self.read(self.cpath);self.pid=self.c['paragraphs'][0]['mentions'][0]['person_id']
 def tearDown(self):self.tmp.cleanup()
 def read(self,path):return json.loads((self.root/path).read_text())
 def write(self,path,obj):(self.root/path).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
 def people(self):return{p['id']:p for p in self.read('registry/persons.json')['persons']}
 def records(self):return[self.read(p)for p in self.contract['expected_documents']]
 def guard(self,pid=None,people=None,records=None):return owner.guard_bundle(self.root,pid or self.pid,self.people()if people is None else people,self.records()if records is None else records)
 def test_complete_source_and_all_three_fathers(self):
  c,roles,e=owner.proof(self.root);self.assertEqual(len(c['role_current_mids']),20);self.assertEqual(sum(map(len,c['role_current_mids'].values())),47);self.guard()
  aa=next(d['assertions']for d in e.values()if d.get('record_type')=='person_assertion_set');self.assertEqual(len(aa),3)
  for a in aa:self.assertTrue(owner.family_valid(a,self.root))
 def test_literal_and_paternal_surnames(self):
  _,_,e=owner.proof(self.root);names=next(d['records']for d in e.values()if d.get('record_type')=='person_name_component_set');aa=next(d['assertions']for d in e.values()if d.get('record_type')=='person_assertion_set');chs={self.c['id']:self.c}
  for n in names:owner.validate_surname(n,names,chs,aa,self.root)
 def test_wrong_father_rejected(self):
  path=next(p for p,d in self.contract['expected_documents'].items()if d.get('record_type')=='person_assertion_set');d=self.read(path);d['assertions'][0]['object_person_id']=d['assertions'][0]['subject_person_id'];self.write(path,d)
  with self.assertRaises(ValueError):self.guard()
 def test_physical_metadata_addition_is_accepted(self):
  r=self.read('registry/persons.json');r['persons'][0]['future_unknown_metadata']={'verified':False,'notes':['independent addition']};self.write('registry/persons.json',r);self.guard();owner.proof(self.root)
 def test_caller_unknown_metadata_mutation_rejected(self):
  p=self.people();p[self.pid]['unexpected_unknown_field']=True
  with self.assertRaises(ValueError):self.guard(people=p)
 def test_caller_bool_integer_unknown_change_rejected(self):
  r=self.read('registry/persons.json');row=next(p for p in r['persons']if p['id']==self.pid);row['extension_value']=False;self.write('registry/persons.json',r);p=self.people();p[self.pid]['extension_value']=0
  with self.assertRaises(ValueError):self.guard(people=p)
 def test_caller_sidecar_missing_rejected(self):
  with self.assertRaises(ValueError):self.guard(records=self.records()[:1])
 def test_caller_endpoint_theft_rejected(self):
  rec=self.records();ch=next(d for d in rec if d.get('record_type')=='marked_chapter');ch['paragraphs'][0]['mentions'][0]['person_id']='foreign_caller_person'
  with self.assertRaises(ValueError):self.guard(pid='foreign_caller_person',records=rec)
 def test_caller_reverse_only_theft_activates_guard(self):
  p=self.people();e=copy.deepcopy(next(e for e in p[self.pid]['evidence']if e['mention_id'].startswith(owner.CID+':')));p['foreign_reverse_only']={'id':'foreign_reverse_only','evidence':[e],'aliases':[]}
  with self.assertRaises(ValueError):self.guard(pid='foreign_reverse_only',people=p)
 def test_physical_reverse_only_theft_rejected(self):
  r=self.read('registry/persons.json');e=copy.deepcopy(next(e for e in self.people()[self.pid]['evidence']if e['mention_id'].startswith(owner.CID+':')));r['persons'].append({'id':'foreign_reverse_only','evidence':[e],'aliases':[]});self.write('registry/persons.json',r)
  with self.assertRaises(ValueError):self.guard(pid='foreign_reverse_only')
 def test_physical_alias_only_theft_rejected(self):
  r=self.read('registry/persons.json');mid=self.c['paragraphs'][0]['mentions'][0]['id'];r['persons'].append({'id':'foreign_alias_only','evidence':[],'aliases':[{'surface':'瑋','mention_ids':[mid]}]});self.write('registry/persons.json',r)
  with self.assertRaises(ValueError):self.guard()
 def test_caller_alias_only_theft_activates_guard(self):
  p=self.people();mid=self.c['paragraphs'][0]['mentions'][0]['id'];p['foreign_alias_only']={'id':'foreign_alias_only','evidence':[],'aliases':[{'surface':'瑋','mention_ids':[mid]}]}
  with self.assertRaises(ValueError):self.guard(pid='foreign_alias_only',people=p)
 def test_physical_alias_missing_rejected(self):
  r=self.read('registry/persons.json');row=next(p for p in r['persons']if p['id']==self.pid);row['aliases']=[a for a in row['aliases']if not any(mid.startswith(owner.CID+':')for mid in a['mention_ids'])];self.write('registry/persons.json',r)
  with self.assertRaises(ValueError):self.guard()
 def test_physical_single_reverse_missing_rejected(self):
  r=self.read('registry/persons.json');row=next(p for p in r['persons']if p['id']==self.pid);target=next(e['mention_id']for e in row['evidence']if e['mention_id'].startswith(owner.CID+':'));row['evidence']=[e for e in row['evidence']if e['mention_id']!=target];self.write('registry/persons.json',r)
  with self.assertRaises(ValueError):self.guard()
 def test_seed_wrong_source_or_person_rejected(self):
  s=self.contract['role_seeds']['liutao'];d=self.read(s['chapter_path']);p,m=owner._mark(d,s['paragraph_id'],s['marker']['id']);m['person_id']=self.pid;self.write(s['chapter_path'],d)
  with self.assertRaises(ValueError):self.guard()
 def test_raw_capture_change_rejected(self):
  p=self.root/self.contract['raw_path'];p.write_bytes(p.read_bytes()+b'\n')
  with self.assertRaises(ValueError):self.guard()
 def test_contract_missing_rejects_physical_and_caller_owner(self):
  (self.root/owner.REF).unlink()
  with self.assertRaises(ValueError):self.guard()
 def test_projection_offset_bool_rejected(self):
  path=self.contract['units_path'];d=self.read(path);d['units'][0]['raw_character_offsets'][0]=True;self.write(path,d)
  with self.assertRaises(ValueError):self.guard()
 def test_ancestor_coherent_rekey_including_typed_parent_qualifier(self):
  _,roles,_=owner.proof(self.root);old=roles['ancestor_zhao'];new='bounded_ancestor_rekey'
  def project(x,key=None,registry=False):
   if type(x)is dict:
    if registry and x.get('id')==old:x['id']=new
    for k,v in list(x.items()):
     if k in owner.TYPED and v==old:x[k]=new
     else:project(v,k,registry)
   elif type(x)is list:
    for v in x:project(v,key,registry)
  for p in self.root.rglob('*.json'):
   rel=str(p.relative_to(self.root))
   if rel in(owner.REF,self.contract['units_path']):continue
   d=json.loads(p.read_text());project(d,registry=rel=='registry/persons.json');p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
  _,after,_=owner.proof(self.root);self.assertEqual(after['ancestor_zhao'],new);self.guard()
 def test_contract_checksum_rejected_before_foreign_path_read(self):
  c=self.read(owner.REF);c['expected_documents']={'must_not_be_read.json':{}};self.write(owner.REF,c)
  with self.assertRaisesRegex(ValueError,'contract checksum mismatch'):self.guard()
 def test_non_json_contract_rejected_by_checksum_first(self):
  (self.root/owner.REF).write_bytes(b'\xffnot-json')
  with self.assertRaisesRegex(ValueError,'contract checksum mismatch'):self.guard()
 def test_full_qualified_liutao_confluence_is_allowed(self):
  _,roles,_=owner.proof(self.root);preferred=roles['liutao'];other=roles['liutao_yangzhou_candidate'];self.assertNotEqual(preferred,other)
  def rewrite(x,key=None):
   if type(x)is dict:
    for k,v in list(x.items()):
     if k in owner.TYPED and v==other:x[k]=preferred
     else:rewrite(v,k)
   elif type(x)is list:
    for v in x:rewrite(v,key)
  for p in self.root.rglob('*.json'):
   rel=str(p.relative_to(self.root))
   if rel in(owner.REF,self.contract['units_path'],'registry/persons.json'):continue
   d=json.loads(p.read_text());rewrite(d);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
  r=self.read('registry/persons.json');target=next(p for p in r['persons']if p['id']==preferred);donor=next(p for p in r['persons']if p['id']==other)
  target['bounded_prior_candidate_metadata']={k:copy.deepcopy(v)for k,v in donor.items()if k not in('id','aliases','evidence')}
  target['evidence'].extend(copy.deepcopy(e)for e in donor['evidence']if e not in target['evidence'])
  for a in donor['aliases']:
   hit=next((x for x in target['aliases']if x['surface']==a['surface']),None)
   if hit is None:target['aliases'].append(copy.deepcopy(a))
   else:hit['mention_ids'].extend(mid for mid in a['mention_ids']if mid not in hit['mention_ids'])
  r['persons']=[p for p in r['persons']if p['id']!=other];self.write('registry/persons.json',r)
  _,after,_=owner.proof(self.root);self.assertEqual(after['liutao'],after['liutao_yangzhou_candidate']);self.guard(pid=preferred)
  self.assertEqual(self.people()[preferred]['bounded_prior_candidate_metadata'],{k:v for k,v in donor.items()if k not in('id','aliases','evidence')})
 def test_one_qualified_liutao_endpoint_change_rejected(self):
  _,roles,_=owner.proof(self.root);s=self.contract['role_seeds']['liutao_yangzhou_candidate'];d=self.read(s['chapter_path']);_,m=owner._mark(d,s['paragraph_id'],s['marker']['id']);m['person_id']=roles['liutao'];self.write(s['chapter_path'],d)
  with self.assertRaises(ValueError):self.guard(pid=roles['liutao'])
 def test_unrelated_fan_pu_confluence_still_rejected(self):
  _,roles,_=owner.proof(self.root);old=roles['pu'];new=roles['fan']
  def rewrite(x):
   if type(x)is dict:
    for k,v in list(x.items()):
     if k in owner.TYPED and v==old:x[k]=new
     else:rewrite(v)
   elif type(x)is list:
    for v in x:rewrite(v)
  for p in self.root.rglob('*.json'):
   rel=str(p.relative_to(self.root))
   if rel in(owner.REF,self.contract['units_path']):continue
   d=json.loads(p.read_text());rewrite(d);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
  with self.assertRaises(ValueError):self.guard(pid=new)
 def test_valid_coherent_rekey_preserves_capture_and_opaque_ids(self):
  old=self.pid;new='bounded_coherent_rekey_person';oldcontract=(self.root/owner.REF).read_bytes();raw=(self.root/self.contract['raw_path']).read_bytes();units=(self.root/self.contract['units_path']).read_bytes();opaque=[]
  def rewrite(x,key=None,registry=False):
   if type(x)is dict:
    if registry and x.get('id')==old:x['id']=new
    for k,v in list(x.items()):
     if k in owner.TYPED and v==old:x[k]=new
     else:rewrite(v,k,registry)
   elif type(x)is list:
    for v in x:rewrite(v,key,registry)
  for p in self.root.rglob('*.json'):
   rel=str(p.relative_to(self.root))
   if rel in(owner.REF,self.contract['units_path']):continue
   d=json.loads(p.read_text());rewrite(d,registry=rel=='registry/persons.json');p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
  # Normal XML output endpoints are rewritten only at explicit ref attributes.
  for p in self.root.rglob('*.xml'):
   b=p.read_bytes();p.write_bytes(b.replace(('ref="'+old+'"').encode(),('ref="'+new+'"').encode()))
   self.assertNotIn(('ref="'+old+'"').encode(),p.read_bytes())
  self.assertEqual((self.root/owner.REF).read_bytes(),oldcontract);self.assertEqual((self.root/self.contract['raw_path']).read_bytes(),raw);self.assertEqual((self.root/self.contract['units_path']).read_bytes(),units)
  _,roles,_=owner.proof(self.root);self.assertEqual(roles['wei'],new);self.guard(pid=new)
  p=self.people();target=next(e['mention_id']for e in p[new]['evidence']if e['mention_id'].startswith(owner.CID+':'));p[new]['evidence']=[e for e in p[new]['evidence']if e['mention_id']!=target]
  with self.assertRaises(ValueError):self.guard(pid=new,people=p)
 def test_claimant_parser_same_bytes_only_once_and_immutable(self):
  from unittest.mock import patch
  owner._physical_claimants.cache_clear();b=(self.root/'registry/persons.json').read_bytes();loads=owner.json.loads
  with patch.object(owner.json,'loads',wraps=loads)as counted:
   one=owner._physical_claimants(b);two=owner._physical_claimants(bytes(bytearray(b)));self.assertEqual(counted.call_count,1)
  self.assertIs(type(one),frozenset);self.assertEqual(one,two);self.assertEqual(owner._physical_claimants.cache_info().hits,1)
 def test_same_size_physical_claim_change_uses_new_bytes(self):
  owner._physical_claimants.cache_clear();mid=self.c['paragraphs'][0]['mentions'][0]['id'];other='x'+mid[1:]
  a=json.dumps({'persons':[{'id':'thief','evidence':[{'mention_id':other}],'aliases':[]}]}).encode();b=a.replace(other.encode(),mid.encode());self.assertEqual(len(a),len(b));self.assertNotIn('thief',owner._physical_claimants(a));self.assertIn('thief',owner._physical_claimants(b));self.assertEqual(owner._physical_claimants.cache_info().misses,2)
 def test_warm_physical_thief_with_caller_source_claim_stripped(self):
  from scripts.validation_context import scope
  owner._physical_claimants.cache_clear();caller=self.people();outside='bounded_physical_only_thief';caller[outside]={'id':outside,'aliases':[],'evidence':[]}
  with scope(self.root):
   self.guard(pid=outside,people=caller)
   r=self.read('registry/persons.json');e=copy.deepcopy(next(e for e in caller[self.pid]['evidence']if e['mention_id'].startswith(owner.CID+':')));r['persons'].append({'id':outside,'aliases':[],'evidence':[e]});self.write('registry/persons.json',r)
   with self.assertRaises(ValueError):self.guard(pid=outside,people=caller)
 def test_warm_physical_alias_thief_omitted_from_caller(self):
  owner._physical_claimants.cache_clear();caller=self.people();outside='bounded_alias_physical_only';self.guard(pid=outside,people=caller);r=self.read('registry/persons.json');mid=self.c['paragraphs'][0]['mentions'][0]['id'];r['persons'].append({'id':outside,'aliases':[{'surface':'瑋','mention_ids':[mid]}],'evidence':[]});self.write('registry/persons.json',r)
  with self.assertRaises(ValueError):self.guard(pid=outside,people=caller)
 def test_warm_cache_does_not_hide_reader_overlay(self):
  from unittest.mock import patch
  owner._physical_claimants.cache_clear();caller=self.people();outside='bounded_reader_only_thief';self.guard(pid=outside,people=caller);r=self.read('registry/persons.json');mid=self.c['paragraphs'][0]['mentions'][0]['id'];r['persons'].append({'id':outside,'aliases':[{'surface':'瑋','mention_ids':[mid]}],'evidence':[]});changed=json.dumps(r).encode();original=pathlib.Path.read_bytes;registry=(self.root/'registry/persons.json').resolve()
  def reader(path):return changed if path==registry else original(path)
  with patch.object(pathlib.Path,'read_bytes',reader):
   with self.assertRaises(ValueError):self.guard(pid=outside,people=caller)
 def test_warm_cache_does_not_hide_missing_registry(self):
  owner._physical_claimants.cache_clear();caller=self.people();self.guard(pid='bounded_unrelated',people=caller);(self.root/'registry/persons.json').unlink()
  with self.assertRaises(FileNotFoundError):self.guard(pid='bounded_unrelated',people=caller)
 def test_requested_claim_predicate_matches_original_membership(self):
  p=self.people();p['reverse_only']={'evidence':[{'mention_id':owner.CID+':x'}]};p['alias_only']={'aliases':[{'mention_ids':[owner.CID+':x']}]};p['empty']={}
  expected=owner._claiming(p)
  for pid in list(p)+['absent']:self.assertEqual(owner._caller_claims(p,pid),pid in expected)
if __name__=='__main__':unittest.main()
