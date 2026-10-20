# coding: utf-8
"""Fixed-unit conferment, memorial and source-line succession, without guessed tenures."""
def exact(anchor,p):
 return(isinstance(anchor,dict)and set(anchor)=={'paragraph_id','start','end','surface'}and anchor['paragraph_id']==p['id']and type(anchor['start'])is int and type(anchor['end'])is int and 0<=anchor['start']<anchor['end']<=len(p['text'])and p['text'][anchor['start']:anchor['end']]==anchor['surface'])
def parts(h,paragraphs,bkey):
 b=h[bkey];e,=b['evidence'];cid,p=paragraphs[e['paragraph_id']];ms={m['id']:m for m in p['mentions']}
 if e['chapter_id']!=cid or e['quote']!=p['text']or e not in h['evidence']or b['evidence']!=h['effective_period']['start']['evidence']or h['status']!='source_attested'or h['human_reviewed']is not False:raise ValueError('source')
 return b,e,p,ms

def heading_posthumous_valid(h,paragraphs,events):
 try:
  key='naming_basis'if h['mode']=='posthumous_naming'else'posthumous_basis';b,e,p,ms=parts(h,paragraphs,key);a=b['title_anchor'];notice=b['notice_anchor'];topic=ms[b['topic_person_mention_id']];death=events[b['death_event_id']]
  return(set(b)=={'kind','source_term','death_event_id','topic_person_mention_id','title_anchor','notice_anchor','evidence'}and b['kind']=='heading_title_confirmed_by_posthumous_notice'
   and h['kind']=='honorific'and h['title']in('孝穆','皇后')and h['mode']==('posthumous_naming'if h['title']=='孝穆'else'posthumous_grant')
   and p['text'].startswith('孝穆趙皇后諱安')and topic['start']==0 and topic['surface']=='孝穆趙皇后'and topic['person_id']==h['person_id']
   and exact(a,p)and a['surface']==h['title']and a['start']==(0 if h['title']=='孝穆'else 3)
   and exact(notice,p)and notice['surface']==b['source_term']=='宋初追崇號謚'
   and death['person_id']==h['person_id']and death['event_type']=='death'and any(x['paragraph_id']==p['id']for x in death['evidence'])
   and p['text'].index('其日后以産疾殂')<notice['start']and h['effective_period']['start']=={'status':'source_event','event_type':h['mode'],'date_expression':'宋初','evidence':b['evidence']}
   and any(x['start']==a['start']and x['end']==a['end']and x['surface']==h['title']and x['usage']=='posthumous_usage'for x in h['attestations']))
 except(KeyError,TypeError,ValueError,StopIteration):return False

def recalled_gift_valid(h,paragraphs):
 try:
  b,e,p,ms=parts(h,paragraphs,'posthumous_basis');a=b['clause_anchor'];term='卓初與趙裔俱贈金紫光祿大夫'
  if(set(b)!={'kind','source_term','clause_anchor','recipient_person_ids','former_office_evidence','evidence'}or b['kind']!='coordinated_recollected_posthumous_gift'
   or h['mode']!='posthumous_grant'or h['kind']!='office'or h['title']!='金紫光祿大夫'or not exact(a,p)or a['surface']!=b['source_term']or b['source_term']!=term):return False
  z=next(m for m in p['mentions']if m['start']==a['start']and m['surface']=='卓');y=next(m for m in p['mentions']if m['start']==a['start']+3 and m['surface']=='趙裔')
  if set(b['recipient_person_ids'])!={z['person_id'],y['person_id']}or h['person_id']not in b['recipient_person_ids']:return False
  if h['effective_period']['start']!={'status':'source_event','event_type':'posthumous_grant','date_expression':None,'evidence':b['evidence']}:return False
  if len(b['former_office_evidence'])!=2:return False
  seen=set()
  for old in b['former_office_evidence']:
   _,op=paragraphs[old['paragraph_id']]
   if old['quote']!=op['text']or '可追贈光祿大夫加金章紫綬'not in op['text']:return False
   for word,pid in [('故洮陽令蕭卓',z['person_id']),('故平原太守趙裔',y['person_id'])]:
    if word in op['text']and any(m.get('person_id')==pid and m['surface']in('蕭卓','趙裔')and op['text'].index(word)<=m['start']<op['text'].index(word)+len(word)for m in op['mentions']):seen.add(pid)
  return seen==set(b['recipient_person_ids'])and any(x['start']==a['start']+7 and x['surface']==h['title']for x in h['attestations'])
 except(KeyError,TypeError,ValueError,StopIteration):return False

def enfeoffment_valid(h,paragraphs):
 try:
  b,e,p,ms=parts(h,paragraphs,'enfeoffment_basis');a=b['clause_anchor'];m=ms[b['recipient_person_mention_id']]
  if (b['kind']!='explicit_named_or_continued_posthumous_enfeoffment'or h['mode']!='posthumous_enfeoffment'or h['kind']!='noble_rank'
   or not exact(a,p)or a['surface']!=b['source_term']or b['recipient_person_id']!=h['person_id']or m['person_id']!=h['person_id']):return False
  if h['title']=='臨賀縣侯':
   return(a['surface']=='於是追封裔臨賀縣侯'and m['surface']=='裔'and m['start']==a['start']+4 and h['effective_period']['start']['date_expression']=='其年'
    and h['effective_period']['start']['normalized_date']['year']==421 and p['text'].index('永初二年')<p['text'].index('其年又詔曰')<a['start'])
  if h['title']=='封陽縣侯':
   prior=b['antecedent_clause_anchor'];return(exact(prior,p)and prior['surface']=='卓初與趙裔俱贈金紫光祿大夫'and prior['end']==a['start']
    and m['surface']=='卓'and m['start']==prior['start']and a['surface']=='又追封封陽縣侯'and h['effective_period']['start']=={'status':'source_event','event_type':'posthumous_enfeoffment','date_expression':None,'evidence':b['evidence']})
  return False
 except(KeyError,TypeError,ValueError,StopIteration):return False

def conferment_valid(h,paragraphs):
 try:
  b,e,p,ms=parts(h,paragraphs,'source_grant_basis');a=b['clause_anchor'];m=ms[b['recipient_person_mention_id']]
  expected={'豫章公太夫人':('義熙七年拜豫章公太夫人','義熙七年'),'太妃':('又加太妃之號',None),'太皇太后':('少帝即位加崇曰太皇太后','少帝即位'),'吳郡夀昌縣君':('妻下邳趙氏封吳郡夀昌縣君',None)}
  term,date=expected[h['title']]
  if set(b)!={'kind','source_term','clause_anchor','recipient_person_mention_id','evidence'}or b['kind']!='explicit_biographical_conferment'or h['mode']!='grant'or h['kind']!='honorific'or not exact(a,p)or a['surface']!=b['source_term']or a['surface']!=term or m['person_id']!=h['person_id']or h['effective_period']['start']['date_expression']!=date:return False
  if h['title']=='吳郡夀昌縣君':
   return m['surface']=='趙氏'and a['start']<m['start']<m['end']<a['end']and not h['effective_period']['start'].get('normalized_date')
  return(m['surface']==h['title']and a['start']<=m['start']<m['end']<=a['end']and (h['effective_period']['start'].get('normalized_date',{}).get('year')==411 if h['title']=='豫章公太夫人'else'normalized_date'not in h['effective_period']['start']))
 except(KeyError,TypeError,ValueError,StopIteration):return False

def line_succession_valid(h,holdings,paragraphs,relations):
 try:
  i=h['inheritance'];b=i['source_chain_binding'];e,=i['evidence'];_,p=paragraphs[e['paragraph_id']];prior=holdings[i['predecessor_holding_id']];a=b['clause_anchor'];rr={r['id']:r for r in relations};father=rr[b['father_assertion_id']];ritual=rr[b['ritual_successor_assertion_id']]
  return(set(i)=={'predecessor_person_id','predecessor_holding_id','resolved_title','source_term','status','evidence','rationale','human_reviewed','predecessor_relation','ritual_predecessor_person_id','intervening_holding_status','source_chain_binding'}
   and set(b)=={'kind','father_assertion_id','ritual_successor_assertion_id','clause_anchor','source_revision'}and i['evidence']==h['evidence']
   and i['predecessor_relation']=='named_source_line_succession'and i['intervening_holding_status']=='not_asserted'and i['human_reviewed']is False and i['status']=='contextual_provisional'
   and prior['mode']=='posthumous_enfeoffment'and prior['title']==i['resolved_title']=='臨賀縣侯'and prior['person_id']==i['predecessor_person_id']
   and h['mode']=='accession'and h['kind']==prior['kind']=='noble_rank'and h['title']=='紹封'
   and b['kind']=='posthumous_founder_named_ritual_line_successor'and b['source_revision']==p['source_position']['source_revision']
   and exact(a,p)and a['surface']==i['source_term']=='以弟孫襲之繼宣之紹封'and p['text'][a['start']-4:a['start']]=='蚤卒無子'
   and father['predicate']=='father'and father['subject_person_id']==i['ritual_predecessor_person_id']and father['object_person_id']==prior['person_id']
   and father['qualifiers']['source_term']=='裔長子宣之'and ritual['predicate']=='ritual_successor_of'and ritual['subject_person_id']==h['person_id']and ritual['object_person_id']==i['ritual_predecessor_person_id']
   and ritual['qualifiers']['legal_adoption_status']=='not_stated'and e['quote']==p['text']and h['effective_period']['start']=={'status':'source_event','event_type':'accession','date_expression':None,'evidence':h['evidence']}
   and h['effective_period']['end']=={'status':'unknown','date_expression':None,'evidence':[]})
 except(KeyError,TypeError,ValueError,StopIteration):return False

def memorial_errors(q,chapter,people,holdings):
 try:
  if q['person_id']not in people or q['proposal_kind']!='memorial_request'or q['human_reviewed']is not False or q['status']!='contextual_provisional':raise ValueError('proposal identity')
  e,=q['evidence'];p=next(p for p in chapter['paragraphs']if p['id']==e['paragraph_id']);a=q['source_anchor'];role=q['role_anchor'];ms={m['id']:m for m in p['mentions']};person=ms[q['person_mention_id']]
  if e['quote']!=p['text']or e['chapter_id']!=chapter['id']or not exact(a,p)or not exact(role,p)or a['surface']!=q['source_term']or role['surface']!=q['title']or person['person_id']!=q['person_id']or not a['start']<=role['start']<role['end']<=a['end']:raise ValueError('proposal source')
  if not a['surface'].startswith(('可','並宜'))or'有司奏曰'not in p['text'][:a['start']]:raise ValueError('not memorial conditional')
  targets=[holdings[x]for x in q['confirmation_holding_ids']]
  if q['outcome']=='not_reported':
   if targets or q['confirmation_scope']is not None or q['title']!='豫章郡建昌縣君':raise ValueError('unreported outcome')
  else:
   if len(targets)!=1 or targets[0]['person_id']!=q['person_id']or targets[0]['mode']not in('grant','posthumous_grant','posthumous_enfeoffment'):raise ValueError('confirmation actor/event')
   target=targets[0];scope=q['confirmation_scope']
   order={p['id']:i for i,p in enumerate(chapter['paragraphs'])};later=False
   for te in target['evidence']:
    if te.get('chapter_id')!=chapter['id']or te.get('paragraph_id')not in order:continue
    if order[te['paragraph_id']]>order[p['id']]:later=True
    elif order[te['paragraph_id']]==order[p['id']]and any(aa['paragraph_id']==p['id']and aa['start']>=a['end']for aa in target['attestations']):later=True
   if not later:raise ValueError('confirmation must be this unit later source clause')
   if scope=='rank_only':
    if q['outcome']!='partially_confirmed'or q['title']!='開國縣侯'or not target['title'].endswith('縣侯')or q['requested_households']!={'value':500,'source_number':'五百','source_term':'食邑五百戸','enactment_status':'not_confirmed'}:raise ValueError('quantity unconfirmed')
   elif scope=='rank_style_and_insignia':
    if q['outcome']!='confirmed_by_later_clause'or q['source_term']!='可追贈光祿大夫加金章紫綬'or target['title']!='金紫光祿大夫':raise ValueError('gift style')
   elif scope=='exact_title':
    if q['outcome']!='confirmed_by_later_clause'or target['title']!=q['title']:raise ValueError('exact title')
   else:raise ValueError('unknown confirmation')
  return[]
 except(KeyError,TypeError,ValueError,StopIteration)as ex:return['奏請與後文實授回證未分層：'+str(ex)]

def source_use_errors(use,chapter,people,holdings):
 try:
  e,=use['evidence'];p=next(p for p in chapter['paragraphs']if p['id']==e['paragraph_id']);m=next(m for m in p['mentions']if m['id']==use['person_mention_id'])
  if use['person_id']not in people or m['person_id']!=use['person_id']or m['kind']!='person'or not exact(use['source_anchor'],p)or use['source_anchor']['surface']!=use['source_term']or e['quote']!=p['text']:raise ValueError('source use')
  if use['usage_kind']not in('contextual_pronoun','title_reference','generic_enfeoffed_woman_status'):raise ValueError('use category')
  terms={'contextual_pronoun':('后','上'),'title_reference':('高祖','太妃','宋王太后','太后','太皇太后'),'generic_enfeoffed_woman_status':('命婦孫','命婦趙')}
  if use['source_term']not in terms[use['usage_kind']]:raise ValueError('term is not this use kind')
  if not use['source_anchor']['start']<=m['start']<m['end']<=use['source_anchor']['end']:raise ValueError('referent outside source use')
  for key in use['holding_ids']:
   h=holdings[key]
   if h['person_id']!=use['person_id']or h['title']!=use['source_term']or not any(a['paragraph_id']==p['id']and a['start']==use['source_anchor']['start']and a['end']==use['source_anchor']['end']and a['person_mention_id']==m['id']for a in h['attestations']):raise ValueError('wrong holding actor/occurrence')
  if use['usage_kind']!='title_reference'and use['holding_ids']:raise ValueError('pronoun/status not holding')
  return[]
 except(KeyError,TypeError,ValueError,StopIteration)as ex:return['來源稱指與人物／持職不符：'+str(ex)]
