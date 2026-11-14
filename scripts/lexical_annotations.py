# coding: utf-8
"""Check source-bound classifications of formerly ambiguous, non-person words."""
import re

def non_person_errors(mention, text):
    term = mention.get('basis_quote')
    starts = [i for i in range(len(text)) if text.startswith(term, i)] if isinstance(term, str) and term else []
    start, end = mention.get('start'), mention.get('end')
    role = mention.get('lexical_role')
    role_valid = role in ('verb', 'reciprocal_adverb')
    if role == 'natural_phenomenon':
        surface = mention.get('surface')
        role_valid = (isinstance(surface, str) and isinstance(term, str)
                      and bool(surface) and surface in term)
    if role == 'interrogative_particle':
        role_valid = (mention.get('surface') == '侯'
                      and term == '君乎君乎，侯不邁哉！')
    if role == 'vacant_office':
        role_valid = mention.get('surface') == '太子' and isinstance(term, str) and term.endswith('無太子')
    elif role == 'sovereign_status':
        role_valid = mention.get('surface') == '天子' and term in ('刻天子璽', '求即天子位')
    elif role == 'office_title_component':
        surface = mention.get('surface')
        allowed_terms = {
            '太子': ('太子太傅', '太子太保', '太子少傅', '太子少保', '太子中庶子', '太子舍人'),
            '僕射': ('尚書左僕射',),
        }
        role_valid = (surface in allowed_terms
                      and term in allowed_terms[surface]
                      and isinstance(term, str)
                      and any(i + term.index(surface) == start for i in starts))
    valid = (mention.get('kind') == 'non_person' and mention.get('person_id') is None
             and 'work_id' not in mention and mention.get('status') == 'contextual_provisional'
             and role_valid
             and isinstance(mention.get('interpretation_note'), str) and bool(mention['interpretation_note'].strip())
             and mention.get('human_reviewed') is False and bool(mention.get('reviewer'))
             and type(start) is int and type(end) is int and 0 <= start < end <= len(text)
             and text[start:end] == mention.get('surface')
             and any(i <= start < end <= i + len(term) for i in starts))
    if role == 'interrogative_particle':
        refs = mention.get('source_references')
        valid = valid and isinstance(refs, list) and bool(refs) and all(
            isinstance(ref, dict)
            and isinstance(ref.get('title'), str) and bool(ref['title'])
            and isinstance(ref.get('url'), str) and ref['url'].startswith(('https://', 'http://'))
            and isinstance(ref.get('quote'), str) and bool(ref['quote'])
            and isinstance(ref.get('source_type'), str) and bool(ref['source_type'])
            and isinstance(ref.get('accessed_on'), str)
            and bool(re.fullmatch(r'\d{4}-\d{2}-\d{2}', ref['accessed_on']))
            for ref in refs)
    return [] if valid else ['非人物判讀須保留詞性、原語境、理由及未經人工審閱狀態，不得暗連人物']
