"""Finite person-reading phase of the complete WS2479706 Jia unit; no text recognition."""
from pathlib import Path
import json,hashlib
try:
 from scripts import fixed_jin031_jia_comparison as core
 from scripts.validation_context import memoized
except ImportError:
 import fixed_jin031_jia_comparison as core
 from validation_context import memoized
EP='source-evidence/jin031-jia-comparison/full-ner-proof.json'
PROOF_SHA='fd0f82c98d6a465494a22e0d857dfbd0d9edfa4c4548f24050a7caddbd76ab26'
IP='corpus/jinshu/031-jia-comparison-identities.json'
NSN='corpus/jinshu/031-jia-comparison-ner-names.json'
H=lambda b:hashlib.sha256(b).hexdigest()
need=core.need
read=core.read
expand=core.expand

def fixed(root):
 data=core.path(root,EP).read_bytes();need(H(data)==PROOF_SHA,'完整NER契約漂移')
 try:from scripts.fixed_jin031_jia_typed import effective
 except ImportError:from fixed_jin031_jia_typed import effective
 return effective(json.loads(data),root)

@memoized(0)
def source_index(root):
 p=Path(root)/core.CH
 if not p.is_file():return {'active':False,'person_ids':[]}
 ch=read(root,core.CH);enabled=bool(ch.get('annotation',{}).get('fixed_jin031_full_ner_ref'))
 ids={m['person_id']for p in ch.get('paragraphs',[])for m in p.get('mentions',[])if m.get('kind')in('person','pronoun')and isinstance(m.get('person_id'),str)}
 if enabled and (Path(root)/'registry/persons.json').is_file():
  for person in read(root,'registry/persons.json')['persons']:
   if any(e.get('chapter_id')==core.CID for e in person.get('evidence',[])) or any(mid.startswith(core.CID+':')for a in person.get('aliases',[])for mid in a.get('mention_ids',[])if isinstance(mid,str)):
    ids.add(person['id'])
 return {'active':enabled,'person_ids':sorted(ids)}

def active(root):return source_index(root)['active']

def reverse(person,ch,p,m):
 evidence={k:ch[k]for k in ('work_id','book_id','source_id')}
 evidence.update(chapter_id=ch['id'],paragraph_id=p['id'],mention_id=m['id'],quote=m['surface'])
 rows=[e for e in person.get('evidence',[])if e.get('mention_id')==m['id']]
 need(len(rows)==1 and all(rows[0].get(k)==v for k,v in evidence.items()),'NER完整七欄reverse')
 need(m.get('kind')=='pronoun' or any(a.get('surface')==m['surface'] and m['id']in a.get('mention_ids',[])for a in person.get('aliases',[])),'NER alias/MID')

def roles(root,b,people,proposals=None):
 parent=core.fixed(root);need(H(core.path(root,b['core_proof_path']).read_bytes())==b['core_proof_sha256'],'原核心證照漂移')
 r=core.roles(root,parent,people)
 for s in b['external_roles']:
  c=read(root,s['native_path']);need(c['id']==s['chapter_id'] and all(c[k]==s[k]for k in ('work_id','book_id','source_id')) and c['source'].get('revision_id')==s['revision_id'],'NER外篇維度')
  p,=[p for p in c['paragraphs']if p['id']==s['paragraph_id']]
  need({k:v for k,v in p.items()if k!='mentions'}==s['paragraph'] and H(p['text'].encode())==s['paragraph_sha256'],'NER完整外篇段')
  m,=[m for m in p['mentions']if m['id']==s['mention_id']]
  need({k:m[k]for k in ('id','start','end','surface','kind')}==s['mention'] and p['text'][m['start']:m['end']]==m['surface'],'NER外篇字位')
  reverse(people[m['person_id']],c,p,m);need(s['role']not in r or r[s['role']]==m['person_id'],'NER同role不一致');r[s['role']]=m['person_id']
 own=read(root,core.CH)
 for s in b['local_roles']:
  p,=[p for p in own['paragraphs']if p['id']==s['paragraph_id']]
  need(H(p['text'].encode())==s['paragraph_sha256'],'NER來源內整段')
  hits=[m for m in p['mentions']if m['id']==s['mention_id']]
  if not hits and proposals is not None:
   need(s['role']in proposals,'首次配置缺role');r[s['role']]=proposals[s['role']];continue
  m,=hits;need({k:m[k]for k in ('id','start','end','surface','kind')}==s['mention'] and m['kind']=='person' and p['text'][m['start']:m['end']]==m['surface'],'NER來源內首MID')
  reverse(people[m['person_id']],own,p,m);r[s['role']]=m['person_id']
 for alias,target in b['role_aliases'].items():need(target in r,'NER alias role缺');r[alias]=r[target]
 for first,second in b['distinct_role_pairs']:need(r[first]!=r[second],'NER明親屬/四女來源角色不得合成同人')
 return r

@memoized(0)
def source_context(root):
 b=fixed(root);people={p['id']:p for p in read(root,'registry/persons.json')['persons']};r=roles(root,b,people)
 return b,r,{pid:people[pid]for pid in set(r.values())}

def prepared(ch,root):
 b,r,people=source_context(root);need(ch==read(root,core.CH)==expand(b['chapter_template'],r),'NER完整actual章/角色/詞句漂移')
 parent=core.fixed(root);raw=core.path(root,b['raw_path']).read_bytes();need(H(raw)==b['raw_sha256']==parent['raw_sha256'],'NER固定raw')
 t=raw.decode();need(t.count(b['opening_heading'])==t.count(b['following_heading'])==1 and t.index(b['opening_heading'])==b['selection_start'] and t.index(b['following_heading'])==b['selection_end'],'NER完整節界')
 for p in ch['paragraphs']:
  loc=p['source_position'];ix=loc['raw_character_offsets'];need(p['text']==''.join(t[i]for i in ix) and H((json.dumps(ix,ensure_ascii=False,indent=2)+'\n').encode())==loc['projection_sha256'] and p['text_layer']=='received_chapter' and loc['revision_id']==2479706,'NER原投影/層')
  for m in p['mentions']:
   need(p['text'][m['start']:m['end']]==m['surface'],'NER提及字位')
   if m['kind']in('person','pronoun'):reverse(people[m['person_id']],ch,p,m)
   else:need(m['kind']=='unresolved' and m['person_id']is None and m['status']=='unresolved','NER集體/未定不得造人')
 for oldp in expand(parent['chapter_template'],r)['paragraphs']:
  p,=[p for p in ch['paragraphs']if p['id']==oldp['id']]
  need(all(p[k]==oldp[k]for k in ('text','source_position','text_layer')),'核心原文/原位改動')
  for m in oldp['mentions']:need([x for x in p['mentions']if x['id']==m['id']]==[m],'核心5MID改動')
 need(ch['annotation']['modern_collation_reports']==parent['chapter_template']['annotation']['modern_collation_reports'] and ch['cross_chapter_references']==expand(parent['chapter_template'],r)['cross_chapter_references'],'兩Wiki ref/父傳互見改動')
 for n in ch['annotation']['modern_collation_reports']:need(t[n['raw_start']:n['raw_end']]==n['raw_text'] and n['human_reviewed']is False and n['image_verified']is False,'NER Wiki注資格')
 for rel,key in ((core.NS,'names_template'),(core.AD,'addresses_template'),(IP,'identities_template'),(NSN,'literal_names_template')):need(read(root,rel)==expand(b[key],r),'NER姓名/原籍/身份側車')
 for key,collection in (('father_assertion','assertions'),('father_name','records')):
  s=parent[key];want=expand(s['record'],r);need([x for x in read(root,s['native_path'])[collection]if x['id']==want['id']]==[want],'原核心父女/父全名證')
 if 'fixed_jin031_typed_ref'in ch['annotation']:
  try:from scripts.fixed_jin031_jia_typed import validate_documents
  except ImportError:from fixed_jin031_jia_typed import validate_documents
  validate_documents(root,r)
 return r,b

def guard_bundle(root,pid,people,records):
 has=any(e.get('chapter_id')==core.CID for e in people.get(pid,{}).get('evidence',[]))
 if pid not in source_index(root)['person_ids'] and not has:return
 b,r,actual=source_context(root)
 need(people.get(pid)==actual.get(pid),'NER caller人物metadata不完整');ch=read(root,core.CH);prepared(ch,root)
 need([c for c in records if c.get('id')==core.CID]==[ch],'NER caller缺完整031章')
 need([c for c in records if c.get('record_type')=='person_name_component_set'and c.get('chapter_id')==core.CID]==[read(root,core.NS),read(root,NSN)],'NER caller缺完整核心及literal/title姓名側車')
 for rel,typ in ((core.AD,'person_address_assertion_set'),(IP,'person_identity_decision_set')):
  need([c for c in records if c.get('record_type')==typ and c.get('chapter_id')==core.CID]==[read(root,rel)],'NER caller缺來源側車 '+typ)
 if 'fixed_jin031_typed_ref'in ch['annotation']:
  try:from scripts.fixed_jin031_jia_typed import proof as typed_proof
  except ImportError:from fixed_jin031_jia_typed import proof as typed_proof
  for rel,value in typed_proof(root)['expected_documents'].items():
   need([c for c in records if c.get('record_type')==value['record_type']and c.get('chapter_id')==core.CID]==[read(root,rel)],'typed caller缺完整031新側車')

@memoized(0)
def accepted_names(root):
 ch=read(root,core.CH)
 if active(root):
  r,b=prepared(ch,root)
  return expand(b['names_template'],r)['records']+expand(b['literal_names_template'],r)['records']
 r,b=core.prepared(ch,root)
 return expand(b['names_template'],r)['records']

def name_record_valid(name,root,all_names=None):
 try:
  expected=accepted_names(root)
  if all_names is not None:
   owned=[n for n in all_names if n.get('chapter_id')==core.CID or str(n.get('person_mention_id','')).startswith(core.CID+':')]
   need(len(owned)==len(expected) and len({n['id']for n in owned})==len(expected) and sorted(owned,key=lambda n:n['id'])==sorted(expected,key=lambda n:n['id']),'NER全catalog姓名槽缺失/多餘或重複')
  return name in expected
 except(ValueError,KeyError,TypeError,OSError,IndexError,StopIteration,AttributeError):return False
