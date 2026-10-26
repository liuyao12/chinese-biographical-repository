"""Finite source-bound deaths; existing regnal-year arithmetic remains mandatory."""
from pathlib import Path
import importlib.util,json,hashlib,copy,sys
CID='c-songshu-045-wyd1739-liucui';SOURCE='corpus/songshu/045-wyd1739-liucui.json'
ROW='source-evidence/song045-wyd1739-liucui/life-moe-yuanjia-row.json'
ROW_SHA='fc8a17ad4e6050f84622b4dd3360c3e37eecfc4fdac0be4608d9281dc121847c'
H=lambda b:hashlib.sha256(b).hexdigest()
def context(root):
 root=Path(root);ch=json.loads((root/SOURCE).read_bytes());old_path=list(sys.path)
 try:
  sys.path[:0]=[str(root),str(root/'scripts')]
  def load(name,path):
   s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
  m=load('life_wyd045_roles',root/'scripts/wyd_song045_roles.py');base=m.source_only_projection(ch,root)
  w=load('life_wyd045_witness',root/'scripts/fixed_wuyingdian_song045_liucui.py');w.validate_source(base,root)
  roles=m.resolve_roles(ch,root);return ch,m.load_contract(root),roles
 finally:sys.path[:]=old_path

def records(root):
 ch,c,roles=context(root);ps={p['id'].split(':')[-1]:p for p in ch['paragraphs']};spec={p['id']:p for p in c['paragraphs']};raw=(Path(root)/ROW).read_bytes();assert H(raw)==ROW_SHA;row=json.loads(raw);assert row['columns']=={'dynasty':'宋','era_name':'元嘉','first_year':'424','last_year':'453'}
 def a(p,s):
  assert p['text'].count(s)==1;lo=p['text'].index(s);return dict(paragraph_id=p['id'],start=lo,end=lo+len(s),surface=s)
 def mark(p,r,within=None):
  candidates=[x for x in spec[p['id']]['mentions']if x.get('role_key')==r and(within is None or within['start']<=x['start']<within['end'])];assert candidates
  return next(x for x in p['mentions']if x['id']==candidates[0]['id'])
 def ev(p,m):return dict(work_id=ch['work_id'],book_id=ch['book_id'],source_id=ch['source_id'],chapter_id=CID,paragraph_id=p['id'],quote=p['text'],person_mention_id=m['id'])
 out=[]
 for slot,role,key,term,clause,date,year,chain in [
  ('cui','liucui','p004','卒','明年粹卒時年五十三','明年',427,[('p004','元嘉三年',3),('p004','明年',4)]),
  ('daoji','liudaoji','p011','卒','十年正月賊衆大至攻逼成都道濟卒','十年正月',433,[('p005','元嘉九年',9),('p006','其年七月',9),('p009','十一月',9),('p010','十二月末',9),('p011','十年正月',10)]),
  ('huai','huaizhi','p004','伏誅','粹庶長子懷之為臨川內史與臧質同逆伏誅',None,None,[])]:
  p=ps[key];cl=a(p,clause);m=mark(p,role,cl);e=ev(p,m)
  b={'kind':'fixed_wyd045_death_scope','slot':slot,'subject_mention_id':m['id'],'paragraph_sha256':H(p['text'].encode()),'source_revision':ch['source']['revision_id'],'clause_anchor':cl,'death_anchor':a(p,clause[:clause.index(term)+len(term)]) if False else dict(paragraph_id=p['id'],start=cl['start']+clause.rindex(term),end=cl['start']+clause.rindex(term)+len(term),surface=term),'human_reviewed':False}
  x=dict(id='le-song045-wyd-'+slot,person_id=roles[role],event_type='death',source_term=term,date_expression=date,status='source_attested',evidence=[e],source_wyd045_death_scope=b,interpretation_note='只記此明示死亡；不由卒年/報齡倒生年或結束全部官爵。' if slot!='huai' else '懷之與臧質同逆伏誅；本源無明年，不借粹卒或其他敘事日期。庶長子排行另存。',reviewer='Codex（AI代理）',human_reviewed=False,model=None)
  if date:
   refs=[{'title':'教育部《重編國語辭典修訂本》中國歷代年號表','url':row['url'],'scope':'modern_era_year_equivalence_only','quote':'元嘉','columns':copy.deepcopy(row['columns']),'fixed_row_reference':{'path':ROW,'sha256':ROW_SHA},'image_verified':False}]
   de=[ev(ps[k],mark(ps[k],role))for k in dict.fromkeys(k for k,_,_ in chain)]
   normalized=dict(era='CE',year=year,era_year=year,year_numbering='astronomical',precision='year',calendar='chinese_civil',source_expression=date,original_quote=p['text'],status='editorial_provisional',evidence=de,references=refs,rationale='AI依完整本源段落與逐年/月錨點換算中國曆年；正月保原詞，不補西曆月日或農曆日序。',reviewer='Codex（AI代理）',human_reviewed=False,model=None)
   normalized['event_evidence_binding']={'kind':'fixed_wyd045_death_local_year','event_id':x['id'],'person_id':x['person_id'],'subject_mention_id':m['id'],'chain':[{'anchor':a(ps[k],phrase),'regnal_year':n,'paragraph_sha256':H(ps[k]['text'].encode())}for k,phrase,n in chain],'calendar_row':{'path':ROW,'sha256':ROW_SHA},'human_reviewed':False}
   normalized['regnal_year_mapping']={'kind':'fixed_wyd045_death_local_year','era_name':'元嘉','start_ce_year':424,'end_ce_year':453,'regnal_year':year-424+1,'reference_index':0}
   x['normalized_date']=normalized
  out.append(x)
 return out

def valid(event,root):
 # fixed-wyd045-extra-heir-deaths
 try:from scripts.wyd_song045_nobles import death_valid,death_applies
 except ImportError:from wyd_song045_nobles import death_valid,death_applies
 if death_applies(event):return death_valid(event,root)
 if not isinstance(event,dict)or not isinstance(event.get('source_wyd045_death_scope'),dict):return False
 try:return any(json.dumps(event,ensure_ascii=False,sort_keys=True,separators=(',',':'))==json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))for x in records(root))
 except(KeyError,TypeError,ValueError,AssertionError,StopIteration,OSError,AttributeError):return False

def date_valid(date,event,chapters,root=None):
 if not isinstance(date,dict)or not isinstance(event,dict)or root is None:return False
 try:
  ch,_,_=context(root);assert chapters.get(CID)==ch
  return valid(event,root)and json.dumps(event.get('normalized_date'),ensure_ascii=False,sort_keys=True,separators=(',',':'))==json.dumps(date,ensure_ascii=False,sort_keys=True,separators=(',',':'))
 except(KeyError,TypeError,ValueError,AssertionError,StopIteration,OSError,AttributeError):return False

def age_record(ch):
 if not isinstance(ch,dict)or ch.get('id')!=CID:raise ValueError('宋045報齡篇錯')
 p=next(p for p in ch['paragraphs']if p['id']==CID+':p004');t=p['text'];phrase='明年粹卒時年五十三';assert t.count(phrase)==1;lo=t.index(phrase);m=next(m for m in p['mentions']if m['start']==lo+2 and m['surface']=='粹');assert m['kind']=='person'
 e=dict(work_id=ch['work_id'],book_id=ch['book_id'],source_id=ch['source_id'],chapter_id=CID,paragraph_id=p['id'],quote=t,person_mention_id=m['id'])
 return dict(id='age-song045-wyd-cui-death',person_id=m['person_id'],value=53,source_number='五十三',source_term='年五十三',unit='source_age_years',counting='unspecified_source_age',birth_year=None,status='source_attested',date_expression=None,evidence=[e],age_context={'kind':'at_death','life_event_id':'le-song045-wyd-cui'},age_interpretation={'kind':'traditional_nominal_age_editorial_reading','status':'editorial_provisional','human_reviewed':False,'rationale':'本庫依傳統虛歲理解此史籍報齡；原句未明計歲法，不偽稱source明說虛歲，不推周歲或出生年。'},interpretation_note='明年粹卒時年五十三：53為本源卒齡，連同人同段死亡；與明年換算分存，不倒生年。',reviewer='Codex（AI代理）',human_reviewed=False,model=None)

def base_annotation(ch):
 a=copy.deepcopy(ch['annotation'])
 if 'age_assertions'in a:
  if json.dumps(a.pop('age_assertions'),ensure_ascii=False,sort_keys=True,separators=(',',':'))!=json.dumps([age_record(ch)],ensure_ascii=False,sort_keys=True,separators=(',',':')):raise ValueError('宋045卒齡須綁粹完整原句、整數53、同死亡事件與虛歲解讀資格')
 return a
