import unittest,json,copy
from pathlib import Path
import jin064_wudi_family_sources as owner
ROOT=Path(__file__).resolve().parents[1]
class Jin064ExplicitSpouse(unittest.TestCase):
 def fixture(self):
  raw=lambda p:(ROOT/p).read_bytes();return raw,{p['id']:p for p in json.loads(raw('registry/persons.json'))['persons']}
 def setup(self):
  raw,people=self.fixture();c,r,docs=owner._proof(raw,people);path=next(p for p,d in docs.items()if d.get('record_type')=='person_assertion_set');return raw,people,c,r,docs,path
 def test_explicit_spouse_is_same_mother_not_unproved_consities(self):
  raw,people,c,r,docs,path=self.setup();a=next(a for a in docs[path]['assertions']if a['id']=='a-jin064-xia-spouse-zhou');self.assertEqual(a['predicate'],'spouse');self.assertEqual(a['subject_person_id'],r['xia']);self.assertEqual(a['object_person_id'],r['m_zhoufei']);self.assertEqual(a['qualifiers']['source_term'],'康王正妃周氏');self.assertTrue(a['qualifiers']['marriage_date_not_inferred']);self.assertTrue(any(a['predicate']=='mother'and a['subject_person_id']==r['qin']and a['object_person_id']==r['m_zhoufei']for a in docs[path]['assertions']))
 def test_missing_explicit_spouse_rejected(self):
  raw,people,c,r,docs,path=self.setup();bad=copy.deepcopy(docs[path]);bad['assertions']=[a for a in bad['assertions']if a['id']!='a-jin064-xia-spouse-zhou'];b=json.dumps(bad,ensure_ascii=False).encode()
  with self.assertRaises(AssertionError):owner._proof(lambda p:b if p==path else raw(p),people)
 def test_cannot_turn_grandmother_into_spouse(self):
  raw,people,c,r,docs,path=self.setup();bad=copy.deepcopy(docs[path]);next(a for a in bad['assertions']if a['id']=='a-jin064-xia-spouse-zhou')['object_person_id']=r['m_chenmeiren'];b=json.dumps(bad,ensure_ascii=False).encode()
  with self.assertRaises(AssertionError):owner._proof(lambda p:b if p==path else raw(p),people)
 def test_marriage_year_not_inferred_from_era_elsewhere(self):
  raw,people,c,r,docs,path=self.setup();bad=copy.deepcopy(docs[path]);next(a for a in bad['assertions']if a['id']=='a-jin064-xia-spouse-zhou')['qualifiers']['marriage_year']=289;b=json.dumps(bad,ensure_ascii=False).encode()
  with self.assertRaises(AssertionError):owner._proof(lambda p:b if p==path else raw(p),people)
if __name__=='__main__':unittest.main()
