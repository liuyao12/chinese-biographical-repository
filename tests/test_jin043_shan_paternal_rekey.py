"""Actual current source-derived father paths, retirement, and qualified captures."""
import json,copy,unittest,hashlib
from pathlib import Path
from unittest.mock import patch
from scripts.person_bundle import load_catalog,bundle
from scripts.family_assemblies import load_assemblies
from scripts import fixed_wuyingdian_jin043_shantao as g
from scripts.retired_person_ids import retired_person_ids,assert_not_retired
from scripts.person_ids import allocate_person_id,valid_person_id
ROOT=Path(__file__).resolve().parents[1]
BASE='source-evidence/jin043-shan-paternal-family/'
ROLES=('shanyao','shantao','shangai','shanchun','shanyun','shanmo','shanjian','shanwei','shanshihui','shanya')
class ShanRekeyTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.people,cls.records=load_catalog(ROOT);cls.chapter=next(r for r in cls.records if r.get('id')==g.CID);cls.roles,_=g.formal_state(cls.chapter,ROOT,cls.people,cls.records)
 def test_real_ten_member_assembly_and_nine_father_paths(self):
  source,assembled=load_assemblies(ROOT,(self.people,self.records));root=self.roles['shanyao'];nodes={self.roles[r]for r in ROLES};self.assertEqual({p for p,v in assembled.items()if v['root_person_id']==root},nodes)
  assertions={a['id']:a for r in self.records if r.get('record_type')=='person_assertion_set'for a in r['assertions']}
  for pid in nodes-{root}:
   row=source[pid];path=self.people[pid]['family_path'];a=assertions[path['source_assertion_id']];self.assertEqual(row['parent_person_id'],path['parent_person_id']);self.assertEqual((a['subject_person_id'],a['object_person_id'],a['predicate']),(pid,path['parent_person_id'],'father'));self.assertFalse(path['human_reviewed'])
 def test_wrong_parent_endpoint_rejected(self):
  records=copy.deepcopy(list(self.records));pid=self.roles['shanya'];parent=self.roles['shangai']
  for r in records:
   if r.get('record_type')=='person_assertion_set':
    for a in r['assertions']:
     if a['id']=='a-jin043-wyd-shantao-xia-father-jian':a['object_person_id']=parent
  with self.assertRaises(ValueError):load_assemblies(ROOT,(self.people,records))
 def test_retired_queries_and_parser_reserve_all_nine(self):
  receipt=json.loads((ROOT/(BASE+'annotation-chain.json')).read_text());retired=retired_person_ids(ROOT);self.assertEqual(len(receipt['retired_person_ids']),9)
  for pid in receipt['retired_person_ids']:
   self.assertIn(pid,retired);self.assertNotIn(pid,self.people)
   with self.assertRaises(ValueError):assert_not_retired(pid,ROOT)
   for provisional in (False,True):
    with self.assertRaises(ValueError):bundle(pid,ROOT,include_provisional=provisional,catalog=(self.people,self.records))
 def test_normal_allocator_skips_old_root(self):
  old=next(pid for pid in json.loads((ROOT/(BASE+'annotation-chain.json')).read_text())['retired_person_ids']if len(pid)==11);fresh='z5x_9q2_v8n';self.assertNotIn(fresh,self.people);self.assertNotIn(fresh,retired_person_ids(ROOT));tokens=iter(old.replace('_','')+fresh.replace('_',''))
  with patch('scripts.person_ids.secrets.choice',side_effect=lambda _:next(tokens)):self.assertEqual(allocate_person_id(self.people,root=ROOT),fresh)
 def test_historical_exact_hash_and_pointer_only(self):
  q=json.loads((ROOT/(BASE+'historical-reference-qualification.json')).read_text());self.assertEqual(len(q['records']),15)
  for r in q['records']:
   data=(ROOT/r['path']).read_bytes();self.assertEqual(hashlib.sha256(data).hexdigest(),r['sha256']);obj=json.loads(data)
   for hit in r['protected_json_pointers']:
    value=obj
    for k in hit['pointer'].strip('/').split('/'):value=value[int(k)]if isinstance(value,list)else value[k.replace('~1','/').replace('~0','~')]
    self.assertEqual(value,hit['value'])
 def test_grandchild_and_root_navigation_data(self):
  for role in ('shanyao','shangai','shanjian','shanya'):
   for policy in (False,True):
    b=bundle(self.roles[role],ROOT,include_provisional=policy,catalog=(self.people,self.records));self.assertEqual(b['canonical_person_id'],self.roles[role]);self.assertFalse(b['id_aliases'])
  b=bundle(self.roles['shanyao'],ROOT,catalog=(self.people,self.records));self.assertTrue(any(a['subject_person_id']==self.roles['shantao']and a['object_person_id']==self.roles['shanyao']and a['predicate']=='father'for a in b['preferred_relations']))
if __name__=='__main__':unittest.main()
