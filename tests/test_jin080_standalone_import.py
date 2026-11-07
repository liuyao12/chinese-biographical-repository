"""Real source/assembly/bundle smoke test in both supported import modes."""
from pathlib import Path
import os
import subprocess
import sys
import textwrap
import unittest
ROOT=Path(__file__).resolve().parents[1]
class Jin080StandaloneImportTests(unittest.TestCase):
 def run_case(self,flat):
  imports=("from person_bundle import bundle,load_catalog\nfrom family_assemblies import load_assemblies\nfrom fixed_jin080_wangxizhi_comparison import resolve" if flat else "from scripts.person_bundle import bundle,load_catalog\nfrom scripts.family_assemblies import load_assemblies\nfrom scripts.fixed_jin080_wangxizhi_comparison import resolve")
  code="from pathlib import Path\nimport json,sys\n"+imports+"\n"+textwrap.dedent("""
  root=Path(sys.argv[1]).resolve()
  catalog=load_catalog(root)
  source_map,assembled=load_assemblies(root,catalog)
  chapter=json.loads((root/'corpus/jinshu/080-wangxizhi-comparison.json').read_text())
  roles=resolve(root,chapter)
  assert source_map[roles['jingzhi']]['parent_person_id'] is None
  assert source_map[roles['jingzhi']]['ancestor_person_id']==roles['xz']
  for role in ['xz','jingzhi']:
   for policy in [False,True]:
    result=bundle(roles[role],root,include_provisional=policy,catalog=catalog)
    assert result['person_ids']==[roles[role]]
  print('actual-assembly-and-four-bundles-ok')
  """)
  env=dict(os.environ);env.pop('PYTHONPATH',None);env['PYTHONDONTWRITEBYTECODE']='1'
  result=subprocess.run([sys.executable,'-B','-c',code,str(ROOT)],cwd=ROOT/'scripts' if flat else ROOT,env=env,text=True,capture_output=True,timeout=240)
  self.assertEqual(result.returncode,0,result.stderr or result.stdout)
  self.assertIn('actual-assembly-and-four-bundles-ok',result.stdout)
 def test_documented_script_import_mode_without_pythonpath(self):self.run_case(True)
 def test_package_import_mode(self):self.run_case(False)
