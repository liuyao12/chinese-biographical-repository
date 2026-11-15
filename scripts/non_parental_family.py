"""Source-bound care and ritual succession do not create biological parentage."""


def non_parental_relation_valid(assertion, paragraphs, assertions=None):
    if assertion.get('id') == 'a-song051-p014-p017-raised-by-yunfu-yin':
        q = assertion.get('qualifiers', {})
        binding = q.get('source_unit_binding', {})
        expected = {'source_term': '殷養女雲敷', 'source_unit_binding': {
            'kind': 'fixed_wyd_song051_p014_p017_family_batch',
            'case': 'raised-by-yunfu-yin',
            'raw_sha256': 'aa7b16d610871f77b747adbe0edb84f8775e1d404140a1e3f6284dccd11aaa45'},
            'interpretation_note': '保留「養女」原稱及殷為養育者；不判定是否符合任何法律收養制度，不推生母或生父。',
            'care_basis': 'source_named_foster_daughter', 'source_relationship': '養女',
            'source_child_sex': 'female', 'legal_adoption_status': 'not_stated',
            'biological_parentage_inference': 'not_inferred'}
        if (assertion.get('predicate') != 'raised_by'
                or assertion.get('status') != 'source_attested'
                or assertion.get('subject_person_id') != 'mhf_ukx_zs1'
                or assertion.get('object_person_id') != '9vj_md6_8sx'
                or q != expected or len(assertion.get('evidence', [])) != 1):
            return False
        e = assertion['evidence'][0]
        hit = paragraphs.get(e.get('paragraph_id'))
        if not hit or hit[0] != e.get('chapter_id') or e.get('quote') != hit[1].get('text'):
            return False
        mentions = {m['id']: m for m in hit[1].get('mentions', [])}
        child = mentions.get(e.get('subject_person_mention_id'))
        carer = mentions.get(e.get('object_person_mention_id'))
        term = expected['source_term']
        text = hit[1]['text']
        return (hit[0] == 'c-songshu-051-wyd1739-zongshi'
                and e.get('paragraph_id') == hit[0] + ':p017'
                and child is not None and child.get('person_id') == assertion['subject_person_id']
                and child.get('surface') == '雲敷'
                and carer is not None and carer.get('person_id') == assertion['object_person_id']
                and carer.get('surface') == '殷'
                and text.count(term) == 1 and text.startswith(term, text.index(term))
                and text[text.index(term) + len('殷養女'):text.index(term) + len(term)] == '雲敷')

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
    child_kind_ok = bool(child) and (child.get('kind') == 'person' or
                                     (child.get('kind') == 'pronoun' and
                                      q.get('care_basis') in ('explicit_yang', 'speaker_recalls_rearing')))
    child_person_id = child.get('person_id') if child else None
    other_person_id = other.get('person_id') if other else None
    if (not isinstance(term, str) or not term or term not in text
            or not child_kind_ok or not other or other.get('kind') != 'person'
            or not isinstance(child_person_id, str) or not child_person_id
            or not isinstance(other_person_id, str) or not other_person_id
            or child_person_id != assertion.get('subject_person_id')
            or other_person_id != assertion.get('object_person_id')
            or child_person_id == other_person_id):
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
