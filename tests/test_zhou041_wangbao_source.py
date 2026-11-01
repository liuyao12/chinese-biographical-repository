import copy,json,unittest
from pathlib import Path
from unittest.mock import patch
from contextlib import ExitStack
from scripts.fixed_zhou041_wangbao import proof,errors,brothers_namespace_members,guard_bundle,CH,CID,REF,source_letter_reference
from scripts.explicit_brothers_namespace import members
from scripts.person_bundle import load_catalog,bundle
ROOT=Path(__file__).resolve().parents[1]
class Zhou041(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.ch,cls.contract,cls.roles=proof(ROOT)
  cls.people,cls.records=load_catalog(ROOT)
  cls.assembly=next(a for a in json.loads((ROOT/'registry/family-assemblies.json').read_bytes())['assemblies']if a['id']=='family-zhou041-zhou-brothers')
  cls.assertions={a['id']:a for rec in cls.records for a in rec.get('assertions',[])}
 def overlay(self,changes):
  ob,ot=Path.read_bytes,Path.read_text
  def raw(p):
   rel=str(p.relative_to(ROOT))if p.is_relative_to(ROOT)else None
   if rel not in changes:return None
   return changes[rel]if isinstance(changes[rel],bytes)else json.dumps(changes[rel],ensure_ascii=False).encode()
  stack=ExitStack();stack.enter_context(patch.object(Path,'read_bytes',lambda p:raw(p)if raw(p)is not None else ob(p)));stack.enter_context(patch.object(Path,'read_text',lambda p,*a,**k:raw(p).decode()if raw(p)is not None else ot(p,*a,**k)));return stack
 def marker(self,ch,role,kind='person'):
  return next(m for p in ch['paragraphs']for m in p['mentions']if m.get('source_role')==role and m['kind']==kind)
 def test_01_complete_projection(self):
  self.assertEqual(len(self.ch['paragraphs']),14);self.assertEqual(len(self.ch['annotation']['modern_collation_reports']),10)
  from scripts.fixed_zhou041_wangbao import project, LETTER_REFERENCES
  raw=(ROOT/self.contract['raw_file']).read_text();selection=self.contract['selection'];paragraphs,notes=project(raw,selection['start'],selection['end'])
  self.assertEqual([{k:p[k]for k in ('id','text','source_position')}for p in self.ch['paragraphs']],paragraphs);self.assertEqual(len(self.ch['annotation']['modern_collation_reports']),len(notes))
  current={m['id']:m for p in self.ch['paragraphs']for m in p['mentions']};original={m['id']:m for p in self.contract['chapter_template']['paragraphs']for m in p['mentions']};self.assertEqual(set(current),set(original))
  for mid,m in current.items():self.assertIs(type(m['start']),int);self.assertIs(type(m['end']),int);self.assertEqual({k:m[k]for k in ('id','start','end','surface')},{k:original[mid][k]for k in ('id','start','end','surface')})
  self.assertEqual({m['id']for m in current.values()if m['kind']=='pronoun'},set(LETTER_REFERENCES))
 def test_02_modern_reports_not_ancient(self):
  for r in self.ch['annotation']['modern_collation_reports']:self.assertEqual(r['layer'],'modern_received_witness_collation_report');self.assertFalse(r['image_verified'])
 def test_03_correction_block_unresolved(self):
  self.assertTrue(any(m['surface']=='〔傷金〕（產）〔彥〕'and m['kind']=='unresolved'for p in self.ch['paragraphs']for m in p['mentions']))
 def test_04_nine_letter_roles(self):
  for p in self.ch['paragraphs']:
   for m in p['mentions']:
    if m['kind']=='pronoun':self.assertTrue(source_letter_reference(m,p['text']));self.assertEqual(m['person_id'],self.roles['$'+m['source_role']])
 def test_05_unknown_letter_not_globally_allowed(self):
  m=copy.deepcopy(self.marker(self.ch,'bao','pronoun'));m['id']='unregistered';self.assertFalse(source_letter_reference(m))
 def test_06_wrong_letter_speaker(self):
  ch=copy.deepcopy(self.ch);self.marker(ch,'bao','pronoun')['person_id']=self.roles['$zhouhongrang']
  with self.overlay({CH:ch}):self.assertTrue(errors(ch,ROOT))
 def test_07_pronoun_alias_rejected(self):
  people=copy.deepcopy(self.people);m=self.marker(self.ch,'bao','pronoun');people[m['person_id']]['aliases'].append({'surface':m['surface'],'mention_ids':[m['id']]})
  with self.assertRaises(AssertionError):proof(ROOT,people=people)
 def test_08_missing_reverse(self):
  people=copy.deepcopy(self.people);pid=self.roles['$bao'];people[pid]['evidence']=[e for e in people[pid]['evidence']if e.get('chapter_id')!=CID]
  with self.assertRaises(AssertionError):proof(ROOT,people=people)
 def test_09_missing_caller_chapter(self):
  with self.assertRaises(AssertionError):guard_bundle(ROOT,self.roles['$bao'],self.people,[r for r in self.records if r.get('id')!=CID])
 def test_10_missing_caller_sidecar(self):
  with self.assertRaises(AssertionError):guard_bundle(ROOT,self.roles['$bao'],self.people,[r for r in self.records if r.get('record_type')!='person_assertion_set'or r.get('chapter_id')!=CID])
 def test_11_wrong_modern_layer(self):
  ch=copy.deepcopy(self.ch);ch['annotation']['modern_collation_reports'][0]['layer']='ancient_commentary'
  with self.overlay({CH:ch}):self.assertTrue(errors(ch,ROOT))
 def test_12_raw_text_immutable(self):
  ch=copy.deepcopy(self.ch);ch['paragraphs'][0]['text']+='字'
  with self.overlay({CH:ch}):self.assertTrue(errors(ch,ROOT))
 def test_13_all_four_rulers_different(self):
  self.assertEqual(len({self.roles['$'+k]for k in ['zhoutaizu','xiaomin','shizong','gaozu']}),4)
 def test_14_ruler_polity_cannot_swap(self):
  ch=copy.deepcopy(self.ch);self.marker(ch,'gaozu')['person_id']=self.roles['$liangwu']
  with self.overlay({CH:ch}):self.assertTrue(errors(ch,ROOT))
 def test_15_received_brothers_joint_namespace(self):
  out=members(self.assembly,self.people,self.assertions,{CID:self.ch},ROOT);self.assertEqual(set(out),{self.roles['$zhouhongzheng'],self.roles['$zhouhongrang']});self.assertNotIn(self.assembly['namespace_id'],self.people)
  for row in out.values():self.assertIsNone(row['root_person_id']);self.assertIsNone(row['parent_person_id'])
 def test_16_brother_direction_rejected(self):
  aa=copy.deepcopy(self.assertions);a=aa['a-zhou041-hongzheng-older-brother-hongrang'];a['subject_person_id'],a['object_person_id']=a['object_person_id'],a['subject_person_id']
  with self.assertRaises(ValueError):members(self.assembly,self.people,aa,{CID:self.ch},ROOT)
 def test_17_no_fabricated_parent(self):
  a=copy.deepcopy(self.assembly);a['root_person_id']=self.roles['$bao']
  with self.assertRaises(ValueError):members(a,self.people,self.assertions,{CID:self.ch},ROOT)
 def test_18_caller_source_cannot_hide(self):
  ch=copy.deepcopy(self.ch);ch['paragraphs'][0]['text']='false'
  with self.assertRaises(ValueError):members(self.assembly,self.people,self.assertions,{CID:ch},ROOT)
 def test_19_all_thirty_current_api(self):
  for role in self.contract['role_seeds']:
   result=bundle(self.roles['$'+role],ROOT,catalog=(self.people,self.records));self.assertTrue(result)
 def test_20_coherent_namespace_rekey_preserves_captures(self):
  oldns=self.assembly['namespace_id'];ns='zzz_zzz_zz1';self.assertNotIn(ns,self.people)
  mapping={oldns:ns,oldns+'_A':ns+'_A',oldns+'_B':ns+'_B'}
  def replace(x):
   if isinstance(x,str):return mapping.get(x,x)
   if isinstance(x,list):return[replace(v)for v in x]
   if isinstance(x,dict):return{k:replace(v)for k,v in x.items()}
   return x
  paths=[CH,'registry/persons.json','registry/family-assemblies.json',*self.contract['sidecar_templates']]
  changes={p:replace(json.loads((ROOT/p).read_bytes()))for p in paths}
  if (ROOT/'source-evidence/liang-xiao-close-family/family-source-contract.json').exists():
   # The new complete-current projection also checks exact XML endpoints.
   xml=CH[:-5]+'.xml';text=(ROOT/xml).read_text()
   for old,new in mapping.items():text=text.replace('ref="'+old+'"','ref="'+new+'"')
   changes[xml]=text.encode()
  original=(ROOT/REF).read_bytes()
  with self.overlay(changes):
   ch,c,r=proof(ROOT);self.assertEqual(r['$zhouhongzheng'],ns+'_A');self.assertEqual((ROOT/REF).read_bytes(),original)
 def test_21_old_unpublished_not_alias(self):
  self.assertNotIn('proposal_reservation',self.contract)
  self.assertFalse((ROOT/'source-evidence/zhou041-wangbao-ws2432538/annotation-chain.json').exists())
  for key in ['zhouhongzheng','zhouhongrang']:self.assertFalse(self.people[self.roles['$'+key]].get('id_aliases'))
 def test_22_near_names_never_replace_source_role(self):
  for role,wrong in [('zhumaichen','gni_7gn_c4a'),('husengyou','p93_tgr_t8r_A'),('xiaoz y','5bd_a4e_ad6'),('zhouhongrang','6t3_2tt_2f0'),('huangluohan','fum_370_iq6_AAAE')]:
   self.assertIn(wrong,self.people);ch=copy.deepcopy(self.ch);self.marker(ch,role)['person_id']=wrong
   with self.overlay({CH:ch}):self.assertTrue(errors(ch,ROOT))
 def test_23_normal_namespace_backend(self):
  from scripts.family_assemblies import load_assemblies
  from scripts.personless_namespace import namespace_index_root
  source,assembled=load_assemblies(ROOT,(self.people,self.records));pids=[self.roles['$zhouhongzheng'],self.roles['$zhouhongrang']]
  self.assertEqual({source[p]['namespace_id']for p in pids},{self.assembly['namespace_id']})
  rows=[{'person_id':p,'label':self.people[p]['label'],'assembled_identity':assembled[p]}for p in pids]
  heading=namespace_index_root(self.assembly['namespace_id'],rows);self.assertEqual(heading['person_id'],pids[0]);self.assertIn('弟兄',heading['label'])
 def test_24_unresolved_schema_separates_no_candidate_readings(self):
  markers={m['id']:(p,m)for p in self.ch['paragraphs']for m in p['mentions']};case_mids=[];pending_mids=[];group_mids=[]
  for c in self.ch['annotation']['unresolved_identity_cases']:
   self.assertTrue(c['note']);self.assertTrue(c['paragraph_ids']);self.assertTrue(c['unknown_identity_possible']);self.assertTrue(c['candidate_person_ids']);self.assertTrue(set(c['candidate_person_ids'])<=set(self.people));case_mids.extend(c['unresolved_mention_ids'])
  for r in self.ch['annotation']['unresolved_source_reference_readings']:
   self.assertEqual(r['record_type'],'unresolved_source_reference_reading');self.assertIsNone(r['person_id']);self.assertEqual(r['candidate_person_ids'],[]);self.assertTrue(r['paragraph_ids']);self.assertTrue(r['unresolved_mention_ids']);pending_mids.extend(r['unresolved_mention_ids'])
  for doc in self.records:
   if doc.get('record_type')=='source_person_reference_group_set'and doc.get('chapter_id')==CID:
    for group in doc['groups']:
     self.assertTrue(group['group_marker_ids']);group_mids.extend(group['group_marker_ids'])
     for mid in group['group_marker_ids']:self.assertEqual(markers[mid][1]['surface'],group['source_term'])
  covered=case_mids+pending_mids+group_mids;self.assertEqual(len(covered),len(set(covered)));self.assertEqual(set(covered),{mid for mid,(p,m)in markers.items()if m['kind']=='unresolved'})
  for mid in covered:
   p,m=markers[mid];self.assertIsNone(m['person_id']);self.assertEqual(p['text'][m['start']:m['end']],m['surface'])
if __name__=='__main__':unittest.main()
