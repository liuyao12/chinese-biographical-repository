"""A marked biography topic survives only explicitly scoped sovereign replies.

This does not select a recipient by nearest mention or by an unmarked name.
Every intervening other person must be an isolated, non-mortal sovereign reply.
"""
import re


def exact(anchor, p):
    return (isinstance(anchor, dict) and set(anchor) == {'paragraph_id','start','end','surface'}
            and anchor['paragraph_id'] == p.get('id') and type(anchor['start']) is int
            and type(anchor['end']) is int and 0 <= anchor['start'] < anchor['end'] <= len(p['text'])
            and p['text'][anchor['start']:anchor['end']] == anchor['surface'])


def explicit_topic_gift_valid(h, paragraphs, mentions, events):
    b=h.get('posthumous_basis',{})
    if not isinstance(b,dict):return False
    keys={'source_term','kind','topic_person_mention_id','death_event_id','death_anchor','gift_anchor','topic_span','sovereign_replies','evidence'}
    if (set(b)!=keys or b.get('kind')!='explicit_topic_scoped_gift' or h.get('mode')!='posthumous_grant'
            or h.get('kind') not in ('office','honorific') or not b['evidence'] or b['evidence']!=h.get('evidence')
            or b['evidence']!=h.get('effective_period',{}).get('start',{}).get('evidence')):return False
    event=events.get(b['death_event_id']);topic=mentions.get(b['topic_person_mention_id'])
    if (not event or event.get('event_type')!='death' or event.get('person_id')!=h.get('person_id')
            or not topic or topic[2].get('person_id')!=h.get('person_id')):return False
    for e in b['evidence']:
        hit=paragraphs.get(e.get('paragraph_id'))
        if not hit:return False
        p=hit[1];text=p['text'];d=b['death_anchor'];g=b['gift_anchor'];scope=b['topic_span']
        if (topic[1]!=p['id'] or e.get('person_mention_id')!=topic[2]['id'] or e.get('quote')!=text
                or p.get('text_layer')!='received_chapter' or not all(exact(a,p)for a in [d,g,scope]) or b.get('source_term')!=scope['surface']
                or (scope['start']>0 and text[scope['start']-1]not in '。；')
                or d['surface']!=event.get('source_term') or not re.search('[卒薨死]',d['surface'])
                or not any(x.get('paragraph_id')==p['id'] and x.get('quote')==text for x in event.get('evidence',[]))
                or not scope['start']<=topic[2]['start']<topic[2]['end']<=d['start']<d['end']<=g['start']<g['end']<=scope['end']
                or text[scope['start']:topic[2]['start']] not in ('','其後','後','初','先是')
                or not re.fullmatch(r'贈[^，。；、]+(?:、[^，。；、]+)*(?:，加[^，。；、]+(?:、[^，。；、]+)*)*',g['surface'])
                or h['title'] not in re.split(r'、|，加',g['surface'][1:])):return False
        permitted=set();replies=b['sovereign_replies']
        if not isinstance(replies,list):return False
        for reply in replies:
            if not isinstance(reply,dict)or set(reply)!={'person_mention_id','clause_anchor'}:return False
            m=mentions.get(reply['person_mention_id']);a=reply['clause_anchor']
            if (not m or m[1]!=p['id'] or m[2].get('person_id')==h['person_id'] or m[2].get('surface')not in ('上','帝','天子')
                    or not exact(a,p) or a['start']!=m[2]['start'] or not topic[2]['end']<=a['start']<a['end']<=d['start']
                    or (a['start']>0 and text[a['start']-1]not in '，。；') or (a['end']<len(text)and text[a['end']]not in '，。；')
                    or not re.fullmatch(re.escape(m[2]['surface'])+r'(?:輒|乃|遂|特|又)?(?:優詔不許|不許|詔許之|許之)',a['surface'])):return False
            permitted.add(m[2]['id'])
        if len(permitted)!=len(replies):return False
        if any(m.get('kind')=='person' and m.get('person_id')!=h['person_id'] and m['id']not in permitted
               and scope['start']<=m['start']<scope['end']for m in p.get('mentions',[])):return False
        if not any(a.get('paragraph_id')==p['id'] and a.get('person_mention_id')==topic[2]['id']
                   and a.get('surface')==h['title'] and g['start']<a.get('start',-1)<a.get('end',len(text)+1)<=g['end']
                   and text[a['start']:a['end']]==h['title']for a in h.get('attestations',[])):return False
    return True


def explicit_recipient_joint_resistance_gift_valid(h, paragraphs, mentions, events):
    """Finite consolation → joint resistance → opponent pacified → career/death/gift.

    Full-paragraph evidence is mandatory. The exact scoped grammar, not an alias
    or nearest-person rule, carries the named recipient across two other roles.
    This checks a received editorial reading; it does not prove that history.
    """
    import hashlib
    def same(a, b):
        if type(a) is not type(b): return False
        if type(a) is dict: return a.keys() == b.keys() and all(same(a[k], b[k]) for k in a)
        if type(a) is list: return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
        return a == b
    try:
        if not all(type(x) is dict for x in (h, paragraphs, mentions, events)): return False
        b = h['posthumous_basis']
        keys = {'kind','source_term','paragraph_sha256','recipient_person_mention_id',
                'ally_person_mention_id','opponent_person_mention_ids','scope_anchor',
                'recipient_clause_anchor','command_anchor','opponent_resolution_anchor',
                'career_anchor','death_event_id','death_anchor','age_anchor','gift_anchor','evidence'}
        start = h['effective_period']['start']
        if (type(b) is not dict or set(b) != keys or b['kind'] != 'explicit_recipient_joint_resistance_gift'
                or type(h.get('attestations')) is not list or h['mode'] != 'posthumous_grant' or h['kind'] != 'office' or h['status'] != 'source_attested'
                or type(b['evidence']) is not list or len(b['evidence']) != 1
                or not same(b['evidence'], h['evidence']) or not same(b['evidence'], start['evidence'])
                or start['status'] != 'source_event' or start['event_type'] != 'posthumous_grant'):
            return False
        e = b['evidence'][0]; cid, p = paragraphs[e['paragraph_id']]; text = p['text']
        if (type(text) is not str or p.get('text_layer') != 'received_chapter' or e['chapter_id'] != cid
                or type(e.get('source_id')) is not str or not e['source_id']
                or e.get('quote') != text or b['source_term'] != text
                or b['paragraph_sha256'] != hashlib.sha256(text.encode()).hexdigest()):
            return False
        physical = {m['id']: m for m in p['mentions']}
        if len(physical) != len(p['mentions']): return False
        def role(mid):
            hit = mentions.get(mid); m = physical.get(mid)
            if (not hit or not m or hit[0] != cid or hit[1] != p['id'] or not same(hit[2], m)
                    or m.get('kind') != 'person' or type(m.get('person_id')) is not str
                    or type(m.get('start')) is not int or type(m.get('end')) is not int
                    or not 0 <= m['start'] < m['end'] <= len(text)
                    or text[m['start']:m['end']] != m.get('surface')):
                return None
            return m
        opponent_ids = b['opponent_person_mention_ids']
        if type(opponent_ids) is not list or len(opponent_ids) != 2: return False
        ids = [b['recipient_person_mention_id'], b['ally_person_mention_id']] + opponent_ids
        if len(set(ids)) != 4: return False
        recipient, ally, opponent, resumed = [role(mid) for mid in ids]
        if not all((recipient, ally, opponent, resumed)): return False
        if (recipient['person_id'] != h['person_id'] or e.get('person_mention_id') != recipient['id']
                or opponent['person_id'] != resumed['person_id']
                or len({recipient['person_id'], ally['person_id'], opponent['person_id']}) != 3):
            return False
        scope, rc, command, aftermath, career, death, gift = [b[k] for k in (
            'scope_anchor','recipient_clause_anchor','command_anchor','opponent_resolution_anchor',
            'career_anchor','death_anchor','gift_anchor')]
        age = b['age_anchor']
        if not all(exact(a, p) for a in [scope, rc, command, aftermath, career, death, gift]): return False
        if age is not None and not exact(age, p): return False
        if (scope['start'] != rc['start'] or scope['end'] != gift['end']
                or scope['start'] > 0 and text[scope['start']-1] not in '。；'
                or any(q in scope['surface'] for q in '「」『』')
                or any(text[:scope['start']].count(a) != text[:scope['start']].count(z)
                       for a, z in [('「','」'),('『','』')])):
            return False
        if (rc['surface'] != '因厚撫慰' + recipient['surface']
                or recipient['end'] != rc['end'] or recipient['start'] != rc['start'] + len('因厚撫慰')):
            return False
        prefixes = ('令與', '命其與')
        prefix = next((x for x in prefixes if command['surface'] == x + ally['surface'] + '等共拒' + opponent['surface']), None)
        if (prefix is None or ally['start'] != command['start'] + len(prefix)
                or opponent['end'] != command['end']
                or opponent['start'] != ally['end'] + len('等共拒')
                or aftermath['surface'] != resumed['surface'] + '平'
                or resumed['start'] != aftermath['start'] or resumed['end'] + 1 != aftermath['end']):
            return False
        # A finite enumeration of office-shaped terms, never an arbitrary career paragraph.
        if not career['surface'].startswith('遷'): return False
        terms = career['surface'][1:].split('、')
        if (not terms or len(terms) > 8 or any(not t or re.search('[以為與其曰卒薨死贈嗣殺，。；：「」『』]', t)
                or not (t == '使持節' or re.fullmatch(r'[\u3400-\u9fff]{1,20}(?:將軍|常侍|諸軍事|刺史|太守|內史)', t))
                for t in terms)):
            return False
        event = events.get(b['death_event_id'])
        if (type(event) is not dict or event.get('event_type') != 'death' or event.get('status') != 'source_attested'
                or event.get('person_id') != h['person_id']
                or not any(same(x, e) for x in event.get('evidence', []))
                or type(event.get('date_expression')) is not str or not event['date_expression']
                or type(event.get('source_term')) is not str or not event['source_term']):
            return False
        death_term = event['source_term']
        expected_death = death_term if death_term.startswith(event['date_expression']) else event['date_expression'] + death_term
        if (death['surface'] != expected_death or not death['surface'].endswith('卒')
                or age is not None and not re.fullmatch(r'時年[零〇一二三四五六七八九十百廿卅兩]+(?:歲)?', age['surface'])
                or gift['surface'] != '贈' + h['title']):
            return False
        chain = [(rc, '，', command), (command, '。', aftermath), (aftermath, '，', career),
                 (career, '。', death)]
        chain += [(death, '，', age), (age, '。', gift)] if age is not None else [(death, '。', gift)]
        if any(left['end'] + len(mark) != right['start'] or text[left['end']:right['start']] != mark
               for left, mark, right in chain):
            return False
        if gift['end'] < len(text) and text[gift['end']] not in '，。；': return False
        covered = {m['id'] for m in p['mentions'] if scope['start'] <= m['start'] < scope['end']
                   and m.get('kind') in ('person','pronoun','unresolved')}
        if covered != set(ids): return False
        return any(type(a) is dict and a.get('paragraph_id') == p['id'] and a.get('person_mention_id') == recipient['id']
                   and a.get('surface') == h['title'] and a.get('usage') == 'posthumous_usage'
                   and type(a.get('start')) is int and type(a.get('end')) is int
                   and a['start'] == gift['start'] + 1 and a['end'] == gift['end']
                   and text[a['start']:a['end']] == h['title'] for a in h.get('attestations', []))
    except (KeyError, TypeError, ValueError, IndexError):
        return False
