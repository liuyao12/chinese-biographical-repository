# coding: utf-8
"""Fixed complete annal units qualify an explicitly bound execution year.

No name/year allowlist. Both source episodes, their grammatical roles and the
independent era table are validated from actual local bytes, never prose NLU.
"""
from pathlib import Path,PurePosixPath
from urllib.parse import urlsplit,parse_qs
import hashlib,re
H=lambda b:hashlib.sha256(b).hexdigest()
def numeral(s):
 z='一二三四五六七八九'
 if s=='元':return 1
 if s in z:return z.index(s)+1
 if re.fullmatch('[一二三四五六七八九]?十[一二三四五六七八九]?',s):
  f,l=s.split('十');return (z.index(f)+1 if f else 1)*10+(z.index(l)+1 if l else 0)
 return None
def anchor(t,a):
 return isinstance(a,dict)and set(a)=={'start','end','quote'}and type(a['start'])is int and type(a['end'])is int and 0<=a['start']<a['end']<=len(t)and t[a['start']:a['end']]==a['quote']
def file(root,path):
 p=PurePosixPath(path)if isinstance(path,str)else None
 if not p or p.is_absolute()or '..'in p.parts or p.parts[0]!='sources':raise ValueError('source path')
 f=Path(root)/path
 if f.is_symlink()or f.resolve()!=Path(root).resolve()/path:raise ValueError('source symlink escape')
 return f.read_bytes()
def archive(root,a):
 rawbytes=file(root,a['raw_file']);raw=rawbytes.decode('utf-8');query=parse_qs(urlsplit(a['url']).query)
 if H(rawbytes)!=a['sha256']or type(a['revision_id'])is not int or a['revision_id']<=0 or query.get('oldid')!=[str(a['revision_id'])]or query.get('title')!=[a['title']]:raise ValueError('fixed revision/raw')
 for u in a['complete_units']:
  lo=raw.index(u['start_boundary']);hi=raw.index(u['end_boundary'],lo+len(u['start_boundary']))
  if lo and raw[lo-1]!='\n':raise ValueError('unit must start at full source line')
  if u['start_boundary'].startswith('=='):
   if u['start_boundary']!='=='+u['year_label']+'==':raise ValueError('year heading')
   following=re.search(r'^==[^=\n]+==$',raw[lo+len(u['start_boundary']):],re.M)
   if following is None or hi!=lo+len(u['start_boundary'])+following.start():raise ValueError('next complete annal year boundary')
  else:
   line=raw[lo:raw.index('\n',lo)]
   if not re.fullmatch(r' ?[^\n，。]{1,30}'+re.escape(u['year_label'])+r'（[^\n）]+）',line):raise ValueError('complete year caption')
   rest=raw[raw.index('\n',lo)+1:];offset=raw.index('\n',lo)+1
   following=re.search(r'^(?: ?[^\n，。]{1,30}(?:元|[一二三四五六七八九十]+)年（[^\n）]+）|\[\[category:[^\n]+)',rest,re.M)
   if following is None or hi!=offset+following.start():raise ValueError('next caption or terminal category boundary')
  if (lo,hi)!=(u['raw_start'],u['raw_end'])or raw[lo:hi]!=u['raw']or H(u['raw'].encode())!=u['sha256']:raise ValueError('complete sequential raw unit')
 return raw
def received_paragraph(c,p,root):
 source=c['source'];rawbytes=file(root,source['raw_file']);raw=rawbytes.decode('utf-8');pos=p['source_position'];line=pos['first_line']
 return(p.get('text_layer')=='received_chapter'and not any(k in p for k in ['annotator','attached_note_to_paragraph_id'])and H(rawbytes)==source.get('wikitext_sha256')and pos.get('revision_id')==source.get('revision_id')and type(line)is int and line>0 and pos.get('last_line')==line and raw.splitlines()[line-1].strip()==p['text'])
def valid(date,event,chapters,root):
 try:
  if root is None:return False
  b=date['archived_death_year'];m=date['regnal_year_mapping'];o=b['origin'];c=chapters[o['chapter_id']];p=next(p for p in c['paragraphs']if p['id']==o['paragraph_id']);t=p['text'];ms={x['id']:x for x in p['mentions']};subject=ms[o['person_mention_id']];actor=ms[o['actor_person_mention_id']]
  if b['kind']!='archived_parallel_execution_year'or m['kind']!='archived_parallel_death_ce_span'or event.get('event_type')!='death'or event.get('status')!='source_attested'or b['life_event_id']!=event.get('id')or b['person_id']!=event.get('person_id')or subject.get('person_id')!=event.get('person_id')or actor.get('person_id')==event.get('person_id'):return False
  if event['evidence'][0].get('person_mention_id')!=subject['id']or event.get('normalized_date')!=date or date.get('evidence')!=event.get('evidence')or date.get('original_quote')!=event['evidence'][0]['quote']or date['original_quote']!=t:return False
  if c['text_sha256']!=H('\n\n'.join(x['text']for x in c['paragraphs']).encode())or o['chapter_text_sha256']!=c['text_sha256']or o['text_sha256']!=H(t.encode())or o['raw_file']!=c['source']['raw_file']or o['raw_sha256']!=c['source']['wikitext_sha256']or not received_paragraph(c,p,root):return False
  clause,term=o['clause'],o['source_term_anchor']
  if not all(anchor(t,x)for x in [clause,term])or term['quote']!=event.get('source_term')or not clause['start']<=term['start']<term['end']<=clause['end']:return False
  if any(not clause['start']<=x['start']<x['end']<=clause['end']or x['kind']!='person'or t[x['start']:x['end']]!=x['surface']for x in [subject,actor]):return False
  if t[:clause['start']].count('「')!=t[:clause['start']].count('」')or any(x in clause['quote']for x in '「」『』'):return False
  A=b['archive'];raw=archive(root,A);unit=next(u for u in A['complete_units']if u['year_label']==b['selected_unit_label']);ya,ea,va,aa=[b[k]for k in ['year_anchor','event_anchor','victim_anchor','actor_anchor']]
  if not all(anchor(raw,x)for x in [ya,ea,va,aa])or not unit['raw_start']<=ya['start']<ya['end']<=ea['start']<ea['end']<=unit['raw_end']or not ea['start']<=va['start']<va['end']<=ea['end']or not ea['start']<=aa['start']<aa['end']<=ea['end']:return False
  if ya['quote']!=date['source_expression']or ya['quote']!=b['selected_unit_label']:return False
  # Event/year anchors cannot be inside a digital ref note or a markup control.
  for match in re.finditer(r'<ref\b[^>]*>.*?</ref>',raw,re.S|re.I):
   if any(match.start()<=x['start']<match.end()for x in [ya,ea,va,aa]):return False
  names={x['surface']for pp in c['paragraphs']for x in pp['mentions']if x.get('person_id')==event['person_id']}
  actor_names={x['surface']for pp in c['paragraphs']for x in pp['mentions']if x.get('person_id')==actor['person_id']}
  if va['quote']not in names or aa['quote']not in actor_names:return False
  inter=raw[ya['end']:ea['start']];inter=re.sub(r'<ref\b[^>]*>.*?</ref>','',inter,flags=re.S|re.I);inter=re.sub(r'（[^）]*）','',inter);inter=inter.replace(date['source_expression'],'')
  if re.search(r'(?:元|[一二三四五六七八九十百]+)年',inter):return False
  # The actual independent era table is retained; not a free numeric assertion.
  r=date['references'][m['reference_index']];table=file(root,r['archived_file']).decode('utf-8');row=r['full_row'];columns=r['columns'];n=numeral(m['source_number'])
  if H(table.encode())!=r['response_sha256']or row not in table or not isinstance(columns.get('dynasty'),str)or not columns['dynasty']or columns['dynasty']not in row or not re.search('>'+re.escape(m['era_name'])+'<',row):return False
  bounds=re.findall(r"<div style='width:8em;'>([0-9]+)</div>",row)
  if bounds!=[str(m['start_ce_year']),str(m['end_ce_year'])]or columns!={'dynasty':columns['dynasty'],'era_name':m['era_name'],'first_year':bounds[0],'last_year':bounds[1]}or n!=m['regnal_year']or date.get('calendar')!='chinese_civil'or date.get('year')!=m['start_ce_year']+n-1 or date['era_year']!=date['year']or not m['start_ce_year']<=date['year']<=m['end_ce_year']or ya['quote']!=m['era_name']+m['source_number']+'年':return False
  if r['quote']!=m['era_name']or r['scope']!='modern_era_year_equivalence_only':return False
  basis=date['basis']
  if basis!={'kind':'parallel_event','source_event_quote':event['source_term'],'reference_url':A['url'],'reference_event_quote':ea['quote'],'reference_year_quote':ya['quote']}:return False
  def rolepos(a):return a['start']-ea['start']
  if b['event_relation']=='named_actor_attacks_named_victim_then_kills':
   # A named actor [escorts sovereign to an explicit gate] attacks named victim,
   # then kills that victim; the origin has the same actor order and actual beheading.
   ap=aa['quote'];vp=va['quote'];q=ea['quote'];match=re.fullmatch(re.escape(ap)+r'(?:(?:奉乘輿)?屯[^，。：「」非未無不]{1,24}，)?攻'+re.escape(vp)+'，殺之',q)
   if not match or rolepos(aa)!=0 or rolepos(va)!=q.index('攻')+1:return False
   origin_pattern=re.escape(actor['surface'])+r'(?:叱|命|令)左右(?:促)?牽出，'+re.escape(subject['surface'])+r'(?:猶)?(?:再顧|顧|泣|請死)?，遂斬於[^，。：「」非未無不]{1,24}'
   if not re.fullmatch(origin_pattern,clause['quote']):return False
  elif b['event_relation']=='named_prisoner_transfer_to_camp_and_execution':
   q=ea['quote'];match=re.fullmatch(r'[甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥]，'+re.escape(aa['quote'])+'取'+re.escape(va['quote'])+'於([^，。：「」]+)，至([^，。：「」]+)，炙而殺之',q)
   if not match or rolepos(aa)!=3 or rolepos(va)!=4+len(aa['quote']):return False
   origin=clause['quote'];expected=actor['surface']+'，'+aa['quote']+'遣部將'
   place=re.search(r'就([^，。：「」]+)收'+re.escape(subject['surface'])+'，至'+re.escape(match[2])+'，炙而殺之$',origin)
   if not place or not(match[1]==place[1]or match[1]==place[1]+'城'or place[1]==match[1]+'城'):return False
   tail=place.group()
   if not origin.startswith(expected)or not origin.endswith(tail):return False
   ante=b['actor_antecedent_anchor'];full=b['full_event_paragraph'];month=b['month_anchor']
   if full['raw_start']!=raw.rfind('\n',0,ea['start'])+1 or full['raw_end']!=raw.index('\n',ea['end']):return False
   if not anchor(raw,ante)or not anchor(raw,month)or ante['quote']not in actor_names or ante['quote']!=o['actor_antecedent_alias']or not full['raw_start']<=ante['start']<ante['end']<ea['start']or raw[full['raw_start']:full['raw_end']]!=full['text']or ea['end']>full['raw_end']:return False
   if month['quote']!=b['local_month_day_confirmation']['month_anchor']['quote']or not ya['end']<=month['start']<month['end']<ea['start']or re.search(r'(?:正|[一二三四五六七八九十]+)月',raw[month['end']:ea['start']]):return False
   # Retain every conflicting annal unit and its real raw, without changing it.
   rejected=b['rejected_context'];rr=archive(root,rejected);ru=next(u for u in rejected['complete_units']if u['year_label']==rejected['selected_unit_label'])
   if rejected['event_quote']not in ru['raw']or not b.get('selection_reason')or not local_day_valid(b,event,chapters,root):return False
   placement=rejected['year_placement'];rt=file(root,placement['era_table_file']).decode('utf-8');rrw=placement['era_table_row'];rn=numeral(placement['source_number'])
   if placement['status']!='not_selected'or placement['era']!='CE'or H(rt.encode())!=placement['era_table_sha256']or rrw not in rt or placement['dynasty']not in rrw or not re.search('>'+re.escape(placement['era_name'])+'<',rrw):return False
   if re.findall(r"<div style='width:8em;'>([0-9]+)</div>",rrw)!=[str(placement['start_ce_year']),str(placement['end_ce_year'])]or rn!=placement['regnal_year']or placement['year']!=placement['start_ce_year']+rn-1 or placement['source_expression']!=placement['era_name']+placement['source_number']+'年'or placement['source_expression']!=ru['year_label']:return False
  else:return False
  return True
 except(KeyError,ValueError,TypeError,IndexError,StopIteration,OSError,UnicodeError,AttributeError):return False

def local_day_valid(binding,event,chapters,root):
 try:
  d=binding['local_month_day_confirmation'];c=next(c for c in chapters.values()if any(p['id']==d['paragraph_id']for p in c['paragraphs']));p=next(p for p in c['paragraphs']if p['id']==d['paragraph_id']);t=p['text'];m=next(m for m in p['mentions']if m['id']==d['person_mention_id']);a=d['clause'];ma=d['month_anchor'];da=d['day_anchor']
  if not received_paragraph(c,p,root)or not all(anchor(t,x)for x in [a,ma,da])or m['person_id']!=event['person_id']or m['start']>=a['start']or t[:a['start']].count('「')!=t[:a['start']].count('」'):return False
  match=re.fullmatch(r'(正|[一二三四五六七八九十]+)月([一二三四五六七八九十]+)日廢，([一二三四五六七八九十]+)日死',a['quote'])
  def num(s):
   z='一二三四五六七八九'
   if s=='正':return 1
   if s in z:return z.index(s)+1
   if '十'in s:
    f,l=s.split('十');return (z.index(f)+1 if f else 1)*10+(z.index(l)+1 if l else 0)
  return bool(match)and all(type(d[k])is int for k in ['month','day','deposition_day'])and 1<=d['month']<=12 and 1<=d['day']<=30 and 1<=d['deposition_day']<=30 and d['month']==num(match[1])and d['deposition_day']==num(match[2])and d['day']==num(match[3])and d['leap_month']is None and ma['quote']==match[1]+'月'and ma['start']==a['start']and da['quote']==match[3]+'日'and da['end']==a['end']-1 and any(e['paragraph_id']==p['id']and e['quote']==t for e in event['evidence'])
 except(KeyError,ValueError,TypeError,IndexError,StopIteration):return False

def date_parts_valid(event,chapters,root):
 try:
  d=event['normalized_date'];p=event['source_date_parts'];b=d['archived_death_year'];a=b['local_month_day_confirmation'];pid=a['paragraph_id']
  keys={'kind','calendar','precision','life_event_id','person_id','month','day','leap_month','source_term','source_anchor','evidence','status','reviewer','human_reviewed'}
  if set(p)!=keys or p['kind']!='explicit_chinese_calendar_month_and_death_day'or not valid(d,event,chapters,root):return False
  anchor_=a['clause'];e=next(e for e in event['evidence']if e['paragraph_id']==pid)
  return(p['calendar']=='chinese_civil'and type(p['month'])is int and type(p['day'])is int and p['precision']=='day'and p['life_event_id']==event['id']and p['person_id']==event['person_id']and p['month']==a['month']and p['day']==a['day']and p['leap_month']is None and p['source_term']==anchor_['quote']and p['source_anchor']=={'paragraph_id':pid,'start':anchor_['start'],'end':anchor_['end'],'surface':anchor_['quote']}and p['evidence']==[e]and p['status']=='source_attested'and p['human_reviewed']is False and bool(p['reviewer']))
 except(KeyError,ValueError,TypeError,IndexError,StopIteration):return False
