"""Finite additive current endpoints on exactly eight validated historical projections.
Historical before bytes/SHA and opaque/nonperson leaves stay unchanged.
No load_catalog, Gaomi, Qiao, Lu or Wangyi proof dependency/cycle.
"""
from pathlib import Path
import copy,hashlib,json
REF='source-evidence/sima-current-legacy-eight/source-contract.json'
SHA='081ad45d2f467a66d95beee457b9c6ea026b6c766003fdd7ef57d6e487c27440'
def _same(a,b):
 if type(a)is not type(b):return False
 if isinstance(a,dict):return a.keys()==b.keys()and all(_same(a[k],b[k])for k in a)
 if isinstance(a,list):return len(a)==len(b)and all(_same(x,y)for x,y in zip(a,b))
 return a==b
def _state(root,people=None,chapters=None):
 root=Path(root);b=(root/REF).read_bytes();assert hashlib.sha256(b).hexdigest()==SHA;c=json.loads(b);assert c['owner']=='sima_current_legacy_eight_exact_paths'and len(c['paths'])==8;people=people if people is not None else{p['id']:p for p in json.loads((root/'registry/persons.json').read_bytes())['persons']};chapters=chapters or{};roles={};historical={}
 for role,ss in c['seeds'].items():
  ids=[];olds=[]
  for s in ss:
   ch=chapters.get(s['path'])
   if ch is None:ch=json.loads((root/s['path']).read_bytes())
   assert _same({k:ch[k]for k in s['dimensions']},s['dimensions']);p,=[p for p in ch['paragraphs']if p['id']==s['paragraph_id']];assert hashlib.sha256(p['text'].encode()).hexdigest()==s['paragraph_sha256'];m,=[m for m in p['mentions']if m['id']==s['marker']['id']];assert _same({k:m[k]for k in s['marker']},s['marker'])and m['kind']=='person'and p['text'][m['start']:m['end']]==m['surface'];pid=m['person_id'];assert pid in people;actor=people[pid];assert[e for e in actor['evidence']if e.get('mention_id')==m['id']]==[s['reverse']];assert sum(a['surface']==m['surface']and m['id']in a['mention_ids']for a in actor['aliases'])==1;ids.append(pid);olds.append(s['historical_endpoint'])
  assert len(set(ids))==len(set(olds))==1;roles[role]=ids[0];historical[role]=olds[0]
 assert len(set(roles.values()))==len(roles);return c,roles,historical
def project_validated_legacy_reference(expected,path,root,people=None,chapters=None):
 c,roles,historical=_state(root,people,chapters)
 if path not in c['paths']:return expected
 out=copy.deepcopy(expected);seen=set()
 for row in c['paths'][path]:
  assert set(row)=={'pointer','role','field_semantics'}and row['field_semantics']=='current_person_endpoint';ptr=row['pointer'];assert ptr.startswith('/')and ptr not in seen;seen.add(ptr);parts=[p.replace('~1','/').replace('~0','~')for p in ptr[1:].split('/')];assert parts[-1]in('person_id','candidate_person_id','selected');at=out
  for k in parts[:-1]:at=at[int(k)]if isinstance(at,list)else at[k]
  key=parts[-1];assert isinstance(at,dict)and isinstance(at[key],str)and at[key]in(historical[row['role']],roles[row['role']]);at[key]=roles[row['role']]
 return out
