"""A validated same-topic death binds a literal, partitioned posthumous gift.
No nearest-person selection, title punctuation insertion, or inferred issuer/date.
"""
import hashlib,re

def valid(h, paragraphs, mentions, events):
 try:
  b=h['posthumous_basis'];keys={'kind','source_term','death_event_id','death_anchor','grant_anchor','title_parts','topic_person_mention_id','intervening_context','death_subject_context','issuer','source_revision','paragraph_sha256','evidence'}
  start=h['effective_period']['start']
  if(set(b)!=keys or b['kind']!='bound_death_serial_gift' or h['mode']!='posthumous_grant' or h['kind']!='office' or h['status']!='source_attested' or len(b['evidence'])!=1 or b['evidence']!=h['evidence']or b['evidence']!=start['evidence']or start['status']!='source_event'or start['event_type']!='posthumous_grant'or start['date_expression']is not None or 'normalized_date'in start or 'normalized_date_range'in start):return False
  e=b['evidence'][0];cid,p=paragraphs[e['paragraph_id']];text=p['text'];topic=mentions[b['topic_person_mention_id']];event=events[b['death_event_id']]
  if(p.get('text_layer')!='received_chapter'or e['chapter_id']!=cid or e['quote']!=text or b['source_term']!=text or b['source_revision']!=p['source_position']['revision_id']or b['paragraph_sha256']!=hashlib.sha256(text.encode()).hexdigest()or topic[:2]!=(cid,p['id'])or topic[2].get('kind')!='person'or topic[2]['person_id']!=h['person_id']or e['person_mention_id']!=topic[2]['id']or event['event_type']!='death'or event['status']!='source_attested'or event['person_id']!=h['person_id']or not any(x['paragraph_id']==p['id']and x['quote']==text and x['chapter_id']==cid and x.get('source_id')==e.get('source_id')for x in event['evidence'])):return False
  people=[m for m in p['mentions']if m.get('kind')=='person'];first=min(people,key=lambda m:m['start']);prefix=text[:topic[2]['start']]
  if(first['person_id']!=h['person_id']or any(m['person_id']!=h['person_id']for m in people if m['start']<topic[2]['start'])or topic[2]['surface']in ('其','之','父','母','子','兄弟','長子','次子')or not(prefix in ('','長子','次子')or event.get('date_expression')and prefix in [event['date_expression']+s for s in ('','春','夏','秋','冬')])):return False
  def exact(a):return isinstance(a,dict)and set(a)=={'paragraph_id','start','end','surface'}and a['paragraph_id']==p['id']and type(a['start'])is int and type(a['end'])is int and 0<=a['start']<a['end']<=len(text)and text[a['start']:a['end']]==a['surface']
  d,g=b['death_anchor'],b['grant_anchor']
  if(not exact(d)or not exact(g)or d['surface']!=event['source_term']or not re.search(r'卒|薨|死|見害',d['surface'])or topic[2]['end']>d['start']or d['end']>g['start']or not g['surface'].startswith('贈')):return False
  if not death_subject_valid(b['death_subject_context'],p,topic[2],event,d,mentions):return False
  parts=b['title_parts'];position=g['start']+1
  if not isinstance(parts,list)or not parts:return False
  for a in parts:
   if(not exact(a)or a['start']!=position or not re.fullmatch(r'(?:司空|中書監|[^，。、；：贈封諡授拜除]{1,16}(?:將軍|刺史))',a['surface'])):return False
   position=a['end']
  if position!=g['end']or sum(a['surface']==h['title']for a in parts)!=1:return False
  part=next(a for a in parts if a['surface']==h['title'])
  if not any(a.get('paragraph_id')==p['id']and a.get('person_mention_id')==topic[2]['id']and a.get('usage')=='posthumous_usage'and all(a.get(k)==part[k]for k in ('start','end','surface'))for a in h['attestations']):return False
  ctx=b['intervening_context'];between=text[d['end']:g['start']];issuer=b['issuer']
  if set(issuer)!={'person_id','source_anchor'}or issuer['person_id']is not None:return False
  if ctx=={'kind':'immediate'}:
   if between!=''or issuer['source_anchor']is not None:return False
  elif ctx.get('kind')=='editorial_lament':
   if set(ctx)!={'kind','anchor'}or not exact(ctx['anchor'])or ctx['anchor']['start']!=d['end']or ctx['anchor']['end']!=g['start']or not re.fullmatch(r'議者(?:惜|傷|痛|哀|譏|嘆)[^曰贈卒薨死害]{1,50}',between)or any(m['start']>=d['end']and m['start']<g['start']for m in people)or issuer['source_anchor']is not None:return False
  elif ctx.get('kind')=='imperial_mourning_notice':
   if set(ctx)!={'kind','anchor'}or not exact(ctx['anchor'])or ctx['anchor']['start']!=d['end']or ctx['anchor']['end']!=g['start']or between not in ('下詔痛惜','下詔哀悼','詔痛惜','詔哀惜')or any(m['start']>=d['end']and m['start']<g['start']for m in people)or issuer['source_anchor']!=ctx['anchor']:return False
  elif ctx.get('kind')=='last_words_funeral_petition':
   keys={'kind','last_words_anchor','policy_anchor','petition_anchor','addressee_mention_id','petition_agent_mention_id','speaker_mention_id'}
   if set(ctx)!=keys:return False
   w,q,petition=[ctx[k]for k in ('last_words_anchor','policy_anchor','petition_anchor')];add=mentions[ctx['addressee_mention_id']];agent=mentions[ctx['petition_agent_mention_id']];speaker=mentions[ctx['speaker_mention_id']]
   if(not all(exact(a)for a in (w,q,petition))or w['start']!=d['end']or w['end']!=q['start']or q['end']!=petition['start']or petition['end']!=g['start']or any(m[:2]!=(cid,p['id'])for m in (add,agent,speaker))or add[2]['person_id']!=agent[2]['person_id']or add[2]['person_id']==h['person_id']or speaker[2]['person_id']!=h['person_id']or speaker[2]['surface']!='吾'):return False
   prefix='臨没謂功曹'+add[2]['surface']+'曰'
   if(not w['surface'].startswith(prefix+'吾')or add[2]['end']!=w['start']+len(prefix)-1 or speaker[2]['start']!=w['start']+len(prefix)or '身殁後乞𦵏'not in w['surface']or re.search(r'贈|[卒薨]',w['surface'])or not re.fullmatch(r'時制[^曰贈卒薨死]{1,20}皆葬[^曰贈卒薨死]{1,10}',q['surface'])or petition['surface']!=agent[2]['surface']+'等申遺意詔許之'or agent[2]['start']!=petition['start']or issuer['source_anchor']!={'paragraph_id':p['id'],'start':petition['end']-3,'end':petition['end'],'surface':'詔許之'}):return False
   allowed={add[2]['id'],agent[2]['id']}
   if any(m['person_id']!=h['person_id']and m['id']not in allowed and d['end']<=m['start']<g['start']for m in people):return False
  else:return False
  return True
 except (KeyError,TypeError,ValueError,IndexError):return False


def death_subject_valid(ctx,p,topic,event,death,mentions):
 """Explicit clause roles override neither the biography topic nor the death recipient."""
 try:
  text=p['text'];pid=event['person_id'];people=[m for m in p['mentions']if m.get('kind')=='person']
  def exact(a):return set(a)=={'paragraph_id','start','end','surface'}and a['paragraph_id']==p['id']and type(a['start'])is int and type(a['end'])is int and 0<=a['start']<a['end']<=len(text)and text[a['start']:a['end']]==a['surface']
  def mention(mid):
   m=mentions[mid]
   if m[1]!=p['id']or m[2].get('kind')!='person':raise ValueError('foreign mention')
   return m[2]
  if ctx.get('kind')=='explicit_restatement':
   if set(ctx)!={'kind','person_mention_id'}:return False
   m=mention(ctx['person_mention_id'])
   return(m['person_id']==pid and topic['start']<=m['start']<m['end']<=death['start']and not any(x['person_id']!=pid and m['end']<=x['start']<death['start']for x in people)and not re.search('(?<!號)曰|云|言|贈|卒|薨|死',text[m['end']:death['start']]))
  if ctx.get('kind')=='parent_appointment_causal_return':
   if set(ctx)!={'kind','anchor','parent_mention_id','child_mention_id'}:return False
   a=ctx['anchor'];parent=mention(ctx['parent_mention_id']);child=mention(ctx['child_mention_id'])
   return(exact(a)and a['end']==death['start']and parent['person_id']==pid and child['person_id']!=pid and re.fullmatch(re.escape('時'+parent['surface']+'子'+child['surface']+'為')+r'[^曰贈卒薨死害]{1,12}故有此授',a['surface'])and parent['start']==a['start']+1 and child['start']==parent['end']+1 and all(x['id']in [parent['id'],child['id']]or x['person_id']==child['person_id']and x['surface']=='子'and x['start']==parent['end']and x['end']==child['start']for x in people if a['start']<=x['start']<a['end'])and death['surface'].startswith('卒年'))
  if ctx.get('kind')=='sibling_victim_continuation':
   keys={'kind','resumption_anchor','attacker_anchor','mourning_anchor','kinship_anchor','subject_mention_id','attacker_mention_id','father_mention_id','relative_mention_id'}
   if set(ctx)!=keys:return False
   r,a,m,k=[ctx[x]for x in ['resumption_anchor','attacker_anchor','mourning_anchor','kinship_anchor']];subject=mention(ctx['subject_mention_id']);attacker=mention(ctx['attacker_mention_id']);father=mention(ctx['father_mention_id']);relative=mention(ctx['relative_mention_id'])
   if(not all(exact(x)for x in (r,a,m,k))or not r['end']==a['start']<a['end']==m['start']<m['end']==k['start']<k['end']==death['start']or subject['person_id']!=pid or subject['start']!=r['start']or r['surface']!=subject['surface']+'兄弟並交遊時俊乃為當時所美'or a['surface']!='及'+attacker['surface']+'入洛'or attacker['person_id']==pid or attacker['start']!=a['start']+1 or m['surface']!='兄弟在'+father['surface']+'䘮中'or father['surface']!='父'or father['person_id']==pid or k['surface']!='以於'+relative['surface']+'有從姨兄弟之親'or relative['person_id']==pid or not death['surface'].startswith('相率奉迎俱見害')):return False
   return all(x['id']in [subject['id'],attacker['id'],father['id'],relative['id']]for x in people if r['start']<=x['start']<death['start'])
  if ctx.get('kind')=='illness_envoy_visit_continuation':
   if set(ctx)!={'kind','illness_anchor','visit_anchor','sovereign_mention_id','envoy_mention_id'}:return False
   ill,visit=ctx['illness_anchor'],ctx['visit_anchor'];sovereign=mention(ctx['sovereign_mention_id']);envoy=mention(ctx['envoy_mention_id'])
   return(exact(ill)and exact(visit)and ill['start']==topic['start']and ill['surface']==topic['surface']+'病篤'and ill['end']==visit['start']and visit['end']==death['start']and sovereign['person_id']!=pid and envoy['person_id']not in [pid,sovereign['person_id']]and visit['surface']==sovereign['surface']+'遣'+envoy['surface']+'就受遺言更遣侍臣問疾一夜數返'and sovereign['start']==visit['start']and envoy['start']==sovereign['end']+1 and death['surface']=='及卒'and all(x['id']in [sovereign['id'],envoy['id']]for x in people if visit['start']<=x['start']<visit['end']))
  return False
 except(KeyError,TypeError,ValueError):return False
