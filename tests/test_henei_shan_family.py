# -*- coding: utf-8 -*-
import json,unittest
from pathlib import Path
from scripts.person_bundle import load_catalog,bundle
from scripts.family_assemblies import load_assemblies
from scripts.retired_person_ids import retired_person_ids
from scripts.person_ids import allocate_child_id
R=Path(__file__).resolve().parents[1]
class HeneiShanFamily(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.catalog=load_catalog(R);cls.people=cls.catalog[0];cls.sm,cls.allmembers=load_assemblies(R,cls.catalog);cls.family=next(f for f in json.loads((R/'registry/family-assemblies.json').read_text())['assemblies']if f['id']=='family-henei-shan-yao');cls.members={m['person_id']:m for m in cls.family['members']};cls.ch=json.loads((R/'corpus/jinshu/043-shantao.json').read_text());cls.paras={p['id']:p for p in cls.ch['paragraphs']};cls.aa=json.loads((R/'corpus/jinshu/043-shantao-assertions.json').read_text())['assertions']
 @classmethod
 def person(cls,n,s):return next(m['person_id']for m in cls.paras[cls.ch['id']+':p'+str(n).zfill(3)]['mentions']if m['surface']==s)
 def test_earliest_explicit_father_is_root_not_a_remote_ancestor(self):
  root=self.person(1,'曜');self.assertEqual(root,self.family['root_person_id']);self.assertEqual(self.members[root]['parent_person_id'],None);self.assertEqual(self.members[root]['source_assertion_id'],None);self.assertEqual(len(self.members),10)
  self.assertEqual(self.members[self.person(1,'山濤')]['parent_person_id'],root)
 def test_every_direct_path_binds_current_source_father(self):
  claims={a['id']:a for a in self.aa}
  for pid,m in self.members.items():
   self.assertEqual(m['source_person_ids'],[pid]);self.assertEqual(m['representative_source_person_id'],pid)
   if m['source_assertion_id']is None:continue
   a=claims[m['source_assertion_id']];self.assertEqual(a['predicate'],'father');self.assertEqual(a['subject_person_id'],pid);self.assertEqual(a['object_person_id'],m['parent_person_id']);self.assertEqual(a['status'],'source_attested');self.assertFalse(a['human_reviewed']);self.assertEqual(self.people[pid]['family_path']['source_assertion_id'],a['id'])
 def test_five_names_do_not_create_five_ordinals(self):
  sons=[self.person(16,s)for s in ['該','淳','允','謨','簡']];tao=self.person(1,'山濤')
  self.assertTrue(all(self.members[p]['parent_person_id']==tao for p in sons))
  for a in self.aa:
   if a['subject_person_id']in sons and a['predicate']=='father':self.assertNotIn('birth_order',a['qualifiers'])
  a=next(a for a in self.aa if a['subject_person_id']==self.person(17,'世回')and a['predicate']=='father');self.assertEqual(a['qualifiers']['birth_order']['ordinal'],2);self.assertEqual(a['qualifiers']['birth_order']['parent_person_id'],self.person(16,'該'))
 def test_mother_wife_cousin_and_sima_are_not_joined(self):
  for a in self.aa:
   if a['predicate']=='maternal_role':
    self.assertNotIn(a['object_person_id'],self.members);self.assertIsNone(a['qualifiers']['biological_mother'])
   if a['predicate']in ['spouse','agnatic_cousin','kinship_unspecified','ritual_successor_of','brother']:
    if a['predicate']=='spouse':self.assertFalse({a['subject_person_id'],a['object_person_id']}<=set(self.members))
    else:self.assertFalse({a['subject_person_id'],a['object_person_id']}<=set(self.members))
 def test_retirement_is_not_an_alias_and_allocator_reserves_branches(self):
  receipt=json.loads((R/'source-evidence/shan-family-assembly/annotation-chain.json').read_text());old=receipt['retired_person_ids'];self.assertEqual(len(old),9);self.assertFalse(receipt['person_aliases_created']);self.assertTrue(set(old)<=retired_person_ids(R));self.assertFalse(set(old)&set(self.people));self.assertFalse(set(old)&{a for p in self.people.values()for a in p.get('id_aliases',[])})
  for pid in old:
   with self.assertRaises((KeyError,ValueError)):bundle(pid,root=R,catalog=self.catalog)
   with self.assertRaises(ValueError):allocate_child_id(pid,set(),root=R)
if __name__=='__main__':unittest.main()
