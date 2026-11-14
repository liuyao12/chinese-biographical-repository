"""Narrow source binding for Xun Qi's named 族父 Xun Yin in Sanguozhi 10."""

CHAPTER = 'c-sanguozhi-010-xunyu-xunyou-jiaxu'
PARAGRAPH = CHAPTER + ':xunyou:u004'
SUBJECT = 'a1f_f17_ccb_A'
OBJECT = '215_e1c_3e3'
SUBJECT_MENTION = PARAGRAPH + ':m0047'
OBJECT_MENTION = PARAGRAPH + ':m0054'
CLAUSE = '荀氏家傳曰衢子祈字伯旗與族父愔俱著名'
TERM = '族父愔'
LAYER_QUOTE = '荀氏家傳曰衢子祈字伯旗與族父愔俱著名祈與孔融論肉刑愔與孔融論聖人優劣並在融集祈位至濟隂太守愔後徴有道至丞相祭酒'


def valid(assertion, paragraphs):
    """Accept only the exact two-endpoint 族父 claim in the Xunshi-jiazhuan layer."""
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
    start = text.find(CLAUSE)
    term_start = text.find(TERM, start) if start >= 0 else -1
    layer = next((x for x in paragraph.get('received_text_layers', [])
                  if x.get('start') == 40 and x.get('end') == 95), None)
    if (chapter != CHAPTER or paragraph.get('id') != PARAGRAPH
            or paragraph.get('text_layer') != 'witness_appended_pei_songzhi_note'
            or not layer or layer.get('layer') != 'ancient_quoted_text'
            or layer.get('authority') != '荀氏家傳' or layer.get('quote') != LAYER_QUOTE
            or assertion.get('id') != 'a-xunyou11-013'
            or assertion.get('predicate') != 'agnatic_senior_kin'
            or assertion.get('status') != 'source_attested'
            or assertion.get('subject_person_id') != SUBJECT
            or assertion.get('object_person_id') != OBJECT
            or set(q) != {'source_term', 'kinship_structure', 'source_clause_binding'}
            or q.get('source_term') != TERM
            or k != {'lineage': 'paternal', 'generation_difference': -1,
                     'collateral': True, 'distance': None,
                     'common_ancestor_person_id': None, 'subject_relative_age': 'unknown'}
            or set(binding) != {'pattern', 'subject_person_mention_id',
                                'object_person_mention_id', 'start', 'end', 'surface'}
            or binding.get('pattern') != 'sanguozhi010_zu_fu_subject_to_senior'
            or binding.get('subject_person_mention_id') != SUBJECT_MENTION
            or binding.get('object_person_mention_id') != OBJECT_MENTION
            or (binding.get('start'), binding.get('end'), binding.get('surface')) != (term_start, term_start + len(TERM), TERM)
            or start != 40 or term_start != 52
            or text[start:start + len(CLAUSE)] != CLAUSE
            or not subject or subject.get('kind') != 'person' or subject.get('person_id') != SUBJECT
            or not obj or obj.get('kind') != 'person' or obj.get('person_id') != OBJECT
            or subject.get('surface') != '祈' or obj.get('surface') != '愔'
            or (subject.get('start'), subject.get('end')) != (47, 48)
            or (obj.get('start'), obj.get('end')) != (54, 55)
            or not assertion.get('evidence')):
        return False
    for e in assertion['evidence']:
        if (e.get('work_id') != 'w-sanguozhi' or e.get('book_id') != 'b-sanguozhi-010'
                or e.get('source_id') != 's-sanguozhi-010-xunyu-xunyou-jiaxu'
                or e.get('chapter_id') != CHAPTER or e.get('paragraph_id') != PARAGRAPH
                or e.get('subject_person_mention_id') != SUBJECT_MENTION
                or e.get('object_person_mention_id') != OBJECT_MENTION
                or e.get('quote') != LAYER_QUOTE
                or e.get('quoted_source_title') != '荀氏家傳'
                or e.get('text_layer') != 'ancient_quoted_text'):
            return False
    refs = assertion.get('references', [])
    return (len(refs) == 1
            and refs[0].get('title') == '《爾雅·釋親》'
            and refs[0].get('quote') == '父之從祖晜弟為族父。'
            and refs[0].get('url') == 'https://zh.wikisource.org/w/index.php?title=釋草_(爾雅)&oldid=8758864#釋親_第四'
            and refs[0].get('source_revision') == '8758864'
            and refs[0].get('scope') == 'kinship_term_interpretation_only')
