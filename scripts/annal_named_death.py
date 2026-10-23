"""A named annal death independently dates an already recorded biographical death."""
import hashlib,re
from pathlib import Path,PurePosixPath

def project_layers(t):
 t=re.sub(r'<pb:[^>]+>','',t);text=[];layers=[];depth=0
 for ch in t:
  if ch=='(':depth+=1;continue
  if ch==')':depth=max(0,depth-1);continue
  if ch.isspace()or ch=='¶':continue
  text.append(ch);layers.append(depth)
 return ''.join(text),layers
def project(t):return project_layers(t)[0]
def span(t,a):return isinstance(a,dict)and set(a)=={'start','end','quote'}and type(a['start'])is int and type(a['end'])is int and 0<=a['start']<a['end']<=len(t)and t[a['start']:a['end']]==a['quote']
def valid(date,event,chapters,root):
 try:
  b=date['named_annal_death_binding'];e,=event['evidence'];ch=chapters[e['chapter_id']];p=next(p for p in ch['paragraphs']if p['id']==e['paragraph_id']);headp=next(p for p in ch['paragraphs']if p['id']==b['biography_head']['paragraph_id']);ms={m['id']:m for m in p['mentions']};subject=ms[e['person_mention_id']];head=next(m for m in headp['mentions']if m['id']==b['biography_head']['mention_id']);a=b['source_anchor']
  assert event['event_type']=='death'and event['status']=='source_attested'and event['normalized_date']==date and b['event_id']==event['id']and b['person_id']==event['person_id']==subject['person_id']==head['person_id']and b['human_reviewed']is False and date['human_reviewed']is False and b['paragraph_sha256']==hashlib.sha256(p['text'].encode()).hexdigest()and e['quote']==p['text']==date['original_quote']and date['evidence']==event['evidence']
  assert subject['start']==a['start']and subject['surface']+'薨'==event['source_term']==a['quote']and span(p['text'],a)and head['start']==0 and headp['text'].startswith(head['surface']+'字')and p['text'][:a['start']].count('「')==p['text'][:a['start']].count('」')
  ref=b['reference'];path=PurePosixPath(ref['path']);assert not path.is_absolute()and'..'not in path.parts and ref['path'].startswith('source-evidence/named-biographical-annal-death/')
  q=(Path(root)/str(path)).resolve();assert Path(root).resolve()in q.parents;raw=q.read_bytes();assert hashlib.sha256(raw).hexdigest()==ref['sha256']and re.fullmatch('[a-f0-9]{40}',ref['revision'])and ref['revision']==ch['source']['revision_id']and ref['url']=='https://raw.githubusercontent.com/kanripo/KR2a0012/'+ref['revision']+'/'+ref['file']and Path(ref['path']).name==ref['file']
  t,layers=project_layers(raw.decode());era,year,ev,actor=[ref[k]for k in('era_heading','year_heading','event','actor')];unit=ref['complete_unit'];assert all(span(t,x)for x in(era,year,ev,actor,unit))and unit['start']<=year['start']<year['end']<=ev['start']<ev['end']<=unit['end']and ev['start']<=actor['start']<actor['end']<=ev['end']and actor['quote']==head['surface']and ev['quote'].endswith(actor['quote']+'薨')
  assert all(not any(layers[x['start']:x['end']])for x in(era,year,ev,actor))
  mapping=date['regnal_year_mapping'];first,last,n=[mapping[k]for k in('start_ce_year','end_ce_year','regnal_year')];nums={'元':1,'二':2,'三':3,'四':4,'五':5,'六':6,'七':7,'八':8,'九':9,'十':10};num=mapping['source_number'];name=mapping['era_name'];assert mapping['kind']=='named_annal_biographical_death'and nums[num]==n and year['quote'].startswith(num+'年')and era['quote']==name+'元年'and era['end']<=unit['start']and name not in t[era['end']:year['start']]
  # Full consecutive annual unit (the preceding year and selected death year).
  assert n>1 and unit['quote'].startswith(next(k for k,v in nums.items()if v==n-1)+'年春')and t[unit['end']:].startswith(next(k for k,v in nums.items()if v==n+1)+'年春')
  between=t[year['end']:ev['start']];assert not re.search(r'(元|[二三四五六七八九十]+)年春',between)
  assert date['calendar']=='chinese_civil'and date['precision']=='year'and date['year_numbering']=='astronomical'and date['status']=='editorial_provisional'and date['era']=='CE'and type(date['year'])is int and date['year']==date['era_year']==first+n-1 and first<=date['year']<=last and not any(k in date for k in('month','day','lunar_month','lunar_day'))
  refs=date['references'];assert refs[0]=={'url':'https://dict.revised.moe.edu.tw/appendix.jsp?ID=3&page=1','scope':'modern_era_year_equivalence_only','quote':name,'columns':{'era_name':name,'first_year':str(first),'last_year':str(last)}}and refs[1]=={'url':ref['url'],'scope':'received_parallel_event','quote':ev['quote']}and refs[2]=={'url':ref['url'],'scope':'received_regnal_year_attestation','quote':year['quote']}
  return date['basis']=={'kind':'parallel_event','source_event_quote':event['source_term'],'reference_url':ref['url'],'reference_event_quote':ev['quote'],'reference_year_quote':year['quote']}
 except(KeyError,TypeError,ValueError,AssertionError,StopIteration,OSError):return False
