"""Two exact WYD044 noble clauses; declination is not a never-held claim."""
import hashlib,json
CID='c-songshu-044-wyd1739-xiehui'
SOURCE_SHA='061fed0d8d0942098345af0a05febccd9ff255fe5f3a5fe1d50b8ddc479a3416'
P2_SHA='bab911df6718de36e4591caefe79808a7c68ae3720f40dbb2bfff2c752dff98a'
P3_SHA='45238af487c0fa018ffe2beb0995b83f895c0a83e9f9af32c16f73b8b9964d5b'
REV='cbr-ai-transcription-sha256:8977928c0263cad8f1ab482fbae1e626c9c1f12bed1b45268adbe8f32f112fc2'

def _build(ch):
 if not isinstance(ch,dict)or ch.get('id')!=CID:raise ValueError('非本固定來源')
 if(ch.get('work_id'),ch.get('book_id'),ch.get('source_id'))!=('w-songshu','b-songshu-044','s-songshu-044-wyd1739-xiehui'):raise ValueError('作品卷源不符')
 if hashlib.sha256(json.dumps(ch['source'],ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()!=SOURCE_SHA:raise ValueError('來源資格漂移')
 ps={p['id'].split(':')[-1]:p for p in ch['paragraphs']};p2,p3=ps['p002'],ps['p003']
 if hashlib.sha256(p2['text'].encode()).hexdigest()!=P2_SHA or hashlib.sha256(p3['text'].encode()).hexdigest()!=P3_SHA:raise ValueError('完整段落漂移')
 def mark(p,suffix,surface,start):
  m,=[m for m in p['mentions']if m['id']==p['id']+':'+suffix]
  if m['kind']!='person'or m['surface']!=surface or m['start']!=start or m['end']!=start+len(surface)or p['text'][start:m['end']]!=surface:raise ValueError('角色字位漂移')
  return m
 head=mark(ps['p001'],'m0000','謝晦',0);a=mark(p2,'m0269','晦',269);b=mark(p3,'m0067','晦',67)
 for m in[a,b,mark(p2,'m0289','武昌縣公',289),mark(p3,'m0103','建平郡公',103)]:
  if m['person_id']!=head['person_id']:raise ValueError('主體不得轉移')
 pid=head['person_id']
 def anchor(p,term):
  if p['text'].count(term)!=1:raise ValueError('原詞不唯一')
  i=p['text'].index(term);return dict(paragraph_id=p['id'],start=i,end=i+len(term),surface=term)
 def evidence(p,m):return dict(work_id=ch['work_id'],book_id=ch['book_id'],chapter_id=CID,source_id=ch['source_id'],paragraph_id=p['id'],quote=p['text'],person_mention_id=m['id'])
 def binding(p,m,kind):return dict(kind=kind,subject_mention_id=m['id'],head_mention_id=head['id'],source_revision=REV,paragraph_sha256=hashlib.sha256(p['text'].encode()).hexdigest())
 e2,e3=evidence(p2,a),evidence(p3,b);unknown=dict(status='unknown',date_expression=None,evidence=[])
 h={'id':'th-song044-wyd-wuchang','person_id':pid,'title':'武昌縣公','kind':'noble_rank','mode':'grant','status':'source_attested','appointment_role':'enfeoffment','source_career_role':binding(p2,a,'wyd_song044_noble_grant'),'evidence':[e2],'attestations':[{'id':'ta-song044-wyd-wuchang','paragraph_id':p2['id'],'person_mention_id':a['id'],**{k:anchor(p2,'武昌縣公')[k]for k in('start','end','surface')},'usage':'narrative','date_expression':None}],'effective_period':{'start':{'status':'source_event','event_type':'grant','date_expression':None,'evidence':[e2]},'end':unknown},'grant_anchor':anchor(p2,'以佐命功封武昌縣公食邑二千戶'),'reported_households':{'value':2000,'source_number':'二千','unit':'戶','scope':'actual_enfeoffment_allotment','actual_revenue':None,'source_anchor':anchor(p2,'食邑二千戶')},'interpretation_note':'本源明封武昌縣公，食邑二千戶；戶數不等於已核實收。本源未載授爵年月；卷043完整同詔與傅亮本傳永初元年支持中國曆420的編輯首選。保外源取得資格，不推月日或以卒年作終點。','human_reviewed':False,'model':None}
 q={'id':'proposal-song044-wyd-jianping','person_id':pid,'person_mention_id':b['id'],'title':'建平郡公','kind':'noble_rank','proposal_kind':'appointment_declination_outcome_unreported','outcome':'not_reported','appointment_stage':'appointment','appointment_issued':True,'acceptance_status':'not_reported','effective_service_attested':False,'role_anchor':anchor(p3,'建平郡公'),'appointment_anchor':anchor(p3,'進封建平郡公'),'reported_declination':{'reported':True,'source_term':'固讓進封','source_anchor':anchor(p3,'固讓進封')},'reported_households':{'value':4000,'source_number':'四千','unit':'戶','scope':'offered_advancement_not_confirmed_held','actual_revenue':None,'source_anchor':anchor(p3,'食邑四千戶')},'source_appointment_context':binding(p3,b,'wyd_song044_declined_noble_advance'),'evidence':[e3],'date_expression':None,'status':'contextual_provisional','interpretation_note':'進封已出、固讓進封已載；本傳未明許讓、不許或其後受封。受封結果未載，不是確定未受或永未持有；四千戶僅進封案記數，不關閉武昌爵。','reviewer':'Codex（AI代理）','human_reviewed':False,'model':None}
 q['appointment_anchor']['end']=q['appointment_anchor']['start']+2;q['appointment_anchor']['surface']='進封'
 return h,q

def records(ch,root=None):
 from pathlib import Path
 try:from .wyd_song044_noble_year import date_record
 except ImportError:from wyd_song044_noble_year import date_record
 h,q=_build(ch)
 start=h['effective_period']['start'];start['date_expression']='永初元年'
 start['normalized_date']=date_record(ch,root or Path(__file__).resolve().parents[1])
 return h,q

def proposal_record(ch):return _build(ch)[1]
def holding_valid(h,ch,root=None):
 try:return isinstance(h,dict)and h==records(ch,root)[0]
 except(KeyError,TypeError,ValueError,StopIteration,AttributeError,OSError):return False

def proposal_errors(q,ch,pids):
 try:
  expected=_build(ch)[1]
  if not isinstance(q,dict)or q!=expected or q['person_id']not in pids:return ['進封與辭讓須綁同人完整原句；受否未載不得變為實持或確定未受']
  return []
 except(KeyError,TypeError,ValueError,StopIteration,AttributeError):return ['武英殿進封辭讓來源／角色無效']
