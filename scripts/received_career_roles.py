"""Finite received career clauses: position-bound grammatical roles, no person-ID/name whitelist.
A frame is reviewed syntax, not a source-supplied executable or NLU inference.
"""
import re,hashlib
FRAMES={'early_recruitment': ('<issuer>為{principal}召<subject>署{office1}<recommender>舉為{office2}',
                       [('office1', 'subject', 'office', 'grant', 'staff_appointment', None, None),
                        ('office2', 'subject', 'office', 'grant', 'recommended_appointment', None, None)]),
 'legal_office_series': ('<issuer>曰<subject>執之是也又引經典有意使孤歎息由是為{office1}轉{office2}{time}為{office3}',
                         [('office1', 'subject', 'office', 'grant', 'appointment', None, None),
                          ('office2', 'subject', 'office', 'transfer', 'transfer', None, None),
                          ('office3', 'subject', 'office', 'grant', 'appointment', 'time', None)]),
 'accession_and_provincial_series': ('<ruler>踐阼徙{office1}出為{office2}{place1}{place2}二郡{suffix}<ruler_repeat>以譙舊鄉故大徙民充之以為屯田而譙土地墝瘠百姓窮困<subject>愍之上表徙民於梁國就沃衍失<ruler_repeat2>意雖聽<subject_repeat>所表心猶恨之遂左遷<subject_repeat2>使將徙民為{office3}<subject_repeat3>心在利民躬自臨視擇居美田百姓頼之遷{place3}{place4}{suffix2}',
                                     [('office1', 'subject', 'office', 'transfer', 'transfer', '文帝踐阼', None),
                                      ('office2', 'subject', 'office', 'grant', 'appointment', None, None),
                                      ('place1', 'subject', 'office', 'grant', 'sequential_appointment', None, 'suffix'),
                                      ('place2', 'subject', 'office', 'grant', 'sequential_appointment', None, 'suffix'),
                                      ('office3', 'subject', 'office', 'grant', 'demoted_appointment', None, None),
                                      ('place3', 'subject', 'office', 'transfer', 'sequential_transfer', None, 'suffix2'),
                                      ('place4', 'subject', 'office', 'transfer', 'sequential_transfer', None, 'suffix2')]),
 'dated_court_service': ('{time}入為{office}先是{otheroffice}<other>受詔定律未就<subject>上論古今科律之意',
                         [('office', 'subject', 'office', 'grant', 'court_appointment', 'time', None)]),
 'proven_court_promotion': ('{duration}多所駮爭詔曰官人秩才聖帝所難必須良佐進可替否{oldoffice}<subject>禀性貞固心平體正可謂明試有功不懈于位者也其以<subject_repeat>為{office}',
                            [('office', 'subject', 'office', 'grant', 'promotion', None, None)]),
 'power_and_restoration_series': ('<ruler>即位賜爵{rank1}時<minister>秉權將樹其黨徙<subject>{office1}以侍中<replacement>代<subject_repeat>頃之出<subject_repeat2>為{office2}司隸<accuser>又枉奏{departure}衆論多訟之乃以<subject_repeat3>為{office3}<minister_repeat>等見收太傅<regent>使<subject_repeat4>行{office4}治其獄復為{office5}加{office6}封{rank2}轉為{office7}故{duty}加{office8}',
                                  [('office1', 'subject', 'office', 'transfer', 'transfer', None, None),
                                   ('rank1', 'subject', 'noble_rank', 'grant', 'enfeoffment', '齊王即位', None),
                                   ('office2', 'subject', 'office', 'grant', 'appointment', None, None),
                                   ('office3', 'subject', 'office', 'grant', 'appointment', None, None),
                                   ('office4', 'subject', 'office', 'grant', 'acting_office', None, None),
                                   ('office5', 'subject', 'office', 'grant', 'reappointment', None, None),
                                   ('office6', 'subject', 'office', 'grant', 'additional_office', None, None),
                                   ('rank2', 'subject', 'noble_rank', 'grant', 'enfeoffment', None, None),
                                   ('office7', 'subject', 'office', 'transfer', 'transfer_with_continued_duty', None, None),
                                   ('office8', 'subject', 'office', 'grant', 'additional_office', None, None)]),
 'late_advancement_and_children': ('<ruler>即位進封{rank1}封一子{childrank}<rebel>作亂大將軍<regent>出征<subject>綱紀後事加{office1}{time}{departure}遷為{office2}固推{candidateoffice1}<candidate1>{candidateoffice2}<candidate2>{candidateoffice3}<candidate3>詔使使者即授印綬進爵封{rank2}邑{number}{unit}{deathdate}薨諡曰{postname}孫<heir>嗣<subject_repeat>子<son1><son2>{sonsdate}<son1_repeat>為{sonoffice1}<son2_repeat>{sonoffice2}',
                                   [('rank1', 'subject', 'noble_rank', 'grant', 'rank_advancement', '高貴鄉公即位', None),
                                    ('office1', 'subject', 'office', 'grant', 'additional_office', None, None),
                                    ('office2', 'subject', 'office', 'transfer', 'appointment_with_explicit_investiture', 'time', None),
                                    ('rank2', 'subject', 'noble_rank', 'grant', 'rank_advancement', None, None),
                                    ('postname', 'subject', 'honorific', 'posthumous_naming', 'posthumous_name', None, None),
                                    ('sonoffice1', 'son1', 'office', 'attestation', 'source_report', 'sonsdate', None),
                                    ('sonoffice2', 'son2', 'office', 'attestation', 'source_report', 'sonsdate', None)]),
 'noted_son_career': ('<subject>{time}為{office}{duty}{deathdate}卒追贈{postoffice}{privilege}',
                      [('office', 'subject', 'office', 'grant', 'appointment', 'time', None),
                       ('postoffice', 'subject', 'office', 'posthumous_grant', 'posthumous_office', None, None),
                       ('privilege', 'subject', 'honorific', 'posthumous_grant', 'posthumous_privilege', None, None)]),
 'grandson_disability_and_service': ('<subject>高朗經博有美於<comparison>起家{office1}{departure}朝廷器重之就家以為{office2}遷{office3}{time}為{office4}',
                                     [('office1', 'subject', 'office', 'grant', 'initial_appointment', None, None),
                                      ('office2', 'subject', 'office', 'grant', 'appointment_at_home', None, None),
                                      ('office3', 'subject', 'office', 'transfer', 'transfer', None, None),
                                      ('office4', 'subject', 'office', 'grant', 'appointment', 'time', None)]),
 'father_and_named_sons_report': ('<father>及子<son1><son2>並至{office}',
                                  [('office', 'father', 'office', 'attestation', 'reported_attainment', None, None),
                                   ('office', 'son1', 'office', 'attestation', 'reported_attainment', None, None),
                                   ('office', 'son2', 'office', 'attestation', 'reported_attainment', None, None)]),
 'northern_service_and_unassumed_calls': ('<subject>善著文章洛陽傾覆北投<principal><principal_repeat>以為{office}<principal_repeat2>敗<subject_repeat>歸<host><ruler>之初累召為{offer1}{offer2}{nonassumption}',
                                          [('office', 'subject', 'office', 'grant', 'staff_appointment', None, None)]),
 'note_father_career': ('<subject>剛毅有大節常喟然有濟世之志不茍合取容{decline}{time}徴{office1}出補{office2}{departure}作尚書章句禮記解詁稍遷{office3}{office4}<rebel>起以<subject_repeat>為{office5}征<rebel_repeat>失利{penalty}頃之復以為{office6}',
                        [('office1', 'subject', 'office', 'grant', 'summoned_appointment', 'time', None),
                         ('office2', 'subject', 'office', 'grant', 'appointment', None, None),
                         ('office3', 'subject', 'office', 'transfer', 'promotion', None, None),
                         ('office4', 'subject', 'office', 'transfer', 'promotion', None, None),
                         ('office5', 'subject', 'office', 'grant', 'military_appointment', None, None),
                         ('office6', 'subject', 'office', 'grant', 'reappointment', None, None)]),
 'old_illness_departure': ('<subject>{departure}隱居{place}', [])}

def analyse(record,ch):
 b=record['source_career_role'];p=next(p for p in ch['paragraphs']if p['id']==b['paragraph_id']);t=p['text'];ms={m['id']:m for m in p['mentions']};roles={k:ms[v]for k,v in b['roles'].items()};fields=b['fields'];scope=b['scope_anchor'];template,slots=FRAMES[b['rule']]
 def exact(a):return set(a)=={'paragraph_id','start','end','surface'}and a['paragraph_id']==p['id']and type(a['start'])is int and type(a['end'])is int and 0<=a['start']<a['end']<=len(t)and t[a['start']:a['end']]==a['surface']
 assert b['kind']=='received_career_role_frame'and b['human_reviewed']is False and b['source_revision']==ch['source']['revision_id']and b['paragraph_sha256']==hashlib.sha256(t.encode()).hexdigest()and exact(scope)
 ev,=record['evidence'];assert ev['work_id']==ch['work_id']and ev['book_id']==ch['book_id']and ev['source_id']==ch['source_id']and ev['chapter_id']==ch['id']and ev['paragraph_id']==p['id']and ev['quote']==t
 tokens=re.split(r'(<[^>]+>|\{[^}]+\})',template);cursor=scope['start'];usedr=set();usedf=set()
 for token in tokens:
  if not token:continue
  if token[0]=='<':
   k=token[1:-1];x=roles[k];assert x['kind']=='person'and x['start']==cursor and t[x['start']:x['end']]==x['surface'];usedr.add(k)
  elif token[0]=='{':
   k=token[1:-1];x=fields[k];assert exact(x)and x['start']==cursor and (k in ('nonassumption','decline') or not re.search(r'[曰云詔未不欲請薨卒。；！？「」『』]',x['surface']))and len(x['surface'])<=20;usedf.add(k)
  else:assert t.startswith(token,cursor);cursor+=len(token);continue
  cursor=x['end']
 assert cursor==scope['end']and set(roles)==usedr and set(fields)==usedf
 for k,m in roles.items():
  base=k.split('_repeat')[0]
  if base!=k:assert roles[base]['person_id']==m['person_id']
 # Primary-text main-career frames must name the biography topic. Appended source biographies use their local named subject.
 if p['text_layer']=='received_chapter':
  head=ch['paragraphs'][0];hm=head['mentions'][0];assert hm['start']==0 and head['text'][hm['end']:].startswith('字')and roles['subject']['person_id']==hm['person_id']
 for m in p['mentions']:
  if m.get('kind')!='person'or not scope['start']<=m['start']<scope['end']:continue
  if m['id']in b['roles'].values():continue
  matching=[slot for slot in slots if fields[slot[0]]['start']<=m['start']<m['end']<=fields[slot[0]]['end']]
  assert matching and all(roles[slot[1]]['person_id']==m['person_id']for slot in matching)
 return p,roles,fields,slots

def holding_valid(h,ch,root=None):
 if isinstance(h,dict)and h.get('source_career_role',{}).get('kind')=='wyd_song044_noble_grant':
  try:from scripts.wyd_song044_nobles import holding_valid as noble_valid
  except ImportError:from wyd_song044_nobles import holding_valid as noble_valid
  return noble_valid(h,ch,root)
 if h.get('source_career_role',{}).get('kind')=='punctuated_biography_career_frame':
  try:from scripts.punctuated_biography_career import holding_valid as punctuated_valid
  except ImportError:from punctuated_biography_career import holding_valid as punctuated_valid
  return punctuated_valid(h,ch)
 if h.get('source_career_role',{}).get('kind')=='epitaph_named_head_career_clause':
  try:from scripts.epitaph_career_roles import holding_valid as epitaph_valid
  except ImportError:from epitaph_career_roles import holding_valid as epitaph_valid
  return epitaph_valid(h,ch)
 if h.get('source_career_role',{}).get('kind')=='layered_biographical_role_frame':
  try:from scripts.layered_biography_titles import holding_valid as layered_valid
  except ImportError:from layered_biography_titles import holding_valid as layered_valid
  return layered_valid(h,ch)
 try:
  p,rs,fs,slots=analyse(h,ch);b=h['source_career_role'];slot=next(x for x in slots if x[0]==b['slot']and x[1]==b['recipient_role']);name,recipient,kind,mode,semantic,time,suffix=slot;x=fs[name];role=rs[recipient];ev,=h['evidence'];a,=h['attestations'];title=x['surface']+(fs[suffix]['surface']if suffix else'')
  assert h['person_id']==role['person_id']and h['title']==title and h['kind']==kind and h['mode']==mode and h['appointment_role']==semantic and h['status']=='source_attested'and h['human_reviewed']is False
  assert a['paragraph_id']==p['id']and a['start']==x['start']and a['end']==x['end']and a['surface']==x['surface']and a['person_mention_id']==role['id']and a['date_expression']is None
  assert ev==dict(work_id=ch['work_id'],book_id=ch['book_id'],source_id=ch['source_id'],chapter_id=ch['id'],paragraph_id=p['id'],quote=p['text'],person_mention_id=role['id'])
  date=fs[time]['surface']if time in fs else time;unknown=dict(status='unknown',date_expression=None,evidence=[]);start=unknown if mode=='attestation'else dict(status='source_event',event_type=mode,date_expression=date,evidence=h['evidence']);actual=h['effective_period']['start'];norm=actual.get('normalized_date')
  if norm:
   assert time in fs and norm['source_expression']==date and norm['original_quote']==p['text']and norm['evidence']==h['evidence'];mapping=norm['regnal_year_mapping'];assert date==mapping['era_name']+mapping['source_number']+'年'and norm['year']==mapping['start_ce_year']+mapping['regnal_year']-1;start['normalized_date']=norm
  assert h['effective_period']==dict(start=start,end=unknown)
  if suffix:assert h['shared_title_suffix']==dict(component_anchor=x,suffix_anchor=fs[suffix],expansion_status='editorial_preferred',qualification='來源共享職名尾字；展開顯示不改原文，不推同時任職或任年。')
  else:assert 'shared_title_suffix'not in h
  return True
 except(KeyError,TypeError,ValueError,AssertionError,StopIteration,IndexError):return False

def detail_valid(d,ch,holdings):
 if d.get('source_career_role',{}).get('kind')=='punctuated_biography_career_frame':
  try:from scripts.punctuated_biography_career import detail_valid as punctuated_detail_valid
  except ImportError:from punctuated_biography_career import detail_valid as punctuated_detail_valid
  return punctuated_detail_valid(d,ch,holdings)
 if d.get('source_career_role',{}).get('kind')=='epitaph_named_head_military_duty':
  try:from scripts.epitaph_career_roles import detail_valid as epitaph_detail_valid
  except ImportError:from epitaph_career_roles import detail_valid as epitaph_detail_valid
  return epitaph_detail_valid(d,ch)
 if d.get('source_career_role',{}).get('kind')=='layered_biographical_role_frame':
  try:from scripts.layered_biography_titles import detail_valid as layered_detail_valid
  except ImportError:from layered_biography_titles import detail_valid as layered_detail_valid
  return layered_detail_valid(d,ch,holdings)
 try:
  p,rs,fs,slots=analyse(d,ch);b=d['source_career_role'];ev,=d['evidence'];subject=rs[b['recipient_role']];v=d['values'];kind=d['kind'];slot=b['slot'];assert d['person_id']==subject['person_id']and d['human_reviewed']is False and d['status']=='source_attested'and ev['quote']==p['text']and ev['person_mention_id']==subject['id']and ev['source_id']==ch['source_id']and ev['chapter_id']==ch['id']and d['date_expression']is None
  f=fs[slot];assert d['source_anchor']==f and d['source_term']==f['surface']and d['paragraph_sha256']==b['paragraph_sha256']and d['source_revision']==b['source_revision']
  rule=b['rule']
  def linked(title):
   h=holdings[v['linked_holding_id']];return h['person_id']==d['person_id']and h['title']==title and holding_valid(h,ch)
  if rule=='proven_court_promotion'and slot=='duration':return kind=='office_duration'and f['surface']=='在職三年'and v==dict(duration_years=3,source_number='三',unit='年',linked_holding_id=v['linked_holding_id'],tenure_end_year=None,derived_start_year=None)and linked(fs['oldoffice']['surface'])and holdings[v['linked_holding_id']]['source_career_role']['rule']=='dated_court_service'and holdings[v['linked_holding_id']]['evidence'][0]['paragraph_id']==p['id']
  if rule=='power_and_restoration_series'and slot=='duty':return kind=='official_duty'and f['surface']=='典選舉'and v==dict(duty_code='personnel_selection',linked_holding_id=v['linked_holding_id'],continued_after_transfer=True)and linked(fs['office7']['surface'])and holdings[v['linked_holding_id']]['source_career_role']['rule']==rule and holdings[v['linked_holding_id']]['source_career_role']['slot']=='office7'
  if rule=='noted_son_career'and slot=='duty':return kind=='official_duty'and f['surface']=='領選'and v==dict(duty_code='personnel_selection',source_term='領選',linked_holding_id=v['linked_holding_id'])and linked(fs['office']['surface'])
  if rule=='late_advancement_and_children'and slot=='childrank':return kind=='unnamed_family_title_grants'and v==dict(recipient_group_source_term='一子',recipient_person_ids=[],biological_children_only=False,grants=[dict(source_rank=f['surface'],recipient_count=1,source_number='一')])
  if rule=='late_advancement_and_children'and slot=='number':return kind=='fief_household_count'and f['surface']=='二十三百'and v==dict(total=2300,total_source_number=f['surface'],unit_source_name=fs['unit']['surface'],increase=None,actual_revenue=None,linked_holding_id=v['linked_holding_id'])and linked(fs['rank2']['surface'])
  if kind=='office_departure':
   allowed={('old_illness_departure','departure'):('old_age_illness_departure_unspecified_office',None),('note_father_career','departure'):('illness_departure','office2'),('power_and_restoration_series','departure'):('dismissal_after_accusation','office2'),('late_advancement_and_children','departure'):('illness_relinquishment_report',None),('grandson_disability_and_service','departure'):('disability_departure','office1')}
   code,office=allowed[(rule,slot)];return v==dict(departure_code=code,linked_holding_id=v.get('linked_holding_id'),date_unknown=True,all_other_offices_ended=False)and (linked(fs[office]['surface'])if office else v['linked_holding_id']is None)
  if rule=='note_father_career'and slot=='decline':return kind=='unaccepted_recruitment_report'and f['surface']=='不應州郡命召'and v==dict(source_group='州郡',specific_office=None,service_attested=False)
  if rule=='note_father_career'and slot=='penalty':return kind=='official_penalty_report'and f['surface']=='抵罪'and v==dict(source_outcome='抵罪',dismissal_explicit=False,death_sentence_inferred=False)
  return False
 except(KeyError,TypeError,ValueError,AssertionError,StopIteration,IndexError):return False

def unassumed_valid(q,ch):
 try:
  p,rs,fs,slots=analyse(q,ch);b=q['source_career_role'];field=fs[b['slot']];m=rs['subject'];ev,=q['evidence'];assert b['rule']=='northern_service_and_unassumed_calls'and b['slot']in('offer1','offer2')and b['recipient_role']=='subject'and q['person_id']==m['person_id']and q['person_mention_id']==m['id']and q['title']==field['surface']and q['role_anchor']==field and q['non_assumption_anchor']==fs['nonassumption']and fs['nonassumption']['surface']=='不得南赴'and q['proposal_kind']=='unassumed_appointment'and q['outcome']=='not_assumed'and q['status']=='contextual_provisional'and q['human_reviewed']is False and q['effective_service_attested']is False and q['appointment_stage']=='appointment'and q['non_assumption_kind']=='did_not_take_up'and q['appointment_anchor']==dict(paragraph_id=p['id'],start=fs['offer1']['start']-3,end=fs['offer1']['start'],surface='累召為')and p['text'][fs['offer1']['start']-3:fs['offer1']['start']]=='累召為'and ev['quote']==p['text']and ev['person_mention_id']==m['id'];return True
 except(KeyError,TypeError,ValueError,AssertionError,StopIteration,IndexError):return False

def event_valid(e,ch):
 try:
  p,rs,fs,slots=analyse(e,ch);b=e['source_career_role'];heir=rs['heir'];subject=rs['subject'];ev,=e['evidence'];a=e['succession_anchor'];assert b['rule']=='late_advancement_and_children'and b['slot']=='heir'and b['recipient_role']=='heir'and e['event_type']=='noble_title_succession'and e['status']=='source_attested'and e['mode']=='accession'and e['title']is None and e['holding_id']is None and e['predecessor_person_id']==subject['person_id']and e['person_id']==heir['person_id']!=subject['person_id']and e['date_expression']is None and'normalized_date'not in e and e['human_reviewed']is False and a==dict(paragraph_id=p['id'],start=heir['start']-1,end=heir['end']+1,surface='孫'+heir['surface']+'嗣')and e['source_term']==a['surface']and p['text'][a['start']:a['end']]==a['surface']and ev['quote']==p['text']and ev['person_mention_id']==heir['id']and ev['chapter_id']==ch['id']and ev['source_id']==ch['source_id'];return True
 except(KeyError,TypeError,ValueError,AssertionError,StopIteration,IndexError):return False
