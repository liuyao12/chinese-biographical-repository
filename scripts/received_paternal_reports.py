"""核自敍的「六世祖」與傳主幼時所稱世父，保存傳述層及原文方向。"""
import re


def _received_endpoints(assertion, paragraphs):
    evidence = assertion.get('evidence', [])
    if len(evidence) != 1:
        return None
    e = evidence[0]
    hit = paragraphs.get(e.get('paragraph_id'))
    if not hit or hit[0] != e.get('chapter_id'):
        return None
    p = hit[1]
    text = p.get('text', '')
    if p.get('text_layer') != 'received_chapter' or text != e.get('quote'):
        return None
    marks = {m['id']: m for m in p.get('mentions', [])}
    endpoints = []
    for role in ('subject', 'object'):
        m = marks.get(e.get(role+'_person_mention_id'))
        if (not m or m.get('kind') != 'person' or not m.get('surface')
                or m.get('person_id') != assertion.get(role+'_person_id')
                or text[m['start']:m['end']] != m['surface']):
            return None
        endpoints.append(m)
    head, relative = endpoints
    if head['start'] != 0 or head['end'] >= relative['start'] or head['person_id'] == relative['person_id']:
        return None
    return text, head, relative


def reported_ancestry_valid(assertion, paragraphs, parse_number):
    data = _received_endpoints(assertion, paragraphs)
    if not data:
        return False
    text, head, ancestor = data
    q = assertion.get('qualifiers', {})
    number = q.get('source_number')
    value = q.get('reported_generation_number')
    if (assertion.get('predicate') != 'ancestor' or q.get('adopted_for_family_tree') is not False
            or q.get('ancestry_precision') != 'reported_self_genealogy'
            or 'generation_distance' not in q or q['generation_distance'] is not None
            or type(value) is not int or value < 1 or not isinstance(number, str)
            or not number or parse_number(number) != value):
        return False
    role = number+'世祖'
    a = ancestor['start'] - len(role)
    return (re.fullmatch(r'字[^，。；「」]{1,5}，[^，。；「」]{1,16}人也。',text[head['end']:a]) is not None
            and text[a:ancestor['start']] == role
            and q.get('source_term') == role + ancestor['surface']
            and re.match(r'，[^。；「」]+，其自敍云爾。',text[ancestor['end']:]) is not None)


def elder_uncle_valid(assertion, paragraphs):
    data = _received_endpoints(assertion, paragraphs)
    if not data:
        return False
    text, nephew, uncle = data
    q = assertion.get('qualifiers', {})
    return (assertion.get('predicate') == 'paternal_uncle' and q.get('lineage') == 'paternal'
            and q.get('source_kin_term_type') == 'resumed_subject_named_shifu'
            and q.get('source_term') == '世父'+uncle['surface']
            and text[nephew['end']:uncle['start']] in ('幼而不羣，世父', '幼而不群，世父')
            and text[uncle['end']:].startswith('有知人鑒，常笑曰：「此兒'))
