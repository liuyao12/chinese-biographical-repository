"""Machine-readable details outside titles/kinship, always bound to received text.
These records never create office holdings, parentage, salary payments or burial events.
"""
import hashlib,re

def errors(chapters,records,root=None):
 out=[];holdings={h['id']:h for r in records for h in r.get('holdings',[])};offers={q['id']:q for ch in chapters.values()for q in ch.get('annotation',{}).get('title_proposals',[])}
 for record in records:
  if record.get('record_type')!='biographical_source_detail_set':continue
  if set(record)!={'format_version','record_type','chapter_id','records'}or record.get('format_version')!='0.2'or record.get('chapter_id')not in chapters or not isinstance(record.get('records'),list)or not record['records']:
   out.append('來源細節集頭／範圍不符');continue
  ch=chapters.get(record.get('chapter_id'),{});seen=set()
  for d in record.get('records',[]):
   if d.get('id')in seen:out.append('來源細節ID重複')
   seen.add(d.get('id'))
   if not valid(d,ch,holdings,offers,root):out.append('來源細節格式／原句／角色不符:'+str(d.get('id')))
 for ch in chapters.values():
  for h in [h for r in records if r.get('chapter_id')==ch['id']for h in r.get('holdings',[])]:
   if (any(k in h for k in ('collective_designation','same_office_designation_as','assumption_basis')) or str(h.get('reported_duration',{}).get('source_term','')).startswith('視事'))and not holding_valid(h,ch,holdings):out.append('稱號額外句法不符:'+h['id'])
 return out

def valid(d,ch,hs,qs,root=None):
 if 'received_source_frame'in d:
  try:from scripts.fixed_received_career import nonholding_valid
  except ImportError:from fixed_received_career import nonholding_valid
  return nonholding_valid(d,ch,root,'detail',hs)
 if 'source_career_role' in d:
  try:from scripts.received_career_roles import detail_valid
  except ImportError:from received_career_roles import detail_valid
  return detail_valid(d,ch,hs)

 if 'source_family_duty_frame' in d:
  try:from scripts.named_family_offices import duty_valid
  except ImportError:from named_family_offices import duty_valid
  return duty_valid(d,{ch['id']:ch},hs)

 if 'source_detail_pattern' in d:
  try:
   from scripts.source_office_reports import detail_valid
  except ImportError:
   from source_office_reports import detail_valid
  return detail_valid(d,ch,hs,root)
 if 'source_role_sequence' in d:
  try:
   from scripts.biographical_appointment_sequence import detail_valid
  except ImportError:
   from biographical_appointment_sequence import detail_valid
  return detail_valid(d,ch,hs)
 try:
  if set(d)!={'status','reviewer','human_reviewed','model','id','person_id','kind','source_term','source_anchor','source_revision','paragraph_sha256','values','date_expression','evidence','interpretation_note'}:return False
  a=d['source_anchor'];p=next(p for p in ch['paragraphs']if p['id']==a['paragraph_id']);t=p['text'];e,=d['evidence'];m=next(x for x in p['mentions']if x['id']==e['person_mention_id']);v=d['values'];term=d['source_term'];kind=d['kind']
  if(e['chapter_id']!=ch['id']or e['source_id']!=ch['source_id']or e['quote']!=t or m['person_id']!=d['person_id']or d['status']!='source_attested'or d['human_reviewed']is not False or d['date_expression']is not None or not d['interpretation_note']or d['source_revision']!=p['source_position']['revision_id']or d['paragraph_sha256']!=hashlib.sha256(t.encode()).hexdigest()or set(a)!={'paragraph_id','start','end','surface'}or a['surface']!=term or not 0<=a['start']<a['end']<=len(t)or t[a['start']:a['end']]!=term):return False
  if not source_subject_valid(d,p,ch):return False
  def linked(key='linked_holding_id'):
   h=hs.get(v[key]);return h and h['person_id']==d['person_id']and any(x['paragraph_id']==p['id']for x in h['evidence'])
  if kind=='recorded_presence':
   if set(v)!={'place_source_name','place_id','modern_identification','movement_source_term','origin_or_residence'}or any(v[k]is not None for k in ('place_id','modern_identification','origin_or_residence')):return False
   place=v['place_source_name'];verb=v['movement_source_term']
   if place not in term or verb not in term or verb not in ('游','從駕','步出','還','詣','見於','出幸','到'):return False
   # Exact stated participant, or the continued biographical topic, not any convenient nearby name.
   return m['surface']in term or (verb in ('步出','見於','到')and m['person_id']==ch['paragraphs'][0]['mentions'][0]['person_id'])or(verb=='出幸'and m['person_id']in {x['person_id']for x in p['mentions']if x['surface']=='輿駕'})
  if kind=='official_duty':return v==dict(duty_code='drafting_secretariat_edicts',organ_source_names=['中書','散騎'],document_source_name='詔冊',linked_holding_id=v.get('linked_holding_id'))and term=='並掌中書、散騎二省詔冊'and linked()and hs[v['linked_holding_id']]['title']=='侍中'
  if kind=='office_emolument':
   keys={'emolument_kind','source_grade','nominal_grade_number','source_number','unit_source_name','actual_payment_value','annual_payment_value','linked_holding_id','outcome'}
   if set(v)!=keys or v['actual_payment_value']is not None or v['annual_payment_value']is not None:return False
   if term=='加秩中二千石':return v==dict(emolument_kind='rank_grade',source_grade='中二千石',nominal_grade_number=2000,source_number='二千',unit_source_name='石',actual_payment_value=None,annual_payment_value=None,linked_holding_id=v['linked_holding_id'],outcome='grade_awarded')and linked()and hs[v['linked_holding_id']]['title']=='義興太守'
   return term=='俸以卿祿，常出在所'and v==dict(emolument_kind='unspecified_grade_basis',source_grade='卿祿',nominal_grade_number=None,source_number=None,unit_source_name=None,actual_payment_value=None,annual_payment_value=None,linked_holding_id=None,outcome='ordered_payment_not_receipt_attested')
  if kind=='office_departure':return term=='遂廢于家'and v==dict(departure_kind='dismissed_offices_unspecified',linked_holding_ids=[],titles_unspecified=True,place_source_name='家')
  if kind=='mourning_service_continuation':return term=='其年，遭母憂，尋有詔攝職如故'and v==dict(service_state='retained_by_decree_after_mourning',linked_holding_ids=[],titles_unspecified=True,biological_mother=None)
  if kind=='ritual_and_duty_exemption':return term=='詔停諸公事及朔望朝謁'and set(v)=={'exemption_codes','source_terms','authorization','linked_holding_ids'}and v['exemption_codes']==['routine_public_business','new_and_full_moon_court_attendance']and v['source_terms']==['諸公事','朔望朝謁']and v['authorization']=='imperial_decree'and len(v['linked_holding_ids'])==3 and {hs[x]['title']for x in v['linked_holding_ids']}=={'侍中','司徒','尚書令'}and all(hs[x]['person_id']==d['person_id']for x in v['linked_holding_ids'])
  if kind=='literary_activity':
   if set(v)!={'activity_code','work_source_name','work_id','completion_attested','source_year'}or v['work_id']is not None or v['source_year']is not None or v['completion_attested']is not True:return False
   return (term=='詔使爲《洞井贊》，於坐奏之'and v['activity_code']=='composition_at_imperial_command'and v['work_source_name']=='洞井贊')or(term==m['surface']+'所著書及文章，並行於世'and v['activity_code']=='works_in_circulation'and v['work_source_name']is None)
  if kind=='staff_principal':
   if set(v)!={'principal_person_id','principal_mention_id','principal_source_title','staff_source_title','linked_holding_id'}or not linked():return False
   who=next(x for x in p['mentions']if x['id']==v['principal_mention_id'])
   if who['person_id']!=v['principal_person_id']or who['person_id']==d['person_id']or hs[v['linked_holding_id']]['title']!=v['staff_source_title']:return False
   return term in (v['principal_source_title']+who['surface']+v['staff_source_title'],who['surface']+'爲'+v['principal_source_title']+'輔政，選'+m['surface']+'爲'+v['staff_source_title'],who['surface']+'進'+v['principal_source_title']+'，又以'+m['surface']+'爲'+v['staff_source_title'])
  if kind=='recalled_unassumed_appointment':return set(v)=={'appointment_record_ids','service_attested'}and v['service_attested']is False and term.endswith(m['surface'])and all(x in qs and qs[x]['person_id']==d['person_id']and qs[x]['proposal_kind']=='unassumed_appointment'and qs[x]['title']in term for x in v['appointment_record_ids'])and len(v['appointment_record_ids'])==2
  if kind=='gift':
   if set(v)!={'gift_state','recipient_person_id','items'}:return False
   if term=='致𤅢數斛酒':
    recipient=next(x for x in p['mentions']if x['start']==a['start']+1)
    return recipient['person_id']==v['recipient_person_id']!=d['person_id']and v['gift_state']=='sent'and v['items']==[dict(source_name='酒',source_number='數',value=None,unit_source_name='斛',quantity_kind='unspecified_count')]
   if v['gift_state']!='ordered_not_receipt_attested'or v['recipient_person_id']!=d['person_id']:return False
   if term=='可賜床帳褥席':return v['items']==[dict(source_name='床帳褥席',source_number=None,value=None,unit_source_name=None,quantity_kind='unsegmented_source_catalogue')]
   exact=[dict(source_name=n,source_number=num,value=value,unit_source_name=u,quantity_kind='exact_source_number'if num else'not_numbered')for n,num,value,u in [('東園秘器',None,None,None),('朝服','一',1,'具'),('衣','一',1,'襲'),('錢','十萬',100000,None),('布','百',100,'匹'),('蠟','百',100,'斤')]]
   return term=='詔給東園秘器，朝服一具，衣一襲，錢十萬，布百匹，蠟百斤'and v['items']==exact
  return False
 except(KeyError,TypeError,ValueError,StopIteration):return False

def holding_valid(h,ch,hs):
 try:
  e,=h['evidence'];p=next(p for p in ch['paragraphs']if p['id']==e['paragraph_id']);t=p['text'];ms={m['id']:m for m in p['mentions']};m=ms[e['person_mention_id']]
  if m['person_id']!=h['person_id']:return False
  if 'reported_duration'in h and str(h['reported_duration'].get('source_term','')).startswith('視事'):
   if not service_duration_valid(h,p,ch):return False
  if 'collective_designation'in h:
   b=h['collective_designation'];members=[ms[x]for x in b['member_mention_ids']]
   if set(b)!={'source_number','count','member_person_ids','member_mention_ids','source_term'}or b['source_number']!='四'or b['count']!=4 or len(members)!=4 or len({x['person_id']for x in members})!=4 or [x['person_id']for x in members]!=b['member_person_ids']or h['person_id']not in b['member_person_ids']or h['title']!='天子四友'or not t.startswith(b['source_term'])or not b['source_term'].endswith('時號爲天子四友。')or any(not 0<=x['start']<len(b['source_term'])for x in members):return False
   if not collective_members_valid(h,p,ch):return False
  if 'same_office_designation_as'in h:
   b=h['same_office_designation_as'];other=hs[b['holding_id']]
   if b!={'holding_id':other['id'],'full_source_title':'太子舍人','source_term':'遷太子舍人，以父憂去職。服闋，復爲舍人','basis':'same_received_paragraph_resumption','period_continuity':False}or b['source_term']not in t or other['title']!='太子舍人'or other['person_id']!=h['person_id']or h['title']!='舍人':return False
  if 'assumption_basis'in h:
   if h['person_id']!=biography_topic(ch)['person_id']:return False
   b=h['assumption_basis']
   if set(b)!={'kind','source_term','person_mention_id','evidence'}or b['person_mention_id']!=m['id']or b['evidence']!=h['evidence']or b['source_term']not in t:return False
   if b['kind']=='return_and_delayed_formal_investiture':
    if h['title']not in ('侍中','司徒','尚書令')or b['source_term']!='到京師，勑材官起府於舊宅，高祖臨軒，遣謁者於府拜授，詔停諸公事及朔望朝謁。':return False
   elif b['kind']=='initial_refusal_then_explicit_acceptance':
    if h['title']not in ('中書監','司徒','衛將軍')or b['source_term']!='後五年，改授中書監、司徒、衛將軍，並固讓不受。遣謁者敦授，乃拜受焉。':return False
   else:return False
  return True
 except(KeyError,TypeError,ValueError,StopIteration):return False


def biography_topic(ch):
 """Source-derived owner, never a person ID or label whitelist.
 This scoped grammar requires the complete received biography head, not a nearby name.
 """
 p=ch['paragraphs'][0];m=p['mentions'][0];t=p['text']
 if m['start']!=0 or not re.match(re.escape(m['surface'])+r'字[^，。]+，[^，。]+人也。祖',t):raise ValueError('unsupported biography head')
 return m

def named_role(p,start,end,pid):
 return any(m.get('person_id')==pid and m['start']==start and m['end']==end for m in p['mentions'])

def source_subject_valid(d,p,ch):
 """Narrow received-clause role grammar; unsupported variants fail closed.
 Giver, ordering sovereign and later same-paragraph appointees are not recipients.
 """
 kind=d['kind'];term=d['source_term'];t=p['text'];pid=d['person_id']
 scoped=kind in ('official_duty','office_departure','mourning_service_continuation','ritual_and_duty_exemption','office_emolument','literary_activity','gift')
 if not scoped:return True
 owner=biography_topic(ch)['person_id']
 if pid!=owner:return False
 def role(pattern,group=1):
  x=re.search(pattern,t)
  return x is not None and named_role(p,x.start(group),x.end(group),owner)
 if kind=='official_duty':
  return role(r'選([^，。]+)爲長史，勑與河南[^。]+時號爲天子四友。續拜侍中，並掌中書、散騎二省詔冊。')
 if kind=='office_departure':
  return role(r'請誅([^。]+)。帝曰：「殺之則遂成其名，正應容之度外耳。」遂廢于家。')
 if kind=='mourning_service_continuation':
  return role(r'^三年元會，詔([^，。]+)乘小輿升殿。其年，遭母憂，尋有詔攝職如故。')
 if kind=='ritual_and_duty_exemption':
  return role(r'([^，。]+)辭腳疾不堪拜謁，乃角巾肩輿，詣雲龍門謝。') and '到京師，勑材官起府於舊宅，高祖臨軒，遣謁者於府拜授，'+term+'。' in t
 if kind=='literary_activity':
  if term.startswith('詔使'):return role(r'勑[^，。]+攜([^，。]+)從駕，詔使爲《洞井贊》，於坐奏之。')
  return role(r'([^，。]+)所著書及文章，並行於世。')
 if kind=='office_emolument':
  if term=='加秩中二千石':return '五年，出爲冠軍將軍、義興太守，加秩中二千石。在郡' in t and '視事三年' in t
  return role(r'新除侍中、中書令([^，。]+)，')
 if kind=='gift':
  if term.startswith('致'):return role(r'([^，。]+)至郡，致[^，。]+數斛酒')
  if term.startswith('可賜'):return role(r'新除侍中、中書令([^，。]+)，')
  # The deceased is the named ongoing subject of the year-opening command;
  # 輿駕 is separately the mourner, not the recipient of the ensuing funeral decree.
  return role(r'^三年元會，詔([^，。]+)乘小輿升殿。') and '乃拜受焉。是冬薨於府，時年六十六。輿駕出臨哭，'+term+'。' in t
 return False

def collective_members_valid(h,p,ch):
 t=p['text'];b=h['collective_designation'];owner=biography_topic(ch)['person_id']
 x=re.match(r'[^，。]+，選([^，。]+)爲長史，勑與河南([^、。]+)、濟陽([^、。]+)、彭城([^，。]+)俱入侍[^，。]+，時號爲天子四友。',t)
 if x is None:return False
 members=[next((m for m in p['mentions']if m['start']==x.start(i)and m['end']==x.end(i)),None)for i in range(1,5)]
 return all(members) and members[0].get('person_id')==owner and [m['id']for m in members]==b['member_mention_ids'] and [m.get('person_id')for m in members]==b['member_person_ids']

def service_duration_valid(h,p,ch):
 d=h['reported_duration'];t=p['text']
 # A local office slot governs 在郡...視事, not the earlier 國子博士.
 return (h['person_id']==biography_topic(ch)['person_id'] and h['title']=='義興太守'
  and d['source_term']=='視事三年' and d['source_number']=='三' and d['value']==3
  and '五年，出爲冠軍將軍、義興太守，加秩中二千石。在郡' in t
  and re.search(r'在郡[^。]*。[^。]*視事三年',t) is not None)
