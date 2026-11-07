# coding: utf-8
"""Finite additive current-source checks; root may point to the composed physical carrier."""
import os,sys,json,copy,importlib.util,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(os.environ.get('CBR_LU_GROWTH_ROOT',str(Path(__file__).resolve().parents[1]))).resolve();sys.path.insert(0,str(ROOT))
s=importlib.util.spec_from_file_location('lu_growth_candidate',Path(os.environ.get('CBR_LU_GROWTH_HELPER',str(ROOT/'scripts/lu_near_paternal_family.py'))));owner=importlib.util.module_from_spec(s);s.loader.exec_module(owner)
class LuNativeMentionGrowth(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=owner.contract(ROOT);cls.physical={p['id']:p for p in owner.read(ROOT,'registry/persons.json')['persons']};cls.base={p['id']:p for p in owner.read(ROOT,next(a['before_capture']for a in cls.c['archives']if a['kind']=='registry'))['persons']};cls.roles={}
  for role,seed in cls.c['role_seeds'].items():
   ch=owner.read(ROOT,seed['path']);m=next(m for p in ch['paragraphs']if p['id']==seed['paragraph_id']for m in p['mentions']if m['id']==seed['marker']['id']);cls.roles[role]=m['person_id']
  cls.ownids={v['id']for v in cls.c['source_templates'].values()};cls.ownmids={m['id']for ch in cls.c['source_templates'].values()for p in ch['paragraphs']for m in p['mentions']};cls.prior={cls.roles[r]:{e['mention_id']for e in cls.base[old]['evidence']}for old,r in cls.c['historical_old_id_role_map'].items()};cls.additions=owner._native_additions(ROOT,cls.prior,cls.ownids,cls.physical,{'w-jinshu':{'corpus/jinshu'}});cls.pid=cls.roles['ji'];cls.want=cls.base[next(k for k,r in cls.c['historical_old_id_role_map'].items()if r=='ji')]
 def check(self,actor=None,physical=None,additions=None):return owner._external_growth_valid(self.physical[self.pid]if actor is None else actor,self.want,self.ownids,self.ownmids,self.additions[self.pid]if additions is None else additions,self.physical if physical is None else physical)
 def test_01_actual_new053_literal_anchor_and_current_ID(self):
  self.assertEqual(len(self.additions[self.pid]),1);e,m=self.additions[self.pid][0];self.assertEqual(e['chapter_id'],'c-jinshu-053-minhuai-family');self.assertEqual(e['mention_id'],'c-jinshu-053-minhuai-family:p002:m0035');self.assertEqual(m['surface'],'陸機');self.check()
 def test_02_unknown_source_evidence_rejected(self):
  a=copy.deepcopy(self.physical[self.pid]);a['evidence'].append(dict(a['evidence'][-1],chapter_id='unknown',mention_id='unknown'));self.assertRaises(AssertionError,self.check,a)
 def test_03_physical_reverse_loss_rejected(self):
  a=copy.deepcopy(self.physical[self.pid]);mid=self.additions[self.pid][0][0]['mention_id'];a['evidence']=[e for e in a['evidence']if e['mention_id']!=mid];p=dict(self.physical);p[self.pid]=a;self.assertRaises(AssertionError,self.check,a,p)
 def test_04_physical_alias_loss_rejected(self):
  a=copy.deepcopy(self.physical[self.pid]);mid=self.additions[self.pid][0][0]['mention_id']
  for al in a['aliases']:al['mention_ids']=[x for x in al['mention_ids']if x!=mid]
  p=dict(self.physical);p[self.pid]=a;self.assertRaises(AssertionError,self.check,a,p)
 def test_05_duplicate_reverse_thief_rejected(self):
  e=self.additions[self.pid][0][0];p=dict(self.physical);p['foreign']={'evidence':[e],'aliases':[]};self.assertRaises(AssertionError,self.check,None,p)
 def test_06_duplicate_alias_thief_rejected(self):
  e=self.additions[self.pid][0][0];p=dict(self.physical);p['foreign']={'evidence':[],'aliases':[{'surface':e['quote'],'mention_ids':[e['mention_id']]}]};self.assertRaises(AssertionError,self.check,None,p)
 def test_07_old_snapshot_reverse_cannot_be_removed(self):
  a=copy.deepcopy(self.physical[self.pid]);mid=self.want['evidence'][0]['mention_id'];a['evidence']=[e for e in a['evidence']if e['mention_id']!=mid];self.assertRaises(AssertionError,self.check,a)
 def test_08_old_snapshot_reverse_order_cannot_change(self):
  a=copy.deepcopy(self.physical[self.pid]);a['evidence'][0],a['evidence'][1]=a['evidence'][1],a['evidence'][0];self.assertRaises(AssertionError,self.check,a)
 def test_09_old_alias_cannot_change(self):
  a=copy.deepcopy(self.physical[self.pid]);a['aliases'][0]['surface']='陸某';self.assertRaises(AssertionError,self.check,a)
 def test_10_caller_only_metadata_and_evidence_rejected_by_entry(self):
  p=dict(self.physical);a=copy.deepcopy(p[self.pid]);a['evidence']=a['evidence'][:-1];p[self.pid]=a
  self.assertRaises(AssertionError,owner.proof,ROOT,p)
 def test_11_current_endpoint_rekey_sameMID_and_raw_conserved(self):
  old=self.pid;new='finite_rekey_role';a=copy.deepcopy(self.physical[old]);a['id']=new;p=dict(self.physical);p.pop(old);p[new]=a;adds=copy.deepcopy(self.additions[old]);adds[0][1]['person_id']=new;owner._external_growth_valid(a,self.want,self.ownids,self.ownmids,adds,p);self.assertEqual(adds[0][0]['mention_id'],self.additions[old][0][0]['mention_id'])
 def test_12_wrong_native_source_endpoint_rejected(self):
  adds=copy.deepcopy(self.additions[self.pid]);adds[0][1]['person_id']='foreign';self.assertRaises(AssertionError,owner._external_growth_valid,self.physical[self.pid],self.want,self.ownids,self.ownmids,adds,self.physical)
 def test_13_new_person_template_role_can_use_same_additive_rule(self):
  role=next(iter(self.c['new_people_templates']));seed=self.c['new_role_mids'][role];ch=owner.read(ROOT,seed['path']);marker=next(m for p in ch['paragraphs']for m in p['mentions']if m['id']==seed['mid']);pid=marker['person_id'];actor=self.physical[pid];adds=[]
  for e in actor['evidence']:
   matching=next((m for p in ch['paragraphs']for m in p['mentions']if m['id']==e['mention_id']),None)
   self.assertIsNotNone(matching);adds.append((e,matching))
  # Treat this actual literal native view as the newly added layer in a bounded
  # consumer fixture. No source text, MID or current person endpoint is invented.
  want=dict(actor,evidence=[],aliases=[]);owner._external_growth_valid(actor,want,set(),set(),adds,self.physical)
  wrong=copy.deepcopy(adds);wrong[0][1]['person_id']=self.pid
  self.assertRaises(AssertionError,owner._external_growth_valid,actor,want,set(),set(),wrong,self.physical)
 def test_14_full_finite_Lu_proof_accepts_current_U(self):
  c,r,*_=owner.proof(ROOT);self.assertEqual(len(r),6)
 def stripped_additions(self):
  mid=self.additions[self.pid][0][0]['mention_id'];p=dict(self.physical);a=copy.deepcopy(p[self.pid]);a['evidence']=[e for e in a['evidence']if e['mention_id']!=mid]
  for al in a['aliases']:al['mention_ids']=[m for m in al['mention_ids']if m!=mid]
  a['aliases']=[al for al in a['aliases']if al['mention_ids']];p[self.pid]=a;return p,a
 def test_15_missing_entire_new_reverse_alias_layer_is_source_owner_responsibility(self):
  p,a=self.stripped_additions();adds=owner._native_additions(ROOT,self.prior,self.ownids,p,{'w-jinshu':{'corpus/jinshu'}});self.assertEqual(adds[self.pid],[]);owner._external_growth_valid(a,self.want,self.ownids,self.ownmids,[],p)
  from scripts import received_sima_family_sources as source053
  def raw(rel):return json.dumps({'persons':list(p.values())},ensure_ascii=False).encode()if rel=='registry/persons.json'else(ROOT/rel).read_bytes()
  self.assertRaises(AssertionError,source053._proof,raw,p)
 def test_16_actual_caller_chapter_finds_whole_missing_new_layer_but_is_not_authority(self):
  p,a=self.stripped_additions();ch=owner.read(ROOT,'corpus/jinshu/053-minhuai-family.json');adds=owner._native_additions(ROOT,self.prior,self.ownids,p,{'w-jinshu':{'corpus/jinshu'}},[ch]);self.assertEqual(len(adds[self.pid]),1);self.assertRaises(AssertionError,owner._external_growth_valid,a,self.want,self.ownids,self.ownmids,adds[self.pid],p)
  bad=copy.deepcopy(ch);next(m for para in bad['paragraphs']for m in para['mentions']if m['id']==self.additions[self.pid][0][0]['mention_id'])['surface']='改字';again=owner._native_additions(ROOT,self.prior,self.ownids,self.physical,{'w-jinshu':{'corpus/jinshu'}},[bad]);self.assertEqual(again[self.pid][0][1]['surface'],'陸機')
if __name__=='__main__':unittest.main()
