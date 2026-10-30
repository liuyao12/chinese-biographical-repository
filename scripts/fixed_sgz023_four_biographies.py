"""Finite complete SGZ023 named-person continuation; no runtime historical inference."""
import json,hashlib,copy
from pathlib import Path
REF='source-evidence/sgz023-peiqian-ws2376966/four-biographies-ner-contract.json'
SHA='b76ed936e0893b195486d25eb877e4e020f128ad46216b2158ab18d07253a16c'

def same(a,b):
 if type(a)is not type(b):return False
 if isinstance(a,dict):return a.keys()==b.keys()and all(same(a[k],b[k])for k in a)
 if isinstance(a,list):return len(a)==len(b)and all(same(x,y)for x,y in zip(a,b))
 return a==b

def _base_proof(root,chapter_override=None):
 root=Path(root).resolve();read=lambda rel:json.loads((root/rel).read_text());raw=(root/REF).read_bytes();assert hashlib.sha256(raw).hexdigest()==SHA;c=json.loads(raw);ch=read(c['chapter_path'])if chapter_override is None else chapter_override;people={p['id']:p for p in read('registry/persons.json')['persons']};anchors={m['id']:(p,m)for p in ch['paragraphs']for m in p['mentions']};roles={}
 assert hashlib.sha256((root/c['parent_contract_path']).read_bytes()).hexdigest()==c['parent_contract_sha256']
 for rel,sha in c['external_readings'].items():assert hashlib.sha256((root/rel).read_bytes()).hexdigest()==sha
 for key,s in c['source_seeds'].items():
  if s['kind']=='new_source_local':
   p,m=anchors[s['first_mid']];pid=m['person_id'];assert m['kind']=='person'and pid in people and people[pid]['label']==s['label']
  else:
   d=read(s['path']);assert same(d['source'],s['source'])and same({k:d[k]for k in s['dimensions']},s['dimensions']);p=next(p for p in d['paragraphs']if p['id']==s['paragraph_id']);m=next(m for m in p['mentions']if m['id']==s['marker']['id']);assert p['text']==s['quote']and same({k:v for k,v in m.items()if k!='person_id'},s['marker']);pid=m['person_id'];assert pid in people and m['kind']=='person';assert [e for e in people[pid]['evidence']if e.get('mention_id')==m['id']]==[s['reverse']];assert any(a['surface']==m['surface']and m['id']in a['mention_ids']for a in people[pid]['aliases'])
  roles['$'+key]=pid
 assert len(roles.values())==len(set(roles.values()))
 def expand(x):
  if isinstance(x,str):return roles.get(x,x)
  if isinstance(x,list):return[expand(v)for v in x]
  if isinstance(x,dict):return{k:expand(v)for k,v in x.items()}
  return x
 assert same(ch,expand(c['chapter_template']))
 for role,t in c['new_people'].items():
  person=people[roles[role]];expected=expand(t);assert all(same(person.get(k),v)for k,v in expected.items()if k not in ('aliases','evidence'))
 sidecars={rel:expand(t)for rel,t in c['sidecars'].items()}
 for rel,t in sidecars.items():assert same(read(rel),t)
 for p in ch['paragraphs']:
  for m in p['mentions']:
   assert p['text'][m['start']:m['end']]==m['surface']
   if m['kind']=='person':
    person=people[m['person_id']];e={k:ch[k]for k in('work_id','book_id','source_id')};e.update(chapter_id=ch['id'],paragraph_id=p['id'],mention_id=m['id'],quote=m['surface']);assert [v for v in person['evidence']if v.get('mention_id')==m['id']]==[e];assert any(a['surface']==m['surface']and m['id']in a['mention_ids']for a in person['aliases'])
   else:assert m['kind']=='unresolved'and m['person_id']is None and m['status']=='unresolved'
 bad=expand(c['bad_original_marker']);badid=bad['id'];assert badid not in anchors
 assert not any(e.get('mention_id')==badid for p in people.values()for e in p['evidence']);assert not any(badid in a['mention_ids']for p in people.values()for a in p['aliases'])
 old=copy.deepcopy(ch);old['annotation']=expand(c['parent_annotation']);added=set(c['new_marker_ids'])
 for p in old['paragraphs']:
  p['mentions']=[m for m in p['mentions']if m['id']not in added]
  if p['id']==badid.rsplit(':',1)[0]:p['mentions'].append(bad);p['mentions'].sort(key=lambda x:x['start'])
  status=c['parent_paragraph_status'][p['id']]
  if status is None:p.pop('annotation_status',None)
  else:p['annotation_status']=status
 assert {m['id']for p in old['paragraphs']for m in p['mentions']}==set(c['preserved_parent_ids'])|{badid}
 # Historical parent proof needs its former erroneous reverse only in this isolated view.
 parent_people=copy.deepcopy(people);person=parent_people[bad['person_id']];person['evidence'].append(c['bad_original_reverse']);a=next((a for a in person['aliases']if a['surface']==bad['surface']),None)
 if a:a['mention_ids'].append(badid)
 else:person['aliases'].append({'surface':bad['surface'],'mention_ids':[badid]})
 return {'chapter':ch,'parent_chapter':old,'parent_people':parent_people,'parent_sidecars':{rel:expand(t)for rel,t in c['parent_sidecars'].items()},'sidecars':sidecars,'people':people,'case':c}

def proof(root):
 if (Path(root)/'source-evidence/sgz023-peiqian-ws2376966/work-author-contract.json').exists():
  try:from scripts.fixed_sgz023_works import proof as typed_proof
  except ImportError:from fixed_sgz023_works import proof as typed_proof
  return typed_proof(root)
 return _base_proof(root)

def guard_bundle(root,pid,people,records):
 path=Path(root)/REF
 if not path.exists():return
 ch=json.loads((Path(root)/'corpus/sanguozhi/023-peiqian-ws2376966.json').read_text());relevant=any(m.get('person_id')==pid for p in ch['paragraphs']for m in p['mentions'])or any(e.get('chapter_id')==ch['id']for e in people.get(pid,{}).get('evidence',[]))
 if not relevant:return
 state=proof(root)
 if ch['annotation'].get('two_hui_identity_adopted'):
  try:from scripts.two_hui_identity import validate as validate_hui
  except ImportError:from two_hui_identity import validate as validate_hui
  joined=validate_hui(root,ch)
  assert '047_850_e7d'not in people and same(people.get(joined),state['people'][joined])
  identity=json.loads((Path(root)/'corpus/sanguozhi/023-peiqian-ws2376966-identities.json').read_text())
  assert sum(same(r,identity)for r in records)==1
 try:from scripts.fixed_sgz023_peiqian import _base_validate
 except ImportError:from fixed_sgz023_peiqian import _base_validate
 _base_validate(state['parent_chapter'],root,state['parent_people'],state['parent_sidecars'])
 assert sum(same(r,ch)for r in records)==1
 for doc in state['sidecars'].values():assert sum(same(r,doc)for r in records)==1
 parent=json.loads((Path(root)/state['case']['parent_contract_path']).read_text())
 for rel in parent['sidecar_templates']:
  expected=json.loads((Path(root)/rel).read_text());assert sum(same(r,expected)for r in records)==1
 for p in ch['paragraphs']:
  for m in p['mentions']:
   if m['kind']!='person':continue
   person=people[m['person_id']];e={k:ch[k]for k in('work_id','book_id','source_id')};e.update(chapter_id=ch['id'],paragraph_id=p['id'],mention_id=m['id'],quote=m['surface']);assert [v for v in person['evidence']if v.get('mention_id')==m['id']]==[e]and any(a['surface']==m['surface']and m['id']in a['mention_ids']for a in person['aliases'])
