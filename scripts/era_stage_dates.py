# coding: utf-8
"""An era-stage word supplies an era, never a numeric regnal year.

Restricted to explicitly bounded, fixed-witness biography timelines. Embedded
speech needs its exact 曰 introducer and return-to-narration year boundary.
"""
import re


def staged(date):
    return (isinstance(date, dict) and date.get('relative_year_reference', {}).get('kind')
            == 'omitted_era_regnal_year_after_era_stage')


def binding_valid(date, record, role):
    if not staged(date):
        return True
    try:
        b = date['narrative_era_scope']['event_binding']
        if not record or b['person_id'] != record['person_id'] or b['record_id'] != record['id']:
            return False
        if role == 'life_event':
            return (b['event_type'] == record['event_type'] == 'death'
                    and b['source_term_anchor']['surface'] == record['source_term']
                    and date['source_expression'] == record['date_expression'])
        return (role == 'start' and record['mode'] == 'grant' and b['event_type'] == 'title_grant'
                and b['title_anchor']['surface'] == record['title']
                and date['source_expression'] == record['effective_period']['start']['date_expression']
                and any(all(a.get(k) == b['title_anchor'][k] for k in ('paragraph_id','start','end','surface'))
                        for a in record['attestations']))
    except (KeyError, TypeError):
        return False


def staged_scope_valid(date, chapters):
    try:
        from scripts.relative_biography_scope import valid
    except ImportError:
        from relative_biography_scope import valid
    if date.get('narrative_era_scope', {}).get('kind') == 'same_fixed_paragraph_era_stage':
        return local_scope_valid(date, chapters)
    if not valid(date, chapters):
        return False
    try:
        s = date['narrative_era_scope']; m = date['regnal_year_mapping']; r = date['relative_year_reference']
        ch = chapters[s['chapter_id']]; ps = {p['id']:p for p in ch['paragraphs']}
        a, d = s['era_anchor'], s['event_date_anchor']; event = s['event_binding']
        # Existing full fixed-witness scope handles ordered paragraphs, revision,
        # exact quotations and ruler identity. New stages cannot use relative offsets.
        if (r['era_expression'] not in (m['era_name']+'初', m['era_name']+'中', m['era_name']+'末')
                or a['surface'] != r['era_expression'] or m['year_offset'] != 0
                or event['person_id'] != s['unit_subject_person_id'] or event['human_reviewed'] is not False):
            return False
        def anchored(x):
            p=ps[x['paragraph_id']];return (set(x)=={'paragraph_id','start','end','surface'}
                and type(x['start'])is int and type(x['end'])is int and 0<=x['start']<x['end']<=len(p['text'])
                and p['text'][x['start']:x['end']]==x['surface'])
        trigger = event['source_term_anchor']; subject = ps[event['subject_paragraph_id']]
        sm = next(x for x in subject['mentions'] if x['id'] == event['subject_mention_id'])
        if (not anchored(trigger) or trigger['paragraph_id'] != d['paragraph_id']
                or event['subject_paragraph_id'] != d['paragraph_id'] or sm.get('kind') != 'person'
                or sm.get('person_id') != event['person_id'] or sm['end'] > d['start']
                or trigger['start'] < d['end']):
            return False
        if event['event_type'] == 'death':
            if trigger['surface'] not in ('卒','薨','死'):
                return False
        elif event['event_type'] == 'title_grant':
            t = event['title_anchor']
            if (trigger['surface'] not in ('為','遷為') or not anchored(t)
                    or t['paragraph_id'] != d['paragraph_id'] or t['start'] < trigger['end']):
                return False
        else:
            return False
        quotes = s['embedded_quotation_scopes']; intro = s['quotation_introducers']
        if len(quotes) != len(intro):
            return False
        for q, i in zip(quotes, intro):
            if (not anchored(i) or not i['surface'].endswith('曰') or i['paragraph_id'] != q['paragraph_id']
                    or i['end'] != q['start']):
                return False
            p=ps[q['paragraph_id']]
            # An explicitly anchored narration year marks the return from speech.
            if not re.match('[元一二三四五六七八九十]+年', p['text'][q['end']:]):
                return False
        ids=s['paragraph_ids']; lo=ids.index(a['paragraph_id']); hi=ids.index(trigger['paragraph_id'])
        for j in range(lo,hi+1):
            p=ps[ids[j]]; left=a['start']if j==lo else 0; right=trigger['end']if j==hi else len(p['text'])
            def quoted(start,end):
                return any(q['paragraph_id']==p['id'] and q['start']<=start and end<=q['end']for q in quotes)
            # A switched named topic cannot be silenced by the biography heading.
            if any(x.get('kind')=='person'and x.get('person_id')!=event['person_id']
                    and left<=x['start']<right and not quoted(x['start'],x['end'])for x in p['mentions']):
                return False
            for found in re.finditer('('+'|'.join(map(re.escape,KNOWN_ERAS))+r')(?:初|中|末|[元一二三四五六七八九十]+年)',p['text'][left:right]):
                if found[1]!=m['era_name']and not quoted(left+found.start(),left+found.end()):
                    return False
            for found in re.finditer('[元一二三四五六七八九十]+年',p['text'][d['end']:trigger['end']]if p['id']==d['paragraph_id']else''):
                if not quoted(d['end']+found.start(),d['end']+found.end()):
                    return False
        if any(q['paragraph_id']==d['paragraph_id']and q['start']<=d['start']<q['end']for q in quotes):
            return False
        for event_anchor in [trigger] + ([event['title_anchor']] if event['event_type']=='title_grant' else []):
            if any(q['paragraph_id']==event_anchor['paragraph_id']and q['start']<=event_anchor['start']<q['end']for q in quotes):
                return False
        return True
    except (KeyError,ValueError,TypeError,IndexError,StopIteration):
        return False


# 固定教育部年號表page2 SHA193f33b9351675fe6b1e72cab84f5b88977a91c37717cf67e611262cad09ac65
KNOWN_ERAS = ['中大同', '中大通', '中興', '五鳳', '元嘉', '元康', '元徽', '元熙', '元興', '光大', '光熙', '升平', '咸和', '咸安', '咸寧', '咸康', '大同', '大寶', '大明', '大通', '天嘉', '天康', '天成', '天正', '天璽', '天監', '天紀', '天興', '天賜', '太元', '太和', '太安', '太寧', '太平', '太康', '太延', '太建', '太清', '太熙', '太興', '始光', '孝建', '寧康', '寶鼎', '延和', '延興', '建元', '建武', '建興', '建衡', '承聖', '昇明', '普通', '景和', '景平', '永元', '永光', '永初', '永和', '永嘉', '永安', '永定', '永寧', '永平', '永康', '永昌', '永明', '永泰', '永熙', '永興', '泰始', '泰常', '泰豫', '甘露', '登國', '皇始', '神瑞', '神鳳', '禎明', '紹泰', '義熙', '至德', '興寧', '隆和', '隆安', '隆昌', '鳳凰']


def local_scope_valid(date, chapters):
    """No ruler inferred: exact single paragraph and explicitly bound biography subject."""
    try:
        s=date['narrative_era_scope'];ch=chapters[s['chapter_id']]
        p=next(x for x in ch['paragraphs'] if x['id']==s['paragraph_id'])
        if (s['source_id']!=ch['source_id'] or s['revision_id']!=ch['source']['revision_id']
            or s['witness_sha256']!=ch['source']['wikitext_sha256']
            or s['full_paragraph']!=p['text'] or s['source_position']!=p['source_position']
            or s['human_reviewed'] is not False or any('ruler' in k for k in s)):
            return False
        def exact(a):
            return (set(a)=={'paragraph_id','start','end','surface'} and a['paragraph_id']==p['id']
                    and type(a['start'])is int and type(a['end'])is int
                    and 0<=a['start']<a['end']<=len(p['text']) and p['text'][a['start']:a['end']]==a['surface'])
        a,d=s['era_anchor'],s['event_date_anchor'];b=s['event_binding'];tr=b['source_term_anchor'];t=b['title_anchor']
        m=date['regnal_year_mapping'];r=date['relative_year_reference']
        sm=next(x for x in p['mentions'] if x['id']==s['unit_subject_mention_id'])
        if (sm.get('kind')!='person' or sm.get('person_id')!=s['unit_subject_person_id'] or sm['start']!=0
            or b['person_id']!=s['unit_subject_person_id'] or b['human_reviewed'] is not False
            or b['subject_mention_id']!=sm['id'] or b['subject_paragraph_id']!=p['id']
            or b['event_type']!='title_grant' or not all(exact(x) for x in (a,d,tr,t))
            or not sm['end']<=a['start']<a['end']<=d['start']<d['end']<=tr['start']<tr['end']<=t['start']
            or a['surface']!=r['era_expression'] or a['surface'] not in tuple(m['era_name']+x for x in ('初','中','末'))
            or d['surface']!=date['source_expression'] or tr['surface']!='除'
            or m['year_offset']!=0 or p['text'][d['end']:tr['start']] not in ('', '，', '來朝，')):return False
        # This narrow grammar allows narrative actions, but no switched subject, quotation or new era/date.
        between=p['text'][a['end']:tr['start']]
        if any(x.get('kind')=='person' and x.get('person_id')!=b['person_id'] and a['end']<=x['start']<tr['end'] for x in p['mentions']):return False
        if any(x in between for x in ('曰','云','言','初，','先是')):return False
        if any(e in between for e in KNOWN_ERAS):return False
        dates=list(re.finditer('[元一二三四五六七八九十]+年',between))
        if len(dates)!=1 or a['end']+dates[0].start()!=d['start'] or a['end']+dates[0].end()!=d['end']:return False
        return date['evidence'][-1]['paragraph_id']==p['id'] and date['evidence'][-1]['quote']==p['text']
    except (KeyError,TypeError,ValueError,StopIteration,IndexError):return False
