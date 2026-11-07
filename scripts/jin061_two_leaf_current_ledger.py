"""Exact two-leaf current061 ledger adapter; no load_catalog/other proof dependency."""
from pathlib import Path
import copy,hashlib,json
REF="source-evidence/jin061-two-leaf-current-ledger/source-contract.json"
SHA="df462e0766bea1445ea575c6cd1428b27750897d679aa4e63fe6d31e6c319dff"
def same(a,b):
 if type(a)is not type(b):return False
 if isinstance(a,dict):return a.keys()==b.keys()and all(same(a[k],b[k])for k in a)
 if isinstance(a,list):return len(a)==len(b)and all(same(x,y)for x,y in zip(a,b))
 return a==b
def proof(root,people=None,expected_cheng=None):
 root=Path(root).resolve()
 def raw(rel):
  p=Path(rel);assert not p.is_absolute()and'..'not in p.parts;p=root/p;assert p.resolve()==p and p.is_file()and not p.is_symlink();return p.read_bytes()
 def load(rel):return json.loads(raw(rel))
 assert hashlib.sha256(raw(REF)).hexdigest()==SHA;c=load(REF)
 assert c['owner']=='jin061_current_ledger_yue_cheng_only'and c['projection_allowed_fields']==['/38/person_id','/55/person_id']
 old=raw(c['immutable_before_capture_path']);assert hashlib.sha256(old).hexdigest()==c['immutable_before_capture_sha256'];before=json.loads(old);expected=copy.deepcopy(before)
 source=load(c['native_source_path']);assert same(source['source'],c['source_metadata_before'])and same({k:source[k]for k in c['source_ids']},c['source_ids'])
 if people is None:people={p['id']:p for p in load('registry/persons.json')['persons']}
 assert[(s['role'],s['row_index'],s['entity_id'])for s in c['seeds']]==[('yue',38,'e-jin061-yue'),('cheng',55,'e-jin061-qiaowang')]
 roles={}
 for seed in c['seeds']:
  index=seed['row_index'];historical=seed['before_native_paragraph'];p,=[p for p in source['paragraphs']if p['id']==historical['id']];assert p['text']==historical['text']
  oldm,=[m for m in historical['mentions']if m['id']==seed['mention_id']];m,=[m for m in p['mentions']if m['id']==seed['mention_id']]
  assert m['kind']==oldm['kind']=='person'and same({k:v for k,v in m.items()if k!='person_id'},{k:v for k,v in oldm.items()if k!='person_id'})
  assert isinstance(before,list)and before[index]['entity_id']==seed['entity_id']and before[index]['person_id']==oldm['person_id']
  pid=m['person_id'];assert pid in people;actor=people[pid];reverse=seed['reverse_template']
  assert same({k:source[k]for k in('work_id','book_id','source_id')},{k:reverse[k]for k in('work_id','book_id','source_id')})and reverse['chapter_id']==source['id']and reverse['paragraph_id']==p['id']and reverse['mention_id']==m['id']and reverse['quote']==m['surface']
  assert[e for e in actor['evidence']if e.get('mention_id')==m['id']]==[reverse]
  assert sum(a['surface']==m['surface']and m['id']in a['mention_ids']for a in actor['aliases'])==1
  expected[index]['person_id']=pid;roles[seed['role']]=pid
 assert len(set(roles.values()))==2
 if expected_cheng is not None:assert roles['cheng']==expected_cheng
 try:from scripts.jin061_sima_current_projection import project_current_sima_leaves
 except ImportError:from jin061_sima_current_projection import project_current_sima_leaves
 expected=project_current_sima_leaves(root,expected,people)
 assert same(load(c['current_ledger_path']),expected)
 return roles
