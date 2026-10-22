"""Source-bound care and ritual succession do not create biological parentage."""


def non_parental_relation_valid(assertion, paragraphs, assertions=None):
    if assertion.get('qualifiers', {}).get('source_clause_binding', {}).get('kind') == 'biography_family_clause':
        try:
            from scripts.biography_family_clause import valid
        except ImportError:
            from biography_family_clause import valid
        return valid(assertion, paragraphs, assertions or [])
    if isinstance(assertion.get('qualifiers'), dict) and isinstance(assertion['qualifiers'].get('source_clause_binding'), dict) and assertion['qualifiers']['source_clause_binding'].get('kind') == 'biography_head_birth_mother_dies_grandmother_care':
        try:
            from scripts.biography_orphan_grandmother_care import valid
        except ImportError:
            from biography_orphan_grandmother_care import valid
        return valid(assertion, paragraphs)

    if assertion.get("qualifiers", {}).get("succession_kind") == "biography_head_younger_brother_eldest_son_weisi":
        try:
            from scripts.biography_ritual_succession import valid
        except ImportError:
            from biography_ritual_succession import valid
        return valid(assertion, paragraphs, assertions or [])
    if assertion.get('qualifiers', {}).get('source_clause_binding', {}).get('kind') == 'congmu_weans_child_and_nurses_named_child':
        try:
            from scripts.song047_collateral_care import valid
        except ImportError:
            from song047_collateral_care import valid
        return valid(assertion, paragraphs)
    q = assertion.get('qualifiers', {})
    if q.get('succession_kind') == 'ji_named_predecessor':
        try:
            from scripts.song041_source_context import kin_clause_valid
        except ImportError:
            from song041_source_context import kin_clause_valid
        return kin_clause_valid(assertion, paragraphs, [])
    if q.get('succession_kind') == 'named_zusun_feng_hou':
        try:
            from scripts.historical_family_clauses import named_zusun_fenghou_valid
        except ImportError:
            from historical_family_clauses import named_zusun_fenghou_valid
        return named_zusun_fenghou_valid(assertion, paragraphs)
    evidence = assertion.get('evidence', [])
    if (assertion.get('predicate') not in ('raised_by', 'ritual_successor_of')
            or assertion.get('status') != 'source_attested'
            or assertion.get('human_reviewed') is not False
            or q.get('legal_adoption_status') != 'not_stated'
            or len(evidence) != 1):
        return False
    e = evidence[0]
    hit = paragraphs.get(e.get('paragraph_id'))
    if not hit or e.get('chapter_id') != hit[0] or e.get('quote') != hit[1].get('text'):
        return False
    p = hit[1]; text = p['text']; term = q.get('source_term')
    ms = {m['id']: m for m in p.get('mentions', [])}
    child = ms.get(e.get('subject_person_mention_id'))
    other = ms.get(e.get('object_person_mention_id'))
    if (not isinstance(term, str) or not term or term not in text
            or not child or not other or child.get('kind') != 'person' or other.get('kind') != 'person'
            or child.get('person_id') != assertion.get('subject_person_id')
            or other.get('person_id') != assertion.get('object_person_id')
            or child['person_id'] == other['person_id']):
        return False
    starts = [i for i in range(len(text)) if text.startswith(term, i)]
    if not any(i <= other['start'] < other['end'] <= i + len(term) for i in starts):
        return False
    if assertion['predicate'] == 'ritual_successor_of':
        keys = {'source_term', 'succession_kind', 'legal_adoption_status', 'parentage_inference'}
        if set(q) != keys or q['parentage_inference'] != 'not_inferred':
            return False
        terms = {'ji_named_relative': '繼叔父' + other['surface'],
                 'si_named_predecessor_hou': '嗣' + other['surface'] + '后'}
        return (term == terms.get(q.get('succession_kind'))
                and any(child['end'] <= i for i in starts))
    kind = q.get('care_basis')
    keys = {'source_term', 'care_basis', 'legal_adoption_status'}
    if kind == 'speaker_recalls_rearing':
        keys.add('speaker_identity_mention_id')
    if set(q) != keys:
        return False
    if kind == 'explicit_yang':
        return (child['surface'] == '之' and term == other['surface'] + '養之'
                and text[other['end']:child['start']] == '養')
    if kind == 'speaker_recalls_rearing':
        speaker = ms.get(q.get('speaker_identity_mention_id'))
        return (child['surface'] == '朕' and term == '撫育之勤，' + other['surface'] + '之仁也'
                and bool(speaker) and speaker.get('kind') == 'person'
                and speaker.get('person_id') == child['person_id'] and speaker['end'] <= child['start']
                and '詔曰' in text[speaker['end']:child['start']])
    if kind == 'welcomed_like_children':
        if term != other['surface'] + '迎與共居，恩同其子':
            return False
        before = text[:min(starts)]; a = before.rfind('二息'); b = before.find('，年各', a)
        return a >= 0 and b > a and a + 2 <= child['start'] < child['end'] <= b
    return False
