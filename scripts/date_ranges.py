# coding: utf-8
"""Explicit year windows; they never supply an exact event year."""
def year_range_errors(value, evidence, expression):
    if not isinstance(value, dict):
        return ['紀年範圍須為物件']
    errors = []
    endpoints = [value.get(k) for k in ('earliest', 'latest')]
    for point in endpoints:
        if not isinstance(point, dict) or set(point) != {'era', 'era_year', 'year'}:
            errors.append('紀年範圍端點須有時代及數字年份'); continue
        era, number, year = point['era'], point['era_year'], point['year']
        if era not in ('BCE', 'CE') or type(number) is not int or number <= 0 or type(year) is not int or year != (1-number if era == 'BCE' else number):
            errors.append('紀年範圍端點年編號不符')
    if not errors and endpoints[1]['year'] - endpoints[0]['year'] != 1:
        errors.append('歲首跨年範圍須涵蓋相鄰兩年，不可倒序或冒作單年')
    if value.get('year_numbering') != 'astronomical' or value.get('precision') != 'year_range' or value.get('basis') != 'regnal_year_crosses_ce_year' or value.get('status') != 'editorial_provisional':
        errors.append('紀年範圍精度、歲首依據或判讀狀態不符')
    if not isinstance(expression, str) or not expression or value.get('evidence') != evidence or value.get('original_quote') not in [e['quote'] for e in evidence] or not any(expression in e['quote'] for e in evidence):
        errors.append('紀年範圍缺相符原紀年與事件引句')
    refs = value.get('references', [])
    if not isinstance(refs, list) or not {'received_regnal_year_attestation', 'digital_editorial_regnal_year_equivalence_only', 'received_calendar_rule'}.issubset({r.get('scope') for r in refs if isinstance(r, dict) and r.get('quote') and str(r.get('url', '')).startswith('https://')}):
        errors.append('紀年範圍須分列原年欄、數位對照與曆法來源')
    if not value.get('rationale') or not value.get('reviewer') or value.get('human_reviewed') is not False:
        errors.append('紀年範圍缺判讀及覆核狀態')
    return errors

def year_range_label(value):
    a, b = value['earliest'], value['latest']
    prefix = lambda p: '西元' + ('前' if p['era'] == 'BCE' else '')
    last = str(b['era_year']) if a['era'] == b['era'] else prefix(b) + str(b['era_year'])
    return f"{prefix(a)}{a['era_year']}至{last}年（暫定範圍）"
