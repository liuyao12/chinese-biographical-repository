"""王雄近系：明父證、旁系角色及退號後引用保全。"""
from pathlib import Path
import json,unittest,copy
from scripts.person_bundle import load_catalog,bundle
from scripts.family_assemblies import load_assemblies
from scripts.retired_person_ids import retired_person_ids,allocation_conflicts
R=Path(__file__).resolve().parents[1]
J=lambda p:json.loads((R/p).read_text())
class WangXiongFamily(unittest.TestCase):
 @classmethod
 def setUpClass(c):
  c.cat=load_catalog(R);c.sm,c.rows=load_assemblies(R,c.cat);c.f=next(a for a in J('registry/family-assemblies.json')['assemblies'] if a['id']=='family-langye-wang-xiong-core');c.m={r['person_id']:r for r in c.f['members']};c.a={a['id']:a for r in c.cat[1] for a in r.get('assertions',[])}
 def test_original_nine_and_reviewed_three_children_have_source_fathers(self):
  self.assertEqual(len(self.m),14);self.assertFalse(self.f['human_reviewed']);expected_core={'ehx_cqg_nfx'+tail for tail in ['', '_A','_B','_AA','_BA','_BB','_AAA','_AAB','_AAC']};self.assertTrue(expected_core<=set(self.m));ch=J('corpus/jinshu/043-wangyan.json');extra={m['person_id']for p in ch['paragraphs']for m in p['mentions']if m['id']in ['c-jinshu-043-wangyan:p010:m0001','c-jinshu-043-wangyan:p003:m0254','c-jinshu-043-wangyan:p005:m0015']};wc=J('corpus/jinshu/043-wangcheng.json');extra|={m['person_id']for p in wc['paragraphs']for m in p['mentions']if m['id']in ['c-jinshu-043-wangcheng:p007:m0260','c-jinshu-043-wangcheng:p007:m0267']};self.assertEqual(set(self.m),expected_core|extra)
  for pid,row in self.m.items():
   if row['parent_person_id'] is None:self.assertEqual(pid,self.f['root_person_id']);continue
   a=self.a[row['source_assertion_id']];self.assertEqual(a['predicate'],'father');self.assertEqual((a['subject_person_id'],a['object_person_id']),(pid,row['parent_person_id']))
 def test_existing_parent_and_ritual_roles_are_not_converted(self):
  a=self.a['a-jin043-wangrong-006'];r=self.a['a-jin043-wangrong-007'];self.assertEqual(a['predicate'],'father');self.assertEqual(r['predicate'],'ritual_successor_of');self.assertEqual(a['subject_person_id'],r['subject_person_id']);self.assertNotIn(a['subject_person_id'],self.m)
 def test_spouse_and_mother_claims_preserved(self):
  self.assertEqual(self.a['a-sgz026-guohuai-family-008']['predicate'],'spouse')
  self.assertEqual(self.a['a-jin043-wangrong-010']['predicate'],'spouse')
  self.assertFalse(any(a['predicate']=='mother' and a['subject_person_id'] in self.m for a in self.a.values() if a['id'].startswith('a-jin043-wangrong')))
 def test_retired_ids_reject_lookup_and_allocation(self):
  mapping=J('source-evidence/wangxiong-family-assembly/annotation-chain.json')['person_id_mapping'];self.assertEqual(len(mapping),8)
  for old,new in mapping.items():
   self.assertNotIn(old,self.cat[0]);self.assertIn(new,self.m);self.assertIn(old,retired_person_ids(R));self.assertTrue(allocation_conflicts(old,retired_person_ids(R)))
   with self.assertRaises((KeyError,ValueError)):bundle(old,root=R,catalog=self.cat,include_provisional=True)
   for folder in ('exports/persons','data/corpus/profiles'):self.assertFalse((R/folder/(old+'.json')).exists())
 def test_ordinal_not_encoded_by_structural_letters(self):
  a=next(a for a in self.a.values() if a['id']=='a-sgz024-cuilin-yi-father-xiong');self.assertEqual(a['qualifiers']['birth_order']['ordinal'],2)

 def bad_family(self,mutate):
  from unittest.mock import patch
  d=J('registry/family-assemblies.json');f=next(x for x in d['assemblies']if x['id']==self.f['id']);mutate(f);original=Path.read_text;target=R/'registry/family-assemblies.json'
  def read(path,*a,**kw):return json.dumps(d) if path==target else original(path,*a,**kw)
  with patch.object(Path,'read_text',read):
   with self.assertRaises((ValueError,KeyError)):load_assemblies(R,self.cat)
 def test_reversed_father_endpoint_rejected(self):
  self.bad_family(lambda f:f['members'][1].update(parent_person_id=f['members'][2]['person_id']))
 def test_same_person_cycle_rejected(self):
  self.bad_family(lambda f:f['members'][1].update(parent_person_id=f['members'][1]['person_id']))
 def test_another_person_source_assertion_rejected(self):
  self.bad_family(lambda f:f['members'][1].update(source_assertion_id=f['members'][2]['source_assertion_id']))
 def test_ritual_successor_cannot_replace_father(self):
  self.bad_family(lambda f:f['members'][1].update(source_assertion_id='a-jin043-wangrong-007'))
