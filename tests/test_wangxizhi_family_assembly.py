"""Source-specific production assembly checks, with IDs resolved from native facts."""
import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text())
class WangXizhiFamilyAssembly(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.assertions={a['id']:a for a in read('corpus/jinshu/080-wangxizhi-assertions.json')['assertions']}
  cls.family=next(x for x in read('registry/family-assemblies.json')['assemblies'] if x['id']=='family-langye-wang-dao')
  cls.rows={x['person_id']:x for x in cls.family['members']}
 def claim(self,n):return self.assertions['a-jin080-wangxizhi-kin_'+n]
 def test_explicit_and_inferred_parentage_separate(self):
  father,grand=self.claim('001'),self.claim('002')
  xi,kuang,zheng=father['subject_person_id'],father['object_person_id'],grand['object_person_id']
  self.assertEqual(self.rows[xi]['source_assertion_id'],father['id'])
  row=self.rows[kuang];self.assertEqual(row['parent_person_id'],zheng);self.assertIsNone(row['source_assertion_id'])
  self.assertEqual(row['parent_connection']['type'],'parent_between_consecutive_ancestors')
  self.assertEqual(row['parent_connection']['status'],'contextual_provisional')
  self.assertFalse(any(a['predicate']=='father' and a['subject_person_id']==kuang for a in self.assertions.values()))
 def test_unnamed_elder_brother_not_new_source_father(self):
  elder=self.claim('012')['subject_person_id'];row=self.rows[elder]
  self.assertIsNone(row['source_assertion_id']);self.assertEqual(row['parent_connection']['type'],'shared_father_through_sibling')
  self.assertEqual(row['parent_person_id'],self.claim('001')['object_person_id'])
 def test_named_children_and_grandchildren_keep_original_fathers(self):
  for n in ('015','016','017','018','019','025','030'):
   a=self.claim(n);row=self.rows[a['subject_person_id']]
   self.assertEqual(row['parent_person_id'],a['object_person_id']);self.assertEqual(row['source_assertion_id'],a['id'])
 def test_jingzhi_missing_father_remains_missing(self):
  a=self.claim('031');row=self.rows[a['subject_person_id']]
  self.assertIsNone(row['parent_person_id']);self.assertIsNone(row['source_assertion_id']);self.assertEqual(row['intermediate_person_ids'],[None])
  self.assertEqual(row['generation_distance'],2);self.assertEqual(row['ancestor_person_id'],self.claim('019')['object_person_id'])
  self.assertEqual(row['ancestor_connection']['type'],'ancestor_through_paternal_uncle');self.assertIn('*',row['person_id'])
  self.assertIsNone(a['qualifiers']['father_person_id']);self.assertEqual(self.claim('032')['predicate'],'ritual_successor_of')
 def test_source_parentage_not_inflated(self):
  self.assertEqual(self.claim('011')['qualifiers']['role'],'mother_unspecified')
  self.assertIsNone(self.claim('011')['qualifiers']['biological_mother'])
 def test_retirement_receipt_is_not_aliases(self):
  x=read('source-evidence/wangxizhi-family-assembly/annotation-chain.json')
  self.assertEqual(len(x['retired_person_ids']),11);self.assertFalse(x['person_aliases_created'])
  people=read('registry/persons.json')['persons'];retired=set(x['retired_person_ids'])
  self.assertFalse(retired&{p['id'] for p in people});self.assertFalse(retired&{a for p in people for a in p.get('id_aliases',[])})
if __name__=='__main__':unittest.main()
