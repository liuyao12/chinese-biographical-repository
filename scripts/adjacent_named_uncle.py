"""Validate both named endpoints in a literal X叔父Y source clause."""
def valid(assertion, paragraphs):
    if assertion.get('predicate') != 'paternal_uncle' or not assertion.get('evidence'):
        return False
    q = assertion.get('qualifiers', {})
    binding = q.get('source_clause_binding', {})
    for ev in assertion['evidence']:
        hit = paragraphs.get(ev.get('paragraph_id'))
        if not hit:
            return False
        _, p = hit
        names = {m['id']: m for m in p.get('mentions', []) if m.get('kind') == 'person'}
        rows = []
        for side in ('subject', 'object'):
            key = side + '_person_mention_id'
            m = names.get(ev.get(key))
            if not m or binding.get(key) != m['id'] or m['person_id'] != assertion[side + '_person_id']:
                return False
            if p['text'][m['start']:m['end']] != m['surface']:
                return False
            rows.append(m)
        child, uncle = rows
        if (child['person_id'] == uncle['person_id'] or p['text'][child['end']:uncle['start']] != '叔父'
                or p['text'][child['start']:uncle['end']] != q.get('source_term')
                or q['source_term'] not in ev.get('quote','')):
            return False
    return True
