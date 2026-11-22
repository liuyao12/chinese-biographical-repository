"""薛綜疏中儋萌妻父周京的原文與具名方向。"""
def valid(row, paragraphs):
    try:
        item, = row['evidence']
        chapter, paragraph = paragraphs[item['paragraph_id']]
        phrase = '九真太守儋萌為妻父周京作主人'
        text = paragraph['text']
        source = paragraph['source_position']
        mention = {m['id']: m for m in paragraph['mentions'] if m['kind']=='person'}
        subject = mention[item['subject_person_mention_id']]
        obj = mention[item['object_person_mention_id']]
        return (
            chapter == item['chapter_id'] == 'c-sanguozhi-053-xuezong'
            and paragraph['id'] == chapter+':line045'
            and source['revision_id'] == 2086397 and text.count(phrase) == 1
            and item['quote'] == text and row['predicate'] == 'father_in_law'
            and row['qualifiers']['source_term'] == '儋萌為妻父周京'
            and (subject['start'], subject['surface'], subject['person_id']) == (text.index(phrase)+4,'儋萌',row['subject_person_id'])
            and (obj['start'], obj['surface'], obj['person_id']) == (text.index(phrase)+9,'周京',row['object_person_id'])
        )
    except (KeyError, TypeError, ValueError):
        return False
