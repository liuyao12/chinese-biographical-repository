"""Validate source-attested succession terms without inventing title words."""


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
                if parents and any(m.get('person_id') == assertion['subject_person_id']
                                   and term_start <= m['start'] < m['end'] <= term_start + len(term)
                                   for m in paragraph['mentions']):
                    return True
    return False
