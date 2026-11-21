"""以同句「彬及兄子安成太守籍之」兩端的人名、官稱與字位核叔侄方向。"""


def jizhi_uncle_valid(assertion, paragraphs):
    try:
        evidence, = assertion['evidence']
        chapter, p = paragraphs[evidence['paragraph_id']]
        if chapter != evidence['chapter_id'] or chapter != 'c-jinshu-076-wangbin':
            return False
        names = {m['id']: m for m in p['mentions'] if m['kind'] == 'person'}
        child = names[evidence['subject_person_mention_id']]
        uncle = names[evidence['object_person_mention_id']]
        text = p['text']
        return (assertion['predicate'] == 'paternal_uncle' and evidence['quote'] == text
                and assertion['subject_person_id'] == child['person_id']
                and assertion['object_person_id'] == uncle['person_id']
                and child['person_id'] != uncle['person_id']
                and text[uncle['start']:uncle['end']] == uncle['surface'] == '彬'
                and text[uncle['end']:child['start']] == '及兄子安成太守'
                and text[child['start']:child['end']] == child['surface'] == '籍之'
                and text[uncle['start']:child['end']] == assertion['qualifiers']['source_term'])
    except (KeyError, TypeError, ValueError, IndexError):
        return False
