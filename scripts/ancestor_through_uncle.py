"""Draft: missing-parent paternal grandson via explicit paternal uncle and uncle's father.
This is assembly inference, never a received grandfather assertion.
"""
def valid(member, rows, assertions, chapters):
    c = member.get('ancestor_connection', {})
    if (c.get('type') != 'ancestor_through_paternal_uncle'
        or c.get('status') != 'contextual_provisional'
        or c.get('human_reviewed') is not False or not c.get('rationale')
        or member.get('parent_person_id') is not None
        or member.get('source_assertion_id') is not None
        or member.get('connection') != 'grandfather'
        or member.get('generation_distance') != 2
        or member.get('intermediate_person_ids') != [None]):
        return False
    child = set(member.get('source_person_ids', []))
    uncle_row = rows.get(c.get('uncle_person_id'), {})
    grand_row = rows.get(member.get('ancestor_person_id'), {})
    uncle, grand = set(uncle_row.get('source_person_ids', [])), set(grand_row.get('source_person_ids', []))
    u, f = assertions.get(c.get('paternal_uncle_assertion_id'), {}), assertions.get(c.get('uncle_father_assertion_id'), {})
    if not child or not uncle or not grand or child & uncle or child & grand or uncle & grand:
        return False
    uq, fq = u.get('qualifiers', {}), f.get('qualifiers', {})
    if not (u.get('status') == f.get('status') == 'source_attested'
            and u.get('predicate') == 'paternal_uncle'
            and u.get('subject_person_id') in child and u.get('object_person_id') in uncle
            and uq.get('lineage') == 'paternal' and uq.get('generation_difference') == -1
            and 'father_person_id' in uq and uq['father_person_id'] is None
            and f.get('predicate') == 'father' and f.get('subject_person_id') in uncle
            and f.get('object_person_id') in grand
            and fq.get('adopted_for_family_tree') is not False
            and uncle_row.get('parent_person_id') == member.get('ancestor_person_id')
            and uncle_row.get('source_assertion_id') == f.get('id')):
        return False
    # Any separately known father must replace this missing-generation assembly,
    # rather than being silently hidden by the inference.
    if any(a.get('predicate') == 'father' and a.get('subject_person_id') in child
           and a.get('status') == 'source_attested' for a in assertions.values()):
        return False
    proofs = {u.get('id'): u, f.get('id'): f}
    refs = c.get('references')
    expected = {(a['id'], e.get('chapter_id'), e.get('paragraph_id'), e.get('quote')) for a in (u, f) for e in a.get('evidence', [])}
    actual = [(r.get('assertion_id'), r.get('chapter_id'), r.get('paragraph_id'), r.get('quote')) for r in refs if isinstance(r, dict)] if isinstance(refs, list) else []
    if not isinstance(refs, list) or len(actual) != len(refs) or len(actual) != len(expected) or set(actual) != expected:
        return False
    for proof in (u, f):
        covered = set()
        for e in proof.get('evidence', []):
            chapter = chapters.get(e.get('chapter_id'), {})
            if any(e.get(k) != chapter.get(k) for k in ('source_id', 'work_id', 'book_id')):
                return False
            ps = {p['id']: p for p in chapter.get('paragraphs', [])}
            paragraph = ps.get(e.get('paragraph_id'), {})
            if paragraph.get('text_layer') != 'received_chapter':
                return False
            marks = {m['id']: m for m in paragraph.get('mentions', [])}
            for role in ('subject', 'object'):
                mid = e.get(role + '_person_mention_id')
                if mid is not None:
                    mark = marks.get(mid, {})
                    if mark.get('kind') != 'person' or mark.get('person_id') != proof.get(role + '_person_id'):
                        return False
                    covered.add(role)
        if covered != {'subject', 'object'}:
            return False
    for ref in refs:
        if not isinstance(ref, dict) or not ref.get('scope'):
            return False
        proof = proofs[ref['assertion_id']]
        matched = False
        for e in proof.get('evidence', []):
            chapter = chapters.get(e.get('chapter_id'), {})
            paras = {p['id']: p for p in chapter.get('paragraphs', [])}
            para = paras.get(e.get('paragraph_id'), {})
            if (all(ref.get(k) == e.get(k) for k in ('quote', 'paragraph_id', 'chapter_id', 'source_id', 'work_id', 'book_id'))
                and e.get('source_id') == chapter.get('source_id')
                and e.get('quote') == para.get('text')
                and ref.get('url') in (chapter.get('source', {}).get('url'), chapter.get('source', {}).get('permalink'))
                and str(ref.get('url', '')).startswith(('http://','https://'))):
                matched = True
        if not matched:
            return False
    return True
