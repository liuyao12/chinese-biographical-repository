"""Finite received role syntax with separately bound elided subjects across annotations."""
import hashlib,re
FRAMES={
 'named_subject_office_report':('<subject>為{office}',[('office','subject','attestation','source_report',None)]),
 'named_heir_attained_office':('<subject>嗣官至{office}',[('office','subject','attestation','reported_attainment',None)]),
 'summoned_then_governor':('{era_phase}徴為{office1}乃始起焉{year}九江蠻反四府選<subject>才兼文武拜{office2}蠻寇賔服{departure}作尚書章句三禮解詁',[('office1','subject','grant','summoned_appointment','era_phase'),('office2','subject','grant','appointment','year')]),
 'governor_after_rebellion':('會南夷反叛以<subject>嘗在九江有恩信拜為{office}<subject_repeat>深達政宜務存清靜𢎞大體而已',[('office','subject','grant','appointment',None)]),
 'court_after_governorship':('嵗餘復徴拜{office1}與{office2}<colleague1>{office3}<colleague2><colleague3><colleague4>等並在東觀校中書五經記傳補續漢記<ruler>以非急務轉為{office4}遷{office5}',[('office1','subject','grant','reappointment',None),('office2','colleague1','attestation','source_report',None),('office3','colleague2','attestation','source_report',None),('office3','colleague3','attestation','source_report',None),('office3','colleague4','attestation','source_report',None),('office4','subject','transfer','transfer',None),('office5','subject','transfer','promotion',None)]),
 'military_recruitment_with_deputy':('{year}黄巾賊起四府舉<subject>拜{office1}{credential}以{office2}<deputy>副將北軍五校士發天下諸郡兵征之連戰破賊帥<rebel>斬獲萬餘人<rebel_repeat>等走保廣宗',[('office1','subject','grant','military_appointment','year'),('credential','subject','grant','credential_authority','year'),('office2','deputy','attestation','source_report',None)]),
 'restored_after_campaign_report':('及{office1}<general>討平黄巾盛稱<subject>行師方略<general_repeat>皆資用規謀濟成其功以{same_year}復為{office2}',[('office1','general','attestation','source_report',None),('office2','subject','grant','reappointment','same_year')]),
 'prefix_office':('{office}<subject>',[('office','subject','attestation','source_report',None)]),
 'past_prefix_office':('故{office}<subject>',[('office','subject','attestation','past_source_report',None)]),
 'noted_named_son_career':('魏志曰<subject>字<style>{age}而孤以學行稱仕魏至{office1}{office2}時舉{office3}詔曰',[('office1','subject','attestation','reported_attainment',None),('office2','subject','attestation','reported_attainment',None),('office3','subject','attestation','source_report',None)]),
 'invited_adviser':('{issuer_office}<issuer>請為{office}',[]),
 'repeated_regional_calls':('州郡數命<subject>{decline}',[]),
 'dismissal_then_old_illness':('<antagonist>乃止但免<subject>官而已<subject_repeat>以老病求歸',[]),
}
# Finite nominal office vocabulary: a bare adjacency frame does not itself
# establish that arbitrary preceding prose is an office. This is deliberately
# incomplete; unrecognised titles need a separate reviewed role contract.
OFFICE_NOUNS=frozenset(('博士','內史','太守','議郎','大夫','侍中','尚書','中郎將','將軍','黄門','黃門','州牧','中郎','軍師'))
def office_noun(surface):
 if not isinstance(surface,str) or not 2<=len(surface)<=12:return False
 if any(c in surface for c in '少與俱事曰云詔非未不欲請薨卒故字為拜遷轉至'):return False
 return any(surface.endswith(noun) for noun in OFFICE_NOUNS)
def exact(p,a):
 return isinstance(a,dict)and set(a)=={'paragraph_id','start','end','surface'}and a['paragraph_id']==p['id']and type(a['start'])is int and type(a['end'])is int and 0<=a['start']<a['end']<=len(p['text'])and p['text'][a['start']:a['end']]==a['surface']
def continuation(context,ch,person_id,target_id):
 try:
  assert context['kind']=='layered_biography_subject_continuation'and context['human_reviewed']is False and context['source_revision']==ch['source']['revision_id']
  ps=ch['paragraphs'];by={p['id']:p for p in ps};assert len(by)==len(ps)
  head=by[context['head_paragraph_id']];hm=next(m for m in head['mentions']if m['id']==context['head_mention_id']);assert hm['start']==0 and hm['person_id']==person_id and head['text'][hm['end']:].startswith('字')
  prior=by[context['paragraph_id']];m=next(m for m in prior['mentions']if m['id']==context['person_mention_id']);assert m['kind']=='person'and m['person_id']==person_id and context['quote']==prior['text']
  lo,hi=ps.index(prior),ps.index(by[target_id]);assert lo<hi and context['paragraph_ids']==[p['id']for p in ps[lo:hi+1]]
  assert context['full_paragraphs']==[dict(paragraph_id=p['id'],quote=p['text'],source_position=p['source_position'])for p in ps[lo:hi+1]]
  assert prior.get('text_layer','received_chapter')=='received_chapter'and by[target_id].get('text_layer','received_chapter')=='received_chapter'
  assert all(p['text_layer']in ('witness_appended_lixian_note','witness_appended_liuban_collation')for p in ps[lo+1:hi])
  a=context['resumption_anchor'];assert exact(prior,a)and a['start']==m['start']and a['end']==len(prior['text'])and a['surface']==m['surface']+'深達政宜務存清靜𢎞大體而已'
  return True
 except(KeyError,TypeError,ValueError,StopIteration,AssertionError):return False
def analyse(h,ch):
 b=h['source_career_role'];p=next(p for p in ch['paragraphs']if p['id']==b['paragraph_id']);t=p['text'];ms={m['id']:m for m in p['mentions']};a=b['scope_anchor'];f=b['fields'];ctx=b.get('subject_context');allms={m['id']:m for q in ch['paragraphs']for m in q['mentions']}
 assert b['kind']=='layered_biographical_role_frame'and b['human_reviewed']is False and b['source_revision']==ch['source']['revision_id']and b['paragraph_sha256']==hashlib.sha256(t.encode()).hexdigest()and exact(p,a)
 roles={k:(allms if k=='subject'and ctx else ms)[v]for k,v in b['roles'].items()}
 if ctx:assert b['rule']=='court_after_governorship'and continuation(ctx,ch,roles['subject']['person_id'],p['id'])and roles['subject']['id']==ctx['person_mention_id']
 template,slots=FRAMES[b['rule']];pos=a['start'];usedr=set();usedf=set()
 for token in re.split(r'(<[^>]+>|\{[^}]+\})',template):
  if not token:continue
  if token.startswith('<'):k=token[1:-1];x=roles[k];assert x['kind']=='person'and x['start']==pos and t[x['start']:x['end']]==x['surface'];usedr.add(k)
  elif token.startswith('{'):
   k=token[1:-1];x=f[k];assert exact(p,x)and x['start']==pos and len(x['surface'])<=20 and (k=='decline'or not any(w in x['surface']for w in '曰云詔非未不欲請薨卒「」'));usedf.add(k)
  else:assert t.startswith(token,pos);pos+=len(token);continue
  pos=x['end']
 assert pos==a['end']and set(f)==usedf and set(roles)==usedr|({'subject'}if ctx else set())
 for k,x in roles.items():
  if '_repeat'in k:assert roles[k.split('_repeat')[0]]['person_id']==x['person_id']
 for m in p['mentions']:
  if m.get('kind')!='person'or not a['start']<=m['start']<a['end']or m['id']in b['roles'].values():continue
  ss=[slot for slot in slots if f[slot[0]]['start']<=m['start']<m['end']<=f[slot[0]]['end']];assert ss and all(roles[slot[1]]['person_id']==m['person_id']for slot in ss)
 if b['rule']in ('summoned_then_governor','governor_after_rebellion','military_recruitment_with_deputy','restored_after_campaign_report'):
  hm=ch['paragraphs'][0]['mentions'][0];assert roles['subject']['person_id']==hm['person_id']
 return p,roles,f,slots
def holding_valid(h,ch):
 try:
  if h['source_career_role']['rule']=='appellation_title_attestation':return appellation_valid(h,ch)
  p,roles,fs,slots=analyse(h,ch);b=h['source_career_role'];slot=next(s for s in slots if s[0]==b['slot']and s[1]==b['recipient_role']);name,recipient,mode,semantic,time=slot;m=roles[recipient];a,=h['attestations'];e,=h['evidence'];unknown=dict(status='unknown',date_expression=None,evidence=[])
  assert name=='credential' or office_noun(fs[name]['surface'])
  assert h['person_id']==m['person_id']and h['title']==fs[name]['surface']and h['kind']==('unclassified'if name=='credential'else'office')and h['mode']==mode and h['appointment_role']==semantic and h['status']=='source_attested'and h['human_reviewed']is False
  assert a['paragraph_id']==p['id']and a['start']==fs[name]['start']and a['end']==fs[name]['end']and a['surface']==fs[name]['surface']and a['person_mention_id']==m['id']
  if a.get('date_expression')is not None:
   assert b['rule']=='past_prefix_office'and re.fullmatch(r'.{2}[初中末]',a['date_expression'])and p['text'].startswith(a['date_expression'])and a['normalized_date_range']['source_expression']==a['date_expression']and a['normalized_date_range']['evidence']==h['evidence']
  else:assert 'normalized_date_range'not in a
  assert e['quote']==p['text']and e['person_mention_id']==m['id']and e['chapter_id']==ch['id']and all(e[k]==ch[k]for k in ('work_id','book_id','source_id'))
  date=fs[time]['surface']if time else None;start=unknown if mode=='attestation'else dict(status='source_event',event_type=mode,date_expression=date,evidence=h['evidence']);actual=h['effective_period']['start']
  if 'normalized_date'in actual:assert time and actual['normalized_date']['source_expression']==date;start['normalized_date']=actual['normalized_date']
  if 'normalized_date_range'in actual:assert time and actual['normalized_date_range']['source_expression']==date;start['normalized_date_range']=actual['normalized_date_range']
  assert h['effective_period']==dict(start=start,end=unknown)
  if ctx:=b.get('subject_context'):
   if recipient=='subject':assert e.get('context')==ctx and a.get('context')==ctx
  return True
 except(KeyError,TypeError,ValueError,AssertionError,StopIteration):return False
def appellation_valid(h,ch):
 try:
  b=h['source_career_role'];p=next(p for p in ch['paragraphs']if p['id']==b['paragraph_id']);m=next(m for m in p['mentions']if m['id']==b['roles']['subject']);f=b['fields'];prefix=f['prefix'];title=f['title'];e,=h['evidence'];a,=h['attestations'];unknown=dict(status='unknown',date_expression=None,evidence=[])
  assert b['kind']=='layered_biographical_role_frame'and b['source_revision']==ch['source']['revision_id']and b['paragraph_sha256']==hashlib.sha256(p['text'].encode()).hexdigest()and b['human_reviewed']is False and set(b['roles'])=={'subject'}and set(f)=={'prefix','title'}
  assert exact(p,prefix)and exact(p,title)and prefix['start']==m['start']and prefix['end']==title['start']and title['end']==m['end']and 1<=len(prefix['surface'])<=2 and b['scope_anchor']==dict(paragraph_id=p['id'],start=m['start'],end=m['end'],surface=m['surface'])
  assert office_noun(title['surface'])
  assert m['kind']=='person'and h['person_id']==m['person_id']and h['title']==title['surface']and h['mode']=='attestation'and h['kind']=='office'and h['appointment_role']=='source_appellation'and h['status']=='source_attested'and h['human_reviewed']is False
  assert a['start']==title['start']and a['end']==title['end']and a['surface']==title['surface']and a['person_mention_id']==m['id']and a['paragraph_id']==p['id']and a['date_expression']is None and e['quote']==p['text']and e['person_mention_id']==m['id']and e['chapter_id']==ch['id']and e['source_id']==ch['source_id']and h['effective_period']==dict(start=unknown,end=unknown)
  return True
 except(KeyError,TypeError,ValueError,AssertionError,StopIteration):return False
def title_context_valid(a,h,ch):
 try:
  ctx=a['context'];return ctx==h['source_career_role']['subject_context']and continuation(ctx,ch,h['person_id'],a['paragraph_id'])and holding_valid(h,ch)
 except(KeyError,TypeError):return False
def same_paragraph_year_valid(date,chapters):
 try:
  b=date['narrative_era_scope'];ch=chapters[b['chapter_id']];p=next(p for p in ch['paragraphs']if p['id']==b['paragraph_id']);t=p['text'];aa=b['era_anchor'];bb=b['event_anchor'];head=ch['paragraphs'][0]['mentions'][0]
  assert b['kind']=='same_paragraph_explicit_year'and b['source_id']==ch['source_id']and b['source_revision']==ch['source']['revision_id']and b['paragraph_sha256']==hashlib.sha256(t.encode()).hexdigest()and b['full_quote']==t
  assert exact(p,aa)and exact(p,bb)and aa['end']<bb['start']and aa['surface']==date['relative_year_reference']['era_expression']and bb['surface']==date['source_expression']=='其年'
  assert b['biography_subject_person_id']==head['person_id']and date['relative_year_reference']['antecedent_expression']==aa['surface']
  # An intervening dated era would invalidate a same-year carry; quotations are not silently ignored.
  assert not re.search(r'[^其]{2}[元一二三四五六七八九十]+年',t[aa['end']:bb['start']])
  assert not any(term in t[aa['end']:bb['start']]for term in ('明年','翌年','次年','後年'))
  assert all(e['paragraph_id']==p['id']and e['quote']==t for e in date['evidence'])
  return True
 except(KeyError,TypeError,ValueError,StopIteration,AssertionError):return False
def offered_errors(q,ch,pids):
 try:
  p,rs,fs,slots=analyse(dict(source_career_role=q['source_appointment_context']),ch);b=q['source_appointment_context'];ctx=q['recipient_context'];head=ch['paragraphs'][0];hm=head['mentions'][0];a=q['role_anchor'];issuer=rs['issuer']
  assert b['rule']=='invited_adviser'and q['person_id']==hm['person_id']in pids and q['person_id']!=issuer['person_id']and q['title']==fs['office']['surface']and a==fs['office']
  assert ctx==dict(kind='biography_head_recipient',paragraph_id=head['id'],person_mention_id=hm['id'],quote=head['text'])
  assert q['proposal_kind']=='appointment_service_unreported'and q['appointment_stage']=='invitation'and q['outcome']=='not_reported'and q['effective_service_attested']is False and not any(k in q for k in ('non_assumption_anchor','non_assumption_kind'))
  assert q['date_expression']is None and q['status']=='contextual_provisional'and q['human_reviewed']is False and q['person_mention_id']==hm['id']
  e,=q['evidence'];assert e['quote']==p['text']and e['chapter_id']==ch['id']and e['source_id']==ch['source_id']and e['person_mention_id']==hm['id']and e['context']==ctx
  return []
 except(KeyError,TypeError,ValueError,StopIteration,AssertionError):return ['延請職任須綁傳主、明示請者與完整原句，未載就任不等未任']
def family_valid(a,paragraphs,chapters):
 try:
  q=a['qualifiers'];b=q['source_clause_binding'];e,=a['evidence'];cid,p=paragraphs[e['paragraph_id']];ch=chapters[cid];t=p['text'];ms={m['id']:m for m in p['mentions']};rs={k:ms[v]for k,v in b['roles'].items()};child=rs['child'];parent=rs['parent'];s=e['subject_person_mention_id'];o=e['object_person_mention_id'];scope=b['clause_anchor']
  assert set(q)=={'source_term','lineage','source_clause_binding'}and q['lineage']=='paternal'and a['predicate']=='father'and a['subject_person_id']==child['person_id']!=parent['person_id']==a['object_person_id']and child['id']==s and parent['id']==o
  assert a['human_reviewed']is False and a['status']=='source_attested'and e['chapter_id']==cid and e['quote']==t and all(e[k]==ch[k]for k in ('work_id','book_id','source_id'))and b['source_revision']==ch['source']['revision_id']and b['paragraph_sha256']==hashlib.sha256(t.encode()).hexdigest()and exact(p,scope)
  assert all(m['kind']=='person'and t[m['start']:m['end']]==m['surface']for m in rs.values())
  if b['rule']=='layered_child_named_titled_father':
   office=b['office_anchor'];assert set(rs)=={'child','parent'}and exact(p,office)and scope['surface']==child['surface']+'父'+office['surface']+parent['surface']and child['start']==scope['start']and office['start']==child['end']+1 and parent['start']==office['end']and parent['end']==scope['end']and q['source_term']=='父'+office['surface']+parent['surface']
  elif b['rule']=='layered_parent_named_son_note':
   assert set(rs)=={'child','parent'}and p['text_layer']=='witness_appended_lixian_note'and scope['start']==parent['start']==0 and scope['surface']==parent['surface']+'子'+child['surface']+'也'and child['start']==parent['end']+1 and q['source_term']=='子'+child['surface']
  elif b['rule']=='layered_biography_commemorated_parent_son':
   assert set(rs)=={'child','parent','parent_pronoun'}and scope['surface']=='子'+child['surface']+'知名'and child['start']==scope['start']+1 and scope['end']==len(t)and q['source_term']=='子'+child['surface']
   head=next(pp for pp in ch['paragraphs']if pp['id']==b['biography_head_paragraph_id']);hm=next(mm for mm in head['mentions']if mm['id']==b['biography_head_mention_id']);assert hm['start']==0 and head['text'][hm['end']:].startswith('字')and hm['person_id']==parent['person_id']
   assert t[:parent['start']].endswith('故北中郎將')and t[parent['end']:].startswith('名著海内學為儒宗')and t[:scope['start']].endswith('以彰厥徳')and rs['parent_pronoun']['surface']=='其'and rs['parent_pronoun']['person_id']==parent['person_id']and t[rs['parent_pronoun']['end']:].startswith('子孫')
  else:return False
  return True
 except(KeyError,TypeError,ValueError,StopIteration,AssertionError):return False
def teaching_valid(a,paragraphs):
 try:
  e,=a['evidence'];cid,p=paragraphs[e['paragraph_id']];b=a['qualifiers']['teaching_clause_binding'];ms={m['id']:m for m in p['mentions']};rs={k:ms[v]for k,v in b['roles'].items()};head,fellow,teacher=(rs[k]for k in ['head','fellow','teacher']);aa=b['clause_anchor'];t=p['text'];learner=rs[b['learner_role']]
  assert b['kind']=='biography_classmates_studied_teacher'and b['learner_role']in ('head','fellow')and head['start']==0 and t[head['end']:].startswith('字')and exact(p,aa)and aa['surface']=='少與'+fellow['surface']+'俱事'+teacher['surface']+'能通古今學'and fellow['start']==aa['start']+2 and teacher['start']==fellow['end']+2
  assert a['predicate']=='teacher'and a['human_reviewed']is False and a['status']=='source_attested'and a['subject_person_id']==learner['person_id']!=teacher['person_id']==a['object_person_id']and e['subject_person_mention_id']==learner['id']and e['object_person_mention_id']==teacher['id']and e['quote']==t and a['qualifiers']['source_term']==aa['surface']and a['qualifiers']['relationship_basis']=='teaching'
  return True
 except(KeyError,TypeError,ValueError,StopIteration,AssertionError):return False
def death_context_valid(context,event,ch,e):
 try:
  assert context['kind']=='layered_biography_death_continuation'and context['source_revision']==ch['source']['revision_id']and context['human_reviewed']is False
  ps=ch['paragraphs'];by={p['id']:p for p in ps};prior=by[context['paragraph_id']];target=by[e['paragraph_id']];m=next(m for m in prior['mentions']if m['id']==context['person_mention_id']);issuer=next(m for m in prior['mentions']if m['id']==context['issuer_mention_id']);hm=ps[0]['mentions'][0]
  assert hm['start']==0 and ps[0]['text'][hm['end']:].startswith('字')and hm['person_id']==m['person_id']==event['person_id']!=issuer['person_id']and m['kind']==issuer['kind']=='person'
  assert prior['text'][m['end']:].startswith('以老病求歸')and prior['text'].endswith('冀州牧'+issuer['surface']+'請為軍師')and m['end']<issuer['start']
  lo,hi=ps.index(prior),ps.index(target);assert lo<hi and context['paragraph_ids']==[p['id']for p in ps[lo:hi+1]]and context['full_paragraphs']==[dict(paragraph_id=p['id'],quote=p['text'],source_position=p['source_position'])for p in ps[lo:hi+1]]
  assert all(p.get('text_layer')in ('witness_appended_lixian_note','witness_appended_liuban_collation')for p in ps[lo+1:hi])and target.get('text_layer','received_chapter')=='received_chapter'
  assert event['event_type']=='death'and event['source_term']=='卒'and target['text'].startswith(event['date_expression']+'卒臨困敕其子儉葬於土穴')and not any(mm.get('person_id')for mm in target['mentions'])and e['quote']==target['text']and context['quote']==prior['text']and e['person_mention_id']==m['id']
  return True
 except(KeyError,TypeError,ValueError,StopIteration,AssertionError):return False
def detail_valid(d,ch,holdings):
 try:
  p,rs,fs,slots=analyse(d,ch);b=d['source_career_role'];a=d['source_anchor'];e,=d['evidence'];v=d['values'];m=rs['subject'];rule=b['rule']
  assert d['person_id']==m['person_id']and d['human_reviewed']is False and d['status']=='source_attested'and d['date_expression']is None and exact(p,a)and d['source_term']==a['surface']and e['quote']==p['text']and e['person_mention_id']==m['id']and d['paragraph_sha256']==b['paragraph_sha256']and d['source_revision']==b['source_revision']
  if rule=='repeated_regional_calls':return a==fs['decline']and a['surface']=='皆不就'and d['kind']=='unaccepted_recruitment_report'and v==dict(source_group='州郡',specific_office=None,service_attested=False)
  if rule=='summoned_then_governor':
   h=holdings[v['linked_holding_id']];return d['kind']=='office_departure'and a==fs['departure']and a['surface']=='以疾去官'and v==dict(departure_code='illness_departure',linked_holding_id=h['id'],date_unknown=True,all_other_offices_ended=False)and h['person_id']==d['person_id']and h['title']==fs['office2']['surface']and holding_valid(h,ch)
  if rule=='dismissal_then_old_illness':return d['kind']=='office_departure'and a['surface']=='免'+m['surface']+'官'and a['start']==m['start']-1 and v==dict(departure_code='dismissal_unspecified_office',linked_holding_id=None,date_unknown=True,all_other_offices_ended=False)
  return False
 except(KeyError,TypeError,ValueError,StopIteration,AssertionError):return False
def address_valid(a,ch):
 try:
  b=a['source_address_binding'];e,=a['evidence'];p=next(p for p in ch['paragraphs']if p['id']==e['paragraph_id']);t=p['text'];ms={m['id']:m for m in p['mentions']};rs={k:ms[v]for k,v in b['roles'].items()};scope=b['scope_anchor'];place=b['place_anchor'];subject=rs[b['subject_role']]
  assert b['kind']=='layered_biography_address'and b['source_revision']==ch['source']['revision_id']and b['paragraph_sha256']==hashlib.sha256(t.encode()).hexdigest()and exact(p,scope)and exact(p,place)and place['surface']==a['place']['source_name']and a['person_id']==subject['person_id']and e['person_mention_id']==subject['id']and e['quote']==t and e['chapter_id']==ch['id']and e['source_id']==ch['source_id']
  assert all(m['kind']=='person'and t[m['start']:m['end']]==m['surface']for m in rs.values())
  rule=b['rule']
  if rule=='biography_origin':
   s=rs['subject'];style=rs['style'];return a['relation']=='biographical_origin'and s['start']==scope['start']==0 and style['person_id']==s['person_id']and t[s['end']:style['start']]=='字'and style['end']==place['start']and scope['surface']==s['surface']+'字'+style['surface']+place['surface']+'人也'and a['source_term']==place['surface']+'人也'
  if rule=='past_migration':
   s=rs['subject'];return a['relation']=='migration_destination'and scope['surface']==s['surface']+'前徙'+place['surface']and s['start']==scope['start']and place['start']==s['end']+2 and a['source_term']=='徙'+place['surface']
  if rule=='same_subject_seclusion':
   s=rs['subject'];other=rs['pursuer'];pronoun=rs['subject_pronoun'];head=ch['paragraphs'][0]['mentions'][0];pattern=s['surface']+'以老病求歸懼不免禍乃詭道從轘轅出'+other['surface']+'果使人追'+pronoun['surface']+'到懐不及遂隱於'+place['surface']+'不交人事'
   return a['relation']=='residence'and head['person_id']==s['person_id']==pronoun['person_id']!=other['person_id']and scope['surface']==pattern and s['start']==scope['start']and other['start']==s['end']+len('以老病求歸懼不免禍乃詭道從轘轅出')and pronoun['start']==other['end']+len('果使人追')and place['start']==pronoun['end']+len('到懐不及遂隱於')and scope['end']==place['end']+len('不交人事')and a['source_term']=='隱於'+place['surface']
  if rule=='two_people_shared_locality':
   one,two=rs['one'],rs['two'];return a['relation']=='source_locality_designation'and b['subject_role']in ('one','two')and one['start']==scope['start']==0 and two['start']==one['end']+4 and place['start']==two['end']+4 and scope['surface']==one['surface']+'多力者也'+two['surface']+'勇者也並'+place['surface']+'人'and a['source_term']=='並'+place['surface']+'人'
  return False
 except(KeyError,TypeError,ValueError,StopIteration,AssertionError):return False
def explicit_death_report_valid(event,ch):
 try:
  b=event['source_layered_death_report'];e,=event['evidence'];p=next(p for p in ch['paragraphs']if p['id']==e['paragraph_id']);t=p['text'];ms={m['id']:m for m in p['mentions']};rs={k:ms[v]for k,v in b['roles'].items()};subject=rs['subject'];a=b['clause_anchor']
  assert b['kind']=='layered_explicit_death_report'and b['source_revision']==ch['source']['revision_id']and b['paragraph_sha256']==hashlib.sha256(t.encode()).hexdigest()and exact(p,a)and subject['start']==a['start']and subject['person_id']==event['person_id']and e['person_mention_id']==subject['id']and e['quote']==t and e['chapter_id']==ch['id']and e['source_id']==ch['source_id']and event['event_type']=='death'and event['date_expression']is None and 'normalized_date'not in event and 'normalized_date_range'not in event
  if b['rule']=='named_subject_collapse':return set(rs)=={'subject'}and a['surface']==subject['surface']+'崩'and event['source_term']=='崩'
  if b['rule']=='accused_subject_dies_of_grief':
   one,two=rs['accuser1'],rs['accuser2'];return set(rs)=={'subject','accuser1','accuser2'}and a['surface']==subject['surface']+'以'+one['surface']+two['surface']+'所構憂死'and one['start']==subject['end']+1 and two['start']==one['end']and event['source_term']=='憂死'
  return False
 except(KeyError,TypeError,ValueError,StopIteration,AssertionError):return False
