# coding: utf-8
"""Finite fixed-witness biography role slots, with no person-ID/name whitelist.
The reviewed grammar covers the complete source unit. Role indexes address actual
person mentions; a slot cannot choose a different same-paragraph recipient.
"""
from pathlib import Path
import json,hashlib,re,copy
KIND='fixed_complete_family_career'
RECIPE_PATH=Path(__file__).with_name('fixed_complete_family_career.json')
ROOT=Path(__file__).resolve().parents[1]
def strict_equal(a,b):
 if type(a)is not type(b):return False
 if isinstance(a,dict):return a.keys()==b.keys()and all(strict_equal(a[k],b[k])for k in a)
 if isinstance(a,list):return len(a)==len(b)and all(strict_equal(x,y)for x,y in zip(a,b))
 return a==b

def grammar(ch,root):
 try:from scripts.fixed_wikisource_units import source_errors
 except ImportError:from fixed_wikisource_units import source_errors
 assert isinstance(ch.get('annotation',{}).get('fixed_wikisource_unit_ref'),str)and ch['annotation']['fixed_wikisource_unit_ref']and not source_errors(ch,root)
 r=json.loads(RECIPE_PATH.read_text());assert ch['source']['revision_id']==r['revision']and ch['source']['raw_file_sha256']==r['raw_sha256']and len(ch['paragraphs'])==len(r['paragraphs'])
 assert ch.get('annotation',{}).get('fixed_complete_family_career_ref')==dict(kind=KIND,source_revision=r['revision'],record_prefix=r['record_prefix'])
 roles=[]
 for p,pattern in zip(ch['paragraphs'],r['paragraphs']):
  ms=[m for m in p['mentions']if m['kind']=='person'];pos=0;used=[]
  for piece in re.split(r'(<r[0-9]+>)',pattern):
   if piece.startswith('<r')and piece.endswith('>'):
    index=int(piece[2:-1]);m=ms[index];assert m['start']==pos and p['text'][pos:m['end']]==m['surface'];pos=m['end'];used.append(index)
   else:assert p['text'].startswith(piece,pos);pos+=len(piece)
  assert pos==len(p['text'])and used==list(range(len(ms)));roles.append(ms)
 return r,roles

def source_date(expression,evidence,s):
 era=expression[:2];start,end={'太康':(280,289),'元康':(291,299),'永興':(304,306),'咸寧':(275,280)}[era]
 ref=dict(title='教育部《重編國語辭典修訂本》中國歷代年號表',url='https://dict.revised.moe.edu.tw/appendix.jsp?ID=3&page=2',quote=era,scope='modern_era_year_equivalence_only',columns=dict(dynasty='西晉',era_name=era,first_year=str(start),last_year=str(end)),accessed_on='2026-10-22',image_verified=False)
 v=dict(year_numbering='astronomical',calendar='chinese_civil',status='editorial_provisional',source_expression=expression,original_quote=evidence[0]['quote'],evidence=evidence,references=[ref],reviewer='Codex（AI代理）',human_reviewed=False)
 if 'ce_year'in s:
  year=s['ce_year'];v.update(era='CE',era_year=year,year=year,precision='year',regnal_year_mapping=dict(kind='ce_regnal_era_span',reference_index=0,start_ce_year=start,end_ce_year=end,regnal_year=year-start+1,source_number='三',era_name=era),rationale='按實讀官方年號表換算中國曆年；四月原詞保留，不計西曆月日、不由卒年推生年或任終。');return 'normalized_date',v
 a,b=s['era_range'];assert(a,b)==(start,end)
 v.update(earliest=dict(era='CE',era_year=a,year=a),latest=dict(era='CE',era_year=b,year=b),precision='year_range',basis='within_named_era',source_stage=expression[-1],era_span_mapping=dict(kind='ce_regnal_era_span',reference_index=0,era_name=era,source_era_name=era,polity_source_name='西晉',start_ce_year=a,end_ce_year=b),rationale='初／中原詞不改；整年號只給最寬外界，不宣稱元年、精確中年或完整持職期間。');return 'normalized_date_range',v

def make(ch,r,roles,s):
 i=s['paragraph_index'];j=s['recipient_paragraph_index'];p=ch['paragraphs'][i];m=roles[j][s['recipient_role']];a=dict(paragraph_id=p['id'],**s['source_anchor']);assert p['text'][a['start']:a['end']]==a['surface']
 if s.get('inside_recipient'):assert i==j and m['start']<=a['start']<a['end']<=m['end']
 evidence=dict(work_id=ch['work_id'],book_id=ch['book_id'],source_id=ch['source_id'],chapter_id=ch['id'],paragraph_id=p['id'],quote=p['text'],person_mention_id=m['id'])
 if i!=j:
  assert j+1==i
  evidence['context']=dict(kind='previous_paragraph_subject',paragraph_id=ch['paragraphs'][j]['id'],person_mention_id=m['id'],quote=ch['paragraphs'][j]['text'])
 ev=[evidence];cat=s['category'];prefix={'holding':'th','life':'le','address':'ad','detail':'bd','proposal':'tp','age':'age'}[cat];sid=prefix+'-'+r['record_prefix']+'-'+s['slot_id']
 bind=dict(kind=KIND,slot=s['slot_id'],paragraph_id=p['id'],source_revision=ch['source']['revision_id'],paragraph_sha256=hashlib.sha256(p['text'].encode()).hexdigest(),person_mention_id=m['id'])
 v=dict(id=sid,person_id=m['person_id'],status='source_attested',evidence=ev,reviewer='Codex（AI代理）',human_reviewed=False,model=None,interpretation_note=s.get('note','依完整收到段落的明示受任者／原詞；未知年月、任終、生年與未名人物不補。'))
 expr=s.get('date_expression');date={}if not expr else dict([source_date(expr,ev,s)])
 if cat=='holding':
  mode=s['mode'];unknown=dict(status='unknown',date_expression=None,evidence=[]);at=dict(id=sid+':a001',**a,person_mention_id=m['id'],usage='narrative',date_expression=expr if mode=='attestation'else None)
  if i!=j:at['context']=copy.deepcopy(evidence['context'])
  if mode=='attestation':at.update(date)
  beginning=copy.deepcopy(unknown)if mode=='attestation'else dict(status='source_event',event_type=mode,date_expression=expr,evidence=ev,**date)
  v.update(title=a['surface'],kind=s['kind'],mode=mode,appointment_role=s.get('appointment_role','source_report'if mode=='attestation'else mode),source_career_role=bind,attestations=[at],effective_period=dict(start=beginning,end=copy.deepcopy(unknown)))
  if mode=='posthumous_grant':v['posthumous_basis']=dict(source_term=p['text'],evidence=ev)
  if mode=='posthumous_naming':
   death=next(x for x in('薨','卒','亡','死')if x in p['text']);v['naming_basis']=dict(source_term=p['text'],death_term=death,evidence=ev)
 elif cat=='life':
  v.update(event_type=s['event_type'],source_term=a['surface'],source_anchor=a,date_expression=expr,fixed_family_career_binding=bind,**date)
  if 'source_month_expression'in s:
   assert expr+s['source_month_expression']in p['text']
   try:from scripts.chinese_civil_years import numeral
   except ImportError:from chinese_civil_years import numeral
   assert s['source_month_expression'].endswith('月')and numeral(s['source_month_expression'][:-1])==s['source_month_number']and 1<=s['source_month_number']<=12
   v.update(source_month_expression=s['source_month_expression'],source_month_number=s['source_month_number'])
 elif cat=='address':
  v.update(relation=s['relation'],place=dict(source_name=s['place'],place_id=None,modern_identification=None),source_term=a['surface'],source_anchor=a,date_expression=None,fixed_family_career_binding=bind)
  if s['relation']=='source_locality_designation':v['qualifiers']=dict(designation_kind='geographical_person_reference',origin_or_residence=None)
  if s['relation']=='service_location':v['qualifiers']=dict(source_position='鎮'if'鎮'in a['surface']else'屯')
 elif cat=='detail':
  values=copy.deepcopy(s['values'])
  if values.get('source_number')and isinstance(values.get('value',values.get('count')),int):
   try:from scripts.biographical_appointment_sequence import integer as numeral
   except ImportError:from biographical_appointment_sequence import integer as numeral
   assert values['source_number']in a['surface']and numeral(values['source_number'])==values.get('value',values.get('count'))
  for key,x in s.get('value_person_roles',{}).items():
   assert key.endswith('_person_id')and key in values and values[key]is None
   values[key]=roles[x['paragraph_index']][x['role']]['person_id']
  v.update(kind=s['kind'],source_term=a['surface'],source_anchor=a,date_expression=expr,source_revision=ch['source']['revision_id'],paragraph_sha256=bind['paragraph_sha256'],values=values,source_career_role=bind,**date)
 elif cat=='proposal':
  v.update(title=a['surface'],kind=s.get('holding_kind',s.get('kind','office')),proposal_kind=s['proposal_kind'],outcome='not_reported'if s['proposal_kind']=='appointment_service_unreported'else'not_assumed'if s['proposal_kind']else'not_enacted',effective_service_attested=False,status='contextual_provisional',person_mention_id=m['id'],role_anchor=a,date_expression=None,source_appointment_context=bind)
  if 'non_assumption_paragraph'in s:
   q=ch['paragraphs'][s['non_assumption_paragraph']-1];term=s['non_assumption_term'];assert q['text'].count(term)==1;lo=q['text'].index(term);v['non_assumption_anchor']=dict(paragraph_id=q['id'],start=lo,end=lo+len(term),surface=term)
  v['source_outcome']=s.get('notice_outcome','source_non_assumption')
 elif cat=='age':
  context=dict(kind=s['age_context'])
  if s['age_context']=='at_death':
   ls,=[x for x in r['slots']if x['category']=='life'and x['event_type']=='death'and x['paragraph_index']==i and x['recipient_role']==s['recipient_role']and x['recipient_paragraph_index']==j];context['life_event_id']='le-'+r['record_prefix']+'-'+ls['slot_id']
  v.update(source_number=s['source_number'],source_term=a['surface'],source_anchor=a,value=s['value'],unit='source_age_years',counting='unspecified_source_age',birth_year=None,age_context=context,reporting_status='direct_report',date_expression=expr,fixed_family_career_binding=bind,**date)
 else:raise AssertionError('unknown finite slot category')
 return v

def records(ch,root=ROOT):
 r,roles=grammar(ch,root);return [make(ch,r,roles,s)for s in r['slots']]

def valid(v,ch,root=ROOT):
 try:
  bind=next(v[k]for k in('source_career_role','source_appointment_context','fixed_family_career_binding')if k in v);assert bind['kind']==KIND
  r,roles=grammar(ch,root);s,=[s for s in r['slots']if s['slot_id']==bind['slot']];return strict_equal(v,make(ch,r,roles,s))
 except(AssertionError,KeyError,ValueError,TypeError,IndexError,StopIteration,AttributeError,OSError):return False

def errors(root,rows):
 out=[];chs={x['id']:x for x in rows if x.get('record_type')=='marked_chapter'};actual={}
 def take(cid,v):
  if any(isinstance(v.get(k),dict)and v[k].get('kind')==KIND for k in('source_career_role','source_appointment_context','fixed_family_career_binding')):actual.setdefault(cid,[]).append(v)
 for row in rows:
  for key in('holdings','events','assertions','records'):
   for v in row.get(key,[]):take(row.get('chapter_id'),v)
 for ch in chs.values():
  for key in('title_proposals','age_assertions'):
   for v in ch.get('annotation',{}).get(key,[]):take(ch['id'],v)
 active={cid for cid,ch in chs.items()if ch.get('annotation',{}).get('fixed_complete_family_career_ref',{}).get('kind')==KIND}
 for cid in set(actual)-active:out.append('固定傳記typed slots缺完整來源批次界線:'+str(cid))
 for cid in active:
  try:
   want=records(chs[cid],root);got=actual.get(cid,[]);wd={v['id']:v for v in want}
   assert len(got)==len(want)and len({v['id']for v in got})==len(got)
   for v in got:
    if not strict_equal(v,wd.get(v.get('id'))):out.append('完整固定傳記typed角色／原詞／紀年不符:'+str(v.get('id')))
  except(AssertionError,KeyError,ValueError,TypeError,IndexError,StopIteration,AttributeError,OSError):out.append('完整固定傳記本批typed slots不得漏記、重複或更換來源角色')
 return out
