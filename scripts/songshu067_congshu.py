"""Validate Songshu 67's source-bound "從叔混" kinship assertion."""

CHAPTER = 'c-songshu-067-xielingyun'
PARAGRAPH = CHAPTER + ':p001'
SUBJECT = 'aa6_83c_juy_CDAA'  # 謝靈運
OBJECT = 'aa6_83c_juy_BAC'    # 謝混
BIOGRAPHICAL_SUBJECT = PARAGRAPH + ':m00000'
SUBJECT_MENTION = PARAGRAPH + ':m00052'
OBJECT_MENTION = PARAGRAPH + ':m00071'
KINSHIP_CLAUSE = '從叔混特知愛之'
SOURCE_TERM = '從叔混'


def valid(assertion, paragraphs):
    """Accept only the received passage and its fixed, linked name anchors."""
    hit = paragraphs.get(PARAGRAPH)
    if not hit:
        return False
    chapter, paragraph = hit
    text = paragraph.get('text', '')
    mentions = {m.get('id'): m for m in paragraph.get('mentions', [])}
    biography = mentions.get(BIOGRAPHICAL_SUBJECT)
    subject = mentions.get(SUBJECT_MENTION)
    obj = mentions.get(OBJECT_MENTION)
    q = assertion.get('qualifiers', {})
    structure = q.get('kinship_structure', {})
    binding = q.get('source_clause_binding', {})
    start = text.find(KINSHIP_CLAUSE)
    expected_structure = {
        'lineage': 'paternal',
        'generation_difference': -1,
        'collateral': True,
        'distance': None,
        'common_ancestor_person_id': None,
        'subject_relative_age': 'unknown',
    }
    expected_binding = {
        'pattern': 'songshu067_congshu_subject_to_senior',
        'biographical_subject_person_mention_id': BIOGRAPHICAL_SUBJECT,
        'subject_person_mention_id': SUBJECT_MENTION,
        'object_person_mention_id': OBJECT_MENTION,
        'start': 69,
        'end': 76,
        'surface': KINSHIP_CLAUSE,
    }
    if (chapter != CHAPTER or paragraph.get('id') != PARAGRAPH
            or assertion.get('id') != 'a-song067-lingyun-congshu-hun-001'
            or assertion.get('predicate') != 'agnatic_senior_kin'
            or assertion.get('status') != 'source_attested'
            or assertion.get('subject_person_id') != SUBJECT
            or assertion.get('object_person_id') != OBJECT
            or set(q) != {'source_term', 'kinship_structure', 'source_clause_binding'}
            or q.get('source_term') != SOURCE_TERM
            or structure != expected_structure or binding != expected_binding
            or start != 69 or text[start:start + len(KINSHIP_CLAUSE)] != KINSHIP_CLAUSE
            or not biography or biography.get('kind') != 'person'
            or biography.get('person_id') != SUBJECT or biography.get('surface') != '謝靈運'
            or (biography.get('start'), biography.get('end')) != (0, 3)
            or not subject or subject.get('kind') != 'person'
            or subject.get('person_id') != SUBJECT or subject.get('surface') != '靈運'
            or (subject.get('start'), subject.get('end')) != (52, 54)
            or not obj or obj.get('kind') != 'person'
            or obj.get('person_id') != OBJECT or obj.get('surface') != '混'
            or (obj.get('start'), obj.get('end')) != (71, 72)
            or any(m.get('kind') == 'person' and m.get('surface') == '之'
                   and m.get('start') == 75 for m in paragraph.get('mentions', []))
            or not assertion.get('evidence') or len(assertion['evidence']) != 1):
        return False
    evidence = assertion['evidence'][0]
    return (evidence.get('work_id') == 'w-songshu'
            and evidence.get('book_id') == 'b-songshu-067'
            and evidence.get('chapter_id') == CHAPTER
            and evidence.get('source_id') == 's-songshu-067-xielingyun'
            and evidence.get('paragraph_id') == PARAGRAPH
            and evidence.get('quote') == text
            and evidence.get('subject_person_mention_id') == SUBJECT_MENTION
            and evidence.get('object_person_mention_id') == OBJECT_MENTION)
