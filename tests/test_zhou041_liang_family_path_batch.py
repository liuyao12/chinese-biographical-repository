"""Finite same-frame batching. No source proof/cache certificate is bypassed."""
import copy,importlib,importlib.util,json,os,pathlib,sys,unittest
from unittest.mock import patch
ROOT=pathlib.Path(os.environ.get('CBR_BATCH_SOURCE_ROOT',pathlib.Path(__file__).resolve().parents[1]))
CODE=pathlib.Path(os.environ.get('CBR_BATCH_CODE_ROOT',ROOT))
sys.path.insert(0,str(ROOT))
import scripts
# External candidate execution uses its two exact code files, all real dependencies
# and physical data stay at ROOT. No Path/file reader is mocked in the real case.
def module(name):
 spec=importlib.util.spec_from_file_location('scripts.'+name,CODE/'scripts'/ (name+'.py'));m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;setattr(scripts,name,m);spec.loader.exec_module(m);return m
if CODE.resolve()==ROOT.resolve():
 from scripts import liang_xiao_close_family as liang, fixed_zhou041_wangbao as zhou
else:
 liang=module('liang_xiao_close_family');zhou=module('fixed_zhou041_wangbao')
class FamilyPathBatchTests(unittest.TestCase):
 def setUp(self):
  self.roles={'$a':'test_one','b':'unused','$b':'test_two','$c':'test_three'}
  self.templates={'a':{'connection':'father','parent_person_id':'father_one','human_reviewed':False},'b':{'connection':'father','parent_person_id':'father_two','human_reviewed':False},'c':{'connection':'father','parent_person_id':'father_three','human_reviewed':False}}
  self.contract={'family_path_templates':self.templates}
  self.paths=[(self.roles['$'+r],copy.deepcopy(p))for r,p in self.templates.items()]
  self.state=(self.contract,self.roles,{}, {}, {})
 def test_same_three_original_predicates_and_single_api(self):
  expected=[any(self.roles['$'+role]==pid and liang.same(path,liang.expand(t,self.roles))for role,t in self.templates.items())for pid,path in self.paths]
  self.assertEqual(expected,[True,True,True])
  with patch.object(liang,'active',return_value=True),patch.object(liang,'proof',return_value=self.state)as proof:
   self.assertTrue(liang.family_paths_valid(ROOT,self.paths));self.assertEqual(proof.call_count,1)
   proof.reset_mock()
   for pid,path in self.paths:self.assertTrue(liang.family_path_valid(ROOT,pid,path))
   self.assertEqual(proof.call_count,3)
 def test_each_wrong_parent_is_rejected_with_one_complete_proof(self):
  for index in range(3):
   bad=copy.deepcopy(self.paths);bad[index][1]['parent_person_id']='wrong'
   with self.subTest(index=index),patch.object(liang,'active',return_value=True),patch.object(liang,'proof',return_value=self.state)as proof:
    self.assertFalse(liang.family_paths_valid(ROOT,bad));self.assertEqual(proof.call_count,1)
 def test_unknown_field_and_bool_integer_changes_still_rejected(self):
  for index in range(3):
   for change in('unknown','bool_int'):
    bad=copy.deepcopy(self.paths)
    if change=='unknown':bad[index][1]['unknown_metadata']='must_not_disappear'
    else:bad[index][1]['human_reviewed']=0
    with self.subTest(index=index,change=change),patch.object(liang,'active',return_value=True),patch.object(liang,'proof',return_value=self.state):self.assertFalse(liang.family_paths_valid(ROOT,bad))
 def test_empty_keeps_zero_complete_proofs_and_no_active_read(self):
  with patch.object(liang,'active',side_effect=AssertionError('must not read')),patch.object(liang,'proof',side_effect=AssertionError('must not prove'))as proof:
   self.assertTrue(liang.family_paths_valid(ROOT,[]));proof.assert_not_called()
 def test_complete_proof_failure_still_rejects_batch_and_single(self):
  for error in(AssertionError('source proof failure'),ValueError('source proof failure')):
   with self.subTest(error=type(error).__name__),patch.object(liang,'active',return_value=True),patch.object(liang,'proof',side_effect=error)as proof:
    self.assertFalse(liang.family_paths_valid(ROOT,self.paths));self.assertFalse(liang.family_path_valid(ROOT,*self.paths[0]));self.assertEqual(proof.call_count,2)
 def test_real_wangbao_full_source_proof_uses_one_complete_liang_proof(self):
  real=liang.proof
  with patch.object(liang,'proof',wraps=real)as calls,patch.object(liang,'family_paths_valid',wraps=liang.family_paths_valid)as batches:
   chapter,contract,roles=zhou.proof(ROOT)
  people={p['id']:p for p in json.loads((ROOT/'registry/persons.json').read_text())['persons']}
  expected=[(roles['$'+key],people[roles['$'+key]]['family_path'])for key in contract['new_people']if people[roles['$'+key]].get('family_path')]
  self.assertEqual(len(expected),3)
  self.assertEqual(batches.call_count,1);self.assertEqual(batches.call_args.args[1],expected);self.assertEqual(calls.call_count,1)
  self.assertEqual(chapter['id'],'c-zhoushu-041-wangbao-ws2432538')
if __name__=='__main__':unittest.main()
