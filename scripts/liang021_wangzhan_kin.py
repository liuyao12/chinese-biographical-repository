"""Read the two differently expressed family roles in Wang Zhan's biography."""
CHAPTER = 'c-liangshu-021-wangzhan'
ZHAN = '7r6_k52_qji_ABAAAACAA'


def senior_valid(assertion, paragraphs):
    try:
        qualifier = assertion['qualifiers']
        evidence, = assertion['evidence']
        cid, paragraph = paragraphs[evidence['paragraph_id']]
        text = paragraph['text']
        if (cid != CHAPTER or evidence['chapter_id'] != cid or evidence['quote'] != text
                or assertion['subject_person_id'] != ZHAN
                or assertion['predicate'] != 'agnatic_senior_kin'
                or qualifier['source_term'] != '從父'
                or qualifier['kinship_structure'] != dict(
                    lineage='paternal', generation_difference=-1, collateral=True, distance=None,
                    common_ancestor_person_id=None, subject_relative_age='unknown')):
            return False
        people = {m['id']: m for m in paragraph['mentions'] if m['kind'] == 'person'}
        child = people[evidence['subject_person_mention_id']]
        senior = people[evidence['object_person_mention_id']]
        clause = '從父尚書僕射僧達聞而異之，謂瞻父曰'
        return (text.startswith('王瞻字思範') and child['person_id'] == ZHAN
                and child['start'] == 0 and child['surface'] == '王瞻' and text.count(clause) == 1
                and senior['person_id'] == assertion['object_person_id']
                and senior['surface'] == '僧達' and senior['start'] == text.index(clause) + 6)
    except (KeyError, ValueError, TypeError):
        return False


def wife_valid(assertion, evidence, chapter):
    try:
        clause = '瞻潔己爲政，妻子不免饑寒。'
        basis = assertion['qualifiers']['reading_basis']
        p = next(p for p in chapter['paragraphs'] if p['id'] == evidence['paragraph_id'])
        start = p['text'].index(clause)
        husband = next(m for m in p['mentions'] if m['id'] == basis['husband_mention_id'])
        wife = next(r for r in chapter['annotation']['person_reference_occurrences']
                    if r['id'] == basis['wife_reference_id'])
        return (chapter['id'] == CHAPTER and chapter['source']['revision_id'] == 1544250
                and evidence['chapter_id'] == CHAPTER and evidence['quote'] == p['text']
                and p['text'].count(clause) == 1 and assertion['predicate'] == 'spouse'
                and assertion['qualifiers']['source_term'] == '妻'
                and husband['person_id'] == assertion['subject_person_id'] == ZHAN
                and husband['start'] == start and husband['surface'] == '瞻'
                and wife['paragraph_id'] == p['id'] and wife['start'] == start + clause.index('妻')
                and wife['surface'] == '妻' and wife['referent_role'] == 'third_person'
                and wife['person_id'] == assertion['object_person_id'] != ZHAN
                and basis['source_quote'] == clause)
    except (KeyError, TypeError, ValueError, StopIteration):
        return False
