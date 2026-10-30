"""Explicit same-event links to an annal year; no person/year lookup or NLU.

The original event evidence is never replaced by the annal container. Both
fixed-source clauses and both marked subjects remain independently checkable.
"""

def fingerprint(ch):
 s=ch.get('source',{})
 return {'source_id':ch.get('source_id'),'revision':s.get('source_commit',s.get('revision_id')),'blob':s.get('source_blob_sha',s.get('source_blob')),'raw_sha256':s.get('response_sha256',s.get('raw_file_sha256'))}

def exact(anchor,p):
 return (isinstance(anchor,dict)and set(anchor)=={'paragraph_id','start','end','surface'}
         and anchor['paragraph_id']==p.get('id')and type(anchor['start'])is int and type(anchor['end'])is int
         and 0<=anchor['start']<anchor['end']<=len(p['text'])and p['text'][anchor['start']:anchor['end']]==anchor['surface'])

def marked(p,mid,pid,*,allow_pronoun=False):
 hits=[m for m in p.get('mentions',[])if m.get('id')==mid]
 if len(hits)!=1:return None
 m=hits[0]
 return m if (m.get('kind')=='person'or(allow_pronoun and m.get('kind')=='pronoun'and m.get('surface')=='之'))and m.get('person_id')==pid and p['text'][m['start']:m['end']]==m['surface'] else None

def cross_chapter_annal_date_valid(date,record,role,chapters):
 try:
  b=date.get('cross_chapter_event_binding')
  if (not isinstance(b,dict)or set(b)!={'kind','record_id','person_id','role','origin','annal','status','human_reviewed','rationale','linkage'}
      or b['kind']!='same_event_fixed_work_annal_date'or b['record_id']!=record.get('id')or b['person_id']!=record.get('person_id')
      or b['role']!=role or role not in('life_event','start')or b['status']!='editorial_provisional'
      or b['human_reviewed']is not False or not b['rationale']or date.get('calendar')!='chinese_civil'
      or date.get('regnal_year_mapping',{}).get('kind')!='ce_regnal_era_span'):
   return False
  mapping=date['regnal_year_mapping'];ref=date['references'][mapping['reference_index']];number=mapping['source_number'];digits='一二三四五六七八九'
  def integer(s):
   if s=='元':return 1
   if s in digits and len(s)==1:return digits.index(s)+1
   if re_full_tens(s):
    a,b=s.split('十');return (digits.index(a)+1 if a else 1)*10+(digits.index(b)+1 if b else 0)
   return None
  import re
  def re_full_tens(s):return isinstance(s,str)and re.fullmatch('[一二三四五六七八九]?十[一二三四五六七八九]?',s)
  n=integer(number);first=mapping['start_ce_year'];last=mapping['end_ce_year']
  if type(first)is not int or type(last)is not int or n is None or n!=mapping['regnal_year']or date.get('year')!=first+n-1 or not first<=date['year']<=last:return False
  if date.get('source_expression')!=mapping['era_name']+number+'年'or ref.get('quote')!=mapping['era_name']or ref.get('scope')!='modern_era_year_equivalence_only'or ref.get('columns',{}).get('first_year')!=str(first)or ref.get('columns',{}).get('last_year')!=str(last):return False
  origin,annal=b['origin'],b['annal']
  keys={'chapter_id','paragraph_id','fingerprint','person_mention_id','event_anchor','subject_clause_anchor'}
  if set(origin)!=keys or set(annal)!=keys|{'year_anchor','date_clause_anchor'}:return False
  oc,ac=chapters[origin['chapter_id']],chapters[annal['chapter_id']]
  if oc['id']==ac['id']or oc['work_id']!=ac['work_id']:return False
  of,af=fingerprint(oc),fingerprint(ac)
  if (origin['fingerprint']!=of or annal['fingerprint']!=af or of['revision']!=af['revision']
      or not all(isinstance(v,str)and v for v in list(of.values())+list(af.values()))):return False
  op=next(p for p in oc['paragraphs']if p['id']==origin['paragraph_id']);ap=next(p for p in ac['paragraphs']if p['id']==annal['paragraph_id'])
  if ap.get('text_layer')!='received_chapter'or ap.get('source_position',{}).get('source_layer')!='received_annal':return False
  om=marked(op,origin['person_mention_id'],record['person_id'],allow_pronoun=True);am=marked(ap,annal['person_mention_id'],record['person_id'])
  if not om or not am:return False
  for side,p,m in [(origin,op,om),(annal,ap,am)]:
   ea,sa=side['event_anchor'],side['subject_clause_anchor']
   if not(exact(ea,p)and exact(sa,p)and sa['start']==m['start']and m['end']<=ea['end']==sa['end']and sa['start']<=ea['start']):return False
   # Every explicitly marked person between this subject and event must be this person.
   if (side is annal or role=='start')and any(x.get('kind')in ('person','pronoun')and sa['start']<=x['start']<sa['end']and x.get('person_id')!=record['person_id']for x in p['mentions']):return False
  oa,aa=origin['event_anchor'],annal['event_anchor']
  year,clause=annal['year_anchor'],annal['date_clause_anchor']
  if (not exact(year,ap)or not exact(clause,ap)or year['surface']!=date.get('source_expression')
      or year['end']>clause['start']or clause['end']!=aa['end']or not clause['start']<=am['start']
      or not isinstance(date.get('evidence'),list)or len(date['evidence'])!=1):return False
  de=date['evidence'][0]
  if (any(de.get(k)!=ac[k]for k in ('work_id','book_id','source_id'))or de.get('chapter_id')!=ac['id']
      or de.get('paragraph_id')!=ap['id']or de.get('person_mention_id')!=am['id']
      or de.get('quote')!=ap['text']or date.get('original_quote')!=ap['text']):return False
  # Preserve full original evidence and bind this exact original record, not an arbitrary other death/holding.
  es=record.get('evidence',[])
  if not any(e.get('chapter_id')==oc['id']and e.get('paragraph_id')==op['id']and e.get('quote')==op['text']and e.get('person_mention_id')==om['id']for e in es):return False
  import re
  linkage=b['linkage'];head=marked(op,linkage.get('biography_head_mention_id'),record['person_id'])
  if not head or head['start']!=0 or not op['text'][head['end']:].startswith(('字','諱')):return False
  if role=='life_event':
   if (record.get('event_type')!='death'or record.get('status')!='source_attested'
       or not isinstance(record.get('source_term'),str)or record['source_term']!=oa['surface']
       or not re.fullmatch(r'(?:㑹|會)?病[薨卒死](?:年[一二三四五六七八九十百]+)?',oa['surface'])
       or aa['surface']!=am['surface']+'薨'):return False
   if set(linkage)!={'kind','biography_head_mention_id'}or linkage['kind']!='existing_illness_death_of_biography_subject':return False
   prefix=clause['surface'][:-len(am['surface']+'薨')]
   if not re.fullmatch(r'[春夏秋冬]?(?:正|[一二三四五六七八九十]+)月[甲乙丙丁戊己庚辛壬癸子丑寅卯辰巳午未申酉戌亥]{0,2}[^年月死卒薨殺害生曰云，。；]{0,12}',prefix):return False
   if any(m.get('kind')in ('person','pronoun')and clause['start']<=m['start']<am['start']and m.get('person_id')!=record['person_id']for m in ap['mentions']):return False
   # This narrow annal grammar is a named person immediately followed by 薨.
   if aa['start']!=am['start']or aa['end']!=am['end']+1:return False
  else:
   title=record.get('title')
   if not appointment_episode_valid(linkage,record,op,ap,oa,aa,am,date,chapters):return False
   if (record.get('mode')!='grant'or not isinstance(title,str)or not title
       or oa['surface']!='進拜'+title or aa['surface']!='為'+title
       or aa['start']!=am['end']or not record.get('effective_period',{}).get('start',{}).get('evidence')):return False
  # All numeric year expressions between the chosen frame and event must remain the same frame.
  import re
  after=ap['text'][year['end']:aa['end']]
  if re.search(r'[元一二三四五六七八九十百]+年',after):return False
  return True
 except(KeyError,TypeError,ValueError,IndexError,StopIteration,AttributeError):return False


def appointment_episode_valid(q,h,op,ap,oa,aa,am,date,chapters):
 try:
  if set(q)!={'kind','biography_head_mention_id','origin_attestation_id','origin_episode_anchor','origin_relocation_anchor','origin_prior_office','annal_prior_office','annal_followup','following_year_reference_index'}or q['kind']!='unique_appointment_episode_with_shared_relocation':return False
  ats=[a for a in h.get('attestations',[])if a.get('id')==q['origin_attestation_id']]
  if len(ats)!=1:return False
  at=ats[0]
  if at['paragraph_id']!=op['id']or at['surface']!=h['title']or at['end']!=oa['end']or at['start']!=oa['end']-len(h['title']):return False
  ep,rel=q['origin_episode_anchor'],q['origin_relocation_anchor']
  if not exact(ep,op)or not exact(rel,op)or ep['end']!=oa['end']or ep['start']>=oa['start']or ep['end']>rel['start']:return False
  # A first assignment followed after three days by this elevation; no repeat assignment or removal is silently collapsed.
  prior=q['origin_prior_office'];target=q['annal_prior_office']
  if not isinstance(prior,str)or not isinstance(target,str)or prior.replace('勲','勳')!=target:return False
  if ep['surface']!='復追為'+prior+'視事三日'+oa['surface']or ap['text'][am['start']-len(target):am['start']]!=target:return False
  if op['text'].count(oa['surface'])!=1 or ap['text'].count(am['surface']+aa['surface'])!=1:return False
  if any(v in op['text'][ep['end']:rel['start']]for v in('罷','免','復拜','復為')):return False
  if not rel['surface'].startswith('因從遷都')or len(rel['surface'])<=4:return False
  follow=q['annal_followup'];fc=chapters[follow['chapter_id']];p=next(p for p in fc['paragraphs']if p['id']==follow['paragraph_id'])
  if (p.get('text_layer')!='received_chapter'or p.get('source_position',{}).get('source_layer')!='received_annal'or p.get('source_position',{}).get('first_line',0)<=ap.get('source_position',{}).get('last_line',0)):return False
  if fc['id']!=date['evidence'][0]['chapter_id']or not exact(follow['year_anchor'],p)or not exact(follow['relocation_anchor'],p):return False
  location=rel['surface'][4:]
  if follow['relocation_anchor']['surface']!='遷都'+location or follow['year_anchor']['start']!=0 or follow['year_anchor']['end']>follow['relocation_anchor']['start']:return False
  ri=q['following_year_reference_index'];ref=date['references'][ri];m=ref['columns'];expr=follow['year_anchor']['surface']
  if expr!=m['era_name']+'元年'or int(m['first_year'])!=date['year']+1 or ref.get('scope')!='modern_era_year_equivalence_only':return False
  return True
 except(KeyError,ValueError,TypeError,IndexError,StopIteration):return False
