"""Position-bound received biography role frames. No person-ID/name whitelist.

Frames encode reviewed narrative syntax; they do not infer recipients using NLU.
The entire local sequence, all person slots and the biography head stay bound.
"""
import hashlib,re
FRAMES={'provincial_recruitment': [['R', 'issuer'], ['L', '臨'], ['F', 'place'], ['L', '辟'], ['R', 'subject'], ['L', '為'], ['F', 'office']], 'minister_recruitment': [['R', 'issuer'], ['L', '辟'], ['R', 'subject'], ['L', '為'], ['F', 'office']], 'early_office_series': [['L', '世以'], ['R', 'subject'], ['L', '為知人除'], ['F', 'county1'], ['F', 'county2'], ['F', 'county3'], ['L', '令'], ['R', 'father'], ['L', '卒去官後以'], ['F', 'old_office'], ['L', '舉高第為'], ['F', 'office2'], ['L', '轉'], ['F', 'office3'], ['L', '魏國既建遷為'], ['F', 'office4']], 'named_transfer': [['R', 'subject'], ['L', '轉為'], ['F', 'office1'], ['L', '領'], ['F', 'office2']], 'accession_office_series': [['R', 'ruler'], ['L', '在東宫深敬器焉待以交友之禮常歎曰自'], ['R', 'ruler_pronoun'], ['L', '有回門人日以親及即王位封'], ['R', 'subject'], ['F', 'rank1'], ['L', '徙為'], ['F', 'office1'], ['L', '制九品官人之法'], ['R', 'subject_repeat'], ['L', '所建也及踐阼遷'], ['F', 'office2'], ['L', '加'], ['F', 'office3'], ['L', '徙'], ['F', 'office4'], ['L', '進爵'], ['F', 'rank2']], 'campaign_office_series': [['R', 'ruler'], ['L', '征'], ['R', 'enemy'], ['L', '至'], ['F', 'place1'], ['L', '使'], ['R', 'subject'], ['L', '領'], ['F', 'office1'], ['R', 'ruler_repeat'], ['L', '還'], ['F', 'credential'], ['F', 'office2'], ['L', '還'], ['F', 'place2'], ['L', '以'], ['R', 'subject_repeat'], ['L', '為'], ['F', 'office3'], ['L', '領'], ['F', 'office4'], ['F', 'duty']], 'testamentary_successor_office_series': [['R', 'ruler'], ['L', '寢疾'], ['R', 'subject'], ['L', '與'], ['R', 'fellow1'], ['R', 'fellow2'], ['L', '等並受遺詔'], ['F', 'regency'], ['R', 'successor'], ['L', '即位進封'], ['F', 'rank'], ['L', '增邑'], ['F', 'increase'], ['L', '并前'], ['F', 'total'], ['L', '戸與'], ['F', 'fellow_title3'], ['R', 'fellow3'], ['F', 'fellow_title1'], ['R', 'fellow1_repeat'], ['F', 'fellow_title2'], ['R', 'fellow2_repeat'], ['L', '並'], ['F', 'privilege'], ['L', '頃之為'], ['F', 'office'], ['L', '故'], ['F', 'duty']], 'death_and_posthumous_name': [['R', 'resumed_subject'], ['L', '弘博不伐皆此類也'], ['F', 'date'], ['L', '薨諡曰'], ['R', 'posthumous_name'], ['L', '子'], ['R', 'child'], ['L', '嗣'], ['R', 'ruler'], ['L', '追思'], ['R', 'subject'], ['L', '功徳']], 'declined_county_appointment': [['R', 'issuer'], ['L', '恨不用'], ['R', 'subject'], ['L', '言舉茂才除'], ['F', 'office'], ['L', '不行隨'], ['R', 'father'], ['L', '避難徐州']], 'origin': [['R', 'subject'], ['L', '字'], ['F', 'courtesy'], ['F', 'place'], ['L', '人也']]}

def analyse(b,ch,person_id):
 p=next(p for p in ch['paragraphs']if p['id']==b['paragraph_id']);t=p['text'];ms={m['id']:m for m in p['mentions']};head=ms[b['biography_subject_mention_id']];a=b['scope_anchor'];rule=b['rule'];roles={k:ms[v]for k,v in b['roles'].items()};fields=b['fields']
 assert b['kind']=='received_biographical_role_sequence'and b['human_reviewed']is False and b['interpretation_note']
 assert p['text_layer']=='received_chapter'and b['source_revision']==ch['source'].get('source_commit',ch['source'].get('revision_id'))and hashlib.sha256(t.encode()).hexdigest()==b['paragraph_sha256']
 assert head.get('kind')=='person'and head['person_id']==person_id and head['start']==0 and t[head['end']:].startswith('字')
 def exact(x):return set(x)=={'paragraph_id','start','end','surface'}and x['paragraph_id']==p['id']and type(x['start'])is int and type(x['end'])is int and 0<=x['start']<x['end']<=len(t)and t[x['start']:x['end']]==x['surface']
 assert exact(a);pos=a['start'];usedr=set();usedf=set()
 for typ,key in FRAMES[rule]:
  if typ=='L':assert t.startswith(key,pos);pos+=len(key)
  elif typ=='R':
   m=roles[key];assert m['kind']=='person'and m['start']==pos and t[pos:m['end']]==m['surface'];usedr.add(key);pos=m['end']
  else:
   x=fields[key];assert exact(x)and x['start']==pos;usedf.add(key);pos=x['end']
   if key=='date':assert re.fullmatch(r'[^曰云詔不未欲薨卒]{1,8}[元一二三四五六七八九十百]+年',x['surface'])
   elif key in ('increase','total'):assert re.fullmatch(r'[一二三四五六七八九十百千萬零〇兩]+',x['surface'])
   else:assert not re.search(r'[曰云詔未不欲請薨卒。；！？「」『』]',x['surface'])and len(x['surface'])<=20
 assert pos==a['end']and set(roles)==usedr and set(fields)==usedf
 for name,m in roles.items():
  if name.startswith('subject')or name in ('resumed_subject','posthumous_name'):assert m['person_id']==person_id
  else:assert m['person_id']!=person_id
 for key in ('ruler','fellow1','fellow2','subject'):
  if key+'_repeat'in roles:assert roles[key]['person_id']==roles[key+'_repeat']['person_id']
 if 'ruler_pronoun'in roles:assert roles['ruler_pronoun']['person_id']==roles['ruler']['person_id']and roles['ruler_pronoun']['surface']=='吾'
 if 'resumed_subject'in roles:assert roles['resumed_subject']['surface']=='其'
 if 'father'in roles and rule=='early_office_series':assert roles['father']['surface']=='父'
 if rule=='testamentary_successor_office_series':assert len({roles[k]['person_id']for k in ('ruler','subject','fellow1','fellow2','successor','fellow3')})==6
 if rule=='campaign_office_series':assert roles['enemy']['person_id']!=roles['ruler']['person_id']
 # Every person occurrence is a reviewed grammatical slot, or an attested title of its slot's person.
 for m in p['mentions']:
  if m.get('kind')!='person'or not a['start']<=m['start']<a['end']:continue
  if m['id']in b['roles'].values():continue
  matches=[(k,x)for k,x in fields.items()if x['start']<=m['start']<m['end']<=x['end']]
  assert len(matches)==1
  key,field=matches[0];who=roles['fellow'+key[-1]]['person_id']if key.startswith('fellow_title')else person_id
  if rule=='minister_recruitment'and key=='office'and m['start']==field['start']and re.fullmatch(r'[東西南北中]?曹掾屬',t[m['end']:field['end']]):who=roles['issuer']['person_id']
  assert m['person_id']==who
 return p,roles,fields

# Each slot is an actual received title; semantic roles separate office, authority and privilege.
SLOTS={
 'provincial_recruitment':{'office':('office','grant','recruitment',None)},
 'minister_recruitment':{'office':('office','grant','recruitment',None)},
 'early_office_series':{'county1':('office','grant','sequential_appointment',None),'county2':('office','grant','sequential_appointment',None),'county3':('office','grant','sequential_appointment',None),'old_office':('office','attestation','previously_held',None),'office2':('office','grant','appointment',None),'office3':('office','transfer','transfer',None),'office4':('office','transfer','transfer','魏國既建')},
 'named_transfer':{'office1':('office','transfer','transfer',None),'office2':('office','grant','concurrent',None)},
 'accession_office_series':{'rank1':('noble_rank','grant','enfeoffment','及即王位'),'office1':('office','transfer','transfer','及即王位'),'office2':('office','transfer','transfer','及踐阼'),'office3':('office','grant','concurrent','及踐阼'),'office4':('office','transfer','transfer',None),'rank2':('noble_rank','grant','advancement',None)},
 'campaign_office_series':{'office1':('office','grant','concurrent',None),'credential':('honorific','grant','military_authorization','帝還'),'office2':('office','grant','military_command','帝還'),'office3':('office','grant','appointment','還許昌'),'office4':('office','grant','concurrent','還許昌'),'duty':('office','grant','official_duty','還許昌')},
 'testamentary_successor_office_series':{'rank':('noble_rank','grant','advancement','明帝即位'),'privilege':('honorific','grant','institutional_privilege',None),'office':('office','grant','appointment','頃之'),'duty':('office','attestation','continued_official_duty','頃之')},
 'death_and_posthumous_name':{'posthumous_name':('honorific','posthumous_naming','posthumous_name',None)}}
# Time labels are source strings, not inferred year numbers; generic ruler names are resolved slots.

def holding_valid(h,ch,root=None):
 try:
  b=h['source_role_sequence'];p,roles,fs=analyse(b,ch,h['person_id']);slot=h['source_role_slot'];kind,mode,semantic,time=SLOTS[b['rule']][slot];x=roles[slot]if slot=='posthumous_name'else fs[slot];a,=h['attestations'];e,=h['evidence'];title=x['surface'];shared=slot.startswith('county')
  if shared:
   suffix=p['text'][fs['county3']['end']:fs['county3']['end']+1];assert suffix=='令';title+=suffix
   assert h['shared_title_suffix']=={'component_anchor':fs[slot],'suffix_anchor':{'paragraph_id':p['id'],'start':fs['county3']['end'],'end':fs['county3']['end']+1,'surface':'令'},'expansion_status':'editorial_preferred','source_order':int(slot[-1]),'qualification':'收到三地名共享令字；依原序分錄，任年未載，不改原字。','secondary_reference_path':'source-evidence/sanguozhi022-chenqun-life/segmentation-reference.json'}
  assert h['title']==title and h['kind']==kind and h['mode']==mode and h['appointment_role']==semantic and h['status']=='source_attested'and h['human_reviewed']is False
  assert a['paragraph_id']==p['id']and a['start']==x['start']and a['end']==x['end']and a['surface']==x['surface']and a['date_expression']is None and a['usage']==('posthumous_usage'if mode=='posthumous_naming'else'narrative')
  person=next(m for m in p['mentions']if m['id']==a['person_mention_id']);assert person['person_id']==h['person_id']and b['scope_anchor']['start']<=person['start']<person['end']<=b['scope_anchor']['end']
  assert e==dict(work_id=ch['work_id'],book_id=ch['book_id'],chapter_id=ch['id'],source_id=ch['source_id'],paragraph_id=p['id'],quote=b['scope_anchor']['surface'],person_mention_id=person['id'])
  unknown={'status':'unknown','date_expression':None,'evidence':[]};start=unknown if mode=='attestation'else dict(status='source_event',event_type=mode,date_expression=None,evidence=h['evidence'])
  end=dict(status='source_event',event_type='explicit_end',date_expression=None,evidence=h['evidence'])if b['rule']=='early_office_series'and slot=='county3'else unknown
  scope={'source_expression':time,'normalized_start_year':None,'normalized_end_year':None,'status':'source_event_order_only'if time else'undated'}
  if 'source_role_year_bridge' in h:
   try:
    from scripts.role_event_year_bridge import valid as role_event_year_valid
   except ImportError:
    from role_event_year_bridge import valid as role_event_year_valid
   assert role_event_year_valid(h,ch,root)
   actual=h['effective_period']['start']
   if 'normalized_date'in actual:
    start['normalized_date']=actual['normalized_date'];scope['normalized_start_year']=actual['normalized_date']['year'];scope['status']='external_event_year'
   else:start['normalized_date_range']=actual['normalized_date_range'];scope['status']='external_event_year_range'
  assert h['effective_period']=={'start':start,'end':end}and h['source_time_scope']==scope
  if mode=='posthumous_naming':assert h['naming_basis']=={'source_term':b['scope_anchor']['surface'],'death_term':'薨','evidence':h['evidence']}
  return True
 except(KeyError,TypeError,ValueError,StopIteration,AssertionError,IndexError):return False

def event_valid(e,ch):
 try:
  b=e['source_role_sequence'];p,roles,fs=analyse(b,ch,e['person_id']);a=fs['date'];ev,=e['evidence'];assert b['rule']=='death_and_posthumous_name'and e['event_type']=='death'and e['source_term']=='薨'and e['date_expression']==a['surface'];assert ev['quote']==b['scope_anchor']['surface']and ev['person_mention_id']==roles['subject']['id'];assert e['normalized_date']['source_expression']==a['surface']and e['normalized_date']['evidence']==e['evidence'];return True
 except(KeyError,TypeError,ValueError,StopIteration,AssertionError):return False

def proposal_errors(q,ch,pids):
 try:
  b=q['source_appointment_context'];p,roles,fs=analyse(b,ch,q['person_id']);assert b['rule']=='declined_county_appointment'and q['person_id']in pids and q['title']==fs['office']['surface']and q['person_mention_id']==roles['subject']['id'];assert q['proposal_kind']=='unassumed_appointment'and q['outcome']=='not_assumed'and q['status']=='contextual_provisional'and q['human_reviewed']is False and q['role_anchor']==fs['office'];assert q['non_assumption_anchor']['surface']=='不行'and q['non_assumption_anchor']['start']==fs['office']['end']and q['non_assumption_anchor']['end']==fs['office']['end']+2;assert q['evidence'][0]['quote']==b['scope_anchor']['surface']and q['evidence'][0]['person_mention_id']==roles['subject']['id'];assert q['non_assumption_anchor']['paragraph_id']==p['id']and q['evidence'][0]==dict(work_id=ch['work_id'],book_id=ch['book_id'],chapter_id=ch['id'],source_id=ch['source_id'],paragraph_id=p['id'],quote=b['scope_anchor']['surface'],person_mention_id=roles['subject']['id'])and 'normalized_date'not in q;return []
 except(KeyError,TypeError,ValueError,StopIteration,AssertionError):return ['未赴任須有本傳受任者與不行原句，不得改為實任']

def integer(term):
 digits={c:i for i,c in enumerate('零一二三四五六七八九')};digits.update({'〇':0,'兩':2});units={'十':10,'百':100,'千':1000,'萬':10000};n=0;total=0
 for c in term:
  if c in digits:n=digits[c]
  elif c in units:
   if units[c]==10000:total=(total+n)*10000;n=0
   else:total+=(n or 1)*units[c];n=0
  else:raise ValueError('non integer')
 return total+n

def detail_valid(d,ch,hs):
 try:
  b=d['source_role_sequence'];p,roles,fs=analyse(b,ch,d['person_id']);v=d['values'];a=d['source_anchor'];e,=d['evidence'];assert d['status']=='source_attested'and d['human_reviewed']is False and d['date_expression']is None and d['source_revision']==b['source_revision']and d['paragraph_sha256']==b['paragraph_sha256'];person=next(m for m in p['mentions']if m['id']==e['person_mention_id']);assert person['person_id']==d['person_id']and b['scope_anchor']['start']<=person['start']<person['end']<=b['scope_anchor']['end'];assert e==dict(work_id=ch['work_id'],book_id=ch['book_id'],chapter_id=ch['id'],source_id=ch['source_id'],paragraph_id=p['id'],quote=b['scope_anchor']['surface'],person_mention_id=person['id']);assert set(a)=={'paragraph_id','start','end','surface'}and a['paragraph_id']==p['id']and type(a['start'])is int and type(a['end'])is int and b['scope_anchor']['start']<=a['start']<a['end']<=b['scope_anchor']['end']and p['text'][a['start']:a['end']]==a['surface']==d['source_term']
  if d['kind']=='official_duty':return b['rule']=='testamentary_successor_office_series'and a['surface']=='並受遺詔輔政'and v=={'duty_code':'received_testamentary_regency_charge','fellow_person_ids':[roles['fellow1']['person_id'],roles['fellow2']['person_id']],'fellow_mention_ids':[roles['fellow1']['id'],roles['fellow2']['id']],'office_title':None}
  if d['kind']=='office_departure':return b['rule']=='early_office_series'and a['surface']=='父卒去官'and v['departure_kind']=='mourning_after_father_death'and v['source_parent_mention_id']==roles['father']['id']and len(v['linked_holding_ids'])==1 and {hs[i]['source_role_slot']for i in v['linked_holding_ids']}=={'county3'}and all(hs[i]['person_id']==d['person_id']and hs[i]['source_role_sequence']==b for i in v['linked_holding_ids'])
  if d['kind']=='fief_household_count':return b['rule']=='testamentary_successor_office_series'and a['surface']=='增邑'+fs['increase']['surface']+'并前'+fs['total']['surface']+'戸'and v=={'increase':integer(fs['increase']['surface']),'total':integer(fs['total']['surface']),'increase_source_number':fs['increase']['surface'],'total_source_number':fs['total']['surface'],'unit_source_name':'戸','actual_revenue':None}
  return False
 except(KeyError,TypeError,ValueError,StopIteration,AssertionError):return False

def errors(chapters,records,root=None):
 out=[];hs={h['id']:h for r in records for h in r.get('holdings',[])}
 for r in records:
  ch=chapters.get(r.get('chapter_id'))
  if not ch:continue
  for h in r.get('holdings',[]):
   if 'source_role_sequence'in h and not holding_valid(h,ch,root):out.append('官爵本傳角色／語法／時段不符:'+str(h.get('id')))
   if 'shared_title_suffix'in h and root is not None:
    try:
     import json
     from pathlib import Path
     ref=json.loads((Path(root)/h['shared_title_suffix']['secondary_reference_path']).read_text());raw=(Path(root)/ref['local_excerpt_path']).read_bytes();fs=h['source_role_sequence']['fields'];expected='除'+ '、'.join(fs[k]['surface']for k in ('county1','county2','county3'))+'令'
     assert hashlib.sha256(raw).hexdigest()==ref['local_excerpt_sha256']and expected in ref['exact_quote']and ref['exact_quote']in raw.decode()and ref['fixed_raw_revision']is None and ref['image_verified']is False and ref['human_reviewed']is False
    except(KeyError,TypeError,ValueError,OSError,AssertionError):out.append('共享令字展開須保次要分詞依據與未圖校資格')
  for e in r.get('events',[]):
   if 'source_role_sequence'in e and not event_valid(e,ch):out.append('死亡本傳角色／紀年不符:'+str(e.get('id')))
 return out
