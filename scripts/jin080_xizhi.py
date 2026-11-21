"""《晉書》卷八十主傳的親屬語、未就與篇終主語。"""

CHAPTER = 'c-jinshu-080-wangxizhi-family'
PERSON = '326_faf_cd3'
ENDING = '年五十九卒，贈金紫光祿大夫。諸子遵父先旨，固讓不受。'


def end_subject_valid(context, evidence, person_id, chapter):
    if person_id != PERSON or chapter.get('id') != CHAPTER or chapter['source'].get('revision_id') != 2603570:
        return False
    if evidence.get('chapter_id') != CHAPTER or evidence.get('source_id') != chapter.get('source_id'):
        return False
    expected = [f'{CHAPTER}:line{n:03}' for n in (72, 74, 76, 78, 80, 82)]
    ps = chapter['paragraphs']
    first = next((i for i,p in enumerate(ps) if p['id'] == expected[0]), -1)
    span = ps[first:first+len(expected)]
    if [p['id'] for p in span] != expected:
        return False
    named = next((m for m in span[0]['mentions'] if m['id'] == context.get('person_mention_id')), None)
    ref = next((r for r in chapter['annotation'].get('person_reference_occurrences', []) if r['id'] == context.get('reference_id')), None)
    return bool(named and ref and context.get('kind') == 'jin080_biography_end'
                and context.get('paragraph_id') == expected[0] and context.get('intervening_paragraph_ids') == expected[1:-1]
                and named['person_id'] == person_id and named.get('kind') == 'person' and named['surface'] == '羲之'
                and span[0]['text'].startswith('初，羲之既優遊無事，與吏部郎謝萬書曰')
                and span[-2]['text'].endswith('萬不能用，果敗。') and span[-1]['text'] == ENDING
                and evidence.get('paragraph_id') == expected[-1] and evidence.get('quote') == ENDING
                and ref['paragraph_id'] == expected[-1] and ref['person_id'] == person_id and ref['surface'] == '父'
                and ref['start'] == ENDING.index('父') and ref['end'] == ref['start'] + 1
                and ref['referent_role'] == 'third_person' and ref['quote'] == '諸子遵父先旨')


def collateral_valid(a, paragraphs):
    term = a.get('qualifiers', {}).get('source_term')
    people = {'司徒導之從子也': ('導', '7r6_k52_qji_ABAA'), '從伯敦、導': ('敦', '39o_b6y_n74')}
    if (term not in people or a.get('predicate') != 'agnatic_senior_kin' or a.get('subject_person_id') != PERSON
            or a.get('qualifiers', {}).get('kinship_structure') != dict(lineage='paternal',generation_difference=-1,
               collateral=True,distance=None,common_ancestor_person_id=None,subject_relative_age='unknown') or len(a.get('evidence', [])) != 1):
        return False
    name, person = people[term]
    evidence = a['evidence'][0]
    chapter_id, p = paragraphs.get(evidence.get('paragraph_id'), (None, {}))
    if chapter_id != CHAPTER or p.get('id') != CHAPTER + ':line014' or a.get('object_person_id') != person:
        return False
    ms = {m['id']: m for m in p['mentions']}
    junior = ms.get(evidence.get('subject_person_mention_id'), {})
    senior = ms.get(evidence.get('object_person_mention_id'), {})
    text = p['text']
    return (text.startswith('王羲之，字逸少，司徒導之從子也。') and term in text and evidence.get('quote') == text
            and junior.get('person_id') == PERSON and junior.get('surface') == '王羲之' and junior['start'] == 0
            and senior.get('person_id') == person and senior.get('surface') == name and senior['start'] == text.index(term) + term.index(name))


def unassumed_valid(proposal, chapter):
    p = next((p for p in chapter['paragraphs'] if p['id'] == CHAPTER + ':line016'), None)
    options = {'侍中': ('召為', '皆不就'), '吏部尚書': ('召為', '皆不就'), '護軍將軍': ('復授', '推遷不拜')}
    title = proposal.get('title')
    if (not p or chapter.get('id') != CHAPTER or chapter['source'].get('revision_id') != 2603570 or title not in options
            or proposal.get('person_id') != PERSON or proposal.get('outcome') != 'not_assumed'
            or proposal.get('proposal_kind') != 'unassumed_appointment' or proposal.get('non_assumption_kind') != 'did_not_take_up'
            or proposal.get('appointment_stage') != 'appointment' or len(proposal.get('evidence', [])) != 1):
        return False
    e = proposal['evidence'][0]
    if (not all(e.get(k) == chapter[k] for k in ('book_id', 'work_id','source_id'))
            or e.get('chapter_id') != CHAPTER or e.get('paragraph_id') != p['id'] or e.get('quote') != p['text']
            or not any(m['id'] == proposal.get('person_mention_id') and m.get('person_id') == PERSON for m in p['mentions'])
            or '羲之既少有美譽，朝廷公卿皆愛其才器，頻召為侍中、吏部尚書，皆不就。復授護軍將軍，又推遷不拜。' not in p['text']):
        return False
    for key, word in zip(('role_anchor', 'appointment_anchor', 'non_assumption_anchor'), (title, *options[title])):
        start = p['text'].index(word)
        if proposal.get(key) != dict(paragraph_id=p['id'],start=start,end=start+len(word),surface=word):
            return False
    return True
