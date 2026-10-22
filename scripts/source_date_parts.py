"""A literal Chinese month bound to one already validated local death/date chain.

No Gregorian conversion, season-to-month inference or day inference is performed.
"""
import re

def explicit_month_parts_valid(parts, text, expression_anchor, parse_number):
    """Lexical component; permits synthetic tests without pretending a new witness."""
    if not isinstance(parts,dict):return False
    a=parts.get('source_anchor');term=parts.get('source_term');number=parts.get('source_number')
    if not isinstance(a,dict)or set(a)!={'paragraph_id','start','end','surface'}or not isinstance(expression_anchor,dict):return False
    try:
        valid=(type(a['start'])is int and type(a['end'])is int and 0<=a['start']<a['end']<=len(text)
               and text[a['start']:a['end']]==a['surface']==term
               and a['paragraph_id']==expression_anchor['paragraph_id']
               and expression_anchor['start']<=a['start']<a['end']<=expression_anchor['end'])
        match=re.fullmatch(r'(閏)?(正|[一二三四五六七八九十]+)月',term)if isinstance(term,str)else None
        if not valid or not match:return False
        n=1 if match[2]=='正'else parse_number(match[2])
        return (number==match[2] and type(parts.get('month'))is int and type(n)is int
                and 1<=n<=12 and parts['month']==n
                and (parts.get('leap_month')is True if match[1]else parts.get('leap_month')is None)
                and ('day'not in parts or parts['day']is None))
    except(KeyError,TypeError,IndexError):return False

def source_date_parts_valid(event,chapters,parse_number,root=None):
    if event.get("source_date_parts",{}).get("kind")=="explicit_chinese_calendar_month_and_death_day":
        try:
            from scripts.archived_parallel_death import date_parts_valid
        except ImportError:
            from archived_parallel_death import date_parts_valid
        return date_parts_valid(event,chapters,root)
    try:
        from scripts.local_death_date_evidence import local_death_date_evidence_valid
    except ImportError:
        from local_death_date_evidence import local_death_date_evidence_valid
    try:
        p=event.get('source_date_parts');d=event.get('normalized_date')
        keys={'kind','calendar','precision','life_event_id','person_id','month','source_number','source_term','leap_month','source_anchor','evidence','status','reviewer','human_reviewed'}
        if (not isinstance(p,dict)or set(p)-{'day'}!=keys
                or p.get('kind')!='explicit_chinese_calendar_month' or p.get('calendar')!='chinese_civil'
                or p.get('precision')!='month' or p.get('status')!='source_attested'
                or p.get('human_reviewed')is not False or not isinstance(p.get('reviewer'),str)or not p['reviewer']
                or p.get('life_event_id')!=event.get('id')or p.get('person_id')!=event.get('person_id')
                or not isinstance(d,dict)or d.get('precision')!='year'
                or not local_death_date_evidence_valid(d,event,chapters,parse_number)):
            return False
        if 'cross_chapter_event_binding' in d:
            b=d['cross_chapter_event_binding']['annal'];e=d['evidence'][0]
            if p['evidence'] != [e]:return False
            chapter=chapters[e['chapter_id']];paragraph=next(x for x in chapter['paragraphs']if x['id']==e['paragraph_id'])
            return explicit_month_parts_valid(p,paragraph['text'],b['date_clause_anchor'],parse_number)
        b=d['event_evidence_binding'];e=d['evidence'][b['date_evidence_index']]
        if p['evidence']!=[e]:return False
        chapter=chapters[e['chapter_id']];paragraph=next(x for x in chapter['paragraphs']if x['id']==e['paragraph_id'])
        return (p['source_anchor']['paragraph_id']==paragraph['id']
                and explicit_month_parts_valid(p,paragraph['text'],b['event_date_expression_anchor'],parse_number))
    except(KeyError,TypeError,ValueError,IndexError,StopIteration,AttributeError):return False
