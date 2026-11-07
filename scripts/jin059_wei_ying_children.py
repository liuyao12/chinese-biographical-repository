"""Finite fixed Jin059 source unit and editable AI reading; IDs follow current MIDs.
Raw conservation, editorial source-role interpretation and caller consistency are
separate checks. No registry row is frozen into the historical reading contract.
"""
from pathlib import Path
import hashlib,json
from functools import lru_cache
REF='source-evidence/sima-family-source-bridges/jin059-children-source-contract.json'
SHA='b7ceaf30b31907c3b9c4403ba6f33508530db2fa2a672495d85af53e4ff0500c'
CID='c-jinshu-059-wei-ying-children'
OWNED=('corpus/jinshu/059-wei-ying-children-fixed.json','corpus/jinshu/059-wei-ying-children-fixed-assertions.json','corpus/jinshu/059-wei-ying-children-fixed-name-components.json','corpus/jinshu/059-wei-ying-children-fixed.xml','source-evidence/sima-family-source-bridges/jin059-children-fixed-units.json','source-evidence/sima-family-source-bridges/jin059-identity-reference-qualifications.json')
TYPED=frozenset(('person_id','subject_person_id','object_person_id','father_person_id','mother_person_id','parent_person_id','preferred_person_id','other_current_person_id'))
def same(a,b):
 if type(a)is not type(b):return False
 if type(a)is dict:return a.keys()==b.keys()and all(same(v,b[k])for k,v in a.items())
 if type(a)is list:return len(a)==len(b)and all(same(x,y)for x,y in zip(a,b))
 return a==b if type(a)in(str,int,float,bool,type(None))else False
def _raw(root,path):
 root=Path(root).resolve();rel=Path(path);assert not rel.is_absolute()and'..'not in rel.parts
 p=root/rel;assert p.resolve()==p;return p.read_bytes()
def _reverse(ch,p,m):return dict(work_id=ch['work_id'],book_id=ch['book_id'],source_id=ch['source_id'],chapter_id=ch['id'],paragraph_id=p['id'],mention_id=m['id'],quote=m['surface'])
def _mark(ch,paragraph_id,mid):
 ps=[p for p in ch['paragraphs']if p['id']==paragraph_id];assert len(ps)==1;p=ps[0];mm=[m for m in p['mentions']if m['id']==mid];assert len(mm)==1;m=mm[0]
 assert type(m['start'])is int and type(m['end'])is int and 0<=m['start']<m['end']<=len(p['text'])and p['text'][m['start']:m['end']]==m['surface']
 return p,m
def _reciprocal(person,ch,p,m):
 assert same([e for e in person.get('evidence',[])if e.get('mention_id')==m['id']],[_reverse(ch,p,m)])
 a=[a for a in person.get('aliases',[])if m['id']in a.get('mention_ids',[])];assert len(a)==1 and a[0]['surface']==m['surface']and a[0]['mention_ids'].count(m['id'])==1

def _proof(raw,people=None,records=None):
 cb=raw(REF);assert hashlib.sha256(cb).hexdigest()==SHA;c=json.loads(cb);load=lambda p:json.loads(raw(p));ch=load(c['chapter_path']);physical_people={p['id']:p for p in load('registry/persons.json')['persons']}
 assert len(physical_people)==len(load('registry/persons.json')['persons'])
 if people is None:people=physical_people
 ms={m['id']:(p,m)for p in ch['paragraphs']for m in p['mentions']};assert len(ms)==sum(len(p['mentions'])for p in ch['paragraphs'])==47
 roles={}
 for role,mids in c['role_current_mids'].items():
  assert mids;pid=ms[mids[0]][1]['person_id'];assert type(pid)is str and pid in physical_people
  assert all(ms[mid][1]['kind']=='person'and ms[mid][1]['source_role']==role and ms[mid][1]['person_id']==pid for mid in mids);roles[role]=pid
 assert set(ms)=={mid for mids in c['role_current_mids'].values()for mid in mids}
 # Independent source seed markers determine current IDs; only declared endpoint
 # fields may differ from the role-neutral editorial template.
 for key,s in c['role_seeds'].items():
  role=s.get('role',key);q=load(s['chapter_path']);p,m=_mark(q,s['paragraph_id'],s['marker']['id']);assert hashlib.sha256(p['text'].encode()).hexdigest()==s['paragraph_sha256']and same({k:v for k,v in m.items()if k!='person_id'},s['marker'])
  pid=m['person_id'];assert type(pid)is str and pid in physical_people
  if role in roles:assert roles[role]==pid
  else:roles[role]=pid
  assert same(_reverse(q,p,m),s['reverse']);_reciprocal(physical_people[pid],q,p,m)
 allowed={frozenset(pair)for pair in c['allowed_possible_same_role_pairs']};rolekeys=list(roles)
 for i,r in enumerate(rolekeys):
  for other in rolekeys[i+1:]:assert roles[r]!=roles[other]or frozenset((r,other))in allowed
 def expand(x,key=None):
  if type(x)is dict:return{k:expand(v,k)for k,v in x.items()}
  if type(x)is list:return[expand(v,key)for v in x]
  if key in TYPED and type(x)is str and x.startswith('@person:'):return roles[x[8:]]
  return x
 expected={path:expand(d)for path,d in c['expected_documents'].items()}
 for path,want in expected.items():assert same(load(path),want)
 for path,want in c['expected_reference_documents'].items():assert same(load(path),expand(want))
 rawbytes=raw(c['raw_path']);assert hashlib.sha256(rawbytes).hexdigest()==c['raw_sha256'];text=rawbytes.decode('utf-8')
 for path,key in((c['units_path'],'units_sha256'),):assert hashlib.sha256(raw(path)).hexdigest()==c[key]
 cap=load(c['units_path']);assert len(cap['units'])==len(ch['paragraphs'])==2
 for p,u in zip(ch['paragraphs'],cap['units']):
  assert text[u['raw_start']:u['raw_end']]==u['raw_paragraph']==text.splitlines()[u['raw_line_number']-1]
  offsets=u['raw_character_offsets'];assert all(type(i)is int and u['raw_start']<=i<u['raw_end']for i in offsets)and offsets==sorted(set(offsets))
  assert ''.join(text[i]for i in offsets)==u['received_text']==p['text']
  assert hashlib.sha256(p['text'].encode()).hexdigest()==u['received_text_sha256']
 assert ch['text_sha256']==hashlib.sha256('\n\n'.join(p['text']for p in ch['paragraphs']).encode()).hexdigest()
 for role,mids in c['role_current_mids'].items():
  pid=roles[role]
  for mid in mids:
   p,m=ms[mid];_mark(ch,p['id'],mid);_reciprocal(physical_people[pid],ch,p,m)
 # Reject reverse-only theft too: a source MID has exactly one physical owner.
 for mid in ms:
  expected_pid=ms[mid][1]['person_id'];assert [pid for pid,p in physical_people.items()if any(e.get('mention_id')==mid for e in p.get('evidence',[]))]==[expected_pid]
  assert [pid for pid,p in physical_people.items()if any(mid in a.get('mention_ids',[])for a in p.get('aliases',[]))]==[expected_pid]
 # The surname bridge is a finite literal-surname source + direct father chain,
 # not a structural-ID, title, label or speculative remote genealogy inference.
 root_seed=c['role_seeds'][c['surname_root_role']];q=load(root_seed['chapter_path']);p,_=_mark(q,root_seed['paragraph_id'],root_seed['marker']['id']);assert c['surname_source_clause']in p['text']
 for link in c['paternal_chain']:
  want=expand(link['assertion']);assert sum(same(a,want)for a in load(link['path'])['assertions'])==1
  assert want['predicate']=='father'and want['status']=='source_attested'and want['subject_person_id']==roles[link['child']]and want['object_person_id']==roles[link['parent']]
  for e in want['evidence']:
   s=next(s for s in c['role_seeds'].values()if s['marker']['id']==e['subject_person_mention_id']);src=load(s['chapter_path']);assert e['quote']==next(p['text']for p in src['paragraphs']if p['id']==e['paragraph_id'])
 for role,literal in c['literal_names'].items():assert any(n.get('person_id')==roles[role]and n.get('surname')==literal['surname']and n.get('ming')==literal['ming']for d in expected.values()if d.get('record_type')=='person_name_component_set'for n in d['records'])
 if records is not None:
  selected=[d for d in records if related(d)];assert len(selected)==len(expected)and all(sum(same(d,w)for d in selected)==1 for w in expected.values())
 # Caller current rows must match physical CURRENT rows including unknown fields.
 # This comparison is intentionally outside the immutable source contract.
 for pid in roles.values():assert pid in people and same(people[pid],physical_people[pid])
 return c,roles,expected

def proof(root,people=None,records=None):return _proof(lambda path:_raw(root,path),people,records)
def related(d):
 if type(d)is not dict:return False
 return d.get('id')==CID or d.get('chapter_id')==CID or any(type(m)is dict and type(m.get('id'))is str and m['id'].startswith(CID+':')for p in d.get('paragraphs',[])if type(p)is dict for m in p.get('mentions',[]))or any(type(n)is dict and n.get('chapter_id')==CID for n in d.get('records',[]))
def owners(ds):
 out=set()
 def visit(x,key=None):
  if type(x)is dict:
   for k,v in x.items():visit(v,k)
  elif type(x)is list:
   for v in x:visit(v,key)
  elif key in TYPED and type(x)is str:out.add(x)
 visit(ds);return out
def _claiming(people):
 return {pid for pid,p in people.items()if any(type(e.get('mention_id'))is str and e['mention_id'].startswith(CID+':')for e in p.get('evidence',[]))or any(type(mid)is str and mid.startswith(CID+':')for a in p.get('aliases',[])for mid in a.get('mention_ids',[]))}
def _caller_claims(people,pid):
 # Exactly the requested membership predicate; never cache caller-owned rows.
 if pid not in people:return False
 p=people[pid]
 return any(type(e.get('mention_id'))is str and e['mention_id'].startswith(CID+':')for e in p.get('evidence',[]))or any(type(mid)is str and mid.startswith(CID+':')for a in p.get('aliases',[])for mid in a.get('mention_ids',[]))
@lru_cache(maxsize=2)
def _physical_claimants(registry_bytes):
 # Full actual bytes are the key; only immutable membership leaves this parser.
 people={p['id']:p for p in json.loads(registry_bytes)['persons']}
 return frozenset(_claiming(people))
def installed(root):return any((Path(root)/p).exists()for p in OWNED)
def guard_bundle(root,pid,people,records):
 selected=[d for d in(records or[])if related(d)];claimed=_caller_claims(people,pid)
 if not(Path(root)/REF).exists():
  if installed(root)or selected or claimed:raise ValueError('Jin059 source/caller installed without contract')
  return
 cb=_raw(root,REF)
 if hashlib.sha256(cb).hexdigest()!=SHA:raise ValueError('Jin059 source contract checksum mismatch')
 c=json.loads(cb);physical=[json.loads(_raw(root,p))for p in c['expected_documents']];pc=_physical_claimants(_raw(root,'registry/persons.json'));po=owners(physical);co=owners(selected)
 if pid not in po|co|pc and not claimed:return
 if pid not in po or len(selected)!=len(physical)or any(sum(same(d,w)for d in selected)!=1 for w in physical):raise ValueError('Jin059 caller/physical catalogue mismatch')
 try:proof(root,people,records)
 except(AssertionError,KeyError,ValueError,TypeError,OSError,StopIteration)as e:raise ValueError('Jin059 source roles, reciprocal endpoints or current caller rows mismatch')from e

def applies(a):return type(a)is dict and type(a.get('qualifiers'))is dict and type(a['qualifiers'].get('source_clause_binding'))is dict and a['qualifiers']['source_clause_binding'].get('source_scope')==CID
def family_valid(a,root):
 try:_,_,e=proof(root);return any(same(a,x)for d in e.values()if d.get('record_type')=='person_assertion_set'for x in d['assertions'])
 except(AssertionError,KeyError,ValueError,TypeError,OSError,StopIteration):return False

def validate_surname(n,names,chapters,assertions,root):
 _,_,e=proof(root);wantnames=[x for d in e.values()if d.get('record_type')=='person_name_component_set'for x in d['records']];wantassert=[x for d in e.values()if d.get('record_type')=='person_assertion_set'for x in d['assertions']]
 assert any(same(n,w)for w in wantnames)
 selected=[x for x in names if x.get('chapter_id')==CID];assert len(selected)==len(wantnames)and all(sum(same(x,w)for x in selected)==1 for w in wantnames)
 assert all(sum(same(a,w)for a in assertions)==1 for w in wantassert)
 ch=next(d for d in e.values()if d.get('record_type')=='marked_chapter');assert same(chapters[CID],ch)
 return None

def errors(root):
 if not(Path(root)/REF).exists():return['059來源或側錄已安裝但缺所屬contract']if installed(root)else[]
 try:proof(root);return[]
 except(AssertionError,KeyError,ValueError,TypeError,OSError,StopIteration):return['059固定原字/明名父子/姓名父系/現役反查或取得資格不符']
