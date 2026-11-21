"""Keep an unadopted 之後 claim without inventing its generation count."""


def reported_generation_formula_valid(assertion, paragraphs, parse_number):
    """Preserve 自某八世生某 without converting 八世 into an adopted exact path."""
    q = assertion.get('qualifiers', {}); number = q.get('source_number')
    count = q.get('reported_generation_number'); term = q.get('source_term')
    if (assertion.get('predicate') != 'ancestor' or q.get('adopted_for_family_tree') is not False
            or q.get('ancestry_precision') != 'reported_generation_formula'
            or 'generation_distance' not in q or q['generation_distance'] is not None
            or type(count) is not int or count < 1 or parse_number(number) != count
            or not isinstance(term, str) or len(assertion.get('evidence', [])) != 1):
        return False
    e = assertion['evidence'][0]; hit = paragraphs.get(e.get('paragraph_id'))
    if not hit or e.get('chapter_id') != hit[0] or e.get('quote') != hit[1].get('text'):
        return False
    p = hit[1]; ms = {m['id']:m for m in p['mentions']}
    child = ms.get(e.get('subject_person_mention_id')); ancestor = ms.get(e.get('object_person_mention_id'))
    if (not child or not ancestor or child.get('kind') != 'person' or ancestor.get('kind') != 'person'
            or child.get('person_id') != assertion.get('subject_person_id')
            or ancestor.get('person_id') != assertion.get('object_person_id')
            or not term.startswith('自' + ancestor['surface'] + number + '世，生')
            or not term.endswith(child['surface'])):
        return False
    return any(p['text'].startswith(term,i) and ancestor['start']==i+1
               and child['end']==i+len(term) for i in range(len(p['text'])))

def unspecified_ancestry_valid(assertion, paragraphs):
    q = assertion.get('qualifiers', {})
    term = q.get('source_term')
    marker = '後' if q.get('source_marker') == '後' else '之後'
    if (assertion.get('predicate') != 'ancestor'
            or q.get('adopted_for_family_tree') is not False
            or q.get('ancestry_precision') != 'unspecified_descent'
            or any(key not in q or q[key] is not None for key in
                   ['generation_distance', 'source_number', 'reported_generation_number'])
            or not isinstance(term, str) or not term.endswith(marker) or len(term) <= len(marker)
            or not assertion.get('evidence')):
        return False
    for e in assertion['evidence']:
        hit = paragraphs.get(e.get('paragraph_id'))
        quote = e.get('quote')
        if not hit or not isinstance(quote, str) or not quote or quote not in hit[1]['text'] or term not in quote:
            return False
        text = hit[1]['text']
        if marker == '後':
            # 本傳傳首「魏司徒陳矯後」，雙錨分繫所傳皇后與「後」前祖名。
            mentions = {m['id']: m for m in hit[1].get('mentions', [])}
            child = mentions.get(e.get('subject_person_mention_id'), {})
            ancestor = mentions.get(e.get('object_person_mention_id'), {})
            if (hit[0] not in ('c-nanqishu-020-chendaozhi', 'c-nanqishu-020-chendaozhi-wyd')
                    or term != '陳矯後' or child.get('surface') not in ('道止', '道正')
                    or child.get('person_id') != assertion.get('subject_person_id')
                    or not text.startswith('宣孝陳皇后諱' + child['surface'])
                    or child.get('start') != len('宣孝陳皇后諱') or child.get('kind') != 'person'
                    or ancestor.get('surface') != '陳矯' or ancestor.get('kind') != 'person'
                    or ancestor.get('person_id') != assertion.get('object_person_id')
                    or not text.startswith('魏司徒' + term, ancestor.get('start', -1) - 3)):
                return False
        if not any(m.get('kind') == 'person' and m.get('person_id') == assertion.get('object_person_id')
                   and m.get('surface') == term[:-len(marker)]
                   and text.startswith(term, m.get('start', -1)) for m in hit[1].get('mentions', [])):
            return False
    return True
