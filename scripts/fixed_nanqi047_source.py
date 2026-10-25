"""Fixed complete Nanqi047 source strata and three literal family roles; no AI runtime."""
import hashlib,json
from pathlib import Path
REF='source-evidence/nanqi047-xietiao/projection.json'
RAW='source-evidence/nanqi047-xietiao/KR2a0017_047-787dd9a7.txt'
RAW_SHA='ef7a016f8e2b2ffac03253a754ad75774e02e67c174793fc769792ac92a0a439'
REV='787dd9a7da495542e8f17c26c96900ce37b2c211'
PROJECTION_SHA='74d8351619b21f5625d31c8c32232e2835d025615a930374043770d7ec8dfbc4'
CIDS=('c-nanqishu-047-xietiao','c-nanqishu-047-compiler-appraisal','c-nanqishu-047-qing-collation')
KIN={'wife-father': {'paragraph_id': 'c-nanqishu-047-xietiao:p011', 'paragraph_sha256': 'ea4ce4df220dc1fa922062f438e4e013f4001e26d5aad9d4d8ff140e321762ba', 'roles': {'wife': {'start': 8, 'end': 9, 'surface': '女'}, 'wangjingze': {'start': 3, 'end': 6, 'surface': '王敬則'}, 'xietiao': {'start': 0, 'end': 1, 'surface': '朓'}}, 'subject_role': 'wife', 'object_role': 'wangjingze', 'predicate': 'father', 'source_term': '敬則女為脁妻'}, 'wife-spouse': {'paragraph_id': 'c-nanqishu-047-xietiao:p011', 'paragraph_sha256': 'ea4ce4df220dc1fa922062f438e4e013f4001e26d5aad9d4d8ff140e321762ba', 'roles': {'wife': {'start': 8, 'end': 9, 'surface': '女'}, 'wangjingze': {'start': 3, 'end': 6, 'surface': '王敬則'}, 'xietiao': {'start': 0, 'end': 1, 'surface': '朓'}}, 'subject_role': 'wife', 'object_role': 'xietiao', 'predicate': 'spouse', 'source_term': '敬則女為脁妻'}, 'younger-brother': {'paragraph_id': 'c-nanqishu-047-xietiao:p006', 'paragraph_sha256': 'a81d2e3e218401d7698823d1cd6531f860b59da0e976132763982cadb3efc056', 'roles': {'jiangsi': {'start': 19, 'end': 20, 'surface': '祀'}, 'jiangshi': {'start': 4, 'end': 6, 'surface': '江祏'}}, 'subject_role': 'jiangsi', 'object_role': 'jiangshi', 'predicate': 'brother', 'source_term': '與弟祀'}}
def errors(chapter,root):
 if not isinstance(chapter,dict):return ['固定047來源須為物件']
 if chapter.get('id')not in CIDS:return []
 try:
  root=Path(root).resolve();pp=root/REF;rp=root/RAW
  assert pp.resolve()==pp and rp.resolve()==rp
  b=pp.read_bytes();assert hashlib.sha256(b).hexdigest()==PROJECTION_SHA
  d=json.loads(b);r=rp.read_bytes();assert hashlib.sha256(r).hexdigest()==RAW_SHA;raw=r.decode('utf-8')
  assert chapter['annotation']['fixed_nanqi047_projection_ref']==REF
  source=chapter['source'];assert isinstance(source,dict)
  assert source['revision_id']==source['source_commit']==REV and source['response_sha256']==source['raw_sha256']==RAW_SHA
  assert chapter['work_id']=='w-nanqishu'and chapter['book_id']=='b-nanqishu-047'and source['image_verified']is False
  q=next(q for q in d['chapters']if q['chapter_id']==chapter['id']);assert len(q['paragraphs'])==len(chapter['paragraphs'])
  for p,v in zip(chapter['paragraphs'],q['paragraphs']):
   assert p['id']==v['paragraph_id']and p['text']==v['text']==''.join(raw[i]for i in v['raw_positions'])
   assert p['text_layer']==v['text_layer']and p['unit_id']==v['unit_id']
   sp=p['source_position'];assert sp['revision_id']==REV and sp['raw_projection_ref']==REF and sp['editorial_excerpt_boundary']is True
   assert sp['first_line']==raw.count('\n',0,v['raw_positions'][0])+1 and sp['last_line']==raw.count('\n',0,v['raw_positions'][-1])+1
  assert ''.join(p['text']for p in chapter['paragraphs'])and hashlib.sha256(''.join(p['text']for p in chapter['paragraphs']).encode()).hexdigest()==q['text_sha256']
  if chapter['id']==CIDS[2]:assert source['source_role']=='Qing_Siku_collation_independent_appendix'
  if chapter['id']==CIDS[0]:assert predecessor_roles_match(chapter,root)
  return []
 except(AssertionError,KeyError,TypeError,ValueError,IndexError,OSError,StopIteration,AttributeError):return ['固定047完整主傳／史評贊／清考證來源、原字、行界或宋052父祖同指不符']
def kinship_valid(a,paragraphs):
 if not isinstance(a,dict)or not isinstance(paragraphs,dict):return False
 try:
  q=a['qualifiers'];b=q['source_clause_binding'];spec=KIN[b['slot']];e,=a['evidence'];cid,p=paragraphs[e['paragraph_id']]
  assert isinstance(q,dict)and isinstance(b,dict)and isinstance(p,dict)
  assert cid==CIDS[0]and p['id']==spec['paragraph_id']and p['text_layer']=='received_chapter'
  assert hashlib.sha256(p['text'].encode()).hexdigest()==spec['paragraph_sha256']==b['paragraph_sha256']
  assert set(b)=={'kind','rule','slot','paragraph_sha256','roles'}and b['kind']=='biography_family_clause'and b['rule']=='fixed_nanqi047_narrative_family'
  assert set(b['roles'])==set(spec['roles']);ms={m['id']:m for m in p['mentions']};roles={k:ms[mid]for k,mid in b['roles'].items()}
  for k,m in roles.items():
   assert m['kind']=='person'and isinstance(m['person_id'],str)and {v:m[v]for v in('start','end','surface')}==spec['roles'][k]
   assert p['text'][m['start']:m['end']]==m['surface']
  assert len({m['person_id']for m in roles.values()})==len(roles)
  s=roles[spec['subject_role']];o=roles[spec['object_role']]
  assert a['predicate']==spec['predicate']and a['subject_person_id']==s['person_id']and a['object_person_id']==o['person_id']
  assert a['status']=='source_attested'and a['human_reviewed']is False and e['chapter_id']==cid and e['quote']==p['text']
  assert e['subject_person_mention_id']==s['id']and e['object_person_mention_id']==o['id']
  want={'source_term':spec['source_term'],'source_clause_binding':b}
  if a['predicate']=='father':want['lineage']='paternal'
  if a['predicate']=='brother':want['relative_birth_order']={'older_person_id':o['person_id'],'younger_person_id':s['person_id'],'operator':'lt','scope':'siblings','older_ordinal':None,'younger_ordinal':None}
  return q==want
 except(AssertionError,KeyError,TypeError,ValueError,IndexError,AttributeError):return False

# Fixed same-person source roles, not a registry ownership or person-ID whitelist.
PREDECESSOR_REF='source-evidence/nanqi047-xietiao/song052-predecessor-source-roles.json'
PREDECESSOR_SHA='e8534f0eb49d21f9cc65297f983ca3e220f2fae21fcfb8a3240fae8468c3b447'
def predecessor_roles_match(chapter,root):
 if not isinstance(chapter,dict):return False
 try:
  root=Path(root).resolve();p=root/PREDECESSOR_REF;assert p.resolve()==p
  b=p.read_bytes();assert hashlib.sha256(b).hexdigest()==PREDECESSOR_SHA;seeds=json.loads(b)
  assert set(seeds)=={'ancestor-shu','father-wei'}
  own=next(p for p in chapter['paragraphs']if p['id']=='c-nanqishu-047-xietiao:p001');ownms={m['id']:m for m in own['mentions']}
  owned={'ancestor-shu':'c-nanqishu-047-xietiao:p001:m0012','father-wei':'c-nanqishu-047-xietiao:p001:m0018'}
  for key,seed in seeds.items():
   path=root/seed['path'];assert path.resolve()==path;foreign=json.loads(path.read_bytes());source=foreign['source'];assert isinstance(source,dict)
   assert foreign['id']==seed['chapter_id']and foreign['source_id']==seed['source_id']and foreign['work_id']=='w-songshu'and foreign['book_id']=='b-songshu-052'
   assert source['revision_id']==source['source_commit']==seed['source_revision']and source['response_sha256']==seed['raw_sha256']and source['image_verified']is False
   fp=next(p for p in foreign['paragraphs']if p['id']==seed['paragraph_id']);assert hashlib.sha256(fp['text'].encode()).hexdigest()==seed['paragraph_sha256']and fp['text']==seed['quote']
   mark=next(m for m in fp['mentions']if m['id']==seed['mention_id']);om=ownms[owned[key]]
   assert mark['kind']==om['kind']=='person'and all(mark[k]==seed[k]for k in('start','end','surface'))and fp['text'][mark['start']:mark['end']]==mark['surface']
   assert isinstance(mark['person_id'],str)and mark['person_id']and om['person_id']==mark['person_id']
  return True
 except(AssertionError,KeyError,ValueError,TypeError,IndexError,AttributeError,StopIteration,OSError):return False
