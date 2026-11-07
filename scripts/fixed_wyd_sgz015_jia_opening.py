"""Exact WYD78-character received opening and complete WeiLue note; no ID allowlist."""
from pathlib import Path
import json,hashlib
CID='c-sanguozhi-015-wyd1739-jia-opening';SID='s-sanguozhi-015-wyd1739-jia-opening'
BASE='source-evidence/sgz015-wyd1739-jia-opening/'
CH='corpus/sanguozhi/015-wyd1739-jia-opening.json'
CONTRACT_SHA='cf5e8d8dfa59d14b77c01fcc40f95281e9c6495eb077fcc500871ae4f31bbb3e'
SURNAME_KIND='contextual_surname_from_wyd_sgz015_named_grandfather'
def need(x,msg):
 if not x:raise ValueError('武英殿魏015傳首：'+msg)
def read(root,rel):
 root=Path(root).resolve();p=(root/rel).resolve();need(p.is_relative_to(root),'path escape');return json.loads(p.read_bytes())
def sub(x,roles):
 if isinstance(x,str) and x.startswith('$'):return roles[x[1:]]
 if isinstance(x,dict):return{k:sub(v,roles) for k,v in x.items()}
 if isinstance(x,list):return[sub(v,roles) for v in x]
 return x
def contract(root):
 b=(Path(root)/(BASE+'native-contract.json')).read_bytes();need(hashlib.sha256(b).hexdigest()==CONTRACT_SHA,'contract SHA');return json.loads(b)
def seed_role(root,c,people):
 s=c['seed'];ch=read(root,s['path']);need(all(ch[k]==v for k,v in s['dimensions'].items()),'seed chapter/source')
 p,=[p for p in ch['paragraphs'] if p['id']==s['paragraph_id']];need(p['text']==s['text'] and p['text_layer']==s['text_layer'],'seed full paragraph/layer')
 need(ch['source']['revision_id']==s['source_revision'] and ch['source']['raw_sha256']==s['source_raw_sha256'],'seed version')
 m,=[m for m in p['mentions'] if m['id']==s['mention_id']];need((m.get('kind'),m['surface'],m['start'],m['end'])==('person',s['surface'],s['start'],s['end']),'seed role')
 pid=m['person_id'];need(pid in people,'seed unknown PID');person=people[pid]
 need(any(a.get('surface')==m['surface'] and m['id'] in a.get('mention_ids',[]) for a in person.get('aliases',[])),'seed alias reverse')
 evidence={k:ch[k] for k in ('work_id','book_id','source_id')};evidence.update(chapter_id=ch['id'],paragraph_id=p['id'],mention_id=m['id'],quote=m['surface'])
 need(evidence in person.get('evidence',[]),'seed evidence reverse')
 return pid

def state(root,ch=None,people=None,records=None):
 c=contract(root);people_actual=read(root,'registry/persons.json')['persons'];by={p['id']:p for p in people_actual};need(len(by)==len(people_actual),'duplicate registry')
 if people is not None:need(people==by,'supplied current people differ')
 if ch is None:ch=read(root,CH)
 need(isinstance(ch,dict),'chapter type');ms={m['id']:m for p in ch.get('paragraphs',[]) for m in p.get('mentions',[])}
 roles={'kui':seed_role(root,c,by)}
 for role,mid in c['new_roles'].items():
  m=ms.get(mid,{});need(m.get('kind')=='person' and m.get('person_id') in by,'new source actor');roles[role]=m['person_id']
 need(len(set(roles.values()))==3,'source actors must differ')
 need(ch==sub(c['chapter_template'],roles),'complete selected text/layers/markers/metadata/AI qualification')
 raw=(Path(root)/(BASE+'transcription-runs.txt')).read_bytes();need(hashlib.sha256(raw).hexdigest()==c['raw_sha256'],'AI transcript raw SHA')
 need(read(root,BASE+'transcription-projection.json')==c['projections'] and read(root,BASE+'image-run-locations.json')==c['locations'],'projection/physical source runs')
 try:from scripts.witness_projection import repository_positions
 except ImportError:from witness_projection import repository_positions
 lines=raw.decode().splitlines();points=[]
 for p in ch['paragraphs']:
  pts,digest=repository_positions(root,p,lines);need(digest==c['raw_sha256'],'projection raw hash');points.extend(pts)
 need(points==[(i,j)for i,t in enumerate(lines,1) for j in range(len(t))],'all78 characters exactly once')
 for key,template in c['sidecar_templates'].items():
  rel=CH.removesuffix('.json')+'-'+key+'.json';need(read(root,rel)==sub(template,roles),'sidecar '+key)
 wanted={pid:[] for pid in roles.values()};links={pid:[] for pid in roles.values()}
 for p in ch['paragraphs']:
  for m in p['mentions']:
   if m['kind']not in('person','pronoun'):continue
   need(p['text'][m['start']:m['end']]==m['surface'],'source anchor')
   pid=m['person_id'];e={k:ch[k] for k in ('work_id','book_id','source_id')};e.update(chapter_id=CID,paragraph_id=p['id'],mention_id=m['id'],quote=m['surface']);wanted[pid].append(e)
   if m['kind']=='person':links[pid].append((m['surface'],m['id']))
 for pid,expected in wanted.items():
  actual=[e for e in by[pid].get('evidence',[]) if e.get('chapter_id')==CID];need(sorted(actual,key=lambda e:e['mention_id'])==sorted(expected,key=lambda e:e['mention_id']),'full reverse source evidence')
  actual_links=[(a['surface'],mid)for a in by[pid].get('aliases',[]) for mid in a.get('mention_ids',[]) if mid.startswith(CID+':')];need(sorted(actual_links)==sorted(links[pid]),'full source aliases')
 if records is not None:need(sum(r==ch for r in records if r.get('id')==CID)==1,'catalog exact source once')
 return {'contract':c,'chapter':ch,'roles':roles,'people':by}
def source_errors(ch,root):
 if not isinstance(ch,dict):return []
 a=ch.get('annotation',{});b=a.get('fixed_transcription_contract') if isinstance(a,dict) else None
 if ch.get('id')!=CID and ch.get('source_id')!=SID and b!='wyd_sgz015_jia_opening':return []
 try:state(root,ch);return []
 except(ValueError,KeyError,TypeError,StopIteration,OSError,IndexError,UnicodeError)as e:return [str(e)]
def guard_bundle(root,pid,people,records):
 ch=next((r for r in records if r.get('record_type')=='marked_chapter' and r.get('id')==CID),None)
 if ch is None:return
 ids={m.get('person_id')for p in ch['paragraphs']for m in p['mentions']if m.get('kind')=='person'}
 if pid in ids:state(root,ch,people,records)
def validate_surname(name,names,chapters,assertions,root):
 need(CID in chapters,'missing supplied source chapter')
 st=state(root,chapters[CID]);c=st['contract'];expected=sub(c['sidecar_templates']['names']['records'][2],st['roles']);need(name==expected,'grandfather surname record')
 for n in sub(c['sidecar_templates']['names']['records'][:2],st['roles']):
  hits=[x for x in names if isinstance(x,dict) and x.get('id')==n['id']];need(len(hits)==1 and hits[0]==n,'literal seed/component exact unique')
 f=sub(c['sidecar_templates']['assertions']['assertions'][0],st['roles']);hits=[x for x in assertions if isinstance(x,dict) and x.get('id')==f['id']];need(len(hits)==1 and hits[0]==f,'same-source direct grandfather no fake father')
 return None

# Named full-unit transcription extension. The78 parent remains exact evidence.
import copy as _copy
import math as _math
FULL_BASE='source-evidence/sgz015-wyd1739-jia-full/'
FULL_CASE=FULL_BASE+'full-phase-contract.json'
FULL_SHA='fe6c5b92a28b3a53526a916faa81f4a8b2b8b97d9ee2e4fbd1b4ea626f18962f'
FULL_PHASE='wyd_sgz015_jia_full_pending_source_extension'
def _full_present(root):return(Path(root)/FULL_CASE).is_file()
def _full_case(root):
 b=(Path(root)/FULL_CASE).read_bytes();need(hashlib.sha256(b).hexdigest()==FULL_SHA,'full-phase contract SHA');c=json.loads(b)
 need(c.get('kind')==FULL_PHASE and c.get('human_reviewed')is False and c.get('image_verified')is False and c.get('model')is None,'full-phase qualification')
 return c
def _full_same(a,b):
 if type(a)is not type(b):return False
 if type(a)is dict:return all(type(k)is str for k in a)and a.keys()==b.keys()and all(_full_same(a[k],b[k])for k in a)
 if type(a)is list:return len(a)==len(b)and all(_full_same(x,y)for x,y in zip(a,b))
 if type(a)is float:return _math.isfinite(a)and _math.isfinite(b)and a==b
 return type(a)in(str,int,bool,type(None))and a==b
def _full_witness_valid(root,incoming,full):
 raw=(Path(root)/(FULL_BASE+'transcription-runs.txt')).read_bytes();need(hashlib.sha256(raw).hexdigest()==full['raw_sha256'],'full transcript raw SHA')
 need(_full_same(read(root,FULL_BASE+'transcription-projection.json'),full['projections']),'full raw projection mismatch')
 need(_full_same(read(root,FULL_BASE+'image-run-locations.json'),full['locations']),'full physical locations mismatch')
 need(_full_same(read(root,FULL_BASE+'editorial-readings.json'),full['unknown_doc']),'full unknown readings mismatch')
 try:from scripts.witness_projection import repository_positions
 except ImportError:from witness_projection import repository_positions
 lines=raw.decode().splitlines();points=[]
 for i,p in enumerate(incoming['paragraphs']):
  pts,digest=repository_positions(root,p,lines);need(digest==full['raw_sha256'],'full paragraph hash');points.extend(pts)
 need(points==[(i,j)for i,t in enumerate(lines,1)for j in range(len(t))]and sum(map(len,lines))==3980,'full3980 characters exactly once, no omitted/supplemented text')
 need(hashlib.sha256('\n\n'.join(p['text']for p in incoming['paragraphs']).encode()).hexdigest()==incoming['text_sha256'],'full text hash')
 ps={p['id']:p for p in incoming['paragraphs']};unknown=full['unknown_doc']['readings'];need(len(unknown)==8,'full eight unknowns')
 for u in unknown:
  p=ps[u['paragraph_id']];need(u['accepted']is None and u['editorial_placeholder']is True and u['original_printed_character_claimed']is False and p['text'][u['start']:u['end']]=='〓'and lines[u['raw_line']-1][u['raw_column']]=='〓','unknown point/qualification mismatch')
 need(sum(p['text'].count('〓')for p in incoming['paragraphs'])==8,'unlisted/missing editorial placeholder')
_opening78_state=state
def state(root,ch=None,people=None,records=None):
 if not _full_present(root):return _opening78_state(root,ch,people,records)
 full=_full_case(root);parent=contract(root)
 for rel,digest in full['parent_fixed_files_sha256'].items():need(hashlib.sha256((Path(root)/rel).read_bytes()).hexdigest()==digest,'78父證不可改')
 incoming=read(root,CH)if ch is None else ch;need(type(incoming)is dict and type(incoming.get('paragraphs'))is list and len(incoming['paragraphs'])>2,'full incoming chapter required')
 # Only the two original paragraphs are projected for the immutable78 owner.
 # Acceptance still requires exact equality of the entire new chapter below.
 view=_copy.deepcopy(incoming);view['source']=_copy.deepcopy(parent['chapter_template']['source']);view['annotation']=_copy.deepcopy(parent['chapter_template']['annotation']);view['text_sha256']=parent['chapter_template']['text_sha256'];view['paragraphs']=_copy.deepcopy(incoming['paragraphs'][:2])
 for p,old in zip(view['paragraphs'],parent['chapter_template']['paragraphs']):p['source_position']=_copy.deepcopy(old['source_position'])
 st=_opening78_state(root,view,people,None);roles=st['roles'];expected=sub(full['chapter_template'],roles)
 need(_full_same(incoming,expected),'full chapter text/pending/old markers/source metadata mismatch')
 if people is not None:need(_full_same(people,st['people']),'full current registry differs')
 _full_witness_valid(root,incoming,full)
 for p in incoming['paragraphs'][2:]:need(p.get('annotation_status')=='pending'and p.get('mentions')==[],'new paragraphs must remain pending without fake NER')
 if records is not None:
  docs=[incoming]+[read(root,CH.removesuffix('.json')+'-'+key+'.json')for key in parent['sidecar_templates']]
  related=[r for r in records if r.get('id')==CID or r.get('chapter_id')==CID]
  need(len(related)==len(docs)and all(sum(_full_same(d,r)for r in related)==1 for d in docs),'full catalog needs one actual chapter and all four exact sidecars, no other same-source additions')
 return dict(st,chapter=incoming,full_contract=full)
try:from scripts.validation_context import memoized as _full_memoized
except ImportError:from validation_context import memoized as _full_memoized
@_full_memoized(0)
def _full_relevant_person_ids(root):
 # Bounded relevance only; caller-specific people/catalog proofs stay uncached.
 ids={p['id']for p in read(root,'registry/persons.json')['persons']if any(e.get('chapter_id')==CID for e in p.get('evidence',[]))}
 path=Path(root)/CH
 if path.is_file():
  ch=read(root,CH)
  ids.update(m.get('person_id')for p in ch.get('paragraphs',[])for m in p.get('mentions',[])if m.get('kind')=='person')
 return sorted(x for x in ids if isinstance(x,str))
_opening78_guard_bundle=guard_bundle
def guard_bundle(root,pid,people,records):
 if not _full_present(root)and not _ner_present(root):return _opening78_guard_bundle(root,pid,people,records)
 if pid not in _full_relevant_person_ids(root):return
 chs=[r for r in records if r.get('record_type')=='marked_chapter'and r.get('id')==CID];need(len(chs)==1,'full catalog missing/repeated actual chapter')
 return state(root,chs[0],people,records)

# Named full NER phase: real chapter/registry closure precedes parent witness subset.
NER_BASE='source-evidence/sgz015-wyd1739-jia-full-ner/'
NER_CASE=NER_BASE+'ner-contract.json'
NER_SHA='3adbbc29215bab6e9715a6143817d9e707b678096f24628934bdebf492fd14f8'
def _ner_present(root):return(Path(root)/NER_CASE).is_file()
def _ner_case(root):
 b=(Path(root)/NER_CASE).read_bytes();need(hashlib.sha256(b).hexdigest()==NER_SHA,'full NER contract SHA');c=json.loads(b)
 need(c.get('kind')=='wyd_sgz015_jia_full_named_mentions_first_pass'and c.get('human_reviewed')is False and c.get('image_verified')is False and c.get('model')is None,'NER source qualification')
 return c
def _ner_seed_qualification(ch,s):
 need(all(_full_same(ch['source'].get(k),v)for k,v in s['source_qualification_fields'].items()),'NER known seed source qualification')
 need(all(_full_same(ch.get('annotation',{}).get(k),v)for k,v in s['annotation_qualification_fields'].items()),'NER known seed AI/human qualification')
def _ner_known_pid(root,s,by):
 ch=read(root,s['path']);_ner_seed_qualification(ch,s);need(all(ch.get(k)==v for k,v in s['dimensions'].items()),'NER known seed source dimensions')
 p,=[p for p in ch['paragraphs']if p['id']==s['paragraph_id']];need(p['text']==s['text']and p['text_layer']==s['text_layer'],'NER known seed complete paragraph/layer')
 need(ch['source']['revision_id']==s['source_revision'],'NER known seed version')
 field=s.get('source_hash_field','raw_sha256')
 if field is not None:need(ch['source'].get(field)==s['source_raw_sha256'],'NER known seed observed hash field')
 m,=[m for m in p['mentions']if m['id']==s['mention_id']];need((m.get('kind'),m.get('surface'),m.get('start'),m.get('end'))==('person',s['surface'],s['start'],s['end']),'NER known source MID/span')
 pid=m.get('person_id');need(pid in by,'NER known seed current person');e={k:ch[k]for k in('work_id','book_id','source_id')};e.update(chapter_id=ch['id'],paragraph_id=p['id'],mention_id=m['id'],quote=m['surface'])
 need(e in by[pid].get('evidence',[])and any(a.get('surface')==m['surface']and m['id']in a.get('mention_ids',[])for a in by[pid].get('aliases',[])),'NER known seed real reverse/alias')
 return pid
@_full_memoized(0)
def _ner_known_models(root):
 # One scoped parse per distinct source; return bounded role proof, not people/catalog.
 c=_ner_case(root);docs={};out={}
 for role,seed in c['known_seeds'].items():
  if seed['path']not in docs:docs[seed['path']]=read(root,seed['path'])
  ch=docs[seed['path']];_ner_seed_qualification(ch,seed);need(all(ch.get(k)==v for k,v in seed['dimensions'].items()),'NER seed model source')
  p,=[p for p in ch['paragraphs']if p['id']==seed['paragraph_id']];need(p['text']==seed['text']and p['text_layer']==seed['text_layer'],'NER seed model full paragraph')
  need(ch['source']['revision_id']==seed['source_revision'],'NER seed model revision');field=seed.get('source_hash_field','raw_sha256')
  if field is not None:need(ch['source'].get(field)==seed['source_raw_sha256'],'NER seed model hash field')
  m,=[m for m in p['mentions']if m['id']==seed['mention_id']];need((m.get('kind'),m.get('surface'),m.get('start'),m.get('end'))==('person',seed['surface'],seed['start'],seed['end']),'NER seed model MID')
  e={k:ch[k]for k in('work_id','book_id','source_id')};e.update(chapter_id=ch['id'],paragraph_id=p['id'],mention_id=m['id'],quote=m['surface']);out[role]={'person_id':m['person_id'],'evidence':e,'source_record_digest':hashlib.sha256(json.dumps(ch,ensure_ascii=False,sort_keys=True,allow_nan=False).encode()).hexdigest()}
 return out
def _ner_literal_names_valid(ch,rows):
 ps={p['id']:p for p in ch['paragraphs']}
 for r in rows:
  p=ps.get(r.get('paragraph_id'));need(p is not None and r.get('quote')==p['text'],'NER literal name complete source paragraph')
  a=r.get('source_anchor',{});start=a.get('start');end=a.get('end');surface=a.get('surface');need(type(start)is int and type(end)is int and 0<=start<end<=len(p['text'])and p['text'][start:end]==surface,'NER literal name actual codepoint slice')
  value=(r.get('surname')or'')+(r.get('ming')or'');need(type(surface)is str and surface==value,'NER literal name components source slice')
  ms=[m for m in p['mentions']if m['id']==r.get('person_mention_id')];need(len(ms)==1,'NER literal name real MID');m=ms[0];need(m.get('kind')=='person'and m.get('person_id')==r.get('person_id')and m['start']<=start<end<=m['end'],'NER literal name owner/MID bounds')
def _ner_identity_rows_valid(ch,c,rows,roles):
 need(len(rows)==len(roles),'NER identity decision role count');ps={p['id']:p for p in ch['paragraphs']};ms={m['id']:(p,m)for p in ch['paragraphs']for m in p['mentions']};inverse={v:k for k,v in roles.items()}
 for d in rows:
  role=inverse.get(d.get('person_id'));need(role is not None,'NER identity current role');mid=c['source_role_first_mentions'][role];p,m=ms[mid];need(m.get('person_id')==d['person_id'],'NER identity source owner')
  own={k:ch[k]for k in('work_id','book_id','source_id')};own.update(chapter_id=ch['id'],paragraph_id=p['id'],mention_id=mid,quote=p['text']);expected=[own]
  if role in c['known_seeds']:
   seed=c['known_seeds'][role];e={k:seed['dimensions'][k]for k in('work_id','book_id','source_id')};e.update(chapter_id=seed['dimensions']['id'],paragraph_id=seed['paragraph_id'],mention_id=seed['mention_id'],quote=seed['text']);expected.append(e)
  allowed=[x['chapter_id']for x in expected];need(d.get('scope')==('same_chapter'if len(allowed)==1 else'cross_chapter')and set(d.get('chapter_ids',[]))==set(allowed)and len(d['chapter_ids'])==len(allowed),'NER identity standard scope/chapter closure')
  need(_full_same(d.get('evidence'),expected),'NER identity complete actual source evidence')
_pending_full_state=state
def state(root,ch=None,people=None,records=None):
 if not _ner_present(root):return _pending_full_state(root,ch,people,records)
 c=_ner_case(root)
 for rel,digest in c['supporting_reference_files'].items():need(hashlib.sha256((Path(root)/rel).read_bytes()).hexdigest()==digest,'NER fixed comparison evidence')
 rows=read(root,'registry/persons.json')['persons'];by={p['id']:p for p in rows};need(len(by)==len(rows),'NER duplicate registry')
 if people is not None:need(_full_same(people,by),'NER incoming registry differs')
 incoming=read(root,CH)if ch is None else ch;need(type(incoming)is dict,'NER actual chapter')
 ms={m['id']:m for p in incoming.get('paragraphs',[])for m in p.get('mentions',[])};roles={};models=_ner_known_models(root)
 for role,mid in c['source_role_first_mentions'].items():
  m=ms.get(mid,{});need(m.get('kind')=='person'and m.get('person_id')in by,'NER source role missing');roles[role]=m['person_id']
  if role in models:
   model=models[role];e=model['evidence'];need(roles[role]==model['person_id']and e in by[roles[role]].get('evidence',[])and any(a.get('surface')==e['quote']and e['mention_id']in a.get('mention_ids',[])for a in by[roles[role]].get('aliases',[])),'NER wrong known keeper/reverse/alias')
 need(len(roles)==c['person_roles']and len(set(roles.values()))==len(roles),'NER role collision')
 need(_full_same(incoming,sub(c['chapter_template'],roles)),'NER complete chapter/markers/voices/qualifications')
 full=_full_case(root);need(FULL_SHA==c['parent_full_contract_sha256']and CONTRACT_SHA==c['parent_original_contract_sha256'],'NER exact named source parents')
 for rel,digest in full['parent_fixed_files_sha256'].items():need(hashlib.sha256((Path(root)/rel).read_bytes()).hexdigest()==digest,'NER 78 parent fixed evidence')
 _full_witness_valid(root,incoming,full)
 # Only after whole new chapter proof, check the preserved witness subset.
 parent=sub(c['parent_two_paragraphs'],roles)
 for i,(a,b)in enumerate(zip(incoming['paragraphs'][:2],parent)):
  need(_full_same({k:v for k,v in a.items()if k!='mentions'},{k:v for k,v in b.items()if k!='mentions'}),'NER original paragraph text/position/metadata')
  actual={m['id']:m for m in a['mentions']};need(set(actual)=={m['id']for m in b['mentions']},'NER original11 MID set')
  for old in b['mentions']:
   now=actual[old['id']]
   if old.get('surface')=='妻':need(all(now[k]==old[k]for k in('id','start','end','surface'))and now['kind']=='person'and now['person_id']==roles['jia_kui_wife'],'NER named wife promotion only')
   else:need(_full_same(now,old),'NER original marker changed')
 docs=[incoming]
 for group in('parent_sidecars','sidecar_templates'):
  for rel,template in c[group].items():
   actual=read(root,rel);need(_full_same(actual,sub(template,roles)),'NER exact '+rel);docs.append(actual)
   if group=='sidecar_templates'and actual.get('record_type')=='person_name_component_set':_ner_literal_names_valid(incoming,actual['records'])
   if group=='sidecar_templates'and actual.get('record_type')=='person_identity_decision_set':_ner_identity_rows_valid(incoming,c,actual['decisions'],roles)
 # Every current endpoint and alias in this source is closed, including stray reverse-only people.
 wanted={pid:[]for pid in roles.values()};links={pid:[]for pid in roles.values()}
 for p in incoming['paragraphs']:
  for m in p['mentions']:
   if m['kind']not in('person','pronoun'):continue
   e={k:incoming[k]for k in('work_id','book_id','source_id')};e.update(chapter_id=CID,paragraph_id=p['id'],mention_id=m['id'],quote=m['surface']);wanted[m['person_id']].append(e)
   if m['kind']=='person':links[m['person_id']].append((m['surface'],m['id']))
 for person in rows:
  pid=person['id'];actual=[e for e in person.get('evidence',[])if e.get('chapter_id')==CID];als=[(a['surface'],mid)for a in person.get('aliases',[])for mid in a.get('mention_ids',[])if mid.startswith(CID+':')]
  need(sorted(actual,key=lambda e:e['mention_id'])==sorted(wanted.get(pid,[]),key=lambda e:e['mention_id']),'NER full seven-field source reverse')
  need(sorted(als)==sorted(links.get(pid,[])),'NER full source aliases')
 for role,meta in c['new_role_metadata'].items():
  person=by[roles[role]];need(all(person.get(k)==v for k,v in meta.items()),'NER source-local actor qualification')
 if records is not None:
  related=[r for r in records if r.get('id')==CID or r.get('chapter_id')==CID]
  need(len(related)==len(docs)and all(sum(_full_same(d,r)for r in related)==1 for d in docs),'NER full actual catalog missing/extra/changed own-source record')
  for role,model in models.items():
   hits=[r for r in records if r.get('id')==c['known_seeds'][role]['dimensions']['id']];need(len(hits)==1 and hashlib.sha256(json.dumps(hits[0],ensure_ascii=False,sort_keys=True,allow_nan=False).encode()).hexdigest()==model['source_record_digest'],'NER caller known source absent/different')
 return {'contract':contract(root),'chapter':incoming,'roles':{'kui':roles['jia_kui'],'xi':roles['jia_xi'],'liufu':roles['wife_brother_liufu']},'ner_roles':roles,'ner_contract':c,'full_contract':full,'people':by}

_ner_previous_source_errors=source_errors
def source_errors(ch,root):
 if not _ner_present(root)or not isinstance(ch,dict)or ch.get('id')!=CID:return _ner_previous_source_errors(ch,root)
 try:
  try:from scripts.person_bundle import load_catalog
  except ImportError:from person_bundle import load_catalog
  people,records=load_catalog(Path(root));state(root,ch,people,records);return []
 except(ValueError,KeyError,TypeError,StopIteration,OSError,IndexError,UnicodeError)as e:return [str(e)]

# Named, source-owned editorial surname continuation; immutable full-NER parent retained.
from contextvars import ContextVar as _CaoContextVar
_CAO_CASE='source-evidence/sgz015-wyd1739-caozhang-surname/continuation.json'
_CAO_SHA='038b08d0195edfeb30e5b59348bc0758e7c9c0e4fd7f11d1c86c33b5ab6bae59'
_CAO_KIND='contextual_surname_from_wyd_sgz015_reference_parent_fullname'
_cao_original_read=read
_cao_view=_CaoContextVar('sgz015_caozhang_parent_witness_view',default=None)
def read(root,rel):
 view=_cao_view.get()
 if view is not None and Path(root).resolve()==view[0]and rel in view[1]:return _copy.deepcopy(view[1][rel])
 return _cao_original_read(root,rel)
def _cao_case(root):
 b=(Path(root)/_CAO_CASE).read_bytes();need(hashlib.sha256(b).hexdigest()==_CAO_SHA,'曹彰 continuation exact SHA');c=json.loads(b)
 need(c.get('kind')=='wyd_sgz015_caozhang_reference_surname_continuation'and c.get('human_reviewed')is False and c.get('image_verified')is False and c.get('model')is None,'曹彰 continuation qualification')
 need(c['parent_ner_contract_sha256']==NER_SHA,'曹彰 immutable NER parent')
 return c
def _cao_reference_valid(r):
 need(r.get('kind')=='fixed_received_reference_comparison_not_native_chapter'and r.get('revision_id')==2347417 and r.get('source_role')=='unknown_print_comparison'and r.get('edition')is None,'曹彰 reference version/edition')
 need(r.get('human_reviewed')is False and r.get('image_verified')is False and r.get('model')is None and r.get('raw_bytes_acquired')is False and r.get('html_acquired')is False and r.get('modern_h2_excluded')is True,'曹彰 reference acquisition boundary')
 need(r.get('work_id')=='w-sanguozhi'and r.get('book_id')=='b-sanguozhi-019'and r.get('composition')is None and r.get('earliest_extant_edition')is None,'曹彰 reference not new base/dated work')
 us=r.get('units');need(type(us)is list and len(us)==3 and [u.get('locator')for u in us]==['L134','L135','L136']and all(type(u.get('text'))is str for u in us),'曹彰 complete three reference units')
 a,b,d=[u['text']for u in us];need(sum(map(len,(a,b,d)))==1230 and a.startswith('任城威王彰，字子文。'),'曹彰 received body, not modern h2')
 need('太祖嘗問諸子所好，使各言其志。彰曰：'in a and '建安二十一年，封鄢陵侯。'in a,'曹彰 title and sons context')
 need('臨發，太祖戒彰曰：『居家為父子，受事為君臣，動以王法從事，爾其戒之！』'in b,'曹彰 reference explicit father/son speech')
 need(d.startswith('太祖東還，以彰行越騎將軍，留長安。太祖至洛陽，得疾，驛召彰，未至，太祖崩。')and '文帝即王位，彰與諸侯就國。'in d,'曹彰 same office/Chang-an/death-succession episode')
def _cao_reverse(ch,p,m,by):
 pid=m.get('person_id');need(pid in by,'曹彰 source actor current registry');e={k:ch[k]for k in('work_id','book_id','source_id')};e.update(chapter_id=ch['id'],paragraph_id=p['id'],mention_id=m['id'],quote=m['surface'])
 need(sum(x==e for x in by[pid].get('evidence',[]))==1 and sum(a.get('surface')==m['surface']and m['id']in a.get('mention_ids',[])for a in by[pid].get('aliases',[]))==1,'曹彰 source seven-field reverse/alias')
def _cao_actual_proof(root,ch=None,people=None,records=None):
 c=_cao_case(root);reg=_cao_original_read(root,'registry/persons.json');by={p['id']:p for p in reg['persons']};need(len(by)==len(reg['persons']),'曹彰 registry duplicate')
 if people is not None:need(_full_same(people,by),'曹彰 actual caller registry differs')
 actual=_cao_original_read(root,CH)if ch is None else ch;need(actual.get('id')==CID and actual.get('source_id')==SID,'曹彰 actual source chapter')
 ps={p['id']:p for p in actual['paragraphs']};ms={m['id']:(p,m)for p in actual['paragraphs']for m in p['mentions']};child=ms[c['native_child_anchors'][0]['id']][1].get('person_id');father=ms[c['native_father_anchors'][0]['id']][1].get('person_id');roles={'child':child,'father':father};need(child!=father and child in by and father in by,'曹彰 distinct current child/parent roles')
 for anchors in('native_child_anchors','native_father_anchors'):
  for want in sub(c[anchors],roles):
   p,m=ms[want['id']];need(_full_same(m,want)and p['text'][m['start']:m['end']]==m['surface'],'曹彰 native role MID/position');_cao_reverse(actual,p,m,by)
 literal=sub(c['literal_name_template'],roles);_ner_literal_names_valid(actual,[literal]);need(literal['surname']is None and literal['ming']=='彰'and literal['source_anchor']=={'start':4,'end':5,'surface':'彰'}and literal['paragraph_id'].endswith(':p015'),'曹彰 literal name boundary')
 p15=ps[literal['paragraph_id']];need(p15['text'].startswith('時鄢陵侯彰行越騎將軍從長安來赴')and '文帝即王位'in p15['text'],'曹彰 source same-event bridge')
 doc=_cao_original_read(root,c['names_path']);hits=[n for n in doc['records']if n.get('id')==literal['id']];expected=sub(c['editorial_name_template'],roles);need(len(hits)==1 and _full_same(hits[0],expected),'曹彰 exact editorial name shape')
 name=hits[0];need(name['surname']=='曹'and name['ming']=='彰'and name['status']=='contextual_provisional'and name['surname_basis']['kind']==_CAO_KIND and name['surname_basis']['literal_source_components']=={'surname':None,'ming':'彰'},'曹彰 literal/editorial components separate')
 for k in('id','person_id','ming','source_anchor','person_mention_id','paragraph_id','chapter_id','quote','title'):need(_full_same(name[k],literal[k]),'曹彰 original name identity/position/title retained')
 person=by[child];need(all(_full_same(person.get(k),v)for k,v in c['actor_metadata_after'].items()),'曹彰 current display metadata');need(not any(a.get('surface')=='曹彰'for a in person.get('aliases',[])),'曹彰 restored full form is not raw alias')
 seed=c['parent_name_seed'];sc=_cao_original_read(root,seed['chapter_path']);need(all(sc.get(k)==v for k,v in seed['dimensions'].items()),'曹彰 parent seed actual dimensions')
 need(all(_full_same(sc['source'].get(k),v)for k,v in seed['source_qualification'].items())and all(_full_same(sc.get('annotation',{}).get(k),v)for k,v in seed['annotation_qualification'].items()),'曹彰 parent seed source/AI qualification')
 need(hashlib.sha256('\n\n'.join(p['text']for p in sc['paragraphs']).encode()).hexdigest()==seed['chapter_text_sha256'],'曹彰 parent source whole text')
 sp,=[p for p in sc['paragraphs']if p['id']==seed['paragraph']['id']];need(all(_full_same(sp.get(k),v)for k,v in seed['paragraph'].items()),'曹彰 parent full paragraph')
 sm,=[m for m in sp['mentions']if m['id']==seed['marker']['id']];need(_full_same(sm,sub(seed['marker'],roles))and sm['surface']=='曹操'and sp['text'][sm['start']:sm['end']]=='曹操'and sm['person_id']==father,'曹彰 parent full-name actor/slice');_cao_reverse(sc,sp,sm,by)
 sd=_cao_original_read(root,seed['path']);ss=[n for n in sd['records']if n.get('id')==seed['record']['id']];sn=sub(seed['record'],roles);need(sd.get('chapter_id')==sc['id']and len(ss)==1 and _full_same(ss[0],sn)and sn['surname']=='曹'and sn['ming']=='操'and sn['person_id']==father,'曹彰 existing literal parent-name record')
 need(name['surname_basis']['father_name_record_id']==sn['id']and name['surname_basis']['father_name_source_mention_id']==sm['id'],'曹彰 surname basis actual source seed')
 rb=(Path(root)/c['reference_path']).read_bytes();need(hashlib.sha256(rb).hexdigest()==c['reference_sha256'],'曹彰 exact complete reference bytes');ref=json.loads(rb);_cao_reference_valid(ref)
 if records is not None:
  need(sum(_full_same(r,sc)for r in records)==1 and sum(_full_same(r,sd)for r in records)==1,'曹彰 caller complete parent-source/name record closure')
 return c,reg,by,actual,doc,roles,literal
_cao_previous_state=state
def state(root,ch=None,people=None,records=None):
 if not _ner_present(root):return _cao_previous_state(root,ch,people,records)
 need((Path(root)/_CAO_CASE).is_file(),'曹彰 required named continuation missing')
 c,reg,by,actual,doc,roles,literal=_cao_actual_proof(root,ch,people,records);child=roles['child']
 # Only the already-proved new row/display fields receive a parent-phase witness view.
 preg=dict(reg);preg['persons']=[dict(p,**c['actor_metadata_before'])if p['id']==child else p for p in reg['persons']];pby={p['id']:p for p in preg['persons']};pdoc=dict(doc);pdoc['records']=[literal if n.get('id')==literal['id']else n for n in doc['records']]
 precords=None if records is None else[pdoc if r.get('record_type')=='person_name_component_set'and r.get('chapter_id')==CID and any(n.get('id')==literal['id']for n in r.get('records',[]))else r for r in records]
 token=_cao_view.set((Path(root).resolve(),{'registry/persons.json':preg,c['names_path']:pdoc}))
 try:st=_cao_previous_state(root,actual,pby if people is not None else None,precords)
 finally:_cao_view.reset(token)
 st['people']=by;st['editorial_surname_continuation']={'case':c,'roles':roles,'literal_name':literal,'current_name':sub(c['editorial_name_template'],roles)};return st
_cao_previous_validate_surname=validate_surname
def validate_surname(name,names,chapters,assertions,root):
 if name.get('surname_basis',{}).get('kind')!=_CAO_KIND:return _cao_previous_validate_surname(name,names,chapters,assertions,root)
 need(CID in chapters,'曹彰 supplied chapter missing');st=state(root,chapters[CID]);d=st['editorial_surname_continuation'];c=d['case'];need(_full_same(name,d['current_name']),'曹彰 supplied editorial name differs')
 need(sum(_full_same(n,name)for n in names if isinstance(n,dict))==1,'曹彰 caller editorial row missing/duplicate')
 seed=c['parent_name_seed'];sn=sub(seed['record'],d['roles']);need(sum(_full_same(n,sn)for n in names if isinstance(n,dict))==1,'曹彰 caller literal Cao Cao record missing/duplicate');need(seed['dimensions']['id']in chapters and _full_same(chapters[seed['dimensions']['id']],_cao_original_read(root,seed['chapter_path'])),'曹彰 caller parent source missing/changed')
 return None
def caozhang_test_inputs(root):
 c=_cao_case(root);return[_CAO_CASE,c['reference_path'],c['parent_name_seed']['path'],c['parent_name_seed']['chapter_path']]
def caozhang_catalog_support(root):
 c=_cao_case(root);return[_cao_original_read(root,c['parent_name_seed']['path']),_cao_original_read(root,c['parent_name_seed']['chapter_path'])]
