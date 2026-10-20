# coding:utf-8
"""五個匯入邊界在package／bare script路徑都可執行；不跑全量CLI驗證。"""
import unittest,subprocess,sys,os,tempfile,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
HARNESS=r'''
import sys,json,ast,importlib
from pathlib import Path
root=Path(sys.argv[1]);mode=sys.argv[2]
sys.path=[str(root if mode=='package' else root/'scripts')]+[p for p in sys.path if p and Path(p).resolve()not in [root,root/'scripts']]
read=lambda p:json.loads((root/p).read_text())
prefix='scripts.'if mode=='package'else''
ann=importlib.import_module(prefix+'annal_year_context');un=importlib.import_module(prefix+'unassumed_appointments');val=importlib.import_module(prefix+'validate_corpus')
c=read('corpus/jinshu/077-yinhao.json');a=read('corpus/jinshu/008-yonghe5.json');h=next(h for h in read('corpus/jinshu/008-yonghe5-titles.json')['holdings']if h['person_id']=='9w8_tqh_ysn_B*AA*A');date=h['attestations'][0]['normalized_date']
assert ann.annal_regnal_year_valid(date,val.source_age_number)
assert ann.annal_year_binding_valid(date,a)
for id in ['tp-jin077-f51-002','tp-jin077-f51-004']:
 assert un.unassumed_appointment_valid(next(x for x in c['annotation']['title_proposals']if x['id']==id),c)
# Execute the validator's actual nested import statement, not a copied approximation.
tree=ast.parse((root/'scripts/validate_corpus.py').read_text());nodes=[n for n in ast.walk(tree)if isinstance(n,ast.Try)and any(isinstance(x,ast.ImportFrom)and x.module=='jin_facts_boundaries'and x.level==1 for x in n.body)]
assert len(nodes)==1
namespace={'__package__':'scripts'if mode=='package'else None,'__name__':'scripts.validate_corpus'if mode=='package'else'__main__'};exec(compile(ast.Module(body=[nodes[0]],type_ignores=[]),'<actual validator import boundary>','exec'),namespace)
event=next(x for x in read('corpus/jinshu/077-yinhao-events.json')['events']if x['id']=='pe-jin077-f51-001');deaths={x['id']:x for x in read('corpus/jinshu/077-yinhao-life-events.json')['events']}
assert namespace['posthumous_restoration_valid'](event,{c['id']:c},deaths)
print(json.dumps({'mode':mode,'five_dynamic_boundaries':True}))
'''
class CliImports(unittest.TestCase):
 def run_mode(self,mode):
  env=dict(os.environ);env.pop('PYTHONPATH',None);env['PYTHONDONTWRITEBYTECODE']='1'
  with tempfile.TemporaryDirectory()as d:
   p=subprocess.run([sys.executable,'-B','-E','-c',HARNESS,str(R),mode],cwd=d,env=env,text=True,capture_output=True)
  self.assertEqual(p.returncode,0,p.stdout+p.stderr);self.assertTrue(json.loads(p.stdout)['five_dynamic_boundaries'])
 def test_package_five_actual_branches(self):self.run_mode('package')
 def test_direct_script_five_actual_branches(self):self.run_mode('script')
if __name__=='__main__':unittest.main()
