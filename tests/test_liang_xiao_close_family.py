import copy
import hashlib
import json
import os
import sys
import unittest
from contextlib import ExitStack
from pathlib import Path
from unittest.mock import patch
ROOT=Path(os.environ.get('CBR_LIANG_FAMILY_ROOT',Path(__file__).resolve().parents[1])).resolve()
sys.path.insert(0,str(ROOT))
from scripts.liang_xiao_close_family import proof,contract,read,raw,typed_projection,guard_bundle,family_valid,REF,NS
from scripts.person_bundle import load_catalog,bundle
from scripts.retired_person_ids import retired_person_ids,allocation_conflicts
from scripts.person_ids import family_path_errors

def coherent_family_rekey_fixture(root,people,records):
 c,roles,*_=proof(root,people=people)
 oldroot=roles['$daoci'];newroot='z97_k3x_h2p';assert newroot not in people
 mapping={pid:newroot+pid[len(oldroot):]for pid in roles.values()}
 rels={a['path']for a in c['archives']}|set(c['source_templates'])|set(c['sidecar_templates'])|{c['name_path']}
 changes={}
 for rel in rels:
  if rel.endswith('.json'):changes[rel]=typed_projection(read(root,rel),mapping)
  else:
   text=raw(root,rel).decode()
   for old,new in mapping.items():text=text.replace('ref="'+old+'"','ref="'+new+'"')
   changes[rel]=text.encode()
 moved_people={mapping.get(k,k):typed_projection(p,mapping)for k,p in people.items()}
 moved_records=[typed_projection(r,mapping)for r in records]
 return changes,moved_people,moved_records,mapping

class LiangXiaoCloseFamily(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c,cls.roles,cls.sources,cls.sides,cls.names=proof(ROOT)
  cls.people,cls.records=load_catalog(ROOT)
  cls.retired=retired_person_ids(ROOT)
  cls.paragraphs={p['id']:(ch['id'],p)for ch in cls.sources.values()for p in ch['paragraphs']}
 def overlay(self,changes):
  ob,ot=Path.read_bytes,Path.read_text
  def data(p):
   rel=str(p.relative_to(ROOT))if p.is_relative_to(ROOT)else None
   if rel not in changes:return None
   v=changes[rel];return v if isinstance(v,bytes)else(json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode()
  st=ExitStack();st.enter_context(patch.object(Path,'read_bytes',lambda p:data(p)if data(p)is not None else ob(p)));st.enter_context(patch.object(Path,'read_text',lambda p,*a,**k:data(p).decode()if data(p)is not None else ot(p,*a,**k)));return st
 def test_real_family_paths_two_new_identities_and_six_discarded(self):
  self.assertEqual(set(self.people),{p['id']for p in read(ROOT,'registry/persons.json')['persons']})
  self.assertEqual(set(self.c['new_role_mids']),{'daoci','shunzhi'})
  for rel,s in self.sides.items():
   for a in s['assertions']:
    self.assertFalse(family_path_errors(a['subject_person_id'],{'connection':'father','parent_person_id':a['object_person_id']}))
    self.assertTrue(family_valid(a,self.paragraphs,ROOT))
  for old in self.c['historical_old_id_role_map']:
   self.assertNotIn(old,self.people)
   self.assertFalse(any(old in p.get('id_aliases',[])for p in self.people.values()))
   self.assertIn(old,self.retired);self.assertTrue(allocation_conflicts(old,self.retired))
 def test_normal_eight_apis_and_old_six_unknown_not_redirect(self):
  for role,pid in self.roles.items():
   b=bundle(pid,ROOT,catalog=(self.people,self.records));self.assertEqual(b['canonical_person_id'],pid)
   self.assertTrue(any(a['id'].startswith(('a-liang-close-family-','a-zhou041-close-kin-'))for a in b['relations']))
  for old in self.c['historical_old_id_role_map']:
   with self.assertRaisesRegex(ValueError,'未知人物 ID'):bundle(old,ROOT,catalog=(self.people,self.records))
 def test_coverage_and_source_qualification_no_claim_full_ner_or_lifetime_dynasty(self):
  for ch in self.sources.values():
   self.assertEqual(ch['annotation']['scope'],'family_role_subset_of_one_complete_received_unit')
   self.assertIsNone(ch['source']['edition']);self.assertFalse(ch['source']['image_verified'])
   self.assertNotIn('選段',ch['title']);self.assertNotIn('首段',ch['source']['title'])
  for role in ('$daoci','$shunzhi'):
   p=self.people[self.roles[role]]
   self.assertNotIn('dynasty',p);self.assertNotIn('birth_year',p)
  self.assertTrue(all(n['surname']=='蕭'and not n['surname_basis']['literal_in_current_mention']for n in self.names['records']))
  for u in read(ROOT,self.c['ledger_path']):
   if 'existing_container'in u:self.assertFalse(Path(u['existing_container']).is_absolute())
 def test_wrong_taizu_shunzhi_parent_or_any_single_endpoint_fails(self):
  rel=next(p for p,ch in self.sources.items()if ch['book_id']=='b-liangshu-022');wrong=copy.deepcopy(self.sources[rel]);wrong['paragraphs'][0]['mentions'][1]['person_id']='dkn_ge4_286_AAAAI'
  with self.overlay({rel:wrong}),self.assertRaises(AssertionError):proof(ROOT)
  for rel,side in self.sides.items():
   wrong=copy.deepcopy(side);wrong['assertions'][0]['object_person_id']=self.roles['$yuan']
   with self.overlay({rel:wrong}),self.assertRaises(AssertionError):proof(ROOT)
 def test_foreign_qualification_or_far_pedigree_surname_cannot_replace_near_proof(self):
  ledger=read(ROOT,self.c['ledger_path']);wrong=copy.deepcopy(ledger);wrong[0]['text']=wrong[0]['text'].replace('姓蕭氏','姓李氏')
  with self.overlay({self.c['ledger_path']:wrong}),self.assertRaises(AssertionError):proof(ROOT)
  wrong=copy.deepcopy(self.names);wrong['records'][0]['surname']='李'
  with self.overlay({self.c['name_path']:wrong}),self.assertRaises(AssertionError):proof(ROOT)
  wrong=copy.deepcopy(ledger);wrong[2]['original_wikitext_obtained']=True
  with self.overlay({self.c['ledger_path']:wrong}),self.assertRaises(AssertionError):proof(ROOT)
 def test_current_projection_mutation_and_old_capture_rewrite_both_fail(self):
  a=next(a for a in self.c['archives']if a['kind']=='current_projection');wrong=read(ROOT,a['path']);wrong['unsupported_added_field']='not a coherent endpoint transformation'
  with self.overlay({a['path']:wrong}),self.assertRaises(AssertionError):proof(ROOT)
  rel=next(iter(self.c['immutable_prior_capture_hashes']));wrong=raw(ROOT,rel)+b'\n'
  with self.overlay({rel:wrong}),self.assertRaises(AssertionError):proof(ROOT)
 def test_caller_reverse_and_names_or_source_omission_cannot_hide_owner(self):
  records=[r for r in self.records if r!=self.names]
  for pid in self.roles.values():
   with self.assertRaises(AssertionError):guard_bundle(ROOT,pid,self.people,records)
  pid=self.roles['$yuan'];people=copy.deepcopy(self.people);people[pid]['evidence']=[]
  with self.assertRaises(AssertionError):guard_bundle(ROOT,pid,people,records)
 def test_new_mother_or_rank1_not_encoded_by_family_letters(self):
  a=next(iter(self.sides.values()))['assertions'][0];wrong=copy.deepcopy(a);wrong['qualifiers']['birth_order']={'ordinal':1,'scope':'sons_of_parent'}
  self.assertFalse(family_valid(wrong,self.paragraphs,ROOT))
  self.assertFalse(any(a['predicate']in('mother','spouse')for s in self.sides.values()for a in s['assertions']))
 def test_legal_coherent_entire_root_rekey_preserves_opaque_captures_and_rejects_after_reverse_loss(self):
  oldroot=self.roles['$daoci'];newroot='z97_k3x_h2p';self.assertNotIn(newroot,self.people)
  mapping={pid:newroot+pid[len(oldroot):]for pid in self.roles.values()};changes={}
  # All actual current source/projection paths; historical proof/captures stay exact.
  rels={a['path']for a in self.c['archives']}|set(self.c['source_templates'])|set(self.c['sidecar_templates'])|{self.c['name_path']}
  for rel in rels:
   if rel.endswith('.json'):changes[rel]=typed_projection(read(ROOT,rel),mapping)
   elif rel.endswith('.xml'):
    s=raw(ROOT,rel).decode()
    for old,new in mapping.items():s=s.replace('ref="'+old+'"','ref="'+new+'"')
    changes[rel]=s.encode()
  people={mapping.get(k,k):typed_projection(p,mapping)for k,p in self.people.items()};records=[typed_projection(r,mapping)for r in self.records]
  opaque=[(p['id'],p['text'],[(m['id'],m['start'],m['end'],m['surface'])for m in p['mentions']])for ch in self.sources.values()for p in ch['paragraphs']]
  captures={a['before_capture']:raw(ROOT,a['before_capture'])for a in self.c['archives']}
  with self.overlay(changes):
   _,roles,sources,*_=proof(ROOT,people=people,records=records);self.assertEqual(roles['$daoci'],newroot)
   self.assertEqual(opaque,[(p['id'],p['text'],[(m['id'],m['start'],m['end'],m['surface'])for m in p['mentions']])for ch in sources.values()for p in ch['paragraphs']])
   for rel,b in captures.items():self.assertEqual(raw(ROOT,rel),b)
   pid=roles['$yuan'];guard_bundle(ROOT,pid,people,records);people[pid]['evidence']=[]
   with self.assertRaises(AssertionError):guard_bundle(ROOT,pid,people,records)

if __name__=='__main__':unittest.main(verbosity=2)
