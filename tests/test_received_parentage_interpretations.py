from pathlib import Path
import ast,copy,json,os,subprocess,sys,tempfile,unittest,shutil,hashlib
from scripts import received_parentage_interpretations as ri
from scripts.person_bundle import bundle,load_catalog
ROOT=Path(__file__).resolve().parents[1]
class ParentageInterpretations(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.chapter=json.loads((ROOT/'corpus/nanqishu/043-xieyue.json').read_text());cls.people={p['id']:p for p in json.loads((ROOT/'registry/persons.json').read_text())['persons']};cls.doc=json.loads((ROOT/'corpus/nanqishu/043-xieyue-relationship-interpretations.json').read_text());cls.assertions=json.loads((ROOT/'corpus/nanqishu/043-xieyue-assertions.json').read_text());cls.role=cls.doc['records'][0]['source_context']['role_mentions'];p=cls.chapter['paragraphs'][0];cls.ms={m['id']:m for m in p['mentions']};cls.father=cls.ms[cls.role['naming_father']]['person_id'];cls.children=[r['subject_person_id']for r in cls.doc['records']]
 def setUp(self):
  self.t=tempfile.TemporaryDirectory(prefix='cbr-parentage-test-');self.addCleanup(self.t.cleanup);self.root=Path(self.t.name)
  for rel in [ri.PIN,'sources/witnesses/nanqi043-ws2400356.wikitext','corpus/nanqishu/043-xieyue.json','corpus/nanqishu/043-xieyue-assertions.json','corpus/nanqishu/043-xieyue-relationship-interpretations.json']:
   p=self.root/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/rel,p)
  pids={m['person_id']for u in self.chapter['paragraphs']for m in u['mentions']if m.get('person_id')};pids.update(v[k]for v in self.assertions['assertions']for k in ['subject_person_id','object_person_id']);self.people={pid:self.people[pid]for pid in pids};p=self.root/'registry/persons.json';p.parent.mkdir();p.write_text(json.dumps(dict(persons=list(self.people.values())),ensure_ascii=False));self.rows=[copy.deepcopy(self.chapter),copy.deepcopy(self.assertions),copy.deepcopy(self.doc)]
 def test_exact_real_source_frame_and_two_records(self):
  self.assertEqual(ri.errors(self.root,self.rows,self.people),[])
  for r in self.doc['records']:
   self.assertTrue(ri.valid(r,self.chapter,self.root,self.people));self.assertEqual(r['status'],'contextual_provisional');self.assertFalse(r['human_reviewed']);self.assertFalse(r['qualification']['source_explicit_parent_for_subject']);self.assertEqual(len(r['source_context']['scope_segments']),3);self.assertEqual(len(r['source_context']['role_mentions']),9)
 def test_both_endpoints_and_both_identity_modes(self):
  for flag in [False,True]:
   for pid,count in [(self.father,2),*( (c,1)for c in self.children)]:
    b=bundle(pid,self.root,flag,catalog=(self.people,self.rows));self.assertEqual(len(b['relationship_interpretations']),count);self.assertTrue({r['id']for r in b['relationship_interpretations']}.isdisjoint({r['id']for r in b['relations']+b['preferred_relations']}));self.assertTrue({r[k]for r in b['relationship_interpretations']for k in ['subject_person_id','object_person_id']}.issubset({p['id']for p in b['persons']}));self.assertIn(self.chapter['id'],{p['chapter_id']for p in b['passages']});self.assertTrue(all(r['id']not in str(b['birth_order_constraints'])for r in self.doc['records']))
 def test_no_interpretation_old_output_shape_and_no_pin_read(self):
  (self.root/ri.PIN).unlink();rows=self.rows[:-1]
  for flag in [False,True]:
   b=bundle(self.children[0],self.root,flag,catalog=(self.people,rows));self.assertNotIn('relationship_interpretations',b)
 def test_provisional_flag_keeps_existing_identity_semantics(self):
  # Deliberately synthetic identity-only fixture; not a historical merger or native datum.
  alias='fixture_equivalence_person';people=dict(self.people);people[alias]={'id':alias,'label':'Synthetic test identity','aliases':[],'evidence':[]};rows=self.rows+[{'record_type':'person_equivalence_set','decisions':[{'id':'fixture-equivalence','person_ids':[alias,self.children[0]],'status':'contextual_provisional','evidence':[]}]}]
  a=bundle(alias,self.root,False,catalog=(people,rows));b=bundle(alias,self.root,True,catalog=(people,rows));self.assertEqual(a['person_ids'],[alias]);self.assertNotIn('relationship_interpretations',a);self.assertEqual(set(b['person_ids']),{alias,self.children[0]});self.assertEqual(len(b['relationship_interpretations']),1)
 def test_wrong_role_endpoints_and_false_certainty_rejected(self):
  r=self.doc['records'][0]
  mutations=[('subject_person_id',self.father),('object_person_id',self.children[1]),('status','source_attested'),('human_reviewed',True),('predicate','mother')]
  for k,v in mutations:
   x=copy.deepcopy(r);x[k]=v;self.assertFalse(ri.valid(x,self.chapter,self.root,self.people),(k,v))
  for k,v in [('source_explicit_parent_for_subject',True),('shared_mother','same'),('absolute_birth_order',3),('graph_effect','preferred_parent')]:
   x=copy.deepcopy(r);x['qualification'][k]=v;self.assertFalse(ri.valid(x,self.chapter,self.root,self.people),k)
 def test_wrong_known_person_kind_and_co_shifted_quote(self):
  for role in ['father','naming_father','head_resumed','third_older_brother']:
   ch=copy.deepcopy(self.chapter);m=next(m for m in ch['paragraphs'][0]['mentions']if m['id']==self.role[role]);m['person_id']=self.children[1];self.assertFalse(ri.valid(self.doc['records'][0],ch,self.root,self.people),role)
  ch=copy.deepcopy(self.chapter);next(m for m in ch['paragraphs'][0]['mentions']if m['id']==self.role['naming_father'])['kind']='unresolved';self.assertFalse(ri.valid(self.doc['records'][0],ch,self.root,self.people))
  ch=copy.deepcopy(self.chapter);ch['paragraphs'][0]['text']=ch['paragraphs'][0]['text'].replace('名兒','名臣');r=copy.deepcopy(self.doc['records'][0]);r['evidence'][0]['quote']=ch['paragraphs'][0]['text'];self.assertFalse(ri.valid(r,ch,self.root,self.people))
 def test_raw_co_shift_cannot_become_new_witness(self):
  p=self.root/'sources/witnesses/nanqi043-ws2400356.wikitext';p.write_text(p.read_text().replace('名兒','名臣'));ch=copy.deepcopy(self.chapter);ch['paragraphs'][0]['text']=ch['paragraphs'][0]['text'].replace('名兒','名臣');ch['source']['wikitext_sha256']=hashlib.sha256(p.read_bytes()).hexdigest();r=copy.deepcopy(self.doc['records'][0]);r['evidence'][0]['quote']=ch['paragraphs'][0]['text'];r['source_context']['paragraph_sha256']=hashlib.sha256(ch['paragraphs'][0]['text'].encode()).hexdigest();r['source_context']['raw_sha256']=ch['source']['wikitext_sha256'];r['source_context']['scope_segments'][2]['literal']=r['source_context']['scope_segments'][2]['literal'].replace('名兒','名臣');r['source_term']=r['source_term'].replace('名兒','名臣');self.assertFalse(ri.valid(r,ch,self.root,self.people))
 def test_only_brothers_or_missing_naming_scope_rejected(self):
  r=copy.deepcopy(self.doc['records'][0]);r['source_context']['scope_segments']=r['source_context']['scope_segments'][1:2];r['source_term']='𤅢四兄颺、朏、顥、嵷，';self.assertFalse(ri.valid(r,self.chapter,self.root,self.people));r=copy.deepcopy(self.doc['records'][0]);r['source_context']['role_mentions'].pop('naming_father');self.assertFalse(ri.valid(r,self.chapter,self.root,self.people))
 def test_consistent_rekey_works_single_role_drift_fails(self):
  ids={self.ms[mid]['person_id']for mid in self.role.values()};mapping={pid:'fixture_rekey_'+str(i)for i,pid in enumerate(sorted(ids))};ch=copy.deepcopy(self.chapter);people=dict(self.people)
  for old,new in mapping.items():people[new]=dict(people[old],id=new)
  for u in ch['paragraphs']:
   for m in u['mentions']:
    if m.get('person_id')in mapping:m['person_id']=mapping[m['person_id']]
  expected=ri.expected(ch,self.root,people);self.assertEqual(len(expected),2);self.assertTrue(all(ri.valid(r,ch,self.root,people)for r in expected));bad=copy.deepcopy(expected[0]);bad['object_person_id']=self.father;self.assertFalse(ri.valid(bad,ch,self.root,people))
 def test_complete_finite_pair_and_malformed_inputs(self):
  for records in [[],self.doc['records'][:1],self.doc['records']*2,None,{}]:
   d=dict(self.doc,records=records);self.assertTrue(ri.errors(self.root,[self.chapter,d],self.people))
  for v in [None,[],0,'record',True]:self.assertFalse(ri.valid(v,self.chapter,self.root,self.people))
  for part,value in [('source',None),('source',[]),('paragraphs',None),('paragraphs',[None])]:
   ch=copy.deepcopy(self.chapter);ch[part]=value;self.assertFalse(ri.valid(self.doc['records'][0],ch,self.root,self.people))
 def test_actual_load_catalog_rejects_invalid_sidecar(self):
  people,rows=load_catalog(self.root);self.assertIn(self.children[0],people);d=copy.deepcopy(self.doc);d['records'][0]['status']='source_attested';(self.root/'corpus/nanqishu/043-xieyue-relationship-interpretations.json').write_text(json.dumps(d,ensure_ascii=False))
  with self.assertRaises(ValueError):load_catalog(self.root)
 def test_known_sidecar_wrong_record_type_cannot_disappear(self):
  d=copy.deepcopy(self.doc);d['record_type']='unrecognized_parentage';(self.root/ri.SIDECAR).write_text(json.dumps(d,ensure_ascii=False))
  with self.assertRaises(ValueError):load_catalog(self.root)
 def test_module_entry_and_direct_invalid_data_reject(self):
  env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=str(ROOT));p=subprocess.run([sys.executable,'-m','scripts.received_parentage_interpretations','--root',str(self.root),'--person-id',self.father],capture_output=True,text=True,env=env,cwd=self.root);self.assertEqual(p.returncode,0,p.stderr);self.assertEqual(json.loads(p.stdout),self.doc['records']);bad=copy.deepcopy(self.doc);bad['records'][0]['status']='source_attested';(self.root/ri.SIDECAR).write_text(json.dumps(bad,ensure_ascii=False));p=subprocess.run([sys.executable,str(ROOT/'scripts/received_parentage_interpretations.py'),'--root',str(self.root)],capture_output=True,text=True,env=env);self.assertNotEqual(p.returncode,0);self.assertNotIn('Traceback',p.stderr)
 def test_actual_validator_dispatch_node(self):
  source=ast.parse((ROOT/'scripts/validate_corpus.py').read_text());fn=next(n for n in source.body if isinstance(n,ast.FunctionDef)and n.name=='validate');nodes=[n for n in ast.walk(fn)if isinstance(n,ast.If)and any(isinstance(c,ast.Constant)and c.value=='person_relationship_interpretation_set'for c in ast.walk(n.test))];self.assertEqual(len(nodes),1);f=ast.FunctionDef(name='dispatch',args=ast.arguments(posonlyargs=[],args=[ast.arg(arg=x)for x in ['root','catalog','pids']],kwonlyargs=[],kw_defaults=[],defaults=[]),body=[ast.Assign(targets=[ast.Name(id='errors',ctx=ast.Store())],value=ast.List(elts=[],ctx=ast.Load())),copy.deepcopy(nodes[0]),ast.Return(value=ast.Name(id='errors',ctx=ast.Load()))],decorator_list=[]);module=ast.fix_missing_locations(ast.Module(body=[f],type_ignores=[]));ns={};exec(compile(module,'actual-validator-dispatch','exec'),ns);self.assertEqual(ns['dispatch'](self.root,(self.people,self.rows),set(self.people)),[]);bad=copy.deepcopy(self.rows);bad[-1]['records'][0]['qualification']['graph_effect']='preferred_parent';self.assertTrue(ns['dispatch'](self.root,(self.people,bad),set(self.people)))
 def test_direct_script_and_import_query_match(self):
  env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');p=subprocess.run([sys.executable,str(ROOT/'scripts/received_parentage_interpretations.py'),'--root',str(self.root),'--person-id',self.father],capture_output=True,text=True,env=env);self.assertEqual(p.returncode,0,p.stderr);self.assertEqual(json.loads(p.stdout),self.doc['records'])
  target=self.root/'scripts/person_bundle.py';target.parent.mkdir(exist_ok=True);shutil.copyfile(ROOT/'scripts/person_bundle.py',target);env['PYTHONPATH']=str(ROOT/'scripts');p=subprocess.run([sys.executable,str(target),self.children[0]],capture_output=True,text=True,env=env,cwd=self.root);self.assertEqual(p.returncode,0,p.stderr);direct=json.loads(p.stdout);imported=bundle(self.children[0],self.root,catalog=load_catalog(self.root));self.assertEqual(direct,imported)
if __name__=='__main__':unittest.main()
