import json,unittest
from pathlib import Path
from unittest.mock import patch
from scripts.person_bundle import load_catalog,bundle
from scripts.surname_from_father import validate
R=Path(__file__).resolve().parents[1]
class LazySurnameHook(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.catalog=load_catalog(R)
 def test_unannotated_name_never_calls_inference_helper(self):
  pid=next(n['person_id']for r in self.catalog[1]if r.get('record_type')=='person_name_component_set'for n in r['records']if n.get('id')=='name-song085-f13-001')
  with patch('scripts.surname_from_father.validate',side_effect=AssertionError('unnecessary inference call')):
   b=bundle(pid,R,True,self.catalog)
  self.assertTrue(b['name_components']);self.assertFalse(any('surname_basis'in n for n in b['name_components']))
 def test_annotated_name_still_validated(self):
  pid=next(n['person_id']for r in self.catalog[1]if r.get('record_type')=='person_name_component_set'for n in r['records']if n.get('id')=='name-song085-f13-027')
  with patch('scripts.surname_from_father.validate',wraps=validate)as m:b=bundle(pid,R,True,self.catalog)
  self.assertEqual(m.call_count,1);self.assertEqual(next(n for n in b['name_components']if 'surname_basis'in n)['surname'],'謝')
