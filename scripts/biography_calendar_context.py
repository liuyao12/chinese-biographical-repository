"""Fixed-witness regnal context for an explicitly bounded biographical unit.

The death quote stays local. Era evidence may be separate, but must identify the
same ruler as the unit's explicit accession. No missing paragraphs or competing
regnal era is allowed. A context binds one recorded death, not the whole life.
"""
import json,re,hashlib,html
from pathlib import Path

def sha(b):return hashlib.sha256(b).hexdigest()
def number(s):
    if s=='元':return 1
    ds='一二三四五六七八九'
    if s in ds and len(s)==1:return ds.index(s)+1
    if re.fullmatch('[一二三四五六七八九]?十[一二三四五六七八九]?',s):
        a,b=s.split('十');return (ds.index(a)+1 if a else 1)*10+(ds.index(b)+1 if b else 0)
    return None

def anchor(a,p):
    return (isinstance(a,dict)and set(a)=={'paragraph_id','start','end','surface'}and a['paragraph_id']==p['id']
            and type(a['start'])is int and type(a['end'])is int and 0<=a['start']<a['end']<=len(p['text'])
            and p['text'][a['start']:a['end']]==a['surface'])

def safe(root,rel):
    p=Path(rel)
    if p.is_absolute()or '..'in p.parts:raise ValueError('context path outside root')
    return Path(root)/p

def era_rows(raw):
    rows=[]
    for row in re.findall(r'<tr\b[^>]*>(.*?)</tr>',raw,re.S):
        val=re.search(r'<td[^>]*class=[\'\"]?val[\'\"]?[^>]*>(.*?)</td>',row,re.S)
        sub=re.search(r'<td[^>]*class=[\'\"]?sub[\'\"]?[^>]*>(.*?)</td>',row,re.S)
        if not val or not sub:continue
        name=html.unescape(re.sub('<[^>]+>','',val[1])).strip()
        years=re.findall(r'<div[^>]*>\s*(\d+)\s*</div>',sub[1])
        if len(years)==2 and re.fullmatch('[\u3400-\u9fff]{1,5}',name):rows.append((name,int(years[0]),int(years[1])))
    return rows

def death_subject_valid(p,a,person_id):
    """A local named resumption, or a bare year/death at the unit paragraph start.

    A different named decedent is never hidden by the biography heading. Only
    isolated sovereign permission replies may intervene after the local topic.
    """
    text=p['text'];before=[m for m in p.get('mentions',[])if m.get('kind')=='person'and m['end']<=a['start']]
    topics=[m for m in before if m.get('person_id')==person_id]
    if not topics:
        return not before and re.fullmatch(r'(?:其年|(?:元|[一二三四五六七八九十]+)年)[，。；\s]*',text[:a['start']])is not None
    topic=max(topics,key=lambda m:m['end'])
    for m in before:
        if m['start']<topic['end']or m.get('person_id')==person_id:continue
        if m.get('surface')not in ('上','帝','天子')or(m['start']>0 and text[m['start']-1]not in '，。；'):return False
        end=next((i for i in range(m['end'],a['start'])if text[i]in '，。；'),None)
        if end is None or not re.fullmatch(re.escape(m['surface'])+r'(?:輒|乃|遂|特|又)?(?:優詔不許|不許|詔許之|許之)',text[m['start']:end]):return False
    return True


def context_errors(r,root):
    es=[]
    def ck(ok,msg):
        if not ok:es.append(msg)
    try:
        chapters={}
        for f in (Path(root)/'corpus').glob('*/*.json'):
            x=json.loads(f.read_text())
            if x.get('record_type')=='marked_chapter':chapters[x['id']]=x
        t=r['timeline'];b=r['basis'];ch=chapters[t['chapter_id']];ps={p['id']:p for p in ch['paragraphs']};p=ps[r['anchor']['paragraph_id']]
        ck(b['kind']=='biographical_regnal_context','傳紀年型別不符')
        source=r['source'];raw=safe(root,source['file']).read_bytes();lines=raw.decode().splitlines();rev=source['revision_id']
        ck(sha(raw)==source['sha256']==ch['source']['wikitext_sha256'] and rev==ch['source']['revision_id'] and source['url']==ch['source']['permalink'],'傳紀年固定來源不符')
        ck(r['raw_line']==p['source_position']['first_line']==p['source_position']['last_line'] and r['full_paragraph']==p['text'],'傳紀年事件原段不符')
        for q in ch['paragraphs']:
            n=q['source_position']['first_line']
            if n>r['raw_line']:continue
            ex=next((x for x in ch['source']['normalization']['excerpts']if x['proposed_paragraph_id']==q['id']),{})
            ck(ex.get('raw_quote')==lines[n-1] and ex.get('raw_quote_sha256')==sha(lines[n-1].encode()) and ex.get('selected_text_sha256')==sha(q['text'].encode()),'傳紀年原行／正文字串雜湊不符')
        heading=t['unit_heading_line'];label=re.sub(r'^=+|=+$','',lines[heading-1]).strip()
        ck(lines[heading-1]==t['unit_heading'] and re.fullmatch(r'==[^=]+==',lines[heading-1]) is not None,'傳紀年單元題頭不符')
        ck(heading<r['raw_line'] and not any(re.match(r'^\s*=',s)for s in lines[heading:r['raw_line']]),'傳紀年中途換傳／換話題')
        expected=[q for q in ch['paragraphs']if heading<q['source_position']['first_line']<=r['raw_line']]
        ck(t['paragraph_ids']==[q['id']for q in expected] and bool(expected),'傳紀年跳段／順序不符')
        first=expected[0];topic=next(m for m in first['mentions']if m['id']==t['unit_subject_mention_id'])
        ck(topic.get('person_id')==t['unit_subject_person_id']==r['event_binding']['person_id'] and topic['surface']==label and topic['start']==0,'傳紀年傳主身份或題頭不符')
        ctx=r['context_lines'];ck([x['line']for x in ctx]==list(range(heading,r['raw_line']+1)),'傳紀年原行跳段')
        for x in ctx:ck(x['text']==lines[x['line']-1] and x['sha256']==sha(x['text'].encode()),'傳紀年原行與雜湊不符')
        a=r['anchor'];scope=r['scope'];bind=r['event_binding'];death=bind['source_term_anchor']
        ck(anchor(a,p) and a['surface']==r['original_expression'] and anchor(death,p) and ((bind['event_type']=='death' and bool(re.search('[卒薨死]',death['surface']))) or (bind['event_type']=='posthumous_enfeoffment' and bool(re.fullmatch('追封[^，。；]+',death['surface'])))),'傳紀年日期／死亡錨點不符')
        ck(a['end']<=death['start'],'傳紀年事件不得承後出的年詞')
        subject_death=bind['subject_death_anchor']
        ck(anchor(subject_death,p) and bool(re.search('[卒薨死]',subject_death['surface'])) and p['text'].count(subject_death['surface'])==1 and subject_death['end']<=death['end'],'傳紀年同人死亡支持錨點不符')
        ck(death_subject_valid(p,subject_death,bind['person_id']),'傳紀年死亡局部主語不符，不能只憑傳題')
        if bind['event_type']=='death':ck(bind['death_event_id']==bind['record_id'] and subject_death==death,'傳紀年死亡事件支持不符')
        ck(scope['start']==0 and scope['end']==len(p['text']) and scope['quote']==p['text'],'傳紀年限單一事件原段')
        accession=t['accession_anchor'];ap=ps[accession['paragraph_id']];em=next(m for m in ap['mentions']if m['id']==t['emperor_mention_id'])
        ck(ap['id']in t['paragraph_ids'] and anchor(accession,ap) and accession['start']==em['start'] and accession['surface'] in (em['surface']+'即位',em['surface']+'入奉大統'),'傳紀年明示即位主體不符')
        ec=r['era_context'];ech=chapters[ec['chapter_id']];ep=next(q for q in ech['paragraphs']if q['id']==ec['paragraph_id']);ea=ec['anchor'];ruler=next(m for m in ep['mentions']if m['id']==ec['emperor_mention_id'])
        ck(ruler.get('person_id')==em.get('person_id') and ruler.get('kind')=='person' and em.get('kind')=='person','傳紀年異帝年號不得接線')
        eraw=safe(root,ec['source']['file']).read_bytes();els=eraw.decode().splitlines();ex=next(x for x in ech['source']['normalization']['excerpts']if x['proposed_paragraph_id']==ep['id'])
        ck(sha(eraw)==ec['source']['sha256']==ech['source']['wikitext_sha256'] and ec['source']['revision_id']==ech['source']['revision_id'] and ec['source']['url']==ech['source']['permalink'] and ex['raw_quote']==els[ec['raw_line']-1] and ex['raw_quote_sha256']==sha(ex['raw_quote'].encode()) and ex['selected_text_sha256']==sha(ep['text'].encode()),'傳紀年獨立年號證據不符')
        match=re.fullmatch(r'(.+?)(元|[一二三四五六七八九十]+)年',ea['surface'])
        ck(anchor(ea,ep) and bool(match) and match[1]==b['era'] and number(match[2])is not None,'傳紀年獨立年號原詞不符')
        ref=r['era_reference'];rr=safe(root,ref['file']).read_bytes();rows=era_rows(rr.decode());ck(sha(rr)==ref['sha256'] and (b['era'],ref['first_year'],ref['last_year'])in rows,'傳紀年現代年號表不符')
        names=sorted({x[0]for x in rows},key=len,reverse=True)
        pattern=r'('+ '|'.join(map(re.escape,names))+r')(元|[一二三四五六七八九十]+)年'
        for q in expected:
            n=q['source_position']['first_line'];lo=accession['end']if q['id']==ap['id']else 0
            if n<ap['source_position']['first_line']:continue
            hi=a['end']if q['id']==p['id']else len(q['text'])
            for year in re.finditer(pattern,q['text'][lo:hi]):ck(year[1]==b['era'],'傳紀年中途換年號')
        expression=r['original_expression'];regnal=b['regnal_year'];num=b['source_number']
        ck(type(regnal)is int and regnal==number(num) and regnal>0,'傳紀年原數不符')
        if expression=='其年':
            prior=b['antecedent_anchor'];ck(anchor(prior,p) and prior['surface']==num+'年' and prior['end']<a['start'],'傳紀年其年先行詞不符')
        else:ck(expression==num+'年' and b.get('antecedent_anchor')is None,'傳紀年省略年號原數不符')
        d=r['normalized_date'];ck(d==dict(year=ref['first_year']+regnal-1,calendar='chinese_civil',precision='year',status='editorial_provisional') and d['year']<=ref['last_year'],'傳紀年中國曆年換算不符')
        ck(r['image_verified']is False and r['human_reviewed']is False and r['model']is None,'傳紀年覆核層不符')
    except (KeyError,ValueError,TypeError,IndexError,StopIteration,OSError)as ex:es.append('傳紀年結構錯誤：'+str(ex))
    return es
