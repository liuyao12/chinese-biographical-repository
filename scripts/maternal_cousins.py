"""母系姨表稱謂保存原路徑；不替未名母親或外祖指定身份。"""


def maternal_cousin_valid(a, paragraphs):
    binding_kind = a.get('qualifiers', {}).get('source_clause_binding', {}).get('kind')
    if binding_kind == 'jinshu073_wushen_yuxi_older_maternal_cousin':
        return jinshu073_wushen_yuxi_valid(a, paragraphs)
    if binding_kind == 'biography_subject_maternal_aunt_older_cousin':
        try:
            from scripts.song047_collateral_care import valid
        except ImportError:
            from song047_collateral_care import valid
        return valid(a, paragraphs)
    q = a.get('qualifiers', {}); k = q.get('kinship_structure', {})
    if (a.get('predicate') != 'maternal_cousin' or q.get('source_term') != '姨弟'
            or k.get('lineage') != 'maternal' or k.get('generation_difference') != 0
            or k.get('collateral') is not True or k.get('maternal_path') != 'mother_sister_son'
            or k.get('distance') is not None or k.get('common_ancestor_person_id') is not None
            or k.get('subject_relative_age') != 'younger' or not a.get('evidence')):
        return False
    order = q.get('relative_birth_order', {})
    if (order.get('older_person_id') != a.get('object_person_id')
            or order.get('younger_person_id') != a.get('subject_person_id')
            or order.get('scope') != 'maternal_cousins' or order.get('operator') != 'lt'
            or order.get('older_ordinal') is not None or order.get('younger_ordinal') is not None):
        return False
    for e in a['evidence']:
        hit = paragraphs.get(e.get('paragraph_id'))
        if not hit or not e.get('quote') or e['quote'] not in hit[1]['text']:
            return False
        p = hit[1]; ms = {m['id']: m for m in p['mentions']}
        sub, obj = ms.get(e.get('subject_person_mention_id')), ms.get(e.get('object_person_mention_id'))
        if (not sub or not obj or sub.get('kind') != 'person' or obj.get('kind') != 'person'
                or sub.get('person_id') != a.get('subject_person_id') or obj.get('person_id') != a.get('object_person_id')
                or sub['start'] >= obj['start'] or not p['text'][obj['end']:].startswith('姨弟')):
            return False
        if not any(i <= sub['start'] and obj['end'] + 2 <= i + len(e['quote'])
                   for i in range(len(p['text'])) if p['text'].startswith(e['quote'], i)):
            return False
    return True


def jinshu073_wushen_yuxi_valid(a, paragraphs):
    """Validate only Jinshu 73's explicit 武沈—庾希 從母兄 clause."""
    try:
        q = a['qualifiers']; k = q['kinship_structure']; order = q['relative_birth_order']
        binding = q['source_clause_binding']; e, = a['evidence']
        cid, p = paragraphs[e['paragraph_id']]; text = p['text']; ms = {m['id']: m for m in p['mentions']}
        subject = ms[e['subject_person_mention_id']]; obj = ms[e['object_person_mention_id']]
        clause = '希之從母兄也'
        start, end = binding['start'], binding['end']
        return (
            a.get('id') == 'a-jinshu073-wushen-yuxi-maternal-cousin'
            and a.get('predicate') == 'maternal_cousin'
            and a.get('status') == 'source_attested'
            and a.get('subject_person_id') == '9c5_a31_807'
            and a.get('object_person_id') == '4qr_wrk_3vd_DA'
            and a.get('human_reviewed') is False
            and set(q) == {'source_term', 'kinship_structure', 'relative_birth_order', 'source_clause_binding'}
            and q['source_term'] == clause
            and set(k) == {'lineage', 'generation_difference', 'collateral', 'distance', 'common_ancestor_person_id', 'subject_relative_age', 'maternal_path'}
            and k == {'lineage': 'maternal', 'generation_difference': 0, 'collateral': True,
                      'distance': None, 'common_ancestor_person_id': None,
                      'subject_relative_age': 'older', 'maternal_path': 'mother_sister_son'}
            and set(order) == {'operator', 'scope', 'older_person_id', 'younger_person_id', 'older_ordinal', 'younger_ordinal'}
            and order == {'operator': 'lt', 'scope': 'maternal_cousins',
                          'older_person_id': '9c5_a31_807', 'younger_person_id': '4qr_wrk_3vd_DA',
                          'older_ordinal': None, 'younger_ordinal': None}
            and set(binding) == {'kind', 'start', 'end', 'surface'}
            and binding['kind'] == 'jinshu073_wushen_yuxi_older_maternal_cousin'
            and binding['surface'] == clause
            and type(start) is int and type(end) is int
            and e['work_id'] == 'w-jinshu' and e['book_id'] == 'b-jinshu-073'
            and e['chapter_id'] == cid == 'c-jinshu-073-yu-yi-bing-tiao'
            and e['source_id'] == 's-jinshu-073-yu-yi-bing-tiao'
            and e['paragraph_id'] == 'c-jinshu-073-yu-yi-bing-tiao:line113'
            and e['quote'] == text
            and subject['kind'] == obj['kind'] == 'person'
            and subject['person_id'] == a['subject_person_id']
            and obj['person_id'] == a['object_person_id']
            and subject['surface'] == '武沈' and obj['surface'] == '希'
            and e['subject_person_mention_id'] == 'c-jinshu-073-yu-yi-bing-tiao:line113:m0077'
            and e['object_person_mention_id'] == 'c-jinshu-073-yu-yi-bing-tiao:line113:m0080'
            and 0 <= start < end <= len(text)
            and start == obj['start'] and end == obj['end'] + len('之從母兄也')
            and text[start:end] == clause
            and text[subject['end']:obj['start']] == '，'
            and text[start:end].endswith('之從母兄也')
            and text.startswith('故青州刺史武沈，希之從母兄也，潛餉給希經年。', subject['start'] - len('故青州刺史'))
        )
    except (KeyError, TypeError, ValueError):
        return False
