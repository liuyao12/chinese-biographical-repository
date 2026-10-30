"""Finite received Liang041 complete unit: source, roles, and reciprocal NER evidence."""
import json,hashlib,re
from pathlib import Path
REF='source-evidence/liang041-wanggui-ws1512987/complete-unit-contract.json'
SHA='f20b4eed82aabb73c636a60eb8a16dd713ee6b7398d7eb9404fe38706ba9e3c2'
CID='c-liangshu-041-wanggui-ws1512987'
def same(a,b):
 return type(a)is type(b)and (a.keys()==b.keys()and all(same(a[k],b[k])for k in a)if isinstance(a,dict)else len(a)==len(b)and all(same(x,y)for x,y in zip(a,b))if isinstance(a,list)else a==b)
def _base_proof(root,ch=None,people=None):
 root=Path(root);b=(root/REF).read_bytes();assert hashlib.sha256(b).hexdigest()==SHA;c=json.loads(b)
 if ch is None:ch=json.loads((root/c['chapter_path']).read_text())
 if people is None:people={p['id']:p for p in json.loads((root/'registry/persons.json').read_text())['persons']}
 rawb=(root/c['raw_file']).read_bytes();assert hashlib.sha256(rawb).hexdigest()==c['raw_sha256'];raw=rawb.decode();s=c['selection'];assert raw.count(s['opening_heading'])==raw.count(s['following_heading'])==1 and raw.index(s['opening_heading'])==s['start']and raw.index(s['following_heading'])==s['end']and raw[s['start']:s['end']]==s['raw']
 assert same(ch,c['chapter_template'])
 for p in ch['paragraphs']:
  ix=p['source_position']['raw_character_offsets'];assert p['text']==''.join(raw[i]for i in ix)
  for m in p['mentions']:
   assert p['text'][m['start']:m['end']]==m['surface']
   if m['kind']=='person':
    person=people[m['person_id']];e={k:ch[k]for k in('work_id','book_id','source_id')};e.update(chapter_id=ch['id'],paragraph_id=p['id'],mention_id=m['id'],quote=m['surface']);assert [v for v in person['evidence']if v.get('mention_id')==m['id']]==[e];assert sum(a['surface']==m['surface']and m['id']in a['mention_ids']for a in person['aliases'])==1
   else:assert m['kind']=='unresolved'and m['person_id']is None and m['status']=='unresolved'
 for pid,want in c['new_people'].items():
  actual=people[pid];assert all(same(actual.get(k),v)for k,v in want.items()if k not in('aliases','evidence'))
 for pid,want in c['registry_reverse'].items():
  actual=people[pid];ev=[e for e in actual['evidence']if e.get('chapter_id')==CID];assert same(ev,want['evidence'])
  al=[{'surface':a['surface'],'mention_ids':[m for m in a['mention_ids']if m.startswith(CID+':')]}for a in actual['aliases']if any(m.startswith(CID+':')for m in a['mention_ids'])];wal=[{'surface':a['surface'],'mention_ids':[m for m in a['mention_ids']if m.startswith(CID+':')]}for a in want['aliases']];assert same(al,wal)
 return ch,c

def proof(root,ch=None,people=None):
 if (Path(root)/'source-evidence/liang041-wanggui-ws1512987/taoshiheng-identity-successor.json').exists():
  try:from scripts.fixed_liang041_taoshiheng import proof as successor_proof
  except ImportError:from fixed_liang041_taoshiheng import proof as successor_proof
  return successor_proof(root,ch,people)
 return _base_proof(root,ch,people)

def errors(ch,root):
 try:proof(root,ch);return []
 except(AssertionError,KeyError,ValueError,TypeError,OSError,IndexError,StopIteration):return ['梁041完整王規附傳固定來源、角色或反查不符；不得以王立/劉子/異朝同名替代或改原字重hash']
def guard_bundle(root,pid,people,records):
 if not(Path(root)/REF).exists():return
 try:from scripts.fixed_liang041_taoshiheng import owner_applies
 except ImportError:from fixed_liang041_taoshiheng import owner_applies
 relevant=any(e.get('chapter_id')==CID for e in people.get(pid,{}).get('evidence',[]))or owner_applies(pid,people,records)
 if not relevant:return
 ch,c=proof(root,people=people);assert sum(same(r,ch)for r in records)==1
 if (Path(root)/'source-evidence/liang041-wanggui-ws1512987/taoshiheng-identity-successor.json').exists():
  try:from scripts.fixed_liang041_taoshiheng import guard_catalog
  except ImportError:from fixed_liang041_taoshiheng import guard_catalog
  guard_catalog(root,people,records)
 if (Path(root)/NAME_REF).exists():validate_names_installed(root,[n for r in records if r.get('record_type')=='person_name_component_set'for n in r['records']])

# Finite names sidecar: the received chapter contract remains unchanged.
NAME_REF='source-evidence/liang041-wanggui-ws1512987/name-components-contract.json'
NAME_SHA='1c60b00472a63f871872f893dce52ce19f9d44ac793dc0750dba027fd80ae0c2'
def name_applies(n):
 return isinstance(n,dict)and(n.get('chapter_id')==CID or str(n.get('person_mention_id','')).startswith(CID+':')or str(n.get('id','')).startswith('name-liang041-'))
def name_contract(root):
 root=Path(root);raw=(root/NAME_REF).read_bytes();assert hashlib.sha256(raw).hexdigest()==NAME_SHA;nc=json.loads(raw);ch,c=proof(root)
 for n in nc['record']['records']:
  p=next(p for p in ch['paragraphs']if p['id']==n['paragraph_id']);a=n['source_anchor'];m=next(m for m in p['mentions']if m['id']==a['mention_id']);assert m['id']==n['person_mention_id']and m['person_id']==n['person_id']and p['text'][a['start']:a['end']]==a['surface']==m['surface'];assert n['name_source_binding']['person_anchor']==a
  z=n['name_source_binding']['zi_anchor']
  if z:
   zm=next(m for m in p['mentions']if m['id']==z['mention_id']);assert zm['person_id']==n['person_id']and zm['surface']==n['zi']and p['text'][m['end']:zm['start']]in ('字','，字')
  if 'surname_basis'in n:
   sb=n['surname_basis'];sa=sb['surname_anchor'];sp=next(p for p in ch['paragraphs']if p['id']==sa['paragraph_id']);sm=next(m for m in sp['mentions']if m['id']==sa['mention_id']);assert sm['surface']=='王規'and sm['person_id']==c['roles']['gui']and n['surname']=='王'and sb['relative_anchor']==a and sb['kinship_term']in p['text'];assert m['surface']==n['ming']
  else:assert m['surface']==n['surname']+n['ming']
 return nc
def name_valid(n,root):
 try:
  nc=name_contract(root);return sum(same(n,w)for w in nc['record']['records'])==1
 except(AssertionError,KeyError,ValueError,TypeError,OSError,IndexError,StopIteration):return False
def validate_names_installed(root,names):
 if not(Path(root)/NAME_REF).exists():return
 nc=name_contract(root);actual=[n for n in names if name_applies(n)];assert same(actual,nc['record']['records'])
def validate_surname(n,names,chapters,assertions,root=None):
 if not name_valid(n,root):raise ValueError('梁041復姓須固定原名錨與具名傳主近親語境')

def uncle_applies(a):
 return isinstance(a,dict)and any(e.get('chapter_id')==CID for e in a.get('evidence',[]))
def uncle_valid(a,paragraphs,root):
 try:
  ch,c=proof(root);p=next(p for p in ch['paragraphs']if p['id']==CID+':p002');sm=next(m for m in p['mentions']if m['id']==CID+':p002:m0000');om=next(m for m in p['mentions']if m['id']==CID+':p002:m0037');e={k:ch[k]for k in ('work_id','book_id','source_id')};e.update(chapter_id=CID,paragraph_id=p['id'],quote=p['text'],subject_person_mention_id=sm['id'],object_person_mention_id=om['id'])
  return a.get('predicate')=='paternal_uncle'and a.get('subject_person_id')==sm['person_id']==c['roles']['gui']and a.get('object_person_id')==om['person_id']==c['roles']['jan']and a.get('qualifiers')=={'source_term':'叔父暕','lineage':'paternal'}and a.get('evidence')==[e]and p['text'][om['start']-2:om['end']]=='叔父暕'
 except(AssertionError,KeyError,ValueError,TypeError,OSError,IndexError,StopIteration):return False

# Header choices use only the two received inherited-rank clauses.
RANK_REF='source-evidence/liang041-wanggui-ws1512987/inherited-rank-heading-contract.json'
RANK_SHA='9c9c39769b311782fbcdb0ffc7d0a115a3f7c8cc668a6fedece3c09eb852dca1'
def inherited_rank_valid(h,ch,root):
 try:
  root=Path(root);fixed,c=proof(root,ch);raw=(root/RANK_REF).read_bytes();assert hashlib.sha256(raw).hexdigest()==RANK_SHA;rc=json.loads(raw);assert sum(same(h,w)for w in rc['holdings'])==1
  b=h['source_career_role'];assert b['kind']=='fixed_liang041_explicit_inherited_rank'and b['contract_ref']==RANK_REF;p=next(p for p in fixed['paragraphs']if p['id']==b['paragraph_id']);a,=h['attestations'];m=next(m for m in p['mentions']if m['id']==b['recipient_mention_id']);assert m['kind']=='person'and m['person_id']==h['person_id'];topic=next(m for pp in fixed['paragraphs']for m in pp['mentions']if m['id']==b['recipient_topic_mention_id']);assert topic['person_id']==m['person_id'];ca=b['source_clause_anchor'];ta=b['title_anchor'];assert p['text'][ca['start']:ca['end']]==ca['surface']=='服闋，襲封'+h['title'];assert ta=={k:a[k]for k in ('paragraph_id','start','end','surface')}and p['text'][ta['start']:ta['end']]==ta['surface']==h['title'];assert h['kind']=='noble_rank'and h['mode']=='accession';assert h['effective_period']['start']['date_expression']is None and h['effective_period']['end']=={'status':'unknown','date_expression':None,'evidence':[]};return True
 except(AssertionError,KeyError,ValueError,TypeError,OSError,IndexError,StopIteration):return False
