"""Scope-only source-role memo; actual sources remain independently checked."""
import copy,json,shutil,subprocess,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from scripts import fixed_jin098_wangdun_comparison as m,validate_corpus as v
from scripts.validation_context import scope,DRIFT_ERROR
ROOT=Path(__file__).resolve().parents[1]
CHREL='corpus/jinshu/098-wangdun-comparison.json'
HELPER_UNDER_TEST=ROOT/'scripts/fixed_jin098_wangdun_comparison.py'
class Jin098ScopeMemo(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.ch=json.loads((ROOT/CHREL).read_bytes());cls.spec=json.loads((ROOT/(m.EP+'ner-roles.json')).read_bytes());cls.roles=m.resolve(ROOT,cls.ch)
 def fixture(self):
  tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup);root=Path(tmp.name)
  def native_paths(x):
   if isinstance(x,dict):
    return {v for k,v in x.items()if k=='native_path'} | set().union(*(native_paths(v)for v in x.values()))
   if isinstance(x,list):return set().union(*(native_paths(v)for v in x))if x else set()
   return set()
  paths={'registry/persons.json',CHREL}|{m.EP+key for key in m.PINS}|native_paths(self.spec)
  for rel in paths:
   dst=root/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/rel,dst)
  return root,paths
 def test_same_scope_key_and_return_isolation(self):
  original=Path.read_bytes;reads=[]
  def read(p):
   if p.resolve()==ROOT/'registry/persons.json':reads.append(1)
   return original(p)
  with patch.object(Path,'read_bytes',read),scope(ROOT):
   a=m.resolve(ROOT,self.ch);a['dun']='caller-pollution';self.assertEqual(m.resolve(str(ROOT),copy.deepcopy(self.ch)),self.roles);self.assertEqual(len(reads),1)
 def test_outside_and_new_scope_fresh(self):
  original=Path.read_bytes;reads=[]
  def read(p):
   if p.resolve()==ROOT/'registry/persons.json':reads.append(1)
   return original(p)
  with patch.object(Path,'read_bytes',read):
   m.resolve(ROOT,self.ch);m.resolve(ROOT,self.ch)
   with scope(ROOT):m.resolve(ROOT,self.ch);m.resolve(ROOT,self.ch)
   with scope(ROOT):m.resolve(ROOT,self.ch)
  self.assertEqual(len(reads),4)
 def test_different_ch_and_wrong_root_not_borrowed(self):
  with tempfile.TemporaryDirectory()as td,scope(ROOT):
   m.resolve(ROOT,self.ch)
   with self.assertRaises((OSError,ValueError)):m.resolve(Path(td),self.ch)
   bad=copy.deepcopy(self.ch);bad['paragraphs'][0]['mentions'][0]['kind']='unresolved';bad['paragraphs'][0]['mentions'][0]['person_id']=None
   with self.assertRaises((ValueError,KeyError)):m.resolve(ROOT,bad)
   bad=copy.deepcopy(self.ch);bad['source']['edition']='武英殿'
   with self.assertRaises(ValueError):m.validate_ner(bad,ROOT)
   self.assertEqual(m.resolve(ROOT,self.ch),self.roles)
 def test_roles_contract_changed_new_scope_rejected(self):
  root,_=self.fixture();path=root/(m.EP+'ner-roles.json');old=path.read_bytes()
  with scope(root):self.assertEqual(m.resolve(root,self.ch),self.roles)
  try:
   path.write_bytes(old+b'\n')
   with scope(root):
    with self.assertRaises(ValueError):m.resolve(root,self.ch)
  finally:path.write_bytes(old)
  with scope(root):self.assertEqual(m.resolve(root,self.ch),self.roles)
 def test_one_end_and_missing_reverse_rejected(self):
  with scope(ROOT):
   m.resolve(ROOT,self.ch);bad=copy.deepcopy(self.ch);old=self.roles['dun']
   for p in bad['paragraphs']:
    for mark in p['mentions']:
     if mark.get('person_id')==old:mark['person_id']='z8x_9yz_0pq'
   with self.assertRaises(ValueError):m.resolve(ROOT,bad)
  root,_=self.fixture();path=root/'registry/persons.json';reg=json.loads(path.read_bytes());next(p for p in reg['persons']if p['id']==self.roles['dun'])['aliases']=[];path.write_text(json.dumps(reg,ensure_ascii=False))
  with scope(root):
   with self.assertRaises(ValueError):m.resolve(root,self.ch)
 def test_complete_source_role_rekey_not_new_person_alias(self):
  root,paths=self.fixture();old=self.roles['dun'];new='z8x_9yz_0pq';self.assertNotIn(new,{p['id']for p in json.loads((root/'registry/persons.json').read_bytes())['persons']})
  def remap(x):
   if type(x)is str:return new if x==old else x
   if type(x)is dict:return{k:remap(v)for k,v in x.items()}
   if type(x)is list:return[remap(v)for v in x]
   return x
  for rel in paths:
   if rel.startswith('corpus/')or rel=='registry/persons.json':
    p=root/rel;p.write_text(json.dumps(remap(json.loads(p.read_bytes())),ensure_ascii=False))
  ch=remap(self.ch)
  with scope(root):
   roles=m.resolve(root,ch);self.assertEqual(roles['dun'],new);self.assertNotEqual(roles['dun'],roles['dao']);self.assertEqual(m.resolve(root,ch),roles)
   with self.assertRaises(ValueError):m.resolve(root,self.ch)
 def test_owning_fingerprint_rejects_dirty_contract(self):
  root,_=self.fixture();path=root/(m.EP+'ner-roles.json');old=path.read_bytes()
  def inner(actual):
   m.resolve(actual,self.ch);path.write_bytes(old+b'\n');m.resolve(actual,self.ch);return []
  try:
   with patch.object(v,'_validate_uncached',inner):errors=v.validate(root)
   self.assertTrue(any(DRIFT_ERROR in e for e in errors))
  finally:path.write_bytes(old)
 def test_flat_package_imports_use_same_scope_handle(self):
  code="""import sys,json,types
from pathlib import Path
root=Path(sys.argv[1]);helper=Path(sys.argv[2]);sys.path.insert(0,str(root/'scripts'))
def load(name):
 module=types.ModuleType(name);module.__file__=str(root/'scripts/fixed_jin098_wangdun_comparison.py');module.__package__=name.rpartition('.')[0];sys.modules[name]=module
 exec(compile(helper.read_bytes(),str(helper),'exec'),module.__dict__);return module
flat=load('fixed_jin098_wangdun_comparison')
import validation_context as vc
assert flat.memoized is vc.memoized
sys.path.insert(0,str(root))
package=load('scripts.fixed_jin098_wangdun_comparison')
from scripts import validation_context as pvc
assert pvc is vc and package.memoized is vc.memoized
ch=json.loads((root/'corpus/jinshu/098-wangdun-comparison.json').read_bytes())
with vc.scope(root):
 a=flat.resolve(root,ch);b=package.resolve(root,ch);assert a==b and a is not b
print(json.dumps(a,sort_keys=True))"""
  with tempfile.TemporaryDirectory()as td:p=subprocess.run([sys.executable,'-B','-c',code,str(ROOT),str(HELPER_UNDER_TEST)],cwd=td,text=True,capture_output=True)
  self.assertEqual(p.returncode,0,p.stderr);self.assertEqual(json.loads(p.stdout),self.roles)
if __name__=='__main__':unittest.main()
