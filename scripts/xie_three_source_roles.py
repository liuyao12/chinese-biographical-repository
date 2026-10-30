"""Three finite source readings; no inferred parentage or global lexical matching."""
import copy,hashlib,json
from pathlib import Path
try:from scripts.validation_context import memoized
except ImportError:from validation_context import memoized
BASE='source-evidence/xie-three-source-roles/'
PROOF_SHA='3f4b374f56c82ac0448beb76783617e0420ea261a0bdb32685cb5f4e7d60a29f'
CARE_ID='a-song056-xiezhan-raised-by-liu'
CARE_KIND='orphan_named_aunt_fuyang_youen'
NS='corpus/nanshi/020-xiehongwei.json'
WY='corpus/songshu/044-wyd1739.json'
SS='corpus/songshu/056-xiezhan.json'
ZH='corpus/shiji/042.json'
FRIEND=('c-nanshi-020-xiehongwei:p017:m0012','c-nanshi-020-xiehongwei:p017:m0015','c-nanshi-020-xiehongwei:p017:m0036')
GUEST='c-nanshi-020-xiehongwei:p017:m0024'
SHUDUAN='c-songshu-044-wyd1739-xiehui:p012:m0126'
SEED='c-shiji-042-zheng:m003-0039'
IDENTITIES={'corpus/nanshi/020-xiehongwei-identities.json':('d-nanshi020-hongwei-chess-friend','d-nanshi020-hongwei-second-guest'),'corpus/songshu/044-wyd1739-identities.json':('d-song044-wyd-shuduan-allusion',)}
def need(ok,msg):
 if not ok:raise ValueError('謝氏三案：'+msg)
def read(root,path):
 root=Path(root).resolve();p=(root/path).resolve();need(p.is_relative_to(root),'來源路徑越界');return json.loads(p.read_bytes())
def fixed(root):
 p=(Path(root).resolve()/BASE/'proof.json').resolve();need(p.is_relative_to(Path(root).resolve()),'proof越界');raw=p.read_bytes();need(hashlib.sha256(raw).hexdigest()==PROOF_SHA,'proof SHA');return json.loads(raw)
def same(a,b):return type(a)is type(b)and json.dumps(a,ensure_ascii=False,sort_keys=True)==json.dumps(b,ensure_ascii=False,sort_keys=True)
def expand(v,roles):
 if isinstance(v,dict):
  if set(v)=={'$role'}:return roles[v['$role']]
  return {k:expand(x,roles)for k,x in v.items()}
 if isinstance(v,list):return [expand(x,roles)for x in v]
 return v
def normalized(ch):
 """Dynamic first-MID symbols preserve consistent rekeys and reject split endpoints."""
 ids={}
 for p in ch['paragraphs']:
  for m in p['mentions']:
   if m.get('kind')in('person','pronoun'):ids.setdefault(m['person_id'],m['id'])
 def visit(v):
  if isinstance(v,str)and v in ids:return {'$source_mid':ids[v]}
  if isinstance(v,dict):return {k:visit(x)for k,x in v.items()}
  if isinstance(v,list):return [visit(x)for x in v]
  return v
 return visit(ch)
def marker(ch,mid):
 hits=[(p,m)for p in ch['paragraphs']for m in p['mentions']if m['id']==mid];need(len(hits)==1,'MID唯一性');p,m=hits[0];need(type(m['start'])is int and type(m['end'])is int and p['text'][m['start']:m['end']]==m['surface'],'MID字位');return p,m
def evidence(ch,p,m):return {'work_id':ch['work_id'],'book_id':ch['book_id'],'source_id':ch['source_id'],'chapter_id':ch['id'],'paragraph_id':p['id'],'mention_id':m['id'],'quote':m['surface']}
def reverse(person,ch,p,m,legacy=False):
 expected=evidence(ch,p,m)
 if legacy:expected={k:expected[k]for k in ('mention_id','chapter_id','paragraph_id','quote')}
 need(any(a.get('surface')==m['surface']and m['id']in a.get('mention_ids',[])for a in person['aliases']),'alias雙向')
 need(expected in person['evidence'],'完整來源reverse')
@memoized(0)
def prepared(root):
 proof=fixed(root);chs={p:read(root,p)for p in proof['chapters']};roles={}
 for path,expected in proof['chapters'].items():need(same(normalized(chs[path]),expected),'固定全文/來源/層/字位/非本案角色漂移：'+path)
 # Source semantics are independent of editable template/PIN: do not let a self-consistent wrong assertion through.
 p,m=marker(chs[SS],'c-songshu-056-xiezhan:p001:m0059');_,aunt=marker(chs[SS],'c-songshu-056-xiezhan:p001:m0064')
 need((m['surface'],m['start'],m['end'],aunt['surface'],aunt['start'],aunt['end'])==('瞻',59,60,'劉',64,65)and p['text'][59:69]=='瞻幼孤叔母劉撫養有恩','瞻幼孤叔母劉撫養句')
 need(marker(chs[SS],'c-songshu-056-xiezhan:p001:m0000')[1]['person_id']==m['person_id'],'瞻完整名錨');roles['child']=m['person_id'];roles['caregiver']=aunt['person_id']
 for role,path,mid in [('friend',NS,FRIEND[0]),('guest',NS,GUEST),('shuduan',ZH,SEED)]:roles[role]=marker(chs[path],mid)[1]['person_id']
 need(len(set(roles.values()))==5,'五個來源角色不得混同')
 for mid in FRIEND:need(marker(chs[NS],mid)[1]['person_id']==roles['friend'],'三個友錨須同人')
 need(marker(chs[WY],SHUDUAN)[1]['person_id']==roles['shuduan'],'叔段必須源自042 seed')
 p3,m3=marker(chs[ZH],SEED);need(m3['surface']=='叔段'and m3['start']==39 and m3['end']==41 and '後生少子叔段' in p3['text'],'042叔段原文')
 p4=next(p for p in chs[ZH]['paragraphs']if p['id']=='c-shiji-042-zheng:p004');need(p4['text'].startswith('莊公元年，封弟段於京，號太叔。')and '莊公發兵伐段' in p4['text'],'封京伐段完整語境')
 # Keep only five endpoint metadata records in the scope memo, never the registry.
 people={p['id']:p for p in read(root,'registry/persons.json')['persons']if p['id']in set(roles.values())};need(len(people)==5,'缺現役來源角色')
 for role,path,mid in [('child',SS,'c-songshu-056-xiezhan:p001:m0059'),('caregiver',SS,'c-songshu-056-xiezhan:p001:m0064'),('shuduan',ZH,SEED),('shuduan',WY,SHUDUAN)]:
  p,m=marker(chs[path],mid);reverse(people[roles[role]],chs[path],p,m,legacy=path==ZH)
 for role,mids in [('friend',FRIEND),('guest',(GUEST,))]:
  actual=people[roles[role]];need(same(actual,expand(proof['anonymous_people'][role],roles)),'未名個體不能冒借已知角色/補性別姓名或跨源同指')
  for mid in mids:
   p,m=marker(chs[NS],mid);reverse(actual,chs[NS],p,m)
 templates=expand(proof['records'],roles)
 a=templates['care'];need(a['predicate']=='raised_by'and a['subject_person_id']==roles['child']and a['object_person_id']==roles['caregiver']and a['qualifiers']=={'source_term':'瞻幼孤叔母劉撫養有恩','care_basis':CARE_KIND,'legal_adoption_status':'not_stated'}and a['human_reviewed']is False,'撫養不升母/法律收養/兄弟')
 for path,ids in IDENTITIES.items():
  actual=read(root,path);expected=templates[path]
  need(actual.get('record_type')=='person_identity_decision_set'and actual.get('chapter_id')==expected['chapter_id'],'身份檔header')
  need(same([d for d in actual['decisions']if d['id']in ids],expected['decisions']),'同指scope/來源/端點/限定不符')
 decision=templates[WY.replace('.json','-identities.json')]['decisions'][0]
 need(decision.get('source_context')=={'kind':'historical_allusion','person_mention_id':SHUDUAN,'contemporary_participation':'not_asserted','transfer_source_event_to_referent':'forbidden','speech_paragraph_ids':['c-songshu-044-wyd1739-xiehui:'+n for n in ('p010','p011','p012','p013')]},'引古不是宋代在場或事件移轉')
 need(decision['scope']=='cross_chapter'and decision['chapter_ids']==[chs[WY]['id'],chs[ZH]['id']]and decision['person_id']==roles['shuduan']and '不將廬陵死亡移給古人' in decision['rationale'],'叔段只引古')
 actual=read(root,'corpus/songshu/056-xiezhan-assertions.json');need(same([x for x in actual['assertions']if family_applies(x)],[a]),'撫養exact有限來源槽')
 review=read(root,'source-evidence/nanshi020-xiehongwei-reading/review.json');mids=set(FRIEND+(GUEST,))
 need(not any(x.get('mention',{}).get('id')in mids for x in review['unresolved']),'current reading仍錯列未定')
 expected=expand(proof['current_reading'],roles)
 need(same([x for x in review['identity_rows']if x.get('key')in ('chess-friend','chess-guest')],expected['identity_rows']),'current role ledger漂移')
 need(same([x for x in review['followup_resolutions']if x.get('mention_id')in mids],expected['followup_resolutions']),'current reading四錨處置缺失')
 return roles,chs,people,templates

def family_applies(a):
 if not isinstance(a,dict):return False
 if a.get('id')==CARE_ID or a.get('qualifiers',{}).get('care_basis')==CARE_KIND:return True
 return any(e.get('paragraph_id')=='c-songshu-056-xiezhan:p001'and e.get('subject_person_mention_id')=='c-songshu-056-xiezhan:p001:m0059'and e.get('object_person_mention_id')=='c-songshu-056-xiezhan:p001:m0064'for e in a.get('evidence',[]))
def family_valid(a,paragraphs,root):
 try:
  _,chs,_,t=prepared(root);p=next(p for p in chs[SS]['paragraphs']if p['id']=='c-songshu-056-xiezhan:p001');need(paragraphs.get(p['id'])==(chs[SS]['id'],p),'caller撫養完整段缺失/漂移');return same(a,t['care'])
 except (ValueError,KeyError,TypeError,OSError,StopIteration):return False

def source_errors(ch,root):
 if not isinstance(ch,dict)or ch.get('id')not in ('c-songshu-056-xiezhan','c-nanshi-020-xiehongwei','c-songshu-044-wyd1739-xiehui'):return []
 try:
  _,chs,_,_=prepared(root);expected=next(c for c in chs.values()if c['id']==ch['id']);need(same(ch,expected),'caller來源不是實體完整章');return []
 except (ValueError,KeyError,TypeError,OSError,StopIteration)as e:return ['謝氏三案：'+str(e)]

def event_applies(e):return isinstance(e,dict)and any(x.get('paragraph_id')=='c-songshu-044-wyd1739-xiehui:p012'and(x.get('person_mention_id')==SHUDUAN or '叔段' in x.get('quote',''))for x in e.get('evidence',[]))
def event_valid(e,root):
 roles,_,_,_=prepared(root)
 return e.get('person_id')!=roles['shuduan'] # 宋代廬陵敘事不能變鄭叔段實際事件。
@memoized(0)
def role_ids(root):
 roles={}
 for role,path,mid in [('child',SS,'c-songshu-056-xiezhan:p001:m0059'),('caregiver',SS,'c-songshu-056-xiezhan:p001:m0064'),('friend',NS,FRIEND[0]),('guest',NS,GUEST),('shuduan',ZH,SEED)]:
  _,m=marker(read(root,path),mid);need(m.get('kind')=='person'and bool(m.get('person_id')),'來源角色錨缺失');roles[role]=m['person_id']
 return roles
def guard_bundle(root,pid,people,records):
 # Legacy/partial fixtures without this source stage retain their former path.
 if not (Path(root)/(BASE+'proof.json')).exists():
  owned=False
  for r in records:
   if r.get('record_type')=='person_assertion_set':owned=owned or any(family_applies(a)for a in r.get('assertions',[]))
   if r.get('record_type')=='marked_chapter':owned=owned or any(m.get('kind')=='person'and m.get('id')in set(FRIEND+(GUEST,SHUDUAN))for p in r.get('paragraphs',[])for m in p.get('mentions',[]))
  need(not owned,'本階段資料仍在，來源proof卻缺失')
  return
 # Only five IDs survive the per-scope first-MID scan; no registry retained.
 if pid not in role_ids(root).values():return
 roles,chs,actual,templates=prepared(root)
 for key,value in actual.items():need(key in people and same(people[key],value),'caller五端點metadata/reverse缺失')
 catalog_chapters={r['id']:r for r in records if r.get('record_type')=='marked_chapter'}
 for path,ch in chs.items():need(ch['id']in catalog_chapters and same(catalog_chapters[ch['id']],ch),'caller缺來源或給假章')
 for path,t in templates.items():
  if path=='care':continue
  selected=[r for r in records if r.get('record_type')=='person_identity_decision_set'and r.get('chapter_id')==t['chapter_id']]
  got=[d for r in selected for d in r['decisions']if d['id']in {x['id']for x in t['decisions']}];need(same(got,t['decisions']),'caller缺同指scope/兩篇evidence')
 care=[a for r in records if r.get('record_type')=='person_assertion_set'for a in r['assertions']if family_applies(a)];need(same(care,[templates['care']]),'caller缺撫養/誤母收養')
 for r in records:
  if r.get('record_type')=='person_life_event_assertion_set':
   for e in r.get('events',[]):
    if event_applies(e):need(event_valid(e,root),'引古叔段不能建宋代生命事件')
