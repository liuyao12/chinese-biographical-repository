"""Finite Jin073 Yuyi rendered source; no glyph correction, lineage guessing or PID whitelist."""
import copy,hashlib,json,re
from pathlib import Path
CID='c-jinshu-073-yuyi-ws2296501-rendered'
CH='corpus/jinshu/073-yuyi-ws2296501-rendered.json'
SID='s-jinshu073-yuyi-ws2296501-rendered'
REF='source-evidence/jin073-yuyi-ws2296501/source-contract.json'
SHA='72fcb8aa52fa47c1dd936601105a0177e6a8710ffcc41ffc02ca47927cbe57a5'
PRONOUNS={'c-jinshu-073-yuyi-ws2296501-rendered:p001:m0099': {'id': 'c-jinshu-073-yuyi-ws2296501-rendered:p001:m0099', 'start': 99, 'end': 101, 'surface': '陛下', 'kind': 'pronoun', 'status': 'resolved_contextual', 'source_identity_role': 'chengdi', 'source_reference_binding': {'kind': 'fixed_jin073_yuyi_reference', 'contract_ref': 'source-evidence/jin073-yuyi-ws2296501/source-contract.json', 'role': 'chengdi', 'paragraph_sha256': '096bd9eb097d96104f44193fc817a8c4dd1403524e00de6fb723bb3df2ec0dbf'}}, 'c-jinshu-073-yuyi-ws2296501-rendered:p006:m0053': {'id': 'c-jinshu-073-yuyi-ws2296501-rendered:p006:m0053', 'start': 53, 'end': 54, 'surface': '臣', 'kind': 'pronoun', 'status': 'resolved_contextual', 'source_identity_role': 'yi', 'source_reference_binding': {'kind': 'fixed_jin073_yuyi_reference', 'contract_ref': 'source-evidence/jin073-yuyi-ws2296501/source-contract.json', 'role': 'yi', 'paragraph_sha256': 'f1df213a7ada87a186deeeb8a98459b231e2f8f7b7fc1794a42bfb1bd70f74aa'}}, 'c-jinshu-073-yuyi-ws2296501-rendered:p006:m0179': {'id': 'c-jinshu-073-yuyi-ws2296501-rendered:p006:m0179', 'start': 179, 'end': 180, 'surface': '臣', 'kind': 'pronoun', 'status': 'resolved_contextual', 'source_identity_role': 'yi', 'source_reference_binding': {'kind': 'fixed_jin073_yuyi_reference', 'contract_ref': 'source-evidence/jin073-yuyi-ws2296501/source-contract.json', 'role': 'yi', 'paragraph_sha256': 'f1df213a7ada87a186deeeb8a98459b231e2f8f7b7fc1794a42bfb1bd70f74aa'}}, 'c-jinshu-073-yuyi-ws2296501-rendered:p008:m0000': {'id': 'c-jinshu-073-yuyi-ws2296501-rendered:p008:m0000', 'start': 0, 'end': 1, 'surface': '臣', 'kind': 'pronoun', 'status': 'resolved_contextual', 'source_identity_role': 'yi', 'source_reference_binding': {'kind': 'fixed_jin073_yuyi_reference', 'contract_ref': 'source-evidence/jin073-yuyi-ws2296501/source-contract.json', 'role': 'yi', 'paragraph_sha256': 'aecf37b8c6826c25a1ac0faf8fd896874f202549d230a070b9f381697410b1e4'}}, 'c-jinshu-073-yuyi-ws2296501-rendered:p009:m0066': {'id': 'c-jinshu-073-yuyi-ws2296501-rendered:p009:m0066', 'start': 66, 'end': 67, 'surface': '臣', 'kind': 'pronoun', 'status': 'resolved_contextual', 'source_identity_role': 'yi', 'source_reference_binding': {'kind': 'fixed_jin073_yuyi_reference', 'contract_ref': 'source-evidence/jin073-yuyi-ws2296501/source-contract.json', 'role': 'yi', 'paragraph_sha256': 'be650c7df2aff29f01341da179430afc9f39fa89641cc3dc3ed392fc6d321e38'}}, 'c-jinshu-073-yuyi-ws2296501-rendered:p010:m0029': {'id': 'c-jinshu-073-yuyi-ws2296501-rendered:p010:m0029', 'start': 29, 'end': 30, 'surface': '臣', 'kind': 'pronoun', 'status': 'resolved_contextual', 'source_identity_role': 'yi', 'source_reference_binding': {'kind': 'fixed_jin073_yuyi_reference', 'contract_ref': 'source-evidence/jin073-yuyi-ws2296501/source-contract.json', 'role': 'yi', 'paragraph_sha256': '32934dd233c4338ac0585e32742301c4539ae66ae63f53c5b7ab3faa00cfbd65'}}, 'c-jinshu-073-yuyi-ws2296501-rendered:p011:m0038': {'id': 'c-jinshu-073-yuyi-ws2296501-rendered:p011:m0038', 'start': 38, 'end': 39, 'surface': '我', 'kind': 'pronoun', 'status': 'resolved_contextual', 'source_identity_role': 'yi', 'source_reference_binding': {'kind': 'fixed_jin073_yuyi_reference', 'contract_ref': 'source-evidence/jin073-yuyi-ws2296501/source-contract.json', 'role': 'yi', 'paragraph_sha256': 'db3b1386aa5275024f2851fae59ccb512865d91d52975f7bd592c1f70248ffc9'}}}

def same(a,b):
 if type(a)is not type(b):return False
 if isinstance(a,dict):return a.keys()==b.keys()and all(same(a[k],b[k])for k in a)
 if isinstance(a,list):return len(a)==len(b)and all(same(x,y)for x,y in zip(a,b))
 return a==b

def read(root,rel):
 root=Path(root).resolve();r=Path(rel);assert not r.is_absolute()and '..'not in r.parts;p=root/r;assert p.resolve()==p and p.is_file();return p.read_bytes()

def expand(x,roles):
 if isinstance(x,str):return roles.get(x,x)
 if isinstance(x,list):return[expand(v,roles)for v in x]
 if isinstance(x,dict):return{k:expand(v,roles)for k,v in x.items()}
 return x

def source_reference(m,text=None):
 if not isinstance(m,dict):return False
 expected=PRONOUNS.get(m.get('id'))
 return expected is not None and same({k:v for k,v in m.items()if k!='person_id'},expected)and isinstance(m.get('person_id'),str)and(text is None or hashlib.sha256(text.encode()).hexdigest()==expected['source_reference_binding']['paragraph_sha256'])

LACUNA_REFERENCE={'id': 'c-jinshu-073-yuyi-ws2296501-rendered:p012:m0102', 'start': 102, 'end': 109, 'surface': '江[A170]', 'kind': 'person', 'status': 'contextual_provisional', 'source_identity_role': 'jiangbin', 'identity_reading_ref': 'source-evidence/jin073-yuyi-ws2296501/textual-decisions.json#jiangbin', 'source_surface_lacuna': {'kind': 'received_digital_lacuna_person_reference', 'contract_ref': 'source-evidence/jin073-yuyi-ws2296501/source-contract.json', 'received_surface': '江[A170]', 'lacuna_token': '[A170]', 'resolved_original_grapheme': None, 'original_grapheme_verified': False, 'actual_print_edition': None, 'image_verified': False, 'not_a_name_component': True, 'not_a_profile_alias': True, 'paragraph_sha256': '3f5ed4266311d3406de9f6d7f0d50fac7ed7a83864f80fe3b3622e18af477906'}, 'identity_judgment': {'kind': 'same_office_same_event_parallel_witness', 'status': 'contextual_provisional', 'current_person_role': 'jiangbin', 'comparison_ref': 'source-evidence/jin073-yuyi-ws2296501/comparison-siku-observation.json', 'human_reviewed': False, 'rationale': '參校同一翼卒未幾、曹據被殺與長史/朱燾/袁真共誅亂事件明江虨，與現役075江虨年代相容且無反證；人物首選與未知缺字字形分開。'}}

def source_lacuna_reference(m,text):
 if not isinstance(m,dict)or not isinstance(text,str):return False
 return same({k:v for k,v in m.items()if k!='person_id'},LACUNA_REFERENCE)and isinstance(m.get('person_id'),str)and hashlib.sha256(text.encode()).hexdigest()==LACUNA_REFERENCE['source_surface_lacuna']['paragraph_sha256']

def proof(root,people=None,records=None):
 raw=read(root,REF);assert hashlib.sha256(raw).hexdigest()==SHA;c=json.loads(raw);ch=json.loads(read(root,CH));people=people if people is not None else{p['id']:p for p in json.loads(read(root,'registry/persons.json'))['persons']};roles={}
 assert hashlib.sha256(read(root,c['source_capture_path'])).hexdigest()==c['source_capture_sha256']
 assert hashlib.sha256(read(root,c['comparison_capture_path'])).hexdigest()==c['comparison_capture_sha256']
 for rel,h in c['auxiliary_capture_pins'].items():assert hashlib.sha256(read(root,rel)).hexdigest()==h
 for role,s in c['role_seeds'].items():
  if s['kind']=='source_local':p,=[p for p in ch['paragraphs']if p['id']==s['paragraph_id']];m,=[m for m in p['mentions']if m['id']==s['mid']];assert m['kind']=='person'and m['source_identity_role']==role
  else:
   source=json.loads(read(root,s['path']));assert source['id']==s['chapter_id']and same(source['source'],s['source']);p,=[p for p in source['paragraphs']if p['id']==s['paragraph_id']];m,=[m for m in p['mentions']if m['id']==s['marker']['id']];assert p['text']==s['quote']and same({k:v for k,v in m.items()if k!='person_id'},s['marker']);assert m['person_id']in people and any(same(e,s['reverse'])for e in people[m['person_id']]['evidence'])
  assert m['person_id']in people;roles['$'+role]=m['person_id']
 assert len(set(roles.values()))==len(roles)
 for ex in c['identity_exclusion_seeds']:
  other=json.loads(read(root,ex['path']));p,=[p for p in other['paragraphs']if p['id']==ex['paragraph_id']];m,=[m for m in p['mentions']if m['id']==ex['marker']['id']];assert p['text']==ex['quote']and same({k:v for k,v in m.items()if k!='person_id'},ex['marker']);assert m['person_id']in people and any(same(e,ex['reverse'])for e in people[m['person_id']]['evidence']);assert roles['$'+ex['role']]!=m['person_id']
 expected=expand(c['expected_owned'],roles)
 for rel,want in expected.items():assert same(json.loads(read(root,rel)),want)
 assert ch['id']==CID and ch['source_id']==SID and same(ch,expected[CH])
 # Both new sons must remain actual children in current family IDs; positions do not assert ordinals.
 try:from scripts.person_ids import family_path_errors
 except ImportError:from person_ids import family_path_errors
 assert set(c['family_path_templates'])=={'fangzhi','yuanzhi'}
 for role in ('fangzhi','yuanzhi'):
  pid=roles['$'+role];path=expand(c['family_path_templates'][role],roles);assert path['connection']=='father'and path['parent_person_id']==roles['$yi']and same(people[pid].get('family_path'),path)and not family_path_errors(pid,path)
 # Surname proof is an actual full-name marker plus this chapter's two exact father clauses.
 assert c['role_seeds']['yi']['marker']['surface']=='庾翼'
 own_mids={m['id']:m for p in ch['paragraphs']for m in p['mentions']};reverse={};aliases={}
 for p in ch['paragraphs']:
  end=0
  for m in p['mentions']:
   assert end<=m['start']<m['end']and p['text'][m['start']:m['end']]==m['surface'];end=m['end']
   if m['kind']not in('person','pronoun'):continue
   pid=m['person_id'];assert pid==roles['$'+m['source_identity_role']]
   reverse.setdefault(pid,[]).append(dict(work_id=ch['work_id'],book_id=ch['book_id'],chapter_id=CID,source_id=SID,paragraph_id=p['id'],mention_id=m['id'],quote=m['surface']))
   if m['kind']=='pronoun':assert source_reference(m,p['text'])
   elif 'source_surface_lacuna'in m:assert source_lacuna_reference(m,p['text'])
   elif 'source_preferred_reading_binding'in m:assert same({k:v for k,v in m.items()if k!='person_id'},c['high_preferred_marker'])
   else:aliases.setdefault(pid,{}).setdefault(m['surface'],[]).append(m['id'])
 for pid,a in people.items():
  assert same([e for e in a['evidence']if e.get('chapter_id')==CID],reverse.get(pid,[]))
  actual={v['surface']:[mid for mid in v['mention_ids']if mid in own_mids]for v in a['aliases']if any(mid in own_mids for mid in v['mention_ids'])};assert same(actual,aliases.get(pid,{}))
 # The received blocks remain exactly projected; comparison is not promoted to base.
 cap=json.loads(read(root,c['source_capture_path']));assert cap['fixed_permalink_body_read']is False and cap['raw_wikitext_obtained']is False and cap['actual_print_base']is None
 for p,b in zip(ch['paragraphs'],cap['body_blocks']):
  text=b['observed_text'];text=text[2:]if text.startswith('> ')else text;text=text.lstrip('　 ');text=re.sub(r'\^\{【\d+†\[\d+\]】\}','',text);text=re.sub(r'【\d+†([^】]+)】',r'\1',text);assert p['text']==text
 cal=json.loads(read(root,'source-evidence/jin073-yuyi-ws2296501/age-life-calendar-contract.json'));assert cal['normalized_year']==345 and cal['source_expression']=='永和元年'and cal['read_scope']=='single av498 row, not entire era-table certification';assert hashlib.sha256(read(root,cal['existing_saved_input'])).hexdigest()==cal['existing_saved_input_sha256']
 works=json.loads(read(root,'registry/works.json'))['works'];work,=[w for w in works if w['id']=='w-jinshu'];book,=[b for b in work['books']if b['id']==ch['book_id']];assert CID in book['chapter_ids'];base=json.loads(read(root,'registry/work-provenance.json'))['text_bases'][SID];assert base['status']=='unknown'and base['edition_id']is None
 if records is not None:
  docs=[d for d in records if isinstance(d,dict)and(d.get('id')==CID or d.get('chapter_id')==CID or d.get('record_type')=='person_name_component_set'and any(n.get('chapter_id')==CID for n in d.get('records',[])))];assert len(docs)==len(expected)and all(sum(same(d,w)for d in docs)==1 for w in expected.values())
 return ch,c,roles,expected

def errors(ch,root):
 try:proof(root);assert same(ch,json.loads(read(root,CH)));return []
 except(AssertionError,KeyError,ValueError,TypeError,StopIteration,OSError)as e:return['晉073庾翼來源字串/角色/反查/生卒報齡資格不符 ('+type(e).__name__+')']

def guard_bundle(root,pid,people,records):
 path=Path(root)/CH
 if not path.is_file():
  if(Path(root)/REF).exists()or any(d.get('id')==CID or d.get('chapter_id')==CID for d in records):raise ValueError('Jin073 owned source missing')
  return
 actual=json.loads(path.read_bytes());owners={m['person_id']for p in actual['paragraphs']for m in p['mentions']if m['kind']in('person','pronoun')}
 if pid in owners:proof(root,people,records)

def validate_surname(n,names,chapters,assertions,root):
 ch,c,r,w=proof(root);ns=w[CH[:-5]+'-name-components.json']['records'];assert sum(same(n,x)for x in ns)==1 and all(x in names for x in ns)and same(chapters[CID],ch)
 return None

def family_valid(a,root):
 try:ch,c,r,w=proof(root);return any(same(a,x)for x in w[CH[:-5]+'-assertions.json']['assertions'])
 except(AssertionError,KeyError,ValueError,TypeError,StopIteration,OSError):return False

def age_valid(a,ch,root):
 try:actual,c,r,w=proof(root);return same(actual,ch)and any(same(a,x)for x in actual['annotation']['age_assertions'])
 except(AssertionError,KeyError,ValueError,TypeError,StopIteration,OSError):return False

def life_valid(e,ch,root):
 try:actual,c,r,w=proof(root);return same(actual,ch)and any(same(e,x)for x in w[CH[:-5]+'-life-events.json']['events'])
 except(AssertionError,KeyError,ValueError,TypeError,StopIteration,OSError):return False
