"""Optional fixed-witness biography scope for omitted regnal years.

This checks an editorially identified timeline, not NLU of every quoted ruler.
Embedded quotations are explicit exact spans; they do not reset the narrator's era.
"""
import re

def valid(date,chapters):
    s=date.get('narrative_era_scope');es=date.get('evidence',[])
    if not isinstance(s,dict) or not isinstance(chapters,dict) or s.get('kind')!='same_biographical_timeline_with_embedded_quotations':return False
    try:
        ch=chapters[s['chapter_id']];ps=ch['paragraphs'];by={p['id']:p for p in ps};ids=[p['id'] for p in ps]
        a,b=s['era_anchor'],s['event_date_anchor'];ia,ib=ids.index(a['paragraph_id']),ids.index(b['paragraph_id'])
        if ia>ib or s['paragraph_ids']!=ids[ia:ib+1] or s['source_id']!=ch['source_id']:return False
        commit=ch['source'].get('source_commit',ch['source'].get('revision_id'))
        if not commit or s['source_commit']!=commit:return False
        def anchor(x):
            p=by[x['paragraph_id']];return (type(x['start'])is int and type(x['end'])is int and 0<=x['start']<x['end']<=len(p['text']) and p['text'][x['start']:x['end']]==x['surface'])
        if not anchor(a) or not anchor(b) or b['surface']!=date['source_expression']:return False
        if ia==ib and a['end']>b['start']:return False
        if a['surface']!=date['relative_year_reference']['era_expression']:return False
        if len(s['full_paragraphs'])!=ib-ia+1:return False
        for p,q in zip(ps[ia:ib+1],s['full_paragraphs']):
            if q!={'paragraph_id':p['id'],'quote':p['text'],'source_position':p['source_position']} or p['source_position'].get('source_commit',p['source_position'].get('revision_id'))!=commit:return False
        topic=s['unit_topic'];tp=by[topic['paragraph_id']];tm=next(m for m in tp['mentions']if m['id']==topic['person_mention_id'])
        if tm['start']!=0 or tm.get('person_id')!=s['unit_subject_person_id'] or ids.index(tp['id'])>ia:return False
        ruler=s['era_ruler_person_id']
        if s['event_ruler_person_id']!=ruler:return False
        for field in ['era_ruler_reference','event_ruler_reference']:
            e=s[field];p=by[e['paragraph_id']];m=next(m for m in p['mentions']if m['id']==e['person_mention_id'])
            if m.get('person_id')!=ruler or m.get('kind')!='person' or ids.index(p['id'])>ib:return False
        quotations=s['embedded_quotation_scopes'];known=s['known_era_names'];sovereigns=s['sovereign_person_ids']
        if not isinstance(known,list) or date['regnal_year_mapping']['era_name']not in known or ruler not in sovereigns:return False
        for q in quotations:
            if not anchor(q):return False
        for i in range(ia,ib+1):
            p=ps[i];lo=a['start']if i==ia else 0;hi=b['end']if i==ib else len(p['text'])
            def quoted(start,end):return any(q['paragraph_id']==p['id'] and q['start']<=start and end<=q['end']for q in quotations)
            for m in p['mentions']:
                if lo<=m['start']<hi and m.get('person_id')in sovereigns and m.get('person_id')!=ruler and not quoted(m['start'],m['end']):return False
            for match in re.finditer('('+'|'.join(map(re.escape,sorted(known,key=len,reverse=True)))+r')(元|[一二三四五六七八九十]+)年',p['text'][lo:hi]):
                if match[1]!=date['regnal_year_mapping']['era_name']and not quoted(lo+match.start(),lo+match.end()):return False
        return bool(es)and es[-1]['paragraph_id']==b['paragraph_id']and es[-1]['quote']==by[b['paragraph_id']]['text']
    except(KeyError,ValueError,TypeError,IndexError,StopIteration):return False
