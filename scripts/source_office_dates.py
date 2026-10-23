"""Exact source-role dates from named eras and separately bounded archived events.
No identity whitelist. In-office observations do not create tenure boundaries.
"""
import copy,hashlib,re,json
from pathlib import Path,PurePosixPath
ROOT=Path(__file__).resolve().parents[1]
def project(s):
 return re.sub(r'\s|¶|[()]','',re.sub(r'<pb:[^>]+>','',s))
def span(t,a):
 assert set(a)=={'start','end','quote'}and type(a['start'])is int and type(a['end'])is int and 0<=a['start']<a['end']<=len(t)and t[a['start']:a['end']]==a['quote'];return a['quote']
def office():
 try:from scripts import source_office_reports as o
 except ImportError:import source_office_reports as o
 return o
def archive(r,root):
 p=PurePosixPath(r['path']);assert not p.is_absolute()and'..'not in p.parts and r['path'].startswith('source-evidence/source-office-event-dates/primary/')
 q=(Path(root or ROOT)/str(p)).resolve();assert Path(root or ROOT).resolve()in q.parents
 raw=q.read_bytes();assert hashlib.sha256(raw).hexdigest()==r['sha256']and re.fullmatch('[0-9a-f]{40}',r['revision'])and r['projection']=='all_layers_drop_layout_wrappers_v1'
 assert r['url']=='https://raw.githubusercontent.com/kanripo/KR2a0012/'+r['revision']+'/'+r['file']and Path(r['path']).name==r['file']
 t=project(raw.decode());context=span(t,r['context']);assert all(r['context']['start']<=a['start']<a['end']<=r['context']['end']for a in r['anchors'].values());quotes={k:span(t,a)for k,a in r['anchors'].items()};return t,context,quotes
def phase(v,h,expression):
 try:from scripts.civil_era_ranges import civil_era_range_errors
 except ImportError:from civil_era_ranges import civil_era_range_errors
 assert not civil_era_range_errors(v,h['evidence'],expression)
def common(h,ch,b):
 o=office();e,=h['evidence'];p=o.paragraph(ch,e);assert h['human_reviewed']is False and b['status']=='contextual_provisional'and b['human_reviewed']is False and b['holding_id']==h['id']and b['person_id']==h['person_id']and b['paragraph_sha256']==hashlib.sha256(p['text'].encode()).hexdigest()and b['source_revision']==ch['source']['revision_id']
 a,=h['attestations'];m=o.mention(p,a['person_mention_id']);assert m['person_id']==h['person_id']and b['source_term']
 sr=h['source_office_role'];assert b['source_term']==sr.get('scope_anchor',{}).get('surface',h['title'])
 if b['kind']!='source_named_era_phase':
  extra={'native_roles','proofs','calendar_reference'}|({'era_phase_range','joint_inference'}if b['kind']=='phase_and_in_office_upper'else{'local_battle_context'}if b['kind']=='battle_in_office_observation'else set());assert set(b)=={'kind','holding_id','person_id','paragraph_sha256','source_revision','source_term','status','human_reviewed'}|extra
 return p

def exact(v,h,b,year,proof,role):
 assert type(v.get('year'))is int and v['year']==v['era_year']==year and v['era']=='CE'and v['calendar']=='chinese_civil'and v['precision']=='year'and v['year_numbering']=='astronomical'and v['status']=='editorial_provisional'and v['human_reviewed']is False and v['evidence']==h['evidence']and v['original_quote']==h['evidence'][0]['quote']and v['rationale']and v['reviewer']
 assert not any(k in v for k in ('month','day','lunar_month','lunar_day','source_date_parts'))
 assert v['regnal_year_mapping']=={'kind':'source_office_event_bridge','holding_id':h['id'],'role':role}
 a=proof['anchors'];assert v['basis']=={'kind':'parallel_event','source_event_quote':b['source_term'],'reference_url':proof['url'],'reference_event_quote':a['event']['quote'],'reference_year_quote':a['year']['quote']}
 assert v['references']==[{'url':proof['url'],'quote':a['event']['quote'],'scope':'received_parallel_event'},{'url':proof['url'],'quote':a['year']['quote'],'scope':'received_regnal_year_attestation'}]

def names(ch,p,b,kind):
 o=office();res={}
 for key,operand in b['native_roles'].items():
  pp=next(x for x in ch['paragraphs']if x['id']==operand['paragraph_id']);m=o.mention(pp,operand['mention_id']);res[key]=m
 assert res['subject']['person_id']==b['person_id']
 if kind in('dead_predecessor_successor','phase_and_in_office_upper'):
  assert res['predecessor_full']['person_id']==res['predecessor']['person_id']!=res['subject']['person_id']
 return res

def external(b,h,ch,p,root):
 kind=b['kind'];rs=names(ch,p,b,kind);proofs=b['proofs'];data=[archive(r,root)for r in proofs];assert all(r['revision']==b['source_revision']for r in proofs)
 if kind in('dead_predecessor_successor','battle_in_office_observation'):
  ann=data[-1];q=ann[2];s=rs['subject_full']['surface'];assert rs['subject_full']['person_id']==h['person_id']and len(s)>1
  assert q['year'].startswith('二年春正月')and q['era']=='正元元年'and proofs[-1]['anchors']['era']['start']<proofs[-1]['anchors']['year']['start']<proofs[-1]['anchors']['event']['start']
  assert q['event'].startswith('八月')and '安西將軍與征西將軍'+s+'并力拒維'in q['event']and q['actor']==s and q['title']=='征西將軍'
  assert q['opponent']==rs['opponent']['surface']and q['defeated']==rs['defeated']['surface']and ('蜀大將軍'+q['opponent']+'寇狄道')in q['event']and ('雍州刺史'+q['defeated']+'與戰洮西')in q['event']
  # This is the full same-year annal, not a later year's event selected by proximity.
  assert proofs[-1]['anchors']['event']['end']<=ann[0].index('甘露元年',proofs[-1]['anchors']['year']['end']) and proofs[-1]['context']['end']==ann[0].index('甘露元年',proofs[-1]['anchors']['year']['end'])and proofs[-1]['context']['start']==proofs[-1]['anchors']['era']['start']
  for key in ('actor','title','opponent','defeated'):assert proofs[-1]['anchors']['event']['start']<=proofs[-1]['anchors'][key]['start']<proofs[-1]['anchors'][key]['end']<=proofs[-1]['anchors']['event']['end']
  assert b['calendar_reference']=={'url':'https://dict.revised.moe.edu.tw/appendix.jsp?ID=3&page=1','era_name':'正元','first':254,'last':256}and 254+2-1==255
  if kind=='dead_predecessor_successor':
   own=h['source_office_role'];assert own['rule']=='dead_predecessor_replacement'and own['slot']in('office','credential','command')and own['roles']['predecessor']==rs['predecessor']['id']and own['roles']['subject']==rs['subject']['id']
   pred=rs['predecessor_full']['surface'];d=data[0][2];assert d['head'].startswith(pred+'字')and d['death'].startswith('正元二年薨追贈')and rs['predecessor']['surface']+'薨'+rs['subject']['surface']+'代為'==b['source_term'][:len(rs['predecessor']['surface'])+len(rs['subject']['surface'])+3]
   assert data[-1][2]['death_actor']==pred and pred+'薨'in data[-1][2]['death']
  else:
   assert h['source_office_role']['kind']=='literal_person_title_mention'and h['mode']=='attestation'and h['title']=='征西'
   context=office().anchor(p,b['local_battle_context']);assert all(context['start']<=rs[k]['start']<rs[k]['end']<=context['end']for k in('opponent','defeated'))and '戰大敗'in context['surface']and '還保狄道城'in context['surface']
  return 255,proofs[-1]
 if kind=='phase_and_in_office_upper':
  role=h['source_office_role'];assert role['rule']=='recalled_replacement_offices'and role['slot']=='office2';v=b['era_phase_range'];phase(v,h,'嘉平初');assert v['earliest']['year']==249 and v['latest']['year']==254
  _,context,q=data[0];s=rs['subject_full']['surface'];pred=rs['predecessor_full']['surface'];assert rs['subject_full']['person_id']==h['person_id']and q['head'].startswith(pred+'字')and q['year']=='嘉平元年'and q['event'].startswith('嘉平元年遷征西將軍都督雍涼諸軍事是歲與'+h['title']+s+'協策降蜀牙門將句安等於翅上')and q['actor']==s and q['title']==h['title']
  assert b['joint_inference']=={'lower_bound':'source_named_era_start','upper_bound':'same_campaign_in_office_attestation','result_year':249,'not_equating_phase_with_year_one':True}
  assert b['calendar_reference']=={'url':'https://dict.revised.moe.edu.tw/appendix.jsp?ID=3&page=1','era_name':'嘉平','first':249,'last':254}
  for key in('actor','title'):assert proofs[0]['anchors']['event']['start']<=proofs[0]['anchors'][key]['start']<proofs[0]['anchors'][key]['end']<=proofs[0]['anchors']['event']['end']
  return 249,proofs[0]
 raise AssertionError('Unknown event bridge')

def valid(h,ch,holdings,root=None):
 try:
  b=h['source_office_date_binding'];p=common(h,ch,b);base=copy.deepcopy(h);del base['source_office_date_binding']
  for a in base['attestations']:a.pop('normalized_date',None)
  base['effective_period']['start'].pop('normalized_date',None);base['effective_period']['start'].pop('normalized_date_range',None)
  assert office().holding_role_valid(base,ch,holdings,root)
  extra=set()if b['kind']=='battle_in_office_observation'else{'normalized_date_range'}if b['kind']=='source_named_era_phase'else{'normalized_date'}
  assert set(h['effective_period']['start'])==set(base['effective_period']['start'])|extra
  assert all(set(a)==set(ba)|({'normalized_date'}if b['kind']=='battle_in_office_observation'and i==0 else set())for i,(a,ba)in enumerate(zip(h['attestations'],base['attestations'])))
  if b['kind']=='source_named_era_phase':
   sr=h['source_office_role'];allowed={('opening_office_series','office1'):'青龍中',('opening_office_series','office2'):'正始中',('posthumous_and_successor_series','new_rank'):'咸熙中'};expr=allowed[(sr['rule'],sr['slot'])];v=h['effective_period']['start']['normalized_date_range'];phase(v,h,expr);assert b['source_term']==sr['scope_anchor']['surface']and set(b)=={'kind','holding_id','person_id','paragraph_sha256','source_revision','source_term','status','human_reviewed'};return True
  year,proof=external(b,h,ch,p,root);role='attestation'if b['kind']=='battle_in_office_observation'else'start';v=h['attestations'][0]['normalized_date']if role=='attestation'else h['effective_period']['start']['normalized_date'];exact(v,h,b,year,proof,role)
  assert h['effective_period']['end']==base['effective_period']['end']
  return True
 except(KeyError,TypeError,ValueError,AssertionError,StopIteration,OSError):return False

def normalized_valid(date,holding,role,chapters,root=None):
 try:
  assert role in('start','attestation');ch=chapters[holding['evidence'][0]['chapter_id']];v=holding['attestations'][0].get('normalized_date')if role=='attestation'else holding['effective_period']['start'].get('normalized_date');
  hs={}
  for path in (Path(root or ROOT)/'corpus').rglob('*.json'):
   record=json.loads(path.read_text())
   if isinstance(record,dict):hs.update({h['id']:h for h in record.get('holdings',[])})
  return date==v and valid(holding,ch,hs,root)
 except(KeyError,TypeError,ValueError,AssertionError,StopIteration):return False

def detail_valid(d,ch,holdings,root=None):
 try:
  base=copy.deepcopy(d);v=base.pop('date_observation');assert office().detail_valid(base,ch,holdings,root)
  assert v['kind']=='source_duty_event_observation_window'and v['duration']is False and v['tenure_boundary']is False and v['human_reviewed']is False and v['calendar']=='chinese_civil'and v['precision']=='year_range'and v['earliest']==257 and v['latest']==258 and v['status']=='contextual_provisional'and v['record_id']==d['id']and v['person_id']==d['person_id']
  assert d['source_detail_pattern']['kind']=='named_duty';o=office();p=o.paragraph(ch,d['evidence'][0]);a=o.anchor(p,v['local_context']);rs={k:o.mention(p,x)for k,x in v['native_roles'].items()};assert rs['subject']['person_id']==d['person_id']and a['surface']==rs['rebel']['surface']+'作亂壽春'+rs['commander']['surface']+'率六軍軍丘頭'+rs['subject']['surface']+'總署行臺'
  assert rs['rebel']['start']==a['start']and rs['commander']['start']==rs['rebel']['end']+4 and rs['subject']['end']==a['end']-4
  assert v['proof']['revision']==ch['source']['revision_id']
  t,context,q=archive(v['proof'],root);r=rs['rebel']['surface'];comm=rs['commander']['surface'];assert q['era']=='甘露元年'and q['year2'].startswith('二年春二月')and q['year3'].startswith('三年春二月')and q['rebellion']==r+'不就徵發兵反殺揚州刺史樂綝'and q['end']=='三年春二月大將軍'+comm+'陷壽春城斬'+r and q['qiutou'].startswith('大將軍親摠六戎營據丘頭')
  assert v['calendar_reference']=={'url':'https://dict.revised.moe.edu.tw/appendix.jsp?ID=3&page=1','era_name':'甘露','first':256,'last':259}and v['proof']['anchors']['era']['start']<v['proof']['anchors']['year2']['start']<v['proof']['anchors']['rebellion']['start']<v['proof']['anchors']['year3']['start']
  return True
 except(KeyError,TypeError,ValueError,AssertionError,StopIteration,OSError):return False
