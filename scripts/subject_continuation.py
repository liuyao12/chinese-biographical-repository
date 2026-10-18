"""Validate a nearby omitted subject without manufacturing a textual name."""

def prior_subject_valid(context, evidence, person_id, chapter):
    if not isinstance(context, dict) or set(context) != {'kind', 'paragraph_id', 'person_mention_id', 'quote', 'intervening_paragraph_ids'}:
        return False
    order = [p['id'] for p in chapter.get('paragraphs', [])]
    before, target = context.get('paragraph_id'), evidence.get('paragraph_id')
    ids = context.get('intervening_paragraph_ids')
    if (context.get('kind') != 'prior_paragraph_subject' or before not in order or target not in order
            or not isinstance(ids, list) or len(ids) > 1
            or order.index(target) - order.index(before) != len(ids) + 1
            or ids != order[order.index(before) + 1:order.index(target)]
            or evidence.get('chapter_id') != chapter.get('id') or evidence.get('source_id') != chapter.get('source_id')):
        return False
    paras = chapter['paragraphs'][order.index(before):order.index(target) + 1]
    positions = [p.get('source_position', {}) for p in paras]
    if (all(p.get('editorial_excerpt_boundary') is True for p in positions)
            and any(type(p.get('first_line')) is not int or type(p.get('last_line')) is not int
                    or p['first_line'] > p['last_line'] for p in positions)):
        return False
    if all(p.get('editorial_excerpt_boundary') is True for p in positions):
        if any(b['first_line'] != a['last_line'] + 1 for a, b in zip(positions, positions[1:])):
            return False
    p = paras[0]
    m = next((m for m in p.get('mentions', []) if m.get('id') == context.get('person_mention_id')), None)
    quote = context.get('quote')
    return (bool(m) and m.get('kind') == 'person' and m.get('person_id') == person_id
            and isinstance(quote, str) and bool(quote)
            and any(i <= m['start'] < m['end'] <= i + len(quote)
                    for i in range(len(p['text'])) if p['text'].startswith(quote, i)))


def title_attestation_subject_valid(attestation, holding, chapter):
    """Keep a title's actual location and its preceding named subject separate."""
    context = attestation.get('context')
    if (not isinstance(context, dict)
            or set(context) != {'kind', 'paragraph_id', 'person_mention_id', 'quote'}
            or context.get('kind') != 'previous_paragraph_subject'
            or attestation.get('person_mention_id') != context.get('person_mention_id')):
        return False
    for evidence in holding.get('evidence', []):
        if (evidence.get('paragraph_id') != attestation.get('paragraph_id')
                or evidence.get('context') != context):
            continue
        carried = dict(context, kind='prior_paragraph_subject', intervening_paragraph_ids=[])
        if prior_subject_valid(carried, evidence, holding.get('person_id'), chapter):
            return True
    return False
