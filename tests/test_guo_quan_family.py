import unittest,json,copy
from pathlib import Path
from scripts.person_bundle import load_catalog,bundle
from scripts.family_assemblies import load_assemblies
from scripts.received_kin_assembly import valid
from scripts.retired_person_ids import retired_person_ids,allocation_conflicts
R=Path(__file__).resolve().parents[1]
OLD=['ozn_wl2_nrm','d7u_f1n_let','vji_mqe_2dj','d2s_53o_65p','8bq_8u2_yd8','28k_44w_ibb','64e_ce8_aba','1cz_c76_jxs','tiq_tug_olu']
class GuoFamilyTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.catalog=load_catalog(R);cls.people,records=cls.catalog;cls.chapters={c['id']:c for c in records if c.get('record_type')=='marked_chapter'};cls.assertions={a['id']:a for c in records if c.get('record_type')=='person_assertion_set'for a in c['assertions']};cls.family=next(x for x in json.loads((R/'registry/family-assemblies.json').read_text())['assemblies']if x['id']=='family-guo-quan-close');cls.rows={x['person_id']:x for x in cls.family['members']}
 def check_row(self,suffix,mutate):
  rows=copy.deepcopy(self.rows);aa=copy.deepcopy(self.assertions);row=rows['r02_hoi_pu7'+suffix];mutate(row,rows,aa);return valid(row,rows,aa,self.chapters,R)
 def test_all_members_and_full_loader(self):
  sm,am=load_assemblies(R,self.catalog);self.assertEqual(len(self.rows),10)
  for pid,row in self.rows.items():self.assertEqual(am[pid]['parent_person_id'],row['parent_person_id'])
  for suffix in ['_A','_AB','_AC','_ABB']:self.assertTrue(self.check_row(suffix,lambda *a:None))
 def test_ancestor_does_not_become_source_father(self):
  a=self.assertions['a-sgz026-guohuai-family-002'];self.assertEqual(a['predicate'],'grandfather');self.assertEqual(a['object_person_id'],'r02_hoi_pu7')
  self.assertFalse(any(a['predicate']=='father'and a['subject_person_id']=='r02_hoi_pu7_A'for a in self.assertions.values()))
 def test_ancestor_wrong_role_and_swapped_proof_rejected(self):
  self.assertFalse(self.check_row('_A',lambda row,rows,aa:row['parent_connection'].update(nearer_ancestor_assertion_id='a-sgz026-guohuai-family-002')))
  self.assertFalse(self.check_row('_A',lambda row,rows,aa:aa['a-sgz026-guohuai-family-001'].update(subject_person_id='r02_hoi_pu7_AB')))
 def test_ancestor_maternal_and_changed_fixed_quote_rejected(self):
  self.assertFalse(self.check_row('_A',lambda row,rows,aa:aa['a-sgz026-guohuai-family-002']['qualifiers'].update(lineage='maternal')))
  self.assertFalse(self.check_row('_A',lambda row,rows,aa:aa['a-sgz026-guohuai-family-002']['evidence'][0].update(quote='祖全父緼')))
 def test_shared_father_no_mother_or_adoption(self):
  for key,value in [('adoptive',True),('sworn',True),('same_mother_only',True),('shared_father',False),('lineage','maternal')]:
   with self.subTest(key=key):self.assertFalse(self.check_row('_AB',lambda row,rows,aa:aa['a-sgz026-guohuai-family-006']['qualifiers'].update({key:value})))
 def test_chain_cycle_missing_edge_wrong_parent_rejected(self):
  self.assertFalse(self.check_row('_AC',lambda row,rows,aa:row['parent_connection'].update(sibling_person_ids=['r02_hoi_pu7_AC','r02_hoi_pu7_AA'])))
  self.assertFalse(self.check_row('_AC',lambda row,rows,aa:row['parent_connection'].update(sibling_assertion_ids=['a-sgz026-guohuai-family-007'])))
  self.assertFalse(self.check_row('_AC',lambda row,rows,aa:rows['r02_hoi_pu7_AB'].update(parent_person_id='r02_hoi_pu7')))
 def test_father_contradiction_and_sister_not_brother(self):
  def wrong(row,rows,aa):
   a=copy.deepcopy(aa['a-sgz026-guohuai-family-001']);a.update(id='contradiction',subject_person_id=row['person_id'],object_person_id='r02_hoi_pu7');aa[a['id']]=a
  self.assertFalse(self.check_row('_ABB',wrong))
  self.assertFalse(self.check_row('_ABB',lambda row,rows,aa:aa['a-sgz026-guohuai-family-010'].update(predicate='sister')))
 def test_wrong_reference_source_and_url_rejected(self):
  self.assertFalse(self.check_row('_A',lambda row,rows,aa:row['parent_connection']['references'][0].update(source_id='wrong')))
  self.assertFalse(self.check_row('_A',lambda row,rows,aa:row['parent_connection']['references'][0].update(url='https://example.invalid/')))
 def test_old_ids_permanent_no_alias_no_current_json(self):
  retired=retired_person_ids(R)
  for old in OLD:
   self.assertIn(old,retired);self.assertTrue(allocation_conflicts(old,retired));self.assertTrue(allocation_conflicts(old+'_A',retired));self.assertNotIn(old,self.people)
   with self.assertRaises(ValueError):bundle(old,R,catalog=self.catalog)
   for prefix in ['exports/persons','data/corpus/profiles']:self.assertFalse((R/prefix/(old+'.json')).exists())
  self.assertFalse(any(old in p.get('id_aliases',[])for p in self.people.values()for old in OLD))
 def test_wives_and_sister_not_assigned_paternal_branch(self):
  for pid in ['foz_lt0_au5','4rl_6u1_b3j']:self.assertNotIn(pid,self.rows)
  sister=[a for a in self.assertions.values()if a['predicate']=='sister'and(a['subject_person_id']=='r02_hoi_pu7_ACA'or a['object_person_id']=='r02_hoi_pu7_ACA')]
  self.assertTrue(sister)
  for a in sister:
   pid=a['object_person_id']if a['subject_person_id']=='r02_hoi_pu7_ACA'else a['subject_person_id'];self.assertNotIn(pid,self.rows)
 def test_source_assertion_ids_and_count_preserved(self):
  aa=json.loads((R/'corpus/sanguozhi/026-guohuai-assertions.json').read_text())['assertions'];self.assertEqual(len(aa),14)
  self.assertEqual({a['id']for a in aa},{'a-sgz026-guohuai-family-'+str(i).zfill(3)for i in range(1,15)})
if __name__=='__main__':unittest.main()
