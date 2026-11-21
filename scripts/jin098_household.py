"""辨識「甲無子，養乙子丙」的三名角色及該處明記的生父。"""
def adoption_valid(assertion, paragraphs, assertions):
    try:
        if assertion['predicate'] != 'adoptive_father' or assertion['status'] != 'source_attested':
            return False
        e, = assertion['evidence']
        cid, p = paragraphs[e['paragraph_id']]
        if cid != e['chapter_id'] or e['quote'] != p['text'] or p.get('text_layer') != 'received_chapter':
            return False
        ms = {m['id']: m for m in p['mentions'] if m.get('kind') == 'person'}
        q = assertion['qualifiers']
        if set(q) != {'source_term','adoption_basis','modern_legal_status','birth_parent_assertion_id'} or q['adoption_basis'] != 'named_adopter_yang_named_son' or q['modern_legal_status'] != 'not_inferred':
            return False
        birth = next(a for a in assertions if a['id'] == q['birth_parent_assertion_id'])
        be, = birth['evidence']
        child = ms[e['subject_person_mention_id']]
        adopter = ms[e['object_person_mention_id']]
        father = ms[be['object_person_mention_id']]
        if (not (be['chapter_id'] == cid and be['paragraph_id'] == p['id'] and be['quote'] == p['text'])
                or be['subject_person_mention_id'] != child['id'] or birth['predicate'] != 'father'
                or birth['status'] != 'source_attested' or len({child['person_id'],father['person_id'],adopter['person_id']}) != 3
                or birth['subject_person_id'] != child['person_id'] or birth['object_person_id'] != father['person_id']
                or assertion['subject_person_id'] != child['person_id'] or assertion['object_person_id'] != adopter['person_id']):
            return False
        for m in (child, adopter, father):
            if type(m['start']) is not int or type(m['end']) is not int or not 0 <= m['start'] < m['end'] <= len(p['text']) or p['text'][m['start']:m['end']] != m['surface']:
                return False
        return (p['text'][adopter['end']:father['start']] == '無子，養'
                and p['text'][father['end']:child['start']] == '子'
                and q['source_term'] == p['text'][adopter['start']:child['end']]
                and birth['qualifiers']['source_term'] == p['text'][father['start']:child['end']])
    except (KeyError, TypeError, ValueError, StopIteration, IndexError):
        return False
