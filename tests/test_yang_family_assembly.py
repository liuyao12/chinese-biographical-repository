# coding:utf-8
from pathlib import Path
import json,sys,copy,unittest
I=Path(__file__).resolve().parents[1]
from scripts.uncle_shared_grandparent import valid
class Semantic(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.ch=json.loads((I/'corpus/jinshu/034-yanghu.json').read_bytes());cls.aa={a['id']:a for a in json.loads((I/'corpus/jinshu/034-yanghu-assertions.json').read_bytes())['assertions']};cls.cids={cls.ch['id']:cls.ch};cls.p='a-jin034-yanghu-'
 def state(self,which='mi'):
  aa=copy.deepcopy(self.aa);u=aa[self.p+'paternal-uncle-'+which];f=aa[self.p+'father'];g=aa[self.p+'paternal-grandfather'];pid=u['object_person_id'];n=f['subject_person_id'];father=f['object_person_id'];grand=g['object_person_id'];rows={x:dict(person_id=x,source_person_ids=[x],source_assertion_id=None,parent_person_id=None)for x in[pid,n,father,grand]};rows[n].update(parent_person_id=father,source_assertion_id=f['id']);rows[father]['parent_person_id']=grand
  refs=[dict(**e,assertion_id=a['id'],scope='完整本傳父祖與伯叔原角色，僅編輯組裝',url=self.ch['source']['url'])for a in[u,f,g]for e in a['evidence']]
  rows[pid].update(parent_person_id=grand,parent_connection=dict(type='parent_from_nephew_named_father_and_grandfather',status='contextual_provisional',human_reviewed=False,rationale='同一完整本傳明父祖及父系伯叔；不新增source父。',nephew_person_id=n,nephew_father_person_id=father,paternal_uncle_assertion_id=u['id'],nephew_father_assertion_id=f['id'],nephew_grandfather_assertion_id=g['id'],references=refs));return rows[pid],rows,aa
 def test_both_uncle_directions(self):
  for k in('mi','dan'):
   m,r,a=self.state(k);self.assertTrue(valid(m,r,a,self.cids,I))
 def test_maternal_uncle_rejected(self):
  m,r,a=self.state();a[m['parent_connection']['paternal_uncle_assertion_id']]['predicate']='maternal_uncle';self.assertFalse(valid(m,r,a,self.cids,I))
 def test_common_grandfather_not_father(self):
  m,r,a=self.state();a[m['parent_connection']['nephew_grandfather_assertion_id']]['predicate']='father';self.assertFalse(valid(m,r,a,self.cids,I))
 def test_wrong_father_role_rejected(self):
  m,r,a=self.state();a[m['parent_connection']['nephew_father_assertion_id']]['object_person_id']=m['person_id'];self.assertFalse(valid(m,r,a,self.cids,I))
 def test_conflicting_father_rejected(self):
  m,r,a=self.state();a['new']=dict(predicate='father',subject_person_id=m['person_id'],object_person_id='other');self.assertFalse(valid(m,r,a,self.cids,I))
 def test_source_father_not_synthesized(self):
  m,r,a=self.state();m['source_assertion_id']='invented';self.assertFalse(valid(m,r,a,self.cids,I))
 def test_quote_mismatch(self):
  m,r,a=self.state();m['parent_connection']['references'][0]['quote']='叔父';self.assertFalse(valid(m,r,a,self.cids,I))
 def test_wrong_source_anchor_consistent_endpoint_rejected(self):
  m,r,a=self.state();u=a[m['parent_connection']['paternal_uncle_assertion_id']];u['evidence'][0]['object_person_mention_id']=a[m['parent_connection']['nephew_father_assertion_id']]['evidence'][0]['object_person_mention_id'];self.assertFalse(valid(m,r,a,self.cids,I))
 def test_distant_collateral_uncle_rejected(self):
  for term in('從伯','從叔'):
   m,r,a=self.state();u=a[m['parent_connection']['paternal_uncle_assertion_id']];u['predicate']='agnatic_senior_kin';u['qualifiers']['source_term']=term;self.assertFalse(valid(m,r,a,self.cids,I))
 def test_maternal_grandfather_not_paternal(self):
  m,r,a=self.state();m['parent_connection']['nephew_grandfather_assertion_id']=self.p+'maternal-grandfather';self.assertFalse(valid(m,r,a,self.cids,I))
 def test_known_conflicting_nephew_father_parent(self):
  m,r,a=self.state();father=r[m['parent_connection']['nephew_father_person_id']]['person_id'];a['new']=dict(predicate='father',subject_person_id=father,object_person_id='other');self.assertFalse(valid(m,r,a,self.cids,I))
 def test_maternal_only_does_not_connect_paternal_siblings(self):
  from scripts.family_assemblies import brother_connects
  for q in [{'same_mother_only':True},{'lineage':'maternal'},{'shared_father':False}]:self.assertFalse(brother_connects(dict(predicate='brother',subject_person_id='a',object_person_id='b',qualifiers=q),{'a'},{'b'}))
class Production(unittest.TestCase):
 def test_seventeen_members_source_editorial_and_missing_fathers(self):
  from scripts.person_bundle import load_catalog
  from scripts.family_assemblies import load_assemblies
  cat=load_catalog(I);s,a=load_assemblies(I,cat);f=next(x for x in json.loads((I/'registry/family-assemblies.json').read_bytes())['assemblies']if x['id']=='family-taishan-yang-xu-core');self.assertEqual(len(f['members']),18);self.assertEqual(sum(m.get('ancestor_connection',{}).get('type')=='ancestor_above_unnamed_sibling_descendant'for m in f['members']),1)
  ch=json.loads((I/'corpus/jinshu/034-yanghu.json').read_bytes());p=ch['paragraphs'][40];liang=next(m['person_id']for m in p['mentions']if m['surface']=='亮');tao=next(m['person_id']for m in p['mentions']if m['surface']=='陶');zhi=next(m['person_id']for m in p['mentions']if m['surface']=='祉')
  for pid in(liang,tao):self.assertIsNone(a[pid]['parent_person_id']);self.assertNotEqual(a[pid].get('parent_person_id'),zhi);self.assertEqual(a[pid]['generation_distance'],2)
  fa=next(m['person_id']for m in ch['paragraphs'][38]['mentions']if m['surface']=='法興');self.assertIn(fa,a);self.assertIsNone(a[fa]['parent_person_id']);self.assertIsNone(a[fa]['source_assertion_id']);self.assertEqual(a[fa]['ancestor_person_id'],'dqd_5q9_pkz_B');self.assertEqual(a[fa]['generation_distance'],6);self.assertEqual(a[fa]['intermediate_person_ids'],[None]*5)
 def test_maternal_only_brother_cannot_create_shared_father(self):
  from scripts.person_bundle import load_catalog
  from scripts.received_kin_assembly import valid as sibling_valid
  from unittest.mock import patch
  cat=load_catalog(I);aa={a['id']:a for r in cat[1]if r.get('record_type')=='person_assertion_set'for a in r['assertions']};chs={r['id']:r for r in cat[1]if r.get('record_type')=='marked_chapter'};f=next(x for x in json.loads((I/'registry/family-assemblies.json').read_bytes())['assemblies']if x['id']=='family-taishan-yang-xu-core');rows={r['person_id']:r for r in f['members']};row=next(r for r in rows.values()if r.get('parent_connection',{}).get('sibling_assertion_id')=='a-jin034-yanghu-same-mother-brother-cheng')
  self.assertTrue(sibling_valid(row,rows,aa,chs,I))
  for flag,value in [('same_mother_only',True),('shared_father',False),('lineage','maternal')]:
   mutated=copy.deepcopy(aa);mutated['a-jin034-yanghu-same-mother-brother-cheng']['qualifiers'][flag]=value
   with patch('scripts.fixed_witness_fact_slots.valid',return_value=True):self.assertFalse(sibling_valid(row,rows,mutated,chs,I))
 def test_old_ids_not_queries_or_reusable(self):
  from scripts.person_bundle import bundle,load_catalog
  from scripts.retired_person_ids import retired_person_ids,allocation_conflicts
  receipt=json.loads((I/'source-evidence/yang-family-assembly/annotation-chain.json').read_bytes());cat=load_catalog(I);retired=retired_person_ids(I)
  for old in receipt['retired_person_ids']:
   self.assertNotIn(old,cat[0]);self.assertIn(old,retired);self.assertTrue(allocation_conflicts(old,retired))
   with self.assertRaises(ValueError):bundle(old,I,catalog=cat)
if __name__=='__main__':unittest.main()
