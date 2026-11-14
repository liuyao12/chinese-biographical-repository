"""Finite exact Songshu 51 p014–p017 family annotation batch, layered over preserved earlier phase guards."""
from pathlib import Path
import json,copy,hashlib
try:from scripts.validation_context import memoized
except ImportError:from validation_context import memoized
CH='corpus/songshu/051-wyd1739.json';CID='c-songshu-051-wyd1739-zongshi';REF='source-evidence/song051-wyd1739-zongshi/yixin-complete-unit-contract.json';PHASE='song051_p014_p017_family_annotation_batch';CONTRACT_SHA='9c18fa21c212cd703e4dd9b52be3283802f62942a0439c54571547f480e215bb'
def same(a,b):
 if type(a)is not type(b):return False
 if type(a)is dict:return all(type(k)is str for k in a)and all(type(k)is str for k in b)and set(a)==set(b)and all(same(a[k],b[k])for k in a)
 if type(a)is list:return len(a)==len(b)and all(same(x,y)for x,y in zip(a,b))
 if a is None or type(a)in(str,int,bool):return a==b
 if type(a)is float:
  try:return json.dumps(a,allow_nan=False)==json.dumps(b,allow_nan=False)
  except ValueError:return False
 return False
def need(ok,msg):
 if not ok:raise ValueError('武英殿宋051第14–17段固定批次：'+msg)
def load(root,rel):
 root=Path(root).resolve();p=(root/rel).resolve();need(p.is_relative_to(root),'檔案越界');return json.loads(p.read_bytes())
def contract(root):
 root=Path(root).resolve();p=(root/REF).resolve();need(p.is_relative_to(root/'source-evidence'),'契約路徑');raw=p.read_bytes();need(hashlib.sha256(raw).hexdigest()==CONTRACT_SHA,'契約SHA');return json.loads(raw)
def materialize(v,roles):
 if type(v)is dict:
  if set(v)=={'$role'}:return roles[v['$role']]
  return{k:materialize(x,roles)for k,x in v.items()}
 if type(v)is list:return[materialize(x,roles)for x in v]
 return v
def has_phase(ch):return type(ch)is dict and type(ch.get('annotation'))is dict and 'additional_annotation_phase'in ch['annotation']
def phase_chapter(c,roles,root):
 ch=materialize(c['base_source_template'],roles);ch['annotation']['additional_annotation_phase']={'kind':PHASE,'contract_path':REF,'coverage':c['coverage'],'human_reviewed':False,'model':None}
 for pid in c.get('later_phase',{}).get('paragraph_ids',[]):
  p=next(p for p in ch['paragraphs'] if p['id']==pid);p['annotation_status']='in_progress'
 for row in c['markers']:
  p=next(p for p in ch['paragraphs']if p['id']==row['paragraph_id']);m=materialize(row['marker'],roles);need(not any(x['id']==m['id']for x in p['mentions']),'新增MID碰撞');p['mentions'].append(m);p['mentions'].sort(key=lambda x:x['start']);p['annotation_status']='in_progress'
 try:from scripts.wyd_song051_p018 import markers as p018_markers, title_uses as p018_title_uses
 except ImportError:from wyd_song051_p018 import markers as p018_markers, title_uses as p018_title_uses
 for row in p018_markers(root):
  p=next(p for p in ch['paragraphs']if p['id']==row['paragraph_id']);m=copy.deepcopy(row['marker']);need(not any(x['id']==m['id']for x in p['mentions']),'p018/p019 MID碰撞');p['mentions'].append(m);p['mentions'].sort(key=lambda x:x['start']);p['annotation_status']='in_progress'
 for row in c.get('later_phase',{}).get('pronoun_reclassifications',[]):
  p=next(p for p in ch['paragraphs']if p['id']==row['paragraph_id']);m=next(m for m in p['mentions']if m['id']==row['mention_id']);m['kind']='pronoun';m['status']='contextual_provisional';m['interpretation_note']=row['interpretation_note']
 for row in c.get('later_phase',{}).get('markers',[]):
  p=next(p for p in ch['paragraphs']if p['id']==row['paragraph_id']);m=materialize(row['marker'],roles);need(not any(x['id']==m['id']for x in p['mentions']),'後續批次MID碰撞');p['mentions'].append(m);p['mentions'].sort(key=lambda x:(x['start'],x['end'],x['id']));p['annotation_status']='in_progress'
 for row in c.get('later_phase',{}).get('mention_reclassifications',[]):
  p=next(p for p in ch['paragraphs']if p['id']==row['paragraph_id']);m=next(m for m in p['mentions']if m['id']==row['mention_id'])
  m.update(kind='person',person_id=row['person_id'],status='contextual_provisional',source_role_key=row['source_role_key']);m.pop('note',None)
 ch['annotation'].setdefault('age_assertions',[]).extend(copy.deepcopy(c.get('later_phase',{}).get('age_assertions',[])))
 ch['annotation']['source_title_uses'].extend(p018_title_uses(ch))
 ch['annotation']['source_title_uses'].extend(copy.deepcopy(c.get('later_phase',{}).get('title_uses',[])))
 return ch
def collect(ch,c):
 roles={}
 for row in c['base_role_mentions']+c['markers']:
  mid=row.get('mention_id')or row['marker']['id'];p=next(p for p in ch['paragraphs']if p['id']==row['paragraph_id']);m,=[m for m in p['mentions']if m['id']==mid];role=row['role_key'];pid=m.get('person_id');need(type(pid)is str and pid,'角色PID');need(role not in roles or roles[role]==pid,'角色跨錨不同號');roles[role]=pid
 return roles
def resolve_seeds(root,c):
 rows=load(root,'registry/persons.json')['persons'];people={p['id']:p for p in rows};need(len(people)==len(rows),'種子registry重複ID');roles={}
 for s in c['existing_seeds']:
  ch=load(root,s['path']);need(all(ch.get(k)==s[k]for k in('work_id','book_id','source_id','chapter_id')if k!='chapter_id')and ch['id']==s['chapter_id'],'種子維度');need(hashlib.sha256(json.dumps(ch['source'],ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()==s['source_metadata_sha256'],'種子來源資格')
  metadata=ch['source'];rp=metadata.get('raw_path')or metadata.get('raw_file');hs=metadata.get('raw_file_sha256')or metadata.get('raw_sha256')
  if rp is not None or hs is not None:
   need(type(rp)is str and rp and type(hs)is str and len(hs)==64,'種子raw資格');f=(Path(root)/rp).resolve();need(f.is_relative_to(Path(root).resolve()),'種子raw越界');need(hashlib.sha256(f.read_bytes()).hexdigest()==hs,'種子rawSHA')
  p=next(p for p in ch['paragraphs']if p['id']==s['paragraph_id']);need(p['text']==s['full_paragraph']['text']and hashlib.sha256(p['text'].encode()).hexdigest()==s['paragraph_text_sha256'],'種子完整段');m,=[m for m in p['mentions']if m['id']==s['mention_id']];need(m['kind']=='person'and m['surface']==s['surface']and p['text'][m['start']:m['end']]==s['surface'],'種子MID原字');pid=m['person_id'];person=people.get(pid);need(person is not None,'種子未登記');need(any(a['surface']==m['surface']and m['id']in a['mention_ids']for a in person['aliases']),'種子反向alias');need(any(e['mention_id']==m['id']and e['paragraph_id']==p['id']and e['quote']==m['surface']for e in person['evidence']),'種子反向evidence');roles[s['role_key']]=pid
 return roles
@memoized(0)
def state(root,ch=None):
 root=Path(root).resolve();actual=load(root,CH);need(ch is None or same(ch,actual),'所給current完整章不符');c=contract(root);roles=collect(actual,c);expected=phase_chapter(c,roles,root)
 # Later independently validated p004–p007 work may coexist with this earlier
 # fixed p014–p017 phase. Project those additions away here; their own validator
 # checks every added mention, title-use and age record against the source.
 projected=copy.deepcopy(actual);expected_paragraphs={p['id']:p for p in expected['paragraphs']}
 for p in projected['paragraphs']:
  if p['id'].rsplit(':',1)[-1] in ('p004','p005','p006','p007'):
   base=expected_paragraphs[p['id']];p['mentions']=copy.deepcopy(base['mentions'])
   if 'annotation_status'in base:p['annotation_status']=base['annotation_status']
   else:p.pop('annotation_status',None)
 projected['annotation']['source_title_uses']=[u for u in projected['annotation'].get('source_title_uses',[])if not u.get('id','').startswith('tu-song051-p004-p007-')]
 projected['annotation']['age_assertions']=[a for a in projected['annotation'].get('age_assertions',[])if not a.get('id','').startswith('age-song051-p004-p007-')]
 need(same(projected,expected),'完整原文/舊新錨/資格/位置或新增metadata差異');seeds=resolve_seeds(root,c);need(all(roles[k]==v for k,v in seeds.items()),'既有人物跨源角色錯接');need(roles['yixin']==roles['old_yixin']and roles['wendi']==roles['old_taizu'],'既有角色被另造');need(len({roles[r]for r in c['new_names']})==len(c['new_names']),'本源不同個體不得同號');need(not({roles[r]for r in c['new_names']}&(set(seeds.values())|{v for k,v in roles.items()if k.startswith('old_')})),'新角色與既有人物錯合')
 rows=load(root,'registry/persons.json')['persons'];people={p['id']:p for p in rows};need(len(people)==len(rows),'current registry重複ID')
 # A title-use can point to an adjacent personal-name mention as its title context;
 # only an anchor that exactly covers the marked surface makes that MID title-only.
 title_use_ids={u['person_mention_id'] for u in actual['annotation'].get('source_title_uses',[]) if u.get('source_anchor',{}).get('surface')==next((m['surface'] for p in actual['paragraphs'] for m in p['mentions'] if m['id']==u.get('person_mention_id')),None)}
 later_title_ids={u['person_mention_id'] for u in c.get('later_phase',{}).get('title_uses',[]) if u.get('source_anchor',{}).get('surface')==next((m['surface'] for p in actual['paragraphs'] for m in p['mentions'] if m['id']==u.get('person_mention_id')),None)}
 title_use_ids.update(later_title_ids)
 for row in c['markers']:
  p=next(p for p in actual['paragraphs']if p['id']==row['paragraph_id']);m=next(m for m in p['mentions']if m['id']==row['marker']['id']);person=people.get(m['person_id']);need(person is not None,'新增角色未登記');has_alias=any(a['surface']==m['surface']and m['id']in a['mention_ids']for a in person['aliases']);need((not has_alias)if m['id']in title_use_ids else has_alias,'新增姓名alias／稱號用稱分類不符');e={k:actual[k]for k in('work_id','book_id','source_id')};e.update(chapter_id=CID,paragraph_id=p['id'],mention_id=m['id'],quote=m['surface']);need(e in person['evidence'],'新增evidence缺反向')
 for row in c.get('later_phase',{}).get('markers',[]):
  p=next(p for p in actual['paragraphs']if p['id']==row['paragraph_id']);m=next(m for m in p['mentions']if m['id']==row['marker']['id'])
  if m['kind']=='unresolved':need(m.get('person_id')is None and m.get('status')=='unresolved','後續未決錨不得暗連人物');continue
  person=people.get(m['person_id']);need(person is not None,'後續批次人物未登記');has_alias=any(a['surface']==m['surface']and m['id']in a['mention_ids']for a in person['aliases']);need((not has_alias) if m['id']in title_use_ids else (has_alias if m['kind']=='person' else not has_alias),'後續姓名／稱號／代詞分類不符');e={k:actual[k]for k in('work_id','book_id','source_id')};e.update(chapter_id=CID,paragraph_id=p['id'],mention_id=m['id'],quote=m['surface']);need((e not in person['evidence']) if m['kind']=='pronoun' else (e in person['evidence']),'後續批次姓名反向evidence／代詞排除不符')
 for row in c.get('later_phase',{}).get('mention_reclassifications',[]):
  p=next(p for p in actual['paragraphs']if p['id']==row['paragraph_id']);m=next(m for m in p['mentions']if m['id']==row['mention_id']);person=people.get(row['person_id'])
  need(m['kind']=='person'and m['person_id']==row['person_id']and person is not None,'既有人物提及重分類端點無效')
  need(any(a['surface']==m['surface']and m['id']in a['mention_ids']for a in person['aliases']),'既有人物提及重分類缺反向alias')
  e={k:actual[k]for k in('work_id','book_id','source_id')};e.update(chapter_id=CID,paragraph_id=p['id'],mention_id=m['id'],quote=m['surface']);need(e in person['evidence'],'既有人物提及重分類缺反向evidence')
 for row in c.get('later_phase',{}).get('pronoun_reclassifications',[]):
  p=next(p for p in actual['paragraphs']if p['id']==row['paragraph_id']);m=next(m for m in p['mentions']if m['id']==row['mention_id']);person=people.get(m.get('person_id'));need(m['kind']=='pronoun' and person is not None,'後續代詞須保留有效指涉');need(not any(m['id']in a.get('mention_ids',[])for a in person['aliases']),'後續代詞不得列作姓名alias');e={k:actual[k]for k in('work_id','book_id','source_id')};e.update(chapter_id=CID,paragraph_id=p['id'],mention_id=m['id'],quote=m['surface']);need(e not in person['evidence'],'後續代詞不得留在姓名反向evidence；person_id僅供指涉')
 try:from scripts.wyd_song051_p018 import markers as p018_markers
 except ImportError:from wyd_song051_p018 import markers as p018_markers
 for row in p018_markers(root):
  p=next(p for p in actual['paragraphs']if p['id']==row['paragraph_id']);m=next(m for m in p['mentions']if m['id']==row['marker']['id']);person=people.get(m['person_id']);need(person is not None,'p018/p019人物未登記');has_alias=any(a['surface']==m['surface']and m['id']in a['mention_ids']for a in person['aliases']);need((not has_alias)if m['id']in title_use_ids else has_alias,'p018/p019姓名alias／稱號用稱分類不符');e={k:actual[k]for k in('work_id','book_id','source_id')};e.update(chapter_id=CID,paragraph_id=p['id'],mention_id=m['id'],quote=m['surface']);need(e in person['evidence'],'p018/p019人物缺反向evidence')
 docs={rel:materialize(v,roles)for rel,v in c['expected_documents'].items()}
 for rel,expected in docs.items():
  candidate=load(root,rel)
  if rel=='corpus/songshu/051-wyd1739-life-events.json':candidate['events']=[e for e in candidate['events']if not e['id'].startswith(('le-song051-p018-','le-song051-p019-'))]
  need(same(candidate,expected),'新人物/姓名/親屬sidecar不符：'+rel)
 family=next(f for f in load(root,'registry/family-assemblies.json')['assemblies']if f['id']=='family-song041-qiao');rows={r['person_id']:r for r in family['members']};need(len(rows)==len(family['members']),'家系重複')
 for expected in materialize(c['expected_family_members'],roles):need(same(rows.get(expected['person_id']),expected),'新近系明父/推定父行不符')
 # Names rely on already checked source-based Liu components, not labels or structural IDs.
 old_names=load(root,'corpus/songshu/051-wyd1739-name-components.json')['records']
 for role in ['yixin','yizong']:
  n,=[n for n in old_names if n['id']=='name-song051-phase1-restored-'+role];need(n['person_id']==roles['old_'+role]and n['surname']=='劉'and n['surname_basis']['kind']=='contextual_surname_from_wyd_song051_named_path','劉姓既有源證種子不符')
 return actual,roles,c,docs

def project_previous_phase(root,ch):
 need(type(ch)is dict,'投影須提供完整current章，不以None或缺章回填')
 actual,roles,c,docs=state(root,ch);projected=materialize(c['base_source_template'],roles)
 for row in c.get('later_phase',{}).get('pronoun_reclassifications',[]):
  p=next(p for p in projected['paragraphs'] if p['id']==row['paragraph_id']);m=next(m for m in p['mentions'] if m['id']==row['mention_id']);m['kind']='pronoun';m['status']='contextual_provisional';m['interpretation_note']=row['interpretation_note']
 # The earlier strict 49-anchor phase consumes its exact source-before annotation;
 # newer title-use/proposal records are guarded by this batch contract instead.
 projected['annotation'].pop('source_title_uses',None);projected['annotation'].pop('title_proposals',None);projected['annotation'].pop('age_assertions',None)
 return projected
def previous_frames(root,paragraphs,chapters):
 actual,roles,c,docs=state(root);given=chapters.get(CID);need(same(given,actual),'親屬所給完整current章不符');projected=materialize(c['base_source_template'],roles);pp=copy.copy(paragraphs);cc=copy.copy(chapters);cc[CID]=projected
 for p in actual['paragraphs']:
  if p['id']in paragraphs:need(type(paragraphs[p['id']])is tuple and len(paragraphs[p['id']])==2 and paragraphs[p['id']][0]==CID and same(paragraphs[p['id']][1],p),'親屬所給current原段不符');pp[p['id']]=(CID,next(x for x in projected['paragraphs']if x['id']==p['id']))
 return pp,cc

def family_valid(a,paragraphs,chapters,root):
 try:
  try:from scripts import fixed_wuyingdian_song051_family_phase as core
  except ImportError:import fixed_wuyingdian_song051_family_phase as core
  core.context(root);ch,roles,c,docs=state(root);need(any(same(a,x)for d in docs.values()for x in d.get('assertions',[])),'非本源明親屬');need(same(chapters.get(CID),ch),'親屬章不同')
  for e in a['evidence']:
   p=next(p for p in ch['paragraphs']if p['id']==e['paragraph_id']);frame=paragraphs.get(p['id']);need(type(frame)is tuple and len(frame)==2 and frame[0]==CID and same(frame[1],p),'親屬段不同')
  return True
 except(ValueError,KeyError,TypeError,OSError,StopIteration,AttributeError):return False

def component_valid(n,ch,root):
 try:
  try:from scripts import fixed_wuyingdian_song051_family_phase as core
  except ImportError:import fixed_wuyingdian_song051_family_phase as core
  need(type(ch)is dict,'姓名須提供完整current章');core.context(root);actual,roles,c,docs=state(root,ch);return any(same(n,x)for d in docs.values()for x in d.get('records',[]))
 except(ValueError,KeyError,TypeError,OSError,StopIteration,AttributeError):return False

def validate_surname(n,names,chapters,assertions,root):
 need(type(chapters)is dict and type(names)is list and type(assertions)is list,'姓名catalog須完整章map及JSON lists')
 actual,roles,c,docs=state(root);need(component_valid(n,chapters.get(CID),root),'姓名完整源證');expected=next(x for d in docs.values()for x in d.get('records',[])if x['id']==n['id']);need('surname_basis'in expected,'非復原姓氏行');need(sum(same(x,n)for x in names)==1,'姓名catalog缺漏/重複');source=load(root,'corpus/songshu/051-wyd1739-name-components.json')['records'];seed=next(x for x in source if x['id']==n['surname_basis']['source_name_record_id']);need(sum(same(x,seed)for x in names)==1,'缺原劉姓證據');aa=[a for d in docs.values()for a in d.get('assertions',[])]
 for aid in n['surname_basis']['source_assertion_ids']:
  a=next(a for a in aa if a['id']==aid);need(sum(same(x,a)for x in assertions)==1,'姓氏路徑親屬catalog不全/重複')
 return True

def guard_bundle(root,pid,people,records):
 candidate=people.get(pid)
 registered=isinstance(candidate,dict)and any(e.get('chapter_id')==CID for e in candidate.get('evidence',[]))
 source_records=[r for r in records if r.get('record_type')=='marked_chapter'and r.get('id')==CID]
 source_relevant=any(m.get('person_id')==pid for source in source_records for p in source.get('paragraphs',[])for m in p.get('mentions',[]))
 if not registered and not source_relevant:return
 ch=load(root,CH)
 if not has_phase(ch):return
 actual,roles,c,docs=state(root);registered={p['id']:p for p in load(root,'registry/persons.json')['persons']};need(same(people.get(pid),registered.get(pid)),'bundle現行人物不符')
 for rel,expected in docs.items():
  if rel in c.get('later_phase',{}).get('bundle_excluded_documents',[]):continue
  hits=[]
  for record in records:
   candidate=record
   if rel=='corpus/songshu/051-wyd1739-life-events.json' and type(record)is dict and record.get('record_type')=='person_life_event_assertion_set':
    candidate=copy.deepcopy(record);candidate['events']=[e for e in candidate['events']if not e['id'].startswith(('le-song051-p018-','le-song051-p019-'))]
   if same(candidate,expected):hits.append(record)
  need(len(hits)==1,'bundle新完整人物/親屬/名字資料缺漏或重複')
