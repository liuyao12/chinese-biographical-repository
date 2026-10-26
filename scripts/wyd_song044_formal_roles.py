"""Exact first-pass individual role layer for one immutable WYD044 witness."""
import json,hashlib
from pathlib import Path
try:from scripts.wyd_song044_formal_model import resolve_existing,local_current
except ImportError:from wyd_song044_formal_model import resolve_existing,local_current
try:from scripts.wyd_song044_role_seed import materialize
except ImportError:from wyd_song044_role_seed import materialize
CID='c-songshu-044-wyd1739-xiehui';REF='source-evidence/song044-wyd1739-xiehui/formal-role-contract.json';CONTRACT_SHA='2b1bc6f3dc350c2450fa2e86feff969faaa3a3b1fd6b8870f7149e53003b9973'
def source_errors(ch,root):
 if not isinstance(ch,dict):return ['宋044正式角色：須為物件']
 if ch.get('id')!=CID:return []
 try:
  try:from scripts.fixed_wuyingdian_song044 import validate_source
  except ImportError:from fixed_wuyingdian_song044 import validate_source
  validate_source(ch,root)
  if all(p.get('annotation_status')=='pending'and not p.get('mentions')for p in ch['paragraphs']):return []
  raw=(Path(root)/REF).read_bytes()
  if hashlib.sha256(raw).hexdigest()!=CONTRACT_SHA:raise ValueError('契約SHA')
  c=json.loads(raw);roles=resolve_existing(root,c);local=local_current(root,c)
  if len(roles)!=51 or len(local)!=45:raise ValueError('來源角色未全登記')
  roles.update(local)
  if ch['annotation']!=c['required_annotation']or len(ch['paragraphs'])!=22:raise ValueError('分層或資格漂移')
  people={p['id']:p for p in json.loads((Path(root)/'registry/persons.json').read_bytes())['persons']}
  for p,s in zip(ch['paragraphs'],c['paragraphs']):
   if p['id']!=s['id']or p['mentions']!=materialize(s['mentions'],roles)or p['annotation_status']!=s['annotation_status']:raise ValueError('固定MID/角色/未定漂移')
   for m in p['mentions']:
    if m['kind']!='person':
     if m.get('person_id')is not None:raise ValueError('非人物帶人物號')
     continue
    person=people[m['person_id']]
    if not any(a['surface']==m['surface']and m['id']in a['mention_ids']for a in person['aliases']):raise ValueError('缺反向alias')
    e={'work_id':ch['work_id'],'book_id':ch['book_id'],'source_id':ch['source_id'],'chapter_id':ch['id'],'paragraph_id':p['id'],'mention_id':m['id'],'quote':m['surface']}
    if e not in person['evidence']:raise ValueError('缺反向evidence')
  return []
 except (KeyError,ValueError,TypeError,OSError,StopIteration,AttributeError)as error:return ['宋044正式角色：'+str(error)]
