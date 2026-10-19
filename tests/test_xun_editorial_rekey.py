"""荀氏父系接合保留明文與編輯推定之別；RETIRED僅為負例識別碼。"""
import json,unittest,copy,tempfile,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.person_bundle import load_catalog
from scripts.family_assemblies import load_assemblies
J=lambda p:json.loads(p.read_text())
# Deliberate retired-ID negative fixtures; never active person references.
RETIRED={'b05_322_dd0','b05_322_dd0_A','b05_322_dd0_AA','7f0_56d_c8f','7f0_56d_c8f_A','1ec_ea1_9cc','479_9a2_415','b4e_77c_7e6'}
EXPECTED={'yoo_ox0_545_BB':'yoo_ox0_545_B','yoo_ox0_545_BC':'yoo_ox0_545_B','yoo_ox0_545_BABBB':'yoo_ox0_545_BABB','yoo_ox0_545_BABBC':'yoo_ox0_545_BABB','yoo_ox0_545_BAF':'yoo_ox0_545_BA'}
class XunEditorialRekey(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.catalog=load_catalog(ROOT);cls.rows=load_assemblies(ROOT,cls.catalog)[1];cls.assertions=[a for r in cls.catalog[1]if r.get('record_type')=='person_assertion_set'for a in r['assertions']]
 def test_five_connections_are_editorial_and_humanfalse(self):
  for pid,parent in EXPECTED.items():
   m=self.rows[pid];self.assertEqual(m['parent_person_id'],parent);self.assertIsNone(m['source_assertion_id']);q=m['parent_connection'];self.assertEqual(q['type'],'shared_father_through_sibling');self.assertIs(q['human_reviewed'],False);self.assertTrue(q['references']);self.assertFalse(any(a['predicate']=='father'and a['subject_person_id']==pid for a in self.assertions))
 def test_three_descendants_keep_direct_source_fathers(self):
  for pid,parent in [('yoo_ox0_545_BBA','yoo_ox0_545_BB'),('yoo_ox0_545_BBAA','yoo_ox0_545_BBA'),('yoo_ox0_545_BCA','yoo_ox0_545_BC')]:
   m=self.rows[pid];self.assertEqual(m['parent_person_id'],parent);self.assertNotIn('parent_connection',m);self.assertTrue(any(a['id']==m['source_assertion_id']and a['predicate']=='father'and a['subject_person_id']==pid and a['object_person_id']==parent for a in self.assertions))
 def test_no_retired_people_profiles_or_public_aliases(self):
  persons=J(ROOT/'registry/persons.json')['persons'];ids={p['id']for p in persons};self.assertEqual(len(ids),len(persons));self.assertFalse(ids&RETIRED)
  added=J(ROOT/'tests/fixtures/xunyou-source-new-person-ids.json');self.assertEqual(len(added),30);self.assertEqual(len(set(added)),30);self.assertTrue(set(added)<=ids)
  for pid in RETIRED:
   self.assertFalse((ROOT/f'exports/persons/{pid}.json').exists());self.assertFalse((ROOT/f'data/corpus/profiles/{pid}.json').exists())
  for pid in EXPECTED:self.assertEqual(J(ROOT/f'exports/persons/{pid}.json')['id_aliases'],[])
 def test_chen_conflicting_order_is_not_resolved_by_suffix(self):
  c=J(ROOT/'corpus/sanguozhi/010.json');p5=next(p for p in c['paragraphs']if p['id'].endswith('full:u005'));p19=next(p for p in c['paragraphs']if p['id'].endswith('full:u019'));self.assertIn('彧弟諶',p5['text']);self.assertIn('彧第四兄諶',p19['text']);a=next(a for a in self.assertions if a['id']=='a-xun10-011');self.assertNotIn('relative_birth_order',a['qualifiers']);self.assertNotIn('birth_order',a['qualifiers'])
 def test_wrong_parent_endpoint_rejected_for_all_five(self):
  for pid in EXPECTED:
   with self.subTest(pid=pid),tempfile.TemporaryDirectory()as d:
    r=Path(d);(r/'registry').mkdir();a=J(ROOT/'registry/family-assemblies.json');m=next(m for a in a['assemblies']for m in a['members']if m['person_id']==pid);m['parent_connection']['sibling_father_assertion_id']='a-houhanshu062-xun-001';(r/'registry/family-assemblies.json').write_text(json.dumps(a))
    with self.assertRaises(ValueError):load_assemblies(r,self.catalog)
 def test_explicit_different_father_negative_kept_for_all_five(self):
  for pid in EXPECTED:
   with self.subTest(pid=pid):
    cat=copy.deepcopy(self.catalog);q=self.rows[pid]['parent_connection'];a=next(a for r in cat[1]if r.get('record_type')=='person_assertion_set'for a in r['assertions']if a['id']==q['sibling_assertion_id']);a.setdefault('qualifiers',{})['shared_father']=False
    with self.assertRaises(ValueError):load_assemblies(ROOT,cat)
 def test_metadata_policy_and_next_number(self):
  d=J(ROOT/'registry/persons.json');self.assertIn('三組隨機',d['allocation']);self.assertIn('後綴表示資料位置，不等於排行',d['allocation']);self.assertIn('使用者重置',d['allocation'])
if __name__=='__main__':unittest.main()
