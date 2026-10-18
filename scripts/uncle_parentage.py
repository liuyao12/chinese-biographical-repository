"""由具名父、叔父及叔父之父作可撤回組裝，不另造原文父子。"""


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
        if not (named or unnamed or named_with_place):
            return False
        if not any(e['quote'] == p['text'][i:i + len(e['quote'])] and i <= subject['start']
                   and obj['end'] <= i + len(e['quote']) for i in range(len(p['text']))):
            return False
    return True
