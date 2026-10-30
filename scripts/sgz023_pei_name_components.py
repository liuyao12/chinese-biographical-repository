"""Three source-bound Pei names; editorial surnames never populate other records."""
import json,hashlib
from pathlib import Path
CID='c-sanguozhi-023-peiqian-ws2376966'
REF='source-evidence/sgz023-peiqian-ws2376966/three-name-components-contract.json'
SHA='1d6a5dd13bff376497ab03aaaa1bafc860e465ece483f1ec4c35aaf3df1d994e'
MIDS={CID+':p009:'+v for v in ('m0458','m0474','m0508')}
def same(a,b):return type(a)is type(b)and(a.keys()==b.keys()and all(same(a[k],b[k])for k in a)if isinstance(a,dict)else len(a)==len(b)and all(same(x,y)for x,y in zip(a,b))if isinstance(a,list)else a==b)
def applies(n):return isinstance(n,dict)and(n.get('person_mention_id')in MIDS or str(n.get('id','')).startswith('name-sgz023-peiqian-') or (isinstance(n.get('component_binding'),dict)and n['component_binding'].get('kind')=='fixed_sgz023_three_literal_ming_zi') or (isinstance(n.get('surname_basis'),dict)and n['surname_basis'].get('kind')=='contextual_surname_from_fixed_sgz023_explicit_shared_father'))
def proof(root):
 root=Path(root);raw=(root/REF).read_bytes();assert hashlib.sha256(raw).hexdigest()==SHA;c=json.loads(raw)
 try:from scripts.fixed_sgz023_works import proof as current_source_proof
 except ImportError:from fixed_sgz023_works import proof as current_source_proof
 state=current_source_proof(root);ch=state['chapter'];p=next(p for p in ch['paragraphs']if p['id']==CID+':p009');ms={m['id']:m for m in p['mentions']};roles={k:ms[mid]['person_id']for k,mid in c['role_mids'].items()};assert len(set(roles.values()))==5 and all(ms[mid]['kind']=='person'for mid in c['role_mids'].values())
 def expand(x):
  if isinstance(x,str):return roles.get(x[1:],x)if x.startswith('$')else x
  if isinstance(x,list):return[expand(v)for v in x]
  if isinstance(x,dict):return{k:expand(v)for k,v in x.items()}
  return x
 expected=expand(c['name_template']);assert same(json.loads((root/c['name_path']).read_bytes()),expected)
 assertions=json.loads((root/c['assertion_path']).read_bytes())['assertions'];selected=expand(c['family_assertion_templates']);assert all(sum(same(a,w)for a in assertions)==1 for w in selected)
 by={a['id']:a for a in selected};seed=expand(c['literal_seed_template']);actual_seed=next(n for n in json.loads((root/c['literal_seed_path']).read_bytes())['records']if n['id']==seed['id']);assert same(actual_seed,seed)
 try:from scripts.fixed_wuyingdian_jin040_jiachong import name_record_valid as literal_seed_valid
 except ImportError:from fixed_wuyingdian_jin040_jiachong import name_record_valid as literal_seed_valid
 assert literal_seed_valid(actual_seed,root)and seed['surname']=='裴'and seed['ming']=='楷'and seed['person_id']==roles['kai']
 for n in expected['records']:
  binding=n['component_binding'];m=ms[binding['ming_mention_id']];z=ms[binding['zi_mention_id']];assert m['person_id']==z['person_id']==n['person_id']and m['surface']==n['ming']and z['surface']==n['zi']and p['text'][m['end']:z['start']]=='，字';assert n['source_anchor']=={k:m[k]for k in ('start','end','surface')}
  sb=n['surname_basis'];a,ka=[by[key]for key in sb['assertion_ids']];assert a['predicate']==ka['predicate']=='father'and a['subject_person_id']==n['person_id']and ka['subject_person_id']==roles['kai']and a['object_person_id']==ka['object_person_id']==roles['hui']==sb['common_father_person_id'];assert n['surname']==seed['surname']and sb['source_name_record_id']==seed['id']
  for claim in (a,ka):
   e,=claim['evidence'];sm=ms[e['subject_person_mention_id']];fm=ms[e['object_person_mention_id']];assert sm['person_id']==claim['subject_person_id']and fm['person_id']==roles['hui']and e['quote']==p['text']
  extra=binding['additional_name_mention_ids'];assert [ms[mid]['surface']for mid in extra]==n['additional_names']
  if extra:assert len(extra)==1 and ms[extra[0]]['person_id']==n['person_id']and p['text'][z['end']:ms[extra[0]]['start']]=='，一名'
 return expected

def name_valid(n,root):
 try:return sum(same(n,w)for w in proof(root)['records'])==1
 except(AssertionError,KeyError,ValueError,TypeError,OSError,IndexError,StopIteration):return False

def installed(root,names):
 if not(Path(root)/REF).exists():return
 expected=proof(root);assert same([n for n in names if applies(n)],expected['records'])

def validate_surname(n,names,chapters,assertions,root=None):
 if not name_valid(n,root):raise ValueError('裴氏三姓名須固定字名/一名錨與同父雙證，不以ID或近字復姓')

def guard_bundle(root,pid,people,records):
 if not(Path(root)/REF).exists():return
 # Ownership follows the true current source slots, never a caller's optional
 # reverse entries or a permanent person-ID list.
 disk=json.loads((Path(root)/'corpus/sanguozhi/023-peiqian-ws2376966.json').read_bytes());assert disk['id']==CID
 paragraph,=[p for p in disk['paragraphs']if p['id']==CID+':p009'];slots=[m for m in paragraph['mentions']if m['id']in MIDS]
 assert len(slots)==3 and {m['id']for m in slots}==MIDS and len({m.get('person_id')for m in slots})==3
 assert all(m.get('kind')=='person'and m.get('person_id')and paragraph['text'][m['start']:m['end']]==m['surface']for m in slots)
 owners={m['person_id']for m in slots}
 caller_chapters=[r for r in records if r.get('record_type')=='marked_chapter'and r.get('id')==CID]
 caller_owners={m.get('person_id')for ch in caller_chapters for p in ch['paragraphs']for m in p['mentions']if m.get('id')in MIDS}
 reverse_claim=any(e.get('mention_id')in MIDS for e in people.get(pid,{}).get('evidence',[]))
 if pid not in owners and pid not in caller_owners and not reverse_claim:return
 assert pid in owners and len(caller_chapters)==1 and same(caller_chapters[0],disk)
 installed(root,[n for r in records if r.get('record_type')=='person_name_component_set'for n in r['records']])
 actor=people[pid]
 for m in slots:
  if m['person_id']!=pid:continue
  expected={k:disk[k]for k in ('work_id','book_id','source_id')};expected.update(chapter_id=CID,paragraph_id=paragraph['id'],mention_id=m['id'],quote=m['surface'])
  assert [e for e in actor.get('evidence',[])if e.get('mention_id')==m['id']]==[expected]
  assert sum(a.get('surface')==m['surface']and m['id']in a.get('mention_ids',[])for a in actor.get('aliases',[]))==1
