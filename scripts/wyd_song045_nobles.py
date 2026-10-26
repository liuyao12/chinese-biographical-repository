"""Finite WYD045 noble sequence; source grants and inferred inheritance stay distinct."""
from pathlib import Path
import copy,json,hashlib,sys,importlib.util
CID='c-songshu-045-wyd1739-liucui';ROW='source-evidence/song045-wyd1739-liucui/nobles-moe-yongchu-row.json';ROW_SHA='34a7f4340228b9c8e7218126e8f01e0c16b3a59a6f7a0530f5860c78361c079e'
J=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))
H=lambda b:hashlib.sha256(b).hexdigest()
def anchor(p,s):
 if p['text'].count(s)!=1:raise ValueError('爵序原句不唯一')
 start=p['text'].index(s);return dict(paragraph_id=p['id'],start=start,end=start+len(s),surface=s)
def ev(ch,p,m):return dict(work_id=ch['work_id'],book_id=ch['book_id'],source_id=ch['source_id'],chapter_id=CID,paragraph_id=p['id'],quote=p['text'],person_mention_id=m['id'])
def context(root):
 root=Path(root);old=list(sys.path)
 try:
  sys.path[:0]=[str(root),str(root/'scripts')]
  s=importlib.util.spec_from_file_location('noble045_life',root/'scripts/wyd_song045_lifecycle.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m.context(root)
 finally:sys.path[:]=old

def proposal(ch):
 p=ch['paragraphs'][14];a=anchor(p,'左光祿大夫徵不就');i=p['text'].index('鎮之門');m=next(m for m in p['mentions']if m['start']==i and m['surface']=='鎮之');assert m['kind']=='person'
 role=dict(a,end=a['start']+5,surface='左光祿大夫');app=dict(a,start=role['end'],end=role['end']+1,surface='徵');no=dict(a,start=app['end'],surface='不就')
 return dict(id='proposal-song045-wyd-zhenzhi-nonassumption',person_id=m['person_id'],person_mention_id=m['id'],title='左光祿大夫',kind='office',proposal_kind='unassumed_appointment',outcome='not_assumed',appointment_stage='appointment',role_anchor=role,appointment_anchor=app,non_assumption_anchor=no,non_assumption_kind='did_not_take_up',evidence=[ev(ch,p,m)],date_expression=None,status='contextual_provisional',interpretation_note='左光祿大夫徵不就：明記未赴任，不入實持；不以元嘉二年卒或年九十餘當徵召日期。',reviewer='Codex（AI代理）',human_reviewed=False,model=None)
def base_annotation(ch):
 a=copy.deepcopy(ch['annotation'])
 if 'title_proposals'in a:
  if J(a.pop('title_proposals'))!=J([proposal(ch)]):raise ValueError('宋045不就原詞／主體／未知日期或任職性質漂移')
 return a

def records(root):
 root=Path(root);ch,c,roles=context(root);ps={p['id'].split(':')[-1]:p for p in ch['paragraphs']};spec={p['id']:p for p in c['paragraphs']};rowpath=(root/ROW).resolve();assert rowpath.is_relative_to(root.resolve()/'source-evidence');rr=rowpath.read_bytes();assert H(rr)==ROW_SHA;row=json.loads(rr);assert row['columns']==dict(dynasty='宋',era_name='永初',first_year='420',last_year='422')
 def mark(p,r,phrase=None):
  area=anchor(p,phrase)if phrase else None
  ss=[m for m in spec[p['id']]['mentions']if m.get('role_key')==r and(area is None or area['start']<=m['start']<area['end'])];assert ss
  return next(m for m in p['mentions']if m['id']==ss[0]['id'])
 def holding(slot,r,pkey,title,mode,phrase,raw=None,date=None):
  p=ps[pkey];area=anchor(p,phrase);has_local=any(x.get('role_key')==r and area['start']<=x['start']<area['end']for x in spec[p['id']]['mentions']);m=mark(p,r,phrase if has_local else None);e=ev(ch,p,m);unknown=dict(status='unknown',date_expression=None,evidence=[]);a=anchor(p,raw or title)
  h=dict(id='th-song045-wyd-'+slot,person_id=roles[r],title=title,kind='office'if mode=='posthumous_grant'else'noble_rank',mode=mode,status='source_attested',appointment_role={'grant':'enfeoffment','transfer':'noble_rank_change','accession':'hereditary_succession','posthumous_grant':'posthumous_office'}[mode],source_career_role={'kind':'fixed_wyd045_noble_sequence','slot':slot,'source_revision':ch['source']['revision_id'],'paragraph_sha256':H(p['text'].encode()),'subject_mention_id':m['id'],'clause_anchor':anchor(p,phrase),'human_reviewed':False},evidence=[e],attestations=[dict(id='ta-song045-wyd-'+slot,**a,person_mention_id=m['id'],usage='posthumous_usage'if mode=='posthumous_grant'else'narrative',date_expression=None)],effective_period={'start':dict(status='source_event',event_type=mode,date_expression=date,evidence=[e]),'end':copy.deepcopy(unknown)},interpretation_note='本源爵官事件；未知月日及終期，不以鄰接背景年或死亡填所有任期。',reviewer='Codex（AI代理）',human_reviewed=False,model=None)
  if mode=='posthumous_grant':h['posthumous_basis']={'source_term':'追贈'+title,'evidence':[e]}
  return h
 xian=holding('cui-xian','liucui','p001','西安縣五等侯','grant','以義功封西安縣五等侯')
 she=holding('cui-she','liucui','p002','灄縣男','grant','事平封灄縣男食邑五百戶')
 jian=holding('cui-jianan','liucui','p002','建安縣侯','transfer','永初元年以佐命功改封建安縣侯食邑千戶',date='永初元年')
 for h,number,value in[(she,'五百',500),(jian,'千',1000)]:h['reported_households']={'value':value,'source_number':number,'unit':'戶','scope':'actual_enfeoffment_allotment','actual_revenue':None,'source_anchor':anchor(ps['p002'],'食邑'+number+'戶')}
 e=jian['evidence'];m=mark(ps['p002'],'liucui');jian['transfer_basis']=dict(kind='noble_rank_change',previous_holding_id=she['id'],previous_title_status='source_context',source_term='改封建安縣侯',actor_mention_id=m['id'],evidence=e,rationale='同人本源前載灄縣男、後明改封建安；只閉此既接前爵，不把西安五等侯也自動關閉。',status='editorial_provisional',human_reviewed=False)
 normalized=dict(era='CE',year=420,era_year=420,year_numbering='astronomical',precision='year',calendar='chinese_civil',source_expression='永初元年',original_quote=ps['p002']['text'],evidence=e,references=[dict(title='教育部《重編國語辭典修訂本》中國歷代年號表',url=row['url'],scope='modern_era_year_equivalence_only',quote='永初',columns=copy.deepcopy(row['columns']),fixed_row_reference=dict(path=ROW,sha256=ROW_SHA),image_verified=False)],regnal_year_mapping=dict(kind='ce_regnal_era_span',era_name='永初',source_number='元',regnal_year=1,start_ce_year=420,end_ce_year=422,reference_index=0),status='editorial_provisional',rationale='本源明永初元年與改封同句；固定宋永初420–422對照，年精度不補月日。',reviewer='Codex（AI代理）',human_reviewed=False,model=None)
 jian['effective_period']['start']['normalized_date']=normalized;she['effective_period']['end']=dict(status='source_event',event_type='explicit_end',date_expression='永初元年',normalized_date=copy.deepcopy(normalized),evidence=e)
 kuang=holding('kuang-jianan','kuangzhi','p004','建安縣侯','accession','曠之嗣',raw='曠之嗣');kuang['attestations'][0]['start']+=2;kuang['attestations'][0]['surface']='嗣'
 chen=holding('chen-jianan','chen','p004','建安縣侯','accession','曠之卒子琛嗣',raw='曠之卒子琛嗣');chen['attestations'][0]['start']=chen['attestations'][0]['end']-1;chen['attestations'][0]['surface']='嗣'
 for h,prev,term,relation in[(kuang,jian,'曠之嗣','a-song045-wyd-kuang-father'),(chen,kuang,'曠之卒子琛嗣','a-song045-wyd-chen-father')]:
  h['inheritance']=dict(predecessor_person_id=prev['person_id'],predecessor_holding_id=prev['id'],resolved_title='建安縣侯',source_term=term,status='contextual_provisional',evidence=h['evidence'],rationale='原文嗣不重出爵名；循本源已明父子與前任本爵鏈判為承建安縣侯，不冒本句逐字明爵，不補承嗣年。',human_reviewed=False)
  h['source_succession_binding']={'kind':'fixed_wyd045_father_succession','father_assertion_id':relation,'predecessor_holding_id':prev['id'],'source_term':term,'status':'contextual_provisional','human_reviewed':False}
  h['title']='嗣';h['interpretation_note']=h['inheritance']['rationale']
 bei=holding('cui-anbei','liucui','p004','安北將軍','posthumous_grant','明年粹卒時年五十三追贈安北將軍持節本官如故')
 tai=holding('sun-taichang','liusun','p015','太常','posthumous_grant','官至吳郡太守追贈太常')
 return [xian,she,jian,kuang,chen,bei,tai],proposal(ch)

def holding_valid(h,ch,holdings,root=None):
 if not isinstance(h,dict)or root is None:return False
 try:
  expected,_=records(root);by={x['id']:x for x in expected};assert J(h)==J(by[h['id']]);actual,_,_=context(root);assert J(ch)==J(actual)
  if 'inheritance'in h:
   prior=by[h['inheritance']['predecessor_holding_id']];assert J(holdings.get(prior['id']))==J(prior)
   aa=json.loads((Path(root)/'corpus/songshu/045-wyd1739-liucui-assertions.json').read_bytes())['assertions'];a=next(a for a in aa if a['id']==h['source_succession_binding']['father_assertion_id']);assert a['predicate']=='father'and a['subject_person_id']==h['person_id']and a['object_person_id']==prior['person_id']
   spec=importlib.util.spec_from_file_location('noble_father_roles',Path(root)/'scripts/wyd_song045_roles.py');rm=importlib.util.module_from_spec(spec);spec.loader.exec_module(rm);expected_a=next(x for x in rm.relation_records(ch,root)if x['id']==a['id']);assert J(a)==J(expected_a)
  if h['mode']=='transfer':assert J(holdings.get(h['transfer_basis']['previous_holding_id']))==J(by[h['transfer_basis']['previous_holding_id']])
  return True
 except(KeyError,TypeError,ValueError,AssertionError,StopIteration,OSError,AttributeError):return False

def extra_deaths(root):
 ch,c,roles=context(root);p=ch['paragraphs'][3];spec=next(x for x in c['paragraphs']if x['id']==p['id']);out=[]
 for role,phrase,term in [('kuangzhi','曠之卒子琛嗣','卒'),('chen','琛卒無子國除','卒')]:
  area=anchor(p,phrase);s=next(s for s in spec['mentions']if s.get('role_key')==role and area['start']<=s['start']<area['end']);m=next(m for m in p['mentions']if m['id']==s['id'])
  out.append(dict(id='le-song045-wyd-'+role,person_id=roles[role],event_type='death',source_term=term,date_expression=None,status='source_attested',evidence=[ev(ch,p,m)],source_wyd045_noble_death_scope={'kind':'fixed_wyd045_heir_death','role':role,'clause_anchor':area,'human_reviewed':False},interpretation_note='本源明此繼承人卒；無年，不承接父祖卒年或同段後文昇明日期。',reviewer='Codex（AI代理）',human_reviewed=False,model=None))
 return out

def event_record(root):
 ch,c,roles=context(root);p=ch['paragraphs'][3];area=anchor(p,'琛卒無子國除');spec=next(x for x in c['paragraphs']if x['id']==p['id']);s=next(s for s in spec['mentions']if s.get('role_key')=='chen'and area['start']<=s['start']<area['end']);m=next(m for m in p['mentions']if m['id']==s['id'])
 return dict(id='event-song045-wyd-chen-state-abolition',person_id=roles['chen'],event_type='noble_state_abolition',status='source_attested',date_expression=None,source_term='國除',title='建安縣侯',holding_id='th-song045-wyd-chen-jianan',source_career_role={'kind':'fixed_wyd045_noble_line_event'},source_clause_binding={'kind':'fixed_wyd045_noble_line_abolition','clause_anchor':area,'subject_mention_id':m['id'],'title_resolution_status':'contextual_provisional','human_reviewed':False},evidence=[ev(ch,p,m)],interpretation_note='琛卒無子國除；爵名沿已明授與兩代父子承嗣鏈識得，本句未再明爵，無年月。不由無子造絕對子女數或以本句終止其他官爵。',reviewer='Codex（AI代理）',human_reviewed=False,model=None)

def death_valid(e,root):
 try:return isinstance(e,dict)and any(J(e)==J(x)for x in extra_deaths(root))
 except(KeyError,TypeError,ValueError,AssertionError,StopIteration,OSError,AttributeError):return False

def event_valid(e,ch,root):
 try:
  actual,_,_=context(root);assert J(e)==J(event_record(root))and J(ch)==J(actual)
  h=json.loads((Path(root)/'corpus/songshu/045-wyd1739-liucui-titles.json').read_bytes())['holdings'];by={x['id']:x for x in h};assert holding_valid(by[e['holding_id']],ch,by,root);return True
 except(KeyError,TypeError,ValueError,AssertionError,StopIteration,OSError,AttributeError):return False

def holding_dispatch_valid(h,ch,root):
 try:
  hs=json.loads((Path(root)/'corpus/songshu/045-wyd1739-liucui-titles.json').read_bytes())['holdings'];return holding_valid(h,ch,{x['id']:x for x in hs},root)
 except(KeyError,TypeError,ValueError,OSError,AttributeError):return False

def proposal_valid(q,ch,root):
 try:
  actual,_,_=context(root);return J(ch)==J(actual)and J(q)==J(proposal(actual))
 except(KeyError,TypeError,ValueError,AssertionError,OSError,AttributeError,StopIteration):return False

_HOLDING_IDS=frozenset('th-song045-wyd-'+s for s in ('cui-xian','cui-she','cui-jianan','kuang-jianan','chen-jianan','cui-anbei','sun-taichang'))
def holding_applies(h):
 return isinstance(h,dict)and(isinstance(h.get('id'),str)and h['id']in _HOLDING_IDS or isinstance(h.get('source_career_role'),dict)and h['source_career_role'].get('kind')=='fixed_wyd045_noble_sequence')
def death_applies(e):
 return isinstance(e,dict)and(e.get('id')in ('le-song045-wyd-kuangzhi','le-song045-wyd-chen')or isinstance(e.get('source_wyd045_noble_death_scope'),dict)and e['source_wyd045_noble_death_scope'].get('kind')=='fixed_wyd045_heir_death')
def event_applies(e):
 return isinstance(e,dict)and(e.get('id')=='event-song045-wyd-chen-state-abolition'or isinstance(e.get('source_clause_binding'),dict)and e['source_clause_binding'].get('kind')=='fixed_wyd045_noble_line_abolition')
def proposal_applies(q):
 if not isinstance(q,dict):return False
 es=q.get('evidence',[])
 return q.get('id')=='proposal-song045-wyd-zhenzhi-nonassumption'or isinstance(es,list)and any(isinstance(e,dict)and e.get('chapter_id')==CID for e in es)
