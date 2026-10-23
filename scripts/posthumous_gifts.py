"""來源先敘死亡、後明贈官的逐字記錄，不補出原文沒有的追字。"""


def posthumous_gift_valid(holding, paragraphs, mentions, life_events=None):
    if isinstance(holding.get('posthumous_basis'), dict) and holding['posthumous_basis'].get('kind') == 'biography_sovereign_mourning_gift_to_resumed_topic':
        try:
            from scripts.lifecycle_offered_biography import gift_valid
        except ImportError:
            from lifecycle_offered_biography import gift_valid
        return gift_valid(holding, paragraphs, mentions, life_events or {})

    if isinstance(holding.get('posthumous_basis'), dict) and holding['posthumous_basis'].get('kind') == 'resumed_biography_death_gift':
        try:
            from scripts.resumed_biography_lifecycle import gift_valid
        except ImportError:
            from resumed_biography_lifecycle import gift_valid
        return gift_valid(holding, paragraphs, mentions, life_events or {})
    if isinstance(holding.get('posthumous_basis'), dict) and holding['posthumous_basis'].get('kind') in ('heading_title_confirmed_by_posthumous_notice', 'coordinated_recollected_posthumous_gift'):
        try:
            from scripts.song041_title_semantics import heading_posthumous_valid, recalled_gift_valid
        except ImportError:
            from song041_title_semantics import heading_posthumous_valid, recalled_gift_valid
        return heading_posthumous_valid(holding, paragraphs, life_events or {}) if holding['posthumous_basis']['kind'] == 'heading_title_confirmed_by_posthumous_notice' else recalled_gift_valid(holding, paragraphs)
    if isinstance(holding.get('posthumous_basis'), dict) and holding['posthumous_basis'].get('kind') in ('imperial_named_serial_gift', 'imperial_decree_topic_death_gift'):
        try:
            from scripts.song047_title_semantics import imperial_gift_valid
        except ImportError:
            from song047_title_semantics import imperial_gift_valid
        return imperial_gift_valid(holding, paragraphs, mentions, life_events or {})
    if isinstance(holding.get('posthumous_basis'), dict) and holding['posthumous_basis'].get('kind') == 'bound_death_serial_gift':
        try:
            from scripts.bound_serial_posthumous import valid
        except ImportError:
            from bound_serial_posthumous import valid
        return valid(holding, paragraphs, mentions, life_events or {})
    if (isinstance(holding.get('posthumous_basis'), dict)
            and holding['posthumous_basis'].get('kind') == 'named_recipient_after_same_paragraph_death'):
        return named_recipient_prior_death_valid(holding, paragraphs, mentions, life_events or {})
    if (isinstance(holding.get('posthumous_basis'), dict)
            and holding['posthumous_basis'].get('kind') == 'biography_topic_death_then_gift'):
        return biography_topic_gift_valid(holding, paragraphs, mentions, life_events or {})
    if (isinstance(holding.get('posthumous_basis'), dict)
            and holding['posthumous_basis'].get('kind') == 'continued_subject_death_then_gift'):
        return continued_subject_gift_valid(holding, paragraphs, mentions, life_events or {})
    if isinstance(holding.get('posthumous_basis'), dict) and holding['posthumous_basis'].get('kind') == 'explicit_topic_scoped_gift':
        try:
            from scripts.explicit_topic_gifts import explicit_topic_gift_valid
        except ImportError:
            from explicit_topic_gifts import explicit_topic_gift_valid
        return explicit_topic_gift_valid(holding, paragraphs, mentions, life_events or {})
    if isinstance(holding.get('posthumous_basis'), dict) and holding['posthumous_basis'].get('kind') == 'coordinated_attendance_death_then_gift':
        return coordinated_attendance_gift_valid(holding, paragraphs, mentions, life_events or {})
    b = holding.get('posthumous_basis')
    if (not isinstance(b, dict) or set(b) != {'kind', 'source_term', 'death_term', 'grant_term', 'recipient_person_mention_id', 'evidence'}
            or b.get('kind') != 'death_then_explicit_gift' or holding.get('mode') != 'posthumous_grant'
            or holding.get('kind') not in ('office', 'honorific') or not b.get('evidence')
            or b['evidence'] != holding.get('evidence')
            or b['evidence'] != holding.get('effective_period', {}).get('start', {}).get('evidence')):
        return False
    death, grant = b.get('death_term'), b.get('grant_term')
    if (not isinstance(death, str) or not any(x in death for x in ['卒', '薨', '死'])
            or not isinstance(grant, str)
            or not re.fullmatch(r'贈[^，。；、]+(?:、[^，。；、]+)*(?:，加[^，。；、]+(?:、[^，。；、]+)*)*', grant)
            or holding.get('title') not in re.split(r'、|，加', grant[1:])):
        return False
    recipient = mentions.get(b.get('recipient_person_mention_id'))
    if not recipient or recipient[2].get('person_id') != holding.get('person_id'):
        return False
    for e in b['evidence']:
        hit = paragraphs.get(e.get('paragraph_id'))
        if (not hit or recipient[1] != e.get('paragraph_id') or e.get('person_mention_id') != recipient[2]['id']
                or hit[1].get('text_layer') != 'received_chapter' or e.get('quote') != hit[1]['text']
                or b.get('source_term') != e['quote']):
            return False
        text = e['quote']
        if text.count(death) != 1 or text.count(grant) != 1:
            return False
        d, g = text.index(death), text.index(grant)
        before = [m for m in hit[1].get('mentions', []) if m.get('kind') == 'person' and m['end'] <= d]
        if (recipient[2]['end'] > d or d + len(death) > g or not before
                or max(before, key=lambda m: m['end'])['person_id'] != holding['person_id']):
            return False
        if not any(a.get('paragraph_id') == e['paragraph_id'] and a.get('person_mention_id') == recipient[2]['id']
                   and a.get('surface') == holding['title'] and g < a.get('start', -1) < g + len(grant)
                   for a in holding.get('attestations', [])):
            return False
    return True


import re


def biography_topic_gift_valid(holding, paragraphs, mentions, life_events):
    """編者明定傳主、死亡事件與贈號句；不按最近出現的帝、妃自動換受贈人。"""
    b = holding.get('posthumous_basis', {})
    keys = {'kind', 'source_term', 'death_term', 'grant_term', 'recipient_person_mention_id',
            'topic_person_mention_id', 'death_event_id', 'grant_recipient_kind', 'evidence'}
    if (set(b) != keys or b.get('kind') != 'biography_topic_death_then_gift'
            or holding.get('mode') != 'posthumous_grant'
            or holding.get('kind') not in ('office', 'noble_rank')
            or not b.get('evidence') or b['evidence'] != holding.get('evidence')
            or b['evidence'] != holding.get('effective_period', {}).get('start', {}).get('evidence')):
        return False
    event = life_events.get(b.get('death_event_id'))
    recipient = mentions.get(b.get('recipient_person_mention_id'))
    topic = mentions.get(b.get('topic_person_mention_id'))
    if (not event or event.get('event_type') != 'death' or event.get('person_id') != holding.get('person_id')
            or not recipient or not topic or recipient[2].get('person_id') != holding.get('person_id')
            or topic[2].get('person_id') != holding.get('person_id')):
        return False
    death, grant, title = b.get('death_term'), b.get('grant_term'), holding.get('title')
    if (not isinstance(death, str) or not isinstance(grant, str) or not isinstance(title, str)
            or not event.get('source_term') or event['source_term'] not in death
            or not event.get('date_expression') or event['date_expression'] + event['source_term'] != death):
        return False
    for e in b['evidence']:
        hit = paragraphs.get(e.get('paragraph_id'))
        if (not hit or recipient[1] != e.get('paragraph_id') or topic[1] != e.get('paragraph_id')
                or e.get('person_mention_id') != recipient[2]['id']
                or hit[1].get('text_layer') != 'received_chapter'
                or e.get('quote') != hit[1]['text'] or b.get('source_term') != e['quote']
                or not any(x.get('paragraph_id') == e['paragraph_id'] and x.get('quote') == e['quote']
                           for x in event.get('evidence', []))):
            return False
        text = e['quote']
        if text.count(death) != 1 or text.count(grant) != 1:
            return False
        d, g = text.index(death), text.index(grant)
        persons = [m for m in hit[1].get('mentions', []) if m.get('kind') == 'person']
        if (not persons or min(persons, key=lambda m: m['start'])['id'] != topic[2]['id']
                or topic[2]['start'] != 0 or topic[2]['end'] > d or d + len(death) > g):
            return False
        form = b['grant_recipient_kind']
        if form == 'named_recipient':
            if (grant != '贈' + recipient[2]['surface'] + title
                    or recipient[2]['start'] != g + 1):
                return False
        elif form == 'deictic_recipient':
            before = [m for m in persons if m['end'] <= g]
            if (grant != '其贈' + title or not before or recipient[2]['end'] > g
                    or max(before, key=lambda m: m['end'])['id'] != recipient[2]['id']):
                return False
        elif form == 'topic_continuation':
            # Exact series 贈A，加B, not an arbitrary title found elsewhere in the paragraph.
            if not re.fullmatch(r'贈[^，。；]+(?:，加[^，。；]+)*', grant):
                return False
            titles = [grant[1:].split('，加')[0]] + grant[1:].split('，加')[1:]
            if title not in titles or recipient[2]['end'] > d:
                return False
        else:
            return False
        if not any(a.get('paragraph_id') == e['paragraph_id']
                   and a.get('person_mention_id') == recipient[2]['id']
                   and a.get('surface') == title and g < a.get('start', -1)
                   and a.get('end', len(text) + 1) <= g + len(grant)
                   and text[a['start']:a['end']] == title for a in holding.get('attestations', [])):
            return False
    return True


def continued_subject_gift_valid(holding, paragraphs, mentions, life_events):
    """省略受贈人時，逐項核對前段主語、同段死亡與明確為贈句。"""
    b = holding.get('posthumous_basis', {})
    if (set(b) != {'kind', 'source_term', 'death_term', 'grant_term', 'death_event_id', 'evidence'}
            or holding.get('mode') != 'posthumous_grant' or holding.get('kind') != 'office'
            or not b.get('evidence') or b['evidence'] != holding.get('evidence')
            or b['evidence'] != holding.get('effective_period', {}).get('start', {}).get('evidence')):
        return False
    event = life_events.get(b['death_event_id'])
    if (not event or event.get('event_type') != 'death' or event.get('status') != 'source_attested'
            or event.get('person_id') != holding.get('person_id')
            or not event.get('date_expression') or not event.get('source_term')
            or b.get('death_term') != event['date_expression'] + event['source_term']
            or b.get('grant_term') != '即以' + holding.get('title', '') + '為贈'):
        return False
    for e in b['evidence']:
        hit = paragraphs.get(e.get('paragraph_id'))
        ctx = e.get('context', {})
        prior = paragraphs.get(ctx.get('paragraph_id'))
        m = mentions.get(ctx.get('person_mention_id'))
        if (not hit or not prior or hit[0] != prior[0] or not m
                or m[1] != ctx.get('paragraph_id') or m[2].get('person_id') != holding.get('person_id')
                or e.get('person_mention_id') != m[2]['id']
                or ctx.get('kind') != 'previous_paragraph_subject'
                or ctx.get('quote') != prior[1].get('text')
                or e.get('quote') != hit[1].get('text') or b['source_term'] != e['quote']
                or hit[1].get('text_layer') != 'received_chapter'):
            return False
        ordered = [key for key, value in paragraphs.items() if value[0] == hit[0]]
        if ordered.index(e['paragraph_id']) == 0 or ordered[ordered.index(e['paragraph_id']) - 1] != ctx['paragraph_id']:
            return False
        if not any(x.get('paragraph_id') == e['paragraph_id'] and x.get('quote') == e['quote']
                   and x.get('context', {}).get('kind') == 'prior_paragraph_subject'
                   and all(x['context'].get(k) == ctx.get(k) for k in ('paragraph_id', 'person_mention_id', 'quote'))
                   and x['context'].get('intervening_paragraph_ids') == [] for x in event.get('evidence', [])):
            return False
        text = e['quote']; death = b['death_term']; grant = b['grant_term']
        if text.count(death) != 1 or text.count(grant) != 1 or text.index(death) + len(death) > text.index(grant):
            return False
        g = text.index(grant)
        if not any(a.get('paragraph_id') == e['paragraph_id'] and a.get('person_mention_id') == m[2]['id']
                   and a.get('context') == ctx and a.get('surface') == holding['title']
                   and a.get('start') == g + 2 and a.get('end') == g + 2 + len(holding['title'])
                   and text[a['start']:a['end']] == holding['title'] for a in holding.get('attestations', [])):
            return False
    return True



def coordinated_attendance_gift_valid(holding, paragraphs, mentions, life_events):
    """A bound coordinated action and actor-aftermath clause, not a free topic override."""
    try:
        from scripts.subject_continuation import coordinated_attendance_aftermath_subject_valid
    except ImportError:
        from subject_continuation import coordinated_attendance_aftermath_subject_valid
    b = holding.get('posthumous_basis', {})
    keys = {'kind','source_term','death_term','grant_term','recipient_person_mention_id','death_event_id',
            'death_anchor','grant_anchor','subject_context','source_revision','paragraph_sha256','evidence'}
    try:
        import hashlib
        if (set(b)!=keys or holding.get('mode')!='posthumous_grant' or holding.get('kind')!='office'
                or len(b['evidence'])!=1 or b['evidence']!=holding.get('evidence')
                or b['evidence']!=holding.get('effective_period',{}).get('start',{}).get('evidence')
                or holding.get('effective_period',{}).get('start',{}).get('status')!='source_event'
                or holding.get('effective_period',{}).get('start',{}).get('event_type')!='posthumous_grant'):
            return False
        e=b['evidence'][0];hit=paragraphs[e['paragraph_id']];p=hit[1];text=p['text'];event=life_events[b['death_event_id']]
        recipient=mentions[b['recipient_person_mention_id']]
        if (p.get('text_layer')!='received_chapter' or e['quote']!=text or b['source_term']!=text
                or b['paragraph_sha256']!=hashlib.sha256(text.encode()).hexdigest()
                or b['source_revision']!=p['source_position']['revision_id']
                or recipient[1]!=p['id'] or recipient[2].get('person_id')!=holding['person_id']
                or b['subject_context']['topic_mention_id']!=recipient[2]['id']
                or e.get('person_mention_id')!=recipient[2]['id']
                or not coordinated_attendance_aftermath_subject_valid(b['subject_context'],p,holding['person_id'])
                or event.get('person_id')!=holding['person_id'] or event.get('event_type')!='death'
                or event.get('status')!='source_attested' or e not in event.get('evidence',[])):
            return False
        def anchored(a):
            return (set(a)=={'paragraph_id','start','end','surface'}and a['paragraph_id']==p['id']
                and type(a['start'])is int and type(a['end'])is int and 0<=a['start']<a['end']<=len(text)
                and text[a['start']:a['end']]==a['surface'])
        d,g=b['death_anchor'],b['grant_anchor'];when=b['subject_context']['temporal_anchor']
        if (not anchored(d) or not anchored(g) or d['start']!=when['start']
                or d['surface']!=when['surface']+'卒' or b['death_term']!=d['surface']
                or event.get('source_term')!=d['surface'] or event.get('date_expression')!=when['surface']
                or g['surface']!='贈'+holding['title'] or b['grant_term']!=g['surface']
                or d['end']+1!=g['start'] or text[d['end']:g['start']]!='，'):
            return False
        return any(a.get('paragraph_id')==p['id']and a.get('person_mention_id')==recipient[2]['id']
                and a.get('surface')==holding['title']and a.get('start')==g['start']+1
                and a.get('end')==g['end']and a.get('usage')=='posthumous_usage'and text[a['start']:a['end']]==holding['title']
                for a in holding.get('attestations',[]))
    except (KeyError,TypeError,ValueError,IndexError):
        return False


def named_recipient_prior_death_valid(holding, paragraphs, mentions, life_events):
    """Bind 贈+named recipient+office to a same-person, earlier death; no topic guessing."""
    import hashlib
    try:
        from scripts.relative_regnal_year import relative_regnal_year_valid
        from scripts.validate_corpus import source_age_number
    except ImportError:
        from relative_regnal_year import relative_regnal_year_valid
        from validate_corpus import source_age_number
    b=holding.get('posthumous_basis',{})
    keys={'kind','source_term','death_event_id','death_anchor','relative_date_anchor','grant_anchor',
          'source_clause_anchor','recipient_person_mention_id','source_revision','paragraph_sha256','evidence'}
    try:
        start=holding['effective_period']['start'];date=start['normalized_date']
        if (set(b)!=keys or holding['kind']!='office' or holding['mode']!='posthumous_grant'
            or holding['status']!='source_attested' or len(b['evidence'])!=1
            or b['evidence']!=holding['evidence'] or b['evidence']!=start['evidence']
            or start['status']!='source_event' or start['event_type']!='posthumous_grant'
            or start['date_expression']!='明年' or date['source_expression']!='明年'):
            return False
        e=b['evidence'][0];cid,p=paragraphs[e['paragraph_id']];text=p['text']
        rec=mentions[b['recipient_person_mention_id']];event=life_events[b['death_event_id']]
        if (e['chapter_id']!=cid or rec[0]!=cid or rec[1]!=p['id'] or rec[2].get('kind')!='person'
            or rec[2].get('person_id')!=holding['person_id'] or e['person_mention_id']!=rec[2]['id']
            or rec[2]['surface'] in ('帝','公','王','其','之','子','父','母','君','陛下')
            or p.get('text_layer')!='received_chapter' or e['quote']!=text or b['source_term']!=text
            or b['source_revision']!=p['source_position']['revision_id']
            or b['paragraph_sha256']!=hashlib.sha256(text.encode()).hexdigest()
            or event['person_id']!=holding['person_id'] or event['event_type']!='death'
            or event['status']!='source_attested'
            or not any(x['paragraph_id']==p['id'] and x['quote']==text and x['chapter_id']==cid and x.get('source_id')==e.get('source_id') for x in event['evidence'])):
            return False
        def exact(a):
            return(set(a)=={'paragraph_id','start','end','surface'} and a['paragraph_id']==p['id']
                   and type(a['start'])is int and type(a['end'])is int and 0<=a['start']<a['end']<=len(text)
                   and text[a['start']:a['end']]==a['surface'])
        d,y,g,c=[b[k]for k in ['death_anchor','relative_date_anchor','grant_anchor','source_clause_anchor']]
        if (not all(exact(a)for a in (d,y,g,c)) or event['source_term']!=d['surface']
            or not d['surface'].endswith(('卒','薨','死')) or y['surface']!='明年'
            or not d['end']<=y['start']<y['end']<c['start']<=g['start']<g['end']
            or g['surface']!='贈'+rec[2]['surface']+holding['title']
            or c['surface'] not in (g['surface'],'其'+g['surface']) or c['end']!=g['end']
            or g['start']!=c['start']+len(c['surface'])-len(g['surface'])
            or rec[2]['start']!=g['start']+1 or rec[2]['end']!=g['start']+1+len(rec[2]['surface'])
            or (c['start']>0 and text[c['start']-1] not in '。，；：「')
            or any(mark in text[:d['end']] for mark in ('曰','「','」','『','』'))):return False
        # Date is independently validated by the existing native relative-year model.
        rr=date['relative_year_reference'];mapping=date['regnal_year_mapping'];death_date=event['normalized_date']
        if (date['evidence']!=b['evidence'] or date['original_quote']!=text
            or rr['source_term']!='明年' or rr['antecedent_expression']!=event['date_expression']
            or rr['era_expression']!=event['date_expression'] or date['year']!=death_date['year']+1
            or death_date['source_expression']!=event['date_expression']
            or not d['surface'].startswith(event['date_expression'])
            or text.find('明年',d['end'])!=y['start']
            or re.search(r'明年|其年|[元一二三四五六七八九十]+年',text[y['end']:g['start']])
            or not relative_regnal_year_valid(date,source_age_number)):
            return False
        return any(a.get('paragraph_id')==p['id'] and a.get('person_mention_id')==rec[2]['id']
                   and a.get('surface')==holding['title'] and a.get('start')==rec[2]['end']
                   and a.get('end')==g['end'] and a.get('usage')=='posthumous_usage'
                   and text[a['start']:a['end']]==holding['title'] for a in holding['attestations'])
    except (KeyError,TypeError,ValueError,IndexError):return False
