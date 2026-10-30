"""Current actual098 source proofs; scope memo never owns caller data or a future root."""
import copy,json,subprocess,sys,tempfile,unittest,shutil
from pathlib import Path
from unittest.mock import patch
from scripts import fixed_jin098_wangdun_comparison as core,fixed_jin098_wangdun_career as career,fixed_jin098_wangdun_life as life,validate_corpus as vc
from scripts.validation_context import scope,DRIFT_ERROR
ROOT=Path(__file__).resolve().parents[1];HELPERS=ROOT/'scripts'
class ProofScopeMemo(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.ch=json.loads((ROOT/career.CH).read_bytes());cls.functions=(career.prepared,life.prepared,core.validate_ner)
  cls.expected=[f(cls.ch,ROOT)for f in cls.functions]
 def all(self,ch=None,root=None):return[f(self.ch if ch is None else ch,ROOT if root is None else root)for f in self.functions]
 def fixture(self):
  td=tempfile.TemporaryDirectory();self.addCleanup(td.cleanup);r=Path(td.name)
  paths={'registry/persons.json',career.CH,core.RAW,career.TITLES,career.DETAILS,life.LIFE,life.ADDR,life.GROUP,life.OLDLIFE,'corpus/jinshu/076-wangbin.json','corpus/jinshu/098-wangdun-comparison-assertions.json','corpus/jinshu/098-wangdun-comparison-names.json','corpus/jinshu/098-wangdun-comparison-identities.json'}|{core.EP+n for n in core.PINS}|set(career.PINS)|set(life.PINS)
  def refs(x):
   if type(x)is dict:
    for v in x.values():refs(v)
   elif type(x)is list:
    for v in x:refs(v)
   elif type(x)is str and x.startswith(('corpus/','sources/'))and(ROOT/x).is_file():paths.add(x)
  for rel in list(paths):
   if rel.endswith('.json'):refs(json.loads((ROOT/rel).read_bytes()))
  for rel in paths:
   q=r/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/rel,q)
  self.assertEqual(self.all(root=r),self.expected)
  return r,paths
 def test_single_scope_hits_and_return_pollution(self):
  original=Path.read_bytes;reads=[]
  def read(p):
   if p==ROOT/'registry/persons.json':reads.append(1)
   return original(p)
  with patch.object(Path,'read_bytes',read),scope(ROOT):
   a=self.all();count=len(reads);a[0][0]['dun']='bad';a[0][1]['title_record']['holdings'][0]['title']='bad';a[1][1]['new_life_record']['events'][0]['person_id']='bad';a[2]['dun']='bad'
   self.assertEqual(self.all(),self.expected);self.assertEqual(self.all(copy.deepcopy(self.ch),str(ROOT)),self.expected);self.assertEqual(len(reads),count)
 def test_outside_new_scope_and_kwargs_are_fresh(self):
  orig=Path.read_bytes;counts=[]
  def read(p):
   if p==ROOT/'registry/persons.json':counts.append(1)
   return orig(p)
  with patch.object(Path,'read_bytes',read):
   self.all();a=len(counts);self.all();self.assertGreater(len(counts),a)
   with scope(ROOT):self.all();b=len(counts);self.all();self.assertEqual(len(counts),b);career.prepared(self.ch,root=ROOT);self.assertGreater(len(counts),b)
   b=len(counts)
   with scope(ROOT):self.all()
   self.assertGreater(len(counts),b)
 def test_different_ch_wrong_root_and_non_json_never_borrow(self):
  with tempfile.TemporaryDirectory()as td,scope(ROOT):
   self.all()
   for fn in self.functions:
    with self.assertRaises((ValueError,OSError,KeyError)):fn(self.ch,Path(td))
    for unsupported in [None,tuple(self.ch.items())]:
     with self.assertRaises((ValueError,TypeError,KeyError)):fn(unsupported,ROOT)
    bad=copy.deepcopy(self.ch);bad['source']['edition']='false print'
    with self.assertRaises((ValueError,KeyError)):fn(bad,ROOT)
   self.assertEqual(self.all(),self.expected)
 def test_two_actual_roots_and_contract_freshness(self):
  r,_=self.fixture();p=r/(career.EP+'phase1-template.json');old=p.read_bytes()
  with scope(ROOT):
   self.all();self.assertEqual(self.all(root=r),self.expected);p.write_bytes(old+b'\n')
   with self.assertRaises(ValueError):career.prepared(self.ch,r)
  p.write_bytes(old)
  with scope(r):self.assertEqual(self.all(root=r),self.expected)
  for fn,rel in [(life.prepared,life.EP+'source-proof.json'),(core.validate_ner,core.EP+'ner-template.json')]:
   file=r/rel;good=file.read_bytes()
   try:
    file.write_bytes(good+b'\n')
    with scope(r):
     with self.assertRaises(ValueError):fn(self.ch,r)
   finally:file.write_bytes(good)
 def test_closed_sidecars_are_still_scanned_on_scope_miss(self):
  r,_=self.fixture()
  for rel,record,fn in [('corpus/jinshu/shadow-titles.json',self.expected[0][1]['title_record'],career.prepared),('corpus/jinshu/shadow-life-events.json',self.expected[1][1]['new_life_record'],life.prepared)]:
   p=r/rel;p.write_text(json.dumps(record,ensure_ascii=False))
   try:
    with scope(r):
     with self.assertRaises(ValueError):fn(self.ch,r)
   finally:p.unlink()
 def test_owning_final_guard_detects_dirty_and_restored_bytes(self):
  r,_=self.fixture();p=r/(life.EP+'source-proof.json');before=p.read_bytes()
  for restore in [False,True]:
   def inner(root):
    self.all(root=root);p.write_bytes(before+b'\n')
    if restore:p.write_bytes(before)
    self.all(root=root);return []
   try:
    with patch.object(vc,'_validate_uncached',inner):errors=vc.validate(r)
    self.assertTrue(any(DRIFT_ERROR in e for e in errors))
   finally:p.write_bytes(before)
 def test_rec_catalog_people_events_not_cached(self):
  roles,t=self.expected[0];lt=self.expected[1][1];people={p['id']:p for p in json.loads((ROOT/'registry/persons.json').read_bytes())['persons']};prior=lt['prior_life_record'];event=lt['new_life_record']['events'][0];group=lt['group_record']['groups'][0];chapters={core.CID:self.ch,'c-jinshu-076-wangbin':json.loads((ROOT/'corpus/jinshu/076-wangbin.json').read_bytes())};events={prior['id']:prior,event['id']:event}
  with scope(ROOT):
   self.all();h=t['title_record']['holdings'][0];self.assertTrue(career.record_valid(h,self.ch,ROOT,'holding'));bad=copy.deepcopy(h);bad['person_id']=roles['dao'];self.assertFalse(career.record_valid(bad,self.ch,ROOT,'holding'))
   with self.assertRaises(ValueError):career.catalog_valid([self.ch,t['title_record']],people,ROOT)
   self.assertTrue(life.group_valid(group,events,chapters,people,ROOT));badp=copy.deepcopy(people);badp[roles['dun']]['label']='bad';self.assertFalse(life.group_valid(group,events,chapters,badp,ROOT));bade=copy.deepcopy(events);bade[event['id']]['person_id']=roles['dao'];self.assertFalse(life.group_valid(group,bade,chapters,people,ROOT))
 def test_legal_full_source_rekey_one_end_and_missing_reverse(self):
  r,paths=self.fixture();old=self.expected[2]['dun'];new='z8x_9yz_0pq';self.assertNotIn(new,{p['id']for p in json.loads((r/'registry/persons.json').read_bytes())['persons']})
  def rekey(x):
   if type(x)is str:return new if x==old else x
   if type(x)is list:return[rekey(v)for v in x]
   if type(x)is dict:return{k:rekey(v)for k,v in x.items()}
   return x
  for rel in paths:
   if rel=='registry/persons.json'or(rel.startswith('corpus/')and rel.endswith('.json')):
    p=r/rel;p.write_text(json.dumps(rekey(json.loads(p.read_bytes())),ensure_ascii=False))
  ch=rekey(self.ch)
  with scope(r):
   values=self.all(ch,r);self.assertEqual(values[2]['dun'],new)
   bad=copy.deepcopy(ch);bad['paragraphs'][0]['mentions'][0]['person_id']=old
   with self.assertRaises(ValueError):core.validate_ner(bad,r)
  p=r/'registry/persons.json';reg=json.loads(p.read_bytes());next(x for x in reg['persons']if x['id']==new)['aliases']=[];p.write_text(json.dumps(reg,ensure_ascii=False))
  with scope(r):
   for fn in self.functions:
    with self.assertRaises(ValueError):fn(ch,r)
 def test_flat_and_package_imports_share_scope_without_shared_mutable_returns(self):
  code="""import sys,types,json
from pathlib import Path
root=Path(sys.argv[1]);helpers=Path(sys.argv[2]);sys.path.insert(0,str(root/'scripts'))
def load(prefix,name):
 full=(prefix+'.'if prefix else'')+'fixed_jin098_wangdun_'+name;m=types.ModuleType(full);m.__file__=str(root/'scripts'/('fixed_jin098_wangdun_'+name+'.py'));m.__package__=prefix;sys.modules[full]=m;exec(compile((helpers/('fixed_jin098_wangdun_'+name+'.py')).read_bytes(),m.__file__,'exec'),m.__dict__);return m
flat=[load('',n)for n in ['comparison','career','life']]
import validation_context as vc
sys.path.insert(0,str(root));import scripts
package=[]
for n in ['comparison','career','life']:
 m=load('scripts',n);setattr(scripts,'fixed_jin098_wangdun_'+n,m);package.append(m)
from scripts import validation_context as pvc
assert vc is pvc
ch=json.loads((root/'corpus/jinshu/098-wangdun-comparison.json').read_bytes())
with vc.scope(root):
 for a,b,name in zip(flat,package,['validate_ner','prepared','prepared']):
  assert a.memoized is b.memoized is vc.memoized
  af=getattr(a,name);bf=getattr(b,name);assert hasattr(af,'__wrapped__')and hasattr(bf,'__wrapped__')
  x=af(ch,root);y=bf(ch,root);assert x==y and x is not y
print('flat/package all3 pass')"""
  with tempfile.TemporaryDirectory()as td:p=subprocess.run([sys.executable,'-B','-c',code,str(ROOT),str(HELPERS)],cwd=td,text=True,capture_output=True)
  self.assertEqual(p.returncode,0,p.stderr)
if __name__=='__main__':unittest.main()
