"""Bind junior-generation collateral claims and source-scoped sibling ordinals."""


def agnatic_senior_kin_valid(assertion, paragraphs):
    if assertion.get('qualifiers', {}).get('source_clause_binding', {}).get('rule') == 'complete_received_kinship_unit':
        try:from scripts.received_unit_kinship import valid as unit_relation_valid
        except ImportError:from received_unit_kinship import valid as unit_relation_valid
        return unit_relation_valid(assertion, paragraphs)
    # Position-bound close-family clauses; retain all older grammar contracts.
    if assertion.get('qualifiers', {}).get('source_clause_binding', {}).get('rule', '').startswith('close_family_'):
        try:
            from scripts.biography_close_family import valid as close_family_valid
        except ImportError:
            from biography_close_family import valid as close_family_valid
        return close_family_valid(assertion, paragraphs)

    if assertion.get('qualifiers', {}).get('source_clause_binding', {}).get('kind') == 'senior_dead_then_congzi_named_junior':
        try:
            from scripts.song047_collateral_care import valid
        except ImportError:
            from song047_collateral_care import valid
        return valid(assertion, paragraphs)
    q = assertion.get('qualifiers', {})
    k = q.get('kinship_structure', {})
    if (not isinstance(k, dict) or set(k) != {'lineage', 'generation_difference', 'collateral',
            'distance', 'common_ancestor_person_id', 'subject_relative_age'}):
        return False
    if (assertion.get('predicate') != 'agnatic_senior_kin'
            or k.get('lineage') != 'paternal' or type(k.get('generation_difference')) is not int
            or k['generation_difference'] != -1 or k.get('collateral') is not True
            or 'distance' not in k or k['distance'] is not None
            or 'common_ancestor_person_id' not in k or k['common_ancestor_person_id'] is not None
            or k.get('subject_relative_age') != 'unknown' or not assertion.get('evidence')):
        return False
    for e in assertion['evidence']:
        hit = paragraphs.get(e.get('paragraph_id'))
        if not hit or e.get('chapter_id') != hit[0]:
            return False
        p = hit[1]; text = p.get('text', ''); mentions = {m['id']: m for m in p.get('mentions', [])}
        child = mentions.get(e.get('subject_person_mention_id'))
        senior = mentions.get(e.get('object_person_mention_id'))
        term = q.get('source_term', '')
        if (not child or not senior or child.get('kind') != 'person' or senior.get('kind') != 'person'
                or child.get('person_id') != assertion.get('subject_person_id')
                or senior.get('person_id') != assertion.get('object_person_id')):
            return False
        binding = q.get('source_clause_binding')
        if binding is not None:
            # Explicit biographical subject + courtesy name + senior + 從子也.
            # Identity is bound by mention IDs; never inferred from equal names.
            courtesy = mentions.get(binding.get('courtesy_name_mention_id')) if isinstance(binding, dict) else None
            if (set(q) != {'source_term', 'kinship_structure', 'source_clause_binding'}
                    or not isinstance(binding, dict)
                    or set(binding) != {'pattern', 'courtesy_name_mention_id'}
                    or binding.get('pattern') != 'biographical_subject_courtesy_senior_congzi'
                    or not courtesy or courtesy.get('kind') != 'person'
                    or courtesy.get('person_id') != child['person_id']
                    or child['person_id'] == senior['person_id']
                    or text[child['start']:child['end']] != child['surface']
                    or text[courtesy['start']:courtesy['end']] != courtesy['surface']
                    or text[senior['start']:senior['end']] != senior['surface']
                    or text[child['end']:courtesy['start']] != '字'
                    or courtesy['end'] != senior['start']
                    or term != senior['surface'] + '從子也'
                    or text[senior['start']:senior['end'] + 3] != term):
                return False
            end = senior['end'] + 3
            local = [m for m in p.get('mentions', []) if m.get('kind') == 'person'
                     and child['start'] <= m['start'] < end]
            if {m['id'] for m in local} != {child['id'], courtesy['id'], senior['id']}:
                return False
            quote = e.get('quote', '')
            if not quote or not any(text.startswith(quote, i) and i <= child['start']
                                    and end <= i + len(quote) for i in range(len(text))):
                return False
            continue
        if term not in ('從子' + child['surface'], '族子' + child['surface']):
            return False
        start = child['start'] - 2
        preceding = [m for m in p.get('mentions', []) if m.get('kind') == 'person'
                     and m['end'] <= start]
        local = max(preceding, key=lambda m: m['end'], default=None)
        if (start < 0 or text[start:child['end']] != term or not local
                or local.get('person_id') != senior['person_id']
                or text[local['end']:start] not in ('舉其', '有', '其', '之', '')):
            return False
        quote = e.get('quote', '')
        if not quote or not any(text.startswith(quote, i) and i <= senior['start']
                                and child['end'] <= i + len(quote) for i in range(len(text))):
            return False
    return True


def source_sibling_group_valid(assertion, paragraphs, person_ids, parse_number):
    q = assertion.get('qualifiers', {}); group = q.get('source_sibling_group'); order = q.get('relative_birth_order', {})
    if (not isinstance(group, dict) or assertion.get('predicate') not in ('brother', 'sister')
            or order.get('ordinal_scope') != 'reported_sibling_group'
            or order.get('group_id') != group.get('id') or not group.get('id')
            or group.get('human_reviewed') is not False):
        return False
    members = group.get('member_person_ids', []); roles = group.get('member_roles', [])
    count = group.get('reported_count'); number = group.get('source_number')
    prefix = {'reported_sisters': '姊妹', 'reported_brothers': '兄弟'}.get(group.get('count_scope'))
    term = group.get('source_term')
    if (not prefix or type(count) is not int or count < 2 or parse_number(number) != count
            or term != prefix + str(number) + '人' or not isinstance(members, list)
            or not all(isinstance(m, str) for m in members)
            or len(members) != count or len(set(members)) != count
            or not set(members) <= set(person_ids) or not isinstance(roles, list)
            or not all(isinstance(role, dict) for role in roles) or len(roles) != count
            or {r.get('person_id') for r in roles} != set(members)
            or not {assertion.get('subject_person_id'), assertion.get('object_person_id')} <= set(members)):
        return False
    anchor = group.get('source_anchor', {}); hit = paragraphs.get(anchor.get('paragraph_id'))
    if not hit:
        return False
    p = hit[1]; text = p.get('text', ''); a, b = anchor.get('start'), anchor.get('end')
    if (type(a) is not int or type(b) is not int or not 0 <= a < b <= len(text)
            or anchor.get('surface') != term or text[a:b] != term
            or not any(e.get('paragraph_id') == p['id'] and e.get('chapter_id') == hit[0]
                       and isinstance(e.get('quote'), str) and e['quote'] in text and term in e['quote']
                       for e in assertion.get('evidence', []))):
        return False
    mentions = {m['id']: m for m in p.get('mentions', [])}; values = {}
    for role in roles:
        m = mentions.get(role.get('person_mention_id')); word = role.get('source_term', '')
        ordinal = role.get('ordinal'); position = role.get('position')
        if (not m or m.get('kind') != 'person' or m.get('person_id') != role.get('person_id')
                or not word or not text.startswith(word, m['start'])
                or m['end'] > m['start'] + len(word)
                or role.get('interpretation_status') not in ('source_attested', 'contextual_provisional')):
            return False
        if word == '后最長':
            valid = type(ordinal) is int and ordinal == 1 and position == 'eldest'
        elif word.startswith('第') and word.endswith('者'):
            valid = (type(ordinal) is int and parse_number(word[1:-1]) == ordinal
                     and 1 <= ordinal <= count and position == 'unspecified')
        elif word == '中者':
            valid = ordinal is None and position == 'unspecified'
        elif word == '小者':
            valid = (ordinal is None and position == 'youngest'
                     and role['interpretation_status'] == 'contextual_provisional')
        else:
            valid = False
        if not valid:
            return False
        values[role['person_id']] = (ordinal, position)
    for direction in ('older', 'younger'):
        pid = order.get(direction + '_person_id')
        if pid not in values or (order.get(direction + '_ordinal'), order.get(direction + '_position')) != values[pid]:
            return False
    return True
