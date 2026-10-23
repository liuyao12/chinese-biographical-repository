import json,unittest
from pathlib import Path
from scripts.person_ids import allocate_child_id
from scripts.retired_person_ids import retired_person_ids,allocation_conflicts,assert_not_retired
from scripts.person_bundle import load_catalog,bundle
R=Path(__file__).resolve().parents[1];OLD=['ag3_nfx_i0f','2td_ovt_6j2'];NEW=['a8f_ec8_e74_AC','344_68f_98e_A']
class TwoSons(unittest.TestCase):
 def test_old_ids_absent_and_retired_not_aliases_or_reusable(self):
  people={p['id']:p for p in json.loads((R/'registry/persons.json').read_text())['persons']};retired=retired_person_ids(R)
  for old,new in zip(OLD,NEW):
   self.assertNotIn(old,people);self.assertIn(new,people);self.assertIn(old,retired);self.assertTrue(allocation_conflicts(old,retired));self.assertTrue(allocation_conflicts(old+'_A',retired));self.assertFalse(people[new].get('id_aliases'))
   with self.assertRaises(ValueError):assert_not_retired(old,R)
 def test_exact_father_assertions_and_family_members(self):
  families=json.loads((R/'registry/family-assemblies.json').read_text())['assemblies'];a=json.loads((R/'corpus/sanguozhi/027-wangchang-assertions.json').read_text())['assertions']
  for pid,parent,seq in [(NEW[0],'a8f_ec8_e74_A','011'),(NEW[1],'344_68f_98e','012')]:
   member=next(m for f in families for m in f['members']if m['person_id']==pid);self.assertEqual(member['parent_person_id'],parent);self.assertEqual(member['connection'],'father');assertion=next(x for x in a if x['id']=='a-sanguozhi027-wangchang-'+seq);self.assertEqual(assertion['subject_person_id'],pid);self.assertEqual(assertion['object_person_id'],parent)
 def test_bundles_both_ends_and_no_unknown_father_invention(self):
  cat=load_catalog(R)
  for pid,parent in [(NEW[0],'a8f_ec8_e74_A'),(NEW[1],'344_68f_98e')]:
   for endpoint in [pid,parent]:self.assertTrue(any(x['predicate']=='father'and x['subject_person_id']==pid and x['object_person_id']==parent for x in bundle(endpoint,root=R,catalog=cat)['relations']))
  self.assertNotIn('family_path',cat[0]['0oh_iwa_lu9']);self.assertFalse(any(x['predicate']=='father'and x['subject_person_id']=='0oh_iwa_lu9'for x in bundle('0oh_iwa_lu9',root=R,catalog=cat)['relations']))
 def test_current_native_endpoints_have_no_retired_ids(self):
  for area in ['corpus','registry','sources']:
   for f in (R/area).rglob('*.json'):
    s=f.read_text()
    for old in OLD:self.assertNotIn(old,s,str(f))
  for f in (R/'source-evidence').rglob('*.json'):
   if 'wangchang-two-sons-family-rekey'in str(f):continue
   for old in OLD:self.assertNotIn(old,f.read_text(),str(f))
 def test_current_allocator_does_not_reuse_new_or_retired_branch(self):
  ids={p['id']for p in json.loads((R/'registry/persons.json').read_text())['persons']}
  self.assertNotEqual(allocate_child_id('a8f_ec8_e74_A',ids,root=R),NEW[0]);self.assertNotEqual(allocate_child_id('344_68f_98e',ids,root=R),NEW[1])
if __name__=='__main__':unittest.main()
