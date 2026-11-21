# coding: utf-8
"""Bind the father named by temple title to Shi’an's printed birth order."""
def valid(assertion, evidence, chapter):
    clause = '始安王子真字孝貞，孝武帝第十一子。'
    if (chapter.get('id') != 'c-songshu-080-shian-zizhen-parent'
            or chapter['source'].get('revision_id') != 2261200 or evidence.get('quote') != clause
            or (assertion.get('predicate'), assertion.get('subject_person_id'), assertion.get('object_person_id'))
                != ('father', 'hx8_st4_jdd_H', 'hx8_st4_jdd')
            or assertion['qualifiers'].get('source_term') != '孝武帝第十一子'):
        return False
    p = next((p for p in chapter['paragraphs'] if p['id'] == evidence.get('paragraph_id')), {})
    if p.get('text') != clause:
        return False
    son = evidence.get('subject_person_mention_id')
    father = evidence.get('object_person_reference_id')
    return (any(m['id'] == son and m['person_id'] == assertion['subject_person_id']
                and m['start'] == clause.index('始安王子真') and m['end'] == m['start'] + 5
                and m['surface'] == '始安王子真' for m in p['mentions'])
            and any(r['id'] == father and r['person_id'] == assertion['object_person_id']
                    and r['paragraph_id'] == p['id'] and r['start'] == clause.index('孝武帝')
                    and r['end'] == r['start'] + 3 and r['surface'] == '孝武帝'
                    for r in chapter['annotation']['person_reference_occurrences']))
