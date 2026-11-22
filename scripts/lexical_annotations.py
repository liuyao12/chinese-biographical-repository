# coding: utf-8
"""Check source-bound classifications of formerly ambiguous, non-person words."""

def non_person_errors(mention, text):
    term = mention.get('basis_quote')
    starts = [i for i in range(len(text)) if text.startswith(term, i)] if isinstance(term, str) and term else []
    start, end = mention.get('start'), mention.get('end')
    role = mention.get('lexical_role')
    role_valid = role in ('verb', 'reciprocal_adverb')
    if role == 'offered_office':
        role_valid = (mention.get('surface') == '中書令' and term == '尋加中書令，固讓'
                      and any(i + 2 == start for i in starts))
    elif role == 'narrative_matter':
        role_valid = (mention.get('surface') == '其' and term == '猶以前憾緩其事')
    elif role == 'office_predicate':
        role_valid = (mention.get('surface') == '司馬' and term == '會稽王道子以為司馬')
    elif role == 'philosophical_term_component':
        role_valid = (mention.get('surface') == '玄' and term == '朗善言玄理'
                      and any(i + 3 == start for i in starts))
    elif role == 'distributive_adverb':
        role_valid = (mention.get('surface') == '皆' and term == '皆其小字也'
                      and any(i == start for i in starts))
    elif role == 'vacant_office':
        role_valid = mention.get('surface') == '太子' and isinstance(term, str) and term.endswith('無太子')
    elif role == 'sovereign_status':
        role_valid = mention.get('surface') == '天子' and term in ('刻天子璽', '求即天子位')
    elif role == 'office_title_component':
        role_valid = (mention.get('surface') == '太子'
                      and term in ('太子太傅', '太子太保', '太子少傅', '太子少保', '太子中庶子', '太子舍人')
                      and any(i == start for i in starts))
    if role == 'geographic_name_in_rebus':
        role_valid = (mention.get('surface') == '溫' and term == '故河內大縣，溫也'
                      and any(i + term.index('溫') == start for i in starts))
    if role == 'office_title_component' and mention.get('surface') == '中書':
        role_valid = term == '中書侍郎' and any(i == start for i in starts)
    if role == 'generic_rank_component':
        role_valid = ((mention.get('surface'), term) in (('臣','逆臣賊子'),('公','王公之上'))
                      and any(i + 1 == start for i in starts))
    valid = (mention.get('kind') == 'non_person' and mention.get('person_id') is None
             and 'work_id' not in mention and mention.get('status') == 'contextual_provisional'
             and role_valid
             and isinstance(mention.get('interpretation_note'), str) and bool(mention['interpretation_note'].strip())
             and mention.get('human_reviewed') is False and bool(mention.get('reviewer'))
             and type(start) is int and type(end) is int and 0 <= start < end <= len(text)
             and text[start:end] == mention.get('surface')
             and any(i <= start < end <= i + len(term) for i in starts))
    return [] if valid else ['非人物判讀須保留詞性、原語境、理由及未經人工審閱狀態，不得暗連人物']
