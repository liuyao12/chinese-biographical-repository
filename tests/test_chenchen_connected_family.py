"""真實原生家族與缺代的可攜回歸，不依賴私有package或/tmp。"""
from pathlib import Path
import json,copy,unittest,sys,subprocess,shutil
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.person_bundle import load_catalog,bundle
from scripts.family_assemblies import load_assemblies
from scripts.person_ids import family_path_errors
J=lambda p:json.loads(p.read_text());SHI='9w8_tqh_ysn';CHEN=SHI+'_B';ZUO=CHEN+'*A';ZHUN=CHEN+'*AA';KUI=CHEN+'*AA*A'
class ChenchenConnectedTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.catalog=load_catalog(ROOT);cls.families=J(ROOT/'registry/family-assemblies.json');cls.rows=next(a for a in cls.families['assemblies']if a['id']=='family-sanguozhi022-shi')['members'];cls.by={r['person_id']:r for r in cls.rows}
 def test_single_root_and_direct_source_father(self):
  source,assembled=load_assemblies(ROOT,self.catalog);self.assertEqual(sum(any(m['person_id']==CHEN for m in a['members'])for a in self.families['assemblies']),1);r=self.by[CHEN];self.assertEqual(r['parent_person_id'],SHI);self.assertEqual(r['source_assertion_id'],'a-houhanshu062-chen-002');self.assertNotIn('parent_connection',r)
  a=next(a for a in J(ROOT/'corpus/houhanshu/062-assertions.json')['assertions']if a['id']==r['source_assertion_id']);self.assertEqual((a['subject_person_id'],a['object_person_id']),(CHEN,SHI));self.assertEqual(a['qualifiers']['source_term'],'有六子紀諶最賢')
 def test_gap_fathers_stay_unknown(self):
  for pid,ancestor in [(ZUO,CHEN),(KUI,ZHUN)]:
   r=self.by[pid];self.assertIsNone(r['parent_person_id']);self.assertEqual(r['ancestor_person_id'],ancestor);self.assertEqual(r['generation_distance'],2);self.assertEqual(r['intermediate_person_ids'],[None]);self.assertEqual(family_path_errors(pid,r),[])
  self.assertEqual(self.by[ZHUN]['parent_person_id'],ZUO)
 def test_letters_not_absolute_order(self):
  for pid in [CHEN,ZUO,ZHUN,KUI]:self.assertIsNone(self.by[pid].get('ordinal'));self.assertIsNone(self.by[pid].get('birth_order'))
  a=next(a for a in J(ROOT/'corpus/houhanshu/062-assertions.json')['assertions']if a['id']=='a-houhanshu062-chen-004');self.assertEqual(a['qualifiers']['relative_birth_order']['older_person_id'],SHI+'_A');self.assertEqual(a['qualifiers']['relative_birth_order']['younger_person_id'],CHEN)
 def reject_family_change(self,change):
  data=copy.deepcopy(self.families);rows=next(a for a in data['assemblies']if a['id']=='family-sanguozhi022-shi')['members'];change({r['person_id']:r for r in rows});original=Path.read_text
  def read(p,*a,**k):return json.dumps(data,ensure_ascii=False)if p==ROOT/'registry/family-assemblies.json'else original(p,*a,**k)
  with patch.object(Path,'read_text',read):
   with self.assertRaises(ValueError):load_assemblies(ROOT,self.catalog)
 def test_wrong_father_rejected(self):self.reject_family_change(lambda r:r[CHEN].update(parent_person_id=SHI+'_A'))
 def test_brother_not_father_source_rejected(self):self.reject_family_change(lambda r:r[CHEN].update(source_assertion_id='a-houhanshu062-chen-004'))
 def test_grandfather_cannot_become_father(self):self.reject_family_change(lambda r:r[ZUO].update(parent_person_id=CHEN))
 def test_fabricated_intermediate_rejected(self):self.reject_family_change(lambda r:r[KUI].update(intermediate_person_ids=[ZHUN]))
 def test_wrong_generation_rejected(self):self.reject_family_change(lambda r:r[ZUO].update(generation_distance=1))
 def test_cycle_rejected(self):self.reject_family_change(lambda r:r[CHEN].update(parent_person_id=ZHUN))
 def test_actual_trace_three_generations(self):
  self.assertIsNotNone(shutil.which('node'),'需要Node執行實際reader家族函式')
  source,assembled=load_assemblies(ROOT,self.catalog);ids={*(SHI+'_'+c for c in 'CDEF'),SHI,SHI+'_A',SHI+'_AA',SHI+'_AAA',SHI+'_AAAA',SHI+'_AAB',CHEN,ZUO,ZHUN,KUI};profiles={}
  for pid in ids:
   b=bundle(pid,root=ROOT,include_provisional=True,catalog=self.catalog)
   if pid in source:b['assembled_identity']=source[pid]
   b['id']=pid;b['label']=next(p['label']for p in b['persons']if p['id']==pid);profiles[pid]=b
  code="""import fs from 'node:fs';import assert from 'node:assert/strict';import {pathToFileURL}from'node:url';
const root=process.argv[1],{traceFamily}=await import(pathToFileURL(root+'/assets/person-family.js'));
const p=JSON.parse(fs.readFileSync(0,'utf8')),load=async id=>{assert(p[id],id);return p[id]};
const s='9w8_tqh_ysn',c=s+'_B',z=c+'*A',n=c+'*AA',k=c+'*AA*A';
const expect=[[c,[[s],[],[]]],[z,[[],[c],[s]]],[n,[[z],[],[c]]],[k,[[],[n],[z]]]];
for(const[id,rows]of expect){const f=await traceFamily(await load(id),load);assert.deepEqual(f.ancestors.map(r=>r.map(x=>x.id)),rows);assert(f.ancestors.flat().every(x=>!x.cycle&&!x.unavailable&&x.role!=='assembly_inferred'));assert.deepEqual(f.mother,[]);}
const f=await traceFamily(await load(s),load);assert.deepEqual(f.children.map(x=>x.id).sort(),[s+'_A',c,...'CDEF'.split('').map(x=>s+'_'+x)].sort());console.log('PASS actual traceFamily 4 + root children');"""
  result=subprocess.run(['node','--input-type=module','-e',code,str(ROOT)],input=json.dumps(profiles,ensure_ascii=False),text=True,capture_output=True);self.assertEqual(result.returncode,0,result.stderr);self.assertIn('PASS actual traceFamily',result.stdout)
if __name__=='__main__':unittest.main()
