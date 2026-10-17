# coding: utf-8
"""Source-bound adjacent age numerals; never convert approximations to bounds."""
DIGITS = '一二三四五六七八九'

def adjacent_age_errors(age, paragraph):
    errors = []
    number = age.get('source_number')
    numbers = [DIGITS.index(x) + 1 for x in number] if isinstance(number, str) and len(number) == 2 and all(x in DIGITS for x in number) else []
    coded = age.get('approximation')
    coded_numbers = coded.get('numbers') if isinstance(coded, dict) else None
    if not (isinstance(coded_numbers, list) and all(type(x) is int for x in coded_numbers)
            and len(numbers) == 2 and numbers[1] == numbers[0] + 1
            and age.get('approximation') == {'kind': 'adjacent_age_numbers', 'numbers': numbers}
            and age.get('value') is None and 'bounds' not in age and 'source_number_bounds' not in age
            and age.get('reporting_status') == 'approximate_report'
            and age.get('source_term') == '皆' + str(number) + '歲'
            and age.get('birth_year') is None and age.get('unit') == 'source_age_years'
            and age.get('counting') == 'unspecified_source_age' and age.get('status') == 'source_attested'):
        errors.append('相鄰數詞報齡須保留約數及原詞，不得當確歲、嚴格上下界或出生年')
    interpretation = age.get('approximation_interpretation')
    if not (isinstance(interpretation, dict) and interpretation.get('status') == 'editorial_provisional'
            and interpretation.get('human_reviewed') is False and bool(interpretation.get('reviewer'))
            and isinstance(interpretation.get('rationale'), str) and bool(interpretation['rationale'].strip())):
        errors.append('報齡約數缺少分存的編者判讀與未經人工審閱狀態')
    group = age.get('group_reference')
    expected = {'source_term', 'naming_term', 'person_ids', 'declared_member_count', 'source_count_term'}
    if not isinstance(group, dict) or set(group) != expected:
        return errors + ['群體約數報齡須明示完整具名範圍及原文人數']
    ids, count, count_term = group.get('person_ids'), group.get('declared_member_count'), group.get('source_count_term')
    term, naming = group.get('source_term'), group.get('naming_term')
    members = ids if isinstance(ids, list) and all(isinstance(x, str) for x in ids) else []
    if not (type(count) is int and 1 <= count <= 9 and count_term == DIGITS[count - 1] + '人'
            and len(members) == count and len(set(members)) == count and age.get('person_id') in members
            and isinstance(term, str) and bool(term) and count_term in term
            and isinstance(naming, str) and bool(naming)):
        return errors + ['群體約數報齡人數、原詞或具名成員不符']
    text = paragraph['text']
    starts = [i for i in range(len(text)) if text.startswith(naming, i)]
    named = {m.get('person_id') for m in paragraph['mentions'] if m.get('kind') == 'person'
             and any(i <= m['start'] < m['end'] <= i + len(naming) for i in starts)}
    if not starts or named != set(members):
        errors.append('群體約數報齡名單須有且僅有原句所列各人物錨點')
    evidence = age.get('evidence')
    if not isinstance(evidence, list) or not evidence:
        return errors + ['群體約數報齡缺少原文證據']
    local = [e for e in evidence if isinstance(e, dict) and e.get('paragraph_id') == paragraph['id']]
    if not local:
        return errors + ['群體約數報齡引句不屬所指段落']
    for item in local:
        quote = item.get('quote')
        mention = next((m for m in paragraph['mentions'] if m['id'] == item.get('person_mention_id')), None)
        if not (isinstance(quote, str) and bool(quote) and quote in text and term in quote and naming in quote
                and isinstance(age.get('source_term'), str) and age['source_term'] in quote
                and mention and mention.get('person_id') == age.get('person_id')):
            errors.append('群體約數報齡須引用本人的錨點、報齡原詞及完整具名名單')
    return errors
