"""Validate source-attested succession terms without inventing title words."""


def adjacent_parent_quoted(assertion, paragraphs, current_id):
    """只接受已明列的同篇相鄰段與引句，不從段號或最近人名推父親。"""
    context = assertion.get('context', {})
    if not isinstance(context, dict):
        return False
    ids = context.get('paragraph_ids', [])
    if (context.get('kind') != 'adjacent_paragraphs' or not isinstance(ids, list)
            or len(ids) != 2 or not all(isinstance(pid, str) for pid in ids)
            or ids[1] != current_id or any(pid not in paragraphs for pid in ids)):
        return False
    previous, current = (paragraphs[pid] for pid in ids)
    if previous[0] != current[0]:
        return False
    order = [pid for pid, hit in paragraphs.items() if hit[0] == current[0]]
    if order.index(ids[1]) != order.index(ids[0]) + 1:
        return False
    paragraph = previous[1]
    for evidence in assertion.get('evidence', []):
        quote = evidence.get('quote')
        if evidence.get('paragraph_id') != ids[0] or not isinstance(quote, str) or not quote:
            continue
        for start in range(len(paragraph['text'])):
            if paragraph['text'].startswith(quote, start) and any(
                    m.get('person_id') == assertion['object_person_id']
                    and start <= m['start'] < m['end'] <= start + len(quote)
                    for m in paragraph['mentions']):
                return True
    return False


def succession_valid(assertion, holdings, paragraphs):
    succession = assertion.get('qualifiers', {}).get('succession')
    required = {'source_term', 'predecessor_person_id', 'predecessor_holding_id',
                'status', 'rationale', 'human_reviewed'}
    if not isinstance(succession, dict) or set(succession) != required:
        return False
    holding = holdings.get(succession['predecessor_holding_id'])
    term = succession['source_term']
    if not (assertion.get('predicate') == 'father' and holding
            and succession['predecessor_person_id'] == assertion.get('object_person_id')
            and holding.get('person_id') == succession['predecessor_person_id']
            and holding.get('kind') in ('noble_rank', 'royal_rank')
            and holding.get('mode') in ('grant', 'accession', 'attestation', 'self_proclamation')
            and succession['status'] == 'contextual_provisional'
            and succession['human_reviewed'] is False
            and isinstance(succession['rationale'], str) and succession['rationale']
            and isinstance(term, str) and '嗣' in term):
        return False
    for evidence in assertion.get('evidence', []):
        hit = paragraphs.get(evidence.get('paragraph_id'))
        quote = evidence.get('quote', '')
        if not hit or not quote or quote not in hit[1]['text'] or term not in quote:
            continue
        paragraph = hit[1]
        prior_parent = adjacent_parent_quoted(assertion, paragraphs, evidence['paragraph_id'])
        for quote_start in range(len(paragraph['text'])):
            if not paragraph['text'].startswith(quote, quote_start):
                continue
            parents = [m for m in paragraph['mentions']
                       if m.get('person_id') == assertion['object_person_id']
                       and quote_start <= m['start'] < m['end'] <= quote_start + len(quote)]
            for term_start in range(quote_start, quote_start + len(quote)):
                if (term_start + len(term) > quote_start + len(quote)
                        or not paragraph['text'].startswith(term, term_start)):
                    continue
                if (parents or prior_parent) and any(m.get('person_id') == assertion['subject_person_id']
                                   and term_start <= m['start'] < m['end'] <= term_start + len(term)
                                   for m in paragraph['mentions']):
                    return True
    return False
