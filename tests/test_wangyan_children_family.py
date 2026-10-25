from pathlib import Path
import json,copy,unittest
from scripts.person_bundle import load_catalog,bundle
from scripts.family_assemblies import load_assemblies
from scripts.retired_person_ids import retired_person_ids,allocation_conflicts
R=Path(__file__).resolve().parents[1];J=lambda p:json.loads((R/p).read_text())
class WangYanChildrenFamily(unittest.TestCase):
 @classmethod
 def setUpClass(c):
  c.cat=load_catalog(R);c.sm,c.rows=load_assemblies(R,c.cat);c.ch=J('corpus/jinshu/043-wangyan.json');c.m={m['id']:m for p in c.ch['paragraphs']for m in p['mentions']};c.father=c.m['c-jinshu-043-wangyan:p001:m0000']['person_id'];c.kids={c.m[mid]['person_id']for mid in ['c-jinshu-043-wangyan:p010:m0001','c-jinshu-043-wangyan:p003:m0254','c-jinshu-043-wangyan:p005:m0015']};c.f=next(a for a in J('registry/family-assemblies.json')['assemblies']if a['id']=='family-langye-wang-xiong-core')
 def test_physical_registry_unique_and_relocation_not_merge(self):
  raw=J('registry/persons.json')['persons'];ids=[p['id']for p in raw];self.assertEqual(len(ids),len(set(ids)));proof=J('source-evidence/wangyan-children-family/rekey-fidelity.json')['registry_physical_list'];self.assertEqual(proof['before_rows'],proof['after_rows']);self.assertEqual(proof['before_unique'],proof['after_unique']);self.assertTrue(proof['exact']);self.assertTrue(self.kids<=set(ids))
 def test_source_fathers_not_new_inferred_parents(self):
  aa=J('corpus/jinshu/043-wangyan-assertions.json')['assertions'];ids={'a-jin043-wangyan-xuan-father-yan','a-jin043-wangyan-youngson-father-yan','a-jin043-wangyan-daughter-father-yan'};rows=[a for a in aa if a['id']in ids];self.assertEqual(len(rows),3);self.assertEqual({a['subject_person_id']for a in rows},self.kids)
  for a in rows:self.assertEqual((a['predicate'],a['object_person_id']),('father',self.father));self.assertEqual(self.rows[a['subject_person_id']]['source_assertion_id'],a['id'])
 def test_three_children_have_same_source_and_assembly_father(self):
  self.assertEqual(len(self.f['members']),14)
  for pid in self.kids:self.assertEqual(self.rows[pid]['parent_person_id'],self.father);self.assertEqual(self.rows[pid]['root_person_id'],self.f['root_person_id'])
 def test_mother_and_absolute_order_not_invented(self):
  for rec in self.cat[1]:
   for a in rec.get('assertions',[]):
    if a.get('subject_person_id')in self.kids:self.assertNotIn(a.get('predicate'),['mother','maternal_role']);self.assertNotIn('birth_order',a.get('qualifiers',{}))
 def test_existing_spouse_and_xuan_office_remain(self):
  aa=J('corpus/jinshu/043-wangyan-assertions.json')['assertions'];daughter=self.m['c-jinshu-043-wangyan:p005:m0015']['person_id'];prince=self.m['c-jinshu-043-wangyan:p005:m0017']['person_id'];a=next(a for a in aa if a['id']=='a-jin043-wangyan-daughter-prince-marriage');self.assertEqual((a['subject_person_id'],a['object_person_id']),(daughter,prince));xuan=self.m['c-jinshu-043-wangyan:p010:m0001']['person_id'];h=next(h for h in J('corpus/jinshu/043-wangyan-titles.json')['holdings']if h['id']=='th-jin043-wangyan-career_33');self.assertEqual((h['person_id'],h['title'],h['mode']),(xuan,'陳留太守','grant'));self.assertIsNone(h['effective_period']['start']['date_expression'])
 def test_identity_source_pair_not_reinferred_by_family_ids(self):
  c=J('corpus/jinshu/035-pei-family.json');m=next(m for p in c['paragraphs']for m in p['mentions']if m['id']=='c-jinshu-035-peikai-family:p019:m0061');self.assertEqual(m['person_id'],self.m['c-jinshu-043-wangyan:p010:m0001']['person_id']);self.assertIn('duy_kcy_44o',retired_person_ids(R));self.assertNotIn('duy_kcy_44o',self.cat[0])
 def test_retired_child_roots_not_alias_queries_or_allocatable(self):
  receipt=J('source-evidence/wangyan-children-family/annotation-chain.json');self.assertEqual(len(receipt['retired_person_ids']),5);self.assertFalse(receipt['person_aliases_created'])
  for old in receipt['retired_person_ids']:
   self.assertNotIn(old,self.cat[0]);self.assertTrue(allocation_conflicts(old,retired_person_ids(R)))
   with self.assertRaises((KeyError,ValueError)):bundle(old,root=R,catalog=self.cat,include_provisional=True)
   for folder in('exports/persons','data/corpus/profiles'):self.assertFalse((R/folder/(old+'.json')).exists())

 def test_cheng_two_sons_exact_source_roles_and_independent_ordinals(self):
  ch=J('corpus/jinshu/043-wangcheng.json');marks={m['id']:m for p in ch['paragraphs']for m in p['mentions']};father=marks['c-jinshu-043-wangcheng:p001:m0000']['person_id'];aa=J('corpus/jinshu/043-wangcheng-assertions.json')['assertions']
  for mid,aid,n in [('c-jinshu-043-wangcheng:p007:m0260','a-jin043-wangcheng-zhan-father',1),('c-jinshu-043-wangcheng:p007:m0267','a-jin043-wangcheng-hui-father',2)]:
   child=marks[mid]['person_id'];a=next(x for x in aa if x['id']==aid);self.assertEqual((a['subject_person_id'],a['predicate'],a['object_person_id']),(child,'father',father));self.assertEqual(a['qualifiers']['birth_order']['ordinal'],n);self.assertEqual(a['qualifiers']['birth_order']['scope'],'sons_of_parent');self.assertEqual(self.rows[child]['parent_person_id'],father);self.assertEqual(self.rows[child]['source_assertion_id'],aid)
 def test_cheng_sons_no_inferred_surname_or_mother(self):
  names=J('corpus/jinshu/043-wangcheng-name-components.json')['records']
  for n in names:
   if n['id']in ['nc-jin043-wangcheng-zhan','nc-jin043-wangcheng-hui']:self.assertIsNone(n['surname'])
