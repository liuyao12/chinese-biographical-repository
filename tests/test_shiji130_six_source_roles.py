import copy,json,unittest
from pathlib import Path
from unittest.mock import patch
from scripts import fixed_shiji130_six_roles as f
from scripts.source_person_reference_groups import validated_sets,for_people
from scripts.cross_chapter_references import errors as xerrors
ROOT=Path(__file__).resolve().parents[1]
class Shiji130Roles(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.ch,cls.groups,cls.roles,cls.cap=f.accepted(ROOT);cls.people={p['id']:p for p in json.loads((ROOT/'registry/persons.json').read_bytes())['persons']};cls.owned={mid for g in cls.groups['groups']for mid in g['group_marker_ids']}|{r['source']['mention_id']for r in cls.ch['cross_chapter_references']}
 def overlay(self,values):
  original=Path.read_bytes
  return patch.object(Path,'read_bytes',lambda p:json.dumps(values[str(p.relative_to(ROOT))],ensure_ascii=False).encode()if p.is_relative_to(ROOT)and str(p.relative_to(ROOT))in values else original(p))
 def test_positive_exact_source_and_four_legacy_reverse(self):
  self.assertEqual(f.errors(self.ch,ROOT),[]);self.assertTrue(f.group_set_valid(self.groups,self.people,ROOT));self.assertEqual(len(self.groups['groups']),4)
 def test_raw_all_MIDs_positions_and_p142_conserved(self):
  base=f.expand(self.cap['base_native_template'],self.roles)
  for a,b in zip(base['paragraphs'],self.ch['paragraphs']):self.assertEqual(a['text'],b['text']);self.assertEqual([(m['id'],m['start'],m['end'],m['surface'],m['person_id'])for m in a['mentions']],[(m['id'],m['start'],m['end'],m['surface'],m['person_id'])for m in b['mentions']])
  m=next(m for p in self.ch['paragraphs']for m in p['mentions']if m['id']==self.cap['protected_mid']);self.assertEqual((m['kind'],m['person_id']),('unresolved',None))
 def test_group_ranges_carry_complete_own_source_without_direct_person_occurrence(self):
  paragraphs={p['id']:p for p in self.ch['paragraphs']}
  for g in self.groups['groups']:
   self.assertEqual([r['mention_id']for r in g['source_ranges']],g['group_marker_ids'])
   for r in g['source_ranges']:
    p=paragraphs[r['paragraph_id']];self.assertEqual(r['quote'],p['text']);self.assertEqual(p['text'][r['start']:r['end']],r['surface']);self.assertEqual(r['source_revision'],2609362);self.assertEqual(r['source_id'],self.ch['source_id']);self.assertNotIn('person_id',r)
 def test_counts_only_explicit_ershu_reports_two(self):
  self.assertEqual([g['reported_count']for g in self.groups['groups']],[None,None,None,2]);self.assertTrue(all(len(g['members'])==2 for g in self.groups['groups']))
 def test_same_guancai_source_roles_are_distinct(self):
  p=next(p for p in self.ch['paragraphs']if p['id'].endswith(':p047'));ms={m['id']:m for m in p['mentions']};self.assertEqual(ms[f.CID+':m047-0000']['kind'],'unresolved');self.assertEqual(ms[f.CID+':m047-0047']['kind'],'work')
 def test_no_source_group_or_title_alias_evidence(self):
  for actor in self.people.values():self.assertFalse(any(e.get('mention_id')in self.owned for e in actor['evidence']));self.assertFalse(any(self.owned.intersection(a['mention_ids'])for a in actor['aliases']))
 def test_all_actual_chapter_targets_validate(self):
  chs={self.ch['id']:self.ch}
  for r in self.ch['cross_chapter_references']:
   target=json.loads((ROOT/('corpus/shiji/'+r['target']['book_id'][-3:]+'.json')).read_bytes());chs[target['id']]=target
  self.assertEqual(xerrors(chs,ROOT),[]);r=self.ch['cross_chapter_references'][2];self.assertEqual(r['source']['surface'],'樊酈列傳');self.assertEqual(r['target']['section_label'],'樊酈滕灌列傳第三十五')
 def test_unknown_owner_and_missing_caller_sidecar_fail(self):
  with self.assertRaises(ValueError):validated_sets([],self.people,ROOT)
  bad=copy.deepcopy(self.groups);bad['owner']='fixed_zhou041_erlu'
  with self.assertRaises(ValueError):f.group_set_valid(bad,self.people,ROOT)
 def test_wrong_member_count_or_alternative_fails(self):
  for mutate in [lambda g:g['groups'][0].update(reported_count=2),lambda g:g['groups'][3].update(reported_count=2.0),lambda g:g['groups'][0]['members'].pop(),lambda g:g['groups'][0].update(completeness='alternative')]:
   d=copy.deepcopy(self.groups);mutate(d)
   with self.assertRaises(ValueError):f.group_set_valid(d,self.people,ROOT)
 def test_wrong_title_target_and_expanded_original_anchor_fail(self):
  for mode in ['target','span']:
   ch=copy.deepcopy(self.ch);m=next(m for p in ch['paragraphs']for m in p['mentions']if m['id']==f.CID+':m107-0029')
   if mode=='target':m['chapter_reference']['target']['chapter_id']='c-shiji-120-jizheng'
   else:m['surface']='樊酈列傳';m['end']+=2
   with self.overlay({f.CH:ch}):self.assertTrue(f.errors(ch,ROOT))
 def test_p142_cannot_be_merged_as_qian(self):
  ch=copy.deepcopy(self.ch);m=next(m for p in ch['paragraphs']for m in p['mentions']if m['id']==self.cap['protected_mid']);m.update(kind='person',person_id=next(v['person_id']for p in ch['paragraphs']for v in p['mentions']if v.get('surface')=='遷'and v['kind']=='person'))
  with self.overlay({f.CH:ch}):self.assertTrue(f.errors(ch,ROOT))
 def test_missing_or_corrupt_original_identity_ledger_fails(self):
  rel='corpus/shiji/130-identities.json';d=json.loads((ROOT/rel).read_bytes());d['decisions'].pop()
  with self.overlay({rel:d}):self.assertTrue(f.errors(self.ch,ROOT))
 def test_external_revision_or_image_qualification_cannot_drift(self):
  spec=self.cap['external_individual_refs'][0]
  for key,value in [('revision_id',999999),('image_verified',True)]:
   ch=json.loads((ROOT/spec['path']).read_bytes());ch['source'][key]=value
   with self.overlay({spec['path']:ch}):self.assertTrue(f.errors(self.ch,ROOT))
 def test_one_endpoint_swap_rejected(self):
  spec=self.cap['external_individual_refs'][0];ch=json.loads((ROOT/spec['path']).read_bytes());m=next(m for p in ch['paragraphs']for m in p['mentions']if m['id']==spec['marker']['id']);m['person_id']=next(p for p in self.people if p!=m['person_id'])
  with self.overlay({spec['path']:ch}):self.assertTrue(f.errors(self.ch,ROOT))
 def test_coherent_current_PID_rekey_has_no_permanent_whitelist(self):
  old=self.groups['groups'][3]['members'][0]['person_id'];new='zzz_zz1_zz2';self.assertNotIn(new,self.people)
  def rekey(v):
   if isinstance(v,str):return new if v==old else v
   if isinstance(v,list):return[rekey(x)for x in v]
   if isinstance(v,dict):return{k:rekey(x)for k,x in v.items()}
   return v
  paths={f.CH,f.GROUP,'registry/persons.json',*self.cap['unchanged_sidecar_templates'],*(s['path']for s in self.cap['external_individual_refs'])};values={p:rekey(json.loads((ROOT/p).read_bytes()))for p in paths}
  with self.overlay(values):self.assertEqual(f.errors(values[f.CH],ROOT),[])
if __name__=='__main__':unittest.main()
