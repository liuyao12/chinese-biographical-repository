"""來源先敘死亡、後明贈官的逐字記錄，不補出原文沒有的追字。"""


def posthumous_gift_valid(holding, paragraphs, mentions, life_events=None):
    if (isinstance(holding.get('posthumous_basis'), dict)
            and holding['posthumous_basis'].get('kind') == 'biography_topic_death_then_gift'):
        return biography_topic_gift_valid(holding, paragraphs, mentions, life_events or {})
    if (isinstance(holding.get('posthumous_basis'), dict)
            and holding['posthumous_basis'].get('kind') == 'continued_subject_death_then_gift'):
        return continued_subject_gift_valid(holding, paragraphs, mentions, life_events or {})
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
