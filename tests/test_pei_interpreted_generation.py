from pathlib import Path
import copy,json,unittest
from unittest.mock import patch
from scripts.person_bundle import load_catalog
from scripts.interpreted_generation_ancestor import valid,TYPE,FACTS,REF
ROOT=Path(__file__).resolve().parents[1]
class PeiInterpretedGenerationTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  _,records=load_catalog(ROOT)
  cls.assertions={a['id']:a for r in records if r.get('record_type')=='person_assertion_set'for a in r['assertions']}
  cls.chapters={r['id']:r for r in records if r.get('record_type')=='marked_chapter'}
  fd=json.loads((ROOT/'registry/family-assemblies.json').read_bytes())
  cls.family=next(a for a in fd['assemblies']if a['id']=='family-hedong-pei-mao-core')
  cls.rows={m['person_id']:m for m in cls.family['members']}
  cls.member=next(m for m in cls.family['members']if m.get('ancestor_connection',{}).get('type')==TYPE)
 def check(self,member=None,assertions=None):
  return valid(member or self.member,self.rows,assertions or self.assertions,self.chapters,ROOT,self.family)
 def test_received_eight_and_qualified_seven_are_distinct(self):
  raw=copy.deepcopy(self.assertions[FACTS[0]])
  self.assertTrue(self.check());self.assertEqual(raw['qualifiers']['reported_generation_number'],8)
  self.assertIsNone(raw['qualifiers']['generation_distance']);self.assertIs(raw['qualifiers']['adopted_for_family_tree'],False)
  self.assertIsNone(self.member['parent_person_id']);self.assertEqual(self.member['intermediate_person_ids'],[None])
  self.assertEqual(raw,self.assertions[FACTS[0]])
 def test_fabricated_parent_and_wrong_ancestor_are_rejected(self):
  for field,value in [('parent_person_id',self.member['ancestor_person_id']),('ancestor_person_id',self.member['person_id']),('generation_distance',3)]:
   with self.subTest(field=field):
    m=copy.deepcopy(self.member);m[field]=value;self.assertFalse(self.check(member=m))
 def test_editorial_summary_cannot_be_silently_changed(self):
  m=copy.deepcopy(self.member);m['ancestor_connection']['generation_interpretation']['preferred_generation_distance']=8
  self.assertFalse(self.check(member=m))
 def test_raw_qualifiers_cannot_be_replaced_by_interpretation(self):
  for field,value in [('reported_generation_number',7),('generation_distance',7),('adopted_for_family_tree',True)]:
   with self.subTest(field=field):
    aa=dict(self.assertions);aa[FACTS[0]]=copy.deepcopy(aa[FACTS[0]]);aa[FACTS[0]]['qualifiers'][field]=value
    self.assertFalse(self.check(assertions=aa))
 def test_new_explicit_parent_requires_review_of_missing_slot(self):
  aa=dict(self.assertions);aa['test-explicit-source-parent']=dict(predicate='father',subject_person_id=self.member['person_id'],object_person_id=self.member['ancestor_person_id'])
  self.assertFalse(self.check(assertions=aa))
 def test_decision_alternatives_and_review_status_are_guarded(self):
  path=ROOT/REF;original=Path.read_bytes;decision=json.loads(original(path))
  for key,value in [('preferred_generation_distance',8),('alternatives',[]),('human_reviewed',True)]:
   with self.subTest(key=key):
    changed=copy.deepcopy(decision);changed[key]=value;data=json.dumps(changed).encode()
    with patch.object(Path,'read_bytes',lambda p:data if p==path else original(p)):self.assertFalse(self.check())
if __name__=='__main__':unittest.main()
