"""Complete bounded WYD043 roles, literal names and documented near-family."""
import copy,json,unittest
from pathlib import Path
from scripts import fixed_wuyingdian_jin043_shantao as g
from scripts.person_bundle import load_catalog,bundle
ROOT=Path(__file__).resolve().parents[1]
class ShantaoNERTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.people,cls.records=load_catalog(ROOT);cls.chapter=next(r for r in cls.records if r.get('id')==g.CID)
 def test_complete_native_and_pending_predecessor(self):
  roles,ct=g.formal_state(self.chapter,ROOT,self.people,self.records);self.assertEqual(len(roles),59)
  self.assertEqual(sum(m['kind']=='person'for p in self.chapter['paragraphs']for m in p['mentions']),251)
  pending=copy.deepcopy(self.chapter);pending['annotation']=json.loads(g.fixed(ROOT,'transcription-witness-contract.json'))['required_annotation']
  for p in pending['paragraphs']:p['mentions']=[];p['annotation_status']='pending'
  self.assertTrue(g.validate_source(pending,ROOT))
 def test_wrong_owner_character_book_and_qualification_rejected(self):
  for kind in ('owner','character','book','human'):
   c=copy.deepcopy(self.chapter)
   if kind=='owner':c['paragraphs'][0]['mentions'][0]['person_id']='not-a-person'
   if kind=='character':c['paragraphs'][0]['text']+='字'
   if kind=='book':next(m for m in c['paragraphs'][12]['mentions']if m['kind']=='work').update(start=2,end=3,surface='書')
   if kind=='human':c['annotation']['human_reviewed']=0
   with self.subTest(kind=kind),self.assertRaises(ValueError):g.formal_state(c,ROOT,self.people)
 def test_reverse_one_end_and_stale_catalog_rejected(self):
  people=copy.deepcopy(self.people);mid=self.chapter['paragraphs'][0]['mentions'][0]['id'];pid=self.chapter['paragraphs'][0]['mentions'][0]['person_id'];people[pid]['evidence']=[e for e in people[pid]['evidence']if e.get('mention_id')!=mid]
  with self.assertRaises(ValueError):g.formal_state(self.chapter,ROOT,people)
  records=list(self.records);i=next(i for i,r in enumerate(records)if r.get('id')==g.CID);c=copy.deepcopy(records[i]);c['paragraphs'][0]['mentions'][0]['surface']='錯';records[i]=c
  with self.assertRaises(ValueError):g.guard_bundle(ROOT,pid,self.people,records)
 def test_missing_or_downgraded_catalog_chapter_rejected(self):
  pid=self.chapter['paragraphs'][0]['mentions'][0]['person_id'];missing=[r for r in self.records if r.get('id')!=g.CID]
  with self.assertRaises(ValueError):g.guard_bundle(ROOT,pid,self.people,missing)
  pending=copy.deepcopy(self.chapter);pending['annotation']=json.loads(g.fixed(ROOT,'transcription-witness-contract.json'))['required_annotation']
  for p in pending['paragraphs']:p['mentions']=[];p['annotation_status']='pending'
  downgraded=[pending if r.get('id')==g.CID else r for r in self.records]
  with self.assertRaises(ValueError):g.guard_bundle(ROOT,pid,self.people,downgraded)
 def test_literal_names_cross_page_father_and_no_invented_anchor(self):
  roles,ct=g.formal_state(self.chapter,ROOT,self.people,self.records);assertions=g.substitute(ct['sidecars']['corpus/jinshu/043-wyd1739-shantao-assertions.json']['assertions'],roles);names=g.substitute(ct['sidecars']['corpus/jinshu/043-wyd1739-shantao-names.json']['records'],roles)
  row=next(n for n in names if n['id']=='name-jin043-wyd-shanya-restored');self.assertEqual(row['surname'],'山');self.assertTrue(g.validate_surname(row,names,{g.CID:self.chapter},assertions,ROOT))
  father=next(a for a in assertions if a['id'].endswith('xia-father-jian'));self.assertEqual(father['context']['paragraph_ids'],[g.CID+':p015',g.CID+':p016']);self.assertFalse(any(m.get('person_id')==roles['shanjian']for m in self.chapter['paragraphs'][15]['mentions']));self.assertIsNone(next(n for n in names if n['id']=='name-jin043-wyd-shanya-literal')['surname'])
 def test_real_three_bundles_both_policies(self):
  roles,_=g.formal_state(self.chapter,ROOT,self.people,self.records)
  for role in ('shantao','shanjian','shanya'):
   for policy in (False,True):
    with self.subTest(role=role,policy=policy):self.assertEqual(bundle(roles[role],ROOT,include_provisional=policy,catalog=(self.people,self.records))['canonical_person_id'],roles[role])
 def test_strict_json_and_old_bad_types(self):
  for a,b in [(True,1),(False,0),((1,),(1,)),([1],(1,)),(float('nan'),float('nan')),({1:'a'},{1:'a'})]:self.assertFalse(g.same(a,b))
  for value in (None,[],'bad'):
   with self.subTest(value=value),self.assertRaises(ValueError):g.validate_source(value,ROOT)
if __name__=='__main__':unittest.main()
