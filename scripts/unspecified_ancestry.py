"""Keep an unadopted 之後 claim without inventing its generation count."""

def unspecified_ancestry_valid(assertion, paragraphs):
    q = assertion.get('qualifiers', {})
    term = q.get('source_term')
    if (assertion.get('predicate') != 'ancestor'
            or q.get('adopted_for_family_tree') is not False
            or q.get('ancestry_precision') != 'unspecified_descent'
            or any(key not in q or q[key] is not None for key in
                   ['generation_distance', 'source_number', 'reported_generation_number'])
            or not isinstance(term, str) or not term.endswith('之後') or len(term) <= 2
            or not assertion.get('evidence')):
        return False
    for e in assertion['evidence']:
        hit = paragraphs.get(e.get('paragraph_id'))
        quote = e.get('quote')
        if not hit or not isinstance(quote, str) or not quote or quote not in hit[1]['text'] or term not in quote:
            return False
        text = hit[1]['text']
        if not any(m.get('kind') == 'person' and m.get('person_id') == assertion.get('object_person_id')
                   and m.get('surface') == term[:-2]
                   and text.startswith(term, m.get('start', -1)) for m in hit[1].get('mentions', [])):
            return False
    return True
