# coding: utf-8
"""A retained biography topic, explicit era and ordinal chain bind an elided death subject."""
import hashlib,re

def valid(date,event,chapters,parse_number,root=None):
 try:
  try:
   from scripts.relative_regnal_year import relative_regnal_year_valid
  except ImportError:
   from relative_regnal_year import relative_regnal_year_valid
  b=date['event_evidence_binding'];c=chapters[b['chapter_id']];ps=c['paragraphs'];by={p['id']:p for p in ps};order=[p['id']for p in ps]
  if len(by)!=len(ps)or b['kind']!='biographical_subject_ordinal_chain_death'or b['person_id']!=event['person_id']or b['life_event_id']!=event['id']or event['event_type']!='death'or event['status']!='source_attested':return False
  if not relative_regnal_year_valid(date,parse_number,chapters)or 'narrative_era_scope'in date:return False
  if 'source_date_parts'in event or any(k in date for k in ['month','day','calendar_month','lunar_month'])or date.get('precision')!='year'or date.get('calendar')!='chinese_civil':return False
  if c['text_sha256']!=hashlib.sha256('\n\n'.join(p['text']for p in ps).encode()).hexdigest():return False
  source=c['source'];fp={'source_id':c['source_id'],'revision_id':source['revision_id'],'raw_sha256':source['raw_file_sha256'],'text_sha256':c['text_sha256']}
  if b['source_fingerprint']!=fp:return False
  def anchor(a):
   p=by[a['paragraph_id']];return(set(a)=={'paragraph_id','start','end','surface'}and type(a['start'])is int and type(a['end'])is int and 0<=a['start']<a['end']<=len(p['text'])and p['text'][a['start']:a['end']]==a['surface'])
  topic=b['biography_subject_reference'];tp=by[topic['paragraph_id']];tm=next(m for m in tp['mentions']if m['id']==topic['person_mention_id'])
  local=b['local_subject_reference'];lp=by[local['paragraph_id']];lm=next(m for m in lp['mentions']if m['id']==local['person_mention_id'])
  if tm['start']!=0 or tm['person_id']!=event['person_id']or lm['person_id']!=event['person_id']or tm['kind']!='person'or lm['kind']!='person':return False
  chain=b['year_chain'];anchors=[x['anchor']for x in chain];da=b['death_anchor']
  if len(chain)<2 or not all(anchor(a)for a in anchors+[da]):return False
  start=order.index(anchors[0]['paragraph_id']);end=order.index(da['paragraph_id']);ids=order[start:end+1]
  if start>end or order.index(tp['id'])>start or local['paragraph_id']!=da['paragraph_id']or b['paragraph_ids']!=ids:return False
  if b['full_paragraphs']!=[{'paragraph_id':pid,'quote':by[pid]['text'],'source_position':by[pid]['source_position']}for pid in ids]:return False
  if 'received_text_projection' in b:
   try:
    from scripts.biographical_work_references import projection_valid, references_valid
   except ImportError:
    from biographical_work_references import projection_valid, references_valid
   if not projection_valid(c,ps,b,root):return False
  else:
   if 'non_subject_references' in b:return False
   for pid in ids:
    p=by[pid];pos=p['source_position']
    if pos['revision_id']!=source['revision_id']or len(pos['raw_character_positions'])!=len(p['text']):return False
  if [(a['paragraph_id'],a['start'])for a in anchors]!=sorted([(a['paragraph_id'],a['start'])for a in anchors],key=lambda x:(order.index(x[0]),x[1])):return False
  era=date['regnal_year_mapping']['era_name'];previous=None
  for i,x in enumerate(chain):
   a=x['anchor'];term=a['surface'];kind=x['kind'];n=x['regnal_year']
   if i==0:
    if kind!='explicit_era_year'or not term.startswith(era)or not term.endswith('年')or parse_number(term[len(era):-1])!=n:return False
   elif kind=='relative_next_year':
    if term!='明年'or n!=previous+1:return False
   elif kind=='omitted_era_ordinal':
    if not term.endswith('年')or parse_number(term[:-1])!=n or n<=previous:return False
   else:return False
   previous=n
  last=chain[-1];last_a=last['anchor']
  if last['kind']!='omitted_era_ordinal'or date['source_expression']!=last_a['surface']or event['date_expression']!=last_a['surface']or date['regnal_year_mapping']['regnal_year']!=last['regnal_year']or date['regnal_year_mapping']['year_offset']!=0:return False
  if da['surface']not in ['卒','薨','死']or event['source_term']!=da['surface']or da['paragraph_id']!=lp['id']or last_a['paragraph_id']!=lp['id']or not lm['end']<=last_a['start']<last_a['end']<=da['start']:return False
  # No named subject change may occur after the retained local topic and before death.
  if 'received_text_projection' in b:
   if not references_valid(b,lp,lm,da):return False
  elif any(m.get('kind')=='person'and lm['end']<=m['start']<da['end']and m.get('person_id')!=event['person_id']for m in lp['mentions']):return False
  e,=event['evidence']
  if e!={**{k:c[k]for k in ['work_id','book_id','source_id']},'chapter_id':c['id'],'paragraph_id':lp['id'],'quote':lp['text'],'person_mention_id':lm['id']}:return False
  if date['original_quote']!=lp['text']or [e['paragraph_id']for e in date['evidence']]!=ids:return False
  for e in date['evidence']:
   if e['quote']!=by[e['paragraph_id']]['text']or e['chapter_id']!=c['id']or any(e[k]!=c[k]for k in ['work_id','book_id','source_id']):return False
  # Explicitly enumerate every numeral-year or 明年 marker in the retained scope up to death.
  actual=[]
  for pid in ids:
   p=by[pid];lo=anchors[0]['start']if pid==ids[0]else 0;hi=da['end']if pid==ids[-1]else len(p['text'])
   actual.extend((pid,m.start()+lo,m.end()+lo,m.group())for m in re.finditer(r'(?:元|[一二三四五六七八九十百]+)年|明年',p['text'][lo:hi]))
  wanted=[]
  for i,a in enumerate(anchors):wanted.append((a['paragraph_id'],a['start']+(len(era)if i==0 else 0),a['end'],a['surface'][len(era):]if i==0 else a['surface']))
  if actual!=wanted:return False
  # Named reign changes must be cited explicitly, never hidden as a same-era chain.
  known=b['known_era_names']
  if not isinstance(known,list)or era not in known or len(set(known))!=len(known):return False
  for pid in ids:
   p=by[pid];lo=anchors[0]['start']if pid==ids[0]else 0;hi=da['end']if pid==ids[-1]else len(p['text'])
   for name in known:
    if name!=era and re.search(re.escape(name)+r'(?:元|[一二三四五六七八九十百]+)年',p['text'][lo:hi]):return False
  return True
 except(KeyError,ValueError,TypeError,IndexError,StopIteration,AttributeError):return False
