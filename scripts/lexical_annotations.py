# coding: utf-8
"""Check source-bound classifications of formerly ambiguous, non-person words."""

def non_person_errors(mention, text, context=None, *, chapter=None, root=None):
    if isinstance(mention, dict) and (mention.get('lexical_role') == 'polity_predicate' or mention.get('id') == 'c-shiji-130-taishigong:m049-0025'):
        try:
            from .source_non_person_retirement import polity_predicate_valid
        except ImportError:
            from source_non_person_retirement import polity_predicate_valid
        return [] if polity_predicate_valid(mention, text, context) else ['國名與述語非人物判讀須由固定完整來源及負向退休證據支持']
    # fixed-c51-office-component-delegate
    binding=mention.get("source_context_binding") if isinstance(mention,dict) else None
    if isinstance(binding,dict) and binding.get("kind")=="received_wyd_complete_unit_office_component":
        try:
            try: from scripts.wyd_song051_yixin import non_person_component_valid
            except ImportError: from wyd_song051_yixin import non_person_component_valid
            valid=non_person_component_valid(mention,text,chapter,root)
        except (ValueError,TypeError,KeyError,OSError,AttributeError): valid=False
        return [] if valid else ["固定完整見證官名組件判讀須綁原章/root/角色/原字"]
    term = mention.get('basis_quote')
    starts = [i for i in range(len(text)) if text.startswith(term, i)] if isinstance(term, str) and term else []
    start, end = mention.get('start'), mention.get('end')
    role = mention.get('lexical_role')
    role_valid = role in ('verb', 'reciprocal_adverb')
    if role == 'vacant_office':
        role_valid = mention.get('surface') == '太子' and isinstance(term, str) and term.endswith('無太子')
    elif role == 'sovereign_status':
        role_valid = mention.get('surface') == '天子' and term in ('刻天子璽', '求即天子位')
    elif role == 'office_title_component':
        role_valid = (mention.get('surface') == '太子'
                      and term in ('太子太傅', '太子太保', '太子少傅', '太子少保', '太子中庶子', '太子舍人')
                      and any(i == start for i in starts))
    valid = (mention.get('kind') == 'non_person' and mention.get('person_id') is None
             and 'work_id' not in mention and mention.get('status') == 'contextual_provisional'
             and role_valid
             and isinstance(mention.get('interpretation_note'), str) and bool(mention['interpretation_note'].strip())
             and mention.get('human_reviewed') is False and bool(mention.get('reviewer'))
             and type(start) is int and type(end) is int and 0 <= start < end <= len(text)
             and text[start:end] == mention.get('surface')
             and any(i <= start < end <= i + len(term) for i in starts))
    return [] if valid else ['非人物判讀須保留詞性、原語境、理由及未經人工審閱狀態，不得暗連人物']
