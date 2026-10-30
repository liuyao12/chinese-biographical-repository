# coding: utf-8
"""One received Tao Shiheng allusion; true caller first, immutable parent proof after."""
import json,copy,hashlib
from pathlib import Path
REF='source-evidence/liang041-wanggui-ws1512987/taoshiheng-identity-successor.json'
SHA='56c86bdedaa9f76fd52613f912a5950058bd292e2078facb14e029a532ffe010'
def same(a,b):
 if type(a)is not type(b):return False
 if isinstance(a,dict):return a.keys()==b.keys()and all(same(a[k],b[k])for k in a)
 if isinstance(a,list):return len(a)==len(b)and all(same(x,y)for x,y in zip(a,b))
 return a==b
def _state(root,ch=None,people=None):
 root=Path(root).resolve()
 def local(rel):
  p=Path(rel);assert not p.is_absolute()and '..'not in p.parts;q=(root/p).resolve();assert q.is_relative_to(root)and q.is_file();return q
 def read(rel):return json.loads(local(rel).read_bytes())
 b=local(REF).read_bytes();assert hashlib.sha256(b).hexdigest()==SHA;captured=json.loads(b)
 seed=captured['source_seed'];doc=read(seed['path']);p=next(p for p in doc['paragraphs']if p['id']==seed['paragraph_id']);sm=next(m for m in p['mentions']if m['id']==seed['marker']['id']);assert same(doc['source'],seed['source'])and p['text']==seed['quote']and same({k:v for k,v in sm.items()if k!='person_id'},seed['marker'])and sm['kind']=='person'
 role=sm['person_id']
 def expand(x):
  if isinstance(x,str):return role if x=='$taokan'else x
  if isinstance(x,list):return[expand(v)for v in x]
  if isinstance(x,dict):return{k:expand(v)for k,v in x.items()}
  return x
 c=expand(captured);actual=read(c['chapter_path']);assert ch is None or same(ch,actual);ch=actual;assert same(ch,c['chapter_after']);assert same(read(c['decision_path']),c['decision_after'])
 if people is None:people={p['id']:p for p in read('registry/persons.json')['persons']}
 assert role in people and c['target_pid']==role
 for rel,expected in c['protected_file_sha256'].items():assert hashlib.sha256(local(rel).read_bytes()).hexdigest()==expected
 parentraw=local(c['parent_ref']).read_bytes();assert hashlib.sha256(parentraw).hexdigest()==c['parent_sha256'];parent=json.loads(parentraw)
 actor=people[c['target_pid']];assert [e for e in actor['evidence']if e.get('mention_id')==sm['id']]==[seed['reverse']];assert any(a.get('surface')==sm['surface']and sm['id']in a.get('mention_ids',[])for a in actor['aliases'])
 cap=c['ssxy_capture'];raw=local(cap['path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==cap['sha256'];t=raw.decode('utf8');sel=cap['selection'];assert t[sel['start']:sel['end']]==sel['raw']and '王愆期推征西陶侃為盟主'in sel['raw']and '庾元規何縁拜陶士衡'in sel['raw']
 markers={m['id']:(p,m)for p in ch['paragraphs']for m in p['mentions']};p,m=markers[c['target_mid']];assert m['kind']=='person'and m['person_id']==c['target_pid']and m['surface']=='陶士衡'and m['start']==0 and m['end']==3 and p['text'].startswith('陶士衡曰：「昔大禹不吝尺璧而重寸陰。」')
 for pid,person in people.items():
  expected=[c['added_reverse']]if pid==c['target_pid']else[];assert same([e for e in person['evidence']if e.get('mention_id')==c['target_mid']],expected)
  got=[a for a in person['aliases']if c['target_mid']in a.get('mention_ids',[])];assert same(got,[c['added_alias']]if pid==c['target_pid']else[])
 # Construct exactly the recorded immediate parent; cannot replace the caller or other fields.
 old=copy.deepcopy(ch);oldp=next(q for q in old['paragraphs']if any(v['id']==c['target_mid']for v in q['mentions']));oldp['mentions']=[copy.deepcopy(c['original_marker'])if v['id']==c['target_mid']else v for v in oldp['mentions']];old['annotation']=copy.deepcopy(parent['chapter_template']['annotation']);assert same(old,parent['chapter_template'])
 try:from scripts.fixed_liang041_wanggui import _base_proof
 except ImportError:from fixed_liang041_wanggui import _base_proof
 old_verified,original=_base_proof(root,old,people);assert same(old_verified,old);return ch,original,c

def proof(root,ch=None,people=None):
 current,parent,case=_state(root,ch,people);return current,parent

def owner_applies(pid,people,records):
 # Stable source roles, never a permanent PID whitelist. Caller reverse loss cannot disable ownership.
 target='c-liangshu-041-wanggui-ws1512987:p007:m0000';seed='c-jinshu-076-wangyi-family:p002:m0006'
 if any(e.get('mention_id')in(target,seed)for e in people.get(pid,{}).get('evidence',[])):return True
 for r in records:
  if r.get('id')not in('c-liangshu-041-wanggui-ws1512987','c-jinshu-076-wangyi-family'):continue
  if any(m.get('id')in(target,seed)and m.get('person_id')==pid for p in r.get('paragraphs',[])for m in p.get('mentions',[])):return True
 return False

def guard_catalog(root,people,records):
 ch,parent,case=_state(root,people=people);assert sum(same(r,case['decision_after'])for r in records)==1
