"""Finite received imperial opening roles. Editorial choices are not historical proof.
All endpoint IDs derive current source MIDs and independent existing role anchors.
"""
from pathlib import Path
import json,hashlib,copy
REF='source-evidence/jin002-004-imperial-openings/source-contract.json'
SHA='ce856f66cd7c7065780c73c4c5fe3ad909851c5a25e8abe7876c84943ec59731'
PRONOUN_RULES={'c-jinshu-002-jingwen-openings:p002:m0186': {'start': 186, 'end': 187, 'surface': '臣', 'source_role': 'zhao', 'voice': 'reported_first_person', 'source_reference_binding': {'kind': 'jin002_004_source_first_person', 'paragraph_id': 'c-jinshu-002-jingwen-openings:p002', 'paragraph_sha256': 'dce5e01a57f367dc6819eabb7dd891e7a73c4529946bb275c63f342770a24230', 'role': 'zhao'}}, 'c-jinshu-003-wudi-opening:p002:m0060': {'start': 60, 'end': 61, 'surface': '吾', 'source_role': 'zhao', 'voice': 'reported_first_person', 'source_reference_binding': {'kind': 'jin002_004_source_first_person', 'paragraph_id': 'c-jinshu-003-wudi-opening:p002', 'paragraph_sha256': '8fe0be2ecbf575610e3a6a4b6e8c3170660c2e24317676b15597c0d59ea5b2df', 'role': 'zhao'}}}

OWNED_PATHS=('corpus/jinshu/002-jingwen-openings.json', 'corpus/jinshu/002-jingwen-openings-name-components.json', 'corpus/jinshu/002-jingwen-openings-assertions.json', 'corpus/jinshu/003-wudi-opening.json', 'corpus/jinshu/003-wudi-opening-name-components.json', 'corpus/jinshu/003-wudi-opening-assertions.json', 'corpus/jinshu/004-huidi-opening.json', 'corpus/jinshu/004-huidi-opening-name-components.json', 'corpus/jinshu/004-huidi-opening-assertions.json', 'corpus/jinshu/002-jingwen-openings.xml', 'corpus/jinshu/003-wudi-opening.xml', 'corpus/jinshu/004-huidi-opening.xml', 'source-evidence/jin002-004-imperial-openings/received-unit-capsules.json', 'source-evidence/jin002-004-imperial-openings/existing-parent-source-reports.json')
def _installed_without_contract(root):
 return any((Path(root)/p).exists()for p in OWNED_PATHS)

def source_reference(m,text=None):
 if not isinstance(m,dict):return False
 w=PRONOUN_RULES.get(m.get('id'))
 return bool(w and m.get('kind')=='pronoun'and m.get('status')=='contextual_provisional'and all(m.get(k)==v for k,v in w.items())and isinstance(m.get('person_id'),str)and(text is None or hashlib.sha256(text.encode()).hexdigest()==w['source_reference_binding']['paragraph_sha256']))
def _raw(root,p):
 root=Path(root).resolve();rel=Path(p);assert not rel.is_absolute()and'..'not in rel.parts;f=root/rel;assert f.resolve()==f;return f.read_bytes()
def _proof(raw,people=None,records=None):
 cb=raw(REF);assert hashlib.sha256(cb).hexdigest()==SHA;c=json.loads(cb);load=lambda p:json.loads(raw(p));chs=[load(p)for p in c['chapter_paths']];ms={m['id']:(ch,p,m)for ch in chs for p in ch['paragraphs']for m in p['mentions']}
 if people is None:people={p['id']:p for p in load('registry/persons.json')['persons']}
 roles={}
 for r,mids in c['role_current_mids'].items():
  pid=ms[mids[0]][2]['person_id'];assert pid in people;roles['$'+r]=pid
  for mid in mids:
   ch,p,m=ms[mid];assert m['person_id']==pid and p['text'][m['start']:m['end']]==m['surface'];e={k:ch[k]for k in('work_id','book_id','source_id')};e.update(chapter_id=ch['id'],paragraph_id=p['id'],mention_id=mid,quote=m['surface']);assert[e0 for e0 in people[pid]['evidence']if e0.get('mention_id')==mid]==[e]
   als=[(a['surface'],x)for a in people[pid]['aliases']for x in a['mention_ids']if x==mid]
   assert als==([(m['surface'],mid)]if m['kind']=='person'else[])
  seed=c['existing_role_seeds'][r];old=load(seed['path']);p=next(p for p in old['paragraphs']if p['id']==seed['paragraph_id']);m=next(m for m in p['mentions']if m['id']==seed['marker']['id']);assert hashlib.sha256(p['text'].encode()).hexdigest()==seed['paragraph_sha256']and{k:v for k,v in m.items()if k!='person_id'}==seed['marker']and m['person_id']==pid
  assert[e for e in people[pid]['evidence']if e.get('mention_id')==m['id']]==[seed['reverse']]
 assert len(set(roles.values()))==len(roles)
 def expand(v):
  if isinstance(v,str):return roles.get(v,v)
  if isinstance(v,list):return[expand(x)for x in v]
  if isinstance(v,dict):return{k:expand(x)for k,x in v.items()}
  return v
 expected={p:expand(v)for p,v in c['expected_documents'].items()}
 for path,want in expected.items():assert load(path)==want
 for path,aa in c['existing_parent_assertions'].items():
  actual=load(path)['assertions']
  for a in expand(aa):assert actual.count(a)==1
 assert load(c['ordinal_report_path'])==expand(c['ordinal_reports'])and hashlib.sha256(raw(c['raw_capture_capsule'])).hexdigest()==c['capsule_sha256']
 for path,digest in c['raw_sources'].items():assert hashlib.sha256(raw(path)).hexdigest()==digest
 if records is not None:
  cs={ch['id']for ch in chs};docs=[d for d in records if d.get('id')in cs or d.get('chapter_id')in cs or d.get('record_type')=='person_name_component_set'and any(n.get('chapter_id')in cs for n in d.get('records',[]))];assert len(docs)==len(expected)and all(sum(d==w for d in docs)==1 for w in expected.values())
 return c,roles,expected

def proof(root,people=None,records=None):
 return _proof(lambda p:_raw(root,p),people,records)

def errors(root):
 if not(Path(root)/REF).exists():return['晉002–004來源或側錄已安裝但缺少所屬contract']if _installed_without_contract(root)else[]
 try:proof(root);return[]
 except(AssertionError,KeyError,TypeError,ValueError,StopIteration,OSError):return['晉002–004完整原段/具體角色/姓名字/父系與收繼/雙端反查不符']
def guard_bundle(root,pid,people,records):
 if not(Path(root)/REF).exists():
  if _installed_without_contract(root):raise ValueError('Jin002–004 source/sidecar installed without contract')
  return
 c=json.loads(_raw(root,REF));cs=[json.loads(_raw(root,p))for p in c['chapter_paths']];owners={m['person_id']for ch in cs for p in ch['paragraphs']for m in p['mentions']if m.get('person_id')};cids={ch['id']for ch in cs}
 for d in records:
  if d.get('chapter_id')in cids:
   owners.update(a.get(k)for a in d.get('assertions',[])for k in('subject_person_id','object_person_id'))
  if d.get('record_type')=='person_name_component_set':owners.update(n.get('person_id')for n in d.get('records',[])if n.get('chapter_id')in cids)
 if pid in owners:proof(root,people,records)
def validate_surname(n,names,chapters,assertions,root):
 c,r,e=proof(root);assert any(n==x for d in e.values()if d.get('record_type')=='person_name_component_set'for x in d['records']);return None
def family_valid(a,root):
 try:c,r,e=proof(root);return any(a==x for d in e.values()if d.get('record_type')=='person_assertion_set'for x in d['assertions'])
 except(AssertionError,KeyError,TypeError,ValueError,StopIteration,OSError):return False
def ordinal_reports(root,ids):
 if not(Path(root)/REF).exists():
  if _installed_without_contract(root):raise ValueError('Jin002–004 ordinal source installed without contract')
  return[]
 c,r,e=proof(root);return[x for x in json.loads(_raw(root,c['ordinal_report_path']))['reports']if x['person_id']in ids]
