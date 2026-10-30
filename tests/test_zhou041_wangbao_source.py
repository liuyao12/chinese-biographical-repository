import copy,json,unittest
from pathlib import Path
from unittest.mock import patch
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
  original=Path.read_bytes
  return patch.object(Path,'read_bytes',lambda p:json.dumps(changes[str(p.relative_to(ROOT))],ensure_ascii=False).encode()if p.is_relative_to(ROOT)and str(p.relative_to(ROOT))in changes else original(p))
 def marker(self,ch,role,kind='person'):
  return next(m for p in ch['paragraphs']for m in p['mentions']if m.get('source_role')==role and m['kind']==kind)
 def test_01_complete_projection(self):
  self.assertEqual(len(self.ch['paragraphs']),14);self.assertEqual(len(self.ch['annotation']['modern_collation_reports']),10)
  counts={k:sum(m['kind']==k for p in self.ch['paragraphs']for m in p['mentions'])for k in ['person','pronoun','unresolved']};self.assertEqual(counts,{'person':97,'pronoun':9,'unresolved':14})
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
  self.assertEqual(len(self.ch['annotation']['unresolved_identity_cases']),2);self.assertEqual(len(self.ch['annotation']['unresolved_source_reference_readings']),11)
  for c in self.ch['annotation']['unresolved_identity_cases']:self.assertTrue(c['note']);self.assertTrue(c['paragraph_ids']);self.assertTrue(c['unknown_identity_possible'])
if __name__=='__main__':unittest.main()
