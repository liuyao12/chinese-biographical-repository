"""明兄弟＋明祖父可限定推導同祖；缺父/從弟距離不可補造。"""
from pathlib import Path
import unittest,json,copy,tempfile
from unittest.mock import patch
from scripts.person_bundle import load_catalog
from scripts.family_assemblies import load_assemblies
from scripts.retired_person_ids import retired_person_ids,assert_not_retired,allocation_conflicts
from scripts.person_ids import allocate_person_id
R=Path(__file__).resolve().parents[1];OLD='k9s_gmw_ywi';NEW='9w8_tqh_ysn_B*B';ZUO='9w8_tqh_ysn_B*A';CHEN='9w8_tqh_ysn_B';KAN='ebp_cc5_u3h';F='registry/family-assemblies.json';A='corpus/sanguozhi/022-chenqun-chentai-assertions.json'
J=lambda p:json.loads((R/p).read_text())
class TanLineage(unittest.TestCase):
 def setUp(self):self.family_override=None;self.assertion_override=None
 def change(self,path,obj):
  # Counterexamples stay in memory or a temporary family file; never edit the corpus under test.
  if path==F:self.family_override=copy.deepcopy(obj)
  elif path==A:self.assertion_override=copy.deepcopy(obj)
  else:raise AssertionError('Unsupported fixture path: '+path)
 def member(self,f):return next(m for a in f['assemblies']if a['id']=='family-sanguozhi022-shi'for m in a['members']if m['person_id']==NEW)
 def load(self):
  people,records=load_catalog(R)
  if self.assertion_override is not None:
   replacement=self.assertion_override;records=[replacement if x.get('id')==replacement['id'] else x for x in records]
  catalog=(people,records)
  if self.family_override is None:return load_assemblies(R,catalog)
  with tempfile.TemporaryDirectory() as name:
   root=Path(name);(root/'registry').mkdir();(root/F).write_text(json.dumps(self.family_override,ensure_ascii=False)+'\n')
   # Other families' archived evidence is read only; the sole modified file is the temporary family fixture.
   (root/'source-evidence').symlink_to(R/'source-evidence',target_is_directory=True)
   return load_assemblies(root,catalog)

 def test_qualified_missing_generation_no_father(self):
  sm,rows=self.load();m=sm[NEW];self.assertEqual(m['ancestor_person_id'],CHEN);self.assertEqual(m['generation_distance'],2);self.assertIsNone(m['parent_person_id']);self.assertIsNone(m['source_assertion_id']);self.assertEqual(m['intermediate_person_ids'],[None]);self.assertEqual(m['ancestor_connection']['type'],'shared_ancestor_through_sibling');self.assertNotIn(KAN,sm)
 def test_original_brother_and_age_inequality_preserved(self):
  a=next(a for a in J(A)['assertions']if a['id']=='a-sanguozhi022-chen-016');self.assertEqual(a['subject_person_id'],NEW);self.assertEqual(a['object_person_id'],ZUO);self.assertEqual(a['predicate'],'brother');self.assertEqual(a['qualifiers']['relative_birth_order'],{'older_person_id':ZUO,'younger_person_id':NEW,'operator':'lt','scope':'siblings','older_ordinal':None,'younger_ordinal':None})
  self.assertFalse(any(a['subject_person_id']==NEW and a['predicate']in ['father','grandfather','mother']for a in J(A)['assertions']))
 def test_tan_received_character_not_full_name(self):
  c=J('corpus/sanguozhi/022-chenqun-chentai.json');p=next(p for p in c['paragraphs']if p['id'].endswith(':p016'));m=next(m for m in p['mentions']if m['id'].endswith(':m0022'));self.assertEqual(m['surface'],'坦');self.assertEqual(p['text'][m['start']:m['end']],'坦');self.assertEqual(m['person_id'],NEW)
 def test_cousin_not_promoted_to_brother(self):
  a=next(a for a in J(A)['assertions']if a['subject_person_id']==KAN);self.assertNotEqual(a['predicate'],'brother');self.assertEqual(a['qualifiers']['source_term'],'從弟堪');self.assertNotIn(KAN,self.load()[0])
 def test_reject_cousin_inference(self):
  f=J(F);m=self.member(f);m['ancestor_connection']['sibling_assertion_id']='a-sanguozhi022-chen-018';self.change(F,f)
  with self.assertRaises(ValueError):self.load()
 def test_reject_fabricated_father(self):
  f=J(F);self.member(f)['parent_person_id']=ZUO;self.change(F,f)
  with self.assertRaises(ValueError):self.load()
 def test_reject_wrong_generation(self):
  f=J(F);self.member(f)['generation_distance']=3;self.change(F,f)
  with self.assertRaises(ValueError):self.load()
 def test_reject_missing_source_reference(self):
  f=J(F);self.member(f)['ancestor_connection']['references']=[];self.change(F,f)
  with self.assertRaises(ValueError):self.load()
 def test_reject_unrelated_quote(self):
  f=J(F);self.member(f)['ancestor_connection']['references'][0]['quote']='同姓不能證同父';self.change(F,f)
  with self.assertRaises(ValueError):self.load()
 def test_reject_maternal_grandfather_as_paternal_path(self):
  a=J(A);next(x for x in a['assertions']if x['id']=='a-sanguozhi022-chen-015')['qualifiers']['lineage']='maternal';self.change(A,a)
  with self.assertRaises(ValueError):self.load()
 def test_retired_id_not_alias_or_reusable(self):
  people={p['id']for p in J('registry/persons.json')['persons']};self.assertNotIn(OLD,people);self.assertIn(NEW,people);self.assertIn(OLD,retired_person_ids(R));self.assertTrue(allocation_conflicts(OLD,retired_person_ids(R)))
  with self.assertRaises(ValueError):assert_not_retired(OLD,R)
  candidate='zz9_zz8_zz7';self.assertFalse(any(p.startswith(candidate)for p in people))
  with patch('scripts.person_ids.secrets.choice',side_effect=list(OLD.replace('_',''))+list(candidate.replace('_',''))):self.assertEqual(allocate_person_id(people,root=R),candidate)
if __name__=='__main__':unittest.main()
