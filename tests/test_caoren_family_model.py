"""Persistent dispatcher malformed-input and reviewed-helper collision regressions."""
from pathlib import Path
import tempfile,shutil,unittest,importlib.util
ROOT=Path(__file__).resolve().parents[1]
class ModelGuards(unittest.TestCase):
 def test_dispatch_bad_types(self):
  from scripts.received_kin_assembly import valid
  for obj in (None,[],[1],'x',1,{},dict(parent_connection=None),dict(parent_connection=[]),dict(parent_connection='x')):
   with self.subTest(obj=obj):self.assertIs(valid(obj,{}, {},{},ROOT),False)
 def test_semantic_plan_helper_collision_and_noop(self):
  p=Path(__file__).parent/'fixtures/caoren_family_model/cbr-caoren-assembly-dispatch-guard-successor/model_plan.py'
  spec=importlib.util.spec_from_file_location('reviewed_caoren_model',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
  with tempfile.TemporaryDirectory()as td:
   root=Path(td);(root/'scripts').mkdir()
   for name in ('received_kin_assembly.py','family_assemblies.py'):
    shutil.copyfile(ROOT/'scripts'/name,root/'scripts'/name)
   expected=m.BASE/'payload/scripts/fixed_witness_assembly_roles.py'
   for rel,b in m.plan(root).items():(root/rel).write_bytes(b)
   self.assertEqual(m.plan(root),{})
   dest=root/'scripts/fixed_witness_assembly_roles.py';self.assertEqual(dest.read_bytes(),expected.read_bytes())
   dest.write_bytes(dest.read_bytes()+b'\n# unreconciled future edit\n')
   with self.assertRaisesRegex(AssertionError,'review required'):m.plan(root)
if __name__=='__main__':unittest.main()
