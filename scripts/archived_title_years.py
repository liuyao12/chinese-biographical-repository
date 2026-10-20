"""Fixed primary-annal parallels date a named title event, never an entire paragraph."""
import hashlib,re
from pathlib import PurePosixPath

def project(raw):
    out=[];depth=0;i=0
    while i<len(raw):
        if raw.startswith('<pb:',i):
            j=raw.find('>',i)
            if j<0:return None
            i=j+1;continue
        c=raw[i];i+=1
        if c=='(':depth+=1;continue
        if c==')':
            depth-=1
            if depth<0:return None
            continue
        if not depth and not c.isspace()and c!='¶':out.append(c)
    return ''.join(out)if depth==0 else None

def has_intervening_year(text):
    # Conservative rejection: a bare year, year+month, era change, or quoted
    # numeric-year statement must be reviewed rather than crossed automatically.
    return re.search(r'[元一二三四五六七八九十百廿卅零〇]+年', text) is not None

def span(text,v):
    return (isinstance(v,dict)and set(v)=={'start','end','quote'}and type(v.get('start'))is int and type(v.get('end'))is int and 0<=v['start']<v['end']<=len(text)and text[v['start']:v['end']]==v.get('quote'))

def valid(date,holding,role,chapters,root):
    if not isinstance(date,dict):return False
    b=date.get('archived_title_year');m=date.get('regnal_year_mapping')
    if not isinstance(b,dict)or not isinstance(m,dict)or m.get('kind')!='archived_parallel_title_ce_span':return False
    if not isinstance(holding,dict)or role not in ('start','end')or holding.get('id')!=b.get('holding_id')or holding.get('person_id')!=b.get('person_id')or role!=b.get('role')or holding.get('kind')!='office':return False
    boundary=holding.get('effective_period',{}).get(role,{})
    if boundary.get('normalized_date')!=date or boundary.get('evidence')!=date.get('evidence')or boundary.get('status')!='source_event':return False
    if role=='start'and boundary.get('event_type')not in ('grant','transfer'):return False
    if role=='end'and boundary.get('event_type')not in ('deposition','explicit_end'):return False
    source=b.get('source_event_quote');title=holding.get('title');ref=b.get('reference',{})
    if not isinstance(ref,dict):return False
    if not isinstance(source,str)or not source or source not in date.get('original_quote','')or not any(source in e.get('quote','')for e in date.get('evidence',[])):return False
    # Source event is exact original text; origin attestation remains mandatory.
    if role=='start'and(title not in source or not any(v in source for v in ('遷','拜','為'))):return False
    if role=='end'and'免'not in source:return False
    path=ref.get('path');p=PurePosixPath(path)if isinstance(path,str)else None
    if not p or p.is_absolute()or'..'in p.parts or not path.startswith('source-evidence/sgz009-titles/'):return False
    try:raw=(root/path).read_bytes()
    except(OSError,TypeError):return False
    if hashlib.sha256(raw).hexdigest()!=ref.get('sha256')or not re.fullmatch('[a-f0-9]{40}',str(ref.get('revision_id',''))):return False
    if ref.get('url')!='https://raw.githubusercontent.com/kanripo/KR2a0012/'+ref['revision_id']+'/'+ref.get('file',''):return False
    text=project(raw.decode('utf-8'));anchors=[ref.get(k)for k in ('era_heading','year_heading','event','actor','title')]
    if not text or not all(span(text,a)for a in anchors):return False
    era,year,event,actor,tanchor=anchors
    if not(era['start']<=year['start']<=event['start']<=actor['start']<actor['end']<=event['end']and event['start']<=tanchor['start']<tanchor['end']<=event['end']):return False
    chapter=chapters.get(date['evidence'][0]['chapter_id'],{});names={x.get('surface')for p in chapter.get('paragraphs',[])for x in p.get('mentions',[])if x.get('person_id')==holding['person_id']}
    if actor['quote']not in names or tanchor['quote']!=title:return False
    name=m.get('era_name');source_name=m.get('source_era_name',name);number=m.get('source_number');n=m.get('regnal_year');first=m.get('start_ce_year');last=m.get('end_ce_year')
    nums={'元':1,'二':2,'三':3,'四':4,'五':5,'六':6,'七':7,'八':8,'九':9,'十':10}
    if not(source_name==name or(source_name,name)==('黄初','黃初'))or not isinstance(source_name,str)or source_name not in era['quote']or not year['quote'].startswith(str(number)+'年')or type(n)is not int or n!=nums.get(number):return False
    if has_intervening_year(text[year['end']:event['start']]):return False
    # A later era heading between the selected era and event is not permitted.
    if any(e in text[era['end']:event['start']]for e in ('太和元年','青龍元年','景初元年','嘉平元年')):return False
    refs=date.get('references',[]);index=m.get('reference_index');r=refs[index]if type(index)is int and 0<=index<len(refs)else{}
    if not(type(first)is int and type(last)is int and type(date.get('year'))is int and type(date.get('era_year'))is int and first<=date.get('year',-1)<=last and date['year']==first+n-1 and date.get('era')=='CE'and date.get('era_year')==date['year']and date.get('calendar')=='chinese_civil'and r.get('scope')=='modern_era_year_equivalence_only'and r.get('quote')==name and r.get('columns')=={'era_name':name,'first_year':str(first),'last_year':str(last)}):return False
    basis=date.get('basis',{})
    if not isinstance(basis,dict)or basis.get('kind')!='parallel_event'or basis.get('source_event_quote')!=source or basis.get('reference_url')!=ref['url']or basis.get('reference_event_quote')!=event['quote']or basis.get('reference_year_quote')!=text[era['start']:year['end']]:return False
    relation=b.get('event_relation');q=event['quote'];a=actor['quote']
    if relation=='same_explicit_appointment':return role=='start'and(a+'為'+title in q)and tanchor['start']==actor['end']+1
    if relation=='same_named_deposition':return role=='end'and('免'+title+a in q)and tanchor['end']==actor['start']
    if relation=='anaphoric_successor':return role=='start'and q.endswith(a+'代之')and re.fullmatch('以[^以]+為'+re.escape(title)+'甲申免以武衛將軍'+re.escape(a)+'代之',q)is not None
    return False

def local_valid(date,holding,role,chapters):
    m=date.get('regnal_year_mapping',{});b=date.get('local_title_year',{})
    if m.get('kind')!='source_orthographic_ce_regnal_span'or not isinstance(holding,dict)or role!='start':return False
    if b.get('holding_id')!=holding.get('id')or b.get('person_id')!=holding.get('person_id'):return False
    boundary=holding.get('effective_period',{}).get(role,{})
    if boundary.get('normalized_date')!=date or boundary.get('evidence')!=date.get('evidence')or boundary.get('event_type')!='grant':return False
    if (m.get('source_era_name'),m.get('era_name'))!=('黄初','黃初')or m.get('source_number')!='三'or m.get('regnal_year')!=3:return False
    e=date.get('evidence',[])
    if len(e)!=1 or date.get('original_quote')!=e[0].get('quote'):return False
    quote=e[0]['quote'];clause=b.get('source_event_quote');yr=b.get('year_anchor');title=b.get('title_anchor')
    if not span(quote,yr)or not span(quote,title)or yr['quote']!='黄初三年'or title['quote']!=holding.get('title')or not isinstance(clause,str)or clause not in quote:return False
    start=quote.index(clause);end=start+len(clause)
    if not(start==yr['start']<yr['end']<=title['start']<title['end']<=end)or '還京都以真為'not in clause:return False
    a=next((a for a in holding.get('attestations',[])if a.get('paragraph_id')==e[0]['paragraph_id']and a.get('start')==title['start']and a.get('surface')==title['quote']),None)
    p=next((p for p in chapters.get(e[0]['chapter_id'],{}).get('paragraphs',[])if p['id']==e[0]['paragraph_id']),{})
    if not a or not any(x.get('id')==a.get('person_mention_id')and x.get('person_id')==holding['person_id']and x.get('surface')=='真'and yr['end']<=x.get('start',-1)<title['start']for x in p.get('mentions',[])):return False
    refs=date.get('references',[]);i=m.get('reference_index');r=refs[i]if type(i)is int and 0<=i<len(refs)else{}
    return date.get('calendar')=='chinese_civil'and date.get('year')==222 and date.get('era_year')==222 and m.get('start_ce_year')==220 and m.get('end_ce_year')==226 and r.get('scope')=='modern_era_year_equivalence_only'and r.get('quote')=='黃初'and r.get('columns')=={'era_name':'黃初','first_year':'220','last_year':'226'}
