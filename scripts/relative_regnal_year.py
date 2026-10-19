# coding: utf-8
"""Validate 明年/其年 using explicit era and preceding regnal-year evidence."""


def relative_regnal_year_valid(date, parse_number):
    mapping = date.get('regnal_year_mapping', {})
    context = date.get('relative_year_reference', {})
    evidence, refs = date.get('evidence', []), date.get('references', [])
    term = context.get('source_term')
    offset = {'明年': 1, '其年': 0}.get(term)
    omitted_era = (context.get('kind') == 'omitted_era_regnal_year'
                   and term == str(mapping.get('source_number')) + '年')
    if omitted_era:
        offset = 0
    if (mapping.get('kind') != 'relative_ce_regnal_era_span' or offset is None
            or date.get('source_expression') != term
            or mapping.get('year_offset') != offset
            or not isinstance(evidence, list) or not evidence or not isinstance(refs, list)):
        return False
    indices = [context.get(k) for k in ['era_evidence_index', 'antecedent_evidence_index', 'event_evidence_index']]
    ri = mapping.get('reference_index')
    if (any(type(i) is not int or not 0 <= i < len(evidence) for i in indices)
            or indices != sorted(indices)
            or type(ri) is not int or not 0 <= ri < len(refs)):
        return False
    era_e, prior_e, event_e = [evidence[i] for i in indices]
    if (len({e.get('chapter_id') for e in evidence}) != 1
            or len({e.get('source_id') for e in evidence}) != 1
            or event_e.get('quote') != date.get('original_quote')):
        return False
    name = mapping.get('era_name')
    number = mapping.get('source_number')
    n = mapping.get('regnal_year')
    first, last = mapping.get('start_ce_year'), mapping.get('end_ce_year')
    if (not isinstance(name, str) or not name or parse_number(number) != n
            or type(n) is not int or n < 1 or type(first) is not int or type(last) is not int
            or not 0 < first <= last or mapping.get('target_regnal_year') != n + offset
            or date.get('era') != 'CE' or date.get('year') != first + n + offset - 1
            or not first <= date['year'] <= last):
        return False
    prior = context.get('antecedent_expression')
    era_term = context.get('era_expression')
    if (prior not in (str(number) + '年', name + str(number) + '年')
            or not isinstance(era_term, str) or not era_term.startswith(name)
            or not era_term.endswith('年')
            or parse_number(era_term[len(name):-1]) is None
            or era_term not in era_e.get('quote', '')
            or prior not in prior_e.get('quote', '') or term not in event_e.get('quote', '')):
        return False
    if not omitted_era and indices[1] == indices[2] and prior_e['quote'].index(prior) >= event_e['quote'].index(term):
        return False
    ref = refs[ri]
    return (ref.get('scope') == 'modern_era_year_equivalence_only'
            and ref.get('quote') == name and str(ref.get('url', '')).startswith('https://')
            and ref.get('columns', {}).get('era_name') == name
            and ref.get('columns', {}).get('first_year') == str(first)
            and ref.get('columns', {}).get('last_year') == str(last))
