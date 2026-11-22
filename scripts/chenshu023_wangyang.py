"""Bind Wang Yang's maternal reference and his unassumed appointments to Chen 23."""

CHAPTER = 'c-chenshu-023-wangyang-complete'
WANG = '7r6_k52_qji_ABAAAAAABAAA'
MOTHER = 'py8_5fd_4x4'
PROVINCE = '出為信威將軍、雲麾始興王長史，行州府事。未行，遷中書令'
COURT = '尋授尚書右僕射，未拜，加侍中，遷左僕射'


def fixed(chapter):
    return chapter['id'] == CHAPTER and chapter['source']['revision_id'] == 1514496


def anchored(row, paragraph, clause, word):
    text = paragraph['text']
    if text.count(clause) != 1 or clause.count(word) != 1:
        return False
    start = text.index(clause) + clause.index(word)
    return (row['paragraph_id'] == paragraph['id'] and row['surface'] == word
            and row['start'] == start and row['end'] == start + len(word))


def mother_valid(assertion, evidence, chapter):
    try:
        paragraph = chapter['paragraphs'][0]
        reference, = (r for r in chapter['annotation']['person_reference_occurrences']
                      if r['id'] == evidence['object_person_reference_id'])
        son, = (m for m in paragraph['mentions'] if m['id'] == evidence['subject_person_mention_id'])
        relation = assertion['qualifiers']
        clause = '丁所生母憂，歸于丹陽。'
        return (fixed(chapter) and paragraph['id'] == evidence['paragraph_id']
                and chapter['source_id'] == evidence['source_id'] and paragraph['text'] == evidence['quote']
                and assertion['predicate'] == 'mother' and assertion['status'] == 'source_attested'
                and relation['source_term'] == '丁所生母憂' and relation['reading_basis']['kind'] == 'chen023_wangyang_birth_mother'
                and son['person_id'] == assertion['subject_person_id'] == WANG
                and son['kind'] == 'person' and son['surface'] == '王瑒'
                and (son['start'], son['end']) == (0, 2) and paragraph['text'].startswith('王瑒字子璵')
                and reference['person_id'] == assertion['object_person_id'] == MOTHER
                and reference['referent_role'] == 'third_person' and anchored(reference, paragraph, clause, '所生母')
                and anchored(relation['reading_basis']['relationship_anchor'], paragraph, clause, '所生母'))
    except (KeyError, TypeError, ValueError, IndexError):
        return False


def proposal_valid(proposal, chapter):
    try:
        paragraph = chapter['paragraphs'][2]
        title = proposal['title']
        clause, verb, result = {
            '信威將軍': (PROVINCE, '出為', '未行'),
            '雲麾始興王長史': (PROVINCE, '出為', '未行'),
            '尚書右僕射': (COURT, '授', '未拜'),
        }[title]
        evidence, = proposal['evidence']
        person, = (m for m in paragraph['mentions'] if m['id'] == proposal['person_mention_id'])
        return (fixed(chapter) and paragraph['id'] == evidence['paragraph_id'] and evidence['quote'] == paragraph['text']
                and chapter['source_id'] == evidence['source_id'] and person['id'] == evidence['person_mention_id']
                and person['kind'] == 'person' and person['surface'] == '瑒' and person['person_id'] == proposal['person_id'] == WANG
                and (person['start'], person['end']) == (paragraph['text'].index('瑒性寬和'), paragraph['text'].index('瑒性寬和') + 1)
                and proposal['appointment_stage'] == 'appointment' and proposal['non_assumption_kind'] == 'did_not_take_up'
                and proposal['outcome'] == 'not_assumed' and proposal['proposal_kind'] == 'unassumed_appointment'
                and anchored(proposal['role_anchor'], paragraph, clause, title)
                and anchored(proposal['appointment_anchor'], paragraph, clause, verb)
                and anchored(proposal['non_assumption_anchor'], paragraph, clause, result))
    except (KeyError, TypeError, ValueError, IndexError):
        return False
