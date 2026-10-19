"""由具名父、叔父及叔父之父作可撤回組裝，不另造原文父子。"""


def _continued_child_list_parentage_valid(connection, nf, nu, uf, chapters):
    """Accept a complete received child list followed by that child's own biography.

    The assertions remain source evidence; only the parent's inferred placement
    uses this bridge. A section heading can cover a source-line gap but cannot
    supply any kinship. The original same-paragraph branch below is unchanged.
    """
    import re
    try:
        from .biographical_kinship import received_paragraphs_contiguous
    except ImportError:
        from biographical_kinship import received_paragraphs_contiguous
    context = nf.get('context', {})
    ids = context.get('paragraph_ids')
    evidence = nf.get('evidence', [])
    if (context.get('kind') != 'adjacent_paragraphs'
            or context.get('status') != 'contextual_provisional'
            or context.get('human_reviewed') is not False or not context.get('rationale')
            or nf.get('qualifiers', {}).get('context_kind') != 'biographical_child_continuation'
            or not isinstance(ids, list) or len(ids) != 2 or len(set(ids)) != 2
            or len(evidence) != 2 or ids != [e.get('paragraph_id') for e in evidence]
            or nf.get('qualifiers', {}).get('parent_paragraph_id') != ids[0]
            or len(nu.get('evidence', [])) != 1):
        return False
    first, last = evidence
    ue = nu['evidence'][0]
    cid = first.get('chapter_id')
    chapter = chapters.get(cid, {})
    if (not chapter or last.get('chapter_id') != cid or ue.get('chapter_id') != cid
            or first.get('source_id') != chapter.get('source_id')
            or last.get('source_id') != chapter.get('source_id')
            or ue.get('source_id') != chapter.get('source_id')):
        return False
    paras = chapter.get('paragraphs', [])
    order = [p.get('id') for p in paras]
    byid = {p.get('id'): p for p in paras}
    upid = ue.get('paragraph_id')
    if (any(pid not in byid for pid in ids + [upid])
            or order[order.index(ids[0]):order.index(upid) + 1] != ids + [upid]):
        return False
    selected = [byid[pid] for pid in ids + [upid]]
    for p, e in zip(selected, evidence + [ue]):
        pos = p.get('source_position', {})
        if (p.get('text_layer') != 'received_chapter' or e.get('quote') != p.get('text')
                or pos.get('editorial_excerpt_boundary') is not True
                or type(pos.get('first_line')) is not int
                or type(pos.get('last_line')) is not int
                or pos['first_line'] > pos['last_line']
                or pos.get('revision_id') != chapter.get('source', {}).get('revision_id')):
            return False
    if not all(received_paragraphs_contiguous(chapter, a, b)
               for a, b in zip(selected, selected[1:])):
        return False
    parent, listing, introduction = selected
    parent_anchor = next((m for m in parent.get('mentions', [])
                          if m.get('kind') == 'person' and m.get('start') == 0
                          and m.get('person_id') == nf.get('object_person_id')), None)
    if (not parent_anchor or parent_anchor.get('surface') != parent['text'][:parent_anchor.get('end', 0)]
            or not re.match(re.escape(parent_anchor['surface']) + '[，,]?字', parent['text'])):
        return False
    match = re.match(r'(?P<number>[一二三四五六七八九十])子[：:](?P<names>[^。]+)。', listing['text'])
    numbers = {char: i + 1 for i, char in enumerate('一二三四五六七八九十')}
    if (not match or nf.get('qualifiers', {}).get('source_term') != match['number'] + '子'):
        return False
    names = match['names'].split('、')
    if len(names) != numbers[match['number']] or any(not name for name in names):
        return False
    cursor = match.start('names')
    children = []
    for name in names:
        marker = next((m for m in listing.get('mentions', [])
                       if m.get('kind') == 'person' and m.get('start') == cursor
                       and m.get('end') == cursor + len(name) and m.get('surface') == name), None)
        if not marker or listing['text'][marker['start']:marker['end']] != name:
            return False
        children.append(marker)
        cursor += len(name) + 1
    if len({m.get('person_id') for m in children}) != len(children):
        return False
    child = next((m for m in children if m.get('person_id') == nf.get('subject_person_id')), None)
    opening = next((m for m in introduction.get('mentions', [])
                    if m.get('kind') == 'person' and m.get('start') == 0
                    and m.get('person_id') == nf.get('subject_person_id')), None)
    if (not child or not opening or opening.get('surface') != child['surface']
            or introduction['text'][:opening.get('end', 0)] != child['surface']
            or not re.match(re.escape(child['surface']) + '[，,]?字', introduction['text'])):
        return False
    # All actual assertion evidence must be referenced. In particular, neither
    # half of the father/child list may be discarded to manufacture three refs.
    proof = {a['id']: a for a in [nf, nu, uf]}
    refs = connection.get('references')
    keys = ('chapter_id', 'paragraph_id', 'source_id', 'quote')
    expected = [(a['id'],) + tuple(e.get(k) for k in keys)
                for a in [nf, nu, uf] for e in a.get('evidence', [])]
    if (not isinstance(refs, list) or any(not isinstance(r, dict) for r in refs)
            or len(refs) != len(expected)):
        return False
    actual = [(r.get('assertion_id'),) + tuple(r.get(k) for k in keys) for r in refs]
    if len(set(actual)) != len(actual) or set(actual) != set(expected):
        return False
    for ref in refs:
        assertion = proof.get(ref.get('assertion_id'))
        source = chapters.get(ref.get('chapter_id'), {})
        p = next((p for p in source.get('paragraphs', []) if p.get('id') == ref.get('paragraph_id')), None)
        if (not assertion or not p or p.get('text_layer') != 'received_chapter'
                or ref.get('quote') != p.get('text') or not ref.get('scope')
                or ref.get('source_id') != source.get('source_id')
                or ref.get('url') not in [source.get('source', {}).get('url'), source.get('source', {}).get('permalink')]):
            return False
        if any(key in ref for key in ('quote_start', 'quote_end')) and (
                type(ref.get('quote_start')) is not int or type(ref.get('quote_end')) is not int
                or ref['quote_start'] != 0 or ref['quote_end'] != len(p['text'])):
            return False
        persons = {m.get('person_id') for m in p.get('mentions', []) if m.get('kind') == 'person'}
        if assertion is not nf and not {assertion['subject_person_id'], assertion['object_person_id']}.issubset(persons):
            return False
        if assertion is nu and not any(m.get('kind') == 'person' and m.get('person_id') == nu['object_person_id']
                                       and p['text'][max(0, m['start'] - 2):m['start']] == '叔父'
                                       for m in p.get('mentions', [])):
            return False
    return True


def parent_through_paternal_uncle_valid(member, rows, assertions, chapters):
    c = member.get('parent_connection')
    if (not isinstance(c, dict) or c.get('type') != 'parent_through_paternal_uncle'
            or c.get('status') != 'contextual_provisional' or c.get('human_reviewed') is not False
            or not c.get('rationale') or member.get('source_assertion_id') is not None):
        return False
    nephew = rows.get(c.get('nephew_person_id'))
    uncle = rows.get(c.get('uncle_person_id'))
    parent = rows.get(member.get('parent_person_id'))
    nf = assertions.get(c.get('nephew_father_assertion_id'))
    nu = assertions.get(c.get('nephew_uncle_assertion_id'))
    uf = assertions.get(c.get('uncle_father_assertion_id'))
    if not all([nephew, uncle, parent, nf, nu, uf]):
        return False
    own, child, brother, father = [set(row['source_person_ids']) for row in [member, nephew, uncle, parent]]
    sets = [own, child, brother, father]
    if any(a.intersection(b) for i, a in enumerate(sets) for b in sets[i + 1:]):
        return False
    if (any(a.get('status') != 'source_attested' for a in [nf, nu, uf])
            or nf.get('predicate') != 'father' or uf.get('predicate') != 'father'
            or nu.get('predicate') != 'paternal_uncle'
            or nf.get('subject_person_id') not in child or nf.get('object_person_id') not in own
            or nu.get('subject_person_id') != nf.get('subject_person_id') or nu.get('object_person_id') not in brother
            or uf.get('subject_person_id') not in brother or uf.get('object_person_id') not in father
            or any(a.get('qualifiers', {}).get('lineage') != 'paternal' for a in [nf, nu, uf])
            or nu.get('qualifiers', {}).get('source_term') != '叔父'
            or nephew.get('parent_person_id') != member.get('person_id')
            or nephew.get('source_assertion_id') != nf['id']
            or uncle.get('parent_person_id') != member.get('parent_person_id')
            or uncle.get('source_assertion_id') != uf['id']):
        return False
    if any(a.get('predicate') == 'father' and a.get('subject_person_id') in own
           and a.get('object_person_id') not in father for a in assertions.values()):
        return False
    same_passage = any(e.get('paragraph_id') == f.get('paragraph_id')
                       and e.get('chapter_id') == f.get('chapter_id')
                       and e.get('quote') == f.get('quote')
                       for e in nf['evidence'] for f in nu['evidence'])
    if not same_passage:
        cursor = member.get('parent_person_id')
        visited = {member.get('person_id')}
        while cursor is not None:
            if cursor in visited:
                return False
            visited.add(cursor)
            cursor = rows.get(cursor, {}).get('parent_person_id')
        return _continued_child_list_parentage_valid(c, nf, nu, uf, chapters)
    refs = c.get('references')
    proof = {a['id']: a for a in [nf, nu, uf]}
    if (not isinstance(refs, list) or len(refs) != 3 or any(not isinstance(x, dict) for x in refs)
            or {ref.get('assertion_id') for ref in refs} != set(proof)):
        return False
    for ref in refs:
        a = proof[ref['assertion_id']]
        chapter = chapters.get(ref.get('chapter_id'), {})
        p = next((p for p in chapter.get('paragraphs', []) if p['id'] == ref.get('paragraph_id')), None)
        if (not p or p.get('text_layer') != 'received_chapter' or ref.get('quote') != p.get('text')
                or not ref.get('scope') or ref.get('source_id') != chapter.get('source_id')
                or ref.get('url') not in [chapter.get('source', {}).get('url'), chapter.get('source', {}).get('permalink')]
                or not any(all(e.get(k) == ref.get(k) for k in ['chapter_id', 'paragraph_id', 'source_id', 'quote'])
                           for e in a.get('evidence', []))):
            return False
        person_ids = {m.get('person_id') for m in p.get('mentions', []) if m.get('kind') == 'person'}
        if not {a['subject_person_id'], a['object_person_id']}.issubset(person_ids):
            return False
        if a is nu and not any(m.get('person_id') == nu['object_person_id'] and m.get('kind') == 'person'
                               and p['text'][max(0, m['start'] - 2):m['start']] == '叔父'
                               for m in p['mentions']):
            return False
    # Father's identity and paternal uncle must be read from the same passage.
    return any(e.get('paragraph_id') == f.get('paragraph_id') and e.get('chapter_id') == f.get('chapter_id')
               and e.get('quote') == f.get('quote') for e in nf['evidence'] for f in nu['evidence'])


def explicit_maternal_uncle_valid(assertion, paragraphs):
    q = assertion.get('qualifiers', {})
    if (assertion.get('predicate') != 'maternal_uncle' or q.get('lineage') != 'maternal'
            or q.get('generation_difference') != -1 or q.get('mother_person_id') is not None
            or not assertion.get('evidence')):
        return False
    for e in assertion['evidence']:
        hit = paragraphs.get(e.get('paragraph_id'))
        if not hit or not e.get('quote') or e['quote'] not in hit[1].get('text', ''):
            return False
        p = hit[1];mentions = {m['id']: m for m in p.get('mentions', [])}
        subject, obj = mentions.get(e.get('subject_person_mention_id')), mentions.get(e.get('object_person_mention_id'))
        if (not subject or not obj or subject.get('kind') != 'person' or obj.get('kind') != 'person'
                or subject.get('person_id') != assertion.get('subject_person_id')
                or obj.get('person_id') != assertion.get('object_person_id')
                or subject['start'] >= obj['start'] or obj['start'] < 1):
            return False
        named = (p['text'][obj['start'] - 1:obj['start']] == '舅'
                 and q.get('source_term') == '舅' + obj['surface'])
        unnamed = (obj['surface'] == '舅' and q.get('source_term') == '舅'
                   and q.get('object_name_status') == 'not_recorded')
        place = q.get('intervening_place_name')
        gap_start = obj['start'] - len(place) if isinstance(place, str) else obj['start']
        named_with_place = (isinstance(place, str) and bool(place) and gap_start > 0
                            and q.get('source_term') == '舅' + place + obj['surface']
                            and p['text'][gap_start - 1:obj['start']] == '舅' + place
                            and not any(m.get('kind') == 'person' and m['start'] < obj['start']
                                        and m['end'] > gap_start for m in p.get('mentions', [])))
        # 「綏，玄之外甥」 states the same directed relationship in reverse.
        nephew_end = obj['end'] + len('之外甥')
        named_nephew_of = (q.get('source_term') == obj['surface'] + '之外甥'
                          and p['text'][obj['end']:nephew_end] == '之外甥'
                          and p['text'][subject['end']:obj['start']] in ('', '，', '、')
                          and (nephew_end == len(p['text'])
                               or p['text'][nephew_end] in '，。；、'))
        if not (named or unnamed or named_with_place or named_nephew_of):
            return False
        if not any(e['quote'] == p['text'][i:i + len(e['quote'])] and i <= subject['start']
                   and obj['end'] <= i + len(e['quote']) for i in range(len(p['text']))):
            return False
    return True
