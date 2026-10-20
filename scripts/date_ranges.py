# coding: utf-8
"""Explicit year windows; they never supply an exact event year."""
from urllib.parse import urlparse

def parallel_event_date(date):
    """原文無紀年時，要求明列事件對讀與參考紀年的不同引句。"""
    if not isinstance(date, dict):
        return False
    basis = date.get('basis')
    required = {'kind', 'source_event_quote', 'reference_url', 'reference_event_quote', 'reference_year_quote'}
    if not isinstance(basis, dict) or set(basis) not in (required, required | {'reference_year_url'}):
        return False
    original = date.get('original_quote')
    quote = basis.get('source_event_quote')
    url = basis.get('reference_url')
    if (basis.get('kind') != 'parallel_event' or not isinstance(original, str)
            or not isinstance(quote, str) or not quote or quote not in original
            or not isinstance(url, str) or urlparse(url).scheme not in ('http', 'https')):
        return False
    year_url = basis.get('reference_year_url', url)
    if not isinstance(year_url, str) or urlparse(year_url).scheme not in ('http', 'https'):
        return False
    refs = date.get('references', [])
    return all(isinstance(basis.get(key), str) and bool(basis[key])
               and any(isinstance(ref, dict) and ref.get('url') == (year_url if key == 'reference_year_quote' else url)
                       and ref.get('quote') == basis[key] and ref.get('scope') in scopes
                       for ref in refs)
               for key, scopes in [('reference_event_quote', ('received_parallel_event',)),
                                  ('reference_year_quote', ('digital_editorial_regnal_year_equivalence_only', 'received_regnal_year_attestation'))])

def year_range_errors(value, evidence, expression):
    if not isinstance(value, dict):
        return ['紀年範圍須為物件']
    if value.get('basis') == 'within_named_era':
        try:
            from .civil_era_ranges import civil_era_range_errors
        except ImportError:
            from civil_era_ranges import civil_era_range_errors
        return civil_era_range_errors(value, evidence, expression)
    if value.get('basis') == 'calendar_reform_transition_year':
        try:
            from .calendar_reform import transition_year_errors
        except ImportError:
            from calendar_reform import transition_year_errors
        return transition_year_errors(value, evidence, expression)
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
    suffix = '中國曆年範圍' if value.get('basis') == 'within_named_era' and value.get('calendar') == 'chinese_civil' else '暫定範圍'
    return f"{prefix(a)}{a['era_year']}至{last}年（{suffix}）"
