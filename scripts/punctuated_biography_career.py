"""Finite punctuated received career clauses, explicit subjects and guarded ellipsis."""
import hashlib,re
KIND='punctuated_biography_career_frame'
# slot,recipient,kind,mode,semantic,time-field
FRAMES={
 'initial_local':('初為{office}，<visitor>常過<subject>，<subject_repeat>歎曰',[('office','head','office','grant','appointment',None)]),
 'staff_and_exclusion':('{time}，為<ruler>{office}。時<rebel>反于蜀，<other>即<rebel_repeat>之從甥，少長<rebel_repeat2>家，<other_repeat>為<ruler_repeat>{otheroffice}，<subject>啟出<other_repeat2>。<ruler_repeat2>雖不用，然知<subject_repeat>雅正。',[('office','head','office','grant','staff_appointment','time'),('otheroffice','other','office','attestation','reported_service',None)]),
 'paired_and_promoted':('<ruler>踐阼，初建東宮，以<subject>及<colleague>並為{office}。遷{office2}、{office3}，封{rank}。',[('office','head','office','grant','paired_appointment',None),('office','colleague','office','grant','paired_appointment',None),('office2','head','office','transfer','transfer',None),('office3','head','office','transfer','transfer',None),('rank','head','noble_rank','grant','enfeoffment',None)]),
 'province_and_privileges':('{time}，遷{office1}、{office2}，尋假{privilege1}、{privilege2}。',[('office1','head','office','transfer','transfer','time'),('office2','head','office','transfer','transfer','time'),('privilege1','head','honorific','grant','ceremonial_privilege',None),('privilege2','head','honorific','grant','ceremonial_privilege',None)]),
 'subordinate_appointment':('時{office1}<other>有俊才，而門寒為豪族所排，<subject>用為{office2}，<other_repeat>後果有名位，時以<subject_repeat>為知人。',[('office1','other','office','attestation','reported_service',None),('office2','other','office','grant','subordinate_appointment',None)]),
 'late_summons':('{time}，徵為{office}。<subject>有重名，當世朝臣皆出<subject_repeat>下。',[('office','subject','office','grant','summoned_appointment','time')]),
 'posthumous_deliberation':('{date}卒，太常上諡為{proposal1}。有司議以貴賤不同號，諡與<ancestor>同，不可，請諡曰{proposal2}。詔曰：「諡所以旌德表行，按諡法一德不懈為{rulepost}。<subject>忠毅清直，立德不渝。」於是遂賜諡曰{postname}。',[('postname','subject','honorific','posthumous_naming','posthumous_name',None)])}
def analyse(record,ch):
 b=record.get('source_career_role',record.get('source_appointment_context'));assert b['kind']==KIND and b['human_reviewed']is False and b['source_revision']==ch['source']['revision_id']
 ps={p['id']:p for p in ch['paragraphs']};assert len(ps)==len(ch['paragraphs']);p=ps[b['paragraph_id']];t=p['text'];a=b['scope_anchor'];ms={m['id']:m for q in ch['paragraphs']for m in q['mentions']};head=ms[b['head_mention_id']];hp=ch['paragraphs'][0]
 assert head['kind']=='person'and head['start']==0 and hp['mentions'][0]['id']==head['id']and re.match(r'，字[^，。]+，[^。]+人也。',hp['text'][head['end']:])and p['text_layer']==hp['text_layer']=='received_chapter'
 assert b['paragraph_sha256']==hashlib.sha256(t.encode()).hexdigest()
 def exact(x):return set(x)=={'paragraph_id','start','end','surface'}and x['paragraph_id']==p['id']and type(x['start'])is int and type(x['end'])is int and 0<=x['start']<x['end']<=len(t)and t[x['start']:x['end']]==x['surface']
 assert exact(a)and (a['start']==0 or t[a['start']-1]in '。；，'or t[:a['start']].endswith(('。」','。』','！」','？」')))and t[:a['start']].count('「')==t[:a['start']].count('」')and t[:a['start']].count('『')==t[:a['start']].count('』');roles={k:ms[v]for k,v in b['roles'].items()};fields=b['fields'];template,slots=FRAMES[b['rule']];cursor=a['start'];usedr=set();usedf=set()
 for token in re.split(r'(<[^>]+>|\{[^}]+\})',template):
  if not token:continue
  if token.startswith('<'):k=token[1:-1];x=roles[k];assert x['kind']=='person'and x['start']==cursor and t[x['start']:x['end']]==x['surface'];usedr.add(k)
  elif token.startswith('{'):k=token[1:-1];x=fields[k];assert exact(x)and x['start']==cursor and len(x['surface'])<=20 and not any(c in x['surface']for c in '曰云詔非未不欲請薨卒，。；：「」');usedf.add(k)
  else:assert t.startswith(token,cursor);cursor+=len(token);continue
  cursor=x['end']
 assert cursor==a['end']and set(roles)==usedr and set(fields)==usedf
 for k,m in roles.items():
  if '_repeat'in k:assert roles[k.split('_repeat')[0]]['person_id']==m['person_id']
 if 'subject'in roles:assert roles['subject']['person_id']==head['person_id']
 for k in ('other','colleague','visitor','ruler','rebel','ancestor'):
  if k in roles:assert roles[k]['person_id']!=head['person_id']
 # No subject changes can be hidden in scalar slots. All actual person marks are role-bound.
 roleids={m['id']for m in roles.values()}
 for m in p['mentions']:
  if m['kind']=='person'and a['start']<=m['start']<a['end']:assert m['id']in roleids
 roles['head']=head
 ev,=record['evidence'];assert ev==dict(work_id=ch['work_id'],book_id=ch['book_id'],source_id=ch['source_id'],chapter_id=ch['id'],paragraph_id=p['id'],quote=t,person_mention_id=roles[b['recipient_role']]['id'])
 return p,roles,fields,slots

def holding_valid(h,ch):
 try:
  p,roles,fields,slots=analyse(h,ch);b=h['source_career_role'];slot,recipient,kind,mode,semantic,time=next(s for s in slots if s[0]==b['slot']and s[1]==b['recipient_role']);x=fields[slot];m=roles[recipient]
  assert h['person_id']==m['person_id']and h['title']==x['surface']and h['kind']==kind and h['mode']==mode and h['appointment_role']==semantic and h['status']=='source_attested'and h['human_reviewed']is False
  title=h['title']
  if kind=='office':assert 1<=len(title)<=20 and (len(title)>1 or title in ('掾','令','率'))and any(title.endswith(s)for s in('令','主薄','主簿','掾','庶子','率','將軍','刺史','別駕','尚書','亭長'))and not any(s in title for s in('少與','有重名','後果','高簡'))
  elif kind=='noble_rank':assert title.endswith(('公','侯','伯','子','男'))and 2<=len(title)<=20
  elif semantic=='ceremonial_privilege':assert title.endswith(('曲蓋','鼓吹'))and 2<=len(title)<=10
  else:assert semantic=='posthumous_name'and len(title)==1 and fields['rulepost']['surface']==title and title not in [fields['proposal1']['surface'],fields['proposal2']['surface']]
  if mode=='posthumous_naming':assert h['naming_basis']==dict(source_term=b['scope_anchor']['surface'],death_term='卒',evidence=h['evidence'])
  else:assert 'naming_basis'not in h
  a,=h['attestations'];assert a==dict(id=a['id'],paragraph_id=p['id'],start=x['start'],end=x['end'],surface=title,person_mention_id=m['id'],usage='narrative',date_expression=None)
  unknown=dict(status='unknown',date_expression=None,evidence=[]);want=unknown if mode=='attestation'else dict(status='source_event',event_type=mode,date_expression=fields[time]['surface']if time else None,evidence=h['evidence']);start=h['effective_period']['start'];base={k:v for k,v in start.items()if k!='normalized_date_range'};assert base==want and h['effective_period']['end']==unknown and 'normalized_date'not in start
  if time:
   try:from scripts.date_ranges import year_range_errors
   except ImportError:from date_ranges import year_range_errors
   assert 'normalized_date_range'in start and not year_range_errors(start['normalized_date_range'],h['evidence'],want['date_expression'])
  else:assert 'normalized_date_range'not in start
  return True
 except(KeyError,ValueError,TypeError,AssertionError,StopIteration,IndexError):return False

def proposal_errors(q,ch,pids):
 try:
  p,rs,fs,slots=analyse(q,ch);b=q['source_appointment_context'];assert b['rule']=='posthumous_deliberation'and b['slot']in('proposal1','proposal2')and b['recipient_role']=='subject';a=fs[b['slot']];head=rs['subject']
  assert q['person_id']==head['person_id']in pids and q['person_mention_id']==head['id']and q['title']==a['surface']and q['role_anchor']==a and q['proposal_kind']=='posthumous_name_proposal'and q['outcome']=='not_enacted'and q['status']=='contextual_provisional'and q['human_reviewed']is False and q['effective_service_attested']is False
  assert q['actual_grant_title']==fs['postname']['surface']and q['actual_grant_anchor']==fs['postname']and q['title']!=q['actual_grant_title']and q['date_expression']is None
  assert 'normalized_date'not in q and 'normalized_date_range'not in q and q['interpretation_note']and q['reviewer']
  return []
 except(KeyError,ValueError,TypeError,AssertionError,StopIteration,IndexError):return ['諡議須綁完整否決/改請/實賜語境，不得作已授稱號或搬死亡日期']

def sister_valid(a,ch):
 try:
  q=a['qualifiers'];b=q['source_clause_binding'];e,=a['evidence'];p=next(p for p in ch['paragraphs']if p['id']==e['paragraph_id']);ms={m['id']:m for m in p['mentions']};s=ms[e['subject_person_mention_id']];o=ms[e['object_person_mention_id']];x=b['scope_anchor'];t=p['text']
  assert b['kind']=='has_widowed_older_sister'and b['paragraph_sha256']==hashlib.sha256(t.encode()).hexdigest()and b['source_revision']==ch['source']['revision_id']and b['human_reviewed']is False
  assert x==dict(paragraph_id=p['id'],start=o['start'],end=s['end'],surface=o['surface']+'有寡姊')and t[x['start']:x['end']]==x['surface']and s['surface']=='寡姊'and s['start']==o['end']+1
  assert (x['start']==0 or t[x['start']-1]in '。；，')and t[:x['start']].count('「')==t[:x['start']].count('」')and t[:x['start']].count('『')==t[:x['start']].count('』')
  assert a['predicate']=='sister'and a['subject_person_id']==s['person_id']!=o['person_id']==a['object_person_id']and s['kind']==o['kind']=='person'and a['status']=='source_attested'and a['human_reviewed']is False and q['source_term']=='寡姊'
  assert set(q)=={'source_term','relative_birth_order','source_clause_binding'}and q['relative_birth_order']==dict(older_person_id=s['person_id'],younger_person_id=o['person_id'],operator='lt',scope='siblings',older_ordinal=None,younger_ordinal=None)
  assert e==dict(work_id=ch['work_id'],book_id=ch['book_id'],source_id=ch['source_id'],chapter_id=ch['id'],paragraph_id=p['id'],quote=t,subject_person_mention_id=s['id'],object_person_mention_id=o['id'])
  return True
 except(KeyError,ValueError,TypeError,AssertionError,StopIteration):return False

def death_valid(event,ch):
 try:
  b=event['source_death_context'];e,=event['evidence'];p=next(p for p in ch['paragraphs']if p['id']==e['paragraph_id']);t=p['text'];m=next(m for m in p['mentions']if m['id']==b['subject_mention_id']);a=b['clause_anchor'];d=b['death_anchor']
  def exact(x):return set(x)=={'paragraph_id','start','end','surface'}and x['paragraph_id']==p['id']and type(x['start'])is int and type(x['end'])is int and 0<=x['start']<x['end']<=len(t)and t[x['start']:x['end']]==x['surface']
  assert b['kind']=='punctuated_biography_death_report'and b['source_revision']==ch['source']['revision_id']and b['paragraph_sha256']==hashlib.sha256(t.encode()).hexdigest()and b['human_reviewed']is False and exact(a)and exact(d)
  assert m['kind']=='person'and event['person_id']==m['person_id']and event['event_type']=='death'and event['status']=='source_attested'and event['human_reviewed']is False and e==dict(work_id=ch['work_id'],book_id=ch['book_id'],source_id=ch['source_id'],chapter_id=ch['id'],paragraph_id=p['id'],quote=t,person_mention_id=m['id'])
  assert a['start']==0 or t[a['start']-1]in '。；，'
  assert event['source_anchor']==d and event['source_term']==d['surface']and t[:a['start']].count('「')==t[:a['start']].count('」')and t[:a['start']].count('『')==t[:a['start']].count('』')and d['end']==a['end']
  if b['rule']=='illness_gift_then_dated_death':
   date=b['date_anchor'];assert exact(date)and date['end']==d['start']and date['surface']==event['date_expression']and event['normalized_date']['source_expression']==date['surface']and d['surface']=='卒'and m['start']==a['start']+1
   pattern='及'+re.escape(m['surface'])+r'疾病，詔賜錢[一二三四五六七八九十百千萬]+，日給酒米。'+re.escape(date['surface'])+'卒'
   assert re.fullmatch(pattern,a['surface'])and not any(x['kind']=='person'and m['end']<=x['start']<a['end']for x in p['mentions'])
  elif b['rule']=='later_executed_subject':assert a['surface']==m['surface']+'後果誅'and m['start']==a['start']and d['surface']=='誅'and event['date_expression']is None and 'normalized_date'not in event and 'normalized_date_range'not in event
  else:return False
  return True
 except(KeyError,ValueError,TypeError,AssertionError,StopIteration,IndexError):return False

FRAMES['excursion_dismissal']=('遂送<visitor>出界數百里，{departure}。',[])
def detail_valid(d,ch,holdings):
 try:
  p,rs,fs,slots=analyse(d,ch);b=d['source_career_role'];m=rs['head'];x=fs['departure'];v=d['values'];linked=holdings[v['linked_holding_id']]
  assert b['rule']=='excursion_dismissal'and b['slot']=='departure'and b['recipient_role']=='head'and d['person_id']==m['person_id']and d['kind']=='office_departure'and d['source_term']==x['surface']=='坐此免官'and d['source_anchor']==x and d['paragraph_sha256']==b['paragraph_sha256']and d['source_revision']==b['source_revision']and d['date_expression']is None and 'normalized_date'not in d and 'normalized_date_range'not in d and d['status']=='source_attested'and d['human_reviewed']is False
  assert v==dict(departure_code='dismissal_after_excursion',linked_holding_id=linked['id'],date_unknown=True,all_other_offices_ended=False)
  assert linked['person_id']==d['person_id']and linked['source_career_role']['rule']=='initial_local'and holding_valid(linked,ch)and linked['attestations'][0]['end']<b['scope_anchor']['start']
  return True
 except(KeyError,ValueError,TypeError,AssertionError,StopIteration,IndexError):return False
