"""原文母親稱謂；未明言生育時不轉成生母或推補婚配。"""


def maternal_role_valid(assertion, paragraphs):
    if assertion.get('fixed_source_fact_binding',{}).get('kind')=='fixed_kanripo_person_fact_slots':
        try:from scripts.fixed_kanripo_fact_slots import valid_from_paragraphs
        except ImportError:from fixed_kanripo_fact_slots import valid_from_paragraphs
        return valid_from_paragraphs(assertion,paragraphs)
    if 'received_family_frame' in assertion.get('qualifiers', {}):
        try:from scripts.punctuated_family_frames import valid
        except ImportError:from punctuated_family_frames import valid
        return valid(assertion, paragraphs)
    if assertion.get('qualifiers', {}).get('source_clause_binding', {}).get('rule')=='attached_received_biography_frame':
        try:from scripts.attached_biography_frames import kinship_valid
        except ImportError:from attached_biography_frames import kinship_valid
        return kinship_valid(assertion,paragraphs)
    if assertion.get('qualifiers', {}).get('source_clause_binding', {}).get('rule', '').startswith('continued_biography_'):
        try:
            from scripts.continued_biography_family import valid as continued_valid
        except ImportError:
            from continued_biography_family import valid as continued_valid
        return continued_valid(assertion, paragraphs)

    # Position-bound close-family clauses; retain all older grammar contracts.
    if assertion.get('qualifiers', {}).get('source_clause_binding', {}).get('rule', '').startswith('close_family_'):
        try:
            from scripts.biography_close_family import valid as close_family_valid
        except ImportError:
            from biography_close_family import valid as close_family_valid
        return close_family_valid(assertion, paragraphs)

    try:
        from scripts.song047_maternal import clause_valid
    except ImportError:
        from song047_maternal import clause_valid
    if clause_valid(assertion, paragraphs):
        return True
    try:
        from scripts.maternal_clauses import maternal_clause_valid
    except ImportError:
        from maternal_clauses import maternal_clause_valid
    if maternal_clause_valid(assertion, paragraphs):
        return True
    try:
        from scripts.biographical_maternal_title import maternal_title_scope_valid
    except ImportError:
        from biographical_maternal_title import maternal_title_scope_valid
    if maternal_title_scope_valid(assertion, paragraphs):
        return True
    # Source-scoped Jin maternal clauses; preserve unspecified role.
    if assertion.get('qualifiers', {}).get('source_clause_binding', {}).get('kind') in ('biography_head_mother_following_named_father', 'opening_mother_death_child_burial_resumption', 'named_child_mother_in_title_formula'):
        try:
            from scripts.huan_kinship_clauses import mother_valid
        except ImportError:
            from huan_kinship_clauses import mother_valid
        return mother_valid(assertion, paragraphs)
    q = assertion.get('qualifiers', {})
    if (assertion.get('predicate') != 'maternal_role'
            or set(q) != {'source_term', 'role', 'biological_mother', 'father_person_id'}
            or q.get('biological_mother') is not None or q.get('father_person_id') is not None
            or q.get('role') not in ('mother_unspecified', 'prior_mother')
            or not assertion.get('evidence')):
        return False
    for e in assertion['evidence']:
        hit = paragraphs.get(e.get('paragraph_id'))
        if not hit or hit[0] != e.get('chapter_id'):
            return False
        p = hit[1]
        ms = {m['id']: m for m in p.get('mentions', [])}
        subject = ms.get(e.get('subject_person_mention_id'))
        obj = ms.get(e.get('object_person_mention_id'))
        if (not subject or not obj or subject.get('person_id') != assertion.get('subject_person_id')
                or obj.get('person_id') != assertion.get('object_person_id')
                or e.get('quote') != p.get('text') or not q.get('source_term')
                or q['source_term'] not in p['text']):
            return False
        term = q['source_term']
        if q['role'] == 'mother_unspecified':
            if term != '母' + obj['surface'] or p['text'][obj['start']-1:obj['end']] != term:
                return False
            # Bind the mother word to the child, rather than any marked person
            # elsewhere in the same paragraph. A documented biography's opening
            # plus its explicit 封母 formula is the separate existing scope.
            local_child = any(m.get('kind') == 'person'
                              and m.get('person_id') == assertion['subject_person_id']
                              and m.get('end') == obj['start'] - 1
                              for m in p.get('mentions', []))
            opening = next((m for m in p.get('mentions', [])
                            if m.get('kind') == 'person' and m.get('start') == 0
                            and m.get('person_id') == assertion['subject_person_id']), None)
            biography_enfeoffment = (opening is not None
                and p['text'][opening['end']:].startswith(('諱', '字'))
                and p['text'][obj['start']-2:obj['start']] == '封母'
                and p['text'][obj['end']:].startswith('為')
                and '立為皇后' in p['text'][opening['end']:obj['start']-2]
                and not any(mark in p['text'][:obj['start']] for mark in ('曰', '云', '：', '「', '『')))
            if not (local_child or biography_enfeoffment):
                return False
        else:
            # 前母 is retained literally: it does not select birth/step/adoptive status.
            if ('皆后之前母也' not in term or obj['surface'] not in term.split('二夫人')[0]
                    or term not in p['text'] or obj['end'] > p['text'].index('前母')):
                return False
    return True
