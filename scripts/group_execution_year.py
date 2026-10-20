"""Bind an explicitly named execution group to a retained biography year chain."""
import re

def valid(date,event,chapters,parse_number):
    try:
        from scripts.relative_regnal_year import relative_regnal_year_valid
        from scripts.relative_biography_scope import valid as scope_valid
    except ImportError:
        from relative_regnal_year import relative_regnal_year_valid
        from relative_biography_scope import valid as scope_valid
    try:
        b=date['event_evidence_binding'];scope=date['narrative_era_scope'];ch=chapters[scope['chapter_id']];ps=ch['paragraphs'];by={p['id']:p for p in ps};ids=[p['id']for p in ps]
        if (b['kind']!='named_group_execution_after_biographical_year_chain'or b['life_event_id']!=event['id']or b['person_id']!=event['person_id']
                or event['event_type']!='death'or event['status']!='source_attested'or event['date_expression']!=date['source_expression']
                or date.get('calendar')!='chinese_civil'or date.get('precision')!='year'or event.get('source_date_parts')is not None
                or not relative_regnal_year_valid(date,parse_number,chapters)or not scope_valid(date,chapters)):return False
        mapping=date['regnal_year_mapping']
        if (mapping.get('era_name'),mapping.get('start_ce_year'),mapping.get('end_ce_year'),mapping.get('target_regnal_year'),date.get('year'),date.get('era_year'))!=('正始',240,249,10,249,249):return False
        if set(b)!={'kind','life_event_id','person_id','source_fingerprint','year_chain','tail_paragraph_ids','tail_full_paragraphs','embedded_source_paragraph_ids','execution_group_anchor','execution_member_mention_ids','event_person_mention_id','reported_plan_anchor'}or any(k in date for k in ['month','day','lunar_month','calendar_month']):return False
        expected={'source_id':ch['source_id'],'revision_id':ch['source']['revision_id'],'raw_sha256':ch['source']['raw_sha256'],'text_sha256':ch['text_sha256']}
        if b['source_fingerprint']!=expected:return False
        anchors=b['year_chain'];required=['正始五年','九年冬','十年正月']
        if [a['surface']for a in anchors]!=required:return False
        def exact(a):
            p=by[a['paragraph_id']];return(set(a)=={'paragraph_id','start','end','surface'}and type(a['start'])is int and type(a['end'])is int and 0<=a['start']<a['end']<=len(p['text'])and p['text'][a['start']:a['end']]==a['surface'])
        if not all(exact(a)for a in anchors)or [ids.index(a['paragraph_id'])for a in anchors]!=sorted(ids.index(a['paragraph_id'])for a in anchors):return False
        if anchors[0]!=scope['era_anchor']or anchors[-1]['paragraph_id']!=scope['event_date_anchor']['paragraph_id']or anchors[-1]['start']!=scope['event_date_anchor']['start']:return False
        e,=event['evidence'];p=by[e['paragraph_id']];start=ids.index(anchors[-1]['paragraph_id']);end=ids.index(p['id'])
        if (end<=start or b['tail_paragraph_ids']!=ids[start:end+1]
                or b['tail_full_paragraphs']!=[{'paragraph_id':x['id'],'quote':x['text'],'source_position':x['source_position']}for x in ps[start:end+1]]
                or e['quote']!=p['text']or any(e[k]!=ch['id'if k=='chapter_id'else k]for k in ['chapter_id','source_id','work_id','book_id'])):return False
        noteids=[x['id']for x in ps[start:end+1]if x.get('text_layer')=='witness_appended_pei_songzhi_note']
        if b['embedded_source_paragraph_ids']!=noteids:return False
        for x in ps[start+1:end+1]:
            if x['id']not in noteids and re.search(r'(元|[一二三四五六七八九十]+)年',x['text']):return False
        ga=b['execution_group_anchor'];plan=b['reported_plan_anchor']
        if not exact(ga)or ga['paragraph_id']!=p['id']or ga['surface']!=event['source_term']or not ga['surface'].startswith('於是収')or not ga['surface'].endswith('等皆伏誅夷三族'):return False
        if not exact(plan)or plan['paragraph_id']!=p['id']or plan['surface']!='湏三月中欲發'or plan['end']>=ga['start']:return False
        mids=b['execution_member_mention_ids'];ms={m['id']:m for m in p['mentions']};members=[ms[mid]for mid in mids]
        if len(members)!=10 or len(set(mids))!=10 or len({m['person_id']for m in members})!=10:return False
        cursor=ga['start']+3
        for m in members:
            if m['kind']!='person'or m['start']!=cursor or p['text'][m['start']:m['end']]!=m['surface']:return False
            cursor=m['end']
        if p['text'][cursor:ga['end']]!='等皆伏誅夷三族':return False
        mid=b['event_person_mention_id']
        return(mid==e['person_mention_id']and mid in mids and ms[mid]['person_id']==event['person_id'])
    except(KeyError,TypeError,ValueError,IndexError,StopIteration):return False
