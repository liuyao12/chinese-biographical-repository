"""Finite Lu Qin received rendered unit; current identity endpoints come from actual MIDs."""
from pathlib import Path
import hashlib,json,re
CID='c-jinshu-044-luqin-family-rendered'
SID='s-jinshu044-lu-rendered-oldcapture'
CH='corpus/jinshu/044-luqin-family-rendered.json'
REF='source-evidence/jin044-lu-rendered/source-contract.json'
SHA='8b5ab2e84c9eb21502fe98f3c59e94d809e4d1678ebfd5e378015a01ae120179'
def same(a,b):
 if type(a)is not type(b):return False
 if isinstance(a,dict):return a.keys()==b.keys()and all(same(a[k],b[k])for k in a)
 if isinstance(a,list):return len(a)==len(b)and all(same(x,y)for x,y in zip(a,b))
 return a==b

def proof(root,ch=None):
 root=Path(root).resolve()
 def load(rel):
  p=Path(rel);assert not p.is_absolute()and '..'not in p.parts
  f=root/p;assert f.resolve()==f and f.is_file();return json.loads(f.read_text())
 payload=root/REF;assert payload.resolve()==payload and hashlib.sha256(payload.read_bytes()).hexdigest()==SHA
 b=load(REF);actual=load(CH);assert ch is None or same(ch,actual);ch=actual
 assert ch['id']==CID and ch['source_id']==SID and ch['annotation']['fixed_jin044_lu_ref']==REF
 capture=root/b['capture_ref'];assert capture.resolve()==capture and hashlib.sha256(capture.read_bytes()).hexdigest()==b['capture_sha256']
 cap=load(b['capture_ref']);assert cap['raw_acquired']is False and cap['raw_revision']is None and cap['image_verified']is False
 rows=[x for x in cap['tool_lines']if x['text'].startswith('　　')and x['tool_line']<211];assert len(rows)==len(ch['paragraphs'])==12
 people={p['id']:p for p in load('registry/persons.json')['persons']};anchors={m['id']:(p,m)for p in ch['paragraphs']for m in p['mentions']};roles={}
 for role,s in b['role_seeds'].items():
  if s['kind']=='source_local':p,m=anchors[s['first_mid']];pid=m['person_id'];assert m['kind']=='person'and pid in people
  else:
   old=load(s['path']);p=next(p for p in old['paragraphs']if p['id']==s['paragraph_id']);m=next(m for m in p['mentions']if m['id']==s['marker']['id']);assert p['text']==s['quote']and same({k:v for k,v in m.items()if k!='person_id'},s['marker']);pid=m['person_id'];assert pid in people and any(same(s['reverse'],e)for e in people[pid]['evidence'])
  roles['$'+role]=pid
 assert len(set(roles.values()))==len(roles)
 for role,seed in b['identity_exclusion_seeds'].items():
  other=load(seed['path']);p=next(p for p in other['paragraphs']if p['id']==seed['paragraph_id']);m=next(m for m in p['mentions']if m['id']==seed['marker']['id']);assert p['text']==seed['quote']and same({k:v for k,v in m.items()if k!='person_id'},seed['marker']);assert m['person_id']in people and any(same(seed['reverse'],e)for e in people[m['person_id']]['evidence'])and any(a['surface']==m['surface']and m['id']in a['mention_ids']for a in people[m['person_id']]['aliases']);assert roles['$'+role]!=m['person_id']
 def expand(x):
  if isinstance(x,str):return roles.get(x,x)
  if isinstance(x,list):return[expand(v)for v in x]
  if isinstance(x,dict):return{k:expand(v)for k,v in x.items()}
  return x
 assert same(ch,expand(b['expected_chapter']))
 family=next(a for a in load('registry/family-assemblies.json')['assemblies']if a['id']==b['assembly_id'])
 for member in expand(b['assembly_members']):assert same([m for m in family['members']if m['person_id']==member['person_id']],[member])
 for rel,expected in b['expected_sidecars'].items():assert same(load(rel),expand(expected))
 for row,p in zip(rows,ch['paragraphs']):
  text=re.sub(r'【\d+†([^】]+)】',r'\1',row['text']).lstrip('　');assert text==p['text']and p['source_position']['rendered_tool_line']==row['tool_line']
  for m in p['mentions']:
   assert m['kind']=='person'and m['surface']not in ('之','其','我','吾','弟','公')and p['text'][m['start']:m['end']]==m['surface']
   actor=people[m['person_id']];ev={'work_id':ch['work_id'],'book_id':ch['book_id'],'chapter_id':CID,'source_id':SID,'paragraph_id':p['id'],'mention_id':m['id'],'quote':m['surface']}
   assert [e for e in actor['evidence']if e.get('mention_id')==m['id']]==[ev]
   assert any(a['surface']==m['surface']and m['id']in a['mention_ids']for a in actor['aliases'])
 return ch,roles

def errors(ch,root):
 try:proof(root,ch);return []
 except (AssertionError,KeyError,ValueError,TypeError,StopIteration,OSError)as exc:return [f'{CID}: 十二段rendered來源/MID/反查資格不符 ({type(exc).__name__})']


def family_valid(record,root):
 try:
  assert record['qualifiers']['source_clause_binding']=={'kind':'fixed_jin044_lu_rendered_roles','contract_ref':REF}
  ch,roles=proof(root)
  data=json.loads((Path(root)/'corpus/jinshu/044-luqin-family-rendered-assertions.json').read_text())
  return any(same(record,a)for a in data['assertions']) and record['predicate'] in ('paternal_uncle','affinity_unspecified')
 except (AssertionError,KeyError,ValueError,TypeError,StopIteration,OSError):return False

def guard_bundle(root,person_id,people,records):
 root=Path(root);path=root/CH
 def owned(record):
  return isinstance(record,dict)and(record.get('id')==CID or record.get('chapter_id')==CID or record.get('source_id')==SID or 'fixed_jin044_lu_ref'in record.get('annotation',{}) or record.get('record_type')=='person_name_component_set'and any(x.get('chapter_id')==CID for x in record.get('records',[])))
 docs=[r for r in records if owned(r)]
 def endpoints(x):
  out=set()
  if isinstance(x,dict):
   out.update(v for k,v in x.items()if k in ('person_id','subject_person_id','object_person_id','older_person_id','younger_person_id','parent_person_id')and isinstance(v,str))
   for v in x.values():out.update(endpoints(v))
  elif isinstance(x,list):
   for v in x:out.update(endpoints(v))
  return out
 caller_related=endpoints(docs)
 if not path.is_file():
  if (root/REF).exists()or person_id in caller_related:raise ValueError('Jin044 owned source missing')
  return
 actual=json.loads(path.read_text());related={m.get('person_id')for p in actual.get('paragraphs',[])for m in p.get('mentions',[])}
 if person_id not in related|caller_related and not any(e.get('chapter_id')==CID for e in people.get(person_id,{}).get('evidence',[])):return
 try:
  ch,roles=proof(root)
  physical_people={p['id']:p for p in json.loads((root/'registry/persons.json').read_text())['persons']}
  for pid in set(roles.values()):assert pid in people and same(people[pid],physical_people[pid])
  b=json.loads((root/REF).read_text());expected=[ch]+[json.loads((root/rel).read_text())for rel in b['expected_sidecars']if rel.startswith('corpus/')]
  assert len(docs)==len(expected)and all(sum(same(x,e)for x in docs)==1 for e in expected)
 except(AssertionError,KeyError,ValueError,TypeError,StopIteration,OSError)as exc:raise ValueError('Jin044 Lu caller/source-role contract invalid')from exc

def ancestor_valid(member,rows,assertions,chapters,root):
 try:
  ch,roles=proof(root)
  assert same(chapters[ch['id']],ch)
  con=member['ancestor_connection'];assert con['owner']==CID and con['placement_status']=='editorial_inferred'and con['literal_grandfather_assertion']is False and con['same_father_independently_attested']is False and con['unknown_father_person_id']is None and con['unknown_father_name']is None and con['father_is_hao_asserted']is False and con['human_reviewed']is False
  assert member['person_id']==roles['$lin'] and member['ancestor_person_id']==roles['$ting'] and member['parent_person_id']is None and member['generation_distance']==2 and member['intermediate_person_ids']==[None]
  uncle=assertions['a-jin044-lu-010'];father=assertions['a-jin044-lu-005']
  assert uncle['predicate']=='paternal_uncle'and uncle['subject_person_id']==roles['$lin']and uncle['object_person_id']==roles['$luzhi']
  assert father['predicate']=='father'and father['subject_person_id']==roles['$luzhi']and father['object_person_id']==roles['$ting']
  actual=json.loads((Path(root)/'corpus/jinshu/044-luqin-family-rendered-assertions.json').read_text())['assertions'];assert uncle in actual and father in actual
  assert roles['$luzhi']in rows and roles['$ting']in rows
  return True
 except(AssertionError,KeyError,ValueError,TypeError,StopIteration,OSError):return False
