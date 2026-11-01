"""Finite received Jin038 six complete units; current source roles, not PID rules."""
from pathlib import Path
import json,hashlib
REF='source-evidence/jin038-wen-children-rendered/source-contract.json'
SHA='842b2a8073f59897f389ee7069347c80f2bda7c9a545848490e1360b2597604b'
CH='corpus/jinshu/038-wen-children-rendered.json'
OWNED_PATHS=('corpus/jinshu/038-wen-children-rendered.json', 'corpus/jinshu/038-wen-children-name-components.json', 'corpus/jinshu/038-wen-children-assertions.json', 'corpus/jinshu/038-wen-children-identities.json')
PRONOUN_RULE={'id': 'c-jinshu-038-wen-children-rendered:p006:m0079', 'start': 79, 'end': 80, 'surface': '吾', 'kind': 'pronoun', 'status': 'contextual_provisional', 'source_reference_binding': {'kind': 'jin038_wen_children_source_first_person', 'paragraph_id': 'c-jinshu-038-wen-children-rendered:p006', 'paragraph_sha256': 'fdec12cbf6d7641bb533163cbf1d5b512827e95095a0655d80223ebecddd6e22', 'speaker_role': 'yan'}, 'note': '延祚傳詔太康脈絡的武帝第一人稱；不作姓名alias/下劃線。'}
def same(a,b):
 if type(a)is not type(b):return False
 if type(a)is dict:return a.keys()==b.keys()and all(same(a[k],b[k])for k in a)
 if type(a)is list:return len(a)==len(b)and all(same(x,y)for x,y in zip(a,b))
 return a==b
def source_reference(m,text=None):
 return isinstance(m,dict)and isinstance(m.get('person_id'),str)and same({k:v for k,v in m.items()if k!='person_id'},PRONOUN_RULE)and(text is None or hashlib.sha256(text.encode()).hexdigest()==PRONOUN_RULE['source_reference_binding']['paragraph_sha256'])
def _raw(root,p):
 root=Path(root).resolve();rel=Path(p);assert not rel.is_absolute()and'..'not in rel.parts;f=root/rel;assert f.resolve()==f;return f.read_bytes()
def _installed(root):return any((Path(root)/p).exists()for p in OWNED_PATHS)
def _proof(raw,people=None,records=None):
 cb=raw(REF);assert hashlib.sha256(cb).hexdigest()==SHA;c=json.loads(cb);load=lambda p:json.loads(raw(p));ch=load(CH);ms={m['id']:(p,m)for p in ch['paragraphs']for m in p['mentions']};physical={p['id']:p for p in load('registry/persons.json')['persons']}
 if people is None:people=physical
 roles={}
 for role,mids in c['role_current_mids'].items():
  pid=ms[mids[0]][1]['person_id'];assert type(pid)is str and pid in people and same(people[pid],physical[pid]);roles[role]=pid
  for mid in mids:
   p,m=ms[mid];assert m['person_id']==pid and type(m['start'])is int and type(m['end'])is int and p['text'][m['start']:m['end']]==m['surface'];e={k:ch[k]for k in('work_id','book_id','source_id')};e.update(chapter_id=ch['id'],paragraph_id=p['id'],mention_id=mid,quote=m['surface']);assert same([x for x in people[pid]['evidence']if x.get('mention_id')==mid],[e]);als=[(a['surface'],x)for a in people[pid]['aliases']for x in a['mention_ids']if x==mid];assert als==([(m['surface'],mid)]if m['kind']=='person'else[])
  if role not in c['existing_role_seeds']:continue
  seed=c['existing_role_seeds'][role];old=load(seed['path']);p=next(p for p in old['paragraphs']if p['id']==seed['paragraph_id']);m=next(m for m in p['mentions']if m['id']==seed['marker']['id']);assert hashlib.sha256(p['text'].encode()).hexdigest()==seed['paragraph_sha256']and same({k:v for k,v in m.items()if k!='person_id'},seed['marker'])and m['person_id']==pid;assert same([e for e in people[pid]['evidence']if e.get('mention_id')==m['id']],[seed['reverse']])
 assert len(set(roles.values()))==len(roles)
 def expand(v):
  if type(v)is dict and set(v)=={'$current_role'}:return roles[v['$current_role']]
  if type(v)is dict:return{k:expand(x)for k,x in v.items()}
  if type(v)is list:return[expand(x)for x in v]
  return v
 expected={p:expand(v)for p,v in c['expected_documents'].items()}
 for path,want in expected.items():assert same(load(path),want)
 assert same(load(c['ordinal_report_path']),expand(c['expected_ordinal_reports']))
 for path,digest in c['raw_sources'].items():assert hashlib.sha256(raw(path)).hexdigest()==digest
 if records is not None:
  cid=ch['id'];docs=[d for d in records if d.get('id')==cid or d.get('chapter_id')==cid or d.get('record_type')=='person_name_component_set'and any(n.get('chapter_id')==cid for n in d.get('records',[]))];assert len(docs)==len(expected)and all(sum(same(d,w)for d in docs)==1 for w in expected.values())
 return c,roles,expected
def proof(root,people=None,records=None):return _proof(lambda p:_raw(root,p),people,records)
def errors(root):
 if not(Path(root)/REF).exists():return['晉038六選段已安裝但缺完整來源契約']if _installed(root)else[]
 try:proof(root);return[]
 except(AssertionError,KeyError,TypeError,ValueError,StopIteration,OSError):return['晉038六選段原文/具體角色/生父與宗祀/明示報序/姓名字/雙端反查不符']
def guard_bundle(root,pid,people,records):
 if not(Path(root)/REF).exists():
  if _installed(root):raise ValueError('Jin038 children installed without source contract')
  return
 cb=_raw(root,REF)
 if hashlib.sha256(cb).hexdigest()!=SHA:raise ValueError('Jin038 source contract checksum mismatch')
 c=json.loads(cb);physical=[json.loads(_raw(root,r))for r in c['expected_documents']];ch=next(d for d in physical if d.get('record_type')=='marked_chapter');cid=ch['id'];mids={m['id']for p in ch['paragraphs']for m in p['mentions']}
 def rows(d,key):
  v=d.get(key,[]);return v if isinstance(v,list)else[]
 def related(d):
  if not isinstance(d,dict):return False
  return(d.get('id')==cid or d.get('chapter_id')==cid or d.get('record_type')=='person_name_component_set'and any(isinstance(n,dict)and n.get('chapter_id')==cid for n in rows(d,'records'))or any(isinstance(m,dict)and isinstance(m.get('id'),str)and m.get('id')in mids for p in rows(d,'paragraphs')if isinstance(p,dict)for m in rows(p,'mentions')))
 def owners(documents):
  result=set()
  def visit(v):
   if isinstance(v,dict):
    for key,value in v.items():
     if isinstance(key,str)and(key=='person_id'or key.endswith('_person_id'))and isinstance(value,str):result.add(value)
     elif isinstance(key,str)and(key=='person_ids'or key.endswith('_person_ids'))and isinstance(value,list):result.update(x for x in value if isinstance(x,str))
     visit(value)
   elif isinstance(v,list):
    for item in v:visit(item)
  visit(documents)
  return result
 selected=[d for d in(records or[])if related(d)];physical_owners=owners(physical);caller_owners=owners(selected);caller_person=people.get(pid,{})if isinstance(people,dict)else{};caller_reverse_claim=(isinstance(caller_person,dict)and any(isinstance(e,dict)and(isinstance(e.get('mention_id'),str)and e.get('mention_id')in mids or e.get('chapter_id')==cid)for e in rows(caller_person,'evidence')))
 if pid not in physical_owners|caller_owners and not caller_reverse_claim:return
 if pid not in physical_owners or len(selected)!=len(physical)or any(sum(same(d,want)for d in selected)!=1 for want in physical):raise ValueError('Jin038 caller/physical source catalogue mismatch')
 proof(root,people,records)

def validate_surname(n,names,chapters,assertions,root):
 c,r,e=proof(root);assert any(same(n,x)for d in e.values()if d.get('record_type')=='person_name_component_set'for x in d['records']);return None
def family_valid(a,root):
 try:c,r,e=proof(root);return any(same(a,x)for d in e.values()if d.get('record_type')=='person_assertion_set'for x in d['assertions'])
 except(AssertionError,KeyError,TypeError,ValueError,StopIteration,OSError):return False

def ordinal_reports(root,ids):
 if not(Path(root)/REF).exists():
  if _installed(root):raise ValueError('Jin038 children ordinal source installed without contract')
  return[]
 c=json.loads(_raw(root,REF));ch=json.loads(_raw(root,CH));ms={m['id']:m for p in ch['paragraphs']for m in p['mentions']};owned={ms[c['role_current_mids'][r][0]]['person_id']for r in c['ordinal_report_roles']}
 if not set(ids).intersection(owned):return[]
 c,r,e=proof(root);return[x for x in json.loads(_raw(root,c['ordinal_report_path']))['reports']if x['person_id']in ids]
