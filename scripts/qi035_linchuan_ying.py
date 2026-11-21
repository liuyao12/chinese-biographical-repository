# coding: utf-8
"""Bind the father named by temple title to Linchuan's printed birth order."""
def valid(assertion, evidence, chapter):
    clause = '臨川獻王映，字宣光，太祖第三子也。'
    if (chapter.get('id') != 'c-nanqishu-035-linchuan-ying-parent'
            or chapter['source'].get('revision_id') != 2401782 or evidence.get('quote') != clause
            or (assertion.get('predicate'), assertion.get('subject_person_id'), assertion.get('object_person_id'))
                != ('father', '47p_kjh_ez7_C', '47p_kjh_ez7')
            or assertion['qualifiers'].get('source_term') != '太祖第三子也'):
        return False
    p = next((p for p in chapter['paragraphs'] if p['id'] == evidence.get('paragraph_id')), {})
    if p.get('text') != clause:
        return False
    son = evidence.get('subject_person_mention_id')
    father = evidence.get('object_person_reference_id')
    return (any(m['id'] == son and m['person_id'] == assertion['subject_person_id']
                and m['start'] == clause.index('映') and m['end'] == m['start'] + 1
                and m['surface'] == '映' for m in p['mentions'])
            and any(r['id'] == father and r['person_id'] == assertion['object_person_id']
                    and r['paragraph_id'] == p['id'] and r['start'] == clause.index('太祖')
                    and r['end'] == r['start'] + 2 and r['surface'] == '太祖'
                    for r in chapter['annotation']['person_reference_occurrences']))
