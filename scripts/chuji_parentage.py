"""Validate explicitly named 出繼; retain biological parentage separately."""


def chuji_parentage_valid(a, paragraphs, assertions):
    if 'received_family_frame' in a.get('qualifiers', {}):
        try:from scripts.punctuated_family_frames import valid
        except ImportError:from punctuated_family_frames import valid
        return valid(a, paragraphs)
    q = a.get('qualifiers', {})
    if q.get('adoption_basis') == 'explicit_shouyang':
        try:
            from scripts.historical_family_clauses import explicit_shouyang_valid
        except ImportError:
            from historical_family_clauses import explicit_shouyang_valid
        return explicit_shouyang_valid(a, paragraphs)
    if q.get('adoption_basis') == 'named_younger_brother_son_as_heir':
        try:
            from scripts.named_heir_parentage import named_brother_son_heir_valid
        except ImportError:
            from named_heir_parentage import named_brother_son_heir_valid
        return named_brother_son_heir_valid(a, paragraphs, assertions)
    if q.get('adoption_basis') == 'named_agnatic_senior_no_heir_as_successor':
        try:
            from scripts.named_agnatic_adoption import named_agnatic_adoption_valid
        except ImportError:
            from named_agnatic_adoption import named_agnatic_adoption_valid
        return named_agnatic_adoption_valid(a, paragraphs, assertions)
    evidence = a.get('evidence', [])
    if (a.get('predicate') != 'adoptive_father'
            or a.get('status') != 'source_attested'
            or q.get('adoption_basis') != 'chuji_named_paternal_uncle'
            or q.get('modern_legal_status') != 'not_inferred'
            or len(evidence) != 1):
        return False
    e = evidence[0]
    hit = paragraphs.get(e.get('paragraph_id'))
    if not hit or hit[0] != e.get('chapter_id'):
        return False
    p = hit[1]
    if e.get('quote') != p.get('text'):
        return False
    mentions = {m['id']: m for m in p.get('mentions', [])}
    child = mentions.get(e.get('subject_person_mention_id'), {})
    parent = mentions.get(e.get('object_person_mention_id'), {})
    if (child.get('kind') != 'person' or parent.get('kind') != 'person'
            or child.get('person_id') != a.get('subject_person_id')
            or parent.get('person_id') != a.get('object_person_id')
            or child['person_id'] == parent['person_id']):
        return False
    term = q.get('source_term')
    if not isinstance(term, str) or not term.startswith('出繼伯父'):
        return False
    starts = [i for i in range(len(p['text'])) if p['text'].startswith(term, i)]
    if not any(child['end'] <= i < parent['start']
               and parent['end'] == i + len(term) for i in starts):
        return False
    by_id = {r['id']: r for r in assertions}
    for key, predicate in [('biological_father_assertion_id', 'father'),
                           ('paternal_uncle_assertion_id', 'paternal_uncle')]:
        r = by_id.get(q.get(key), {})
        if (r.get('predicate') != predicate
                or r.get('status') != 'source_attested'
                or r.get('subject_person_id') != child['person_id']
                or len(r.get('evidence', [])) != 1):
            return False
        re = r['evidence'][0]
        rm = mentions.get(re.get('object_person_mention_id'), {})
        if (re.get('paragraph_id') != p['id'] or re.get('quote') != p['text']
                or re.get('subject_person_mention_id') != child['id']
                or rm.get('person_id') != r.get('object_person_id')
                or rm.get('kind') != 'person'):
            return False
        if predicate == 'paternal_uncle':
            if r.get('object_person_id') != parent['person_id']:
                return False
        elif (r.get('object_person_id') in (child['person_id'], parent['person_id'])
              or p['text'][rm['start'] - 1:rm['start']] != '父'):
            return False
    return True
