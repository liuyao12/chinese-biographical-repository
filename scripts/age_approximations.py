# coding: utf-8
"""Source-bound adjacent age numerals; never convert approximations to bounds."""
DIGITS = '一二三四五六七八九'

def age_approximation_errors(age, paragraph):
    if isinstance(age.get('subject_scope'), dict) and age['subject_scope'].get('kind') == 'immediate_child_age':
        try:
            from scripts.individual_adjacent_age import individual_adjacent_age_errors
        except ImportError:
            from individual_adjacent_age import individual_adjacent_age_errors
        return individual_adjacent_age_errors(age, paragraph)
    if age.get('approximation', {}).get('kind') != 'approaching_age':
        return adjacent_age_errors(age, paragraph)
    number = age.get('source_number')
    # Current source form is a whole tens numeral, not a range or exact age.
    target = (DIGITS.index(number[0]) + 1) * 10 if isinstance(number, str) and len(number) == 2 and number[0] in DIGITS and number[1] == '十' else None
    if (target is None or age.get('approximation') != {'kind': 'approaching_age', 'target': target}
            or age.get('value') is not None or 'bounds' in age or 'source_number_bounds' in age
            or age.get('source_term') not in ('年向' + number, '年垂' + number, '年近' + number)
            or age.get('reporting_status') != 'approximate_report'
            or age.get('birth_year') is not None or age.get('unit') != 'source_age_years'
            or age.get('counting') != 'unspecified_source_age' or age.get('status') != 'source_attested'):
        return ['年向報齡須保留趨近數字，不得補確歲、嚴格界限或生年']
    interpretation = age.get('approximation_interpretation', {})
    if (interpretation.get('status') != 'editorial_provisional'
            or interpretation.get('human_reviewed') is not False
            or not interpretation.get('reviewer') or not interpretation.get('rationale')):
        return ['年向報齡缺少分存的編者判讀']
    if age.get('source_term') in ('年垂' + number, '年近' + number):
        scope = age.get('subject_scope', {})
        if not isinstance(scope, dict):
            return ['年垂報齡缺具名主語範圍']
        text = paragraph['text']
        named = {m['id']: m for m in paragraph.get('mentions', []) if m.get('kind') == 'person'}
        subject = named.get(scope.get('subject_person_mention_id'), {})
        if (set(scope) != {'kind', 'subject_person_mention_id'}
                or scope.get('kind') != 'named_subject_in_biography' or 'speaker_scope' in age
                or paragraph.get('text_layer') != 'received_chapter'
                or text.count(age['source_term']) != 1
                or subject.get('person_id') != age.get('person_id')):
            return ['年垂報齡須連到本段具名敘述主語，不得當奏表自報']
        at = text.index(age['source_term'])
        before = [m for m in named.values() if m['end'] <= at]
        if (not before or subject.get('end', len(text) + 1) > at
                or max(before, key=lambda m: m['end'])['person_id'] != age['person_id']):
            return ['年垂報齡主語須與報齡前最近具名人物相合']
        evidence = age.get('evidence')
        if (not isinstance(evidence, list) or not evidence
                or any(not isinstance(e, dict) or e.get('paragraph_id') != paragraph['id'] or e.get('quote') != text
                       or e.get('person_mention_id') != subject['id'] for e in evidence)):
            return ['年垂報齡須保存完整原段及本人錨點']
        return []
    scope = age.get('speaker_scope', {})
    ms = {m['id']: m for m in paragraph.get('mentions', [])}
    speaker = ms.get(scope.get('speaker_person_mention_id'), {})
    anchor = scope.get('speech_start_anchor', {})
    text = paragraph['text']
    start, end = anchor.get('start'), anchor.get('end')
    if (scope.get('kind') != 'self_report_in_memorial'
            or speaker.get('person_id') != age.get('person_id') or speaker.get('surface') != '臣'
            or type(start) is not int or type(end) is not int or not 0 <= start < end <= len(text)
            or anchor.get('paragraph_id') != paragraph['id'] or anchor.get('surface') != '又表曰：「'
            or text[start:end] != anchor['surface']):
        return ['年向自報須連到奏表起點及本人臣字錨點']
    at = text.find(age['source_term'], end)
    if at < 0 or not end <= speaker['start'] < speaker['end'] <= at or '」' in text[end:at]:
        return ['年向報齡不在該本人奏表範圍']
    return []

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
