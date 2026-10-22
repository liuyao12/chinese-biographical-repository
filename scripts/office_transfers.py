"""Explicit office transfers retain their own source phrase, separate from royal enfeoffment."""

def office_transfer_valid(holding, paragraphs, mentions):
    b = holding.get('office_transfer_basis')
    start = holding.get('effective_period', {}).get('start', {})
    if (holding.get('kind') != 'office' or holding.get('mode') != 'transfer'
            or not isinstance(b, dict) or set(b) != {'kind', 'verb', 'titles', 'source_term', 'evidence'}
            or b.get('kind') != 'explicit_office_transfer'
            or b.get('verb') not in ('轉', '轉拜', '轉為', '轉授', '遷', '徙', '復轉')
            or not isinstance(b.get('titles'), list) or not b['titles']
            or not all(isinstance(t, str) and t for t in b['titles'])
            or holding.get('title') not in b['titles']
            or b.get('source_term') != b['verb'] + '、'.join(b['titles'])
            or not b.get('evidence') or b['evidence'] != holding.get('evidence')
            or start.get('status') != 'source_event' or start.get('event_type') != 'transfer'
            or start.get('evidence') != b['evidence']):
        return False
    for e in b['evidence']:
        hit = paragraphs.get(e.get('paragraph_id'))
        if not hit or e.get('quote') != hit[1].get('text') or b['source_term'] not in e['quote']:
            return False
        context = e.get('context')
        mid = context.get('person_mention_id') if isinstance(context, dict) else e.get('person_mention_id')
        actor = mentions.get(mid)
        if not actor or actor[2].get('person_id') != holding.get('person_id'):
            return False
        lo = e['quote'].index(b['source_term'])
        hi = lo + len(b['source_term'])
        if not any(a.get('paragraph_id') == e['paragraph_id'] and a.get('surface') == holding['title']
                   and a.get('person_mention_id') == mid and lo <= a.get('start', -1)
                   and a.get('end', hi + 1) <= hi
                   and e['quote'][a['start']:a['end']] == holding['title']
                   for a in holding.get('attestations', [])):
            return False
    return True
