"""Finite source binding for Shiji 120's "黯姑姊子司馬安" kinship claim."""

CHAPTER = 'c-shiji-120-jizheng'
PARAGRAPH = CHAPTER + ':p014'
SUBJECT = 'fmh_dmt_cql'  # 汲黯
OBJECT = '84g_35d_vcn'   # 司馬安
SUBJECT_MENTION = CHAPTER + ':m014-0025'
OBJECT_MENTION = CHAPTER + ':m014-0029'
CLAUSE = '黯姑姊子司馬安'
SOURCE_TERM = '姑姊子'
COMMENTARY_URL = 'https://www.shidianguji.com/zh/book/CSYP023/chapter/1kxsuizuagxlu'
HANSHU_PARAGRAPH = 'c-hanshu-050-zhangfengjizheng:jian:p003'
HANSHU_CHAPTER = 'c-hanshu-050-zhangfengjizheng'
HANSHU_SUBJECT_MENTION = HANSHU_CHAPTER + ':jian:m003-0026'
HANSHU_OBJECT_MENTION = HANSHU_CHAPTER + ':jian:m003-0029'
HANSHU_SURFACE = '黯姊子司馬安'


def valid(assertion, paragraphs):
    """Accept only the fixed Shiji wording with both current person anchors."""
    q = assertion.get('qualifiers', {})
    binding = q.get('source_clause_binding', {})
    hit = paragraphs.get(PARAGRAPH)
    if not hit:
        return False
    chapter, paragraph = hit
    text = paragraph.get('text', '')
    mentions = {m.get('id'): m for m in paragraph.get('mentions', [])}
    subject = mentions.get(SUBJECT_MENTION)
    obj = mentions.get(OBJECT_MENTION)
    start = text.find(CLAUSE)
    expected_qualifiers = {
        'source_term': SOURCE_TERM,
        'paternal_aunt_person_id': None,
        'generation_difference': 0,
        'exact_distance': None,
        'common_ancestor_person_id': None,
        'subject_relative_age': 'unknown',
        'source_clause_binding': {
            'pattern': 'shiji120_jian_sima_an_paternal_aunt_child',
            'subject_person_mention_id': SUBJECT_MENTION,
            'object_person_mention_id': OBJECT_MENTION,
            'start': 25,
            'end': 32,
            'surface': CLAUSE,
        },
    }
    if (chapter != CHAPTER or paragraph.get('id') != PARAGRAPH
            or paragraph.get('text_layer') != 'received_chapter'
            or assertion.get('id') != 'a-shiji120-004'
            or assertion.get('predicate') != 'paternal_aunt_child'
            or assertion.get('status') != 'source_attested'
            or assertion.get('subject_person_id') != SUBJECT
            or assertion.get('object_person_id') != OBJECT
            or q != expected_qualifiers
            or start != 25 or text[start:start + len(CLAUSE)] != CLAUSE
            or not subject or subject.get('kind') != 'person'
            or subject.get('person_id') != SUBJECT or subject.get('surface') != '黯'
            or (subject.get('start'), subject.get('end')) != (25, 26)
            or not obj or obj.get('kind') != 'person'
            or obj.get('person_id') != OBJECT or obj.get('surface') != '司馬安'
            or (obj.get('start'), obj.get('end')) != (29, 32)
            or not assertion.get('evidence') or len(assertion['evidence']) != 1):
        return False
    evidence = assertion['evidence'][0]
    if (evidence.get('work_id') != 'w-shiji'
            or evidence.get('book_id') != 'b-shiji-120'
            or evidence.get('chapter_id') != CHAPTER
            or evidence.get('source_id') != 's-shiji120-jizheng'
            or evidence.get('paragraph_id') != PARAGRAPH
            or evidence.get('quote') != text
            or evidence.get('subject_person_mention_id') != SUBJECT_MENTION
            or evidence.get('object_person_mention_id') != OBJECT_MENTION):
        return False
    references = assertion.get('references', [])
    if (len(references) != 1
            or references[0].get('title') != '《兩漢刊誤補遺》卷六'
            or references[0].get('url') != COMMENTARY_URL
            or references[0].get('quote') != '司馬安之於汲黯，自史記言之，則爲姑之子，於黯爲内兄弟。自漢書言之，則爲姊之子，實黯之自出也。'
            or references[0].get('image_verified') is not False):
        return False
    comparisons = assertion.get('comparative_evidence', [])
    return (len(comparisons) == 1
            and comparisons[0].get('work_id') == 'w-hanshu'
            and comparisons[0].get('book_id') == 'b-hanshu-050'
            and comparisons[0].get('chapter_id') == 'c-hanshu-050-zhangfengjizheng'
            and comparisons[0].get('source_id') == 's-hanshu-050-zhangfengjizheng'
            and comparisons[0].get('paragraph_id') == HANSHU_PARAGRAPH
            and HANSHU_SURFACE in comparisons[0].get('quote', '')
            and comparisons[0].get('subject_person_mention_id') == HANSHU_SUBJECT_MENTION
            and comparisons[0].get('object_person_mention_id') == HANSHU_OBJECT_MENTION)
