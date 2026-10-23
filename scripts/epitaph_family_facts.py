"""Fail-closed complete named epitaph clauses; no canonical identity allowlists."""
import hashlib,re
KIND='epitaph_named_family_full'
def errors(chapters,records):
 out=[]
 for c in chapters.values():
  rs=[r for r in records if r.get('chapter_id')==c['id'] and r.get('record_type')in {'person_assertion_set','person_life_event_assertion_set','person_name_component_set','person_address_assertion_set','person_event_assertion_set'}]
  binding=c.get('annotation',{}).get('epitaph_fact_binding')
  if not binding:
   if c.get('paragraphs')and c['paragraphs'][0].get('text_layer')=='epitaph_as_modernly_transcribed'and rs:out.append('Typed epitaph facts need complete source binding')
   continue
  try:_valid(c,rs,binding)
  except (AssertionError,KeyError,ValueError,TypeError,StopIteration,IndexError):out.append('Epitaph full-context family/date/name binding invalid: '+c['id'])
 return out

def _valid(c,rs,b):
 if b.get('kind')=='epitaph_named_head_titled_ancestors':
  try:
   from scripts.epitaph_titled_ancestors import valid
  except ImportError:
   from epitaph_titled_ancestors import valid
  if c.get('annotation',{}).get('epitaph_life_binding'):
   try:from scripts.epitaph_named_lifecycle import valid as life_valid
   except ImportError:from epitaph_named_lifecycle import valid as life_valid
   life_valid(c,rs)
   return valid(c,[r for r in rs if r['record_type']=='person_assertion_set'],b)
  return valid(c,rs,b)
 assert set(b)=={'kind','paragraph_id','roles','paragraph_sha256','source_id','witness_pdf_sha256'} and b['kind']==KIND
 p,=c['paragraphs'];t=p['text'];assert b['paragraph_id']==p['id']and b['source_id']==c['source_id']and hashlib.sha256(t.encode()).hexdigest()==b['paragraph_sha256']
 witness=c['source']['transcription_witness'];assert witness['pdf_sha256']==b['witness_pdf_sha256']and witness['original_stone_or_rubbing_image_verified']is False and c['source']['revision_id']is None
 assert p['text_layer']=='epitaph_as_modernly_transcribed'
 ms={m['id']:m for m in p['mentions']};roles={k:ms[v]for k,v in b['roles'].items()}
 assert set(roles)=={'head','zi','grandfather','father','wife','wife_zi','younger1','younger2','younger3'}
 for m in roles.values():assert m['kind']=='person'and t[m['start']:m['end']]==m['surface']
 S=lambda k:roles[k]['surface'];I=lambda k:roles[k]['person_id']
 assert I('head')==I('zi')and I('wife')==I('wife_zi')and len({I(k)for k in roles if k not in ('zi','wife_zi')})==7
 assert len(S('head'))>=2 and S('wife').endswith('氏')and len(S('wife'))==2
 pat=r'晉故男子(?P<origin>[^非不未無]+里)'+re.escape(S('head'))+'字'+re.escape(S('zi'))+r'故(?P<titles>[^非不未無]+)'+re.escape(S('grandfather'))+'之孫贛令'+re.escape(S('father'))+r'之元子年(?P<age>[一二三四五六七八九十廿卅]+)(?P<date>(?P<era>[^非不未無年月日]+)(?P<year>[一二三四五六七八九十元]+)年(?P<month>[一二三四五六七八九十]+)月(?P<day>[一二三四五六七八九十]+)日)卒葬于舊墓在贛令墓之後故刻塼於墓為識妻(?P<worigin>[^非不未無]+)'+re.escape(S('wife'))+'字'+re.escape(S('wife_zi'))+'弟'+''.join(re.escape(S(k))for k in ['younger1','younger2','younger3'])
 hit=re.fullmatch(pat,t);assert hit
 # Reconstruct every named role position from the complete grammar, not nearest names.
 prefix='晉故男子'+hit['origin'];assert roles['head']['start']==len(prefix)
 literals=[('head',prefix),('zi',prefix+S('head')+'字'),('grandfather',prefix+S('head')+'字'+S('zi')+'故'+hit['titles'])]
 for k,pre in literals:assert roles[k]['start']==len(pre)
 assert roles['father']['start']==roles['grandfather']['end']+len('之孫贛令')
 assert roles['wife']['start']==t.index('妻',hit.end('date'))+1+len(hit['worigin'])and roles['wife_zi']['start']==roles['wife']['end']+1
 cursor=roles['wife_zi']['end']+1
 for k in ['younger1','younger2','younger3']:assert roles[k]['start']==cursor;cursor=roles[k]['end']
 def evidence(e,sk,ok=None):
  assert e['quote']==t and e['paragraph_id']==p['id']and e['chapter_id']==c['id']and all(e[k]==c[k]for k in ['work_id','book_id','source_id'])
  if ok:assert e['subject_person_mention_id']==roles[sk]['id']and e['object_person_mention_id']==roles[ok]['id']
  else:assert e['person_mention_id']==roles[sk]['id']
 assertions=[a for r in rs if r['record_type']=='person_assertion_set'for a in r['assertions']]
 expected={('father',I('head'),I('father')):('head','father','之元子'),('grandfather',I('head'),I('grandfather')):('head','grandfather','之孫'),('spouse',I('head'),I('wife')):('head','wife','妻')}
 for k in ['younger1','younger2','younger3']:expected[('brother',I(k),I('head'))]=(k,'head','弟')
 assert len(assertions)==len(expected)
 for a in assertions:
  sk,ok,term=expected.pop((a['predicate'],a['subject_person_id'],a['object_person_id']));q=a['qualifiers'];assert q['source_clause_binding']==b and q['source_term']==term
  assert a['status']=='source_attested'and a['human_reviewed']is False and len(a['evidence'])==1;evidence(a['evidence'][0],sk,ok)
  extras={}
  if a['predicate']=='father':extras={'birth_order':{'parent_person_id':I('father'),'scope':'sons_of_parent','ordinal':1,'position':'eldest','interpretation_status':'source_attested'}}
  if a['predicate']=='grandfather':extras={'lineage':'paternal'}
  if a['predicate']=='brother':extras={'relative_birth_order':{'older_person_id':I('head'),'younger_person_id':I(sk),'operator':'lt','scope':'siblings','older_ordinal':None,'younger_ordinal':None}}
  assert q=={'source_term':term,'source_clause_binding':b,**extras}
 names=[n for r in rs if r['record_type']=='person_name_component_set'for n in r['records']];assert len(names)==7
 for k in ['head','grandfather','father','wife','younger1','younger2','younger3']:
  n,=[n for n in names if n['person_id']==I(k)];assert n['quote']==t and n['paragraph_id']==p['id']and n['chapter_id']==c['id']and n['human_reviewed']is False
  assert n['surname']==(S(k)[0]if k in ['head','wife']else None)and n['ming']==(S(k)[1:]if k=='head'else None if k=='wife'else S(k))and n.get('zi')==(S('zi')if k=='head'else S('wife_zi')if k=='wife'else None)and n['additional_names']==[]
 ages=c['annotation']['age_assertions'];age,=ages
 assert age['person_id']==I('head')and age['source_number']==hit['age']and age['source_term']=='年'+hit['age']and age['birth_year']is None and age['date_expression']is None and age['human_reviewed']is False;evidence(age['evidence'][0],'head')
 events=[e for r in rs if r['record_type']=='person_life_event_assertion_set'for e in r['events']];event,=events
 assert event['person_id']==I('head')and event['event_type']=='death'and event['source_term']=='卒'and event['date_expression']==hit['date']and event['human_reviewed']is False
 evidence(event['evidence'][0],'head');assert len(event['evidence'])==1
 def anchor(v,s):assert v=={'paragraph_id':p['id'],'start':t.index(s),'end':t.index(s)+len(s),'surface':s}
 anchor(event['source_anchor'],'卒');dp=event['epitaph_date_parts'];assert set(dp)=={'calendar','month','day','month_anchor','day_anchor','precision'}and dp['calendar']=='chinese_lunisolar'and dp['precision']=='source_month_day_no_gregorian_conversion'
 anchor(dp['month_anchor'],hit['month']+'月');anchor(dp['day_anchor'],hit['day']+'日')
 try:from scripts.validate_corpus import source_age_number,normalized_date_errors
 except ImportError:from validate_corpus import source_age_number,normalized_date_errors
 assert dp['month']==source_age_number(hit['month'])and dp['day']==source_age_number(hit['day'])and 1<=dp['month']<=12 and 1<=dp['day']<=30
 date=event['normalized_date'];assert date['source_expression']==hit['era']+hit['year']+'年'and date['evidence']==event['evidence']and date['original_quote']==t and not normalized_date_errors(date,{c['id']:c})
 # Preserve exact reported age; no age-derived birth in any record.
 assert age['value']==source_age_number(hit['age'])and age['counting']=='unspecified_source_age'
 addresses=[a for r in rs if r['record_type']=='person_address_assertion_set'for a in r['assertions']];assert len(addresses)==2
 for relation,place,term in [('biographical_origin',hit['origin'],hit['origin']),('burial_place','舊墓在贛令墓之後','葬于舊墓在贛令墓之後')]:
  a,=[a for a in addresses if a['relation']==relation];assert a['person_id']==I('head')and a['place']=={'source_name':place,'place_id':None,'modern_identification':None}and a['source_term']==term and a['date_expression']is None and 'normalized_date'not in a;evidence(a['evidence'][0],'head')
