"""核王允之本傳對敦、導之「從伯」。"""


def yun_congbo_valid(assertion, paragraphs):
    try:
        e, = assertion['evidence']
        chap, p = paragraphs[e['paragraph_id']]
        terms = {'從伯敦': ('line020', '允之字深猷。總角，從伯敦謂為似己', '敦'),
                 '從伯導': ('line022', '除義興太守，以憂哀不拜，從伯導與其書曰', '導')}
        term = assertion['qualifiers']['source_term']
        key, phrase, name = terms[term]
        names = {m['id']:m for m in p['mentions'] if m.get('kind') == 'person'}
        child = names[e['subject_person_mention_id']]
        elder = names[e['object_person_mention_id']]
        t = p['text']
        return (chap == e['chapter_id'] == 'c-jinshu-076-wangshu-family'
                and e['paragraph_id'] == chap + ':' + key
                and t.count(phrase) == 1 and e['quote'] == t
                and assertion['predicate'] == 'agnatic_senior_kin'
                and assertion['subject_person_id'] == child['person_id'] == 'a04_d8f_416'
                and assertion['object_person_id'] == elder['person_id']
                and assertion['qualifiers']['kinship_structure'] == dict(
                    lineage='paternal', generation_difference=-1, collateral=True, distance=None,
                    common_ancestor_person_id=None, subject_relative_age='unknown')
                and t[child['start']:child['end']] == child['surface'] == '允之'
                and t[elder['start']:elder['end']] == elder['surface'] == name
                and elder['start'] == t.index(phrase) + phrase.index(term) + len('從伯'))
    except (KeyError, ValueError, IndexError, TypeError):
        return False
