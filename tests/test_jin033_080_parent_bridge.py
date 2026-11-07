from pathlib import Path
import unittest,json,copy
from unittest.mock import patch
from scripts.person_bundle import load_catalog
from scripts.family_assemblies import load_assemblies
from scripts.ancestry_chain import consecutive_ancestor_parent_valid
from scripts.fixed_jin080_wangxizhi_comparison import resolve,validate_source
from scripts.retired_person_ids import retired_person_ids
from scripts.person_ids import allocate_person_id
ROOT=Path(__file__).resolve().parents[1]
class ParentBridge(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.people,cls.records=load_catalog(ROOT);cls.chs={r['id']:r for r in cls.records if r.get('record_type')=='marked_chapter'};cls.ch=cls.chs['c-jinshu-080-wangxizhi-comparison'];cls.roles=resolve(ROOT,cls.ch);cls.facts={a['id']:a for r in cls.records if r.get('record_type')=='person_assertion_set'for a in r['assertions']};cls.smap,cls.assembled=load_assemblies(ROOT,(cls.people,cls.records));cls.member=cls.assembled[cls.roles['kuang']];cls.family=next(a for a in json.loads((ROOT/'registry/family-assemblies.json').read_bytes())['assemblies']if any(m['person_id']==cls.roles['kuang']for m in a['members']));cls.rows={m['person_id']:m for m in cls.family['members']};cls.original=cls.rows[cls.roles['kuang']]
 def valid(self,m=None,a=None,c=None):return consecutive_ancestor_parent_valid(self.original if m is None else m,self.rows,self.facts if a is None else a,self.chs if c is None else c,root=ROOT)
 def test_actual_normal_source_and_path(self):self.assertEqual(validate_source(self.ch,ROOT),self.roles);self.assertTrue(self.valid())
 def test_literal_ancestor_and_editorial_father_separate(self):
  self.assertEqual(self.facts['a-jin080-xizhi-grandfather-zheng']['qualifiers']['lineage'],'paternal');self.assertEqual(self.member['parent_person_id'],self.roles['zheng']);self.assertIsNone(self.member['source_assertion_id']);self.assertFalse(any(a['predicate']=='father'and a['subject_person_id']==self.roles['kuang']for a in self.facts.values()))
 def test_native033_three_existing_edges_not_duplicated(self):
  for aid in ['a-jinshu033-wang-009','a-jinshu033-wang-012','a-jinshu033-wang-015']:
   a=self.facts[aid];self.assertEqual(a['predicate'],'father');self.assertEqual(a['status'],'source_attested')
 def test_no_old_local_duplicate(self):
  self.assertNotEqual(self.family['id'],'family-jin080-wangkuang-near-family');self.assertEqual(self.assembled[self.roles['xz']]['root_person_id'],self.member['root_person_id']);self.assertEqual(self.assembled[self.roles['jingzhi']]['root_person_id'],self.member['root_person_id'])
 def test_jingzhi_father_stays_unknown(self):
  r=self.assembled[self.roles['jingzhi']];self.assertIsNone(r['parent_person_id']);self.assertEqual(r['ancestor_person_id'],self.roles['xz']);self.assertEqual(r['generation_distance'],2);self.assertEqual(r['intermediate_person_ids'],[None])
 def test_405_kuang_not_joined(self):self.assertNotEqual(self.roles['kuang'],self.roles['kuang405']);self.assertNotIn(self.roles['kuang405'],self.rows)
 def test_source_review_uses_current_endpoints(self):
  r=json.loads((ROOT/'source-evidence/jin080-wangxizhi-comparison/paternal-grandfather-reading.json').read_bytes());self.assertEqual(r['subject_person_id'],self.roles['xz']);self.assertEqual(r['object_person_id'],self.roles['zheng']);self.assertFalse(r['human_reviewed'])
 def test_original_unspecified_refused(self):
  a=copy.deepcopy(self.facts);a['a-jin080-xizhi-grandfather-zheng']['qualifiers']['lineage']='unspecified';self.assertFalse(self.valid(a=a))
 def test_maternal_refused(self):
  a=copy.deepcopy(self.facts);a['a-jin080-xizhi-grandfather-zheng']['qualifiers']['lineage']='maternal';self.assertFalse(self.valid(a=a))
 def test_wrong_chain_subject(self):
  m=copy.deepcopy(self.original);m['parent_connection']['chain_subject_person_id']=self.roles['kuang405'];self.assertFalse(self.valid(m=m))
 def test_swapped_near_far(self):
  m=copy.deepcopy(self.original);c=m['parent_connection'];c['nearer_ancestor_assertion_id'],c['farther_ancestor_assertion_id']=c['farther_ancestor_assertion_id'],c['nearer_ancestor_assertion_id'];self.assertFalse(self.valid(m=m))
 def test_literal_father_claim_rejected(self):
  m=copy.deepcopy(self.original);m['source_assertion_id']='a-jin080-xizhi-father-kuang';self.assertFalse(self.valid(m=m))
 def test_competing_father_rejected(self):
  a=copy.deepcopy(self.facts);a['wrong']={'predicate':'father','subject_person_id':self.roles['kuang'],'object_person_id':self.roles['kuang405']};self.assertFalse(self.valid(a=a))
 def test_missing_reference(self):
  m=copy.deepcopy(self.original);m['parent_connection']['references'].pop();self.assertFalse(self.valid(m=m))
 def test_fake_continuous_quote_rejected(self):
  m=copy.deepcopy(self.original);m['parent_connection']['references'][0]['quote']='祖正父曠';self.assertFalse(self.valid(m=m))
 def test_cross_paragraph_rejected(self):
  a=copy.deepcopy(self.facts);a['a-jin080-xizhi-grandfather-zheng']['evidence'][0]['paragraph_id']='wrong';self.assertFalse(self.valid(a=a))
 def test_human_false_not_zero(self):
  m=copy.deepcopy(self.original);m['parent_connection']['human_reviewed']=0;self.assertFalse(self.valid(m=m))
 def test_retired_ten_reserved_not_alias(self):
  old=json.loads((ROOT/'source-evidence/jin080-wanglan-bridge/retirement-080-wanglan-join.json').read_bytes())['retired_person_ids'];self.assertEqual(len(old),10);self.assertTrue(set(old)<=retired_person_ids(ROOT));self.assertFalse(set(old)&set(self.people));self.assertFalse(set(old)&{i for p in self.people.values()for i in p.get('id_aliases',[])})
 def test_allocator_retries_previous_root(self):
  chars=iter('5j4fa5n5wz9zz9zz9z')
  with patch('scripts.person_ids.secrets.choice',side_effect=lambda _:next(chars)):self.assertEqual(allocate_person_id(set(self.people),root=ROOT),'z9z_z9z_z9z')
if __name__=='__main__':unittest.main()
