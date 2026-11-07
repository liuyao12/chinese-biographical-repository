"""Finite Jin035 classical allusion successor; complete source before parent view."""
from pathlib import Path
import json,hashlib,copy
CASE='source-evidence/jin035-peixiu-peiwei/allusion-ner-contract.json'
CASE_SHA='473d702191971ad876a615392763240f9ae93466810f901116e965e9267f6991'
def same(a,b):
 if type(a)is not type(b):return False
 if isinstance(a,dict):return a.keys()==b.keys()and all(same(a[k],b[k])for k in a)
 if isinstance(a,list):return len(a)==len(b)and all(same(x,y)for x,y in zip(a,b))
 return a==b
def validate_successor(root, chapter_override=None):
 root=Path(root).resolve();read=lambda rel:json.loads((root/rel).read_text());raw=(root/CASE).read_bytes();assert hashlib.sha256(raw).hexdigest()==CASE_SHA;case=json.loads(raw)
 assert hashlib.sha256((root/case['parent_contract_path']).read_bytes()).hexdigest()==case['parent_contract_sha256']
 assert hashlib.sha256((root/case['projection_path']).read_bytes()).hexdigest()==case['projection_sha256']
 assert hashlib.sha256((root/case['raw_file']).read_bytes()).hexdigest()==case['raw_sha256']
 ch=chapter_override if chapter_override is not None else read(case['chapter_path']);people={p['id']:p for p in read('registry/persons.json')['persons']};anchors={m['id']:(p,m)for p in ch['paragraphs']for m in p['mentions']};roles={}
 for key,seed in case['known_seeds'].items():
  d=read(seed['chapter_path']);assert same(d['source'],seed['source'])and same({k:d[k]for k in seed['dimensions']},seed['dimensions'])
  p=next(p for p in d['paragraphs']if p['id']==seed['paragraph_id']);m=next(m for m in p['mentions']if m['id']==seed['marker']['id']);assert p['text']==seed['quote']and same({k:v for k,v in m.items()if k!='person_id'},seed['marker'])
  pid=m['person_id'];assert m['kind']=='person'and pid in people;roles['$'+key]=pid
  e=seed['reverse'];assert same([x for x in people[pid].get('evidence',[])if x.get('mention_id')==m['id']],[e]);assert any(a['surface']==m['surface']and m['id']in a['mention_ids']for a in people[pid]['aliases'])
 def expand(x):
  if isinstance(x,str):return roles.get(x,x)
  if isinstance(x,list):return[expand(v)for v in x]
  if isinstance(x,dict):return{k:expand(v)for k,v in x.items()}
  return x
 assert same(ch,expand(case['chapter_template']))
 sidecars={rel:expand(t)for rel,t in case['sidecars'].items()}
 for rel,expected in sidecars.items():assert same(read(rel),expected)
 for p in ch['paragraphs']:
  for m in p['mentions']:
   assert p['text'][m['start']:m['end']]==m['surface']
   if m['kind']=='person':
    person=people[m['person_id']];e={k:ch[k]for k in ('work_id','book_id','source_id')};e.update(chapter_id=ch['id'],paragraph_id=p['id'],mention_id=m['id'],quote=m['surface']);assert same([v for v in person['evidence']if v.get('mention_id')==m['id']],[e]);assert any(a['surface']==m['surface']and m['id']in a['mention_ids']for a in person['aliases'])
   else:
    assert m['kind']=='unresolved'and m['person_id']is None and m['status']=='unresolved'
    assert all(pid in people for pid in m.get('candidate_person_ids',[]))
 added=set(case['new_marker_ids']);assert len(added)==46 and added<=anchors.keys();assert sum(anchors[mid][1]['kind']=='person'for mid in added)==24
 old=copy.deepcopy(ch);old['annotation']=expand(case['parent_annotation'])
 for p in old['paragraphs']:
  p['mentions']=[m for m in p['mentions']if m['id']not in added]
  if p['id']in case['parent_paragraph_annotation_status']:p['annotation_status']=case['parent_paragraph_annotation_status'][p['id']]
 assert {m['id']for p in old['paragraphs']for m in p['mentions']}==set(case['preserved_parent_marker_ids'])
 return {'chapter':ch,'parent_chapter':old,'sidecars':sidecars,'case':case}
