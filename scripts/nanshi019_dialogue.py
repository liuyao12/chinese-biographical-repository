"""核對謝澹附傳中須分辨問者、答者、被引者及旁系長輩的句子。"""
import hashlib


CHAPTER = 'c-nanshi-019-dan19'
SOURCE = 's-nanshi-019-dan19-ws1531762'
PARAGRAPHS = {
    'p001': 'd36ce545c3816a9ce851ea141ae6636d6396c0dad2b396c817a232ed29b4070b',
    'p003': '2575f45acdd8c246d939428e78f6a07d84cb8886258754d5e12e259b2456c216',
    'p004': '7077cb5f0cdd8f08a5058eec00913dc3d8cfb8bd80eb6a6bbe78edb6f6843293',
}


def fixed_paragraph(paragraph, suffix):
    return (paragraph.get('id') == CHAPTER + ':' + suffix
            and hashlib.sha256(paragraph['text'].encode()).hexdigest() == PARAGRAPHS[suffix]
            and paragraph.get('source_position', {}).get('revision_id') == 1531762)


def occurrence(rows, paragraph, phrase, surface):
    text = paragraph['text']
    assert text.count(phrase) == 1 and phrase.count(surface) == 1
    start = text.index(phrase) + phrase.index(surface)
    match, = (row for row in rows if row['surface'] == surface and row['start'] == start
              and row['end'] == start + len(surface))
    return match


def age_anchor(age, chapter):
    """返回實際答者的姓名錨，或被引人物的非姓名錨。"""
    try:
        if chapter['id'] != CHAPTER or chapter['source_id'] != SOURCE:
            return None
        paragraph, = (p for p in chapter['paragraphs'] if p['id'] == CHAPTER + ':p003')
        if not fixed_paragraph(paragraph, 'p003'):
            return None
        binding = age['reported_dialogue']
        roles = paragraph['mentions']
        if binding['role'] == 'answer':
            subject = occurrence(roles, paragraph, '澹問晦年', '晦')
            speaker = subject
            term, number, years = '答曰三十五', '三十五', 35
        elif binding['role'] == 'recollection':
            refs = [r for r in chapter['annotation']['person_reference_occurrences']
                    if r['paragraph_id'] == paragraph['id'] and r['referent_role'] == 'third_person']
            subject = occurrence(refs, paragraph, '昔荀中郎年二十九', '荀中郎')
            speaker = occurrence(roles, paragraph, '澹笑曰', '澹')
            term, number, years = '年二十九', '二十九', 29
        else:
            return None
        e, = age['evidence']
        key = 'person_reference_id' if binding['role'] == 'recollection' else 'person_mention_id'
        if (binding['speaker_mention_id'] == speaker['id'] and e.get(key) == subject['id']
                and not ({'person_reference_id','person_mention_id'} - {key}) & e.keys()
                and age['person_id'] == subject['person_id'] and age['source_number'] == number
                and age['source_term'] == term and age['value'] == years and type(age['value']) is int
                and age['age_context'] == {'kind': 'during_life'} and age['date_expression'] is None
                and e['work_id'] == 'w-nanshi' and e['book_id'] == 'b-nanshi-019'
                and e['source_id'] == SOURCE and e['chapter_id'] == CHAPTER
                and e['paragraph_id'] == paragraph['id'] and e['quote'] == paragraph['text']):
            return subject
    except (AssertionError, KeyError, TypeError, ValueError):
        return None
    return None


def collateral_valid(assertion, paragraphs):
    frames = {
        'opening_congshu': ('p001', '晦從叔也', '晦', '澹字景恆', '澹', '從叔'),
        'visitor_congzi': ('p003', '從子晦爲荊州', '晦', '詣澹別', '澹', '從子晦'),
        'listener_congzi': ('p004', '從子瞻曰', '瞻', '澹常以爲憂', '澹', '從子瞻'),
    }
    try:
        q = assertion['qualifiers']
        suffix, junior_phrase, junior_form, senior_phrase, senior_form, term = frames[q['nanshi019_role']]
        e, = assertion['evidence']
        cid, paragraph = paragraphs[e['paragraph_id']]
        if cid != CHAPTER or not fixed_paragraph(paragraph, suffix):
            return False
        junior = occurrence(paragraph['mentions'], paragraph, junior_phrase, junior_form)
        senior = occurrence(paragraph['mentions'], paragraph, senior_phrase, senior_form)
        return (assertion['predicate'] == 'agnatic_senior_kin' and assertion['status'] == 'source_attested'
                and assertion['subject_person_id'] == junior['person_id']
                and assertion['object_person_id'] == senior['person_id'] != junior['person_id']
                and e['subject_person_mention_id'] == junior['id'] and e['object_person_mention_id'] == senior['id']
                and q['source_term'] == term and e['quote'] == paragraph['text']
                and e['source_id'] == SOURCE and e['book_id'] == 'b-nanshi-019' and e['work_id'] == 'w-nanshi'
                and q['kinship_structure'] == dict(lineage='paternal',generation_difference=-1,collateral=True,
                    distance=None,common_ancestor_person_id=None,subject_relative_age='unknown'))
    except (KeyError, TypeError, ValueError, AssertionError):
        return False
