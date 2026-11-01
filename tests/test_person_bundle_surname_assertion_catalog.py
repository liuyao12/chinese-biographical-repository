"""Surname proofs consume the whole source catalogue, never display relations."""
import copy,unittest,os
from pathlib import Path
from scripts.person_bundle import load_catalog,bundle
from scripts.surname_from_father import validate
from scripts.validation_context import scope
ROOT=Path(os.environ.get('CBR_SURNAME_SOURCE_ROOT',Path(__file__).resolve().parents[1]))
CID='c-jinshu-059-wei-ying-children'
class SurnameAssertionCatalog(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.transaction=scope(ROOT);cls.transaction.__enter__();cls.addClassCleanup(cls.transaction.__exit__,None,None,None)
  cls.catalog=load_catalog(ROOT);cls.people,cls.records=cls.catalog
  cls.names=[n for r in cls.records if r.get('record_type')=='person_name_component_set'for n in r['records']]
  cls.chapters={r['id']:r for r in cls.records if r.get('record_type')=='marked_chapter'}
  cls.assertions=[a for r in cls.records if r.get('record_type')=='person_assertion_set'for a in r['assertions']]
  cls.owned=[n for n in cls.names if n.get('chapter_id')==CID and 'surname_basis'in n]
 def test_normal_bundle_all_owned_names(self):
  self.assertTrue(self.owned)
  for n in self.owned:
   with self.subTest(name=n['id']):
    result=bundle(n['person_id'],root=ROOT,include_provisional=True,catalog=self.catalog)
    self.assertEqual(result['canonical_person_id'],n['person_id']);self.assertEqual(result['requested_person_id'],n['person_id']);self.assertTrue(any(x['id']==n['id']for x in result['name_components']))
 def test_all_actual_surname_kinds_accept_raw_catalog(self):
  for n in self.names:
   if 'surname_basis'in n:
    with self.subTest(name=n['id'],kind=n['surname_basis']['kind']):validate(n,self.names,self.chapters,self.assertions,root=ROOT)
 def test_unrelated_source_assertion_cannot_be_dropped(self):
  n=self.owned[0];doc=next(r for r in self.records if r.get('record_type')=='person_assertion_set'and r.get('chapter_id')==CID)
  unrelated=next(a for a in doc['assertions']if n['person_id']not in(a['subject_person_id'],a['object_person_id']))
  shortened=[a for a in self.assertions if a['id']!=unrelated['id']]
  with self.assertRaises(AssertionError):validate(n,self.names,self.chapters,shortened,root=ROOT)
 def test_typed_assertion_and_duplicate_conservation(self):
  n=self.owned[0];doc=next(r for r in self.records if r.get('record_type')=='person_assertion_set'and r.get('chapter_id')==CID);target=doc['assertions'][0]
  bad=copy.deepcopy(self.assertions);next(a for a in bad if a['id']==target['id'])['human_reviewed']=0
  with self.assertRaises(AssertionError):validate(n,self.names,self.chapters,bad,root=ROOT)
  with self.assertRaises(AssertionError):validate(n,self.names,self.chapters,self.assertions+[copy.deepcopy(target)],root=ROOT)
if __name__=='__main__':unittest.main()
