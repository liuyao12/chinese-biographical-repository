"""Finite complete received p001–p019 career. Explicit AI source reading, never NLU or PID authority."""
from pathlib import Path
import copy,hashlib,json
try:from scripts.validation_context import memoized
except ImportError:from validation_context import memoized
try:from scripts import fixed_jin098_wangdun_comparison as core
except ImportError:import fixed_jin098_wangdun_comparison as core
KIND='fixed_jin098_received_career_phase1'
CH='corpus/jinshu/098-wangdun-comparison.json'
TITLES='corpus/jinshu/098-wangdun-comparison-titles.json'
DETAILS='corpus/jinshu/098-wangdun-comparison-source-details.json'
EP='source-evidence/jin098-wangdun-career/'
PINS={'source-evidence/jin098-wangdun-career/phase1-template.json': '7960cbc364612ecefeb23bf0115e767f2dae851498bfad8f2edb20f0139924fb', 'source-evidence/jin098-wangdun-career/complete-stage-units.json': 'be8cb467779582a6a2e66f0f9150e9b1160de9c9ade5535c090ec82b33f5691c', 'source-evidence/jin098-wangdun-career/calendar-row-proof.json': 'f67d1b1f6ed33fd1a47e3805c6f585a4c183a1f4f7f2fb52dbb0989d25de8377'}
PINS[EP+'date-bridge-proof.json']='9e42aa257e46360f164af595f2de2259fe3d5b7d47a10f017c682e869396f20a'
def read(root,rel):return json.loads(core.path(root,rel).read_bytes())
def fixed(root,name):
 rel=EP+name;b=core.path(root,rel).read_bytes();core.need(hashlib.sha256(b).hexdigest()==PINS[rel],'098完整官序契約漂移');return json.loads(b)
@memoized(1)
def prepared(ch,root):
 root=Path(root).resolve();core.need(core.same(ch,read(root,CH)),'官序傳入章不是完整actual root');roles=core.resolve(root,ch);t=core.expand(fixed(root,'phase1-template.json'),roles);proof=fixed(root,'complete-stage-units.json')
 core.need(ch['id']==proof['chapter_id']==core.CID and ch['source_id']==core.SID and all(ch[k]==proof[k]for k in('work_id','book_id'))and core.same(ch['source'],proof['source']),'官序完整來源維度或比較資格變動');ps={p['id']:p for p in ch['paragraphs']};core.need(len(ps)==len(ch['paragraphs']),'官序段ID重複')
 for u in proof['units']:
  p=ps[u['paragraph_id']];core.need(p['text']==u['text']and hashlib.sha256(p['text'].encode()).hexdigest()==u['sha256']and p['text_layer']==u['text_layer']=='received_chapter','完整兩表/官序原文或層漂移')
 core.need(hashlib.sha256(core.path(root,ch['source']['raw_path']).read_bytes()).hexdigest()==core.RAW_SHA,'官序raw漂移')
 core.need(all(k in ch['annotation']and core.same(ch['annotation'][k],v)for k,v in t['annotation'].items()),'官序stage/全未受任槽不符')
 for rel,key in[(TITLES,'title_record'),(DETAILS,'detail_record')]:core.need(core.same(read(root,rel),t[key]),'官序稱號/細節槽缺失或被替代')
 for pattern,canonical in[('*-titles.json',TITLES),('*-source-details.json',DETAILS)]:
  for q in (root/'corpus').glob('*/'+pattern):
   if str(q.relative_to(root))==canonical:continue
   r=json.loads(q.read_bytes());core.need(r.get('chapter_id')!=core.CID,'098官序不可藏第二份影子sidecar')
 people={p['id']:p for p in read(root,'registry/persons.json')['persons']};person=people[roles['dun']]
 for rec in t['title_record']['holdings']+t['detail_record']['records']+t['annotation']['title_proposals']:
  b=rec.get('source_career_role',rec.get('source_appointment_context'));p=ps[b['paragraph_id']];mid=b['recipient_mention_id'];m,=[m for m in p['mentions']if m['id']==mid];a=b['role_anchor'];scope=b['scope_anchor']
  core.need(b['kind']==KIND and b['human_reviewed']is False and b['head_mention_id']==core.CID+':p001:m0000'and b['source_revision']==ch['source']['revision_id']and b['paragraph_sha256']==hashlib.sha256(p['text'].encode()).hexdigest(),'官序原段綁定不符');core.need(m.get('kind')=='person'and m['person_id']==roles['dun']==rec['person_id'],'官序主體錯人')
  for x in[a,scope]:core.need(set(x)=={'paragraph_id','start','end','surface'}and x['paragraph_id']==p['id']and type(x['start'])is int and type(x['end'])is int and 0<=x['start']<x['end']<=len(p['text'])and p['text'][x['start']:x['end']]==x['surface'],'官序職名/任免原詞字位不符')
  core.need(any(e.get('mention_id')==mid and e.get('paragraph_id')==p['id']for e in person.get('evidence',[]))and any(mid in a.get('mention_ids',[])and a.get('surface')==m['surface']for a in person.get('aliases',[])),'官序缺同人反向引用')
 check_calendar(root)
 try:from scripts.fixed_jin098_wangdun_career_dates import prepared as date_prepared
 except ImportError:from fixed_jin098_wangdun_career_dates import prepared as date_prepared
 core.need(core.same(t,date_prepared(root,ch,roles)),'098七日期範圍/外年橋不符')
 return roles,t

def joint_stripped_chapter(ch,root):
 """Both owners see the unchanged actual chapter; no intermediate fake root view."""
 ann=ch.get('annotation',{});view=copy.deepcopy(ch);career_keys=set();life_keys=set()
 if isinstance(ann,dict)and ('career_stage'in ann or 'title_proposals'in ann):
  _,t=prepared(ch,root);career_keys=set(t['annotation'])
 if isinstance(ann,dict)and ('life_stage'in ann or 'age_assertions'in ann):
  try:from scripts.fixed_jin098_wangdun_life import prepared as life_prepared
  except ImportError:from fixed_jin098_wangdun_life import prepared as life_prepared
  _,life=life_prepared(ch,root);life_keys=set(life['life_annotation'])
 core.need(not career_keys.intersection(life_keys),'兩來源owner annotation keys衝突')
 for k in career_keys|life_keys:view['annotation'].pop(k)
 return view

def record_valid(rec,ch,root,family):
 try:
  _,t=prepared(ch,root);core.validate_ner(ch,root);rows={'holding':t['title_record']['holdings'],'detail':t['detail_record']['records'],'proposal':t['annotation']['title_proposals']}[family];core.need(core.same([x for x in rows if x['id']==rec.get('id')],[rec]),'官序記錄不是完整已驗來源槽');return True
 except(ValueError,KeyError,TypeError,OSError,IndexError,AttributeError,StopIteration):return False

def catalog_valid(records,people,root):
 q=Path(root)/CH
 if not q.exists():return
 ch=read(root,CH);ann=ch.get('annotation',{});stage=ann.get('career_stage')=='fixed_jin098_career_p001_p019'
 own=[r for r in records if r.get('id')==core.CID or r.get('chapter_id')==core.CID]
 present=any(r.get('annotation',{}).get('career_stage')=='fixed_jin098_career_p001_p019'or any(h.get('source_career_role',{}).get('kind')==KIND for h in r.get('holdings',[])+r.get('records',[]))for r in own)
 if not stage:core.need(not present,'catalog官序stage不是root來源');return
 # A deliberately unrelated partial catalog remains an ordinary legacy caller.
 head,=[m for p in ch['paragraphs']if p['id']==core.CID+':p001'for m in p['mentions']if m['id']==core.CID+':p001:m0000']
 if not own and head['person_id']not in people:return
 _,t=prepared(ch,root)
 for typ,want in [('marked_chapter',ch),('title_holding_assertion_set',t['title_record']),('biographical_source_detail_set',t['detail_record'])]:core.need(core.same([r for r in own if r.get('record_type')==typ],[want]),'passed catalog官序/生命/稱號或細節缺失，不得借actualroot補假catalog')

def date_valid(date,record,role,chapters,root):
 try:
  core.need(role=='source_detail'and isinstance(record,dict),'323僅本源細節事件');ch=read(root,CH);_,t=prepared(ch,root);rows=[r for r in t['detail_record']['records']if r.get('normalized_date')is not None];want,=[r for r in rows if r['id']==record.get('id')];core.need(core.same(want,record)and core.same(date,want['normalized_date']),'紀年不是本源p019該事件完整記錄');core.need(core.same(chapters.get(core.CID),ch),'紀年傳入章不是actualroot');cal=fixed(root,'calendar-row-proof.json');raw=core.path(root,cal['existing_capture_path']).read_bytes();core.need(hashlib.sha256(raw).hexdigest()==cal['existing_capture_sha256']and cal['exact_row_html'].encode()in raw and hashlib.sha256(cal['exact_row_html'].encode()).hexdigest()==cal['row_sha256'],'官方年號列/hash漂移');core.need(cal['row_id']=='av494'and'>太寧</a>'in cal['exact_row_html']and'>東晉<'in cal['exact_row_html']and'>323<'in cal['exact_row_html']and'>326<'in cal['exact_row_html'],'不是東晉太寧列');return True
 except(ValueError,KeyError,TypeError,OSError,IndexError,AttributeError,StopIteration):return False


def check_calendar(root):
 cal=fixed(root,'calendar-row-proof.json');raw=core.path(root,cal['existing_capture_path']).read_bytes();core.need(hashlib.sha256(raw).hexdigest()==cal['existing_capture_sha256']and cal['exact_row_html'].encode()in raw and hashlib.sha256(cal['exact_row_html'].encode()).hexdigest()==cal['row_sha256'],'太甯元年所據官方東晉列/固定hash漂移');core.need(cal['row_id']=='av494'and '>太寧</a>'in cal['exact_row_html']and '>東晉<'in cal['exact_row_html']and '>323<'in cal['exact_row_html']and '>326<'in cal['exact_row_html'],'不是東晉太寧323–326列')
