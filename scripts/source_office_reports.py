"""Explicit source office reports, duties, aggregate grants and unnamed successions.

No person-name/ID whitelist; all source roles are stored exact-position operands.
"""
import hashlib,re

def paragraph(ch,e):
 assert all(e[k]==ch[k]for k in ('work_id','book_id','source_id'))and e['chapter_id']==ch['id']
 p=next(p for p in ch['paragraphs']if p['id']==e['paragraph_id']);assert e['quote']==p['text'];return p

def anchor(p,a):
 assert set(a)=={'paragraph_id','start','end','surface'}and a['paragraph_id']==p['id']and type(a['start'])is int and type(a['end'])is int and 0<=a['start']<a['end']<=len(p['text'])and p['text'][a['start']:a['end']]==a['surface'];return a

def mention(p,mid):
 m=next(m for m in p['mentions']if m['id']==mid);assert m['kind']=='person'and p['text'][m['start']:m['end']]==m['surface'];return m

def qualified_office_valid(h,ch):
 try:
  q=h['source_qualification'];e,=h['evidence'];p=paragraph(ch,e);a,=h['attestations'];subject=mention(p,a['person_mention_id']);w=next(m for m in p['mentions']if m['id']==q['reported_work_mention_id'])
  ce=q['objection_evidence'];cp=paragraph(ch,ce);critic=mention(cp,q['commentator_mention_id']);cm=mention(cp,ce['person_mention_id']);author=mention(cp,q['objection_author_mention_id']);ca=anchor(cp,q['objection_clause_anchor'])
  assert q['kind']=='reported_office_challenged_by_commentary'and q['preferred_historical_office_assertion_id']is None and q['human_reviewed']is False and q['interpretation_note']
  assert h['kind']=='office'and h['mode']=='attestation'and subject['person_id']==cm['person_id']==h['person_id']and w['kind']=='work'and w['work_id']==q['reported_work_id']
  assert a['start']==subject['start']and subject['surface'].startswith(h['title'])and a['end']==a['start']+len(h['title'])and a['surface']==h['title']
  assert ca['surface']=='本傳'+cm['surface']+'不為'+h['title']+'未詳'+author['surface']+'所由知之'and ca['start']<=cm['start']<cm['end']<=ca['end']and ca['start']<=author['start']<author['end']<=ca['end']
  assert p['text'].startswith(author['surface']+w['surface']+'曰')and critic['start']==0 and cp['text'].startswith(critic['surface']+'案'+ca['surface'])
  unknown={'status':'unknown','date_expression':None,'evidence':[]};assert h['effective_period']=={'start':unknown,'end':unknown}
  return True
 except(KeyError,TypeError,ValueError,AssertionError,StopIteration):return False

def detail_valid(d,ch,holdings,root=None):
 if 'date_observation' in d:
  try:from scripts.source_office_dates import detail_valid as dated_valid
  except ImportError:from source_office_dates import detail_valid as dated_valid
  return dated_valid(d,ch,holdings,root)

 try:
  e,=d['evidence'];p=paragraph(ch,e);t=p['text'];m=mention(p,e['person_mention_id']);b=d['source_detail_pattern'];scope=anchor(p,b['scope_anchor']);a=anchor(p,d['source_anchor']);v=d['values'];f=b['fields'];text=scope['surface']
  assert d['person_id']==m['person_id']and b['subject_mention_id']==m['id']and d['status']=='source_attested'and d['human_reviewed']is False and d['date_expression']is None and d['source_term']==a['surface']and scope['start']<=a['start']<a['end']<=scope['end']and scope['start']<=m['start']<m['end']<=scope['end']
  assert d['source_revision']==ch['source']['revision_id']and d['paragraph_sha256']==hashlib.sha256(t.encode()).hexdigest()
  for x in f.values():anchor(p,x);assert scope['start']<=x['start']<x['end']<=scope['end']
  # Frames reconstruct the whole local clause, including subject, not nearest-name matching.
  if b['kind']=='appointment_selection_duty':
   assert set(f)=={'office','additional1','additional2'}and text=='後徵'+m['surface']+'為'+f['office']['surface']+'典選舉加'+f['additional1']['surface']+f['additional2']['surface']and m['start']==scope['start']+2
   assert d['kind']=='official_duty'and a['surface']=='典選舉'and v=={'duty_code':'personnel_selection','office_source_name':f['office']['surface'],'office_title_holding_id':v.get('office_title_holding_id')}
   holding=holdings[v['office_title_holding_id']];assert holding['person_id']==d['person_id']and holding['title']==f['office']['surface']and any(x['paragraph_id']==p['id']for x in holding['evidence'])
  elif b['kind']=='named_duty':
   assert not f and text==m['surface']+'總署行臺'and m['start']==scope['start']and d['kind']=='official_duty'and a['surface']=='總署行臺'and v=={'duty_code':'general_administration_of_mobile_secretariat','organ_source_name':'行臺','office_title':None}
  elif b['kind']=='named_command_supervision':
   assert set(f)=={'subordinate_group'}and text=='詔'+f['subordinate_group']['surface']+'受'+m['surface']+'節度'and m['end']==scope['end']-2 and m['start']==f['subordinate_group']['end']+1
   assert d['kind']=='command_authority'and a==scope and v=={'authority_code':'command_over_source_group','subordinate_group_source_name':f['subordinate_group']['surface'],'subordinate_group_person_ids':[],'new_office_appointment':False}
  elif b['kind']=='aggregate_fief_and_family_grants':
   assert set(f)=={'increase_number','unit','count1','rank1','count2','rank2'}
   n=lambda key:integer(f[key]['surface'])
   assert text==m['surface']+'前後以功增邑'+f['increase_number']['surface']+f['unit']['surface']+'賜子弟'+f['count1']['surface']+'人'+f['rank1']['surface']+f['count2']['surface']+'人'+f['rank2']['surface']and m['start']==scope['start']
   if d['kind']=='fief_household_count':assert a['surface']=='增邑'+f['increase_number']['surface']+f['unit']['surface']and v=={'increase':n('increase_number'),'increase_source_number':f['increase_number']['surface'],'aggregation':'cumulative_across_unspecified_awards','total':None,'unit_source_name':f['unit']['surface'],'actual_revenue':None}
   else:assert d['kind']=='unnamed_family_title_grants'and a['surface']=='賜子弟'+f['count1']['surface']+'人'+f['rank1']['surface']+f['count2']['surface']+'人'+f['rank2']['surface']and v=={'recipient_group_source_term':'子弟','recipient_person_ids':[],'biological_children_only':False,'grants':[{'source_rank':f['rank1']['surface'],'recipient_count':n('count1'),'source_number':f['count1']['surface']},{'source_rank':f['rank2']['surface'],'recipient_count':n('count2'),'source_number':f['count2']['surface']}]}
  else:return False
  frames={
   'appointment_selection_duty':[('L','後徵'),('M',None),('L','為'),('F','office'),('L','典選舉加'),('F','additional1'),('F','additional2')],
   'named_duty':[('M',None),('L','總署行臺')],
   'named_command_supervision':[('L','詔'),('F','subordinate_group'),('L','受'),('M',None),('L','節度')],
   'aggregate_fief_and_family_grants':[('M',None),('L','前後以功增邑'),('F','increase_number'),('F','unit'),('L','賜子弟'),('F','count1'),('L','人'),('F','rank1'),('F','count2'),('L','人'),('F','rank2')]}
  cursor=scope['start']
  for typ,key in frames[b['kind']]:
   x=m if typ=='M'else f[key]if typ=='F'else None
   if x:assert x['start']==cursor;cursor=x['end']
   else:assert t.startswith(key,cursor);cursor+=len(key)
  assert cursor==scope['end']
  # All person slots in the local clause must be this subject (not a hidden other recipient).
  assert all(x['person_id']==m['person_id']for x in p['mentions']if x.get('kind')=='person'and scope['start']<=x['start']<scope['end'])
  return True
 except(KeyError,TypeError,ValueError,AssertionError,StopIteration):return False

def integer(s):
 try:
  from scripts.biographical_appointment_sequence import integer as parse
 except ImportError:
  from biographical_appointment_sequence import integer as parse
 n=parse(s);assert n>0;return n

def succession_valid(e,paragraphs):
 try:
  assert e['status']=='source_attested'and set(e)=={'id','person_id','event_type','status','date_expression','source_term','title','holding_id','source_clause_binding','evidence','interpretation_note','reviewer','human_reviewed','model','mode','predecessor_person_id'}
  cid,p=paragraphs[e['evidence'][0]['paragraph_id']];ev,=e['evidence'];b=e['source_clause_binding'];a=anchor(p,b['succession_anchor']);t=p['text'];roles={k:mention(p,v)for k,v in b['roles'].items()}
  assert ev['chapter_id']==cid and ev['quote']==t and e['event_type']=='noble_title_succession'and e['mode']=='accession'and e['title']is None and e['holding_id']is None and e['date_expression']is None and 'normalized_date'not in e and e['human_reviewed']is False and e['source_term']==a['surface']
  if b['kind']=='biographical_head_named_son_succession':
   head,heir=roles['predecessor'],roles['heir'];assert set(roles)=={'predecessor','heir'}and head['start']==0 and t[head['end']:].startswith('字')and a['surface']=='子'+heir['surface']+'嗣'and heir['start']==a['start']+1 and heir['end']==a['end']-1
   context=anchor(p,b['death_succession_context_anchor']);resumed=mention(p,b['resumed_predecessor_mention_id']);assert resumed['person_id']==head['person_id']and context['start']==resumed['start']and context['end']==a['end']
   before=t[resumed['end']:a['start']];match=re.fullmatch(r'([^曰云詔「」『』\n]{0,120}?)(薨|卒|死)(?:追贈[^曰云詔「」『』薨卒死]{1,12})?(?:諡曰[^曰云詔「」『』薨卒死]{1,8})?',before);assert match and not re.search(r'(未|不|欲|將|當|議|請|可|宜|應)$',match.group(1))
   assert all(m['person_id']in(head['person_id'],heir['person_id'])for m in p['mentions']if m.get('kind')=='person'and context['start']<=m['start']<context['end'])
  elif b['kind']=='named_childless_brother_succession':
   first,repeat,heir=roles['predecessor'],roles['predecessor_repeat'],roles['heir'];assert set(roles)=={'predecessor','predecessor_repeat','heir'}and first['person_id']==repeat['person_id']and a['surface']=='子'+first['surface']+'嗣'+repeat['surface']+'薨無嗣弟'+heir['surface']+'紹封'and first['start']==a['start']+1 and repeat['start']==first['end']+1 and heir['start']==repeat['end']+4
   head=first
  else:return False
  assert e['predecessor_person_id']==head['person_id']!=heir['person_id']==e['person_id']and ev['person_mention_id']==heir['id']
  return True
 except(KeyError,TypeError,ValueError,AssertionError,StopIteration):return False

OFFICE_FRAMES={
 'opening_office_series':[('R','subject'),('L','字'),('F','courtesy'),('F','time1'),('L','除'),('F','office1'),('F','time2'),('L','徙'),('F','office2'),('L','為'),('F','office3'),('L','加'),('F','office4'),('F','credential'),('F','office5')],
 'recalled_replacement_offices':[('R','subject'),('L','皆挂之於壁不發其封及徵為'),('F','office1'),('L','悉以還之'),('F','time'),('L','代'),('R','predecessor'),('L','為'),('F','office2'),('L','加'),('F','office3')],
 'dead_predecessor_replacement':[('R','predecessor'),('L','薨'),('R','subject'),('L','代為'),('F','office'),('F','credential'),('F','command')],
 'later_selection_appointment':[('L','後徵'),('R','subject'),('L','為'),('F','office1'),('L','典選舉加'),('F','office2'),('F','office3')],
 'campaign_and_return_series':[('L','吳大將'),('R','opponent'),('L','出淮泗以'),('R','subject'),('L','為'),('F','office1'),('F','credential'),('F','command'),('L','詔徐州監軍已下受'),('R','subject_repeat'),('L','節度'),('R','opponent_repeat'),('L','退軍還轉為'),('F','office2')],
 'posthumous_and_successor_series':[('R','subject'),('L','前後以功增邑'),('F','increase'),('F','unit'),('L','賜子弟'),('F','count1'),('L','人'),('F','rank1'),('F','count2'),('L','人'),('F','rank2'),('F','death_date'),('L','薨追贈'),('F','post_office'),('L','諡曰'),('F','post_name'),('L','子'),('R','heir'),('L','嗣'),('R','heir_repeat'),('L','薨無嗣弟'),('R','successor'),('L','紹封'),('F','regrant_time'),('L','開建五等以'),('R','subject_repeat'),('L','著勲前朝改封'),('R','successor_repeat'),('L','為'),('F','new_rank')]}
OFFICE_SLOTS={
 'opening_office_series':{'office1':('office','grant','subject','青龍中'),'office2':('office','transfer','subject','正始中'),'office3':('office','grant','subject',None),'office4':('office','grant','subject',None),'credential':('honorific','grant','subject',None),'office5':('office','grant','subject',None)},
 'recalled_replacement_offices':{k:('office','grant','subject','嘉平初'if k=='office2'else None)for k in ('office1','office2','office3')},
 'dead_predecessor_replacement':{'office':('office','grant','subject',None),'credential':('honorific','grant','subject',None),'command':('office','grant','subject',None)},
 'later_selection_appointment':{k:('office','grant','subject',None)for k in ('office1','office2','office3')},
 'campaign_and_return_series':{'office1':('office','grant','subject',None),'credential':('honorific','grant','subject',None),'command':('office','grant','subject',None),'office2':('office','transfer','subject',None)},
 'posthumous_and_successor_series':{'post_office':('office','posthumous_grant','subject',None),'post_name':('honorific','posthumous_naming','subject',None),'new_rank':('noble_rank','transfer','successor','咸熙中')}}

def holding_role_valid(h,ch,holdings,root=None):
 if 'source_office_date_binding' in h:
  try:from scripts.source_office_dates import valid as dated_valid
  except ImportError:from source_office_dates import valid as dated_valid
  return dated_valid(h,ch,holdings,root)

 try:
  e,=h['evidence'];p=paragraph(ch,e);t=p['text'];b=h['source_office_role'];a,=h['attestations'];m=mention(p,a['person_mention_id']);assert m['person_id']==h['person_id']and b['human_reviewed']is False
  if b['kind']=='literal_person_title_mention':
   previous=holdings[b['same_stage_holding_id']];return h['kind']=='office'and h['appointment_role']=='narrative_short_office_reference'and h['effective_period']=={'start':{'status':'unknown','date_expression':None,'evidence':[]},'end':{'status':'unknown','date_expression':None,'evidence':[]}}and h['mode']=='attestation'and h['title']==m['surface']==a['surface']and a['start']==m['start']and a['end']==m['end']and previous['person_id']==h['person_id']and previous['title']==h['title']+'將軍'and previous['mode']=='grant'
  if b['kind']=='named_title_prefix':return h['kind']=='office'and h['effective_period']=={'start':{'status':'unknown','date_expression':None,'evidence':[]},'end':{'status':'unknown','date_expression':None,'evidence':[]}}and h['mode']=='attestation'and a['end']==m['start']and t[a['start']:m['start']]==h['title']and b['subject_mention_id']==m['id']
  assert b['kind']=='received_office_role_frame';scope=anchor(p,b['scope_anchor']);roles={k:mention(p,mid)for k,mid in b['roles'].items()};fields=b['fields'];cursor=scope['start'];usedr=set();usedf=set()
  for typ,key in OFFICE_FRAMES[b['rule']]:
   if typ=='L':assert t.startswith(key,cursor);cursor+=len(key)
   else:
    x=roles[key]if typ=='R'else anchor(p,fields[key]);assert x['start']==cursor;cursor=x['end'];(usedr if typ=='R'else usedf).add(key)
  assert cursor==scope['end']and usedr==set(roles)and usedf==set(fields)
  for k in ('subject','predecessor','opponent','heir','successor'):
   if k+'_repeat'in roles:assert roles[k]['person_id']==roles[k+'_repeat']['person_id']
  for k in ('predecessor','opponent','heir','successor'):
   if k in roles:assert roles[k]['person_id']!=roles['subject']['person_id']
  head=mention(p,b['biography_subject_mention_id']);assert head['start']==0 and t[head['end']:].startswith('字')and head['person_id']==roles['subject']['person_id']
  slot=b['slot'];kind,mode,recipient,date=OFFICE_SLOTS[b['rule']][slot];x=fields[slot]
  assert h['title']==x['surface']and h['kind']==kind and h['mode']==mode and h['person_id']==roles[recipient]['person_id']and m['person_id']==roles[recipient]['person_id']and scope['start']<=m['start']<m['end']<=scope['end']and a['start']==x['start']and a['end']==x['end']and a['surface']==x['surface']
  semantics={'opening_office_series':{'office1':'appointment','office2':'transfer','office3':'appointment','office4':'additional_office','credential':'military_authorization','office5':'appointment'},'recalled_replacement_offices':{'office1':'recruited_appointment','office2':'replacement_appointment','office3':'additional_office'},'dead_predecessor_replacement':{'office':'replacement_appointment','credential':'military_authorization','command':'military_command'},'later_selection_appointment':{'office1':'recruited_appointment','office2':'additional_office','office3':'additional_office'},'campaign_and_return_series':{'office1':'military_appointment','credential':'military_authorization','command':'military_command','office2':'transfer'},'posthumous_and_successor_series':{'post_office':'posthumous_office','post_name':'posthumous_name','new_rank':'noble_rank_change'}}
  assert h['appointment_role']==semantics[b['rule']][slot]and h['effective_period']['start']=={'status':'source_event','event_type':mode,'date_expression':date,'evidence':h['evidence']}and a['date_expression']is None and h['effective_period']['end']=={'status':'unknown','date_expression':None,'evidence':[]}
  if h['title'].startswith('都督')and h['title'].endswith('諸軍事'):region=h['title'][2:-3]
  elif h['title'].endswith('刺史'):region=h['title'][:-2]
  else:region=None
  if region is not None:assert h['jurisdictions']==[dict(source_name=region,place_id=None,modern_identification=None)]
  else:assert 'jurisdictions'not in h
  assert all(x['id']in b['roles'].values()or any(f['start']<=x['start']<x['end']<=f['end']and x['person_id']==roles[recipient]['person_id']for f in fields.values())for x in p['mentions']if x.get('kind')=='person'and scope['start']<=x['start']<scope['end'])
  return True
 except(KeyError,TypeError,ValueError,AssertionError,StopIteration):return False
