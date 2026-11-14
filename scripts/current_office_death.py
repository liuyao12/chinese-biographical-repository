"""A local 卒官 can end its immediately preceding named office, never every title."""

def current_office_death_valid(holding, paragraphs, mentions):
    basis = holding.get('end_basis', {})
    end = holding.get('effective_period', {}).get('end', {})
    title, date = holding.get('title'), end.get('date_expression')
    if (set(basis) != {'kind', 'source_term', 'evidence'}
            or basis.get('kind') != 'died_in_last_named_office'
            or holding.get('kind') != 'office'
            or not isinstance(title, str) or not title
            or not (date is None or isinstance(date, str) and bool(date))
            or basis.get('source_term') != title + '。' + (date + '，' if date else '') + '卒官'
            or end.get('status') != 'source_event' or end.get('event_type') != 'explicit_end'
            or not basis.get('evidence') or basis['evidence'] != end.get('evidence')
            or basis['evidence'] != holding.get('evidence')):
        return False
    for evidence in basis['evidence']:
        hit = paragraphs.get(evidence.get('paragraph_id'))
        quote = evidence.get('quote')
        if (not hit or not isinstance(quote, str) or not quote or quote not in hit[1]['text']
                or basis['source_term'] not in quote):
            return False
        context = evidence.get('context')
        mid = context.get('person_mention_id') if isinstance(context, dict) else evidence.get('person_mention_id')
        anchor = mentions.get(mid)
        if not anchor or anchor[2].get('person_id') != holding.get('person_id'):
            return False
        if context is None and anchor[1] != evidence.get('paragraph_id'):
            return False
        # Each occurrence still points to this title's actual source coordinates.
        if not any(a.get('paragraph_id') == evidence.get('paragraph_id')
                   and a.get('surface') == title and a.get('person_mention_id') == mid
                   and hit[1]['text'].startswith(basis['source_term'], a.get('start', -1))
                   for a in holding.get('attestations', [])):
            return False
    return True
