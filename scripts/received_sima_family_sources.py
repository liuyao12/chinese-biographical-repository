"""Finite received Sima family units; AI readings remain editable.
Current IDs derive stable native source roles and reciprocal current catalog leaves.
Raw/capture conservation is separate from the semantic expected view.
"""
from pathlib import Path
import json,hashlib
REF='source-evidence/sima-family-source-bridges/source-contract.json'
SHA='b6fa287ffd1604b3ed2fdc22d1b16da27a9b973df310205414f45c927a34cc2d'
PRONOUN_RULES={'c-jinshu-053-minhuai-family:p001:m0067': {'start': 67, 'end': 68, 'surface': '汝', 'source_role': 'hui', 'voice': 'quoted_addressee_second_person', 'source_reference_binding': {'kind': 'received_sima_family_pronoun', 'paragraph_id': 'c-jinshu-053-minhuai-family:p001', 'paragraph_sha256': '09a9755de725bde1fc81796377e86c7ccab8de41f3367244da0b203bbbc9fba6', 'role': 'hui'}}, 'c-jinshu-053-minhuai-family:p001:m0199': {'start': 199, 'end': 200, 'surface': '我', 'source_role': 'wu', 'voice': 'quoted_speaker_first_person', 'source_reference_binding': {'kind': 'received_sima_family_pronoun', 'paragraph_id': 'c-jinshu-053-minhuai-family:p001', 'paragraph_sha256': '09a9755de725bde1fc81796377e86c7ccab8de41f3367244da0b203bbbc9fba6', 'role': 'wu'}}}
OWNED_PATHS=('corpus/jinshu/053-minhuai-family.json', 'corpus/jinshu/053-minhuai-family-name-components.json', 'corpus/jinshu/053-minhuai-family-assertions.json', 'source-evidence/sima-family-source-bridges/jin053-received-units.json', 'corpus/jinshu/053-minhuai-family.xml', 'corpus/jinshu/053-minhuai-family-life-events.json', 'corpus/jinshu/053-minhuai-family-titles.json')
def same(a,b):
 """Type-strict JSON-tree equality; bool/int and non-JSON shapes stay distinct."""
 if type(a)is not type(b):return False
 if type(a)is dict:
  return ({(type(k),k)for k in a}=={(type(k),k)for k in b}and all(same(v,b[k])for k,v in a.items()))
 if type(a)is list:return len(a)==len(b)and all(same(x,y)for x,y in zip(a,b))
 return a==b if type(a)in(str,int,float,bool,type(None))else False
def _caller_reverse_claim(people,pid,cid,mids=()):
 """Applicability only: a caller's exact current reverse claim must reach proof."""
 person=people.get(pid)if isinstance(people,dict)else None
 evidence=person.get('evidence',[])if isinstance(person,dict)else []
 if not isinstance(evidence,list):return False
 return any(isinstance(e,dict)and(e.get('chapter_id')==cid or isinstance(e.get('mention_id'),str)and e['mention_id']in mids)for e in evidence)
def source_reference(m,text=None):
 if isinstance(m,dict)and isinstance(m.get('id'),str)and m['id'].startswith('c-jinshu-064-wudi-sons-rendered:'):
  try:from scripts.jin064_wudi_family_sources import source_reference as jin064_reference
  except ImportError:from jin064_wudi_family_sources import source_reference as jin064_reference
  return jin064_reference(m,text)
 if not isinstance(m,dict):return False
 w=PRONOUN_RULES.get(m.get('id'))
 return bool(w and m.get('kind')=='pronoun'and m.get('status')=='contextual_provisional'and isinstance(m.get('person_id'),str)and bool(m['person_id'])and all(same(m.get(k),v)for k,v in w.items())and(text is None or hashlib.sha256(text.encode()).hexdigest()==w['source_reference_binding']['paragraph_sha256']))
def _raw(root,p):
 root=Path(root).resolve();rel=Path(p);assert not rel.is_absolute()and'..'not in rel.parts;f=root/rel;assert f.resolve()==f;return f.read_bytes()
def _proof(raw,people=None,records=None):
 cb=raw(REF);assert hashlib.sha256(cb).hexdigest()==SHA;c=json.loads(cb);load=lambda p:json.loads(raw(p));ch=load(c['chapter_path']);ms={m['id']:(p,m)for p in ch['paragraphs']for m in p['mentions']}
 if people is None:people={p['id']:p for p in load('registry/persons.json')['persons']}
 roles={}
 for role,mids in c['role_current_mids'].items():
  assert mids;proper=[ms[mid][1]for mid in mids if ms[mid][1]['kind']=='person'];assert proper;pid=proper[0]['person_id'];assert pid in people and all(ms[mid][1]['person_id']==pid for mid in mids);roles[role]=pid
 assert len(set(roles.values()))==len(roles)
 for role,s in c['role_seeds'].items():
  q=load(s['chapter_path']);p=next(p for p in q['paragraphs']if p['id']==s['paragraph_id']);m=next(m for m in p['mentions']if m['id']==s['marker']['id']);assert hashlib.sha256(p['text'].encode()).hexdigest()==s['paragraph_sha256']and same({k:v for k,v in m.items()if k!='person_id'},s['marker'])and m['person_id']==roles[role];assert same([e for e in people[roles[role]]['evidence']if e.get('mention_id')==m['id']],[s['reverse']])
 try:from scripts.jin002_004_imperial_openings import _proof as imperial_proof
 except ImportError:from jin002_004_imperial_openings import _proof as imperial_proof
 _,imperial_roles,_=imperial_proof(raw,people)
 assert all(roles[r]==imperial_roles['$'+s]for r,s in c['existing_imperial_role_bridge'].items())
 def expand(x):
  if isinstance(x,str)and x.startswith('@person:'):return roles[x[8:]]
  if isinstance(x,list):return[expand(v)for v in x]
  if isinstance(x,dict):return{k:expand(v)for k,v in x.items()}
  return x
 expected={p:expand(v)for p,v in c['expected_documents'].items()}
 for p,v in expected.items():assert same(load(p),v)
 assert hashlib.sha256(raw(c['capture_path'])).hexdigest()==c['capture_sha256']
 cap=load(c['capture_path']);assert len(cap['units'])==len(ch['paragraphs'])and all(p['text']==u['received_text']and p['source_position']['tool_line']==u['tool_line']for p,u in zip(ch['paragraphs'],cap['units']))
 assert ch['text_sha256']==hashlib.sha256('\n\n'.join(p['text']for p in ch['paragraphs']).encode()).hexdigest()
 for role,mids in c['role_current_mids'].items():
  person=people[roles[role]]
  for mid in mids:
   p,m=ms[mid];e={'work_id':ch['work_id'],'book_id':ch['book_id'],'source_id':ch['source_id'],'chapter_id':ch['id'],'paragraph_id':p['id'],'mention_id':mid,'quote':m['surface']};assert same([x for x in person['evidence']if x.get('mention_id')==mid],[e]);aliases=[a for a in person['aliases']if mid in a.get('mention_ids',[])]
   if m['kind']=='pronoun':assert not aliases and source_reference(m,p['text'])
   else:assert len(aliases)==1 and aliases[0]['surface']==m['surface']
 if records is not None:
  selected=[d for d in records if d.get('id')==ch['id']or d.get('chapter_id')==ch['id']or d.get('record_type')=='person_name_component_set'and any(n.get('chapter_id')==ch['id']for n in d.get('records',[]))];assert len(selected)==len(expected)and all(sum(same(d,v)for d in selected)==1 for v in expected.values())
 return c,roles,expected
def proof(root,people=None,records=None):return _proof(lambda p:_raw(root,p),people,records)
def _installed(root):return any((Path(root)/p).exists()for p in OWNED_PATHS)
def _base_errors(root):
 if not(Path(root)/REF).exists():return['接收司馬近系來源或側錄已安裝但缺所屬contract']if _installed(root)else[]
 try:proof(root);return[]
 except(AssertionError,KeyError,ValueError,TypeError,OSError,StopIteration):return['接收司馬近系完整來源/明父母子嗣/姓名字/代詞反查或取得資格不符']
def guard_bundle(root,pid,people,records):
 try:from scripts.jin059_wei_ying_children import guard_bundle as jin059_guard
 except ImportError:from jin059_wei_ying_children import guard_bundle as jin059_guard
 jin059_guard(root,pid,people,records)
 try:from scripts.jin064_wudi_family_sources import guard_bundle as jin064_guard
 except ImportError:from jin064_wudi_family_sources import guard_bundle as jin064_guard
 jin064_guard(root,pid,people,records)
 if not(Path(root)/REF).exists():
  if _installed(root)or _caller_reverse_claim(people,pid,'c-jinshu-053-minhuai-family'):raise ValueError('Received Sima source installed without contract')
  return
 cb=_raw(root,REF)
 if hashlib.sha256(cb).hexdigest()!=SHA:raise ValueError('Received Sima source contract checksum mismatch')
 c=json.loads(cb);physical=[json.loads(_raw(root,p))for p in c['expected_documents']];ch=next(d for d in physical if d.get('record_type')=='marked_chapter');cid=ch['id'];mids={m['id']for p in ch['paragraphs']for m in p['mentions']}
 def related(d):
  return isinstance(d,dict)and(d.get('id')==cid or d.get('chapter_id')==cid or d.get('record_type')=='person_name_component_set'and any(n.get('chapter_id')==cid for n in d.get('records',[]))or any(m.get('id')in mids for p in d.get('paragraphs',[])for m in p.get('mentions',[])))
 def owners(documents):
  result=set()
  for d in documents:
   if isinstance(d.get('person_id'),str):result.add(d['person_id'])
   for e in d.get('events',[])+d.get('holdings',[]):
    if isinstance(e,dict)and isinstance(e.get('person_id'),str):result.add(e['person_id'])
   for p in d.get('paragraphs',[]):result.update(m['person_id']for m in p.get('mentions',[])if isinstance(m.get('person_id'),str))
   if d.get('record_type')=='person_name_component_set':result.update(n['person_id']for n in d.get('records',[])if isinstance(n.get('person_id'),str))
   if d.get('record_type')=='person_assertion_set':
    for a in d.get('assertions',[]):result.update(a[k]for k in('subject_person_id','object_person_id')if isinstance(a.get(k),str))
  return result
 selected=[d for d in(records or[])if related(d)];physical_owners=owners(physical);caller_owners=owners(selected)
 reverse_mids={mid for group in c['role_current_mids'].values()for mid in group}
 caller_reverse_claim=_caller_reverse_claim(people,pid,'c-jinshu-053-minhuai-family',reverse_mids)
 if pid not in physical_owners|caller_owners and not caller_reverse_claim:return
 if pid not in physical_owners or len(selected)!=len(physical)or any(sum(same(d,want)for d in selected)!=1 for want in physical):raise ValueError('Received Sima caller/physical catalogue mismatch')
 proof(root,people,records)

def family_valid(a,root):
 try:from scripts.jin059_wei_ying_children import applies as jin059_applies,family_valid as jin059_valid
 except ImportError:from jin059_wei_ying_children import applies as jin059_applies,family_valid as jin059_valid
 if jin059_applies(a):return jin059_valid(a,root)
 try:from scripts.jin064_wudi_family_sources import applies as jin064_applies,family_valid as jin064_valid
 except ImportError:from jin064_wudi_family_sources import applies as jin064_applies,family_valid as jin064_valid
 if jin064_applies(a):return jin064_valid(a,root)
 try:_,_,e=proof(root);return any(same(a,x)for d in e.values()if d.get('record_type')=='person_assertion_set'for x in d['assertions'])
 except(AssertionError,KeyError,ValueError,TypeError,OSError,StopIteration):return False
def validate_surname(n,names,chapters,assertions,root):
 if isinstance(n,dict)and isinstance(n.get("surname_basis"),dict)and n["surname_basis"].get("source_scope")=="c-jinshu-059-wei-ying-children":
  try:from scripts.jin059_wei_ying_children import validate_surname as jin059_surname
  except ImportError:from jin059_wei_ying_children import validate_surname as jin059_surname
  return jin059_surname(n,names,chapters,assertions,root)
 if isinstance(n,dict)and isinstance(n.get("surname_basis"),dict)and n["surname_basis"].get("source_scope")=="c-jinshu-064-wudi-sons-rendered":
  try:from scripts.jin064_wudi_family_sources import validate_surname as jin064_surname
  except ImportError:from jin064_wudi_family_sources import validate_surname as jin064_surname
  return jin064_surname(n,names,chapters,assertions,root)
 _,_,e=proof(root);assert any(same(n,x)for d in e.values()if d.get('record_type')=='person_name_component_set'for x in d['records']);return None

def errors(root):
 try:from scripts.jin064_wudi_family_sources import errors as jin064_errors
 except ImportError:from jin064_wudi_family_sources import errors as jin064_errors
 try:from scripts.jin059_wei_ying_children import errors as jin059_errors
 except ImportError:from jin059_wei_ying_children import errors as jin059_errors
 return _base_errors(root)+jin064_errors(root)+jin059_errors(root)
