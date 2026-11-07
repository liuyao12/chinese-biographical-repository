"""Finite current-rendered Jin038 complete units. No print or fixed-body claim."""
from pathlib import Path
import json,hashlib
REF='source-evidence/jin038-wen-nine-you-rendered/source-contract.json'
SHA='416e3a4107304fbd0c9452bdbe4243cb2cb2a431194b001c6efe54b78a2b2f54'
OWNED_PATHS=('corpus/jinshu/038-wen-nine-you-rendered.json', 'corpus/jinshu/038-wen-nine-you-name-components.json', 'corpus/jinshu/038-wen-nine-you-assertions.json')
PRONOUN_RULE={'id': 'c-jinshu-038-wen-nine-you-rendered:p002:m0358', 'start': 358, 'end': 359, 'surface': '我', 'kind': 'pronoun', 'status': 'contextual_provisional', 'note': '攸謂左右引語的第一人稱；plain rendering，不作姓名下劃線/alias，後續需有限代詞消費proof。', 'source_reference_binding': {'kind': 'jin038_wen_you_first_person', 'paragraph_id': 'c-jinshu-038-wen-nine-you-rendered:p002', 'paragraph_sha256': 'a10f4d40c106384814823ac423df43150d76d35ddf74f80b5657ab17347762bc', 'speaker_mention_id': 'c-jinshu-038-wen-nine-you-rendered:p002:m0346'}}
def _installed_without_contract(root):return any((Path(root)/p).exists()for p in OWNED_PATHS)
def source_reference(m,text=None):
 if not isinstance(m,dict):return False
 return bool(m.get('kind')=='pronoun'and isinstance(m.get('person_id'),str)and {k:v for k,v in m.items()if k!='person_id'}=={k:v for k,v in PRONOUN_RULE.items()if k!='person_id'}and(text is None or hashlib.sha256(text.encode()).hexdigest()==PRONOUN_RULE['source_reference_binding']['paragraph_sha256']))
def same(a,b):
 if type(a)is not type(b):return False
 if type(a)is dict:return a.keys()==b.keys()and all(same(a[k],b[k])for k in a)
 if type(a)is list:return len(a)==len(b)and all(same(x,y)for x,y in zip(a,b))
 return a==b
def _raw(root,p):
 root=Path(root).resolve();rel=Path(p);assert not rel.is_absolute()and'..'not in rel.parts;f=root/rel;assert f.resolve()==f;return f.read_bytes()
def _proof(raw,people=None,records=None):
 cb=raw(REF);assert hashlib.sha256(cb).hexdigest()==SHA;c=json.loads(cb);load=lambda p:json.loads(raw(p));chs=[load('corpus/jinshu/038-wen-nine-you-rendered.json')];ms={m['id']:(ch,p,m)for ch in chs for p in ch['paragraphs']for m in p['mentions']}
 physical={p['id']:p for p in load('registry/persons.json')['persons']}
 if people is None:people=physical
 roles={}
 for r,mids in c['role_current_mids'].items():
  pid=ms[mids[0]][2]['person_id'];assert type(pid)is str and pid in people and pid in physical and same(people[pid],physical[pid]);roles[r]=pid
  for mid in mids:
   ch,p,m=ms[mid];assert m['person_id']==pid and p['text'][m['start']:m['end']]==m['surface'];e={k:ch[k]for k in('work_id','book_id','source_id')};e.update(chapter_id=ch['id'],paragraph_id=p['id'],mention_id=mid,quote=m['surface']);assert[e0 for e0 in people[pid]['evidence']if e0.get('mention_id')==mid]==[e]
   als=[(a['surface'],x)for a in people[pid]['aliases']for x in a['mention_ids']if x==mid]
   assert als==([(m['surface'],mid)]if m['kind']=='person'else[])
  if r not in c['existing_role_seeds']:continue
  seed=c['existing_role_seeds'][r];old=load(seed['path']);p=next(p for p in old['paragraphs']if p['id']==seed['paragraph_id']);m=next(m for m in p['mentions']if m['id']==seed['marker']['id']);assert hashlib.sha256(p['text'].encode()).hexdigest()==seed['paragraph_sha256']and{k:v for k,v in m.items()if k!='person_id'}==seed['marker']and m['person_id']==pid
  assert[e for e in people[pid]['evidence']if e.get('mention_id')==m['id']]==[seed['reverse']]
 assert len(set(roles.values()))==len(roles)
 def expand(v):
  if isinstance(v,dict)and set(v)=={'$current_role'}:return roles[v['$current_role']]
  if isinstance(v,str):return v
  if isinstance(v,list):return[expand(x)for x in v]
  if isinstance(v,dict):return{k:expand(x)for k,x in v.items()}
  return v
 expected={p:expand(v)for p,v in c['expected_documents'].items()}
 for path,want in expected.items():assert same(load(path),want)
 # new_role_metadata remains the byte-preserved historical registration snapshot.
 # Current rows are authoritative only after strict caller/physical equality above;
 # all source-owned MID, alias, name and relation proofs remain mandatory.
 for path,digest in c['raw_sources'].items():assert hashlib.sha256(raw(path)).hexdigest()==digest
 if records is not None:
  cs={ch['id']for ch in chs};docs=[d for d in records if d.get('id')in cs or d.get('chapter_id')in cs or d.get('record_type')=='person_name_component_set'and any(n.get('chapter_id')in cs for n in d.get('records',[]))];assert len(docs)==len(expected)and all(sum(same(d,w)for d in docs)==1 for w in expected.values())
 return c,roles,expected

def proof(root,people=None,records=None):
 return _proof(lambda p:_raw(root,p),people,records)

def errors(root):
 if not(Path(root)/REF).exists():return['晉038九男/攸來源或側錄已安裝但缺少所屬contract']if _installed_without_contract(root)else[]
 try:proof(root);return[]
 except(AssertionError,KeyError,TypeError,ValueError,StopIteration,OSError):return['晉038九男/攸完整原段/具體角色/姓名字/父系與收繼/雙端反查不符']
def guard_bundle(root,pid,people,records):
 if not(Path(root)/REF).exists():
  if _installed_without_contract(root):raise ValueError('Jin038 source/sidecar installed without contract')
  return
 c=json.loads(_raw(root,REF));cs=[json.loads(_raw(root,'corpus/jinshu/038-wen-nine-you-rendered.json'))];owners={m['person_id']for ch in cs for p in ch['paragraphs']for m in p['mentions']if m.get('person_id')};cids={ch['id']for ch in cs}
 for d in records:
  if d.get('chapter_id')in cids:
   owners.update(a.get(k)for a in d.get('assertions',[])for k in('subject_person_id','object_person_id'))
  if d.get('record_type')=='person_name_component_set':owners.update(n.get('person_id')for n in d.get('records',[])if n.get('chapter_id')in cids)
 if pid in owners:proof(root,people,records)
def validate_surname(n,names,chapters,assertions,root):
 c,r,e=proof(root);assert any(same(n,x)for d in e.values()if d.get('record_type')=='person_name_component_set'for x in d['records']);return None
def family_valid(a,root):
 try:c,r,e=proof(root);return any(same(a,x)for d in e.values()if d.get('record_type')=='person_assertion_set'for x in d['assertions'])
 except(AssertionError,KeyError,TypeError,ValueError,StopIteration,OSError):return False