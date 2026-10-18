"""核對完整連續傳文中的子嗣承接；不以遠段或補字代替證據。"""

def child_continuation_errors(assertion, chapter):
    errors = []
    context = assertion.get('context', {})
    ids = context.get('paragraph_ids')
    paras = chapter.get('paragraphs', [])
    order = [p['id'] for p in paras]
    byid = {p['id']: p for p in paras}
    evidence = assertion.get('evidence', [])
    valid = (context.get('kind') == 'biographical_child_continuation'
             and assertion.get('predicate') == 'father'
             and isinstance(ids, list) and len(ids) >= 2
             and all(isinstance(i, str) and i in order for i in ids)
             and len(set(ids)) == len(ids)
             and bool(context.get('rationale'))
             and context.get('status') == 'contextual_provisional'
             and context.get('human_reviewed') is False
             and ids == [e.get('paragraph_id') for e in evidence])
    if valid:
        valid = ids == order[order.index(ids[0]):order.index(ids[-1]) + 1]
    if valid:
        for pid, e in zip(ids, evidence):
            p = byid[pid]
            position = p.get('source_position', {})
            valid &= (e.get('chapter_id') == chapter.get('id')
                      and e.get('source_id') == chapter.get('source_id')
                      and e.get('quote') == p.get('text')
                      and p.get('text_layer') == 'received_chapter'
                      and position.get('editorial_excerpt_boundary') is True
                      and type(position.get('first_line')) is int
                      and type(position.get('last_line')) is int
                      and position['first_line'] <= position['last_line']
                      and position.get('revision_id') == chapter.get('source', {}).get('revision_id'))
        if valid:
            for a, b in zip(ids, ids[1:]):
                pa, pb = byid[a]['source_position'], byid[b]['source_position']
                valid &= pa['last_line'] + 1 == pb['first_line']
    if not valid:
        return ['傳主子嗣承接須保留同一固定見證的完整連續原段、原行與判讀']
    anchor = next((m for m in byid[ids[0]].get('mentions', [])
                   if m.get('id') == context.get('parent_mention_id')), None)
    child = next((m for m in byid[ids[-1]].get('mentions', [])
                  if m.get('id') == context.get('child_mention_id')), None)
    if (not anchor or anchor.get('kind') != 'person'
            or anchor.get('person_id') != assertion.get('object_person_id')
            or not child or child.get('kind') != 'person'
            or child.get('person_id') != assertion.get('subject_person_id')
            or child.get('start') != 1 or not byid[ids[-1]]['text'].startswith('子')
            or assertion.get('qualifiers', {}).get('source_term') != '子'
            or assertion.get('qualifiers', {}).get('lineage') != 'paternal'):
        errors.append('傳主子嗣承接的父名錨點或段首子某錨點不符')
    return errors
