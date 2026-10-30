# coding:utf-8
"""Finite fixed035 registration phase: complete source; seventeen source-local actors."""
import hashlib,json
from pathlib import Path
CASE='source-evidence/jin035-peixiu-peiwei/registration-contract.json'
CASE_SHA='4229063b85517c9018a2d350f64e7b11cd4f7d70ff0b2518e13285b805e3c5ee'
CID='c-jinshu-035-peixiu-peiwei'
def same(a,b):
 if type(a)is not type(b):return False
 if type(a)is dict:return a.keys()==b.keys()and all(same(a[k],b[k])for k in a)
 if type(a)is list:return len(a)==len(b)and all(same(x,y)for x,y in zip(a,b))
 return a==b
def _registration_errors(ch,root,b=None):
 try:
  root=Path(root).resolve()
  def read(rel):return json.loads((root/rel).read_text(encoding='utf-8'))
  rawcase=(root/CASE).read_bytes();assert hashlib.sha256(rawcase).hexdigest()==CASE_SHA
  expected=json.loads(rawcase);assert b is None or same(b,expected);b=expected
  assert hashlib.sha256((root/b['projection_path']).read_bytes()).hexdigest()==b['projection_sha256']
  raw=(root/b['raw_file']).read_bytes();assert hashlib.sha256(raw).hexdigest()==b['raw_sha256']
  actual=read(b['chapter_path']);assert actual==ch and ch['id']==CID
  people={p['id']:p for p in read('registry/persons.json')['persons']};mids={m['id']:(p,m)for p in ch['paragraphs']for m in p['mentions']};roles={}
  for key,mid in b['role_first_mids'].items():
   p,m=mids[mid];assert m['kind']=='person'and m['person_id']in people;roles['$'+key]=m['person_id']
  def expand(x):
   if isinstance(x,str):return roles.get(x,x)
   if isinstance(x,list):return[expand(v)for v in x]
   if isinstance(x,dict):return{k:expand(v)for k,v in x.items()}
   return x
  assert same(ch,expand(b['chapter_template']))
  for key,s in b['known_seeds'].items():
   d=read(s['chapter_path']);assert d['source']==s['source']and {a:d[a]for a in s['dimensions']}==s['dimensions']
   p=next(p for p in d['paragraphs']if p['id']==s['paragraph_id']);m=next(m for m in p['mentions']if m['id']==s['marker']['id']);assert p['text']==s['quote']and {a:v for a,v in m.items()if a!='person_id'}==s['marker']and m['person_id']==roles['$'+key]
   person=people[m['person_id']];assert [e for e in person['evidence']if e['mention_id']==m['id']]==[s['reverse']]and any(a['surface']==m['surface']and m['id']in a['mention_ids']for a in person['aliases'])
  try:from scripts.witness_projection import repository_positions
  except ImportError:from witness_projection import repository_positions
  lines=raw.decode('utf-8').splitlines();used=[]
  for p in ch['paragraphs']:
   points,digest=repository_positions(root,p,lines);assert digest==b['raw_sha256'];used+=points
   for m in p['mentions']:
    assert p['text'][m['start']:m['end']]==m['surface'];person=people[m['person_id']];e={k:ch[k]for k in('work_id','book_id','source_id')};e.update(chapter_id=CID,paragraph_id=p['id'],mention_id=m['id'],quote=m['surface'])
    assert [v for v in person['evidence']if v.get('mention_id')==m['id']]==[e]and any(a['surface']==m['surface']and m['id']in a['mention_ids']for a in person['aliases'])
  assert used==sorted(set(used))and len(used)==sum(len(p['text'])for p in ch['paragraphs'])
  assert hashlib.sha256('\n\n'.join(p['text']for p in ch['paragraphs']).encode()).hexdigest()==ch['text_sha256']
  return []
 except(AssertionError,KeyError,ValueError,TypeError,OSError,StopIteration,IndexError):return ['035裴秀頠完整比較來源、17角色phase、固定投影、seed或雙向來源資格不符']

# Named typed-family successor. Original registration branch stays available and strict.
TYPED_CASE='source-evidence/jin035-peixiu-peiwei/typed-family-contract.json'
TYPED_SHA='ae348807413368925e82935c3d9b398eac9454d0f15204d32493544dfd76a66b'
try:from scripts.validation_context import memoized
except ImportError:from validation_context import memoized
def _typed_base_state(root, chapter_override=None, extra_sidecars=()):
 root=Path(root).resolve()
 def read(rel):return json.loads((root/rel).read_text(encoding='utf-8'))
 cb=(root/TYPED_CASE).read_bytes();assert hashlib.sha256(cb).hexdigest()==TYPED_SHA;case=json.loads(cb)
 parentb=(root/case['parent_contract_path']).read_bytes();assert hashlib.sha256(parentb).hexdigest()==case['parent_contract_sha256']==CASE_SHA;parent=json.loads(parentb)
 chapter=chapter_override if chapter_override is not None else read(case['chapter_path']);people={p['id']:p for p in read('registry/persons.json')['persons']};mids={m['id']:(p,m)for p in chapter['paragraphs']for m in p['mentions']}
 first={**parent['role_first_mids'],**case['new_role_first_mids']};roles={}
 for key,mid in first.items():
  p,m=mids[mid];assert m['kind']=='person'and m['person_id']in people;roles['$'+key]=m['person_id']
 def expand(x):
  if isinstance(x,str):return roles.get(x,x)
  if isinstance(x,list):return[expand(v)for v in x]
  if isinstance(x,dict):return{k:expand(v)for k,v in x.items()}
  return x
 assert same(chapter,expand(case['chapter_template']))
 # First validate the complete current source and all extra rows, never hide new data in an old view.
 sidecars={rel:expand(t)for rel,t in case['sidecars'].items()}
 for rel,expected in sidecars.items():assert same(read(rel),expected)
 actual=[chapter if str(f.relative_to(root))==case['chapter_path'] else read(str(f.relative_to(root)))for f in sorted((root/'corpus').glob('*/*.json'))if f.name.startswith('035-peixiu-peiwei')and f.suffix=='.json'and str(f.relative_to(root))not in extra_sidecars]
 assert len(actual)==3 and all(sum(same(x,d)for x in actual)==1 for d in [chapter,*sidecars.values()])
 import copy
 old=copy.deepcopy(chapter);old['annotation'].pop('typed_family_phase_ref')
 for p in old['paragraphs']:p['mentions']=[m for m in p['mentions']if m['id']in case['preserved_parent_marker_ids']]
 assert same(old,expand(parent['chapter_template']))
 for key,spec in {**parent['known_seeds'],**case['known_seeds']}.items():
  seed=read(spec['chapter_path']);assert same(seed['source'],spec['source'])and same({k:seed[k]for k in spec['dimensions']},spec['dimensions'])
  if 'paragraph'in spec:
   expected=expand(spec['paragraph']);p=next(p for p in seed['paragraphs']if p['id']==expected['id']);assert same(p,expected);m=next(m for m in p['mentions']if m['id']==spec['reverse']['mention_id'])
  else:
   p=next(p for p in seed['paragraphs']if p['id']==spec['paragraph_id']);m=next(m for m in p['mentions']if m['id']==spec['marker']['id']);assert p['text']==spec['quote']and same({k:v for k,v in m.items()if k!='person_id'},spec['marker'])
  assert m['person_id']==roles['$'+key];person=people[m['person_id']];assert same([e for e in person['evidence']if e['mention_id']==m['id']],[spec['reverse']])and any(a['surface']==m['surface']and m['id']in a['mention_ids']for a in person['aliases'])
 raw=(root/parent['raw_file']).read_bytes();assert hashlib.sha256(raw).hexdigest()==parent['raw_sha256'];assert hashlib.sha256((root/parent['projection_path']).read_bytes()).hexdigest()==parent['projection_sha256']
 try:from scripts.witness_projection import repository_positions
 except ImportError:from witness_projection import repository_positions
 for p in chapter['paragraphs']:
  repository_positions(root,p,raw.decode().splitlines())
  for m in p['mentions']:
   person=people[m['person_id']];e={k:chapter[k]for k in('work_id','book_id','source_id')};e.update(chapter_id=CID,paragraph_id=p['id'],mention_id=m['id'],quote=m['surface'])
   assert same([v for v in person['evidence']if v['mention_id']==m['id']],[e])and any(a['surface']==m['surface']and m['id']in a['mention_ids']for a in person['aliases'])
 for key,path in case['family_path_templates'].items():assert same(people[roles['$'+key]]['family_path'],expand(path))
 return {'chapter':chapter,'sidecars':sidecars,'roles':roles,'case':case}
@memoized(0)
def _typed_state(root):
 if (Path(root)/'source-evidence/jin035-peixiu-peiwei/contemporary-ner-contract.json').exists():
  try:from scripts.fixed_jin035_contemporary import validate_successor as current_proof
  except ImportError:from fixed_jin035_contemporary import validate_successor as current_proof
  try:from scripts.fixed_jin035_classical_allusions import validate_successor as parent_proof
  except ImportError:from fixed_jin035_classical_allusions import validate_successor as parent_proof
  current=current_proof(root);parent=parent_proof(root,current['parent_chapter'])
  sidecars={**parent['sidecars'],**current['sidecars']}
  state=_typed_base_state(root,parent['parent_chapter'],tuple(sidecars))
  state['chapter']=current['chapter'];state['sidecars'].update(sidecars);state['allusion_case']=parent['case'];state['contemporary_case']=current['case']
  return state
 if not(Path(root)/'source-evidence/jin035-peixiu-peiwei/allusion-ner-contract.json').exists():return _typed_base_state(root)
 try:from scripts.fixed_jin035_classical_allusions import validate_successor
 except ImportError:from fixed_jin035_classical_allusions import validate_successor
 proof=validate_successor(root)
 state=_typed_base_state(root,proof['parent_chapter'],tuple(proof['sidecars']))
 state['chapter']=proof['chapter'];state['sidecars'].update(proof['sidecars']);state['allusion_case']=proof['case']
 return state
def errors(ch,root,b=None):
 if not (Path(root)/TYPED_CASE).exists():return _registration_errors(ch,root,b)
 try:
  state=_typed_state(root);assert same(ch,state['chapter']);return []
 except(AssertionError,KeyError,ValueError,TypeError,OSError,IndexError,StopIteration):return ['035具名親屬姓名phase完整來源/全部原錨/新角色/側檔/反查或有源家族路徑不符']
def family_valid(a,paragraphs,root):
 try:
  st=_typed_state(root);doc=st['sidecars']['corpus/jinshu/035-peixiu-peiwei-assertions.json'];expected=next(x for x in doc['assertions']if x['id']==a['id']);assert same(a,expected)
  for p in st['chapter']['paragraphs']:assert same(paragraphs[p['id']],(CID,p))
  return True
 except(AssertionError,KeyError,ValueError,TypeError,OSError,IndexError,StopIteration):return False
def validate_surname(n,names,chapters,assertions,root):
 try:
  st=_typed_state(root);assert same(chapters[CID],st['chapter']);expected=next(x for x in st['sidecars']['corpus/jinshu/035-peixiu-peiwei-names.json']['records']if x['id']==n['id']);assert same(n,expected)
  assert sum(same(x,n)for x in names)==1
  for a in st['sidecars']['corpus/jinshu/035-peixiu-peiwei-assertions.json']['assertions']:assert sum(same(x,a)for x in assertions)==1
 except(AssertionError,KeyError,ValueError,TypeError,OSError,IndexError,StopIteration):raise ValueError('035復姓須完整本源父子/父系祖稱與literal姓名seed；不得用結構ID、母或嗣爵補姓')
def guard_bundle(root,person_id,people,records):
 if not(Path(root)/TYPED_CASE).exists():return
 # No full registry parsing for unrelated people: caller evidence plus current marker IDs.
 d=json.loads((Path(root)/'corpus/jinshu/035-peixiu-peiwei.json').read_text())
 related={m['person_id']for p in d['paragraphs']for m in p['mentions']}
 if person_id not in related and not any(e.get('chapter_id')==CID for e in people.get(person_id,{}).get('evidence',[])):return
 st=_typed_state(root)
 assert sum(same(x,st['chapter'])for x in records)==1
 for doc in st['sidecars'].values():assert sum(same(x,doc)for x in records)==1
 for p in st['chapter']['paragraphs']:
  for m in p['mentions']:
   if m['kind']=='unresolved':
    assert m['person_id']is None and m['status']=='unresolved';continue
   assert m['kind']in ('person','pronoun')and m['person_id']in people
   person=people[m['person_id']];e={k:d[k]for k in('work_id','book_id','source_id')};e.update(chapter_id=CID,paragraph_id=p['id'],mention_id=m['id'],quote=m['surface'])
   assert [v for v in person.get('evidence',[])if v.get('mention_id')==m['id']]==[e]
   if m['kind']=='pronoun':
    try:from scripts.fixed_jin035_contemporary import source_first_person
    except ImportError:from fixed_jin035_contemporary import source_first_person
    assert source_first_person(m,p['text'])and not any(m['id']in a['mention_ids']for v in people.values()for a in v.get('aliases',[]))
   else:assert any(a['surface']==m['surface']and m['id']in a['mention_ids']for a in person.get('aliases',[]))
