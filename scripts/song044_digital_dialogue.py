"""核對固定本宋書卷44問答中的兩個報齡。"""
from hashlib import sha256

CHAPTER = 'c-songshu-044-xiehui-digital'
SOURCE = 's-songshu-044-xiehui-digital-ws1746033'
RAW_SHA = '9ca7cb37e05e0ebcc400fb220a1f3970ddc2c0f948483f04b71ea93847a69898'
PARAGRAPH_SHA = 'a51dc0836ba394f21b7862c6986e002a716e5770d4ce637ff975c8a34858f67b'
HUI, DAN, XIAN = 'aa6_83c_juy_AAAA', 'ph1_0cf_nxw', 'yoo_ox0_545_BABAAAB'


def occurrence(rows, paragraph, clause, word, person):
    text = paragraph['text']
    if text.count(clause) != 1 or clause.count(word) != 1:
        raise ValueError(clause)
    start = text.index(clause) + clause.index(word)
    hit, = (row for row in rows if row['person_id'] == person and row['surface'] == word
            and row['start'] == start and row['end'] == start + len(word))
    return hit


def age_anchor(age, chapter):
    try:
        if (chapter['id'] != CHAPTER or chapter['source_id'] != SOURCE
                or chapter['source']['revision_id'] != 1746033
                or chapter['source']['raw_file_sha256'] != RAW_SHA):
            return None
        p, = (r for r in chapter['paragraphs'] if r['id'] == CHAPTER + ':p006')
        if (sha256(p['text'].encode()).hexdigest() != PARAGRAPH_SHA
                or p['source_position']['revision_id'] != 1746033
                or p['source_position']['first_line'] != 19 or p['source_position']['last_line'] != 19
                or p['text_layer'] != 'received_chapter'):
            return None
        roles = [r for r in p['mentions'] if r['kind'] == 'person']
        binding = age['reported_dialogue']
        if binding['role'] == 'answer':
            clause = '澹問晦年，晦答曰：「三十五。」'
            subject = occurrence(roles, p, '晦答曰：「三十五。」', '晦', HUI)
            asker = occurrence(roles, p, '澹問晦年', '澹', DAN)
            expected = dict(role='answer', speaker_mention_id=subject['id'],
                            asker_mention_id=asker['id'], clause=clause)
            field, term, number, value = 'person_mention_id', '晦答曰：「三十五。」', '三十五', 35
        elif binding['role'] == 'recollection':
            clause = '澹笑曰：「昔荀中郎年二十七為北府都督'
            refs = [r for r in chapter['annotation']['person_reference_occurrences']
                    if r['paragraph_id'] == p['id'] and r['referent_role'] == 'third_person']
            speaker = occurrence(roles, p, '澹笑曰', '澹', DAN)
            subject = occurrence(refs, p, clause, '荀中郎', XIAN)
            expected = dict(role='recollection', speaker_mention_id=speaker['id'], clause=clause)
            field, term, number, value = 'person_reference_id', '年二十七', '二十七', 27
        else:
            return None
        e, = age['evidence']
        if (binding == expected and clause in p['text'] and age['person_id'] == subject['person_id']
                and age['source_term'] == term and age['source_number'] == number
                and type(age['value']) is int and age['value'] == value
                and age['age_context'] == {'kind': 'during_life'} and age['birth_year'] is None
                and age['counting'] == 'unspecified_source_age' and age['date_expression'] is None
                and age['status'] == 'source_attested' and age['human_reviewed'] is False
                and e == {'work_id': 'w-songshu', 'book_id': 'b-songshu-044',
                          'source_id': SOURCE, 'chapter_id': CHAPTER, 'paragraph_id': p['id'],
                          'quote': p['text'], field: subject['id']}):
            return subject
    except (ValueError, KeyError, TypeError):
        return None
    return None
