"""母系姨表稱謂保存原路徑；不替未名母親或外祖指定身份。"""


def maternal_cousin_valid(a, paragraphs):
    if a.get('qualifiers', {}).get('source_clause_binding', {}).get('kind') == 'song051_named_congmu_xiong':
        q = a.get('qualifiers', {}); k = q.get('kinship_structure', {}); order = q.get('relative_birth_order', {})
        if (a.get('predicate') != 'maternal_cousin' or q.get('source_term') != '道規從母兄'
                or k.get('lineage') != 'maternal' or k.get('generation_difference') != 0
                or k.get('collateral') is not True or k.get('maternal_path') != 'mother_sister_son'
                or k.get('distance') is not None or k.get('common_ancestor_person_id') is not None
                or k.get('subject_relative_age') != 'older' or not a.get('evidence')
                or order.get('older_person_id') != a.get('subject_person_id')
                or order.get('younger_person_id') != a.get('object_person_id')
                or order.get('scope') != 'maternal_cousins' or order.get('operator') != 'lt'
                or order.get('older_ordinal') is not None or order.get('younger_ordinal') is not None):
            return False
        binding = q['source_clause_binding']
        for e in a['evidence']:
            hit = paragraphs.get(e.get('paragraph_id'))
            if not hit or hit[0] != e.get('chapter_id') or not e.get('quote'):
                return False
            p = hit[1]; quote = p['text']; start = binding.get('start'); end = binding.get('end')
            import hashlib
            if (quote != e['quote'] or not quote.startswith('道規從母兄', start)
                    or end != start + len('道規從母兄')
                    or binding.get('paragraph_sha256') != hashlib.sha256(quote.encode()).hexdigest()
                    or binding.get('source_revision') != 'cbr-ai-transcription-sha256:aa7b16d610871f77b747adbe0edb84f8775e1d404140a1e3f6284dccd11aaa45'):
                return False
            ms = {m['id']: m for m in p.get('mentions', [])}
            sub, obj = ms.get(e.get('subject_person_mention_id')), ms.get(e.get('object_person_mention_id'))
            if (not sub or not obj or sub.get('person_id') != a.get('subject_person_id')
                    or obj.get('person_id') != a.get('object_person_id')
                    or sub.get('surface') != '遵' or obj.get('surface') != '道規'
                    or not (sub['start'] < start and obj['start'] == start)):
                return False
        return True
    if a.get('qualifiers', {}).get('source_clause_binding', {}).get('kind') == 'biography_subject_maternal_aunt_older_cousin':
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
