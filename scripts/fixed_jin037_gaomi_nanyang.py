"""Finite Jin037 received near-family unit; raw conservation and reviewed roles separate."""
from pathlib import Path
import json,hashlib,copy
CID="c-jinshu-037-gaomi-nanyang-ws2630018"
CH="corpus/jinshu/037-gaomi-nanyang-ws2630018.json"
REF="source-evidence/jin037-gaomi-nanyang/source-contract.json"
SHA="79e8994c86f59746b8b2c0d5ed05d9c6fb76328caa467f4231ab1abf0e6a516e"
def same(a,b):
 if type(a)is not type(b):return False
 if isinstance(a,dict):return a.keys()==b.keys()and all(same(a[k],b[k])for k in a)
 if isinstance(a,list):return len(a)==len(b)and all(same(x,y)for x,y in zip(a,b))
 return a==b

def project_legacy_person_leaves(original,rows,migration,roles):
 """Only fixed typed person_id pointers change; opaque IDs/quotes never do."""
 value=copy.deepcopy(original);seen=set()
 for row in rows:
  assert set(row)=={'pointer','role','field_semantics'}and row['field_semantics']=='person_endpoint'
  pointer=row['pointer'];assert isinstance(pointer,str)and pointer.startswith('/')and pointer not in seen;seen.add(pointer)
  bits=pointer[1:].split('/');assert bits[-1]=='person_id'
  parent=value
  for bit in bits[:-1]:
   bit=bit.replace('~1','/').replace('~0','~')
   if isinstance(parent,list):assert bit.isdigit()and str(int(bit))==bit;parent=parent[int(bit)]
   else:assert isinstance(parent,dict);parent=parent[bit]
  assert isinstance(parent,dict)and'person_id'in parent
  old=parent['person_id'];current=roles['$'+row['role']]
  assert isinstance(old,str)and old in migration and migration[old]==current
  parent['person_id']=current
 return value

try:from scripts.validation_context import memoized
except ImportError:from validation_context import memoized

@memoized(0)
def proof(root,chapter=None):
 root=Path(root).resolve()
 def read(path):
  rel=Path(path);assert not rel.is_absolute()and'..'not in rel.parts
  p=root/rel;assert p.resolve()==p and p.is_file();return p.read_bytes()
 def load(path):return json.loads(read(path))
 assert hashlib.sha256(read(REF)).hexdigest()==SHA
 c=load(REF);ch=load(CH);assert chapter is None or same(ch,chapter)
 raw=read(c['raw_path']);assert hashlib.sha256(raw).hexdigest()==c['raw_sha256'];text=raw.decode()
 projection_raw=read(c['projection_path']);assert hashlib.sha256(projection_raw).hexdigest()==c['projection_sha256'];projection=json.loads(projection_raw)
 assert ch['id']==CID and ch['source']['revision_id']==2630018 and ch['source']['edition']is None and ch['source']['image_verified']is False
 people={p['id']:p for p in load('registry/persons.json')['persons']};ms={m['id']:(p,m)for p in ch['paragraphs']for m in p['mentions']};roles={}
 for role,s in c['role_seeds'].items():
  if s['kind']=='source_local':p,m=ms[s['first_mid']]
  else:
   other=load(s['path']);p=next(p for p in other['paragraphs']if p['id']==s['paragraph_id']);m=next(m for m in p['mentions']if m['id']==s['marker']['id']);assert p['text']==s['quote']and same({k:v for k,v in m.items()if k!='person_id'},s['marker']);assert [e for e in people[m['person_id']]['evidence']if e.get('mention_id')==m['id']]==[s['reverse']]
  assert m['kind']=='person'and m['person_id']in people;roles['$'+role]=m['person_id']
 assert len(set(roles.values()))==len(roles)
 def expand(x):
  if isinstance(x,str):return roles.get(x,x)
  if isinstance(x,list):return[expand(v)for v in x]
  if isinstance(x,dict):return{k:expand(v)for k,v in x.items()}
  return x
 migration={}
 for seed in c['endpoint_migration_seeds']:
  data=read(seed['before_capture']);assert hashlib.sha256(data).hexdigest()==seed['before_sha256'];before=json.loads(data);oldp=before['paragraph'];assert oldp['id']==seed['paragraph_id']and before['source_path']==seed['source_path']and before['mention_id']==seed['mention_id'];oldm=next(m for m in oldp['mentions']if m['id']==seed['mention_id']);current=load(seed['source_path']);newp=next(p for p in current['paragraphs']if p['id']==seed['paragraph_id']);newm=next(m for m in newp['mentions']if m['id']==seed['mention_id'])
  assert oldp['text']==newp['text']and same({k:v for k,v in oldm.items()if k!='person_id'},{k:v for k,v in newm.items()if k!='person_id'})and newm['person_id']==roles['$'+seed['role']]
  assert oldm['kind']==newm['kind']=='person'and oldm['person_id']!=newm['person_id']
  e={k:current[k]for k in('work_id','book_id','source_id')};e.update(chapter_id=current['id'],paragraph_id=newp['id'],mention_id=newm['id'],quote=newm['surface']);actor=people[newm['person_id']]
  assert [x for x in actor['evidence']if x.get('mention_id')==newm['id']]==[e]and sum(newm['id']in a['mention_ids']and a['surface']==newm['surface']for a in actor['aliases'])==1
  if oldm['person_id']in migration:assert migration[oldm['person_id']]==newm['person_id']
  else:migration[oldm['person_id']]=newm['person_id']
 for row in c['legacy_reference_migrations']:
  data=read(row['before_capture']);assert hashlib.sha256(data).hexdigest()==row['before_sha256'];expected=project_legacy_person_leaves(json.loads(data),row['typed_person_pointers'],migration,roles)
  try:from scripts.jin039_wangyi_parallel import project_current_ledger
  except ImportError:from jin039_wangyi_parallel import project_current_ledger
  expected=project_current_ledger(expected,row['path'],root)
  try:from scripts.sima_current_legacy_projection import project_validated_legacy_reference
  except ImportError:from sima_current_legacy_projection import project_validated_legacy_reference
  expected=project_validated_legacy_reference(expected,row['path'],root);assert same(load(row['path']),expected)
 bridge=load(c['jun_parallel_reference_path']);assert same(bridge,expand(c['jun_parallel_reference_template']))and bridge['raw_path']==c['raw_path']and bridge['raw_sha256']==c['raw_sha256']
 assert text[bridge['raw_start']:bridge['raw_end']]==bridge['complete_received_text']and'恭王俊字道度，出嗣高密王略'in bridge['complete_received_text']
 assert same(ch,expand(c['expected_chapter']))
 for path,wanted in c['expected_sidecars'].items():assert same(load(path),expand(wanted))
 assert same(load(c['identity_readings_path']),expand(c['identity_readings_template']))
 family=next(a for a in load('registry/family-assemblies.json')['assemblies']if a['id']==c['assembly_id'])
 for m in expand(c['assembly_members']):assert [x for x in family['members']if x['person_id']==m['person_id']]==[m]
 assert len(ch['paragraphs'])==len(projection['paragraphs'])==18
 for p,u in zip(ch['paragraphs'],projection['paragraphs']):
  positions=p['source_position']['raw_character_offsets'];assert u['paragraph_id']==p['id']and u['text']==p['text']and positions==u['raw_character_offsets']and ''.join(text[i]for i in positions)==p['text']
  for m in p['mentions']:
   assert type(m['start'])is int and type(m['end'])is int and p['text'][m['start']:m['end']]==m['surface']
   if m['kind']=='unresolved':assert m['person_id']is None;continue
   if m['kind']=='work':assert m['person_id']is None and m['work_id']in{w['id']for w in load('registry/works.json')['works']};continue
   assert m['kind']=='person'and m['surface']not in('之','其','我','吾','公','臣','陛下')
   actor=people[m['person_id']];e={k:ch[k]for k in('work_id','book_id','source_id')};e.update(chapter_id=CID,paragraph_id=p['id'],mention_id=m['id'],quote=m['surface'])
   assert [a for a in actor['evidence']if a.get('mention_id')==m['id']]==[e]
   assert sum(a['surface']==m['surface']and m['id']in a['mention_ids']for a in actor['aliases'])==1
 return ch,roles

def errors(chapter,root):
 try:proof(root,chapter);return []
 except(AssertionError,KeyError,ValueError,TypeError,StopIteration,OSError,IndexError)as e:return [CID+': 固定原文/角色/反查/推父資格不符 ('+type(e).__name__+')']

def applies(a):
 if not isinstance(a,dict)or not isinstance(a.get('qualifiers'),dict):return False
 b=a['qualifiers'].get('source_clause_binding')
 return isinstance(b,dict)and b.get('rule')=='fixed_jin037_near_family'
def family_valid(a,paragraphs,root):
 try:
  ch,_=proof(root);rows=json.loads((Path(root)/'corpus/jinshu/037-gaomi-nanyang-assertions.json').read_bytes())['assertions'];assert applies(a)and sum(same(a,x)for x in rows)==1
  e,=a['evidence'];cid,p=paragraphs[e['paragraph_id']];assert cid==CID and same(p,next(p for p in ch['paragraphs']if p['id']==e['paragraph_id']))
  return True
 except(AssertionError,KeyError,ValueError,TypeError,StopIteration,OSError,IndexError):return False

def guard_bundle(root,pid,people,records):
 if not(Path(root)/REF).exists():return
 physical=json.loads((Path(root)/CH).read_bytes());owners={m['person_id']for p in physical['paragraphs']for m in p['mentions']if m.get('person_id')};callers=[r for r in records if r.get('record_type')=='marked_chapter'and r.get('id')==CID];caller_owners={m.get('person_id')for ch in callers for p in ch['paragraphs']for m in p['mentions']}
 names=json.loads((Path(root)/'corpus/jinshu/037-gaomi-nanyang-names.json').read_bytes());owners.update(n['person_id']for n in names['records'])
 caller_owners.update(n.get('person_id')for r in records if r.get('record_type')=='person_name_component_set'and r.get('chapter_id')==CID for n in r['records'])
 if pid not in owners and pid not in caller_owners:return
 assert pid in owners and len(callers)==1 and same(callers[0],physical)
 ch,_=proof(root);c=json.loads((Path(root)/REF).read_bytes());disk_people={p['id']:p for p in json.loads((Path(root)/'registry/persons.json').read_bytes())['persons']}
 for owner in owners:assert same(people[owner],disk_people[owner])
 for path in c['expected_sidecars']:
  actual=json.loads((Path(root)/path).read_bytes());matches=[r for r in records if r.get('record_type')==actual['record_type']and r.get('chapter_id')==CID];assert len(matches)==1 and same(matches[0],actual)

def legacy_projection_valid(root,path,before_sha256):
 try:
  proof(root);c=json.loads((Path(root)/REF).read_bytes())
  return sum(row['path']==path and row['before_sha256']==before_sha256 for row in c['legacy_reference_migrations'])==1
 except(AssertionError,KeyError,ValueError,TypeError,StopIteration,OSError,IndexError):return False

def unresolved_kin_errors(record,chapter,root):
 try:
  ch,_=proof(root,chapter);assert record['id']=='uk-jin037-teng-unnamed-uncle'and sum(same(record,r)for r in ch['annotation']['unresolved_kinship_references'])==1
  e,=record['evidence'];p=next(p for p in ch['paragraphs']if p['id']==e['paragraph_id']);a=record['source_anchor'];m=next(m for m in p['mentions']if m['id']==e['person_mention_id'])
  assert p['text'][a['start']:a['end']]==record['source_term']==m['surface']+'出後叔父'and m['start']==a['start']and m['person_id']==record['person_id']
  assert record['reference_person_candidates']==[]and record['adoptive_father_person_id']is None and record['reference_identity_status']=='not_named_by_this_source'
  return []
 except(AssertionError,KeyError,ValueError,TypeError,StopIteration,OSError,IndexError):return ['晉037未名出後叔父不得填權/綏或造養父']
