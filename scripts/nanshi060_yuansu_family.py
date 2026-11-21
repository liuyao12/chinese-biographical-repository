"""Identify the unnamed daughter by her single place in the received marriage clause."""
def valid(assertion, evidence, chapter):
    clause = '元素娶尚書僕射琅邪王僧朗女，生子寧早卒，寧遺腹生子叡，亦當從戮，僧朗啟孝武救之得免。'
    paragraph = next((p for p in chapter['paragraphs'] if p['id'] == evidence['paragraph_id']), {})
    if (chapter.get('id') != 'c-nanshi-060-yinjun-yuansu-family'
            or chapter['source'].get('revision_id') != 1495505
            or paragraph.get('text') != clause or evidence.get('quote') != clause):
        return False
    wife = 'q7m_r8k_2vn_E'
    patterns = {
        'father': (wife, 'q7m_r8k_2vn', '王僧朗女', '王僧朗'),
        'mother': ('9ac_ddl_9iz_A', wife, '王僧朗女，生子寧', '寧'),
        'spouse': ('9ac_ddl_9iz', wife, '元素娶尚書僕射琅邪王僧朗女', '元素'),
    }
    subject, obj, term, name = patterns.get(assertion['predicate'], (None,) * 4)
    if (subject, obj, term) != (assertion['subject_person_id'], assertion['object_person_id'],
                                assertion['qualifiers'].get('source_term')):
        return False
    ref_key, mid_key = (('subject', 'object') if subject == wife else ('object', 'subject'))
    rid, mid = evidence.get(ref_key + '_person_reference_id'), evidence.get(mid_key + '_person_mention_id')
    expected = obj if subject == wife else subject
    return (any(r['id'] == rid and r['person_id'] == wife and r['surface'] == '女'
                and r['start'] == clause.index('女') and r['end'] == r['start'] + 1
                and r['paragraph_id'] == paragraph['id']
                for r in chapter['annotation']['person_reference_occurrences'])
            and any(m['id'] == mid and m['person_id'] == expected and m['surface'] == name
                    and m['start'] == clause.index(name) and m['end'] == m['start'] + len(name)
                    for m in paragraph['mentions']))
