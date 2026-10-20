"""Bound an undated event within a named Chinese civil-calendar era."""


def civil_era_range_errors(value, evidence, expression):
    errors = []
    mapping = value.get('era_span_mapping')
    refs = value.get('references')
    if not isinstance(mapping, dict) or not isinstance(refs, list):
        return ['中國曆年號範圍缺少年號起迄及對照來源']
    index = mapping.get('reference_index')
    ref = refs[index] if type(index) is int and 0 <= index < len(refs) else {}
    name, polity = mapping.get('era_name'), mapping.get('polity_source_name')
    first, last = mapping.get('start_ce_year'), mapping.get('end_ce_year')
    columns = ref.get('columns', {}) if isinstance(ref, dict) else {}
    valid = (value.get('basis') == 'within_named_era'
             and value.get('calendar') == 'chinese_civil'
             and value.get('precision') == 'year_range'
             and value.get('year_numbering') == 'astronomical'
             and value.get('status') == 'editorial_provisional'
             and isinstance(name, str) and bool(name)
             and isinstance(polity, str) and bool(polity)
             and type(first) is int and type(last) is int and 0 < first < last
             and mapping.get('kind') == 'ce_regnal_era_span'
             and expression in tuple(name + stage for stage in ('初', '中', '末'))
             and expression == value.get('source_expression')
             and (expression.endswith('中') or value.get('source_stage') == expression[-1])
             and value.get('evidence') == evidence and isinstance(evidence, list) and bool(evidence)
             and isinstance(value.get('original_quote'), str)
             and all(isinstance(e, dict) and isinstance(e.get('quote'), str) for e in evidence)
             and value.get('original_quote') in [e.get('quote') for e in evidence if isinstance(e, dict)]
             and any(expression in e.get('quote', '') for e in evidence if isinstance(e, dict))
             and isinstance(ref, dict) and ref.get('scope') == 'modern_era_year_equivalence_only'
             and str(ref.get('url', '')).startswith('https://') and ref.get('quote') == name
             and isinstance(columns, dict) and columns.get('era_name') == name
             and columns.get('dynasty') == polity
             and columns.get('first_year') == str(first) and columns.get('last_year') == str(last)
             and bool(value.get('rationale')) and bool(value.get('reviewer'))
             and value.get('human_reviewed') is False)
    if not valid:
        errors.append('中國曆年號範圍須保留初中末原詞、政體及相符年號起迄，不得選定單年')
    for key, year in [('earliest', first), ('latest', last)]:
        point = value.get(key)
        if (point != {'era': 'CE', 'era_year': year, 'year': year}
                or not isinstance(point, dict)
                or type(point.get('era_year')) is not int or type(point.get('year')) is not int):
            errors.append('中國曆年號範圍端點與年號對照不符')
    if 'year' in value or 'era_year' in value:
        errors.append('年號內未定年不得另填確定年份')
    return errors
