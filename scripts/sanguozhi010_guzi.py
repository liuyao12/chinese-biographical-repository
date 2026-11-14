"""Narrow source binding for Xun You's anonymous paternal-aunt child, Xin Tao."""

CHAPTER = 'c-sanguozhi-010-xunyu-xunyou-jiaxu'
PARAGRAPH = CHAPTER + ':xunyou:u016'
SUBJECT = '696_456_df6_AA'
OBJECT = '98a_aea_b7b'
SUBJECT_MENTION = PARAGRAPH + ':m0003'
OBJECT_MENTION = PARAGRAPH + ':m0006'
SOURCE_QUOTE = '魏書曰攸姑子辛韜曽問攸說太祖取冀州時事攸曰佐治為袁譚乞降王師自往平之吾何知焉自是韜及内外莫敢復問軍國事也'
CLAUSE = '攸姑子辛韜'


def valid(assertion, paragraphs):
    """Accept only the exact named endpoints and Wei Shu commentary layer in SGZ 10."""
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
    layer = next((x for x in paragraph.get('received_text_layers', [])
                  if x.get('start') == 0 and x.get('end') == 52), None)
    start = text.find(CLAUSE)
    if (chapter != CHAPTER or paragraph.get('id') != PARAGRAPH
            or paragraph.get('text_layer') != 'witness_appended_pei_songzhi_note'
            or not layer or layer.get('layer') != 'ancient_quoted_text'
            or layer.get('authority') != '魏書' or layer.get('quote') != SOURCE_QUOTE
            or text != SOURCE_QUOTE or start != 3
            or assertion.get('id') != 'a-xunyou11-014'
            or assertion.get('predicate') != 'paternal_aunt_child'
            or assertion.get('status') != 'source_attested'
            or assertion.get('subject_person_id') != SUBJECT
            or assertion.get('object_person_id') != OBJECT
            or set(q) != {'source_term', 'paternal_aunt_person_id', 'generation_difference',
                          'exact_distance', 'common_ancestor_person_id', 'subject_relative_age',
                          'source_clause_binding'}
            or q.get('source_term') != '姑子'
            or q.get('paternal_aunt_person_id') is not None
            or q.get('generation_difference') != 0
            or q.get('exact_distance') is not None
            or q.get('common_ancestor_person_id') is not None
            or q.get('subject_relative_age') != 'unknown'
            or set(binding) != {'pattern', 'subject_person_mention_id',
                                'object_person_mention_id', 'start', 'end', 'surface'}
            or binding.get('pattern') != 'sanguozhi010_gu_zi_subject_to_aunt_child'
            or binding.get('subject_person_mention_id') != SUBJECT_MENTION
            or binding.get('object_person_mention_id') != OBJECT_MENTION
            or (binding.get('start'), binding.get('end'), binding.get('surface')) != (3, 8, CLAUSE)
            or not subject or subject.get('kind') != 'person' or subject.get('person_id') != SUBJECT
            or subject.get('surface') != '攸' or (subject.get('start'), subject.get('end')) != (3, 4)
            or not obj or obj.get('kind') != 'person' or obj.get('person_id') != OBJECT
            or obj.get('surface') != '辛韜' or (obj.get('start'), obj.get('end')) != (6, 8)
            or not assertion.get('evidence')):
        return False
    for e in assertion['evidence']:
        if (e.get('work_id') != 'w-sanguozhi' or e.get('book_id') != 'b-sanguozhi-010'
                or e.get('source_id') != 's-sanguozhi-010-xunyu-xunyou-jiaxu'
                or e.get('chapter_id') != CHAPTER or e.get('paragraph_id') != PARAGRAPH
                or e.get('subject_person_mention_id') != SUBJECT_MENTION
                or e.get('object_person_mention_id') != OBJECT_MENTION
                or e.get('quote') != SOURCE_QUOTE
                or e.get('quoted_source_title') != '魏書'
                or e.get('text_layer') != 'ancient_quoted_text'):
            return False
    refs = assertion.get('references', [])
    return (len(refs) == 1
            and refs[0].get('title') == '《爾雅·釋親》'
            and refs[0].get('quotes') == ['父之姊妹為姑。', '姑之子為甥。']
            and refs[0].get('url') == 'https://zh.wikisource.org/w/index.php?title=釋草_(爾雅)&oldid=8758864#釋親_第四'
            and refs[0].get('source_revision') == '8758864'
            and refs[0].get('scope') == 'kinship_term_interpretation_only')
