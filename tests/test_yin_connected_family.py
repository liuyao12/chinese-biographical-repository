"""殷羨、浩、涓明父同根；原生實例與reader實際追溯。"""
from pathlib import Path
import json,copy,unittest,subprocess,shutil
from unittest.mock import patch
from scripts.person_bundle import load_catalog,bundle
from scripts.family_assemblies import load_assemblies
ROOT=Path(__file__).resolve().parents[1];X='djo_u3b_i9w';H=X+'_A';J=X+'_AA';U='ali_hbb_4bn'
def read(p):return json.loads((ROOT/p).read_text())
class YinConnectedFamily(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.catalog=load_catalog(ROOT);cls.families=read('registry/family-assemblies.json');cls.family=next(f for f in cls.families['assemblies']if f['id']=='family-jin008077-yinhao');cls.rows={p['person_id']:p for p in cls.family['members']}
 def test_single_root_and_two_direct_fathers(self):
  self.assertEqual(self.family['root_person_id'],X);self.assertEqual(set(self.rows),{X,H,J});self.assertEqual(self.rows[H]['parent_person_id'],X);self.assertEqual(self.rows[J]['parent_person_id'],H)
  self.assertEqual(self.rows[H]['source_assertion_id'],'a-jinshu-077-yinhao-1-father');self.assertEqual(self.rows[J]['source_assertion_id'],'a-jinshu-077-yinhao-012-father')
  for p in self.rows.values():self.assertNotIn('parent_connection',p);self.assertIsNone(p.get('ordinal'))
  for pid in self.rows:self.assertEqual(sum(any(m['person_id']==pid for m in f['members'])for f in self.families['assemblies']),1)
 def test_unknown_mothers_and_uncle_chain_not_invented(self):
  assertions=read('corpus/jinshu/077-yinhao-assertions.json')['assertions'];uncle=next(a for a in assertions if a['predicate']=='paternal_uncle');self.assertEqual((uncle['subject_person_id'],uncle['object_person_id']),(H,U));self.assertNotIn(U,self.rows)
  self.assertFalse(any(a['predicate']in ['mother','maternal_role','adoptive_father']and a['subject_person_id']in [X,H,J]for a in assertions));self.assertFalse(any(a['predicate']=='brother'and {a['subject_person_id'],a['object_person_id']}=={X,U}for a in assertions))
 def reject_family(self,fn):
  data=copy.deepcopy(self.families);f=next(f for f in data['assemblies']if f['id']==self.family['id']);fn({p['person_id']:p for p in f['members']});original=Path.read_text
  def readtext(p,*a,**k):return json.dumps(data,ensure_ascii=False)if p==ROOT/'registry/family-assemblies.json'else original(p,*a,**k)
  with patch.object(Path,'read_text',readtext):
   with self.assertRaises(ValueError):load_assemblies(ROOT,self.catalog)
 def test_wrong_father_rejected(self):self.reject_family(lambda rows:rows[H].update(parent_person_id=U))
 def test_uncle_assertion_cannot_be_father(self):self.reject_family(lambda rows:rows[H].update(source_assertion_id='a-jinshu-077-yinhao-2-paternal_uncle'))
 def test_grandfather_cannot_replace_father(self):self.reject_family(lambda rows:rows[J].update(parent_person_id=X))
 def test_cycle_rejected(self):self.reject_family(lambda rows:rows[H].update(parent_person_id=J))
 def test_resumed_uncle_fixture_has_current_person_endpoint(self):
  f=read('tests/fixtures/resumed_paternal_uncle.json');self.assertEqual(f['assertion']['subject_person_id'],H);self.assertEqual(f['assertion']['id'],'a-jinshu-077-yinhao-2-paternal_uncle');self.assertEqual(f['paragraph']['mentions'][0]['person_id'],H);self.assertEqual(f['paragraph']['mentions'][0]['id'],'c-jinshu-077-yinhao:p002:m0000')
 def test_retired_person_requests_have_no_alias(self):
  old='_'.join(['9td','pwy','3bw']);ids={p['id']for p in read('registry/persons.json')['persons']};self.assertNotIn(old,ids);self.assertNotIn(old+'_A',ids)
  for pid in [old,old+'_A']:
   with self.assertRaises(ValueError):bundle(pid,root=ROOT,catalog=self.catalog,include_provisional=True)
 def test_actual_traceFamily_three_generations(self):
  self.assertIsNotNone(shutil.which('node'));source,_=load_assemblies(ROOT,self.catalog);profiles={}
  for pid in [X,H,J,U]:
   p=bundle(pid,root=ROOT,catalog=self.catalog,include_provisional=True)
   if pid in source:p['assembled_identity']=source[pid]
   p['id']=pid;p['label']=next(x['label']for x in p['persons']if x['id']==pid);profiles[pid]=p
  code="""import fs from 'node:fs';import assert from 'node:assert/strict';import{pathToFileURL}from'node:url';const root=process.argv[1],{traceFamily}=await import(pathToFileURL(root+'/assets/person-family.js')),profiles=JSON.parse(fs.readFileSync(0,'utf8')),load=async id=>{assert(profiles[id],id);return profiles[id]},x='djo_u3b_i9w',h=x+'_A',j=x+'_AA';for(const[id,ancestors,children]of [[x,[[],[],[]],[h]],[h,[[x],[],[]],[j]],[j,[[h],[x],[]],[]]]){const f=await traceFamily(await load(id),load);assert.deepEqual(f.ancestors.map(row=>row.map(p=>p.id)),ancestors);assert.deepEqual(f.children.map(p=>p.id),children);assert.deepEqual(f.mother,[]);assert(f.ancestors.flat().every(p=>!p.cycle&&!p.unavailable&&p.role!=='assembly_inferred'));}console.log('PASS actual traceFamily 3 and children');"""
  r=subprocess.run(['node','--input-type=module','-e',code,str(ROOT)],input=json.dumps(profiles,ensure_ascii=False),text=True,capture_output=True);self.assertEqual(r.returncode,0,r.stderr);self.assertIn('PASS actual traceFamily 3 and children',r.stdout)
