"""Finite editorial merge by source roles, not automated historical identity proof.

The catalogue endpoint is mutable. Stable MIDs, received glyphs, qualifications,
and the two enumerated current-ledger person leaves delimit this owner.
"""
import copy,hashlib,json
from pathlib import Path
REF='source-evidence/jin039-wangyi-parallel/identity-reading.json'
SHA='b76c38229a204fbfe96f67f5fe136e2fb8a616f5e985120b053133bb302d9009'
CH='corpus/jinshu/039.json'
CANON='corpus/jinshu/076.json'
DEC='corpus/jinshu/039-wangyi-identities.json'
LEDGER='source-evidence/jin059-jiong-yi-source/identity-reading-notes.json'
RET='source-evidence/jin039-wangyi-parallel/retirement-wanggao.json'
def same(a,b):
 if type(a)is not type(b):return False
 if isinstance(a,dict):return a.keys()==b.keys()and all(same(a[k],b[k])for k in a)
 if isinstance(a,list):return len(a)==len(b)and all(same(x,y)for x,y in zip(a,b))
 return a==b

def _slot(v,pointer):
 parts=pointer.split('/')[1:];assert parts[-1]=='person_id';at=v
 for k in parts[:-1]:at=at[int(k)]if isinstance(at,list)else at[k]
 assert isinstance(at,dict)and'person_id'in at;return at

def _proof(raw,people=None,records=None):
 b=raw(REF);assert hashlib.sha256(b).hexdigest()==SHA;c=json.loads(b);load=lambda p:json.loads(raw(p))
 ch=load(CH);source=load(CANON);ret=load(RET);dec=load(DEC)
 old=c['retired_registry_record_before']['id'];anchor=c['canonical_native_anchor'];sp,=[p for p in source['paragraphs']if p['id']==anchor['paragraph_id']];sm,=[m for m in sp['mentions']if m['id']==anchor['mid']]
 assert same(source['source'],c['canonical_source_metadata'])and sp['text']==c['canonical_paragraph_text']
 assert same({k:v for k,v in sm.items()if k!='person_id'},c['canonical_marker_without_endpoint'])
 pid=sm['person_id'];assert pid!=old
 if people is None:people={p['id']:p for p in load('registry/persons.json')['persons']}
 assert pid in people and old not in people;actor=people[pid]
 expected=copy.deepcopy(c['canonical_registry_before_unknown_metadata']);expected['id']=pid
 assert same({k:v for k,v in actor.items()if k not in ('aliases','evidence')},expected)
 assert [e for e in actor['evidence']if e.get('mention_id')==sm['id']]==[c['canonical_reverse']]
 assert all(e in actor['evidence']for e in c['canonical_prior_evidence'])
 for before in c['canonical_prior_aliases']:
  after,=[a for a in actor['aliases']if a['surface']==before['surface']]
  assert same({k:v for k,v in before.items()if k!='mention_ids'},{k:v for k,v in after.items()if k!='mention_ids'})and all(mid in after['mention_ids']for mid in before['mention_ids'])
 assert [(a['surface'],mid)for a in actor['aliases']for mid in a['mention_ids']if mid==sm['id']]==[(sm['surface'],sm['id'])]
 assert same(ch['source'],c['target_source_metadata'])
 p,=[p for p in ch['paragraphs']if p['id']==c['target_paragraph_id']];assert same({k:v for k,v in p.items()if k!='mentions'},c['target_paragraph_without_mentions'])
 current=[]
 for before in c['target_markers_without_endpoint']:
  m,=[m for m in p['mentions']if m['id']==before['id']];assert same({k:v for k,v in m.items()if k!='person_id'},before)and m['person_id']==pid
  e,=[e for e in c['retired_registry_record_before']['evidence']if e['mention_id']==m['id']]
  assert [x for x in actor['evidence']if x.get('mention_id')==m['id']]==[e]
  assert [(a['surface'],mid)for a in actor['aliases']for mid in a['mention_ids']if mid==m['id']]==[(m['surface'],m['id'])];current.append(m)
 d=copy.deepcopy(c['decision_template']);d['decisions'][0]['person_id']=pid;assert same(dec,d)
 assert same(ret,{'record_type':'editorial_annotation_rekey_receipt','identity_decision_id':d['decisions'][0]['id'],'retired_person_ids':[old],'retirement_policy':'audit_only_not_canonical_not_alias_not_reusable','person_aliases_created':False})
 # Decision's person endpoint belongs to its sole decision, not the set header.
 assert d['decisions'][0]['person_id']==pid
 obs=raw(c['primary_observation_path']);assert hashlib.sha256(obs).hexdigest()==c['primary_observation_sha256']
 assert c['digital_primary_qualification']['observed_quote']in obs.decode()
 ledger=load(LEDGER)
 for pointer,mid in zip(c['ledger']['explicit_person_pointers'],c['ledger']['stable_marker_ids']):
  slot=_slot(ledger,pointer);want=next(m for m in current if m['id']==mid);assert same(slot,want)
 for a in c['immutable_prior_captures']:assert hashlib.sha256(raw(a['path'])).hexdigest()==a['sha256']
 if records is not None:
  assert [x for x in records if x.get('id')==ch['id']]==[ch]
  ownerid=d['decisions'][0]['id'];assert [x for x in records if any(y.get('id')==ownerid for y in x.get('decisions',[]))]==[dec]
 return c,pid,old,current

def _raw(root):
 root=Path(root).resolve()
 def read(rel):
  p=Path(rel);assert not p.is_absolute()and'..'not in p.parts;q=root/p;assert q.resolve()==q and q.is_file();return q.read_bytes()
 return read

def proof(root,people=None,records=None):return _proof(_raw(root),people,records)
def active(root):return(Path(root)/REF).is_file()
def errors(root):
 if not active(root):return[]
 try:proof(root);return[]
 except(AssertionError,KeyError,ValueError,TypeError,OSError,IndexError,StopIteration):return['039 source-role identity merge, exact current ledger/reverse or received qualification mismatch']
def guard_bundle(root,pid,people,records):
 if not active(root):return
 load=lambda p:json.loads(_raw(root)(p));c=load(REF);source=load(CANON);canonical=next(m['person_id']for p in source['paragraphs']for m in p['mentions']if m['id']==c['canonical_native_anchor']['mid'])
 caller={m.get('person_id')for x in records if x.get('record_type')=='marked_chapter'for p in x['paragraphs']for m in p['mentions']if m['id']in c['target_mid_anchors']}
 physical={m.get('person_id')for p in load(CH)['paragraphs']for m in p['mentions']if m['id']in c['target_mid_anchors']}
 if pid==canonical or pid in caller|physical:proof(root,people,records)
def _project_current_ledger(expected,path,raw,root=None):
 if path!=LEDGER:return expected
 c,pid,old,current=_proof(raw);value=copy.deepcopy(expected)
 for pointer,mid in zip(c['ledger']['explicit_person_pointers'],c['ledger']['stable_marker_ids']):
  slot=_slot(value,pointer);want=next(m for m in current if m['id']==mid)
  assert slot['person_id']in(old,pid)and same({k:v for k,v in slot.items()if k!='person_id'},{k:v for k,v in want.items()if k!='person_id'})
  slot['person_id']=pid
 if root is not None:
  try:from scripts.sima_current_legacy_projection import project_validated_legacy_reference
  except ImportError:from sima_current_legacy_projection import project_validated_legacy_reference
  value=project_validated_legacy_reference(value,path,root)
 assert same(json.loads(raw(LEDGER)),value)
 return value

def project_current_ledger(expected,path,root):
 if path!=LEDGER or not active(root):return expected
 return _project_current_ledger(expected,path,_raw(root),root)
