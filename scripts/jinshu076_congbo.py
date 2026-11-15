"""Narrow source binding for Wang Biao Zhi's explicit 從伯導 clause."""

CHAPTER = 'c-jinshu-076-wangbiaozhi'
PARAGRAPH = CHAPTER + ':line055'
SUBJECT = '7r6_k52_qji_ABDBB'
OBJECT = '7r6_k52_qji_ABAA'
SUBJECT_MENTION = PARAGRAPH + ':m0000'
OBJECT_MENTION = PARAGRAPH + ':m0038'


def valid(assertion, paragraphs):
    """Accept only the attested direction and exact 從伯 wording in Jinshu 76."""
    q = assertion.get('qualifiers', {})
    binding = q.get('source_clause_binding', {})
    k = q.get('kinship_structure', {})
    hit = paragraphs.get(PARAGRAPH)
    if not hit:
        return False
    chapter, paragraph = hit
    text = paragraph.get('text', '')
    mentions = {m.get('id'): m for m in paragraph.get('mentions', [])}
    subject = mentions.get(SUBJECT_MENTION)
    obj = mentions.get(OBJECT_MENTION)
    if (chapter != CHAPTER or paragraph.get('id') != PARAGRAPH
            or assertion.get('id') != 'a-jinshu076-wangbiaozhi-congbo-wangdao'
            or assertion.get('predicate') != 'agnatic_senior_kin'
            or assertion.get('status') != 'source_attested'
            or assertion.get('subject_person_id') != SUBJECT
            or assertion.get('object_person_id') != OBJECT
            or set(q) != {'source_term', 'kinship_structure', 'source_clause_binding'}
            or q.get('source_term') != '從伯導'
            or k != {'lineage': 'paternal', 'generation_difference': -1,
                     'collateral': True, 'distance': None,
                     'common_ancestor_person_id': None, 'subject_relative_age': 'unknown'}
            or set(binding) != {'pattern', 'subject_person_mention_id',
                                'object_person_mention_id', 'start', 'end', 'surface'}
            or binding.get('pattern') != 'jinshu076_congbo_subject_to_senior'
            or binding.get('subject_person_mention_id') != SUBJECT_MENTION
            or binding.get('object_person_mention_id') != OBJECT_MENTION
            or (binding.get('start'), binding.get('end'), binding.get('surface')) != (36, 39, '從伯導')
            or not subject or subject.get('kind') != 'person' or subject.get('person_id') != SUBJECT
            or not obj or obj.get('kind') != 'person' or obj.get('person_id') != OBJECT
            or subject.get('surface') != '彪之' or obj.get('surface') != '導'
            or (subject.get('start'), subject.get('end')) != (0, 2)
            or (obj.get('start'), obj.get('end')) != (38, 39)
            or text[36:39] != '從伯導'
            or not assertion.get('evidence')):
        return False
    for e in assertion['evidence']:
        if (e.get('work_id') != 'w-jinshu' or e.get('book_id') != 'b-jinshu-076'
                or e.get('source_id') != 's-jinshu-076-wangbiaozhi'
                or e.get('chapter_id') != CHAPTER or e.get('paragraph_id') != PARAGRAPH
                or e.get('subject_person_mention_id') != SUBJECT_MENTION
                or e.get('object_person_mention_id') != OBJECT_MENTION
                or not isinstance(e.get('quote'), str) or not e['quote']
                or not any(text.startswith(e['quote'], i) and i <= subject['start']
                           and obj['end'] <= i + len(e['quote'])
                           for i in range(len(text) + 1))):
            return False
    return True
