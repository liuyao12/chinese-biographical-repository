"""Bounded WYD044 explicit brother's-son roles and qualified grandfather inference."""
import json,hashlib
from pathlib import Path
CID='c-songshu-044-wyd1739-xiehui'
REF='source-evidence/song044-wyd1739-xiehui/formal-role-contract.json'
CONTRACT_SHA='2b1bc6f3dc350c2450fa2e86feff969faaa3a3b1fd6b8870f7149e53003b9973'
def _context(root):
 try:from scripts.fixed_wuyingdian_song044 import validate_source
 except ImportError:from fixed_wuyingdian_song044 import validate_source
 try:from scripts.wyd_song044_formal_model import resolve_existing,local_current
 except ImportError:from wyd_song044_formal_model import resolve_existing,local_current
 root=Path(root);raw=(root/REF).read_bytes()
 if hashlib.sha256(raw).hexdigest()!=CONTRACT_SHA:raise ValueError('宋044契約SHA')
 c=json.loads(raw);ch=json.loads((root/'corpus/songshu/044-wyd1739.json').read_bytes());validate_source(ch,root);roles=resolve_existing(root,c);roles.update(local_current(root,c))
 if len(roles)!=96:raise ValueError('宋044角色未完整')
 try:from scripts.wyd_song044_role_seed import materialize
 except ImportError:from wyd_song044_role_seed import materialize
 try:from scripts.wyd_song044_age import base_annotation
 except ImportError:from wyd_song044_age import base_annotation
 if base_annotation(ch)!=c['required_annotation']or len(ch['paragraphs'])!=22:raise ValueError('宋044本源角色資格')
 for p,spec in zip(ch['paragraphs'],c['paragraphs']):
  if p['id']!=spec['id']or p['mentions']!=materialize(spec['mentions'],roles):raise ValueError('宋044本源MID或角色不一致')
 people={p['id']:p for p in json.loads((root/'registry/persons.json').read_bytes())['persons']}
 for p in ch['paragraphs']:
  for m in p['mentions']:
   if m.get('source_role_key')not in ('hui','chong','shao','shiyou'):continue
   person=people[m['person_id']]
   if not any(a['surface']==m['surface']and m['id']in a['mention_ids']for a in person['aliases']):raise ValueError('宋044父叔侄反向alias')
   if not any(e.get('chapter_id')==CID and e.get('paragraph_id')==p['id']and e.get('mention_id')==m['id']for e in person['evidence']):raise ValueError('宋044父叔侄反向evidence')
 return ch,c,roles

def nephew_valid(a,paragraphs,root):
 if not isinstance(a,dict) or not isinstance(a.get('qualifiers'),dict):return False
 binding=a['qualifiers'].get('source_clause_binding')
 if not isinstance(binding,dict) or binding.get('kind')!='wyd_song044_biographical_xiongzi':return False
 try:
  ch,c,roles=_context(root)
  try:from scripts.wyd_song044_kinship import assertions
  except ImportError:from wyd_song044_kinship import assertions
  expected=[x for x in assertions(ch,roles)['assertions']if x['id'].endswith(('-shao-uncle','-shiyou-uncle'))]
  if a not in expected:return False
  for e in a['evidence']:
   hit=paragraphs.get(e['paragraph_id']);p=next(p for p in ch['paragraphs']if p['id']==e['paragraph_id'])
   if not hit or hit[0]!=CID or hit[1]!=p:return False
  return True
 except (KeyError,ValueError,TypeError,OSError,StopIteration,AttributeError):return False

def ancestor_valid(member,rows,assertions_by_id,chapters,root):
 try:
  ch,c,roles=_context(root)
  try:from scripts.wyd_song044_kinship import assertions,assembly_delta
  except ImportError:from wyd_song044_kinship import assertions,assembly_delta
  facts=assertions(ch,roles);expected=assembly_delta({'assemblies':[{'id':'family-chenjun-xie-lang','members':[]}]},None,ch,roles,facts)
  candidates=[r for r in expected['assemblies'][0]['members']if r.get('ancestor_connection')]
  if member not in candidates or ch!=chapters.get(CID):return False
  if member['ancestor_person_id']!=roles['chong']or member['parent_person_id']is not None:return False
  if any(roles[k]not in rows for k in ['hui','chong']):return False
  proof=member['ancestor_connection'];nephew=assertions_by_id.get(proof['nephew_assertion_id']);father=assertions_by_id.get(proof['uncle_father_assertion_id'])
  expected_by={a['id']:a for a in facts['assertions']}
  if nephew!=expected_by[proof['nephew_assertion_id']]or father!=expected_by[proof['uncle_father_assertion_id']]:return False
  pid=member['person_id']
  # A conflicting biological/adoptive/explicit ancestor claim cannot be silently covered.
  for a in assertions_by_id.values():
   if a.get('subject_person_id')!=pid:continue
   if a.get('predicate')in ('father','adoptive_father'):return False
   if a.get('predicate')in ('grandfather','ancestor')and a.get('object_person_id')!=roles['chong']:return False
  return nephew['subject_person_id']==pid and nephew['object_person_id']==roles['hui']and father['subject_person_id']==roles['hui']and father['object_person_id']==roles['chong']
 except (KeyError,ValueError,TypeError,OSError,StopIteration,AttributeError):return False
