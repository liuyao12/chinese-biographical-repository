"""The memo is valid only inside an owning immutable validation snapshot."""
import copy,json,shutil,subprocess,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from scripts import wyd_song045_roles as m,validate_corpus as v
from scripts.validation_context import scope,DRIFT_ERROR
ROOT=Path(__file__).resolve().parents[1]
class Wyd045ScopeMemo(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.ch=json.loads((ROOT/m.PATH).read_bytes());cls.c=m.load_contract(ROOT);cls.roles=m.resolve_roles(cls.ch,ROOT,cls.c)
 def fixture(self):
  td=tempfile.TemporaryDirectory();self.addCleanup(td.cleanup);root=Path(td.name)
  paths={'registry/persons.json',m.PATH,m.CONTRACT}|{s['path']for s in self.c['foreign_seeds'].values()}
  for rel in paths:
   dest=root/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/rel,dest)
  return root,paths
 def test_same_semantics_one_body_read_and_return_isolation(self):
  original=Path.read_bytes;reads=[]
  def read(p):
   if p.resolve()==ROOT/'registry/persons.json':reads.append(str(p))
   return original(p)
  with patch.object(Path,'read_bytes',read),scope(ROOT):
   a=m.resolve_roles(self.ch,ROOT,self.c);a['liucui']='polluted'
   b=m.resolve_roles(copy.deepcopy(self.ch),str(ROOT),copy.deepcopy(self.c))
   self.assertEqual(b,self.roles);self.assertEqual(len(reads),1)
 def test_scope_outside_or_new_scope_never_keeps_old_result(self):
  original=Path.read_bytes;reads=[]
  def read(p):
   if p.resolve()==ROOT/'registry/persons.json':reads.append(1)
   return original(p)
  with patch.object(Path,'read_bytes',read):
   for _ in range(2):self.assertEqual(m.resolve_roles(self.ch,ROOT,self.c),self.roles)
   with scope(ROOT):m.resolve_roles(self.ch,ROOT,self.c);m.resolve_roles(self.ch,ROOT,self.c)
   with scope(ROOT):m.resolve_roles(self.ch,ROOT,self.c)
  self.assertEqual(len(reads),4)
 def test_different_ch_or_contract_are_not_reused(self):
  with scope(ROOT):
   self.assertEqual(m.resolve_roles(self.ch,ROOT,self.c),self.roles)
   bad=copy.deepcopy(self.ch);bad['paragraphs'][0]['text']+='甲'
   with self.assertRaises(ValueError):m.resolve_roles(bad,ROOT,self.c)
   bad=copy.deepcopy(self.c);next(iter(bad['foreign_seeds'].values()))['source_id']+='-wrong'
   with self.assertRaises(ValueError):m.resolve_roles(self.ch,ROOT,bad)
   self.assertEqual(m.resolve_roles(self.ch,ROOT,self.c),self.roles)
 def test_different_root_never_borrows_good_result(self):
  with tempfile.TemporaryDirectory()as td,scope(ROOT):
   m.resolve_roles(self.ch,ROOT,self.c)
   with self.assertRaises(OSError):m.resolve_roles(self.ch,Path(td),self.c)
 def test_complete_source_uid_relocation_and_one_end_rejected(self):
  root,paths=self.fixture();old=self.roles['liudaoji'];new='z8x_9yz_0pq'
  reg=json.loads((root/'registry/persons.json').read_bytes());self.assertFalse(any(p['id']==new for p in reg['persons']))
  def remap(x):
   if type(x)is dict:return{k:remap(v)for k,v in x.items()}
   if type(x)is list:return[remap(v)for v in x]
   if type(x)is str:return x.replace(old,new)
   return x
  for rel in paths:
   if rel==m.CONTRACT:continue
   p=root/rel;p.write_text(json.dumps(remap(json.loads(p.read_bytes())),ensure_ascii=False))
  ch=remap(self.ch)
  with scope(root):
   self.assertEqual(m.resolve_roles(ch,root,self.c)['liudaoji'],new)
   with self.assertRaises(ValueError):m.resolve_roles(self.ch,root,self.c)
  # Exact metadata/source spans remain unchanged: this is a role resolver proof,
  # not a claim that a complete family-path rekey passed the whole native CLI.
 def test_missing_reverse_and_wrong_role_rejected(self):
  root,_=self.fixture();path=root/'registry/persons.json';reg=json.loads(path.read_bytes());person=next(p for p in reg['persons']if p['id']==self.roles['liucui']);person['aliases']=[];path.write_text(json.dumps(reg,ensure_ascii=False))
  with scope(root):
   with self.assertRaises(ValueError):m.resolve_roles(self.ch,root,self.c)
  bad=copy.deepcopy(self.ch)
  for p in bad['paragraphs']:
   for mark in p['mentions']:
    if mark.get('person_id')==self.roles['liudaoji']:mark['person_id']=self.roles['liucui']
  with scope(ROOT):
   m.resolve_roles(self.ch,ROOT,self.c)
   with self.assertRaises(ValueError):m.resolve_roles(bad,ROOT,self.c)
 def test_dirty_root_rejected_by_owning_validate_fingerprint(self):
  root,_=self.fixture();path=root/'registry/persons.json';old=path.read_bytes()
  def inner(actual_root):
   m.resolve_roles(self.ch,actual_root,self.c);path.write_bytes(old+b'\n')
   # Existing scope memo assumes immutable input. The owning full-snapshot
   # wrapper must detect this drift; do not claim each hit rereads disk.
   m.resolve_roles(self.ch,actual_root,self.c);return []
  try:
   with patch.object(v,'_validate_uncached',inner):errors=v.validate(root)
   self.assertTrue(any(DRIFT_ERROR in e for e in errors))
  finally:path.write_bytes(old)
 def test_flat_and_package_import_share_scope_handle(self):
  code='''import sys,json
from pathlib import Path
root=Path(sys.argv[1]);sys.path.insert(0,str(root/'scripts'))
import wyd_song045_roles as m,validation_context as c
assert m.memoized is c.memoized
sys.path.insert(0,str(root))
from scripts import validation_context as package_c,wyd_song045_roles as package_m
assert package_c is c and package_m.memoized is c.memoized
ch=json.loads((root/m.PATH).read_bytes());co=m.load_contract(root)
with c.scope(root):
 a=m.resolve_roles(ch,root,co);b=m.resolve_roles(ch,root,co);assert a==b and a is not b
 assert package_m.resolve_roles(ch,root,co)==a
print(json.dumps(a,sort_keys=True))'''
  with tempfile.TemporaryDirectory()as td:
   p=subprocess.run([sys.executable,'-B','-c',code,str(ROOT)],cwd=td,capture_output=True,text=True)
  self.assertEqual(p.returncode,0,p.stderr);self.assertEqual(json.loads(p.stdout),self.roles)
if __name__=='__main__':unittest.main()
