from pathlib import Path
import unittest,json,copy
from scripts.person_bundle import load_catalog,bundle
from scripts.family_assemblies import load_assemblies
from scripts.fixed_jin080_wangxizhi_comparison import resolve
from scripts.jin080_nephew_assembly import ancestor_valid,AID
from scripts.retired_person_ids import retired_person_ids,assert_not_retired
from scripts.person_ids import allocate_person_id
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
class FamilyRekey(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.people,cls.records=load_catalog(ROOT);cls.chs={r['id']:r for r in cls.records if r.get('record_type')=='marked_chapter'};cls.ch=cls.chs['c-jinshu-080-wangxizhi-comparison'];cls.roles=resolve(ROOT,cls.ch);cls.assertions={a['id']:a for r in cls.records if r.get('record_type')=='person_assertion_set'for a in r['assertions']};cls.assembly=next(a for a in json.loads((ROOT/'registry/family-assemblies.json').read_bytes())['assemblies']if any(m['person_id']==cls.roles['jingzhi']for m in a['members']));cls.rows={r['person_id']:r for r in cls.assembly['members']};cls.row=cls.rows[cls.roles['jingzhi']]
 def valid(self,row=None,rows=None,assertions=None,chs=None):return ancestor_valid(self.row if row is None else row,self.rows if rows is None else rows,self.assertions if assertions is None else assertions,self.chs if chs is None else chs,ROOT)
 def test_actual_normal_assembly(self):
  self.assertTrue(self.valid());a,b=load_assemblies(ROOT,(self.people,self.records));self.assertEqual(b[self.roles['jingzhi']]['parent_person_id'],None);self.assertEqual(b[self.roles['jingzhi']]['ancestor_person_id'],self.roles['xz'])
 def test_no_named_father_or_new_literal_grandfather(self):
  self.assertIsNone(self.row['parent_person_id']);self.assertEqual(self.row['intermediate_person_ids'],[None]);self.assertFalse(any(a['subject_person_id']==self.roles['jingzhi']and a['predicate']in('father','grandfather')for a in self.assertions.values()))
 def test_wrong_child(self):
  r=copy.deepcopy(self.row);r['person_id']=self.roles['xz'];self.assertFalse(self.valid(row=r))
 def test_wrong_ancestor(self):
  r=copy.deepcopy(self.row);r['ancestor_person_id']=self.roles['kuang'];self.assertFalse(self.valid(row=r))
 def test_invented_father(self):
  r=copy.deepcopy(self.row);r['parent_person_id']=self.roles['huizhi'];self.assertFalse(self.valid(row=r))
 def test_invented_intermediate(self):
  r=copy.deepcopy(self.row);r['intermediate_person_ids']=[self.roles['huizhi']];self.assertFalse(self.valid(row=r))
 def test_wrong_distance(self):
  r=copy.deepcopy(self.row);r['generation_distance']=1;self.assertFalse(self.valid(row=r))
 def test_bool_distance(self):
  r=copy.deepcopy(self.row);r['generation_distance']=True;self.assertFalse(self.valid(row=r))
 def test_human_false_is_not_zero(self):
  r=copy.deepcopy(self.row);r['ancestor_connection']['human_reviewed']=0;self.assertFalse(self.valid(row=r))
 def test_ritual_not_biological_proof(self):
  r=copy.deepcopy(self.row);r['ancestor_connection']['nephew_assertion_id']='a-jin080-jingzhi-ritual-successor';self.assertFalse(self.valid(row=r))
 def test_missing_nephew(self):
  a=copy.deepcopy(self.assertions);del a['a-jin080-jingzhi-uncle-xianzhi'];self.assertFalse(self.valid(assertions=a))
 def test_missing_uncle_father(self):
  a=copy.deepcopy(self.assertions);del a['a-jin080-xianzhi-father-xizhi'];self.assertFalse(self.valid(assertions=a))
 def test_reversed_uncle(self):
  a=copy.deepcopy(self.assertions);r=a['a-jin080-jingzhi-uncle-xianzhi'];r['subject_person_id'],r['object_person_id']=r['object_person_id'],r['subject_person_id'];self.assertFalse(self.valid(assertions=a))
 def test_wrong_uncle_father(self):
  a=copy.deepcopy(self.assertions);a['a-jin080-xianzhi-father-xizhi']['object_person_id']=self.roles['kuang'];self.assertFalse(self.valid(assertions=a))
 def test_conflicting_father(self):
  a=copy.deepcopy(self.assertions);a['test']={'subject_person_id':self.roles['jingzhi'],'predicate':'father','object_person_id':self.roles['caozhi']};self.assertFalse(self.valid(assertions=a))
 def test_changed_full_paragraph(self):
  c=copy.deepcopy(self.chs);c[self.ch['id']]['paragraphs'][-1]['text']+='字';self.assertFalse(self.valid(chs=c))
 def test_missing_context(self):self.assertFalse(self.valid(chs={}))
 def test_405_kuang_stays_separate(self):
  self.assertNotEqual(self.roles['kuang'],self.roles['kuang405']);self.assertNotIn(self.roles['kuang405'],self.rows)
 def test_retired_nine_not_alias(self):
  ids=json.loads((ROOT/'source-evidence/jin080-wangxizhi-family-rekey/retirement-080-family.json').read_bytes())['retired_person_ids'];self.assertEqual(len(ids),9);self.assertTrue(set(ids)<=retired_person_ids(ROOT));self.assertFalse(set(ids)&set(self.people))
  for pid in ids:
   with self.assertRaises(ValueError):assert_not_retired(pid,ROOT)
 def test_allocator_retries_retired_root(self):
  chars=iter('326fafcd3z9zz9zz9z')
  with patch('scripts.person_ids.secrets.choice',side_effect=lambda _:next(chars)):
   self.assertEqual(allocate_person_id(set(self.people),root=ROOT),'z9z_z9z_z9z')
if __name__=='__main__':unittest.main()
