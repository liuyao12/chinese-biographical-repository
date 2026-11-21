# coding: utf-8
"""Bind the father named by temple title to the Prince of Badong's fourth-child statement."""
def valid(assertion, evidence, chapter):
    clause = '魚復侯子響字雲音，世祖第四子也。豫章王嶷無子，養子響，後有子，表留爲嫡。'
    if (chapter.get('id') != 'c-nanqishu-040-zixiang-xi-family'
            or chapter['source'].get('revision_id') != 2272748 or evidence.get('quote') != clause
            or (assertion.get('predicate'), assertion.get('subject_person_id'), assertion.get('object_person_id'))
                != ('father', 'kix_r92_2ed_G', 'kix_r92_2ed')
            or assertion['qualifiers'].get('source_term') != '世祖第四子也'):
        return False
    p = next((p for p in chapter['paragraphs'] if p['id'] == evidence.get('paragraph_id')), {})
    if p.get('text') != clause:
        return False
    son = evidence.get('subject_person_mention_id')
    father = evidence.get('object_person_reference_id')
    return (any(m['id'] == son and m['person_id'] == assertion['subject_person_id']
                and m['start'] == clause.index('子響') and m['end'] == m['start'] + 2
                and m['surface'] == '子響' for m in p['mentions'])
            and any(r['id'] == father and r['person_id'] == assertion['object_person_id']
                    and r['paragraph_id'] == p['id'] and r['start'] == clause.index('世祖')
                    and r['end'] == r['start'] + 2 and r['surface'] == '世祖'
                    for r in chapter['annotation']['person_reference_occurrences']))
