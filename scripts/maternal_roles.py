"""原文母親稱謂；未明言生育時不轉成生母或推補婚配。"""


def maternal_role_valid(assertion, paragraphs):
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
        else:
            # 前母 is retained literally: it does not select birth/step/adoptive status.
            if ('皆后之前母也' not in term or obj['surface'] not in term.split('二夫人')[0]
                    or term not in p['text'] or obj['end'] > p['text'].index('前母')):
                return False
    return True
