"""母系姨表稱謂保存原路徑；不替未名母親或外祖指定身份。"""


def maternal_cousin_valid(a, paragraphs):
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
