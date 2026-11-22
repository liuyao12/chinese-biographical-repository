#!/usr/bin/env python3
# coding: utf-8
"""檢查穩定 ID、字元錨點、人物證據、身份判斷及 XML／JSON 一致性。"""
from pathlib import Path
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from urllib.parse import urlparse
try:
    from scripts.era_stage_dates import binding_valid
except ImportError:
    from era_stage_dates import binding_valid
ROOT = Path(__file__).resolve().parents[1]

def source_age_number(number):
    digits = '一二三四五六七八九'
    if not isinstance(number, str): return None
    if re.fullmatch('[廿卅卌](?:有?[一二三四五六七八九])?', number):
        rest=number[1:].removeprefix('有')
        return {'廿':20,'卅':30,'卌':40}[number[0]] + (digits.index(rest)+1 if rest else 0)
    if number in digits and len(number) == 1: return digits.index(number) + 1
    if re.fullmatch('[一二三四五六七八九]?十(?:有?[一二三四五六七八九])?', number):
        tens, ones = number.split('十')
        ones = ones.removeprefix('有')
        return (digits.index(tens) + 1 if tens else 1) * 10 + (digits.index(ones) + 1 if ones else 0)
    match = re.fullmatch('([一二三四五六七八九]?)百(?:有?([一二三四五六七八九]?十[一二三四五六七八九]?))?', number)
    if match:
        return (digits.index(match[1]) + 1 if match[1] else 1) * 100 + (source_age_number(match[2]) if match[2] else 0)
    return None

def direct_source_age_valid(age):
    number = age.get('source_number')
    if (isinstance(number, str) and age.get('source_term') == number + '而卒'
            and age.get('age_context', {}).get('kind') == 'at_death'):
        term = age['source_term']
        return (type(age.get('value')) is int and age['value'] == source_age_number(number)
                and bool(age.get('evidence')) and all(
                    re.search(r'[，。；]' + re.escape(term) + r'[。；]', e.get('quote', ''))
                    for e in age['evidence']))
    number = age.get('source_number'); parsed = source_age_number(number)
    return (type(age.get('value')) is int and parsed is not None and age['value'] == parsed
            and age.get('source_term') in ('年' + str(number), '時年' + str(number), '年登' + str(number), '年始' + str(number),
                                           '年' + str(number) + '歲', str(number) + '歲', str(number) + '歳', str(number) + '嵗'))


def named_office_end_valid(holding, paragraphs, mentions):
    """明言終於此職的終期，不能以一般死亡替代所有官爵終期。"""
    basis = holding.get('end_basis'); end = holding.get('effective_period',{}).get('end',{})
    if isinstance(basis, dict) and basis.get('kind') in ('named_last_office_mourning_leave', 'named_son_office_removed_for_slaughtering_cattle'):
        try:
            from scripts.lifecycle_offered_biography import end_valid
        except ImportError:
            from lifecycle_offered_biography import end_valid
        return end_valid(holding, paragraphs, mentions)
    if isinstance(basis, dict) and basis.get('kind') == 'resumed_biography_mother_mourning_office_end':
        try:
            from scripts.resumed_biography_lifecycle import mourning_end_valid
        except ImportError:
            from resumed_biography_lifecycle import mourning_end_valid
        return mourning_end_valid(holding, paragraphs, mentions)
    if isinstance(basis, dict) and basis.get('kind') == 'died_in_last_named_office':
        try:
            from scripts.current_office_death import current_office_death_valid
        except ImportError:
            from current_office_death import current_office_death_valid
        return current_office_death_valid(holding, paragraphs, mentions)
    if (not isinstance(basis,dict) or set(basis)!={'kind','source_term','evidence'}
            or holding.get('kind')!='office' or basis.get('kind')!='died_in_named_office'
            or basis.get('source_term')!='竟以'+holding.get('title','')+'終'
            or end.get('status')!='source_event' or end.get('event_type')!='explicit_end'
            or not basis.get('evidence') or basis['evidence']!=end.get('evidence')):
        return False
    for e in basis['evidence']:
        hit=paragraphs.get(e.get('paragraph_id')); m=mentions.get(e.get('person_mention_id'))
        quote=e.get('quote','');term=basis['source_term']
        if (not hit or not m or m[1]!=e.get('paragraph_id')
                or m[2].get('person_id')!=holding.get('person_id')
                or not quote or quote not in hit[1]['text'] or term not in quote):return False
        positions=[i for i in range(len(hit[1]['text']))if hit[1]['text'].startswith(term,i)]
        if not any(m[2]['end']<=i and not any(other.get('person_id') not in (None,holding['person_id'])
                    and m[2]['end']<=other['start']<i+len(term) for other in hit[1]['mentions'])for i in positions):return False
    return True


def reported_appointment_count_valid(count, title):
    return (isinstance(count, dict)
             and set(count) == {'value', 'unit', 'source_number', 'source_term', 'status', 'evidence'}
             and type(count.get('value')) is int and count['value'] > 0
             and count.get('unit') == 'appointment'
             and count.get('status') == 'source_attested'
             and source_age_number(count.get('source_number')) == count['value']
             and count.get('source_term') == count['source_number'] + '為' + title
             and isinstance(count.get('evidence'), list) and bool(count['evidence'])
             and all(isinstance(e, dict) and isinstance(e.get('quote'), str)
                     and count['source_term'] in e['quote'] for e in count['evidence']))

def reported_office_event_count_valid(count, event_type):
    verbs = {'departure': '去相', 'reinstatement': '復位'}
    return (event_type in verbs and isinstance(count, dict)
            and set(count) == {'value', 'unit', 'source_number', 'source_term', 'status', 'evidence'}
            and type(count.get('value')) is int and count['value'] > 0
            and count.get('unit') == 'office_event' and count.get('status') == 'source_attested'
            and source_age_number(count.get('source_number')) == count['value']
            and count.get('source_term') == count['source_number'] + verbs[event_type]
            and isinstance(count.get('evidence'), list) and bool(count['evidence'])
            and all(isinstance(e, dict) and isinstance(e.get('quote'), str)
                    and count['source_term'] in e['quote'] for e in count['evidence']))

try:
    from scripts.date_ranges import parallel_event_date
except ImportError:
    from date_ranges import parallel_event_date


def normalized_date_errors(date, chapters=None, root=ROOT, bound_record=None, bound_role=None):
    errors = []
    if not isinstance(date, dict):
        return ['紀年換算須為物件']
    if 'rendered_collective_award_year_binding' in date:
        try:from scripts.wyd_song044_noble_year import valid as noble_year_valid
        except ImportError:from wyd_song044_noble_year import valid as noble_year_valid
        return [] if noble_year_valid(date,bound_record,bound_role,chapters or {},root) else ['跨來源同詔封年須綁完整比較單元、兩人同爵食邑、明年及取得資格']
    era, year, number = date.get('era'), date.get('year'), date.get('era_year')
    if era not in ('BCE', 'CE') or type(year) is not int or type(number) is not int or number <= 0:
        errors.append('紀年換算須有數字年份與正整數時代年')
    elif year != (number if era == 'CE' else 1 - number):
        errors.append('紀年換算天文年與時代年不一致')
    if date.get('year_numbering') != 'astronomical' or date.get('precision') != 'year':
        errors.append('紀年換算年編號或精度無效')
    if date.get('status') != 'editorial_provisional' or not date.get('original_quote') or not date.get('evidence') or not date.get('references'):
        errors.append('紀年換算原句、證據、參考或判讀狀態缺失')
    if not date.get('rationale') or not date.get('reviewer') or date.get('human_reviewed') is not False:
        errors.append('紀年换算判讀或覆核狀態無效'.replace('换','換'))
    if 'calendar' in date:
        if date.get('calendar') != 'chinese_civil':
            errors.append('明示年度曆法未知')
        else:
            mapping = date.get('regnal_year_mapping')
            valid = isinstance(mapping, dict)
            if valid:
                refs = date.get('references'); index = mapping.get('reference_index')
                ref = refs[index] if isinstance(refs, list) and type(index) is int and 0 <= index < len(refs) else {}
                first, last, n = mapping.get('start_ce_year'), mapping.get('end_ce_year'), mapping.get('regnal_year')
                number, name = mapping.get('source_number'), mapping.get('era_name')
                parsed = 1 if number == '元' else source_age_number(number)
                source_name = mapping.get('source_era_name', name)
                spelling_ok = (source_name == name or (source_name, name) in
                               (('昇平', '升平'), ('升明', '昇明'), ('興寜', '興寧')))
                if 'era_name_bridge' in date:
                    try:
                        from scripts.primary_era_abbreviation import valid as era_abbreviation_valid
                    except ImportError:
                        from primary_era_abbreviation import valid as era_abbreviation_valid
                    spelling_ok = era_abbreviation_valid(date, chapters or {}, root)
                prefix = mapping.get('source_polity_prefix', '')
                prefix_ok = ('source_polity_prefix' not in mapping or
                             (isinstance(prefix, str) and bool(prefix) and isinstance(ref, dict)
                              and isinstance(ref.get('columns'), dict)
                              and ref['columns'].get('dynasty') == prefix))
                expression = ((prefix if isinstance(prefix, str) else '') + source_name + str(number) + '年'
                              if isinstance(source_name, str) else None)
                valid = (mapping.get('kind') == 'ce_regnal_era_span' and era == 'CE'
                         and type(first) is int and type(last) is int and 0 < first <= last
                         and type(n) is int and n > 0 and n == parsed
                         and year == first + n - 1 and year <= last
                         and spelling_ok and prefix_ok and expression == date.get('source_expression')
                         and isinstance(date.get('original_quote'), str) and expression in date['original_quote']
                         and isinstance(ref, dict) and ref.get('scope') == 'modern_era_year_equivalence_only'
                         and ref.get('quote') == name and isinstance(ref.get('url'), str) and ref['url'].startswith('https://')
                         and isinstance(ref.get('columns'), dict)
                         and ref.get('columns', {}).get('era_name') == name
                         and ref.get('columns', {}).get('first_year') == str(first)
                         and ref.get('columns', {}).get('last_year') == str(last))
            if isinstance(mapping, dict) and mapping.get('kind') == 'xiangshan_m9_inscribed_year':
                try: from scripts.xiangshan_m9_epitaphs import inscribed_year_valid as xm9_inscribed_year_valid
                except ImportError: from xiangshan_m9_epitaphs import inscribed_year_valid as xm9_inscribed_year_valid
                valid=xm9_inscribed_year_valid(date,bound_record,bound_role,chapters or {},root)
            if isinstance(mapping, dict) and mapping.get('kind') == 'fixed_received_local_regnal_year':
                try:from scripts.fixed_received_career import local_date_valid
                except ImportError:from fixed_received_career import local_date_valid
                chapter=(chapters or {}).get((bound_record or {}).get('evidence',[{}])[0].get('chapter_id'),{})
                valid=local_date_valid(date,chapter,root,bound_record,bound_role)
            if isinstance(mapping, dict) and mapping.get('kind') == 'fixed_wyd_execution_narrative_year':
                try:from scripts.wyd_song044_life import date_valid as wyd_execution_date_valid
                except ImportError:from wyd_song044_life import date_valid as wyd_execution_date_valid
                valid = bound_role == 'life_event' and wyd_execution_date_valid(date,bound_record,chapters or {},root)
            if isinstance(mapping, dict) and mapping.get('kind') == 'relative_ce_regnal_era_span':
                try:
                    from scripts.relative_regnal_year import relative_regnal_year_valid
                except ImportError:
                    from relative_regnal_year import relative_regnal_year_valid
                valid = relative_regnal_year_valid(date, source_age_number, chapters)
            if isinstance(mapping, dict) and mapping.get('kind') == 'annal_ce_regnal_era_span':
                try:
                    from scripts.annal_year_context import annal_regnal_year_valid, annal_year_binding_valid
                except ImportError:
                    from annal_year_context import annal_regnal_year_valid, annal_year_binding_valid
                valid = (annal_regnal_year_valid(date, source_age_number)
                         and isinstance(chapters, dict)
                         and annal_year_binding_valid(date, chapters.get(date['evidence'][0]['chapter_id'], {})))
            if isinstance(mapping, dict) and mapping.get('kind') == 'era_only_antecedent_ce_span':
                try:
                    from scripts.era_only_dates import valid as era_only_valid
                except ImportError:
                    from era_only_dates import valid as era_only_valid
                valid = era_only_valid(date, source_age_number, chapters)
            if isinstance(mapping, dict) and mapping.get('kind') in ('archived_parallel_title_ce_span', 'source_orthographic_ce_regnal_span'):
                try:
                    from scripts.archived_title_years import valid as archived_title_year_valid, local_valid as local_title_year_valid
                except ImportError:
                    from archived_title_years import valid as archived_title_year_valid, local_valid as local_title_year_valid
                valid = (archived_title_year_valid(date, bound_record, bound_role, chapters or {}, root)
                         if mapping['kind'] == 'archived_parallel_title_ce_span'
                         else local_title_year_valid(date, bound_record, bound_role, chapters or {}))
            if isinstance(mapping, dict) and mapping.get('kind') == 'source_office_event_bridge':
                try:
                    from scripts.source_office_dates import normalized_valid as source_office_date_valid
                except ImportError:
                    from source_office_dates import normalized_valid as source_office_date_valid
                valid = source_office_date_valid(date, bound_record, bound_role, chapters or {}, root)
            if isinstance(mapping, dict) and mapping.get('kind') == 'reviewed_archived_role_event':
                try:
                    from scripts.role_event_year_bridge import normalized_valid as role_event_year_valid
                except ImportError:
                    from role_event_year_bridge import normalized_valid as role_event_year_valid
                valid = role_event_year_valid(date, bound_record, bound_role, chapters or {}, root)
            if isinstance(mapping, dict) and mapping.get('kind') == 'fixed_primary_parallel_ce_regnal_span':
                try:
                    from scripts.fixed_primary_biography_dates import valid as fixed_primary_date_valid
                except ImportError:
                    from fixed_primary_biography_dates import valid as fixed_primary_date_valid
                valid = fixed_primary_date_valid(date, chapters or {}, root, bound_record, bound_role)
            if isinstance(mapping,dict) and mapping.get('kind')=='qi006_wangyan_era_year':
                try: from scripts.nanshi024_wangyan import annal_date_valid as qi006_yan_date
                except ImportError: from nanshi024_wangyan import annal_date_valid as qi006_yan_date
                valid=qi006_yan_date(date,bound_record,bound_role,chapters or {},root)
            if isinstance(mapping, dict) and mapping.get('kind') == 'named_annal_biographical_death':
                try:
                    from scripts.annal_named_death import valid as annal_named_death_valid
                except ImportError:
                    from annal_named_death import valid as annal_named_death_valid
                valid = (bound_role == 'life_event' and isinstance(bound_record, dict)
                         and annal_named_death_valid(date, bound_record, chapters or {}, root))
            if isinstance(mapping, dict) and mapping.get('kind') == 'archived_parallel_death_ce_span':
                try:
                    from scripts.archived_parallel_death import valid as archived_death_valid
                except ImportError:
                    from archived_parallel_death import valid as archived_death_valid
                valid = (bound_role == 'life_event' and isinstance(bound_record, dict)
                         and archived_death_valid(date, bound_record, chapters or {}, root))
            if 'calendar_context' in date:
                try:
                    from scripts.calendar_wiring import date_shape_valid
                except ImportError:
                    from calendar_wiring import date_shape_valid
                valid = date_shape_valid(date)
            if not valid:
                errors.append('中國曆年度換算須有原紀年、相符年序及現代年號起迄對照')
    if 'basis' in date and not parallel_event_date(date):
        errors.append('平行事件定年缺少原句或分層參考證據')
    return errors


def reported_relationship_errors(variant, paragraph):
    """未採納的古注弟說保持獨立，不得轉成已採用的家族邊。"""
    if 'reported_relationship' not in variant:
        return []
    r = variant['reported_relationship']
    if not isinstance(r, dict):
        return ['古注親屬異說格式無效']
    errors = []
    expected = {'predicate', 'subject_person_id', 'object_person_id', 'object_generation_relative_to_subject',
                'older_person_id', 'younger_person_id', 'status'}
    subject, obj = r.get('subject_person_id'), r.get('object_person_id')
    valid = (set(r) == expected and r.get('predicate') == 'brother'
             and r.get('status') == 'commentary_claim_not_adopted'
             and variant.get('adopted') is False and variant.get('status') == 'reported_not_collated'
             and isinstance(subject, str) and bool(subject) and isinstance(obj, str) and bool(obj)
             and subject != obj and {subject, obj}.issubset(set(variant.get('person_ids', [])))
             and type(r.get('object_generation_relative_to_subject')) is int
             and r['object_generation_relative_to_subject'] == 0
             and r.get('older_person_id') == obj and r.get('younger_person_id') == subject)
    if not valid:
        errors.append('古注弟說須保留同輩、長幼方向及未採納狀態')
    raw = variant.get('raw_quote', '')
    cleaned = re.sub(r'[/¶\s]', '', re.sub(r'<pb:[^>]*>', '', raw)) if isinstance(raw, str) else ''
    mentions = paragraph.get('mentions', []) if isinstance(paragraph, dict) else []
    subjects = [m['surface'] for m in mentions if m.get('person_id') == subject]
    objects = [m['surface'] for m in mentions if m.get('person_id') == obj]
    if (not isinstance(variant.get('quote'), str) or not variant['quote'] or variant['quote'] not in cleaned
            or not any(word + '(' in cleaned for word in subjects)
            or not any(variant.get('reported_reading') == word + '弟' for word in objects)):
        errors.append('古注弟說原引文、注語詞頭或對象不符')
    return errors


def title_proposal_errors(proposal, chapter, person_ids, holdings=None):
    if isinstance(proposal,dict) and proposal.get('source_appointment_context',{}).get('kind')=='wyd_song044_declined_noble_advance':
        try:from scripts.wyd_song044_nobles import proposal_errors as noble_proposal_errors
        except ImportError:from wyd_song044_nobles import proposal_errors as noble_proposal_errors
        return noble_proposal_errors(proposal,chapter,person_ids)
    if proposal.get('source_appointment_context',{}).get('kind')=='punctuated_biography_career_frame':
        try:from scripts.punctuated_biography_career import proposal_errors
        except ImportError:from punctuated_biography_career import proposal_errors
        return proposal_errors(proposal,chapter,person_ids)
    if proposal.get('source_appointment_context',{}).get('kind')=='layered_biographical_role_frame':
        try:from scripts.layered_biography_titles import offered_errors
        except ImportError:from layered_biography_titles import offered_errors
        return offered_errors(proposal,chapter,person_ids)
    if proposal.get('source_appointment_context', {}).get('kind') == 'received_biographical_role_sequence':
        try:
            from scripts.biographical_appointment_sequence import proposal_errors
        except ImportError:
            from biographical_appointment_sequence import proposal_errors
        return proposal_errors(proposal, chapter, person_ids)
    if isinstance(proposal.get('source_appointment_context'), dict) and proposal['source_appointment_context'].get('kind') == 'fixed_biography_offered_office_sequence':
        try:
            from scripts.biography_offered_offices import errors as offered_errors
        except ImportError:
            from biography_offered_offices import errors as offered_errors
        return offered_errors(proposal, chapter, person_ids)

    """區分未實行提議與實行情況未載的任官約定，不計入實授稱號。"""
    if proposal.get('proposal_kind') == 'memorial_request':
        try:
            from scripts.song041_title_semantics import memorial_errors
        except ImportError:
            from song041_title_semantics import memorial_errors
        return memorial_errors(proposal, chapter, person_ids, holdings or {})
    errors = []
    def check(ok, message):
        if not ok: errors.append(message)
    check(proposal.get('person_id') in person_ids, '稱號提議人物未知')
    check(isinstance(proposal.get('title'), str) and bool(proposal['title']), '稱號提議缺原稱')
    agreed = proposal.get('proposal_kind') == 'agreed_appointment'
    unassumed = proposal.get('proposal_kind') == 'unassumed_appointment'
    check(proposal.get('proposal_kind') in (None, 'agreed_appointment', 'unassumed_appointment'), '稱號安排類型未知')
    check(proposal.get('outcome') == ('not_reported' if agreed else 'not_assumed' if unassumed else 'not_enacted'),
          '任官約定須保存實行情況未載' if agreed else '稱號提議須明示未實行')
    if unassumed:
        try:
            from scripts.unassumed_appointments import unassumed_appointment_valid
        except ImportError:
            from unassumed_appointments import unassumed_appointment_valid
        check(unassumed_appointment_valid(proposal, chapter), '未赴任須保留任用詞、職稱、同人及未受未行原詞的完整錨點')
    check(proposal.get('status') == 'contextual_provisional'
          and bool(proposal.get('interpretation_note')) and bool(proposal.get('reviewer'))
          and proposal.get('human_reviewed') is False, '稱號提議缺判讀或冒作人工覆核')
    evidence = proposal.get('evidence')
    check(isinstance(evidence, list) and bool(evidence), '稱號提議缺來源證據')
    for e in evidence if isinstance(evidence, list) else []:
        p = next((p for p in chapter['paragraphs'] if p['id'] == e.get('paragraph_id')), None)
        check(bool(p) and e.get('chapter_id') == chapter['id'] and e.get('source_id') == chapter['source_id'], '稱號提議來源不符')
        if not p: continue
        quote = e.get('quote'); starts = [i for i in range(len(p['text']) + 1) if isinstance(quote, str) and quote and p['text'].startswith(quote, i)]
        check(bool(starts), '稱號提議引句不符')
        mentions = {m['id']: m for m in p['mentions']}
        person = mentions.get(proposal.get('person_mention_id'))
        carried_proposal = False
        if unassumed and e.get('context') is not None:
            try:
                from scripts.subject_continuation import prior_subject_valid
            except ModuleNotFoundError:
                from subject_continuation import prior_subject_valid
            context = e['context']
            carried_proposal = prior_subject_valid(context, e, proposal.get('person_id'), chapter)
            if carried_proposal and context.get('person_mention_id') == proposal.get('person_mention_id'):
                prior = next(p for p in chapter['paragraphs'] if p['id'] == context['paragraph_id'])
                person = next((m for m in prior['mentions'] if m['id'] == context['person_mention_id']), None)
            else:
                carried_proposal = False
                check(False, '未赴任省略主語缺少有效前段錨點')
        if agreed:
            def source_anchor(value):
                if not isinstance(value, dict) or set(value) != {'paragraph_id', 'start', 'end', 'surface'}:
                    return None
                start, end = value['start'], value['end']
                return value if (value['paragraph_id'] == p['id'] and type(start) is int and type(end) is int
                    and 0 <= start < end <= len(p['text']) and p['text'][start:end] == value['surface']) else None
            role = source_anchor(proposal.get('role_anchor'))
            agreement = source_anchor(proposal.get('agreement_anchor'))
            check(bool(role) and role['surface'] == proposal.get('title'), '任官約定職稱字元錨點不符')
            check(bool(agreement) and agreement['surface'].startswith('約'), '任官約定須有原約詞錨點')
            clause = '使' + person['surface'] + '為' + proposal['title'] if person and isinstance(proposal.get('title'), str) else None
            check(bool(role) and bool(person) and proposal.get('source_term') == clause
                  and person['start'] > 0 and p['text'][person['start']-1:role['end']] == clause,
                  '任官約定須逐字連到使某人為職的原句')
            check(bool(agreement) and bool(role) and bool(person)
                  and agreement['end'] <= person['start']
                  and any(i <= agreement['start'] and role['end'] <= i + len(quote) for i in starts),
                  '任官約定引句須涵蓋前置約詞及職稱')
        else:
            role = mentions.get(proposal.get('role_mention_id'))
            if unassumed and role and role.get('kind') == 'non_person' and role.get('lexical_role')=='offered_office':
                try: from scripts.unassumed_appointments import unassumed_role
                except ImportError: from unassumed_appointments import unassumed_role
                role=unassumed_role(proposal,p)
            if unassumed and role is None:
                try:
                    from scripts.unassumed_appointments import unassumed_role
                except ImportError:
                    from unassumed_appointments import unassumed_role
                role = unassumed_role(proposal, p)
            check(bool(role) and role.get('kind') == 'unresolved' and role.get('person_id') is None
                  and role.get('surface') == proposal.get('title'), '稱號提議職稱不得當人物')
        check(bool(person) and person.get('kind') == 'person' and person.get('person_id') == proposal.get('person_id'), '稱號提議人物錨點不符')
        check(bool(role) and bool(person) and any(i <= (role['start'] if carried_proposal else min(role['start'], person['start']))
              and (role['end'] if carried_proposal else max(role['end'], person['end'])) <= i + len(quote) for i in starts), '稱號提議引句須涵蓋人物及職稱')
    return errors


def validate(root=ROOT, *, shared_context=True):
    """One content-checked readonly snapshot; uncached mode is the comparison path."""
    try:
        from scripts.validation_context import scope, fingerprint, DRIFT_ERROR
    except ImportError:
        from validation_context import scope, fingerprint, DRIFT_ERROR
    if not shared_context:
        with scope(root, enabled=False):
            return _validate_uncached(root)
    try:
        before = fingerprint(root)
    except (OSError, ValueError) as error:
        return [DRIFT_ERROR + '：' + str(error)]
    with scope(root):
        errors = _validate_uncached(root)
        try:
            after = fingerprint(root)
            if before != after:
                errors.append(DRIFT_ERROR)
        except (OSError, ValueError) as error:
            errors.append(DRIFT_ERROR + '：' + str(error))
        return errors


def _validate_uncached(root=ROOT):
    errors = []
    def check(ok, message):
        if not ok: errors.append(message)
    def read(path):
        return json.loads((root / path).read_text(encoding='utf-8'))
    try:
        registry = read('registry/persons.json')
        catalogue = read('registry/works.json')
        progress = read('corpus/progress.json')
        people = registry['persons']
        pids = [p['id'] for p in people]
        check(len(pids) == len(set(pids)), '人物 ID 重複')
        pids = set(pids)
        try:
            from scripts.person_ids import valid_person_id, LEGACY, FAMILY, LEGACY_FAMILY, family_path_errors
        except ModuleNotFoundError:
            from person_ids import valid_person_id, LEGACY, FAMILY, LEGACY_FAMILY, family_path_errors
        check(all(valid_person_id(pid) for pid in pids), '人物 ID 格式不符')
        check(not any(LEGACY_FAMILY.fullmatch(pid) for pid in pids), '舊連字號家族 ID 只可作別名')
        id_aliases = [alias for person in people for alias in person.get('id_aliases', [])]
        check(len(id_aliases) == len(set(id_aliases)) and not set(id_aliases).intersection(pids), '人物 ID 別名重複或占用正式 ID')
        check(all(valid_person_id(alias) for alias in id_aliases), '人物 ID 別名格式不符')
        try:
            from scripts.retired_person_ids import retired_person_ids
        except ModuleNotFoundError:
            from retired_person_ids import retired_person_ids
        retired_ids = retired_person_ids(root)
        check(not retired_ids.intersection(pids), '已退休人物 ID 不得重新登記為正式人物')
        check(not retired_ids.intersection(id_aliases), '已退休人物 ID 不得重新登記為相容別名')
        migration_path = root / 'registry/person-id-migrations.json'
        if migration_path.exists():
            migration = json.loads(migration_path.read_text())
            alias_targets = {alias: person['id'] for person in people for alias in person.get('id_aliases', [])}
            entries = migration.get('mapping', [])
            check(len(entries) == len(alias_targets)
                  and {e['previous_id']: e['person_id'] for e in entries} == alias_targets,
                  '人物 ID 遷移對照與相容別名不符')
            retirement = migration.get('alias_retirement')
            if retirement:
                check(retirement.get('status') == 'retired_after_reference_update'
                      and retirement.get('active_reference_count') == 0
                      and type(retirement.get('retired_alias_count')) is int
                      and retirement['retired_alias_count'] > 0
                      and not alias_targets and not entries,
                      '舊 ID 撤除後不得殘留相容別名或遷移對照')
            migration_count = migration.get('person_count')
            check(type(migration_count) is int
                  and len(set(alias_targets.values())) <= migration_count <= len(people)
                  and migration.get('person_count_scope', 'at_migration') == 'at_migration'
                  and migration.get('identity_merges_performed') is False
                  and all(FAMILY.fullmatch(pid) for pid in pids), '人物 ID 全面遷移範圍或身份政策不符')
        legacy_numbers = [int(pid[5:]) for pid in pids if isinstance(pid, str) and LEGACY.fullmatch(pid)]
        check(registry['next_number'] > max(legacy_numbers, default=0), '舊人物 ID 分配游標會重用 ID')
        works = {w['id']: w for w in catalogue['works']}
        check(len(works) == len(catalogue['works']), '著作 ID 重複')
        books = {}
        chapter_books = {}
        for wid, w in works.items():
            for b in w['books']:
                check(b['id'] not in books, '卷 ID 重複')
                books[b['id']] = b
                check(b['work_id'] == wid, '卷的著作 ID 不符')
                for cid in b['chapter_ids']:
                    check(cid not in chapter_books, '篇 ID 屬於多卷')
                    chapter_books[cid] = b['id']
        try:
            from scripts.table_evidence import load_tables, table_evidence_errors, table_title_range_errors, table_regnal_range_errors
        except ModuleNotFoundError:
            from table_evidence import load_tables, table_evidence_errors, table_title_range_errors, table_regnal_range_errors
        tables = load_tables(root)
        table_chapters = {table['source']['chapter_id']: table for table in tables.values()}
        check(len(table_chapters) == len(tables), '表格證據篇ID重複')
        for table in tables.values():
            source = table['source']
            check(source['work_id'] in works
                  and chapter_books.get(source['chapter_id']) == source['book_id']
                  and books.get(source['book_id'], {}).get('work_id') == source['work_id'],
                  '表格證據著作卷篇未登記或歸屬不符')
        mentions = {}; paragraphs = {}; chapters = {}; files = {}
        case_paragraphs = {}
        for candidate_path in sorted((root / 'corpus').glob('*/*.json')):
            candidate = json.loads(candidate_path.read_text(encoding='utf-8'))
            if candidate.get('record_type') == 'marked_chapter':
                case_paragraphs.update({p['id']: p for p in candidate['paragraphs']})
        for path in sorted((root / 'corpus').glob('*/*.json')):
            d = json.loads(path.read_text(encoding='utf-8'))
            if d.get('record_type') != 'marked_chapter': continue
            cid = d['id']; files[cid] = path
            check(cid not in chapters, '篇 ID 重複')
            chapters[cid] = d
            check(d['work_id'] in works, f'{cid}: 著作不存在')
            check(chapter_books.get(cid) == d['book_id'], f'{cid}: 卷篇歸屬不符')
            check(books.get(d['book_id'], {}).get('work_id') == d['work_id'], f'{cid}: 卷著作歸屬不符')
            for key in ('url','permalink','license_url'):
                u=urlparse(d['source'][key]); check(u.scheme in ('http','https') and bool(u.netloc), f'{cid}: 來源網址無效')
            digest = hashlib.sha256('\n\n'.join(p['text'] for p in d['paragraphs']).encode('utf-8')).hexdigest()
            check(digest == d['text_sha256'], f'{cid}: 文本 SHA-256 不符')
            for p in d['paragraphs']:
                check(p['id'] not in paragraphs, '段落 ID 重複')
                check(p['id'].startswith(cid + ':'), '段落 ID 不屬於篇')
                paragraphs[p['id']] = (cid,p)
                last=0
                for m in p['mentions']:
                    check(m['id'] not in mentions, '提及 ID 重複')
                    mentions[m['id']] = (cid,p['id'],m)
                    check(isinstance(m['start'],int) and isinstance(m['end'],int) and 0 <= m['start'] < m['end'] <= len(p['text']), '提及字元位置無效')
                    check(m['start'] >= last, '提及位置重疊或未排序')
                    check(p['text'][m['start']:m['end']] == m['surface'], '提及引句與位置不符')
                    last=m['end']
                    if m['kind'] == 'person':
                        check(m['person_id'] in pids, '提及引用未知人物 ID')
                        if not any(ch.isalnum() for ch in m['surface']):
                            try: from scripts.nan023_wanghuan import pua_zhou_valid
                            except ImportError: from nan023_wanghuan import pua_zhou_valid
                            check(pua_zhou_valid(d, p, m, root), '人物提及不得僅為標點或空白')
                    elif m['kind'] == 'unresolved': check(m['person_id'] is None and m['status']=='unresolved', '未定提及不得暗選人物')
                    elif m['kind'] == 'non_person':
                        try:
                            from scripts.lexical_annotations import non_person_errors
                        except ModuleNotFoundError:
                            from lexical_annotations import non_person_errors
                        errors.extend(non_person_errors(m, p['text']))
                    elif m['kind'] == 'work':
                        check(m.get('person_id') is None and m.get('work_id') in works and m.get('status') in ('source_explicit', 'contextual_provisional'), '著作提及須引用已登記著作且不得連人物')
                    else: check(False,'未知提及類型')
            try:
                from scripts.work_reference_resolution import chapter_errors as work_reference_errors
            except ModuleNotFoundError:
                from work_reference_resolution import chapter_errors as work_reference_errors
            errors.extend(work_reference_errors(d))
            try:
                from scripts.fixed_wikisource_units import source_errors as fixed_wikisource_unit_errors
            except ImportError:
                from fixed_wikisource_units import source_errors as fixed_wikisource_unit_errors
            errors.extend(fixed_wikisource_unit_errors(d, root))
            try:
                from scripts.fixed_kanripo_projection import errors as fixed_kanripo_projection_errors
            except ImportError:
                from fixed_kanripo_projection import errors as fixed_kanripo_projection_errors
            try: from scripts.wang_family_women_sources import errors as wang_women_source_errors
            except ImportError: from wang_family_women_sources import errors as wang_women_source_errors
            errors.extend(wang_women_source_errors(d, root))
            try: from scripts.wyd_song071_wang import errors as vyd71_source_errors
            except ImportError: from wyd_song071_wang import errors as vyd71_source_errors
            try: from scripts.wyd_song063_wangtanshou import errors as wyd63_source_errors
            except ImportError: from wyd_song063_wangtanshou import errors as wyd63_source_errors
            errors.extend(wyd63_source_errors(d, root))
            try: from scripts.song063_wanghua_reading import errors as wanghua_errors
            except ImportError: from song063_wanghua_reading import errors as wanghua_errors
            errors.extend(wanghua_errors(d, root))
            try:
                from scripts.qi036_xiechaozong import errors as qi36_chao_errors
            except ImportError:
                from qi036_xiechaozong import errors as qi36_chao_errors
            errors.extend(qi36_chao_errors(d, root))
            try: from scripts.liang050_xie_witnesses import errors as liang50_xie_errors
            except ImportError: from liang050_xie_witnesses import errors as liang50_xie_errors
            errors.extend(liang50_xie_errors(d, root))
            try: from scripts.jin096_xiedaoyun import errors as daoyun96_errors
            except ImportError: from jin096_xiedaoyun import errors as daoyun96_errors
            errors.extend(daoyun96_errors(d, root))
            try: from scripts.jin096_zhong_and_guan import errors as jin96_zhong_errors
            except ImportError: from jin096_zhong_and_guan import errors as jin96_zhong_errors
            errors.extend(jin96_zhong_errors(d, root))
            errors.extend(vyd71_source_errors(d, root))
            try: from scripts.nanshi024_wangsiyuan import errors as nan24siy_errors
            except ImportError: from nanshi024_wangsiyuan import errors as nan24siy_errors
            errors.extend(nan24siy_errors(d,root))
            try: from scripts.nanshi024_guhaozhi import errors as nan24gh_errors
            except ImportError: from nanshi024_guhaozhi import errors as nan24gh_errors
            errors.extend(nan24gh_errors(d,root))
            try: from scripts.nanshi024_wangyan_brothers import errors as nan24wab_errors
            except ImportError: from nanshi024_wangyan_brothers import errors as nan24wab_errors
            errors.extend(nan24wab_errors(d,root))
            try: from scripts.nanshi024_wangyan import errors as nan24yan_errors
            except ImportError: from nanshi024_wangyan import errors as nan24yan_errors
            errors.extend(nan24yan_errors(d,root))
            try: from scripts.xiangshan_m9_epitaphs import errors as xm9_errors
            except ImportError: from xiangshan_m9_epitaphs import errors as xm9_errors
            errors.extend(xm9_errors(d,root))
            try: from scripts.nanshi024_wangmeng import errors as nan24meng_errors
            except ImportError: from nanshi024_wangmeng import errors as nan24meng_errors
            errors.extend(nan24meng_errors(d,root))
            try: from scripts.song093_wyd import errors as s93wyd_source
            except ImportError: from song093_wyd import errors as s93wyd_source
            errors.extend(s93wyd_source(d,root))
            try: from scripts.song093_wanghongzhi import errors as hongzhi_source_errors
            except ImportError: from song093_wanghongzhi import errors as hongzhi_source_errors
            errors.extend(hongzhi_source_errors(d,root))
            try: from scripts.song093_wangtansheng import errors as tansheng_source_errors, song_errors as tansheng_song_errors
            except ImportError: from song093_wangtansheng import errors as tansheng_source_errors, song_errors as tansheng_song_errors
            errors.extend(tansheng_source_errors(d, root))
            errors.extend(tansheng_song_errors(d, root))
            try: from scripts.nanshi024_wanghongzhi import errors as nan24hong_errors
            except ImportError: from nanshi024_wanghongzhi import errors as nan24hong_errors
            errors.extend(nan24hong_errors(d,root))
            try: from scripts.nanshi024_ruanwanling import errors as nan24rw_errors
            except ImportError: from nanshi024_ruanwanling import errors as nan24rw_errors
            errors.extend(nan24rw_errors(d,root))
            try: from scripts.nanshi024_wangsu import errors as nan24su_errors
            except ImportError: from nanshi024_wangsu import errors as nan24su_errors
            errors.extend(nan24su_errors(d,root))
            try: from scripts.nanshi024_wangqunzhi import errors as nan24qun_errors
            except ImportError: from nanshi024_wangqunzhi import errors as nan24qun_errors
            errors.extend(nan24qun_errors(d,root))
            try: from scripts.nanshi024_wangqing import errors as nan24qing_errors
            except ImportError: from nanshi024_wangqing import errors as nan24qing_errors
            errors.extend(nan24qing_errors(d,root))
            try: from scripts.nanshi024_wangjinzhi import errors as nan24jz_errors
            except ImportError: from nanshi024_wangjinzhi import errors as nan24jz_errors
            errors.extend(nan24jz_errors(d,root))
            try: from scripts.nanshi024_wangzhunzhi import errors as nan24zz_errors
            except ImportError: from nanshi024_wangzhunzhi import errors as nan24zz_errors
            errors.extend(nan24zz_errors(d,root))
            try: from scripts.nanshi024_wangyuezhi import errors as nan24yz_errors
            except ImportError: from nanshi024_wangyuezhi import errors as nan24yz_errors
            errors.extend(nan24yz_errors(d,root))
            try: from scripts.nanshi024_wangshaozhi_wyd import errors as n24szwyd_source
            except ImportError: from nanshi024_wangshaozhi_wyd import errors as n24szwyd_source
            errors.extend(n24szwyd_source(d,root))
            try: from scripts.nanshi024_wangshaozhi import errors as nan24sz_errors
            except ImportError: from nanshi024_wangshaozhi import errors as nan24sz_errors
            errors.extend(nan24sz_errors(d,root))
            try: from scripts.nanqi047_xietiao_wife import errors as qi47wife_errors
            except ImportError: from nanqi047_xietiao_wife import errors as qi47wife_errors
            errors.extend(qi47wife_errors(d,root))
            try: from scripts.nanqi047_wangrong_wyd import errors as q47wyd_source
            except ImportError: from nanqi047_wangrong_wyd import errors as q47wyd_source
            errors.extend(q47wyd_source(d,root))
            try: from scripts.nanshi059_wangsengru import errors as nan59sr_errors
            except ImportError: from nanshi059_wangsengru import errors as nan59sr_errors
            errors.extend(nan59sr_errors(d,root))
            try: from scripts.liang033_wangsengru import errors as liang33sr_errors
            except ImportError: from liang033_wangsengru import errors as liang33sr_errors
            errors.extend(liang33sr_errors(d,root))
            try: from scripts.nanqi047_wangrong import errors as qi47rong_errors
            except ImportError: from nanqi047_wangrong import errors as qi47rong_errors
            errors.extend(qi47rong_errors(d,root))
            try: from scripts.nan023_wangyu import errors as nan23yu_errors
            except ImportError: from nan023_wangyu import errors as nan23yu_errors
            errors.extend(nan23yu_errors(d,root))
            try: from scripts.nan023_wanghou import errors as nan23hou_errors
            except ImportError: from nan023_wanghou import errors as nan23hou_errors
            errors.extend(nan23hou_errors(d,root))
            try: from scripts.nan023_wanggu import errors as nan23gu_errors
            except ImportError: from nan023_wanggu import errors as nan23gu_errors
            errors.extend(nan23gu_errors(d,root))
            try: from scripts.nan023_wangzhi import errors as nan23zhi_errors
            except ImportError: from nan023_wangzhi import errors as nan23zhi_errors
            errors.extend(nan23zhi_errors(d,root))
            try: from scripts.nan023_wangmai import errors as nan23mai_errors
            except ImportError: from nan023_wangmai import errors as nan23mai_errors
            errors.extend(nan23mai_errors(d,root))
            try: from scripts.nan023_wangtong import errors as nan23tong_errors
            except ImportError: from nan023_wangtong import errors as nan23tong_errors
            errors.extend(nan23tong_errors(d,root))
            try: from scripts.nan023_wangxi import errors as nan23xi_errors
            except ImportError: from nan023_wangxi import errors as nan23xi_errors
            errors.extend(nan23xi_errors(d,root))
            try: from scripts.nan023_wangfen import errors as nan23fen_errors
            except ImportError: from nan023_wangfen import errors as nan23fen_errors
            errors.extend(nan23fen_errors(d,root))
            try: from scripts.nan023_wanghuan import errors as nan23huan_errors
            except ImportError: from nan023_wanghuan import errors as nan23huan_errors
            errors.extend(nan23huan_errors(d,root))
            try: from scripts.nan023_wangyun import errors as nan23yun_errors
            except ImportError: from nan023_wangyun import errors as nan23yun_errors
            errors.extend(nan23yun_errors(d,root))
            try: from scripts.nan023_chuzhanzhi import errors as nan23chu_errors
            except ImportError: from nan023_chuzhanzhi import errors as nan23chu_errors
            errors.extend(nan23chu_errors(d,root))
            try: from scripts.nan023_wanghui_sons import errors as nan23huiz_errors
            except ImportError: from nan023_wanghui_sons import errors as nan23huiz_errors
            errors.extend(nan23huiz_errors(d,root))
            try: from scripts.nan023_wangxuan import errors as nan23xuan_errors
            except ImportError: from nan023_wangxuan import errors as nan23xuan_errors
            errors.extend(nan23xuan_errors(d,root))
            try: from scripts.nan023_wangqiu import errors as nan23qiu_errors
            except ImportError: from nan023_wangqiu import errors as nan23qiu_errors
            errors.extend(nan23qiu_errors(d,root))
            try: from scripts.nan023_wanghui import errors as nan23hui_errors
            except ImportError: from nan023_wanghui import errors as nan23hui_errors
            errors.extend(nan23hui_errors(d,root))
            try: from scripts.nan023_wangliang import errors as nan23liang_errors
            except ImportError: from nan023_wangliang import errors as nan23liang_errors
            errors.extend(nan23liang_errors(d,root))
            try: from scripts.nan023_wangying import errors as nan23ying_errors
            except ImportError: from nan023_wangying import errors as nan23ying_errors
            errors.extend(nan23ying_errors(d,root))
            try: from scripts.nan023_wangzao import errors as nan23zao_errors
            except ImportError: from nan023_wangzao import errors as nan23zao_errors
            errors.extend(nan23zao_errors(d,root))
            try: from scripts.nan023_heyu import errors as nan23heyu_errors
            except ImportError: from nan023_heyu import errors as nan23heyu_errors
            errors.extend(nan23heyu_errors(d,root))
            try: from scripts.nan023_jiangxiao import errors as nan23jiang_errors
            except ImportError: from nan023_jiangxiao import errors as nan23jiang_errors
            errors.extend(nan23jiang_errors(d,root))
            try: from scripts.nan023_chuai import errors as nan23chuai_errors
            except ImportError: from nan023_chuai import errors as nan23chuai_errors
            errors.extend(nan23chuai_errors(d,root))
            try: from scripts.nan023_wangmao import errors as nan23mao_errors
            except ImportError: from nan023_wangmao import errors as nan23mao_errors
            errors.extend(nan23mao_errors(d,root))
            try: from scripts.nan023_print import errors as nan23p_errors
            except ImportError: from nan023_print import errors as nan23p_errors
            errors.extend(nan23p_errors(d,root))
            try: from scripts.nan023_digital import errors as nan23dan_errors
            except ImportError: from nan023_digital import errors as nan23dan_errors
            errors.extend(nan23dan_errors(d,root))
            try: from scripts.song052_wangdan import errors as wangdan52_errors
            except ImportError: from song052_wangdan import errors as wangdan52_errors
            errors.extend(wangdan52_errors(d,root))
            try: from scripts.song052_xieshu import errors as xieshu52_errors
            except ImportError: from song052_xieshu import errors as xieshu52_errors
            errors.extend(xieshu52_errors(d,root))
            try: from scripts.song052_xiejingren import errors as xiejingren52_errors
            except ImportError: from song052_xiejingren import errors as xiejingren52_errors
            errors.extend(xiejingren52_errors(d,root))
            try: from scripts.song052_xiechun import errors as chun52_errors
            except ImportError: from song052_xiechun import errors as chun52_errors
            errors.extend(chun52_errors(d,root))
            try: from scripts.liang021_wangjiansihui import errors as sih21_errors
            except ImportError: from liang021_wangjiansihui import errors as sih21_errors
            errors.extend(sih21_errors(d,root))
            try: from scripts.liang021_wangxun import errors as xun21_errors
            except ImportError: from liang021_wangxun import errors as xun21_errors
            errors.extend(xun21_errors(d,root))
            try: from scripts.liang021_wangfen_family import errors as wf21_errors
            except ImportError: from liang021_wangfen_family import errors as wf21_errors
            errors.extend(wf21_errors(d,root))
            try: from scripts.liang021_wangjun import errors as j21_errors
            except ImportError: from liang021_wangjun import errors as j21_errors
            errors.extend(j21_errors(d,root))
            try: from scripts.liang021_wangtai_readings import errors as tai21_read_errors
            except ImportError: from liang021_wangtai_readings import errors as tai21_read_errors
            errors.extend(tai21_read_errors(d,root))
            try: from scripts.liang033_wangyun_witness import errors as liang33_errors
            except ImportError: from liang033_wangyun_witness import errors as liang33_errors
            errors.extend(liang33_errors(d, root))
            try: from scripts.wangyun_external_sources import errors as wangyun_external_errors
            except ImportError: from wangyun_external_sources import errors as wangyun_external_errors
            errors.extend(wangyun_external_errors(d, root))
            try: from scripts.liang021_print_columns import errors as liang21_print_errors
            except ImportError: from liang021_print_columns import errors as liang21_print_errors
            errors.extend(liang21_print_errors(d, root))
            try: from scripts.qi020_huiduan import wenxuan_errors
            except ImportError: from qi020_huiduan import wenxuan_errors
            errors.extend(wenxuan_errors(d, root))
            try: from scripts.qi020_chulingqu import shaoxing_witness_errors
            except ImportError: from qi020_chulingqu import shaoxing_witness_errors
            errors.extend(shaoxing_witness_errors(d, root))
            try: from scripts.ws_song071_wang import errors as vws71_source_errors
            except ImportError: from ws_song071_wang import errors as vws71_source_errors
            errors.extend(vws71_source_errors(d, root))
            errors.extend(fixed_kanripo_projection_errors(d, root))
            try: from scripts.qi023_wangjian_witnesses import errors as qi23_source_errors
            except ImportError: from qi023_wangjian_witnesses import errors as qi23_source_errors
            errors.extend(qi23_source_errors(d,root))
            try: from scripts.nanshi022_wangjian_source import errors as nan22_jian_errors
            except ImportError: from nanshi022_wangjian_source import errors as nan22_jian_errors
            errors.extend(nan22_jian_errors(d,root))
            try: from scripts.pei_royal_biographies import errors as pei_source_errors
            except ImportError: from pei_royal_biographies import errors as pei_source_errors
            errors.extend(pei_source_errors(d,root))
            try:
                from scripts.nanshi022_print import errors as nanshi022_print_errors
            except ImportError:
                from nanshi022_print import errors as nanshi022_print_errors
            errors.extend(nanshi022_print_errors(d, root))
            # fixed-wuyingdian-song044-transcription: source-only exact witness gate.
            try:
                from scripts.fixed_wuyingdian_song044 import source_errors as wuyingdian_song044_errors
            except ImportError:
                from fixed_wuyingdian_song044 import source_errors as wuyingdian_song044_errors
            wuyingdian_issues = wuyingdian_song044_errors(d, root)
            errors.extend(wuyingdian_issues)
            try:
                from scripts.wyd_song044_formal_roles import source_errors as wyd_formal_role_errors
            except ImportError:
                from wyd_song044_formal_roles import source_errors as wyd_formal_role_errors
            errors.extend(wyd_formal_role_errors(d, root))
            wuyingdian_song044_layer_valid = (d.get('id') == 'c-songshu-044-wyd1739-xiehui'
                and isinstance(d.get('annotation'),dict) and d.get('annotation', {}).get('fixed_transcription_contract') == 'wuyingdian_song044_transcription'
                and not wuyingdian_issues)
            if any('annotation_status' in p for p in d['paragraphs']):
                for p in d['paragraphs']:
                    check(p.get('annotation_status') in ('pending','in_progress','named_mentions_first_pass','reviewed'),'段落標註狀態無效或缺失')
                    if p.get('annotation_status')=='pending':check(not p['mentions'],'待標註段落不得混入已接受的提及')
                if any(p.get('annotation_status') in ('pending','in_progress') for p in d['paragraphs']):
                    check(d['annotation']['status']=='in_progress','篇仍有待標註段落，不得宣稱首輪完成')
            try:
                from scripts.referent_interpretations import interpretation_errors
            except ModuleNotFoundError:
                from referent_interpretations import interpretation_errors
            errors.extend(interpretation_errors(d, pids))
            try:
                from scripts.person_references import reference_errors
            except ModuleNotFoundError:
                from person_references import reference_errors
            errors.extend(reference_errors(d, pids))
            try:
                from scripts.source_excerpts import excerpt_errors
            except ImportError:
                from source_excerpts import excerpt_errors
            errors.extend(excerpt_errors(d))
            try:
                from scripts.biographical_kinship import digital_paratext_errors
            except ImportError:
                from biographical_kinship import digital_paratext_errors
            errors.extend(digital_paratext_errors(d))
            try:
                from scripts.epitaph_transcription_witness import errors as epitaph_witness_errors
            except ImportError:
                from epitaph_transcription_witness import errors as epitaph_witness_errors
            errors.extend(epitaph_witness_errors(d, root, works, books))
            case_ids=set()
            for case in d['annotation'].get('unresolved_identity_cases',[]):
                check(case.get('id') and case['id'] not in case_ids,'未決身份 ID 無效或重複')
                case_ids.add(case.get('id'))
                candidates=case.get('candidate_person_ids',[])
                unknown = case.get('unknown_identity_possible') is True
                check(len(candidates)>=(1 if unknown or case.get('candidate_list_exhaustive') is False else 2) and len(set(candidates))==len(candidates) and all(pid in pids for pid in candidates),'未決身份候選人物無效')
                check(case.get('status')=='unresolved' and bool(case.get('note')),'未決身份狀態或說明缺失')
                if 'candidate_list_exhaustive' in case:
                    check(type(case['candidate_list_exhaustive']) is bool, '候選名單是否窮盡須明示布林值')
                refs=case.get('paragraph_ids',[])
                local={p['id']:p for p in d['paragraphs']}
                check(bool(refs) and any(ref in local for ref in refs) and all(ref in case_paragraphs for ref in refs),'未決身份段落引用無效')
                supported={m['person_id'] for ref in refs if ref in case_paragraphs for m in case_paragraphs[ref]['mentions'] if m['kind']=='person'}
                if 'person_reference_ids' in case:
                    requested=case['person_reference_ids']
                    bound=[r for r in d['annotation'].get('person_reference_occurrences',[]) if r['id'] in requested and r['paragraph_id'] in refs and r['person_id'] in candidates]
                    check(bool(requested) and len(bound)==len(set(requested))==len(requested),'未決身份指代須逐一對應本篇候選、段落及原字位')
                    supported.update(r['person_id'] for r in bound)
                check(set(candidates)<=supported,'未決身份缺少各候選人物的段落證據')
                if unknown:
                    unresolved = case.get('unresolved_mention_ids', [])
                    anchors = {m['id']: m for ref in refs if ref in case_paragraphs for m in case_paragraphs[ref]['mentions']}
                    check(bool(unresolved) and len(unresolved)==len(set(unresolved))
                          and all(mid in anchors and anchors[mid]['kind']=='unresolved'
                                  and anchors[mid].get('person_id') is None for mid in unresolved),
                          '未知敘者可能須有未連人物的原文錨點')
            xml=ET.parse(path.with_suffix('.xml')).getroot()
            check(xml.tag=='text', 'XML 根元素不符')
            for attr,key in [('work-id','work_id'),('book-id','book_id'),('chapter-id','id'),('source-id','source_id')]:
                check(xml.get(attr)==d[key], 'XML 著作卷篇來源 ID 不符')
            xp=xml.findall('p')
            check(len(xp)==len(d['paragraphs']), 'XML 段落數不符')
            try:
                from scripts.reading_layout import partition
            except ImportError:
                from reading_layout import partition
            for x,(p,reading_role,reading_index) in zip(xp,partition(d)):
                check(x.get('reading-role')==reading_role and x.get('reading-index')==(str(reading_index) if reading_index is not None else None),'XML 閱讀角色／次序不符')
                check(x.get('id')==p['id'] and ''.join(x.itertext())==p['text'], 'XML 正文還原與 JSON 不符')
                check(x.get('annotation-status')==p.get('annotation_status'),'XML 段落標註狀態不符')
                check(x.get('text-layer')==p.get('text_layer'),'XML 文字層次不符')
                try:
                    from scripts.liuxiaobiao_layers import valid as liuxiaobiao_layer_valid
                except ImportError:
                    from liuxiaobiao_layers import valid as liuxiaobiao_layer_valid
                try:
                    from scripts.jin065_wangdao_main import formal_comment as wangdao_formal_comment
                except ImportError:
                    from jin065_wangdao_main import formal_comment as wangdao_formal_comment
                try:
                    from scripts.jin065_appraisal_layers import valid as jin065_appraisal_layer
                except ImportError:
                    from jin065_appraisal_layers import valid as jin065_appraisal_layer
                try:
                    from scripts.jin080_xumai import appraisal_valid as jin080_appraisal_valid
                except ImportError:
                    from jin080_xumai import appraisal_valid as jin080_appraisal_valid
                try: from scripts.nan023_wangxuan import editorial_note as nan23xuan_editorial_note
                except ImportError: from nan023_wangxuan import editorial_note as nan23xuan_editorial_note
                if 'text_layer' in p: check(nan23xuan_editorial_note(p,d,root) or p['text_layer'] in ('received_chapter','epitaph_as_modernly_transcribed','witness_appended_pei_songzhi_note','witness_appended_bangu_note','witness_appended_suoyin_zan','witness_appended_chu_note','witness_appended_zhengyi_note','witness_appended_edict','witness_duyu_annotation_excerpt','witness_received_text_and_duyu_annotation_excerpt','witness_peisongzhi_quoted_simabiao_xuzhuan','witness_appended_lixian_note','witness_appended_liuban_collation','witness_appended_qing_siku_collation') or (p.get('text_layer') == 'witness_appended_liuxiaobiao_note' and (liuxiaobiao_layer_valid(p, d, root) or wangdao_formal_comment(p, d, root))) or (p.get('text_layer') == 'received_compiler_appraisal' and jin065_appraisal_layer(p,d,root)) or (p.get('text_layer') == 'received_compiler_appraisal' and jin080_appraisal_valid(p,d,root)) or (p.get('text_layer') in ('received_compiler_appraisal','witness_appended_wuyingdian_collation') and wuyingdian_song044_layer_valid),'文字層次無效')
                try:
                    from scripts.houhan_text_layers import layer_errors
                except ImportError:
                    from houhan_text_layers import layer_errors
                for issue in layer_errors(p): check(False,issue)
                xm=list(x)
                check(len(xm)==len(p['mentions']), 'XML 提及數不符')
                check(all(e.tag in ('persName','rs','title','seg') for e in x),'XML 含未知正文標籤')
                for e,m in zip(xm,p['mentions']):
                    check(e.get('id')==m['id'] and e.text==m['surface'], 'XML 提及錨點不符')
                    check(e.tag==({'person':'persName','work':'title','non_person':'seg'}.get(m['kind'], 'rs')), 'XML 提及類型不符')
                    check(e.get('ref')==(m.get('work_id') if m['kind']=='work' else m['person_id']), 'XML 人物或著作引用不符')
                    if m['kind']=='unresolved': check(e.get('type')=='unresolved','XML 未定類型不符')
                    if m['kind']=='non_person': check(e.get('type')=='non-person' and e.get('subtype')==m.get('lexical_role'),'XML 非人物詞性不符')
        check(not set(chapters).intersection(table_chapters), '正文與表格篇ID不得重複')
        check(set(chapter_books)==set(chapters) | set(table_chapters), '著作目錄與文本篇清單不符')
        for wid, work in works.items():
            if work.get('status') != 'referenced_only':
                continue
            evidence = work.get('reference_attestations', [])
            check(bool(evidence) and not work['books'], '僅被引用著作須有原文證據且不得冒作已匯入正文')
            for item in evidence:
                hit = mentions.get(item.get('mention_id'))
                check(bool(hit) and hit[0] == item.get('chapter_id')
                      and hit[1] == item.get('paragraph_id')
                      and hit[2].get('kind') == 'work' and hit[2].get('work_id') == wid
                      and chapters.get(hit[0], {}).get('source_id') == item.get('source_id')
                      and paragraphs.get(hit[1], (None, {}))[1].get('text') == item.get('quote'),
                      '著作登記證據須對應同一書名錨點及完整原文')
        # source-author-prefix: validate literal source authorship roles.
        try:
            from scripts.source_author_prefix import source_author_errors
        except ImportError:
            from source_author_prefix import source_author_errors
        for issue in source_author_errors(works, chapters):
            check(False, issue)
        kinship_case_ids = set()
        for chapter in chapters.values():
            for case in chapter['annotation'].get('kinship_interpretation_cases', []):
                check(case['id'] not in kinship_case_ids, '親屬詮釋案例ID重複'); kinship_case_ids.add(case['id'])
                endpoints = {case['subject_person_id'], case['object_person_id']}
                check(len(endpoints) == 2 and endpoints.issubset(pids), '親屬詮釋端點無效')
                check(case['status'] == 'interpretation_disputed' and case['human_reviewed'] is False, '親屬分歧不得冒作人工審閱')
                check(len(case['alternatives']) >= 2 and len({a['id'] for a in case['alternatives']}) == len(case['alternatives']), '親屬詮釋選項不足或重複')
                if case['default_alternative_id'] is not None:
                    selection = case.get('selection', {})
                    check(case['default_alternative_id'] in {a['id'] for a in case['alternatives']}
                          and selection.get('status') == 'editorial_preferred'
                          and selection.get('confidence_level') in ('high', 'moderate', 'low')
                          and bool(selection.get('rationale')) and bool(selection.get('reviewer'))
                          and selection.get('human_reviewed') is False, '親屬預設選項須匹配候選並附編輯判斷')
                    for evidence in selection.get('comparative_evidence', []):
                        hit = paragraphs.get(evidence['paragraph_id'])
                        check(bool(hit) and hit[0] == evidence['chapter_id']
                              and evidence['quote'] in hit[1]['text']
                              and chapters[hit[0]]['source_id'] == evidence['source_id'], '親屬語義比較引句或來源不符')
                check(bool(case['evidence']) and bool(case['source_term']) and bool(case['interpretation_note']), '親屬詮釋缺少原詞或證據')
                for evidence in case['evidence']:
                    hit = paragraphs.get(evidence['paragraph_id'])
                    check(bool(hit) and hit[0] == chapter['id'] == evidence['chapter_id']
                          and evidence['quote'] == hit[1]['text'] and case['source_term'] in evidence['quote']
                          and evidence['source_id'] == chapter['source_id'], '親屬詮釋引句或篇來源不符')
                    if hit:
                        local = {m['person_id'] for m in hit[1]['mentions'] if m['kind'] == 'person'}
                        check(endpoints.issubset(local), '親屬詮釋兩端未見於正文證據')
                for alternative in case['alternatives']:
                    predicate = alternative['predicate']; qualifiers = alternative['qualifiers']; reference = alternative['reference']
                    check(predicate in ('maternal_uncle', 'brother'), '親屬詮釋關係未知')
                    check(type(qualifiers.get('object_generation_relative_to_subject')) is int
                          and qualifiers['object_generation_relative_to_subject'] == (-1 if predicate == 'maternal_uncle' else 0), '親屬詮釋世代方向不符')
                    check(bool(reference.get('quote')) and bool(reference.get('commentator'))
                          and reference.get('url', '').startswith(('https://', 'http://'))
                          and reference.get('image_verified') is False, '親屬詮釋注語署名來源不完整')
            for variant in chapter['annotation'].get('reported_variants', []):
                hit = paragraphs.get(variant['paragraph_id'])
                check(bool(hit) and hit[0] == chapter['id'] and variant['source_term'] in hit[1]['text'], '所報異文原詞與正文不符')
                check(set(variant['person_ids']).issubset(pids) and bool(variant['person_ids']), '所報異文人物無效')
                check(variant['status'] == 'reported_not_collated' and variant['adopted'] is False
                      and variant['received_reading'] in variant['source_term']
                      and variant['reported_reading'] in variant['quote'], '所報異文未區分原文或冒作採用')
                check(bool(variant['commentator']) and variant['url'].startswith(('https://', 'http://')), '所報異文缺注家來源')
                errors.extend(reported_relationship_errors(variant, hit[1] if hit else None))
        family_relations = [a for path in (root / 'corpus').glob('*/*-assertions.json')
                            for a in json.loads(path.read_text()).get('assertions', [])]
        assertion_index = {a['id']: a for a in family_relations}
        try:
            from scripts.unresolved_relation_identity import group_errors
        except ImportError:
            from unresolved_relation_identity import group_errors
        for grouped_chapter in chapters.values():
            errors.extend(group_errors(grouped_chapter, assertion_index, pids, chapters))
        equivalence_index = {d['id']: d for path in (root / 'corpus').glob('*/*-equivalences.json')
                             for d in json.loads(path.read_text()).get('decisions', [])}
        try:
            from scripts.relative_birth_order_decisions import decision_errors as relative_order_errors
        except ImportError:
            from relative_birth_order_decisions import decision_errors as relative_order_errors
        errors.extend(relative_order_errors(root, chapters, assertion_index, pids))
        try:
            from scripts.song047_title_semantics import unresolved_title_errors
        except ImportError:
            from song047_title_semantics import unresolved_title_errors
        for chapter in chapters.values():
            errors.extend(unresolved_title_errors(chapter, pids))
        tree_decision_ids = set()
        for path in (root / 'corpus').glob('*/family-tree-decisions.json'):
            record = json.loads(path.read_text())
            check(record.get('record_type') == 'family_tree_decision_set', '編輯世系集類型無效')
            for decision in record['decisions']:
                check(decision['id'] not in tree_decision_ids, '編輯世系決定 ID 重複'); tree_decision_ids.add(decision['id'])
                check(decision['subject_person_id'] in pids
                      and decision['subject_person_id'] in decision['participant_person_ids']
                      and set(decision['participant_person_ids']).issubset(pids), '編輯世系人物端點無效')
                check(decision['status'] == 'editorial_preferred' and decision['human_reviewed'] is False
                      and bool(decision['rationale']) and bool(decision['reviewer'])
                      and decision['confidence_level'] in ('high', 'moderate', 'low', 'inconclusive'), '編輯世系缺少判斷或可信程度')
                preferred = assertion_index.get(decision['preferred_assertion_id'])
                subject_ids = set(decision.get('subject_person_ids', [decision['subject_person_id']]))
                check(decision['subject_person_id'] in subject_ids and subject_ids.issubset(set(decision['participant_person_ids'])), '編輯世系同指端點無效')
                if len(subject_ids) > 1:
                    eqs = [equivalence_index.get(eid) for eid in decision.get('identity_equivalence_decision_ids', [])]
                    check(bool(eqs) and all(eqs) and any(subject_ids.issubset(set(eq['person_ids'])) for eq in eqs if eq), '編輯世系跨候選須有同指依據')
                if decision['preferred_assertion_id'] is not None:
                    check(bool(preferred) and preferred['subject_person_id'] == decision['subject_person_id']
                          and preferred['object_person_id'] == decision['preferred_parent_person_id']
                          and decision['default_view'] in ('use_preferred_parent_edge', 'use_preferred_legal_parent_edge'), '預設世系未匹配來源陳述')
                    if decision['default_view'] == 'use_preferred_legal_parent_edge':
                        check(decision['parentage_role'] == 'legal_or_dynastic' and decision.get('biological_parent_status') == 'unknown', '王室父子不得混同已核生父')
                else:
                    check(decision['preferred_parent_person_id'] is None
                          and decision['default_view'] == 'omit_unproven_biological_parent_edge', '生父未定決定不得暗補父親')
                for aid in decision['excluded_assertion_ids']:
                    assertion = assertion_index.get(aid)
                    check(bool(assertion) and assertion['subject_person_id'] in subject_ids
                          and aid != decision['preferred_assertion_id'], '預設世系排除主張端點不符')
                check(bool(decision['evidence']), '編輯世系缺少來源證據')
                for evidence in decision['evidence']:
                    hit = paragraphs.get(evidence['paragraph_id'])
                    check(bool(hit) and hit[0] == evidence['chapter_id']
                          and evidence['quote'] in hit[1]['text']
                          and chapters[hit[0]]['source_id'] == evidence['source_id'], '編輯世系引句或來源不符')
        assembly_path = root / 'registry/family-assemblies.json'
        assembled_ids = {m['person_id'] for a in json.loads(assembly_path.read_text())['assemblies'] for m in a['members']} if assembly_path.exists() else set()
        for person in people:
            path = person.get('family_path')
            if path is None:
                check(not (FAMILY.fullmatch(person['id']) and len(person['id']) > 11) or person['id'] in assembled_ids, '家族後代 ID 缺少有來源的親屬路徑')
                continue
            parent = path.get('ancestor_person_id', path.get('parent_person_id'))
            check(parent in pids and person['id'] != parent, '家族路徑所據親屬不存在或自環')
            errors.extend(family_path_errors(person['id'], path))
            check(path.get('status') == 'contextual_provisional'
                  and path.get('human_reviewed') is False, '家族路徑關係或審閱狀態無效')
            if 'family_tree_decision_id' in path:
                check(path['family_tree_decision_id'] in tree_decision_ids, '家族路徑所據編輯決定不存在')
            check(bool(path.get('evidence')) and bool(path.get('interpretation_note')), '家族路徑缺少證據或判讀')
            derived_path = 'parent_connection' in path
            if derived_path:
                try:
                    from scripts.family_assemblies import registry_sibling_path_valid
                except ModuleNotFoundError:
                    from family_assemblies import registry_sibling_path_valid
                check(registry_sibling_path_valid(person['id'], path, assertion_index),
                      '暫定父系的兄弟鏈、明父或逐段引證不符')
            for evidence in path.get('evidence', []):
                if evidence.get('kind') == 'table_cell':
                    try:
                        from scripts.table_evidence import table_family_path_errors
                    except ImportError:
                        from table_evidence import table_family_path_errors
                    errors.extend(table_family_path_errors(person['id'], path, tables, family_relations))
                    continue
                hit = paragraphs.get(evidence.get('paragraph_id'))
                check(bool(hit) and hit[0] == evidence.get('chapter_id')
                      and evidence.get('quote') == hit[1]['text']
                      and evidence.get('source_term', '') in hit[1]['text']
                      and chapters[hit[0]]['source_id'] == evidence.get('source_id'), '家族路徑來源與原文不符')
                check(derived_path or any(a.get('qualifiers', {}).get('adopted_for_family_tree') is not False
                          and a.get('qualifiers', {}).get('lineage') != 'maternal'
                          and a['predicate'] == path.get('connection') and a['subject_person_id'] == person['id']
                          and a['object_person_id'] == parent
                          and (a['predicate'] != 'ancestor' or a.get('qualifiers', {}).get('generation_distance') == path.get('generation_distance'))
                          and any(e.get('kind') != 'table_cell' and e.get('paragraph_id') == evidence.get('paragraph_id') for e in a['evidence'])
                          for a in family_relations), '家族路徑缺少相符的來源親屬陳述')
        mention_ids_by_person = {}
        for mid, hit in mentions.items():
            mention_ids_by_person.setdefault(hit[2]['person_id'], set()).add(mid)
        registry_mentions = dict(mentions)
        table_mids_by_person = {}
        for table in tables.values():
            for fragment in table['fragments']:
                for row in fragment['rows']:
                    for cell in row['cells']:
                        for mention in cell.get('person_mentions', []):
                            mid = mention['id']
                            check(mid not in registry_mentions, '人物登記提及ID跨來源重複')
                            registry_mentions[mid] = (table['source']['chapter_id'], None, mention)
                            table_mids_by_person.setdefault(mention['person_id'], set()).add(mid)
        for p in people:
            scope = p.get('evidence_scope', 'corpus_mentions')
            check(scope in ('corpus_mentions', 'corpus_and_native_table_mentions'), '人物登記證據範圍未知')
            check(bool(p['evidence']), f'{p["id"]}: 人物沒有原文證據')
            evidenced=set()
            for e in p['evidence']:
                if e.get('kind') == 'person_reference':
                    try:
                        from scripts.jin075_reference_evidence import reference_evidence_valid
                    except ImportError:
                        from jin075_reference_evidence import reference_evidence_valid
                    check(reference_evidence_valid(e, chapters.get(e['chapter_id']), p['id']), '登記非姓名指涉同段、字位及人物須相合')
                    continue
                if e.get('kind') == 'table_cell':
                    try:
                        from scripts.table_evidence import table_person_evidence_errors
                    except ImportError:
                        from table_evidence import table_person_evidence_errors
                    check(scope == 'corpus_and_native_table_mentions', '表格人物登記須明示原表證據範圍')
                    errors.extend(table_person_evidence_errors(e, tables, p['id']))
                else:
                    hit=mentions.get(e['mention_id'])
                    check(bool(hit) and hit[0]==e['chapter_id'] and hit[1]==e['paragraph_id'] and hit[2]['person_id']==p['id'] and hit[2]['surface']==e['quote'], '人物證據與提及不符')
                evidenced.add(e['mention_id'])
            for alias in p['aliases']:
                check(bool(alias['mention_ids']), '異稱沒有證據')
                for mid in alias['mention_ids']:
                    hit=registry_mentions.get(mid)
                    check(mid in evidenced and bool(hit) and hit[2]['surface']==alias['surface'], '異稱證據不符')
            expected=set(mention_ids_by_person.get(p['id'], set()))
            if scope == 'corpus_and_native_table_mentions':
                expected.update(table_mids_by_person.get(p['id'], set()))
            check(expected==evidenced, '人物提及與證據雙向索引不完整')
        dids=set()
        identity_decisions_by_id = {}
        for path in (root/'corpus').glob('*/*-identities.json'):
            d=json.loads(path.read_text(encoding='utf-8'))
            for decision in d['decisions']:
                identity_decisions_by_id[decision['id']] = decision
                check(decision['id'] not in dids,'身份判斷 ID 重複');dids.add(decision['id'])
                check(decision['person_id'] in pids,'身份判斷引用未知人物')
                check(bool(decision['evidence']),'身份判斷無證據')
                if 'alternatives' in decision:
                    try:
                        from scripts.identity_alternatives import identity_alternative_errors
                    except ImportError:
                        from identity_alternatives import identity_alternative_errors
                    errors.extend(identity_alternative_errors(decision, pids))
                if 'ancestor_reference' in decision:
                    try:
                        from scripts.ancestor_reference import ancestor_reference_valid
                    except ImportError:
                        from ancestor_reference import ancestor_reference_valid
                    reference_assertions = {
                        a['id']: a for source_path in (root / 'corpus').glob('*/*-assertions.json')
                        for a in json.loads(source_path.read_text(encoding='utf-8'))['assertions']}
                    reference_families = json.loads((root / 'registry/family-assemblies.json').read_text(encoding='utf-8'))['assemblies']
                    check(ancestor_reference_valid(decision, chapters, reference_assertions, reference_families),
                          '引語曾祖須有正確發言人及三代來源父系路徑，不得由ID字母或錯誤主語推定')
                scope=decision.get('scope','same_chapter')
                allowed=decision.get('chapter_ids',[d['chapter_id']])
                check(scope in ('same_chapter','cross_chapter'),'身份判斷範圍未知')
                check(len(allowed)==len(set(allowed)) and set(allowed).issubset(chapters),'身份判斷引用未知或重複篇 ID')
                check(d['chapter_id'] in allowed,'身份判斷未包含所屬篇')
                check(len(allowed)==1 if scope=='same_chapter' else len(allowed)>=2,'身份判斷範圍與篇數不符')
                observed=set()
                for e in decision['evidence']:
                    hit=paragraphs.get(e['paragraph_id'])
                    check(bool(hit) and hit[0] in allowed and e['quote'] in hit[1]['text'],'身份判斷引句不在所屬正文')
                    if hit:
                        observed.add(hit[0])
                        try: from scripts.song042_issued_roles import verified_roles
                        except ImportError: from song042_issued_roles import verified_roles
                        if 'person_reference_id' in e:
                            observed_roles=[r for r in chapters[hit[0]]['annotation'].get('person_reference_occurrences',[]) if r['id']==e['person_reference_id'] and r['paragraph_id']==e['paragraph_id'] and r['surface']==e.get('reference_surface') and r['person_id']==decision['person_id']]
                            check(len(observed_roles)==1 and any(hit[1]['text'].startswith(e['quote'], i) and i <= observed_roles[0]['start'] and observed_roles[0]['end'] <= i+len(e['quote']) for i in range(len(hit[1]['text']))),'身份判斷稱謂須在同段引文內對應該人的原字位')
                        else:
                            check(any(m['person_id']==decision['person_id'] for m in hit[1]['mentions']+verified_roles(chapters[hit[0]],hit[1])),'身份判斷段落未提及該人物')
                check(set(allowed).issubset(observed),'跨篇身份判斷未列各篇證據')
                if 'chronology_caution' in decision:
                    try:
                        from scripts.title_chronology_cautions import chronology_caution_errors
                    except ImportError:
                        from title_chronology_cautions import chronology_caution_errors
                    errors.extend(chronology_caution_errors(decision, tables, chapters, paragraphs))
                reading = decision.get('preferred_reading')
                if reading is not None:
                    anchor = mentions.get(reading.get('person_mention_id')) if isinstance(reading, dict) else None
                    variants = [v for cid in allowed for v in chapters[cid]['annotation'].get('reported_variants', [])]
                    variant = next((v for v in variants if isinstance(reading, dict) and v['id'] == reading.get('variant_id')), None)
                    check(isinstance(reading, dict) and set(reading) == {'person_mention_id', 'received_surface', 'preferred_surface', 'source_spelling_is_not_alias', 'variant_id', 'status', 'rationale'}
                          and bool(anchor) and bool(variant)
                          and anchor[1] == variant['paragraph_id']
                          and anchor[2]['person_id'] == decision['person_id']
                          and anchor[2]['surface'] == reading['received_surface'] == variant['received_reading']
                          and reading['preferred_surface'] == variant['reported_reading']
                          and decision['person_id'] in variant['person_ids']
                          and reading['source_spelling_is_not_alias'] is True
                          and reading['status'] == 'editorial_provisional' and bool(reading['rationale'])
                          and decision.get('human_reviewed') is False, '人物首選校讀須有同段異文、人物錨點及明示別名限制')
                if 'parallel_context_reading' in decision:
                    try:
                        from scripts.parallel_context_identity import valid as parallel_context_identity_valid
                    except ImportError:
                        from parallel_context_identity import valid as parallel_context_identity_valid
                    check(parallel_context_identity_valid(decision, chapters, {p['id']: p for p in people}, root), '平行敘事身份須有兩候選、完整固定原證、同事件字面及非別名界限')
                target=next((p for p in people if p['id']==decision['person_id']),None)
                if decision.get('surface_usage') == 'source_scoped_reference':
                    try: from scripts.scoped_reference_decisions import scoped_reference_decision_valid
                    except ImportError: from scoped_reference_decisions import scoped_reference_decision_valid
                    check(scoped_reference_decision_valid(decision, chapters), '稱謂決議須有原已發錨點、角色、對象及原句')
                elif target: check(set(decision['surfaces']).issubset({a['surface'] for a in target['aliases']}),'身份判斷包含未見異稱')
        for path in (root/'corpus').glob('*/*-distinctions.json'):
            d=json.loads(path.read_text(encoding='utf-8'))
            check(d['record_type']=='person_distinction_set','人物區分集類型不符')
            check(d['chapter_id'] in chapters,'人物區分集篇不存在')
            for distinction in d['distinctions']:
                check(distinction['id'] not in dids,'身份判斷 ID 重複');dids.add(distinction['id'])
                ids=distinction['person_ids']
                check(len(ids)>=2 and len(set(ids))==len(ids) and set(ids).issubset(pids),'人物區分端點無效或重複')
                check(distinction['status'] in ('contextual_provisional','source_explicit'),'人物區分狀態無效')
                check(bool(distinction['evidence']) and bool(distinction['rationale']),'人物區分無證據或理由')
                supported=set();own=False
                for e in distinction['evidence']:
                    hit=paragraphs.get(e['paragraph_id'])
                    check(bool(hit) and e['quote'] in hit[1]['text'],'人物區分引句不在正文')
                    if hit:
                        own=own or hit[0]==d['chapter_id']
                        supported.update(m['person_id'] for m in hit[1]['mentions'] if m['person_id'] in ids)
                check(own,'人物區分未包含所屬篇證據')
                check(set(ids).issubset(supported),'人物區分未有各端點證據')
        canonical_links={}
        for path in (root/'corpus').glob('*/*-equivalences.json'):
            d=json.loads(path.read_text(encoding='utf-8'))
            check(d['record_type']=='person_equivalence_set','同指決定集類型不符')
            check(d['chapter_id'] in chapters,'同指決定篇不存在')
            for decision in d['decisions']:
                check(decision['id'] not in dids,'身份判斷 ID 重複');dids.add(decision['id'])
                ids=decision['person_ids'];canonical=decision['canonical_person_id']
                check((len(ids)>=2 and not decision.get('identity_materialized')) or (len(ids)==1 and decision.get('identity_materialized') is True), '同指決定端點無效或重複')
                check(len(set(ids))==len(ids) and set(ids).issubset(pids),'同指決定端點無效或重複')
                check(canonical in ids,'同指決定代表不在端點中')
                check(decision['status'] in ('source_explicit','contextual_provisional'),'同指決定狀態無效')
                check(bool(decision['evidence']) and bool(decision['rationale']),'同指決定缺少證據或理由')
                scope=decision.get('scope','same_chapter')
                scope_chapters=decision.get('chapter_ids',[d['chapter_id']])
                check(scope in ('same_chapter','cross_chapter'),'同指決定範圍無效')
                check(isinstance(scope_chapters,list) and len(set(scope_chapters))==len(scope_chapters) and d['chapter_id'] in scope_chapters and set(scope_chapters).issubset(chapters),'同指決定範圍篇無效或重複')
                check((scope=='same_chapter' and scope_chapters==[d['chapter_id']]) or (scope=='cross_chapter' and len(scope_chapters)>=2),'同指決定範圍與篇數不符')
                supported=set();evidence_chapters=set()
                for e in decision['evidence']:
                    hit=paragraphs.get(e['paragraph_id']);quote=e['quote']
                    check(bool(hit) and hit[0]==e['chapter_id'] and e['chapter_id'] in scope_chapters and bool(quote) and quote in hit[1]['text'],'同指決定引句與所屬篇不符')
                    check(chapters.get(e['chapter_id'],{}).get('source_id')==e['source_id'],'同指決定來源 ID 不符')
                    evidence_chapters.add(e['chapter_id'])
                    mids=e['mention_ids'];check(bool(mids) and len(mids)==len(set(mids)),'同指決定提及錨點缺失或重複')
                    selected=[]
                    for mid in mids:
                        mention=mentions.get(mid)
                        check(bool(mention) and mention[1]==e['paragraph_id'] and mention[2]['person_id'] in ids,'同指決定提及不屬於證據段落或端點')
                        if mention:selected.append(mention[2])
                    if hit and quote:
                        starts=[i for i in range(len(hit[1]['text'])) if hit[1]['text'].startswith(quote,i)]
                        enclosed=any(all(i<=m['start'] and m['end']<=i+len(quote) for m in selected) for i in starts)
                        check(enclosed,'同指決定提及不在精確引句範圍')
                    supported.update(m['person_id'] for m in selected)
                check(set(scope_chapters).issubset(evidence_chapters),'同指決定缺少各篇證據')
                check(set(ids).issubset(supported),'同指決定未有各端點提及證據')
                if decision.get('identity_materialized'):
                    check(len({mid for e in decision['evidence'] for mid in e['mention_ids']}) >= 2, '已整併身份仍須有不同來源提及錨點證據')
                for pid in ids:
                    if pid==canonical:continue
                    check(pid not in canonical_links or canonical_links[pid]==canonical,'同指決定代表衝突')
                    canonical_links[pid]=canonical
        applied_decisions = {d['id']: d for path in (root/'corpus').glob('*/*-equivalences.json') for d in json.loads(path.read_text())['decisions']}
        for chapter in chapters.values():
            seen_cases = {c['id'] for c in chapter.get('annotation', {}).get('unresolved_identity_cases', [])}
            for case in chapter.get('annotation', {}).get('resolved_identity_cases', []):
                pid = case.get('person_id')
                check(case.get('id') and case['id'] not in seen_cases and pid in pids and case.get('status') == 'contextual_provisional' and bool(case.get('note')), '已接合身份案件缺少人物、狀態或說明')
                seen_cases.add(case.get('id'))
                references = [applied_decisions.get(i) for i in case.get('identity_equivalence_decision_ids', [])]
                check(bool(references) and all(d and d.get('identity_materialized') is True and d['person_ids'] == [pid] for d in references), '已接合身份案件缺少已套用的同指證據')
                refs = case.get('paragraph_ids', [])
                check(bool(refs) and all(ref in paragraphs for ref in refs) and any(m['person_id'] == pid for ref in refs if ref in paragraphs for m in paragraphs[ref][1]['mentions']), '已接合身份案件缺少原段落人物提及')
        for start in canonical_links:
            seen=set();current=start
            while current in canonical_links:
                if current in seen:
                    check(False,'同指決定代表循環');break
                seen.add(current);current=canonical_links[current]
        def validate_date_evidence(date, context_evidence, expression=None, bound_record=None, bound_role=None):
            errors.extend(normalized_date_errors(date, chapters, root=root, bound_record=bound_record, bound_role=bound_role))
            if isinstance(date, dict):
                check(binding_valid(date, bound_record, bound_role), '初中末年號紀年須綁實際同人同官授任／生卒記錄')
            if not isinstance(date, dict):
                return
            if 'rendered_collective_award_year_binding' in date:
                return # the exact external-source guard above validates both the date and its holding
            context_ids = {e['paragraph_id'] for e in context_evidence}
            anchored = False
            for evidence in date.get('evidence', []):
                hit = paragraphs.get(evidence['paragraph_id'])
                valid = bool(hit) and hit[0] == evidence['chapter_id']
                check(valid and evidence['quote'] in hit[1]['text'], '紀年換算證據篇段不符')
                if valid:
                    check(chapters[hit[0]]['source_id'] == evidence['source_id'], '紀年換算來源 ID 不符')
                    original = date.get('original_quote')
                    anchored |= (evidence['paragraph_id'] in context_ids
                                 and isinstance(original, str) and original in evidence['quote'])
            if 'cross_chapter_event_binding' in date:
                try:
                    from scripts.cross_chapter_annal_date import cross_chapter_annal_date_valid
                except ImportError:
                    from cross_chapter_annal_date import cross_chapter_annal_date_valid
                cross_event_date = cross_chapter_annal_date_valid(date, bound_record, bound_role, chapters)
                check(cross_event_date, '跨篇同事件紀年須有固定同版雙主語及精確原事件／全年日期錨點')
                anchored = anchored or cross_event_date
            check(anchored, '紀年換算原句未見於本筆事件證據')
            if expression is not None:
                check(isinstance(date.get('original_quote'), str)
                      and expression in date['original_quote'], '紀年換算原句未含本筆日期表述')

        gift_life_events = {e['id']: e for path in (root/'corpus').glob('*/*-life-events.json')
                            for e in json.loads(path.read_text(encoding='utf-8')).get('events', [])}
        title_ids=set();title_occurrence_ids=set()
        title_records = {h['id']: h for path in (root/'corpus').glob('*/*-titles.json')
                         for h in json.loads(path.read_text(encoding='utf-8'))['holdings']}
        for path in (root/'corpus').glob('*/*-titles.json'):
            d=json.loads(path.read_text(encoding='utf-8'))
            check(d['record_type']=='title_holding_assertion_set','稱號持有集類型不符')
            check(d['chapter_id'] in chapters,'稱號持有篇不存在')
            if d['chapter_id'] in chapters:
                try: from scripts.liang033_wangyun_witness import side_errors as liang33_side_errors
                except ImportError: from liang033_wangyun_witness import side_errors as liang33_side_errors
                errors.extend(liang33_side_errors(d, chapters[d['chapter_id']], root, 'holdings'))
            if d['chapter_id'] in chapters:
                try: from scripts.liang021_wangtai_readings import side_errors as tai21_side_errors
                except ImportError: from liang021_wangtai_readings import side_errors as tai21_side_errors
                errors.extend(tai21_side_errors(d,chapters[d['chapter_id']],root,'holdings'))
            if d['chapter_id'] in chapters:
                try: from scripts.liang021_wangjun import side_errors as j21_side_errors
                except ImportError: from liang021_wangjun import side_errors as j21_side_errors
                errors.extend(j21_side_errors(d,chapters[d['chapter_id']],root,'holdings'))
            if d['chapter_id'] in chapters:
                try: from scripts.liang021_wangfen_family import side_errors as wf21_side_errors
                except ImportError: from liang021_wangfen_family import side_errors as wf21_side_errors
                errors.extend(wf21_side_errors(d,chapters[d['chapter_id']],root,'holdings'))
            if d['chapter_id'] in chapters:
                try: from scripts.liang021_wangxun import side_errors as xun21_side_errors
                except ImportError: from liang021_wangxun import side_errors as xun21_side_errors
                errors.extend(xun21_side_errors(d,chapters[d['chapter_id']],root,'holdings'))
            if d['chapter_id'] in chapters:
                try: from scripts.liang021_wangjiansihui import side_errors as sih21_side_errors
                except ImportError: from liang021_wangjiansihui import side_errors as sih21_side_errors
                errors.extend(sih21_side_errors(d,chapters[d['chapter_id']],root,'holdings'))
            if d['chapter_id'] in chapters:
                try: from scripts.song052_xiechun import side_errors as chun52_side_errors
                except ImportError: from song052_xiechun import side_errors as chun52_side_errors
                errors.extend(chun52_side_errors(d,chapters[d['chapter_id']],root,'holdings'))
            if d['chapter_id'] in chapters:
                try: from scripts.song052_xiejingren import side_errors as xiejingren52_side_errors
                except ImportError: from song052_xiejingren import side_errors as xiejingren52_side_errors
                errors.extend(xiejingren52_side_errors(d,chapters[d['chapter_id']],root,'holdings'))
            if d['chapter_id'] in chapters:
                try: from scripts.nan023_digital import side_errors as nan23dan_side_errors
                except ImportError: from nan023_digital import side_errors as nan23dan_side_errors
                errors.extend(nan23dan_side_errors(d,chapters[d['chapter_id']],root,'holdings'))
            if d['chapter_id'] in chapters:
                try: from scripts.song052_wangdan import side_errors as wangdan52_side_errors
                except ImportError: from song052_wangdan import side_errors as wangdan52_side_errors
                errors.extend(wangdan52_side_errors(d,chapters[d['chapter_id']],root,'holdings'))
            if d['chapter_id'] in chapters:
                try: from scripts.song052_xieshu import side_errors as xieshu52_side_errors
                except ImportError: from song052_xieshu import side_errors as xieshu52_side_errors
                errors.extend(xieshu52_side_errors(d,chapters[d['chapter_id']],root,'holdings'))
            if d['chapter_id'] in chapters:
                try: from scripts.nan023_print import side_errors as nan23p_side_errors
                except ImportError: from nan023_print import side_errors as nan23p_side_errors
                errors.extend(nan23p_side_errors(d,chapters[d['chapter_id']],root,'holdings'))
            if d['chapter_id'] in chapters:
                try: from scripts.nan023_wangmao import side_errors as nan23mao_side_errors
                except ImportError: from nan023_wangmao import side_errors as nan23mao_side_errors
                errors.extend(nan23mao_side_errors(d,chapters[d['chapter_id']],root,'holdings'))
            if d['chapter_id'] in chapters:
                try: from scripts.nan023_jiangxiao import side_errors as nan23jiang_side_errors
                except ImportError: from nan023_jiangxiao import side_errors as nan23jiang_side_errors
                errors.extend(nan23jiang_side_errors(d,chapters[d['chapter_id']],root,'holdings'))
            if d['chapter_id'] in chapters:
                try: from scripts.nan023_chuai import side_errors as nan23chuai_side_errors
                except ImportError: from nan023_chuai import side_errors as nan23chuai_side_errors
                errors.extend(nan23chuai_side_errors(d,chapters[d['chapter_id']],root,'holdings'))
            if d['chapter_id'] in chapters:
                try: from scripts.nan023_heyu import side_errors as nan23heyu_side_errors
                except ImportError: from nan023_heyu import side_errors as nan23heyu_side_errors
                errors.extend(nan23heyu_side_errors(d,chapters[d['chapter_id']],root,'holdings'))
            if d['chapter_id'] in chapters:
                try: from scripts.nan023_wangzao import side_errors as nan23zao_side_errors
                except ImportError: from nan023_wangzao import side_errors as nan23zao_side_errors
                errors.extend(nan23zao_side_errors(d,chapters[d['chapter_id']],root,'holdings'))
            if d['chapter_id'] in chapters:
                try: from scripts.nan023_wangying import side_errors as nan23ying_side_errors
                except ImportError: from nan023_wangying import side_errors as nan23ying_side_errors
                errors.extend(nan23ying_side_errors(d,chapters[d['chapter_id']],root,'holdings'))
            if 'superseded_holdings' in d:
                try: from scripts.scoped_reference_decisions import superseded_holdings_valid
                except ImportError: from scoped_reference_decisions import superseded_holdings_valid
                check(superseded_holdings_valid(chapters[d['chapter_id']],d),'舊官爵須指向有原句、同主同官的已核受召紀錄')
            if d['chapter_id'] in chapters:
                try: from scripts.nan023_wangliang import side_errors as nan23liang_side_errors
                except ImportError: from nan023_wangliang import side_errors as nan23liang_side_errors
                errors.extend(nan23liang_side_errors(d,chapters[d['chapter_id']],root,'holdings'))
            if d['chapter_id'] in chapters:
                try: from scripts.nan023_wanghui import side_errors as nan23hui_side_errors
                except ImportError: from nan023_wanghui import side_errors as nan23hui_side_errors
                errors.extend(nan23hui_side_errors(d,chapters[d['chapter_id']],root,'holdings'))
            if d['chapter_id'] in chapters:
                try: from scripts.nan023_wangqiu import side_errors as nan23qiu_side_errors
                except ImportError: from nan023_wangqiu import side_errors as nan23qiu_side_errors
                errors.extend(nan23qiu_side_errors(d,chapters[d['chapter_id']],root,'holdings'))
            if d['chapter_id'] in chapters:
                try: from scripts.nan023_wangxuan import side_errors as nan23xuan_side_errors
                except ImportError: from nan023_wangxuan import side_errors as nan23xuan_side_errors
                errors.extend(nan23xuan_side_errors(d,chapters[d['chapter_id']],root,'holdings'))
            if d['chapter_id'] in chapters:
                try: from scripts.nan023_wanghui_sons import side_errors as nan23huiz_side_errors
                except ImportError: from nan023_wanghui_sons import side_errors as nan23huiz_side_errors
                errors.extend(nan23huiz_side_errors(d,chapters[d['chapter_id']],root,'holdings'))
            if d['chapter_id'] in chapters:
                try: from scripts.nan023_chuzhanzhi import side_errors as nan23chu_side_errors
                except ImportError: from nan023_chuzhanzhi import side_errors as nan23chu_side_errors
                errors.extend(nan23chu_side_errors(d,chapters[d['chapter_id']],root,'holdings'))
            if d['chapter_id'] in chapters:
                try: from scripts.nan023_wangyun import side_errors as nan23yun_side_errors
                except ImportError: from nan023_wangyun import side_errors as nan23yun_side_errors
                errors.extend(nan23yun_side_errors(d,chapters[d['chapter_id']],root,'holdings'))
            if d['chapter_id'] in chapters:
                try: from scripts.nan023_wanghuan import side_errors as nan23huan_side_errors
                except ImportError: from nan023_wanghuan import side_errors as nan23huan_side_errors
                errors.extend(nan23huan_side_errors(d,chapters[d['chapter_id']],root,'holdings'))
            if d['chapter_id'] in chapters:
                try: from scripts.nan023_wangxi import side_errors as nan23xi_side_errors
                except ImportError: from nan023_wangxi import side_errors as nan23xi_side_errors
                errors.extend(nan23xi_side_errors(d,chapters[d['chapter_id']],root,'holdings'))
            if d['chapter_id'] in chapters:
                try: from scripts.nan023_wangfen import side_errors as nan23fen_side_errors
                except ImportError: from nan023_wangfen import side_errors as nan23fen_side_errors
                errors.extend(nan23fen_side_errors(d,chapters[d['chapter_id']],root,'holdings'))
            if d['chapter_id'] in chapters:
                try: from scripts.nan023_wangtong import side_errors as nan23tong_side_errors
                except ImportError: from nan023_wangtong import side_errors as nan23tong_side_errors
                errors.extend(nan23tong_side_errors(d,chapters[d['chapter_id']],root,'holdings'))
            if d['chapter_id'] in chapters:
                try: from scripts.nan023_wangmai import side_errors as nan23mai_side_errors
                except ImportError: from nan023_wangmai import side_errors as nan23mai_side_errors
                errors.extend(nan23mai_side_errors(d,chapters[d['chapter_id']],root,'holdings'))
            if d['chapter_id'] in chapters:
                try: from scripts.nan023_wangzhi import side_errors as nan23zhi_side_errors
                except ImportError: from nan023_wangzhi import side_errors as nan23zhi_side_errors
                errors.extend(nan23zhi_side_errors(d,chapters[d['chapter_id']],root,'holdings'))
            if d['chapter_id'] in chapters:
                try: from scripts.nan023_wanggu import side_errors as nan23gu_side_errors
                except ImportError: from nan023_wanggu import side_errors as nan23gu_side_errors
                errors.extend(nan23gu_side_errors(d,chapters[d['chapter_id']],root,'holdings'))
            if d['chapter_id'] in chapters:
                try: from scripts.nan023_wanghou import side_errors as nan23hou_side_errors
                except ImportError: from nan023_wanghou import side_errors as nan23hou_side_errors
                errors.extend(nan23hou_side_errors(d,chapters[d['chapter_id']],root,'holdings'))
            if d['chapter_id'] in chapters:
                try: from scripts.nan023_wangyu import side_errors as nan23yu_side_errors
                except ImportError: from nan023_wangyu import side_errors as nan23yu_side_errors
                errors.extend(nan23yu_side_errors(d,chapters[d['chapter_id']],root,'holdings'))
            if d['chapter_id'] in chapters:
                try: from scripts.nanqi047_wangrong import side_errors as qi47rong_side_errors
                except ImportError: from nanqi047_wangrong import side_errors as qi47rong_side_errors
                errors.extend(qi47rong_side_errors(d,chapters[d['chapter_id']],root,'holdings'))
            if d['chapter_id'] in chapters:
                try: from scripts.liang033_wangsengru import side_errors as liang33sr_side_errors
                except ImportError: from liang033_wangsengru import side_errors as liang33sr_side_errors
                errors.extend(liang33sr_side_errors(d,chapters[d['chapter_id']],root,'holdings'))
            if d['chapter_id'] in chapters:
                try: from scripts.nanshi059_wangsengru import side_errors as nan59sr_side_errors
                except ImportError: from nanshi059_wangsengru import side_errors as nan59sr_side_errors
                errors.extend(nan59sr_side_errors(d,chapters[d['chapter_id']],root,'holdings'))
            if d['chapter_id'] in chapters:
                try: from scripts.nanqi047_wangrong_wyd import side_errors as q47wyd_sides
                except ImportError: from nanqi047_wangrong_wyd import side_errors as q47wyd_sides
                errors.extend(q47wyd_sides(d,chapters[d['chapter_id']],root,'holdings'))
            if d['chapter_id'] in chapters:
                try: from scripts.nanshi024_wangshaozhi import side_errors as nan24sz_side_errors
                except ImportError: from nanshi024_wangshaozhi import side_errors as nan24sz_side_errors
                errors.extend(nan24sz_side_errors(d,chapters[d['chapter_id']],root,'holdings'))
            if d['chapter_id'] in chapters:
                try: from scripts.nanshi024_wangshaozhi_wyd import side_errors as n24szwyd_sides
                except ImportError: from nanshi024_wangshaozhi_wyd import side_errors as n24szwyd_sides
                errors.extend(n24szwyd_sides(d,chapters[d['chapter_id']],root,'holdings'))
            if d['chapter_id'] in chapters:
                try: from scripts.nanshi024_wangyuezhi import side_errors as nan24yz_side_errors
                except ImportError: from nanshi024_wangyuezhi import side_errors as nan24yz_side_errors
                errors.extend(nan24yz_side_errors(d,chapters[d['chapter_id']],root,'holdings'))
            if d['chapter_id'] in chapters:
                try: from scripts.nanshi024_wangzhunzhi import side_errors as nan24zz_side_errors
                except ImportError: from nanshi024_wangzhunzhi import side_errors as nan24zz_side_errors
                errors.extend(nan24zz_side_errors(d,chapters[d['chapter_id']],root,'holdings'))
            if d['chapter_id'] in chapters:
                try: from scripts.nanshi024_wangjinzhi import side_errors as nan24jz_side_errors
                except ImportError: from nanshi024_wangjinzhi import side_errors as nan24jz_side_errors
                errors.extend(nan24jz_side_errors(d,chapters[d['chapter_id']],root,'holdings'))
            if d['chapter_id'] in chapters:
                try: from scripts.nanshi024_wangqing import side_errors as nan24qing_side_errors
                except ImportError: from nanshi024_wangqing import side_errors as nan24qing_side_errors
                errors.extend(nan24qing_side_errors(d,chapters[d['chapter_id']],root,'holdings'))
            if d['chapter_id'] in chapters:
                try: from scripts.nanshi024_wangqunzhi import side_errors as nan24qun_side_errors
                except ImportError: from nanshi024_wangqunzhi import side_errors as nan24qun_side_errors
                errors.extend(nan24qun_side_errors(d,chapters[d['chapter_id']],root,'holdings'))
            if d['chapter_id'] in chapters:
                try: from scripts.nanshi024_wangsu import side_errors as nan24su_side_errors
                except ImportError: from nanshi024_wangsu import side_errors as nan24su_side_errors
                errors.extend(nan24su_side_errors(d,chapters[d['chapter_id']],root,'holdings'))
            if d['chapter_id'] in chapters:
                try: from scripts.nanshi024_ruanwanling import side_errors as nan24rw_side_errors
                except ImportError: from nanshi024_ruanwanling import side_errors as nan24rw_side_errors
                errors.extend(nan24rw_side_errors(d,chapters[d['chapter_id']],root,'holdings'))
            if d['chapter_id'] in chapters:
                try: from scripts.nanshi024_wanghongzhi import side_errors as n24hong_sides
                except ImportError: from nanshi024_wanghongzhi import side_errors as n24hong_sides
                errors.extend(n24hong_sides(d,chapters[d['chapter_id']],root,'holdings'))
            if d['chapter_id'] in chapters:
                try: from scripts.song093_wangtansheng import title_errors as tansheng_titles
                except ImportError: from song093_wangtansheng import title_errors as tansheng_titles
                errors.extend(tansheng_titles(d, chapters[d['chapter_id']], root))
            if d['chapter_id'] in chapters:
                try: from scripts.song093_wanghongzhi import side_errors as hongzhi_sides
                except ImportError: from song093_wanghongzhi import side_errors as hongzhi_sides
                errors.extend(hongzhi_sides(d,chapters[d['chapter_id']],root,'holdings'))
            if d['chapter_id'] in chapters:
                try: from scripts.song093_wyd import side_errors as s93wyd_sides
                except ImportError: from song093_wyd import side_errors as s93wyd_sides
                errors.extend(s93wyd_sides(d,chapters[d['chapter_id']],root,'holdings'))
            if d['chapter_id'] in chapters:
                try: from scripts.nanshi024_wangmeng import side_errors as nan24meng_side_errors
                except ImportError: from nanshi024_wangmeng import side_errors as nan24meng_side_errors
                errors.extend(nan24meng_side_errors(d,chapters[d['chapter_id']],root,'holdings'))
            if d['chapter_id'] in chapters:
                try: from scripts.xiangshan_m9_epitaphs import side_errors as xm9_side_errors
                except ImportError: from xiangshan_m9_epitaphs import side_errors as xm9_side_errors
                errors.extend(xm9_side_errors(d,chapters[d['chapter_id']],root,'holdings'))
            if d['chapter_id'] in chapters:
                try: from scripts.nanshi024_wangyan import side_errors as nan24yan_side_errors
                except ImportError: from nanshi024_wangyan import side_errors as nan24yan_side_errors
                errors.extend(nan24yan_side_errors(d,chapters[d['chapter_id']],root,'holdings'))
            if d['chapter_id'] in chapters:
                try: from scripts.nanshi024_wangyan_brothers import side_errors as nan24wab_side_errors
                except ImportError: from nanshi024_wangyan_brothers import side_errors as nan24wab_side_errors
                errors.extend(nan24wab_side_errors(d,chapters[d['chapter_id']],root,'holdings'))
            if d['chapter_id'] in chapters:
                try: from scripts.nanshi024_guhaozhi import side_errors as nan24gh_side_errors
                except ImportError: from nanshi024_guhaozhi import side_errors as nan24gh_side_errors
                errors.extend(nan24gh_side_errors(d,chapters[d['chapter_id']],root,'holdings'))
            if d['chapter_id'] in chapters:
                try: from scripts.nanshi024_wangsiyuan import side_errors as nan24siy_side_errors
                except ImportError: from nanshi024_wangsiyuan import side_errors as nan24siy_side_errors
                errors.extend(nan24siy_side_errors(d,chapters[d['chapter_id']],root,'holdings'))
            for h in d['holdings']:
                check(h['id'] not in title_ids,'稱號持有 ID 重複');title_ids.add(h['id'])
                check(h['person_id'] in pids and bool(h['title']),'稱號持有人或用稱無效')
                check(h['status']=='source_attested','稱號持有狀態無效')
                check(h['kind'] in ('royal_rank','imperial_rank','noble_rank','office','honorific','unclassified'),'稱號種類無效')
                check(h['mode'] in ('grant','transfer','posthumous_grant','posthumous_enfeoffment','posthumous_naming','self_proclamation','accession','demotion','attestation'),'稱號事件種類無效')
                check(bool(h['evidence']) and bool(h['attestations']),'稱號缺少來源或用稱錨點')
                wyd63_title_reference = False
                if 'nanshi024_wangyan_title_reference' in h:
                    try: from scripts.nanshi024_wangyan import ruler_holding as nan24yan_ruler_holding
                    except ImportError: from nanshi024_wangyan import ruler_holding as nan24yan_ruler_holding
                    wyd63_title_reference=nan24yan_ruler_holding(h,chapters[d['chapter_id']],root)
                    check(wyd63_title_reference,'王晏任主簿時爲長史的齊武帝須有同句官名與帝號')
                if 'printed_title_holder_reference' in h:
                    try: from scripts.wyd_song063_wangtanshou import reference_title_valid
                    except ImportError: from wyd_song063_wangtanshou import reference_title_valid
                    wyd63_title_reference = reference_title_valid(h, chapters[d['chapter_id']], root)
                    check(wyd63_title_reference, '宋卷六十三殿本稱官須核同一持有人稱謂及官號字位')
                if 'received_source_frame' in h:
                    try:from scripts.fixed_received_career import holding_valid as fixed_received_holding_valid
                    except ImportError:from fixed_received_career import holding_valid as fixed_received_holding_valid
                    check(fixed_received_holding_valid(h,chapters[d['chapter_id']],root),'固定收到官序須綁完整見證、原句角色、實際官名與受任者')
                if 'source_family_office_frame' in h:
                    try:
                        from scripts.named_family_offices import valid as family_office_valid
                    except ImportError:
                        from named_family_offices import valid as family_office_valid
                    check(family_office_valid(h, chapters), '具名子列授爵與兄弟任官須逐角色綁原文，不得按列序推排行')
                if 'source_career_role' in h:
                    try:
                        from scripts.received_career_roles import holding_valid as career_holding_valid
                    except ImportError:
                        from received_career_roles import holding_valid as career_holding_valid
                    check(career_holding_valid(h, chapters[d['chapter_id']],root), '來源職歷須逐原句角色綁實際受任者、共享職尾及任期界線')
                if 'source_office_role' in h:
                    try:
                        from scripts.source_office_reports import holding_role_valid
                    except ImportError:
                        from source_office_reports import holding_role_valid
                    check(holding_role_valid(h, chapters[d['chapter_id']], title_records, root), '官爵來源角色與完整任職語法不符，不得以同段人名冒作受任者')
                if 'source_qualification' in h:
                    try:
                        from scripts.source_office_reports import qualified_office_valid
                    except ImportError:
                        from source_office_reports import qualified_office_valid
                    check(qualified_office_valid(h, chapters[d['chapter_id']]), '受古注質疑的來源官稱須綁同人、引書與批評兩端，不得變實任首選')
                def title_evidence(e):
                    hit=paragraphs.get(e['paragraph_id'])
                    check(bool(hit) and hit[0]==d['chapter_id']==e['chapter_id'] and bool(e['quote']) and e['quote'] in hit[1]['text'],'稱號引句與所屬篇不符')
                    check(chapters.get(e['chapter_id'],{}).get('source_id')==e['source_id'],'稱號來源 ID 不符')
                    if hit:
                        if 'context' not in e:
                            check(wyd63_title_reference or any(m['person_id']==h['person_id'] for m in hit[1]['mentions']),'稱號引句段落未提及持有人')
                        else:
                            context=e['context']
                            valid=isinstance(context,dict)
                            if valid:
                                previous=paragraphs.get(context.get('paragraph_id'))
                                mention=mentions.get(context.get('person_mention_id'))
                                order=[p['id'] for p in chapters.get(d['chapter_id'],{}).get('paragraphs',[])]
                                quote=context.get('quote')
                                valid=(context.get('kind')=='previous_paragraph_subject' and bool(previous)
                                       and previous[0]==d['chapter_id'] and context['paragraph_id'] in order
                                       and e['paragraph_id'] in order and order.index(e['paragraph_id'])==order.index(context['paragraph_id'])+1
                                       and bool(mention) and mention[1]==context['paragraph_id'] and mention[2]['person_id']==h['person_id']
                                       and isinstance(quote,str) and bool(quote) and quote in previous[1]['text'])
                                if valid:
                                    anchor=mention[2];text=previous[1]['text']
                                    valid=any(i<=anchor['start'] and anchor['end']<=i+len(quote)
                                              for i in range(len(text)) if text.startswith(quote,i))
                            if isinstance(context,dict) and context.get('kind')=='layered_biography_subject_continuation':
                                try:from scripts.layered_biography_titles import title_context_valid
                                except ImportError:from layered_biography_titles import title_context_valid
                                valid=title_context_valid(h['attestations'][0],h,chapters[d['chapter_id']])
                            if isinstance(context,dict) and context.get('kind')=='wang_xi_biography_end':
                                try: from scripts.liang021_wangfen_family import xi_end_title as wf_end_title
                                except ImportError: from liang021_wangfen_family import xi_end_title as wf_end_title
                                valid=wf_end_title(h['attestations'][0],h,chapters[d['chapter_id']])
                            if isinstance(context,dict) and context.get('kind')=='liang033_sengru_resumed_biography':
                                try: from scripts.liang033_wangsengru import resumed_title as sengru_resumed_title
                                except ImportError: from liang033_wangsengru import resumed_title as sengru_resumed_title
                                valid=sengru_resumed_title(h['attestations'][0],h,chapters[d['chapter_id']])
                            check(valid,'稱號省略主語的前段錨點或引句無效')
                for e in h['evidence']:title_evidence(e)
                if 'source_grant_basis' in h:
                    try:
                        from scripts.song041_title_semantics import conferment_valid
                    except ImportError:
                        from song041_title_semantics import conferment_valid
                    check(conferment_valid(h, paragraphs), '明授名號須有拜／加／封與同人原位，不得以奏請充實授或借近年')
                if 'punctuation_attribution' in h:
                    try:
                        from scripts.office_attributions import punctuation_attribution_errors
                    except ModuleNotFoundError:
                        from office_attributions import punctuation_attribution_errors
                    errors.extend(punctuation_attribution_errors(h, paragraphs, mentions))
                if 'end_basis' in h:
                    check(named_office_end_valid(h, paragraphs, mentions), '明示終職須綁同人此職原詞，不得以一般死亡補所有職爵')
                if 'inheritance' in h:
                    inheritance = h['inheritance']
                    valid = isinstance(inheritance, dict) and set(inheritance) - {'predecessor_relation'} == {
                        'predecessor_person_id', 'predecessor_holding_id', 'resolved_title',
                        'source_term', 'status', 'evidence', 'rationale', 'human_reviewed'}
                    if valid:
                        predecessor = title_records.get(inheritance['predecessor_holding_id'])
                        cursor = predecessor
                        visited = {h['id']}
                        inherited_chain_valid = True
                        while isinstance(cursor, dict) and 'inheritance' in cursor:
                            link = cursor['inheritance']
                            if (cursor['id'] in visited or cursor.get('kind') != h['kind']
                                or cursor.get('mode') != 'accession' or not isinstance(link, dict)
                                or link.get('resolved_title') != inheritance['resolved_title']):
                                inherited_chain_valid = False
                                break
                            visited.add(cursor['id'])
                            cursor = title_records.get(link.get('predecessor_holding_id'))
                        inherited_chain_valid = (inherited_chain_valid and isinstance(cursor, dict)
                            and cursor['id'] not in visited
                            and cursor.get('kind') == h['kind']
                            and cursor.get('title') == inheritance['resolved_title'])
                        valid = (h['kind'] in ('noble_rank', 'royal_rank') and h['mode'] == 'accession'
                            and bool(predecessor) and predecessor['kind'] == h['kind']
                            and predecessor['person_id'] == inheritance['predecessor_person_id']
                            and predecessor['person_id'] != h['person_id']
                            and inherited_chain_valid
                            and inheritance['status'] == 'contextual_provisional'
                            and inheritance['human_reviewed'] is False
                            and bool(inheritance['rationale'])
                            and isinstance(inheritance['source_term'], str)
                            and bool(inheritance['source_term'])
                            and isinstance(inheritance['evidence'], list) and bool(inheritance['evidence'])
                            and all(inheritance['source_term'] in e.get('quote', '')
                                    for e in inheritance['evidence'])
                            and inheritance.get('predecessor_relation', 'father') in ('father', 'brother')
                            and any(a['predicate'] == inheritance.get('predecessor_relation', 'father')
                                    and a['subject_person_id'] == h['person_id']
                                    and a['object_person_id'] == predecessor['person_id']
                                    and any(e['paragraph_id'] == ie.get('paragraph_id')
                                            for e in a['evidence'] for ie in inheritance['evidence'])
                                    for a in family_relations))
                    if isinstance(inheritance, dict) and inheritance.get('predecessor_relation') == 'named_collateral_succession':
                        try:
                            from scripts.collateral_title_succession import valid as collateral_succession_valid
                        except ImportError:
                            from collateral_title_succession import valid as collateral_succession_valid
                        valid = collateral_succession_valid(h, title_records, paragraphs, family_relations)
                    if isinstance(inheritance, dict) and inheritance.get('predecessor_relation') == 'named_source_line_succession':
                        try:
                            from scripts.song041_title_semantics import line_succession_valid
                        except ImportError:
                            from song041_title_semantics import line_succession_valid
                        valid = line_succession_valid(h, title_records, paragraphs, family_relations)
                    check(valid, '承爵判讀缺少相符的前任爵位、父子或原詞證據')
                    if valid:
                        for e in inheritance['evidence']:title_evidence(e)
                if h['mode'] == 'transfer' and h['kind'] == 'office':
                    try:
                        from scripts.office_transfers import office_transfer_valid
                    except ImportError:
                        from office_transfers import office_transfer_valid
                    valid_transfer = office_transfer_valid(h, paragraphs, mentions)
                    if 'source_role_sequence' in h:
                        try:
                            from scripts.biographical_appointment_sequence import holding_valid
                        except ImportError:
                            from biographical_appointment_sequence import holding_valid
                        valid_transfer = holding_valid(h, chapters[d['chapter_id']], root)
                    if 'source_career_role' in h:
                        try:
                            from scripts.received_career_roles import holding_valid as career_holding_valid
                        except ImportError:
                            from received_career_roles import holding_valid as career_holding_valid
                        valid_transfer = career_holding_valid(h, chapters[d['chapter_id']],root)
                    if 'received_source_frame' in h:
                        try:from scripts.fixed_received_career import holding_valid as fixed_received_transfer_valid
                        except ImportError:from fixed_received_career import holding_valid as fixed_received_transfer_valid
                        valid_transfer=fixed_received_transfer_valid(h,chapters[d['chapter_id']],root)
                    check(valid_transfer, '官職轉任須有同人原詞、逐職錨點及相符任用證據，不作王爵徙封')
                if (h['mode']=='transfer' and h['kind'] != 'office') or 'transfer_basis' in h:
                    if h['kind'] == 'noble_rank':
                        try:
                            from scripts.noble_transfers import noble_transfer_errors
                        except ModuleNotFoundError:
                            from noble_transfers import noble_transfer_errors
                        errors.extend(noble_transfer_errors(h, title_records, paragraphs, mentions, chapters))
                    else:
                        try:
                            from scripts.royal_transfers import royal_transfer_errors
                        except ModuleNotFoundError:
                            from royal_transfers import royal_transfer_errors
                        errors.extend(royal_transfer_errors(h, title_records, paragraphs, mentions))
                if 'chronology_source_choice' in h:
                    try:
                        from scripts.royal_transfers import chronology_choice_errors
                    except ModuleNotFoundError:
                        from royal_transfers import chronology_choice_errors
                    errors.extend(chronology_choice_errors(h, paragraphs, chapters))
                if 'chronology_preference' in h:
                    try:
                        from scripts.title_chronology_preference import title_chronology_preference_valid
                    except ImportError:
                        from title_chronology_preference import title_chronology_preference_valid
                    check(title_chronology_preference_valid(h, title_records),
                          '稱號紀年首選須保留同人同次事件的各來源與不同數字紀年，不得改抹異說')
                if h['mode']=='posthumous_enfeoffment' or 'enfeoffment_basis' in h:
                    try:
                        from scripts.posthumous_enfeoffments import valid as enfeoffment_valid
                    except ImportError:
                        from posthumous_enfeoffments import valid as enfeoffment_valid
                    if h.get('enfeoffment_basis', {}).get('kind') == 'issued_wyd_song063_award':
                        try: from scripts.wyd_song063_wangtanshou import award_valid as wyd63_award_valid
                        except ImportError: from wyd_song063_wangtanshou import award_valid as wyd63_award_valid
                        valid = wyd63_award_valid(h, chapters[d['chapter_id']], gift_life_events, root)
                    else:
                        valid = enfeoffment_valid(h, paragraphs, mentions, gift_life_events)
                    if h.get('enfeoffment_basis',{}).get('kind') == 'nanshi024_wangmeng_funeral_award':
                        try: from scripts.nanshi024_wangmeng import funeral_award as wangmeng_funeral_award
                        except ImportError: from nanshi024_wangmeng import funeral_award as wangmeng_funeral_award
                        valid=wangmeng_funeral_award(h,chapters[d['chapter_id']],gift_life_events,root)
                    if h.get('enfeoffment_basis',{}).get('kind') == 'nanshi024_wangsiyuan_funeral_award':
                        try: from scripts.nanshi024_wangsiyuan import funeral_award as wangsiyuan_funeral_award
                        except ImportError: from nanshi024_wangsiyuan import funeral_award as wangsiyuan_funeral_award
                        valid=wangsiyuan_funeral_award(h,chapters[d['chapter_id']],gift_life_events,root)
                    check(valid, '追封須有同人已記死亡、明文追封爵號及相符字位')
                if h['mode']=='posthumous_grant' or 'posthumous_basis' in h:
                    basis=h.get('posthumous_basis')
                    explicit_retrospective=(isinstance(basis,dict)
                        and set(basis)=={'source_term','evidence'}
                        and isinstance(basis.get('source_term'),str)
                        and ('追尊' in basis['source_term'] or '追贈' + h['title'] in basis['source_term']))
                    death_then_grant=(isinstance(basis,dict)
                        and set(basis)=={'source_term','death_term','grant_term','evidence'}
                        and all(isinstance(basis.get(k),str) and basis[k] for k in ('source_term','death_term','grant_term'))
                        and bool(re.search(r'[死卒薨崩]',basis['death_term']))
                        and basis['grant_term'] in ('賜夫人為'+h['title'], '號為'+h['title'])
                        and basis['death_term'] in basis['source_term']
                        and basis['grant_term'] in basis['source_term']
                        and basis['source_term'].index(basis['death_term'])+len(basis['death_term'])<=basis['source_term'].index(basis['grant_term']))
                    try:
                        from scripts.posthumous_gifts import posthumous_gift_valid
                    except ImportError:
                        from posthumous_gifts import posthumous_gift_valid
                    explicit_gift = posthumous_gift_valid(h, paragraphs, mentions, gift_life_events)
                    if isinstance(basis,dict) and basis.get('kind') == 'explicit_topic_scoped_gift_with_sovereign_reference':
                        try: from scripts.song042_sovereign_gift_reference import valid as referenced_gift_valid
                        except ImportError: from song042_sovereign_gift_reference import valid as referenced_gift_valid
                        explicit_gift = referenced_gift_valid(h, chapters.get(d['chapter_id']), paragraphs, mentions, gift_life_events)
                    try:
                        from scripts.retrospective_parent_honorific import parent_honorific_grant_valid
                    except ImportError:
                        from retrospective_parent_honorific import parent_honorific_grant_valid
                    parent_honorific = parent_honorific_grant_valid(h, paragraphs)
                    valid=(h['mode']=='posthumous_grant' and (explicit_retrospective or death_then_grant or explicit_gift or parent_honorific)
                           and isinstance(basis['evidence'],list) and bool(basis['evidence'])
                           and basis['evidence']==h['effective_period']['start']['evidence']
                           and all(isinstance(e,dict) and isinstance(e.get('quote'),str)
                                   and basis['source_term'] in e['quote'] for e in basis['evidence']))
                    if isinstance(basis, dict) and basis.get('kind') == 'issued_wyd_song063_award':
                        try: from scripts.wyd_song063_wangtanshou import award_valid as wyd63_award_valid
                        except ImportError: from wyd_song063_wangtanshou import award_valid as wyd63_award_valid
                        valid = wyd63_award_valid(h, chapters[d['chapter_id']], gift_life_events, root)
                    elif isinstance(basis,dict) and basis.get('kind')=='nan22jian_funeral_award':
                        try: from scripts.nanshi022_wangjian_source import award_valid as n22jian_award_valid
                        except ImportError: from nanshi022_wangjian_source import award_valid as n22jian_award_valid
                        valid=n22jian_award_valid(h,chapters[d['chapter_id']],gift_life_events,root)
                    elif isinstance(basis, dict) and basis.get('kind') == 'qi23_wang_death_award':
                        try: from scripts.qi023_wangjian_witnesses import award_valid as qi23_award_valid
                        except ImportError: from qi023_wangjian_witnesses import award_valid as qi23_award_valid
                        valid = qi23_award_valid(h,chapters[d['chapter_id']],gift_life_events,root)
                    elif isinstance(basis, dict) and basis.get('kind') == 'song071_ws_wang_posthumous_awards':
                        try: from scripts.ws_song071_wang import award_valid as ws71_award_valid
                        except ImportError: from ws_song071_wang import award_valid as ws71_award_valid
                        valid = ws71_award_valid(h, chapters[d['chapter_id']], gift_life_events, root)
                    if isinstance(basis, dict) and basis.get('kind') == 'song071_print_wang_posthumous_awards':
                        try: from scripts.wyd_song071_wang import award_valid as wyd71_award_valid
                        except ImportError: from wyd_song071_wang import award_valid as wyd71_award_valid
                        valid = wyd71_award_valid(h, chapters[d['chapter_id']], gift_life_events, root)
                    if isinstance(basis, dict) and basis.get('kind') == 'song071_wang_posthumous_awards':
                        try: from scripts.song071_wang_awards import valid as song071_award_valid
                        except ImportError: from song071_wang_awards import valid as song071_award_valid
                        valid = song071_award_valid(h, paragraphs, mentions, gift_life_events)
                    if 'source_career_role' in h:
                        try:
                            from scripts.received_career_roles import holding_valid as career_holding_valid
                        except ImportError:
                            from received_career_roles import holding_valid as career_holding_valid
                        valid = valid or career_holding_valid(h, chapters[d['chapter_id']],root)
                    if isinstance(basis,dict) and basis.get('kind')=='wang_xi_death_then_gift':
                        try:from scripts.liang021_wangfen_family import xi_end_title
                        except ImportError:from liang021_wangfen_family import xi_end_title
                        valid=(xi_end_title(h['attestations'][0],h,chapters[d['chapter_id']])
                               and basis['death_term']=='卒' and basis['grant_term']=='贈'+h['title']
                               and basis['source_term'] in h['evidence'][0]['quote']
                               and basis['evidence']==h['evidence']==h['effective_period']['start']['evidence'])
                    if isinstance(basis,dict) and basis.get('kind')=='wangjian_death_then_three_gifts':
                        try: from scripts.liang021_wangjiansihui import gift_valid as sih21_gift
                        except ImportError: from liang021_wangjiansihui import gift_valid as sih21_gift
                        valid=sih21_gift(h,chapters[d['chapter_id']],gift_life_events,root)
                    if isinstance(basis,dict) and basis.get('kind')=='song52_jingren_death_grant':
                        try: from scripts.song052_xiejingren import gift_valid as sj52_gift
                        except ImportError: from song052_xiejingren import gift_valid as sj52_gift
                        valid=sj52_gift(h,chapters[d['chapter_id']],gift_life_events,root)
                    if isinstance(basis,dict) and basis.get('kind')=='nan23_yan_gift_and_name':
                        try: from scripts.nan023_digital import yan_award as nan23_yan_award
                        except ImportError: from nan023_digital import yan_award as nan23_yan_award
                        valid=nan23_yan_award(h,chapters[d['chapter_id']],root)
                    if isinstance(basis,dict) and basis.get('kind')=='nan23p_yan_gift_and_name':
                        try: from scripts.nan023_print import yan_award as nan23p_yan_award
                        except ImportError: from nan023_print import yan_award as nan23p_yan_award
                        valid=nan23p_yan_award(h,chapters[d['chapter_id']],root)
                    if isinstance(basis,dict) and basis.get('kind')=='nan23_liang_you_posthumous_grant':
                        try: from scripts.nan023_wangliang import you_award as nan23_you_award
                        except ImportError: from nan023_wangliang import you_award as nan23_you_award
                        valid=nan23_you_award(h,chapters[d['chapter_id']],root)
                    if isinstance(basis,dict) and basis.get('kind')=='nan23_qiu_final_gift':
                        try: from scripts.nan023_wangqiu import qiu_gift as nan23qiu_gift
                        except ImportError: from nan023_wangqiu import qiu_gift as nan23qiu_gift
                        valid=nan23qiu_gift(h,chapters[d['chapter_id']],root)
                    if isinstance(basis,dict) and basis.get('kind')=='nan23_named_biography_death_gift':
                        try: from scripts.nan023_wangxi import biography_death_gift
                        except ImportError: from nan023_wangxi import biography_death_gift
                        valid=biography_death_gift(h,chapters[d['chapter_id']],gift_life_events,root)
                    if isinstance(basis,dict) and basis.get('kind')=='nan23_yu_death_and_gift':
                        try: from scripts.nan023_wangyu import gift_valid as nan23yu_gift_valid
                        except ImportError: from nan023_wangyu import gift_valid as nan23yu_gift_valid
                        valid=nan23yu_gift_valid(h,chapters[d['chapter_id']],gift_life_events,root)
                    if h.get('posthumous_basis',{}).get('kind') == 'nanshi024_wangmeng_funeral_award':
                        try: from scripts.nanshi024_wangmeng import funeral_award as wangmeng_funeral_award
                        except ImportError: from nanshi024_wangmeng import funeral_award as wangmeng_funeral_award
                        valid=wangmeng_funeral_award(h,chapters[d['chapter_id']],gift_life_events,root)
                    if h.get('posthumous_basis',{}).get('kind') == 'nanshi024_wangsiyuan_funeral_award':
                        try: from scripts.nanshi024_wangsiyuan import funeral_award as wangsiyuan_funeral_award
                        except ImportError: from nanshi024_wangsiyuan import funeral_award as wangsiyuan_funeral_award
                        valid=wangsiyuan_funeral_award(h,chapters[d['chapter_id']],gift_life_events,root)
                    check(valid,'追尊授號缺少相符原詞與起點證據')
                    if valid:
                        for e in basis['evidence']:title_evidence(e)
                if h['mode']=='posthumous_naming' or 'naming_basis' in h:
                    basis=h.get('naming_basis')
                    if isinstance(basis, dict) and basis.get('kind') == 'issued_wyd_song063_award':
                        try: from scripts.wyd_song063_wangtanshou import award_valid as wyd63_award_valid
                        except ImportError: from wyd_song063_wangtanshou import award_valid as wyd63_award_valid
                        valid = wyd63_award_valid(h, chapters[d['chapter_id']], gift_life_events, root)
                    elif isinstance(basis,dict) and basis.get('kind')=='nan22jian_funeral_award':
                        try: from scripts.nanshi022_wangjian_source import award_valid as n22jian_award_valid
                        except ImportError: from nanshi022_wangjian_source import award_valid as n22jian_award_valid
                        valid=n22jian_award_valid(h,chapters[d['chapter_id']],gift_life_events,root)
                    elif isinstance(basis, dict) and basis.get('kind') == 'qi23_wang_death_award':
                        try: from scripts.qi023_wangjian_witnesses import award_valid as qi23_award_valid
                        except ImportError: from qi023_wangjian_witnesses import award_valid as qi23_award_valid
                        valid = qi23_award_valid(h,chapters[d['chapter_id']],gift_life_events,root)
                    elif isinstance(basis, dict) and basis.get('kind') == 'song071_ws_wang_posthumous_awards':
                        try: from scripts.ws_song071_wang import award_valid as ws71_award_valid
                        except ImportError: from ws_song071_wang import award_valid as ws71_award_valid
                        valid = ws71_award_valid(h, chapters[d['chapter_id']], gift_life_events, root)
                    elif isinstance(basis, dict) and basis.get('kind') == 'song071_print_wang_posthumous_awards':
                        try: from scripts.wyd_song071_wang import award_valid as wyd71_award_valid
                        except ImportError: from wyd_song071_wang import award_valid as wyd71_award_valid
                        valid = wyd71_award_valid(h, chapters[d['chapter_id']], gift_life_events, root)
                    elif isinstance(basis, dict) and basis.get('kind') == 'song071_wang_posthumous_awards':
                        try: from scripts.song071_wang_awards import valid as song071_award_valid
                        except ImportError: from song071_wang_awards import valid as song071_award_valid
                        valid = song071_award_valid(h, paragraphs, mentions, gift_life_events)
                    elif isinstance(basis, dict) and basis.get('kind') == 'named_jin079_family_death_award':
                        try: from scripts.jin079_family_awards import valid as family_award_valid
                        except ImportError: from jin079_family_awards import valid as family_award_valid
                        valid = family_award_valid(h, paragraphs, mentions, gift_life_events)
                    elif isinstance(basis, dict) and basis.get('kind') == 'named_recipient_after_death':
                        try:
                            from scripts.named_posthumous_naming import named_posthumous_naming_valid
                        except ImportError:
                            from named_posthumous_naming import named_posthumous_naming_valid
                        valid = named_posthumous_naming_valid(h, paragraphs, mentions, gift_life_events)
                    elif isinstance(basis, dict) and basis.get('kind') == 'heading_title_confirmed_by_posthumous_notice':
                        try:
                            from scripts.song041_title_semantics import heading_posthumous_valid
                        except ImportError:
                            from song041_title_semantics import heading_posthumous_valid
                        valid = heading_posthumous_valid(h, paragraphs, gift_life_events)
                    else:
                        explicit_naming = False
                        if isinstance(basis, dict) and isinstance(basis.get('source_term'), str):
                            term = basis['source_term']
                            explicit_naming = bool(re.search(r'(?:諡|謚)(?:為|爲|曰)?' + re.escape(h['title']), term))
                            named = re.search(r'立號曰[「『]?' + re.escape(h['title']) + r'[」』]?', term)
                            death = basis.get('death_term')
                            if named and isinstance(death, str) and death and death in term:
                                explicit_naming |= term.index(death) + len(death) <= named.start()
                        valid=(h['mode']=='posthumous_naming' and isinstance(basis,dict)
                               and set(basis)=={'source_term','death_term','evidence'}
                               and isinstance(basis['source_term'],str)
                               and explicit_naming
                               and h['title'] in basis['source_term']
                               and isinstance(basis['death_term'],str)
                               and bool(re.search(r'卒|薨|死',basis['death_term']))
                               and isinstance(basis['evidence'],list) and bool(basis['evidence'])
                               and basis['evidence']==h['effective_period']['start']['evidence']
                               and all(isinstance(e,dict) and isinstance(e.get('quote'),str)
                                       and basis['source_term'] in e['quote'] and basis['death_term'] in e['quote']
                                       for e in basis['evidence']))
                    if d['chapter_id']=='c-liangshu-021-wangxun' and h['title']=='溫子':
                        try: from scripts.liang021_wangxun import naming_valid as xun21_name
                        except ImportError: from liang021_wangxun import naming_valid as xun21_name
                        valid=xun21_name(h,chapters[d['chapter_id']],root)
                    if isinstance(basis,dict) and basis.get('kind')=='nan23_yan_gift_and_name':
                        try: from scripts.nan023_digital import yan_award as nan23_yan_award
                        except ImportError: from nan023_digital import yan_award as nan23_yan_award
                        valid=nan23_yan_award(h,chapters[d['chapter_id']],root)
                    if isinstance(basis,dict) and basis.get('kind')=='nan23p_yan_gift_and_name':
                        try: from scripts.nan023_print import yan_award as nan23p_yan_award
                        except ImportError: from nan023_print import yan_award as nan23p_yan_award
                        valid=nan23p_yan_award(h,chapters[d['chapter_id']],root)
                    if h.get('naming_basis',{}).get('kind') == 'nanshi024_wangmeng_funeral_award':
                        try: from scripts.nanshi024_wangmeng import funeral_award as wangmeng_funeral_award
                        except ImportError: from nanshi024_wangmeng import funeral_award as wangmeng_funeral_award
                        valid=wangmeng_funeral_award(h,chapters[d['chapter_id']],gift_life_events,root)
                    if h.get('naming_basis',{}).get('kind') == 'nanshi024_wangsiyuan_funeral_award':
                        try: from scripts.nanshi024_wangsiyuan import funeral_award as wangsiyuan_funeral_award
                        except ImportError: from nanshi024_wangsiyuan import funeral_award as wangsiyuan_funeral_award
                        valid=wangsiyuan_funeral_award(h,chapters[d['chapter_id']],gift_life_events,root)
                    check(valid,'死後諡名缺少相符命名詞、死亡詞與起點證據')
                    if valid:
                        for e in basis['evidence']:title_evidence(e)
                if 'reported_office_event_counts' in h:
                    counts = h['reported_office_event_counts']
                    valid = (h['kind'] == 'office' and isinstance(counts, dict) and bool(counts)
                             and all(reported_office_event_count_valid(c, key) for key, c in counts.items()))
                    check(valid, '離相或復位次數缺少相符原詞與來源證據')
                    if valid:
                        for count in counts.values():
                            for e in count['evidence']: title_evidence(e)
                if 'reported_appointment_count' in h:
                    count = h['reported_appointment_count']
                    valid = reported_appointment_count_valid(count, h['title'])
                    check(valid, '任用次數缺少相符數詞、稱號與來源證據')
                    if valid:
                        for e in count['evidence']: title_evidence(e)
                if 'reported_duration' in h:
                    duration=h['reported_duration']
                    required={'value','unit','source_term','source_number','counting','status','evidence'}
                    bounded=isinstance(duration,dict) and 'bounds' in duration
                    approximate=isinstance(duration,dict) and 'approximation' in duration
                    valid=isinstance(duration,dict) and set(duration)==required | ({'bounds'} if bounded else set()) | ({'approximation'} if approximate else set())
                    if valid:
                        number=duration['source_number']; digits='一二三四五六七八九'; parsed=None
                        if isinstance(number,str):
                            if number in digits and len(number)==1:parsed=digits.index(number)+1
                            elif re.fullmatch('[一二三四五六七八九]?十[一二三四五六七八九]?',number):
                                tens,ones=number.split('十')
                                parsed=(digits.index(tens)+1 if tens else 1)*10+(digits.index(ones)+1 if ones else 0)
                        common=(duration['unit'] in ('regnal_year','title_year','title_month')
                            and duration['counting'] in ('inclusive_regnal_years','unspecified_source_years','unspecified_source_months')
                            and ((duration['unit']=='title_month')==(duration['counting']=='unspecified_source_months'))
                            and (duration['unit']!='title_year' or duration['counting']=='unspecified_source_years')
                            and duration['status']=='source_attested' and isinstance(duration['source_term'],str)
                            and isinstance(duration['evidence'],list) and bool(duration['evidence'])
                            and all(isinstance(e,dict) and isinstance(e.get('quote'),str)
                                    and duration['source_term'] in e['quote'] for e in duration['evidence']))
                        if approximate:
                            approximation=duration['approximation']
                            numbers=approximation.get('numbers') if isinstance(approximation,dict) else None
                            source_numbers=([digits.index(c)+1 for c in number]
                                if isinstance(number,str) and len(number)==2 and all(c in digits for c in number) else None)
                            valid=(common and not bounded and duration['unit']=='title_year'
                                and duration['value'] is None
                                and isinstance(approximation,dict) and set(approximation)=={'kind','numbers'}
                                and approximation['kind']=='adjacent_year_numbers'
                                and isinstance(numbers,list) and len(numbers)==2
                                and all(type(n) is int for n in numbers) and numbers==source_numbers
                                and numbers[1]==numbers[0]+1
                                and re.search(r'(?<![零〇一二三四五六七八九十百千萬億廿卅卌兩])'
                                    +re.escape(number)+r'(?:年|歲|歳)',duration['source_term']) is not None)
                            check(valid,'稱號相鄰年數約數須保留原數詞、未知精確值及非界限數字')
                        elif bounded:
                            implicit_month = (duration['unit']=='title_month' and number is None
                                and duration['source_term'] in ('居月餘','月餘'))
                            if implicit_month:parsed=1
                            bounds=duration['bounds']
                            literal=(implicit_month or isinstance(number,str) and (
                                duration['unit']=='title_month' and duration['source_term']==number+'餘月'
                                or duration['unit']=='title_year' and duration['source_term'] in
                                    (number+'餘年',number+'餘歲',number+'餘歳')))
                            valid=(common and duration['unit'] in ('title_month','title_year')
                                and duration['value'] is None and parsed is not None
                                and isinstance(bounds,dict) and type(bounds.get('lower')) is int
                                and bounds=={'lower':parsed,'lower_inclusive':False,'upper':None,'upper_inclusive':None}
                                and literal)
                            check(valid,'稱號時長界限須保留餘字、未知精確值及排他下界')
                        else:
                            valid=(common and type(duration['value']) is int and parsed is not None
                                and duration['value']==parsed
                                and re.search(r'(?<![零〇一二三四五六七八九十百千萬億廿卅卌兩])'
                                    +re.escape(number)+(r'月' if duration['unit']=='title_month' else r'(?:年|歲|歳)'),duration['source_term']) is not None)
                    check(valid,'稱號來源在位年數或原詞證據無效')
                    if valid:
                        for e in duration['evidence']:title_evidence(e)
                if 'duration_scope' in h:
                    scope = h['duration_scope']
                    ids = scope.get('holding_ids') if isinstance(scope, dict) else None
                    valid = (isinstance(scope, dict)
                        and set(scope) == {'kind', 'holding_ids', 'relation', 'rationale'}
                        and scope['kind'] == 'multiple_holdings'
                        and isinstance(ids, list) and len(ids) >= 2
                        and all(isinstance(i, str) for i in ids) and len(set(ids)) == len(ids)
                        and h['id'] in ids and bool(scope['rationale'])
                        and scope['relation'] in ('successive', 'unspecified')
                        and isinstance(h.get('reported_duration'), dict)
                        and h['reported_duration'].get('unit') == 'title_year'
                        and all(i in title_records and title_records[i]['person_id'] == h['person_id']
                                and title_records[i]['kind'] == h['kind'] for i in ids))
                    check(valid, '跨稱號任事年數缺少同人同類稱號與明示範圍')
                if 'granting_polity' in h:
                    polity = h['granting_polity']; valid = isinstance(polity, dict)
                    check(valid and polity.get('authority_person_id') in pids
                          and polity.get('place_id') is None and polity.get('modern_identification') is None
                          and bool(polity.get('source_name')) and bool(polity.get('evidence')),
                          '授予政體須有原國名、授予者與證據，不補現代位置')
                    if valid:
                        for e in polity.get('evidence', []):
                            hit = paragraphs.get(e.get('paragraph_id')); anchor = mentions.get(e.get('person_mention_id'))
                            quote = e.get('quote'); name = polity.get('source_name')
                            check(bool(hit) and hit[0] == d['chapter_id'] == e.get('chapter_id')
                                  and e.get('source_id') == chapters[d['chapter_id']]['source_id']
                                  and isinstance(quote, str) and quote in hit[1]['text']
                                  and isinstance(name, str) and name in quote and bool(anchor)
                                  and anchor[1] == e.get('paragraph_id') and name in anchor[2]['surface']
                                  and anchor[2]['person_id'] == polity.get('authority_person_id')
                                  and any(i <= anchor[2]['start'] and anchor[2]['end'] <= i + len(quote)
                                          for i in range(len(hit[1]['text'])) if hit[1]['text'].startswith(quote, i)),
                                  '授予政體原國名與授予者錨點或引句不符')
                if 'service_realization' in h:
                    service = h['service_realization']
                    check(isinstance(service, dict) and set(service) == {'status', 'source_term', 'evidence'}
                          and h['mode'] == 'grant' and service.get('status') == 'not_taken_up'
                          and '不往' in service.get('source_term', '') and bool(service.get('evidence')),
                          '授予未赴任須保留不往原詞與證據，不改成已實任')
                    if isinstance(service, dict):
                        for e in service.get('evidence', []):
                            hit = paragraphs.get(e.get('paragraph_id')); anchor = mentions.get(e.get('person_mention_id'))
                            check(bool(hit) and hit[0] == d['chapter_id'] == e.get('chapter_id')
                                  and e.get('source_id') == chapters[d['chapter_id']]['source_id']
                                  and e.get('quote', '') in hit[1]['text']
                                  and service.get('source_term', '') in e.get('quote', '')
                                  and bool(anchor) and anchor[1] == e.get('paragraph_id')
                                  and anchor[2]['person_id'] == h['person_id'], '未赴任人物、來源原詞或證據不符')
                if 'jurisdictions' in h:
                    places=h['jurisdictions']
                    valid=(h['kind'] in ('office','royal_rank') and isinstance(places,list) and bool(places)
                           and all(isinstance(place,dict) and isinstance(place.get('source_name'),str)
                                   and bool(place['source_name'])
                                   and any(place['source_name'] in e.get('quote','') for e in h['evidence'])
                                   and place.get('place_id') is None and place.get('modern_identification') is None
                                   for place in places))
                    check(valid,'稱號所屬原地名缺少引句或未保留未知定位')
                    if h['kind']=='royal_rank':
                        royal=(h['title']=='王' and isinstance(places,list) and bool(places)
                               and all(isinstance(place,dict) and isinstance(place.get('source_name'),str)
                                       and any('王'+place['source_name'] in e.get('quote','') for e in h['evidence'])
                                       for place in places))
                        if not royal and h.get('mode') == 'transfer' and (
                                'resumption_basis' in h or h.get('transfer_basis', {}).get('kind') == 'elided_rank_regrant'):
                            royal = not royal_transfer_errors(h, title_records, paragraphs, mentions)
                        check(royal,'王國範圍須保留王某地原句，不得由任意地名補入')
                for a in h['attestations']:
                    check(a['id'] not in title_occurrence_ids,'稱號用稱 ID 重複');title_occurrence_ids.add(a['id'])
                    hit=paragraphs.get(a['paragraph_id']);m=mentions.get(a['person_mention_id'])
                    check(bool(hit) and hit[0]==d['chapter_id'],'稱號用稱段落不符')
                    carried_title_subject = False
                    if 'context' in a:
                        try:
                            from scripts.subject_continuation import title_attestation_subject_valid
                        except ImportError:
                            from subject_continuation import title_attestation_subject_valid
                        carried_title_subject = title_attestation_subject_valid(a, h, chapters[d['chapter_id']])
                        check(carried_title_subject, '稱號用稱省略主語承接無效')
                    check(wyd63_title_reference or carried_title_subject or bool(m) and m[1]==a['paragraph_id'] and m[2]['person_id']==h['person_id'],'稱號用稱人物提及不符')
                    shared_suffix_valid = False
                    if 'shared_title_suffix' in h:
                        try:
                            from scripts.biographical_appointment_sequence import holding_valid
                        except ImportError:
                            from biographical_appointment_sequence import holding_valid
                        shared_suffix_valid = holding_valid(h, chapters[d['chapter_id']], root)
                        if 'source_career_role' in h:
                            try:
                                from scripts.received_career_roles import holding_valid as career_holding_valid
                            except ImportError:
                                from received_career_roles import holding_valid as career_holding_valid
                            shared_suffix_valid = career_holding_valid(h, chapters[d['chapter_id']],root)
                    if h.get('shared_title_suffix', {}).get('kind') == 'liang050_received_county_pair':
                        try: from scripts.liang050_county_pair import valid as county_pair_valid
                        except ImportError: from liang050_county_pair import valid as county_pair_valid
                        shared_suffix_valid = county_pair_valid(h, chapters[d['chapter_id']], root)
                    check((a['surface']==h['title'] or shared_suffix_valid) and a['usage'] in ('narrative','retrospective','posthumous_usage'),'稱號用稱文字或種類不符')
                    if hit:
                        check(isinstance(a['start'],int) and isinstance(a['end'],int) and 0<=a['start']<a['end']<=len(hit[1]['text']) and hit[1]['text'][a['start']:a['end']]==a['surface'],'稱號用稱字元位置不符')
                        enclosed=False
                        for e in h['evidence']:
                            if e['paragraph_id']!=a['paragraph_id']:continue
                            starts=[i for i in range(len(hit[1]['text'])) if hit[1]['text'].startswith(e['quote'],i)]
                            if any(i<=a['start'] and a['end']<=i+len(e['quote']) and (wyd63_title_reference or carried_title_subject or m and i<=m[2]['start'] and m[2]['end']<=i+len(e['quote'])) for i in starts):enclosed=True
                        check(enclosed,'稱號用稱及持有人不在精確引句範圍')
                    if 'normalized_date' in a:
                        expression = a.get('date_expression')
                        check(expression is None or isinstance(expression, str) and bool(expression), '用稱日期表述無效')
                        validate_date_evidence(a['normalized_date'], h['evidence'], expression, h, 'attestation')
                    if 'normalized_date_range' in a:
                        try:
                            from scripts.date_ranges import year_range_errors
                        except ImportError:
                            from date_ranges import year_range_errors
                        check('normalized_date' not in a, '用稱跨年範圍不得另填確定單年')
                        expression = a.get('date_expression')
                        errors.extend(year_range_errors(a['normalized_date_range'], h['evidence'], expression))
                        errors.extend(table_regnal_range_errors(a['normalized_date_range'], expression, tables, mentions))
                period=h['effective_period']
                for endpoint in ('start','end'):
                    boundary=period[endpoint]
                    check(boundary['status'] in ('unknown','source_event'),'稱號時段端點狀態無效')
                    expected={'status','date_expression','evidence'}
                    if boundary['status']=='source_event':
                        expected.add('event_type')
                        if 'normalized_date' in boundary:expected.add('normalized_date')
                        if 'normalized_date_range' in boundary:expected.add('normalized_date_range')
                    check(set(boundary)==expected,'稱號端點含未定義欄位，不能暗補正規化日期')
                    if boundary['status']=='unknown':
                        check(boundary['date_expression'] is None and not boundary['evidence'] and 'event_type' not in boundary,'未知稱號端點不得暗補日期或事件')
                    else:
                        check(bool(boundary['evidence']),'稱號時段事件缺少證據')
                        allowed=('grant','transfer','posthumous_grant','posthumous_enfeoffment','posthumous_naming','self_proclamation','accession','demotion') if endpoint=='start' else ('deposition','renunciation','abolition','explicit_end')
                        check(boundary['event_type'] in allowed,'稱號端點事件類型無效，死亡或首次用稱不得自動替代起訖')
                        for e in boundary['evidence']:title_evidence(e)
                        date=boundary['date_expression']
                        cross_endpoint_date = False
                        if 'cross_chapter_event_binding' in boundary.get('normalized_date', {}):
                            try:
                                from scripts.cross_chapter_annal_date import cross_chapter_annal_date_valid
                            except ImportError:
                                from cross_chapter_annal_date import cross_chapter_annal_date_valid
                            cross_endpoint_date = cross_chapter_annal_date_valid(boundary['normalized_date'], h, endpoint, chapters)
                        if 'rendered_collective_award_year_binding' in boundary.get('normalized_date', {}):
                            try:from scripts.wyd_song044_noble_year import valid as noble_year_valid
                            except ImportError:from wyd_song044_noble_year import valid as noble_year_valid
                            cross_endpoint_date=noble_year_valid(boundary['normalized_date'],h,endpoint,chapters,root)
                        check(cross_endpoint_date or date is None or isinstance(date,str) and bool(date) and any(date in e['quote'] for e in boundary['evidence']),'稱號日期表述不在端點證據')
                        if 'normalized_date' in boundary:
                            check(isinstance(date, str) and bool(date) or parallel_event_date(boundary['normalized_date']), '稱號數字紀年須有原始日期表述')
                            validate_date_evidence(boundary['normalized_date'], boundary['evidence'], date, h, endpoint)
                        if 'normalized_date_range' in boundary:
                            try:
                                from scripts.date_ranges import year_range_errors
                            except ModuleNotFoundError:
                                from date_ranges import year_range_errors
                            check('normalized_date' not in boundary, '稱號單年與範圍不可同時採用')
                            year_window = boundary['normalized_date_range']
                            range_expression = date
                            if isinstance(year_window, dict) and 'parallel_event' in year_window:
                                parallel = dict(year_window, basis=year_window['parallel_event'])
                                valid = date is None and parallel_event_date(parallel)
                                check(valid, '稱號跨年範圍平行事件對讀無效')
                                errors.extend(table_title_range_errors(year_window, h, endpoint, tables, boundary))
                                if valid:
                                    range_expression = year_window['parallel_event']['source_event_quote']
                            errors.extend(year_range_errors(year_window, boundary['evidence'], range_expression, root=root))
                            errors.extend(table_regnal_range_errors(year_window, date, tables, mentions))
                check(period['start']['status']==('unknown' if h['mode']=='attestation' else 'source_event'),'稱號起點與授予／用稱種類不符')
                if h['mode']!='attestation':check(period['start'].get('event_type')==h['mode'],'稱號起點與事件種類不符')
        aids=set()
        # Table-native title assertions retain cells and composed column dates.
        for path in (root/'corpus').glob('*/*-table-title-events.json'):
            d=json.loads(path.read_text(encoding='utf-8'))
            table=tables.get(d.get('table_id'))
            check(d.get('record_type')=='table_title_holding_assertion_set' and bool(table)
                  and d.get('chapter_id')==table['source']['chapter_id'], '表格原生稱號集來源或篇ID不符')
            try:
                from scripts.table_title_holdings import table_title_errors
            except ImportError:
                from table_title_holdings import table_title_errors
            for h in d.get('holdings',[]):
                check(h.get('table_title_basis',{}).get('table_id')==d.get('table_id'),'表格稱號不得跨集換來源')
                check(h.get('id') not in title_ids,'稱號持有 ID 重複');title_ids.add(h.get('id'))
                errors.extend(table_title_errors(h,tables,pids))
                for a in h.get('attestations',[]):
                    check(a.get('id') not in title_occurrence_ids,'稱號用稱 ID 重複');title_occurrence_ids.add(a.get('id'))

        for path in (root/'corpus').glob('*/*-assertions.json'):
            d=json.loads(path.read_text(encoding='utf-8'))
            check(d['record_type']=='person_assertion_set','人物陳述集類型不符')
            check(d['chapter_id'] in chapters or d['chapter_id'] in table_chapters,'人物陳述集篇不存在')
            try: from scripts.wangyun_external_sources import kinship_errors as wangyun_external_kinship_errors
            except ImportError: from wangyun_external_sources import kinship_errors as wangyun_external_kinship_errors
            if d['chapter_id'] in chapters:
                errors.extend(wangyun_external_kinship_errors(d['assertions'], chapters[d['chapter_id']], root))
            if d['chapter_id'] in chapters:
                try: from scripts.liang033_wangyun_witness import side_errors as liang33_side_errors
                except ImportError: from liang033_wangyun_witness import side_errors as liang33_side_errors
                errors.extend(liang33_side_errors(d, chapters[d['chapter_id']], root, 'assertions'))
            if d['chapter_id'] in chapters:
                try: from scripts.liang021_wangtai_readings import side_errors as tai21_side_errors
                except ImportError: from liang021_wangtai_readings import side_errors as tai21_side_errors
                errors.extend(tai21_side_errors(d,chapters[d['chapter_id']],root,'assertions'))
            if d['chapter_id'] in chapters:
                try: from scripts.liang021_wangjun import side_errors as j21_side_errors
                except ImportError: from liang021_wangjun import side_errors as j21_side_errors
                errors.extend(j21_side_errors(d,chapters[d['chapter_id']],root,'assertions'))
            if d['chapter_id'] in chapters:
                try: from scripts.liang021_wangfen_family import side_errors as wf21_side_errors
                except ImportError: from liang021_wangfen_family import side_errors as wf21_side_errors
                errors.extend(wf21_side_errors(d,chapters[d['chapter_id']],root,'assertions'))
            if d['chapter_id'] in chapters:
                try: from scripts.liang021_wangxun import side_errors as xun21_side_errors
                except ImportError: from liang021_wangxun import side_errors as xun21_side_errors
                errors.extend(xun21_side_errors(d,chapters[d['chapter_id']],root,'assertions'))
            if d['chapter_id'] in chapters:
                try: from scripts.liang021_wangjiansihui import side_errors as sih21_side_errors
                except ImportError: from liang021_wangjiansihui import side_errors as sih21_side_errors
                errors.extend(sih21_side_errors(d,chapters[d['chapter_id']],root,'assertions'))
            if d['chapter_id'] in chapters:
                try: from scripts.song052_xiechun import side_errors as chun52_side_errors
                except ImportError: from song052_xiechun import side_errors as chun52_side_errors
                errors.extend(chun52_side_errors(d,chapters[d['chapter_id']],root,'assertions'))
            if d['chapter_id'] in chapters:
                try: from scripts.song052_xiejingren import side_errors as xiejingren52_side_errors
                except ImportError: from song052_xiejingren import side_errors as xiejingren52_side_errors
                errors.extend(xiejingren52_side_errors(d,chapters[d['chapter_id']],root,'assertions'))
            if d['chapter_id'] in chapters:
                try: from scripts.nan023_digital import side_errors as nan23dan_side_errors
                except ImportError: from nan023_digital import side_errors as nan23dan_side_errors
                errors.extend(nan23dan_side_errors(d,chapters[d['chapter_id']],root,'assertions'))
            if d['chapter_id'] in chapters:
                try: from scripts.song052_wangdan import side_errors as wangdan52_side_errors
                except ImportError: from song052_wangdan import side_errors as wangdan52_side_errors
                errors.extend(wangdan52_side_errors(d,chapters[d['chapter_id']],root,'assertions'))
            if d['chapter_id'] in chapters:
                try: from scripts.song052_xieshu import side_errors as xieshu52_side_errors
                except ImportError: from song052_xieshu import side_errors as xieshu52_side_errors
                errors.extend(xieshu52_side_errors(d,chapters[d['chapter_id']],root,'assertions'))
            if d['chapter_id'] in chapters:
                try: from scripts.nan023_print import side_errors as nan23p_side_errors
                except ImportError: from nan023_print import side_errors as nan23p_side_errors
                errors.extend(nan23p_side_errors(d,chapters[d['chapter_id']],root,'assertions'))
            if d['chapter_id'] in chapters:
                try: from scripts.nan023_wangmao import side_errors as nan23mao_side_errors
                except ImportError: from nan023_wangmao import side_errors as nan23mao_side_errors
                errors.extend(nan23mao_side_errors(d,chapters[d['chapter_id']],root,'assertions'))
            if d['chapter_id'] in chapters:
                try: from scripts.nan023_jiangxiao import side_errors as nan23jiang_side_errors
                except ImportError: from nan023_jiangxiao import side_errors as nan23jiang_side_errors
                errors.extend(nan23jiang_side_errors(d,chapters[d['chapter_id']],root,'assertions'))
            if d['chapter_id'] in chapters:
                try: from scripts.nan023_chuai import side_errors as nan23chuai_side_errors
                except ImportError: from nan023_chuai import side_errors as nan23chuai_side_errors
                errors.extend(nan23chuai_side_errors(d,chapters[d['chapter_id']],root,'assertions'))
            if d['chapter_id'] in chapters:
                try: from scripts.nan023_heyu import side_errors as nan23heyu_side_errors
                except ImportError: from nan023_heyu import side_errors as nan23heyu_side_errors
                errors.extend(nan23heyu_side_errors(d,chapters[d['chapter_id']],root,'assertions'))
            if d['chapter_id'] in chapters:
                try: from scripts.nan023_wangzao import side_errors as nan23zao_side_errors
                except ImportError: from nan023_wangzao import side_errors as nan23zao_side_errors
                errors.extend(nan23zao_side_errors(d,chapters[d['chapter_id']],root,'assertions'))
            if d['chapter_id'] in chapters:
                try: from scripts.nan023_wangliang import side_errors as nan23liang_side_errors
                except ImportError: from nan023_wangliang import side_errors as nan23liang_side_errors
                errors.extend(nan23liang_side_errors(d,chapters[d['chapter_id']],root,'assertions'))
            if d['chapter_id'] in chapters:
                try: from scripts.nan023_wangying import side_errors as nan23ying_side_errors
                except ImportError: from nan023_wangying import side_errors as nan23ying_side_errors
                errors.extend(nan23ying_side_errors(d,chapters[d['chapter_id']],root,'assertions'))
            if d['chapter_id'] in chapters:
                try: from scripts.nan023_wanghui import side_errors as nan23hui_side_errors
                except ImportError: from nan023_wanghui import side_errors as nan23hui_side_errors
                errors.extend(nan23hui_side_errors(d,chapters[d['chapter_id']],root,'assertions'))
            if d['chapter_id'] in chapters:
                try: from scripts.nan023_wangqiu import side_errors as nan23qiu_side_errors
                except ImportError: from nan023_wangqiu import side_errors as nan23qiu_side_errors
                errors.extend(nan23qiu_side_errors(d,chapters[d['chapter_id']],root,'assertions'))
            if d['chapter_id'] in chapters:
                try: from scripts.nan023_wangxuan import side_errors as nan23xuan_side_errors
                except ImportError: from nan023_wangxuan import side_errors as nan23xuan_side_errors
                errors.extend(nan23xuan_side_errors(d,chapters[d['chapter_id']],root,'assertions'))
            if d['chapter_id'] in chapters:
                try: from scripts.nan023_wanghui_sons import side_errors as nan23huiz_side_errors
                except ImportError: from nan023_wanghui_sons import side_errors as nan23huiz_side_errors
                errors.extend(nan23huiz_side_errors(d,chapters[d['chapter_id']],root,'assertions'))
            if d['chapter_id'] in chapters:
                try: from scripts.nan023_chuzhanzhi import side_errors as nan23chu_side_errors
                except ImportError: from nan023_chuzhanzhi import side_errors as nan23chu_side_errors
                errors.extend(nan23chu_side_errors(d,chapters[d['chapter_id']],root,'assertions'))
            if d['chapter_id'] in chapters:
                try: from scripts.nan023_wangyun import side_errors as nan23yun_side_errors
                except ImportError: from nan023_wangyun import side_errors as nan23yun_side_errors
                errors.extend(nan23yun_side_errors(d,chapters[d['chapter_id']],root,'assertions'))
            if d['chapter_id'] in chapters:
                try: from scripts.nan023_wanghuan import side_errors as nan23huan_side_errors
                except ImportError: from nan023_wanghuan import side_errors as nan23huan_side_errors
                errors.extend(nan23huan_side_errors(d,chapters[d['chapter_id']],root,'assertions'))
            if d['chapter_id'] in chapters:
                try: from scripts.nan023_wangxi import side_errors as nan23xi_side_errors
                except ImportError: from nan023_wangxi import side_errors as nan23xi_side_errors
                errors.extend(nan23xi_side_errors(d,chapters[d['chapter_id']],root,'assertions'))
            if d['chapter_id'] in chapters:
                try: from scripts.nan023_wangfen import side_errors as nan23fen_side_errors
                except ImportError: from nan023_wangfen import side_errors as nan23fen_side_errors
                errors.extend(nan23fen_side_errors(d,chapters[d['chapter_id']],root,'assertions'))
            if d['chapter_id'] in chapters:
                try: from scripts.nan023_wangtong import side_errors as nan23tong_side_errors
                except ImportError: from nan023_wangtong import side_errors as nan23tong_side_errors
                errors.extend(nan23tong_side_errors(d,chapters[d['chapter_id']],root,'assertions'))
            if d['chapter_id'] in chapters:
                try: from scripts.nan023_wangmai import side_errors as nan23mai_side_errors
                except ImportError: from nan023_wangmai import side_errors as nan23mai_side_errors
                errors.extend(nan23mai_side_errors(d,chapters[d['chapter_id']],root,'assertions'))
            if d['chapter_id'] in chapters:
                try: from scripts.nan023_wangzhi import side_errors as nan23zhi_side_errors
                except ImportError: from nan023_wangzhi import side_errors as nan23zhi_side_errors
                errors.extend(nan23zhi_side_errors(d,chapters[d['chapter_id']],root,'assertions'))
            if d['chapter_id'] in chapters:
                try: from scripts.nan023_wanggu import side_errors as nan23gu_side_errors
                except ImportError: from nan023_wanggu import side_errors as nan23gu_side_errors
                errors.extend(nan23gu_side_errors(d,chapters[d['chapter_id']],root,'assertions'))
            if d['chapter_id'] in chapters:
                try: from scripts.nan023_wanghou import side_errors as nan23hou_side_errors
                except ImportError: from nan023_wanghou import side_errors as nan23hou_side_errors
                errors.extend(nan23hou_side_errors(d,chapters[d['chapter_id']],root,'assertions'))
            if d['chapter_id'] in chapters:
                try: from scripts.nan023_wangyu import side_errors as nan23yu_side_errors
                except ImportError: from nan023_wangyu import side_errors as nan23yu_side_errors
                errors.extend(nan23yu_side_errors(d,chapters[d['chapter_id']],root,'assertions'))
            if d['chapter_id'] in chapters:
                try: from scripts.nanqi047_wangrong import side_errors as qi47rong_side_errors
                except ImportError: from nanqi047_wangrong import side_errors as qi47rong_side_errors
                errors.extend(qi47rong_side_errors(d,chapters[d['chapter_id']],root,'assertions'))
            if d['chapter_id'] in chapters:
                try: from scripts.liang033_wangsengru import side_errors as liang33sr_side_errors
                except ImportError: from liang033_wangsengru import side_errors as liang33sr_side_errors
                errors.extend(liang33sr_side_errors(d,chapters[d['chapter_id']],root,'assertions'))
            if d['chapter_id'] in chapters:
                try: from scripts.nanshi059_wangsengru import side_errors as nan59sr_side_errors
                except ImportError: from nanshi059_wangsengru import side_errors as nan59sr_side_errors
                errors.extend(nan59sr_side_errors(d,chapters[d['chapter_id']],root,'assertions'))
            if d['chapter_id'] in chapters:
                try: from scripts.nanqi047_wangrong_wyd import side_errors as q47wyd_sides
                except ImportError: from nanqi047_wangrong_wyd import side_errors as q47wyd_sides
                errors.extend(q47wyd_sides(d,chapters[d['chapter_id']],root,'assertions'))
            if d['chapter_id'] in chapters:
                try: from scripts.nanshi024_wangshaozhi import side_errors as nan24sz_side_errors
                except ImportError: from nanshi024_wangshaozhi import side_errors as nan24sz_side_errors
                errors.extend(nan24sz_side_errors(d,chapters[d['chapter_id']],root,'assertions'))
            if d['chapter_id'] in chapters:
                try: from scripts.nanshi024_wangshaozhi_wyd import side_errors as n24szwyd_sides
                except ImportError: from nanshi024_wangshaozhi_wyd import side_errors as n24szwyd_sides
                errors.extend(n24szwyd_sides(d,chapters[d['chapter_id']],root,'assertions'))
            if d['chapter_id'] in chapters:
                try: from scripts.nanshi024_wangyuezhi import side_errors as nan24yz_side_errors
                except ImportError: from nanshi024_wangyuezhi import side_errors as nan24yz_side_errors
                errors.extend(nan24yz_side_errors(d,chapters[d['chapter_id']],root,'assertions'))
            if d['chapter_id'] in chapters:
                try: from scripts.nanshi024_wangzhunzhi import side_errors as nan24zz_side_errors
                except ImportError: from nanshi024_wangzhunzhi import side_errors as nan24zz_side_errors
                errors.extend(nan24zz_side_errors(d,chapters[d['chapter_id']],root,'assertions'))
            if d['chapter_id'] in chapters:
                try: from scripts.nanshi024_wangjinzhi import side_errors as nan24jz_side_errors
                except ImportError: from nanshi024_wangjinzhi import side_errors as nan24jz_side_errors
                errors.extend(nan24jz_side_errors(d,chapters[d['chapter_id']],root,'assertions'))
            if d['chapter_id'] in chapters:
                try: from scripts.nanshi024_wangqing import side_errors as nan24qing_side_errors
                except ImportError: from nanshi024_wangqing import side_errors as nan24qing_side_errors
                errors.extend(nan24qing_side_errors(d,chapters[d['chapter_id']],root,'assertions'))
            if d['chapter_id'] in chapters:
                try: from scripts.nanshi024_wangqunzhi import side_errors as nan24qun_side_errors
                except ImportError: from nanshi024_wangqunzhi import side_errors as nan24qun_side_errors
                errors.extend(nan24qun_side_errors(d,chapters[d['chapter_id']],root,'assertions'))
            if d['chapter_id'] in chapters:
                try: from scripts.nanshi024_wangsu import side_errors as nan24su_side_errors
                except ImportError: from nanshi024_wangsu import side_errors as nan24su_side_errors
                errors.extend(nan24su_side_errors(d,chapters[d['chapter_id']],root,'assertions'))
            if d['chapter_id'] in chapters:
                try: from scripts.nanshi024_ruanwanling import side_errors as nan24rw_side_errors
                except ImportError: from nanshi024_ruanwanling import side_errors as nan24rw_side_errors
                errors.extend(nan24rw_side_errors(d,chapters[d['chapter_id']],root,'assertions'))
            if d['chapter_id'] in chapters:
                try: from scripts.nanshi024_wanghongzhi import side_errors as n24hong_sides
                except ImportError: from nanshi024_wanghongzhi import side_errors as n24hong_sides
                errors.extend(n24hong_sides(d,chapters[d['chapter_id']],root,'assertions'))
            if d['chapter_id'] in chapters:
                try: from scripts.song093_wanghongzhi import side_errors as hongzhi_sides
                except ImportError: from song093_wanghongzhi import side_errors as hongzhi_sides
                errors.extend(hongzhi_sides(d,chapters[d['chapter_id']],root,'assertions'))
            if d['chapter_id'] in chapters:
                try: from scripts.song093_wyd import side_errors as s93wyd_sides
                except ImportError: from song093_wyd import side_errors as s93wyd_sides
                errors.extend(s93wyd_sides(d,chapters[d['chapter_id']],root,'assertions'))
            if d['chapter_id'] in chapters:
                try: from scripts.nanshi024_wangmeng import side_errors as nan24meng_side_errors
                except ImportError: from nanshi024_wangmeng import side_errors as nan24meng_side_errors
                errors.extend(nan24meng_side_errors(d,chapters[d['chapter_id']],root,'assertions'))
            if d['chapter_id'] in chapters:
                try: from scripts.xiangshan_m9_epitaphs import side_errors as xm9_side_errors
                except ImportError: from xiangshan_m9_epitaphs import side_errors as xm9_side_errors
                errors.extend(xm9_side_errors(d,chapters[d['chapter_id']],root,'assertions'))
            if d['chapter_id'] in chapters:
                try: from scripts.nanshi024_wangyan import side_errors as nan24yan_side_errors
                except ImportError: from nanshi024_wangyan import side_errors as nan24yan_side_errors
                errors.extend(nan24yan_side_errors(d,chapters[d['chapter_id']],root,'assertions'))
            if d['chapter_id'] in chapters:
                try: from scripts.nanshi024_wangyan_brothers import side_errors as nan24wab_side_errors
                except ImportError: from nanshi024_wangyan_brothers import side_errors as nan24wab_side_errors
                errors.extend(nan24wab_side_errors(d,chapters[d['chapter_id']],root,'assertions'))
            if d['chapter_id'] in chapters:
                try: from scripts.nanshi024_guhaozhi import side_errors as nan24gh_side_errors
                except ImportError: from nanshi024_guhaozhi import side_errors as nan24gh_side_errors
                errors.extend(nan24gh_side_errors(d,chapters[d['chapter_id']],root,'assertions'))
            if d['chapter_id'] in chapters:
                try: from scripts.nanshi024_wangsiyuan import side_errors as nan24siy_side_errors
                except ImportError: from nanshi024_wangsiyuan import side_errors as nan24siy_side_errors
                errors.extend(nan24siy_side_errors(d,chapters[d['chapter_id']],root,'assertions'))
            for a in d['assertions']:
                check(a['id'] not in aids,'人物陳述 ID 重複');aids.add(a['id'])
                check(a['subject_person_id'] in pids and a['object_person_id'] in pids,'人物陳述引用未知人物')
                check(a['subject_person_id']!=a['object_person_id'],'人物陳述關係自環')
                check(a['predicate'] in ('father','mother','maternal_role','stepmother','adoptive_mother','adoptive_father','raised_by','ritual_successor_of','spouse','brother','sister','paternal_uncle','maternal_uncle','maternal_aunt','kinship_generation','agnatic_cousin','agnatic_senior_kin','maternal_cousin', 'grandfathers_brother','grandfather','grandmother','great_grandfather','ancestor','kinship_unspecified','affinity_unspecified','father_in_law','teacher'),'人物陳述關係類型未知')
                check(a['status']=='source_attested' and bool(a['evidence']),'人物陳述未有來源證據')
                qualifiers = a.get('qualifiers', {})
                if 'corroborating_evidence' in a:
                    supporting = a['corroborating_evidence']
                    check(a['predicate'] == 'spouse' and isinstance(supporting, list) and bool(supporting),
                          '婚配對讀須附已具直接證據的配偶陳述')
                    for ref in supporting:
                        hit = paragraphs.get(ref.get('paragraph_id'))
                        witness = chapters.get(ref.get('chapter_id'), {})
                        check(bool(hit) and hit[0] == ref.get('chapter_id')
                              and all(ref.get(key) == witness.get(key) for key in ('work_id', 'book_id', 'source_id'))
                              and bool(ref.get('quote')) and ref['quote'] in hit[1]['text']
                              and ref.get('role') in ('marriage_context', 'joint_burial_attestation',
                                  'spouse_title_identification', 'burial_year_context',
                                  'matching_burial_attestation', 'shared_burial_wording'),
                              '婚配對讀須保存可定位的原句及其證據角色')
                if 'source_kinship_frame' in qualifiers or a['predicate'] == 'father_in_law':
                    try:
                        from scripts.received_quoted_family import valid as received_quoted_family_valid
                    except ImportError:
                        from received_quoted_family import valid as received_quoted_family_valid
                    check(received_quoted_family_valid(a, paragraphs, chapters, root), '收到本傳或引書親屬須綁完整原句、固定raw、實際角色及方向，不補未名連接人')
                if 'nanshi024_reported_kin' in qualifiers:
                    try: from scripts.nanshi024_reported_kin import valid as n24_reported_family
                    except ImportError: from nanshi024_reported_kin import valid as n24_reported_family
                    check(all(n24_reported_family(a, e, chapters[e['chapter_id']]) for e in a['evidence']),
                          '南史二十四敬弘妻、妻弟與兩處女兒稱謂須符合固定原句與雙人字位')
                if 'literal_source_binding' in qualifiers:
                    try:
                        from scripts.literal_family_reports import kinship_valid
                    except ImportError:
                        from literal_family_reports import kinship_valid
                    check(kinship_valid(a, paragraphs, chapters, root), '逐字親屬句須有同源正文層、雙端角色與完整固定raw，不補父代或排行')
                pei_valid = False
                if 'pei_kin_frame' in qualifiers:
                    try: from scripts.pei_royal_biographies import kin_valid as pei_kin_valid
                    except ImportError: from pei_royal_biographies import kin_valid as pei_kin_valid
                    pei_valid=pei_kin_valid(a,chapters[d['chapter_id']],root)
                    check(pei_valid,'裴后與兩妃的原文身分、父母及婚配方向不合')
                n22jian_valid = False
                if 'nan22jian_kin_frame' in qualifiers:
                    try: from scripts.nanshi022_wangjian_source import kin_valid as n22jian_kin_valid
                    except ImportError: from nanshi022_wangjian_source import kin_valid as n22jian_kin_valid
                    n22jian_valid=n22jian_kin_valid(a,chapters[d['chapter_id']],root)
                    check(n22jian_valid,'王儉、王遜及所引世系原文端點不合')
                wyd63_kinship = False
                if 'wyd_song063_kin_frame' in qualifiers:
                    try: from scripts.wyd_song063_wangtanshou import kin_valid as wyd63_kin_valid
                    except ImportError: from wyd_song063_wangtanshou import kin_valid as wyd63_kin_valid
                    wyd63_kinship = wyd63_kin_valid(a, chapters[d['chapter_id']], root)
                    check(wyd63_kinship, '宋卷六十三殿本親屬須核兩端稱謂及具名、長幼和方向')
                liang33_valid = False
                if 'liang033_family_reading' in qualifiers:
                    try: from scripts.liang033_wangyun_witness import kin_valid as liang33_kin_valid
                    except ImportError: from liang033_wangyun_witness import kin_valid as liang33_kin_valid
                    liang33_valid = liang33_kin_valid(a,chapters[d['chapter_id']],root)
                    check(liang33_valid, '王筠、謝覽兄弟等原句須核兩端及方向')
                tai21_valid=False
                if 'liang021_tai_reading' in qualifiers:
                    try: from scripts.liang021_wangtai_readings import kin_valid as tai21_kin_valid
                    except ImportError: from liang021_wangtai_readings import kin_valid as tai21_kin_valid
                    tai21_valid=tai21_kin_valid(a,chapters[d['chapter_id']],root)
                    check(tai21_valid,'王泰親屬及府主親屬的方向與原文不符')
                j21_valid=False
                if 'liang021_jun_reading' in qualifiers:
                    try: from scripts.liang021_wangjun import kin_valid as j21_kin_valid
                    except ImportError: from liang021_wangjun import kin_valid as j21_kin_valid
                    j21_valid=j21_kin_valid(a,chapters[d['chapter_id']],root)
                    check(j21_valid,'王峻、琮親屬原字及其方向須相符')
                wf21_valid=False
                if 'liang021_fen_reading' in qualifiers:
                    try: from scripts.liang021_wangfen_family import kin_valid as wf21_kin_valid
                    except ImportError: from liang021_wangfen_family import kin_valid as wf21_kin_valid
                    wf21_valid=wf21_kin_valid(a,chapters[d['chapter_id']],root)
                    check(wf21_valid,'王份家親屬原字及其方向須相符')
                xun21_valid=False
                if 'liang021_wangxun_reading' in qualifiers:
                    try: from scripts.liang021_wangxun import kin_valid as xun21_kin_valid
                    except ImportError: from liang021_wangxun import kin_valid as xun21_kin_valid
                    xun21_valid=xun21_kin_valid(a,chapters[d['chapter_id']],root)
                    check(xun21_valid,'本傳親屬原字及其方向須相符')
                sih21_valid=False
                if 'liang021_wangjiansihui_reading' in qualifiers:
                    try: from scripts.liang021_wangjiansihui import kin_valid as sih21_kin_valid
                    except ImportError: from liang021_wangjiansihui import kin_valid as sih21_kin_valid
                    sih21_valid=sih21_kin_valid(a,chapters[d['chapter_id']],root)
                    check(sih21_valid,'本傳親屬原字及其方向須相符')
                chun52_valid=False
                if 'song052_xiechun_reading' in qualifiers:
                    try: from scripts.song052_xiechun import kin_valid as chun52_kin_valid
                    except ImportError: from song052_xiechun import kin_valid as chun52_kin_valid
                    chun52_valid=chun52_kin_valid(a,chapters[d['chapter_id']],root)
                    check(chun52_valid,'本傳親屬原字及其方向須相符')
                xiejingren52_valid=False
                if 'song052_xiejingren_reading' in qualifiers:
                    try: from scripts.song052_xiejingren import kin_valid as xiejingren52_kin_valid
                    except ImportError: from song052_xiejingren import kin_valid as xiejingren52_kin_valid
                    xiejingren52_valid=xiejingren52_kin_valid(a,chapters[d['chapter_id']],root)
                    check(xiejingren52_valid,'本傳親屬原字及其方向須相符')
                nan23dan_valid=False
                if 'nan023_digital_reading' in qualifiers:
                    try: from scripts.nan023_digital import kin_valid as nan23dan_kin_valid
                    except ImportError: from nan023_digital import kin_valid as nan23dan_kin_valid
                    nan23dan_valid=nan23dan_kin_valid(a,chapters[d['chapter_id']],root)
                    check(nan23dan_valid,'本傳親屬原字及其方向須相符')
                wangdan52_valid=False
                if 'song052_wangdan_reading' in qualifiers:
                    try: from scripts.song052_wangdan import kin_valid as wangdan52_kin_valid
                    except ImportError: from song052_wangdan import kin_valid as wangdan52_kin_valid
                    wangdan52_valid=wangdan52_kin_valid(a,chapters[d['chapter_id']],root)
                    check(wangdan52_valid,'本傳親屬原字及其方向須相符')
                xieshu52_valid=False
                if 'song052_xieshu_reading' in qualifiers:
                    try: from scripts.song052_xieshu import kin_valid as xieshu52_kin_valid
                    except ImportError: from song052_xieshu import kin_valid as xieshu52_kin_valid
                    xieshu52_valid=xieshu52_kin_valid(a,chapters[d['chapter_id']],root)
                    check(xieshu52_valid,'本傳親屬原字及其方向須相符')
                nan23p_valid=False
                if 'nan023_print_reading' in qualifiers:
                    try: from scripts.nan023_print import kin_valid as nan23p_kin_valid
                    except ImportError: from nan023_print import kin_valid as nan23p_kin_valid
                    nan23p_valid=nan23p_kin_valid(a,chapters[d['chapter_id']],root)
                    check(nan23p_valid,'本傳親屬原字及其方向須相符')
                nan23mao_valid=False
                if 'nan023_wangmao_reading' in qualifiers:
                    try: from scripts.nan023_wangmao import kin_valid as nan23mao_kin_valid
                    except ImportError: from nan023_wangmao import kin_valid as nan23mao_kin_valid
                    nan23mao_valid=nan23mao_kin_valid(a,chapters[d['chapter_id']],root)
                    check(nan23mao_valid,'本傳親屬原字及其方向須相符')
                nan23jiang_valid=False
                if 'nan023_jiangxiao_reading' in qualifiers:
                    try: from scripts.nan023_jiangxiao import kin_valid as nan23jiang_kin_valid
                    except ImportError: from nan023_jiangxiao import kin_valid as nan23jiang_kin_valid
                    nan23jiang_valid=nan23jiang_kin_valid(a,chapters[d['chapter_id']],root)
                    check(nan23jiang_valid,'本傳親屬原字及其方向須相符')
                nan23chuai_valid=False
                if 'nan023_chuai_reading' in qualifiers:
                    try: from scripts.nan023_chuai import kin_valid as nan23chuai_kin_valid
                    except ImportError: from nan023_chuai import kin_valid as nan23chuai_kin_valid
                    nan23chuai_valid=nan23chuai_kin_valid(a,chapters[d['chapter_id']],root)
                    check(nan23chuai_valid,'本傳親屬原字及其方向須相符')
                nan23heyu_valid=False
                if 'nan023_heyu_reading' in qualifiers:
                    try: from scripts.nan023_heyu import kin_valid as nan23heyu_kin_valid
                    except ImportError: from nan023_heyu import kin_valid as nan23heyu_kin_valid
                    nan23heyu_valid=nan23heyu_kin_valid(a,chapters[d['chapter_id']],root)
                    check(nan23heyu_valid,'本傳親屬原字及其方向須相符')
                nan23zao_valid=False
                if 'nan023_wangzao_reading' in qualifiers:
                    try: from scripts.nan023_wangzao import kin_valid as nan23zao_kin_valid
                    except ImportError: from nan023_wangzao import kin_valid as nan23zao_kin_valid
                    nan23zao_valid=nan23zao_kin_valid(a,chapters[d['chapter_id']],root)
                    check(nan23zao_valid,'本傳親屬原字及其方向須相符')
                nan23liang_valid=False
                if 'nan023_wangliang_reading' in qualifiers:
                    try: from scripts.nan023_wangliang import kin_valid as nan23liang_kin_valid
                    except ImportError: from nan023_wangliang import kin_valid as nan23liang_kin_valid
                    nan23liang_valid=nan23liang_kin_valid(a,chapters[d['chapter_id']],root)
                    check(nan23liang_valid,'本傳親屬原字及其方向須相符')
                nan23ying_valid=False
                if 'nan023_wangying_reading' in qualifiers:
                    try: from scripts.nan023_wangying import kin_valid as nan23ying_kin_valid
                    except ImportError: from nan023_wangying import kin_valid as nan23ying_kin_valid
                    nan23ying_valid=nan23ying_kin_valid(a,chapters[d['chapter_id']],root)
                    check(nan23ying_valid,'本傳親屬原字及其方向須相符')
                nan23hui_valid=False
                if 'nan023_wanghui_reading' in qualifiers:
                    try: from scripts.nan023_wanghui import kin_valid as nan23hui_kin_valid
                    except ImportError: from nan023_wanghui import kin_valid as nan23hui_kin_valid
                    nan23hui_valid=nan23hui_kin_valid(a,chapters[d['chapter_id']],root)
                    check(nan23hui_valid,'本傳親屬原字及其方向須相符')
                nan23qiu_valid=False
                if 'nan023_wangqiu_reading' in qualifiers:
                    try: from scripts.nan023_wangqiu import kin_valid as nan23qiu_kin_valid
                    except ImportError: from nan023_wangqiu import kin_valid as nan23qiu_kin_valid
                    nan23qiu_valid=nan23qiu_kin_valid(a,chapters[d['chapter_id']],root)
                    check(nan23qiu_valid,'本傳親屬原字及其方向須相符')
                nan23xuan_valid=False
                if 'nan023_wangxuan_reading' in qualifiers:
                    try: from scripts.nan023_wangxuan import kin_valid as nan23xuan_kin_valid
                    except ImportError: from nan023_wangxuan import kin_valid as nan23xuan_kin_valid
                    nan23xuan_valid=nan23xuan_kin_valid(a,chapters[d['chapter_id']],root)
                    check(nan23xuan_valid,'本傳親屬原字及其方向須相符')
                nan23huiz_valid=False
                if 'nan023_wanghui_sons_reading' in qualifiers:
                    try: from scripts.nan023_wanghui_sons import kin_valid as nan23huiz_kin_valid
                    except ImportError: from nan023_wanghui_sons import kin_valid as nan23huiz_kin_valid
                    nan23huiz_valid=nan23huiz_kin_valid(a,chapters[d['chapter_id']],root)
                    check(nan23huiz_valid,'本傳親屬原字及其方向須相符')
                nan23chu_valid=False
                if 'nan023_chuzhanzhi_reading' in qualifiers:
                    try: from scripts.nan023_chuzhanzhi import kin_valid as nan23chu_kin_valid
                    except ImportError: from nan023_chuzhanzhi import kin_valid as nan23chu_kin_valid
                    nan23chu_valid=nan23chu_kin_valid(a,chapters[d['chapter_id']],root)
                    check(nan23chu_valid,'本傳親屬原字及其方向須相符')
                nan23yun_valid=False
                if 'nan023_wangyun_reading' in qualifiers:
                    try: from scripts.nan023_wangyun import kin_valid as nan23yun_kin_valid
                    except ImportError: from nan023_wangyun import kin_valid as nan23yun_kin_valid
                    nan23yun_valid=nan23yun_kin_valid(a,chapters[d['chapter_id']],root)
                    check(nan23yun_valid,'本傳親屬原字及其方向須相符')
                nan23huan_valid=False
                if 'nan023_wanghuan_reading' in qualifiers:
                    try: from scripts.nan023_wanghuan import kin_valid as nan23huan_kin_valid
                    except ImportError: from nan023_wanghuan import kin_valid as nan23huan_kin_valid
                    nan23huan_valid=nan23huan_kin_valid(a,chapters[d['chapter_id']],root)
                    check(nan23huan_valid,'本傳親屬原字及其方向須相符')
                nan23xi_valid=False
                if 'nan023_wangxi_reading' in qualifiers:
                    try: from scripts.nan023_wangxi import kin_valid as nan23xi_kin_valid
                    except ImportError: from nan023_wangxi import kin_valid as nan23xi_kin_valid
                    nan23xi_valid=nan23xi_kin_valid(a,chapters[d['chapter_id']],root)
                    check(nan23xi_valid,'本傳親屬原字及其方向須相符')
                nan23fen_valid=False
                if 'nan023_wangfen_reading' in qualifiers:
                    try: from scripts.nan023_wangfen import kin_valid as nan23fen_kin_valid
                    except ImportError: from nan023_wangfen import kin_valid as nan23fen_kin_valid
                    nan23fen_valid=nan23fen_kin_valid(a,chapters[d['chapter_id']],root)
                    check(nan23fen_valid,'本傳親屬原字及其方向須相符')
                nan23tong_valid=False
                if 'nan023_wangtong_reading' in qualifiers:
                    try: from scripts.nan023_wangtong import kin_valid as nan23tong_kin_valid
                    except ImportError: from nan023_wangtong import kin_valid as nan23tong_kin_valid
                    nan23tong_valid=nan23tong_kin_valid(a,chapters[d['chapter_id']],root)
                    check(nan23tong_valid,'本傳親屬原字及其方向須相符')
                nan23mai_valid=False
                if 'nan023_wangmai_reading' in qualifiers:
                    try: from scripts.nan023_wangmai import kin_valid as nan23mai_kin_valid
                    except ImportError: from nan023_wangmai import kin_valid as nan23mai_kin_valid
                    nan23mai_valid=nan23mai_kin_valid(a,chapters[d['chapter_id']],root)
                    check(nan23mai_valid,'本傳親屬原字及其方向須相符')
                nan23zhi_valid=False
                if 'nan023_wangzhi_reading' in qualifiers:
                    try: from scripts.nan023_wangzhi import kin_valid as nan23zhi_kin_valid
                    except ImportError: from nan023_wangzhi import kin_valid as nan23zhi_kin_valid
                    nan23zhi_valid=nan23zhi_kin_valid(a,chapters[d['chapter_id']],root)
                    check(nan23zhi_valid,'本傳親屬原字及其方向須相符')
                nan23gu_valid=False
                if 'nan023_wanggu_reading' in qualifiers:
                    try: from scripts.nan023_wanggu import kin_valid as nan23gu_kin_valid
                    except ImportError: from nan023_wanggu import kin_valid as nan23gu_kin_valid
                    nan23gu_valid=nan23gu_kin_valid(a,chapters[d['chapter_id']],root)
                    check(nan23gu_valid,'本傳親屬原字及其方向須相符')
                nan23hou_valid=False
                if 'nan023_wanghou_reading' in qualifiers:
                    try: from scripts.nan023_wanghou import kin_valid as nan23hou_kin_valid
                    except ImportError: from nan023_wanghou import kin_valid as nan23hou_kin_valid
                    nan23hou_valid=nan23hou_kin_valid(a,chapters[d['chapter_id']],root)
                    check(nan23hou_valid,'本傳親屬原字及其方向須相符')
                nan23yu_valid=False
                if 'nan023_wangyu_reading' in qualifiers:
                    try: from scripts.nan023_wangyu import kin_valid as nan23yu_kin_valid
                    except ImportError: from nan023_wangyu import kin_valid as nan23yu_kin_valid
                    nan23yu_valid=nan23yu_kin_valid(a,chapters[d['chapter_id']],root)
                    check(nan23yu_valid,'本傳親屬原字及其方向須相符')
                qi47rong_valid=False
                if 'nanqi047_wangrong_reading' in qualifiers:
                    try: from scripts.nanqi047_wangrong import kin_valid as qi47rong_kin_valid
                    except ImportError: from nanqi047_wangrong import kin_valid as qi47rong_kin_valid
                    qi47rong_valid=qi47rong_kin_valid(a,chapters[d['chapter_id']],root)
                    check(qi47rong_valid,'本傳親屬原字及其方向須相符')
                liang33sr_valid=False
                if 'liang033_wangsengru_reading' in qualifiers:
                    try: from scripts.liang033_wangsengru import kin_valid as liang33sr_kin_valid
                    except ImportError: from liang033_wangsengru import kin_valid as liang33sr_kin_valid
                    liang33sr_valid=liang33sr_kin_valid(a,chapters[d['chapter_id']],root)
                    check(liang33sr_valid,'本傳親屬原字及其方向須相符')
                nan59sr_valid=False
                if 'nanshi059_wangsengru_reading' in qualifiers:
                    try: from scripts.nanshi059_wangsengru import kin_valid as nan59sr_kin_valid
                    except ImportError: from nanshi059_wangsengru import kin_valid as nan59sr_kin_valid
                    nan59sr_valid=nan59sr_kin_valid(a,chapters[d['chapter_id']],root)
                    check(nan59sr_valid,'本傳親屬原字及其方向須相符')
                q47wyd_valid=False
                if 'nanqi047_wangrong_wyd_reading' in qualifiers:
                    try: from scripts.nanqi047_wangrong_wyd import kin_valid as q47wyd_kin
                    except ImportError: from nanqi047_wangrong_wyd import kin_valid as q47wyd_kin
                    q47wyd_valid=q47wyd_kin(a,chapters[d['chapter_id']],root)
                    check(q47wyd_valid,'王融殿本親屬原證及其方向不符')
                qi47wife_ok=False
                if 'nanqi047_xietiao_wife' in qualifiers:
                    try: from scripts.nanqi047_xietiao_wife import valid as qi47wife_valid
                    except ImportError: from nanqi047_xietiao_wife import valid as qi47wife_valid
                    qi47wife_ok=qi47wife_valid(a,chapters[d['chapter_id']],root)
                    check(qi47wife_ok,'王敬則女原證及父夫方向不合')
                nan24sz_valid=False
                if 'nanshi024_wangshaozhi_reading' in qualifiers:
                    try: from scripts.nanshi024_wangshaozhi import kin_valid as nan24sz_kin_valid
                    except ImportError: from nanshi024_wangshaozhi import kin_valid as nan24sz_kin_valid
                    nan24sz_valid=nan24sz_kin_valid(a,chapters[d['chapter_id']],root)
                    check(nan24sz_valid,'本傳親屬原字及其方向須相符')
                n24szwyd_valid=False
                if 'nanshi024_wangshaozhi_wyd_reading' in qualifiers:
                    try: from scripts.nanshi024_wangshaozhi_wyd import kin_valid as n24szwyd_kin
                    except ImportError: from nanshi024_wangshaozhi_wyd import kin_valid as n24szwyd_kin
                    n24szwyd_valid=n24szwyd_kin(a,chapters[d['chapter_id']],root)
                    check(n24szwyd_valid,'王韶之殿本親屬原證及其方向不符')
                nan24yz_valid=False
                if 'nanshi024_wangyuezhi_reading' in qualifiers:
                    try: from scripts.nanshi024_wangyuezhi import kin_valid as nan24yz_kin_valid
                    except ImportError: from nanshi024_wangyuezhi import kin_valid as nan24yz_kin_valid
                    nan24yz_valid=nan24yz_kin_valid(a,chapters[d['chapter_id']],root)
                    check(nan24yz_valid,'本傳親屬原字及其方向須相符')
                nan24zz_valid=False
                if 'nanshi024_wangzhunzhi_reading' in qualifiers:
                    try: from scripts.nanshi024_wangzhunzhi import kin_valid as nan24zz_kin_valid
                    except ImportError: from nanshi024_wangzhunzhi import kin_valid as nan24zz_kin_valid
                    nan24zz_valid=nan24zz_kin_valid(a,chapters[d['chapter_id']],root)
                    check(nan24zz_valid,'本傳親屬原字及其方向須相符')
                nan24jz_valid=False
                if 'nanshi024_wangjinzhi_reading' in qualifiers:
                    try: from scripts.nanshi024_wangjinzhi import kin_valid as nan24jz_kin_valid
                    except ImportError: from nanshi024_wangjinzhi import kin_valid as nan24jz_kin_valid
                    nan24jz_valid=nan24jz_kin_valid(a,chapters[d['chapter_id']],root)
                    check(nan24jz_valid,'本傳親屬原字及其方向須相符')
                nan24qing_valid=False
                if 'nanshi024_wangqing_reading' in qualifiers:
                    try: from scripts.nanshi024_wangqing import kin_valid as nan24qing_kin_valid
                    except ImportError: from nanshi024_wangqing import kin_valid as nan24qing_kin_valid
                    nan24qing_valid=nan24qing_kin_valid(a,chapters[d['chapter_id']],root)
                    check(nan24qing_valid,'本傳親屬原字及其方向須相符')
                nan24qun_valid=False
                if 'nanshi024_wangqunzhi_reading' in qualifiers:
                    try: from scripts.nanshi024_wangqunzhi import kin_valid as nan24qun_kin_valid
                    except ImportError: from nanshi024_wangqunzhi import kin_valid as nan24qun_kin_valid
                    nan24qun_valid=nan24qun_kin_valid(a,chapters[d['chapter_id']],root)
                    check(nan24qun_valid,'本傳親屬原字及其方向須相符')
                nan24su_valid=False
                if 'nanshi024_wangsu_reading' in qualifiers:
                    try: from scripts.nanshi024_wangsu import kin_valid as nan24su_kin_valid
                    except ImportError: from nanshi024_wangsu import kin_valid as nan24su_kin_valid
                    nan24su_valid=nan24su_kin_valid(a,chapters[d['chapter_id']],root)
                    check(nan24su_valid,'本傳親屬原字及其方向須相符')
                nan24rw_valid=False
                if 'nanshi024_ruanwanling_reading' in qualifiers:
                    try: from scripts.nanshi024_ruanwanling import kin_valid as nan24rw_kin_valid
                    except ImportError: from nanshi024_ruanwanling import kin_valid as nan24rw_kin_valid
                    nan24rw_valid=nan24rw_kin_valid(a,chapters[d['chapter_id']],root)
                    check(nan24rw_valid,'本傳親屬原字及其方向須相符')
                n24hong_valid=False
                if 'nanshi024_wanghongzhi_reading' in qualifiers:
                    try: from scripts.nanshi024_wanghongzhi import kin_valid as nan24hong_kin
                    except ImportError: from nanshi024_wanghongzhi import kin_valid as nan24hong_kin
                    n24hong_valid=nan24hong_kin(a,chapters[d['chapter_id']],root)
                    check(n24hong_valid,'南史王弘之撫育與諸親須有原文角色與字位')
                hongzhi_valid=False
                if 'song093_hongzhi_reading' in qualifiers:
                    try: from scripts.song093_wanghongzhi import kin_valid as hongzhi_kin_valid
                    except ImportError: from song093_wanghongzhi import kin_valid as hongzhi_kin_valid
                    hongzhi_valid=hongzhi_kin_valid(a,chapters[d['chapter_id']],root)
                    check(hongzhi_valid,'宋書王弘之親屬須繫傳主與各別原詞')
                s93wyd_valid=False
                if 'song093_wyd_reading' in qualifiers:
                    try: from scripts.song093_wyd import kin_valid as s93wyd_kin
                    except ImportError: from song093_wyd import kin_valid as s93wyd_kin
                    s93wyd_valid=s93wyd_kin(a,chapters[d['chapter_id']],root)
                    check(s93wyd_valid,'殿本王弘之、阮萬齡家世原詞不符')
                nan24meng_valid=False
                if 'nanshi024_wangmeng_reading' in qualifiers:
                    try: from scripts.nanshi024_wangmeng import kin_valid as nan24meng_kin_valid
                    except ImportError: from nanshi024_wangmeng import kin_valid as nan24meng_kin_valid
                    nan24meng_valid=nan24meng_kin_valid(a,chapters[d['chapter_id']],root)
                    check(nan24meng_valid,'本傳親屬原字及其方向須相符')
                xm9_valid=False
                if 'xiangshan_m9_epitaphs_reading' in qualifiers:
                    try: from scripts.xiangshan_m9_epitaphs import kin_valid as xm9_kin_valid
                    except ImportError: from xiangshan_m9_epitaphs import kin_valid as xm9_kin_valid
                    xm9_valid=xm9_kin_valid(a,chapters[d['chapter_id']],root)
                    check(xm9_valid,'本傳親屬原字及其方向須相符')
                nan24yan_valid=False
                if 'nanshi024_wangyan_reading' in qualifiers:
                    try: from scripts.nanshi024_wangyan import kin_valid as nan24yan_kin_valid
                    except ImportError: from nanshi024_wangyan import kin_valid as nan24yan_kin_valid
                    nan24yan_valid=nan24yan_kin_valid(a,chapters[d['chapter_id']],root)
                    check(nan24yan_valid,'本傳親屬原字及其方向須相符')
                nan24wab_valid=False
                if 'nanshi024_wangyan_brothers_reading' in qualifiers:
                    try: from scripts.nanshi024_wangyan_brothers import kin_valid as nan24wab_kin_valid
                    except ImportError: from nanshi024_wangyan_brothers import kin_valid as nan24wab_kin_valid
                    nan24wab_valid=nan24wab_kin_valid(a,chapters[d['chapter_id']],root)
                    check(nan24wab_valid,'本傳親屬原字及其方向須相符')
                nan24gh_valid=False
                if 'nanshi024_guhaozhi_reading' in qualifiers:
                    try: from scripts.nanshi024_guhaozhi import kin_valid as nan24gh_kin_valid
                    except ImportError: from nanshi024_guhaozhi import kin_valid as nan24gh_kin_valid
                    nan24gh_valid=nan24gh_kin_valid(a,chapters[d['chapter_id']],root)
                    check(nan24gh_valid,'本傳親屬原字及其方向須相符')
                nan24siy_valid=False
                if 'nanshi024_wangsiyuan_reading' in qualifiers:
                    try: from scripts.nanshi024_wangsiyuan import kin_valid as nan24siy_kin_valid
                    except ImportError: from nanshi024_wangsiyuan import kin_valid as nan24siy_kin_valid
                    nan24siy_valid=nan24siy_kin_valid(a,chapters[d['chapter_id']],root)
                    check(nan24siy_valid,'本傳親屬原字及其方向須相符')
                qi23_valid = False
                if 'qi23_kin_frame' in qualifiers:
                    try: from scripts.qi023_wangjian_witnesses import kin_valid as qi23_kin_valid
                    except ImportError: from qi023_wangjian_witnesses import kin_valid as qi23_kin_valid
                    qi23_valid = qi23_kin_valid(a,chapters[d['chapter_id']],root)
                    check(qi23_valid, '王儉傳、親屬傳首與帝女表須合具名或稱號的原字與方向')
                if qualifiers.get('source_clause_binding', {}).get('kind') == 'biography_family_clause':
                    try:
                        from scripts.biography_family_clause import valid as biography_family_clause_valid
                    except ImportError:
                        from biography_family_clause import valid as biography_family_clause_valid
                    check(biography_family_clause_valid(a, paragraphs, d['assertions'], chapters), '傳記親屬句須有完整上下文、逐詞人物錨點及明確方向')
                j44_valid = False
                if qualifiers.get('source_clause_binding',{}).get('kind') == 'jin044_family':
                    try: from scripts.jin044_family_sources import valid as j44_family
                    except ImportError: from jin044_family_sources import valid as j44_family
                    j44_valid = len(a['evidence']) == 1 and j44_family(a, a['evidence'][0], chapters[d['chapter_id']], chapters, root)
                    check(j44_valid, '盧諶與崔悅的從母、姪稱須回讀該版本及劉琨妻兩端')
                if (a['predicate'] == 'maternal_aunt' and qualifiers.get('source_clause_binding',{}).get('kind') not in ('jin067_liukun_wife_wen_maternal_aunt','jin044_family')) or 'relative_age_interpretation' in qualifiers:
                    try:
                        from scripts.song047_collateral_care import valid, chronology_caution_valid
                    except ImportError:
                        from song047_collateral_care import valid, chronology_caution_valid
                    check(valid(a, paragraphs), '母系旁親／哺養須有固定原句與雙人物錨點，不得補父母或親等')
                    if 'relative_age_interpretation' in qualifiers:
                        check(chronology_caution_valid(a, root), '從母兄年代張力須綁既有407／41／363原證，不得默採長幼或推生日')
                if qualifiers.get('parentage_basis') == 'marital_biographical_birth_context':
                    try:
                        from scripts.song041_source_context import marital_birth_context_valid
                    except ImportError:
                        from song041_source_context import marital_birth_context_valid
                    check(marital_birth_context_valid(a, paragraphs, d['assertions']), '婚生父稱判讀須有同句婚配、明生母與兩個明名孩子，不得由配偶泛推父親')
                if 'dissolution_petition' in qualifiers:
                    try: from scripts.jin096_huifeng import petition_valid as huifeng_petition_valid
                    except ImportError: from jin096_huifeng import petition_valid as huifeng_petition_valid
                    check(huifeng_petition_valid(a,paragraphs),'惠風請絕婚須保留請者、歸家與未錄准狀')
                if 'marriage_termination' in qualifiers:
                    try:
                        from scripts.marriage_termination import marriage_termination_valid
                    except ImportError:
                        from marriage_termination import marriage_termination_valid
                    check((nan23zao_valid and qualifiers.get('nan023_wangzao_reading')=='yingyuan-zao') or marriage_termination_valid(a, paragraphs),
                          '離婚須保留同段婚配原句及具名夫妻錨點，不得刪婚配或虛填離婚日期')
                if 'resolved_subject_identity_decision_id' in qualifiers:
                    resolution = identity_decisions_by_id.get(qualifiers['resolved_subject_identity_decision_id'], {})
                    ancestor_ref = resolution.get('ancestor_reference', {})
                    valid = (a['predicate'] == 'grandfather' and qualifiers.get('lineage') == 'maternal'
                             and qualifiers.get('source_term') == '外孫'
                             and qualifiers.get('generation_difference') == -2
                             and 'mother_person_id' in qualifiers and qualifiers['mother_person_id'] is None
                             and resolution.get('person_id') == a['subject_person_id']
                             and bool(ancestor_ref) and len(a['evidence']) == 1)
                    for e in a['evidence']:
                        hit = paragraphs.get(e.get('paragraph_id'))
                        ms = {m['id']: m for m in hit[1]['mentions']} if hit else {}
                        obj = ms.get(e.get('object_person_mention_id'), {})
                        valid = (valid and e.get('paragraph_id') == ancestor_ref.get('paragraph_id')
                                 and e.get('subject_person_mention_id') == ancestor_ref.get('ancestor_mention_id')
                                 and obj.get('person_id') == a['object_person_id']
                                 and '曾祖是' + obj.get('surface', '') + '外孫' in e.get('quote', ''))
                    check(valid, '外孫主體指涉須連到已驗三代判讀，外祖錨點及未名母親分存')
                if qualifiers.get('relationship_basis') == 'named_wifes_father':
                    try:
                        from scripts.wife_father_clause import wife_father_clause_valid
                    except ImportError:
                        from wife_father_clause import wife_father_clause_valid
                    check(wife_father_clause_valid(a, paragraphs, chapters), '妻父從句須綁完整原句與父夫妻三角色，不得推生母或反轉端點')
                if a['predicate'] in ('raised_by', 'ritual_successor_of') or 'care_basis' in qualifiers or 'succession_kind' in qualifiers:
                    try:
                        from scripts.non_parental_family import non_parental_relation_valid
                    except ModuleNotFoundError:
                        from non_parental_family import non_parental_relation_valid
                    check(tai21_valid or pei_valid or n22jian_valid or qi23_valid or ((nan23qiu_valid and qualifiers.get('nan023_wangqiu_reading')=='huan-successor') or ((nan23huan_valid and qualifiers.get('nan023_wanghuan_reading')=='successor') or (n24hong_valid and qualifiers.get('nanshi024_wanghongzhi_reading')=='care') or (hongzhi_valid and qualifiers.get('song093_hongzhi_reading')=='care') or (s93wyd_valid and qualifiers.get('song093_wyd_reading')=='care') or non_parental_relation_valid(a, paragraphs, family_relations))), '撫養或宗祀承繼須有雙人錨點與原詞，不得推成生父母或法定收養')
                if a['predicate'] == 'agnatic_senior_kin':
                    check('kinship_structure' in qualifiers, '父系晚一代稱謂缺少世代結構')
                if a['predicate'] == 'maternal_cousin':
                    check('kinship_structure' in qualifiers, '母系姨表關係缺原路徑結構')
                if 'adopted_for_family_tree' in qualifiers:
                    if nan23chu_valid and qualifiers.get('nan023_chuzhanzhi_reading') in ('son','younger'):
                        check(qualifiers.get('adopted_for_family_tree') is False and a['predicate'] in ('father','brother'), '親稱不同的兩源陳述不得冒作唯一家系')
                    elif qualifiers.get('ancestry_precision') == 'reported_generation_formula':
                        try:
                            from scripts.unspecified_ancestry import reported_generation_formula_valid
                        except ImportError:
                            from unspecified_ancestry import reported_generation_formula_valid
                        check(reported_generation_formula_valid(a, paragraphs, source_age_number), '自某幾世生某須分存原數與未採遠系，不得補精確世距或接入家族')
                    elif qualifiers.get('ancestry_precision') == 'reported_self_genealogy':
                        try: from scripts.received_paternal_reports import reported_ancestry_valid
                        except ImportError: from received_paternal_reports import reported_ancestry_valid
                        check(reported_ancestry_valid(a, paragraphs, source_age_number), '自敍世祖須綁傳主、祖名、原數與自敍引句，不補確定世距')
                    elif qualifiers.get('ancestry_precision') == 'unspecified_descent':
                        try:
                            from scripts.unspecified_ancestry import unspecified_ancestry_valid
                        except ImportError:
                            from unspecified_ancestry import unspecified_ancestry_valid
                        check(unspecified_ancestry_valid(a, paragraphs), '未定世數之後主張須保留未知數值及具名祖先錨點，不得納入家族樹')
                    else:
                        number = qualifiers.get('source_number')
                        check(qualifiers.get('adopted_for_family_tree') is False and a['predicate'] == 'ancestor'
                              and qualifiers.get('generation_distance') is None
                              and type(qualifiers.get('reported_generation_number')) is int
                              and source_age_number(number) == qualifiers['reported_generation_number']
                              and isinstance(number, str) and number + '世孫' in qualifiers.get('source_term', '')
                              and any(qualifiers.get('source_term', '') in e.get('quote', '') for e in a['evidence']),
                              '未採遠祖說須保留原世孫數，不得補成已採納的精確父系距離')
                if a['predicate'] == 'teacher' or qualifiers.get('relationship_basis') == 'teaching':
                    term = qualifiers.get('source_term')
                    valid = (a['predicate'] == 'teacher' and qualifiers.get('relationship_basis') == 'teaching'
                             and isinstance(term, str) and bool(term)
                             and any(marker in term for marker in ('學', '教', '受', '傳', '弟子', '師')))
                    for e in a['evidence']:
                        hit = paragraphs.get(e.get('paragraph_id'))
                        if not hit:
                            valid = False
                            continue
                        quote = e.get('quote', '')
                        starts = [i for i in range(len(hit[1]['text']) + 1) if quote and hit[1]['text'].startswith(quote, i)]
                        valid = valid and isinstance(term, str) and term in quote
                        for role, endpoint in (('subject', 'subject_person_id'), ('object', 'object_person_id')):
                            anchors = [m for m in hit[1]['mentions'] if m['id'] == e.get(role + '_person_mention_id')]
                            valid = valid and len(anchors) == 1 and anchors[0].get('person_id') == a[endpoint] and any(
                                i <= anchors[0]['start'] and anchors[0]['end'] <= i + len(quote) for i in starts)
                    if 'teaching_clause_binding' in qualifiers:
                        try:
                            from scripts.contextual_relations import teaching_clause_valid
                        except ImportError:
                            from contextual_relations import teaching_clause_valid
                        valid = teaching_clause_valid(a, paragraphs)
                    check(valid, '師承須有學教原詞及同引句學生老師雙錨點，不得改作親屬')
                if 'succession' in qualifiers:
                    try:
                        from scripts.title_successions import succession_valid
                    except ModuleNotFoundError:
                        from title_successions import succession_valid
                    check(succession_valid(a, title_records, paragraphs),
                          '嗣位原詞須有父子、前任爵位及同段人物錨點，不得虛構爵名或起訖')
                if a['predicate'] == 'paternal_uncle':
                    try:
                        from scripts.directed_uncle_roles import paternal_uncle_direction_valid
                    except ImportError:
                        from directed_uncle_roles import paternal_uncle_direction_valid
                    try:
                        from scripts.wyd_song044_nephew import nephew_valid as wyd_nephew_valid
                    except ImportError:
                        from wyd_song044_nephew import nephew_valid as wyd_nephew_valid
                    try: from scripts.nanshi022_wanggui_kin import valid as gui_kin_valid
                    except ImportError: from nanshi022_wanggui_kin import valid as gui_kin_valid
                    check(tai21_valid or n22jian_valid or qi23_valid or (nan23hui_valid and qualifiers.get('nan023_wanghui_reading')=='uncle-mi') or (nan23qiu_valid and qualifiers.get('nan023_wangqiu_reading')=='lu-uncle') or (nan23yun_valid and qualifiers.get('nan023_wangyun_reading') in ('yun-uncle','early-uncle')) or (nan23huan_valid and qualifiers.get('nan023_wanghuan_reading') in ('uncle','uncle-again')) or (nan23yu_valid and qualifiers.get('nan023_wangyu_reading') in ('zhi-uncle',)) or (nan24siy_valid and qualifiers.get('nanshi024_wangsiyuan_reading')=='zhaolue-uncle') or paternal_uncle_direction_valid(a, paragraphs) or wyd_nephew_valid(a, paragraphs, root)
                          or (qualifiers.get('reading_basis', {}).get('kind') == 'nanshi022_wanggui_opening_kin' and all(gui_kin_valid(a, e, chapters, root) for e in a['evidence'])),
                          '叔父關係須依原詞與人物字位定向，不得互換叔侄端點')
                if a['predicate'] == 'maternal_uncle':
                    try:
                        from scripts.uncle_parentage import explicit_maternal_uncle_valid
                    except ImportError:
                        from uncle_parentage import explicit_maternal_uncle_valid
                    try: from scripts.nanshi022_wangtai_nephew import valid as wangtai_nephew_valid
                    except ImportError: from nanshi022_wangtai_nephew import valid as wangtai_nephew_valid
                    check(pei_valid or (qualifiers.get('source_term') == '姊子'
                          and qualifiers.get('generation_difference') == -1
                          and qualifiers.get('lineage') == 'maternal'
                          and qualifiers.get('mother_person_id') is None
                          and any('姊子' in e.get('quote', '') for e in a['evidence']))
                          or (nan23xuan_valid and qualifiers.get('nan023_wangxuan_reading')=='yan-uncle') or (nan23zhi_valid and qualifiers.get('nan023_wangzhi_reading')=='nephew') or (nan23gu_valid and qualifiers.get('nan023_wanggu_reading')=='nephew') or explicit_maternal_uncle_valid(a, paragraphs) or wangtai_nephew_valid(a, chapters, root),
                          '甥舅關係須有姊子原詞、舅某或相鄰具名某之外甥錨點，保留母系世代與未名母親')
                if a['predicate'] == 'grandmother':
                    try:
                        from scripts.reported_grandmother import reported_grandmother_valid
                    except ImportError:
                        from reported_grandmother import reported_grandmother_valid
                    explicit_grandmother = reported_grandmother_valid(a, paragraphs)
                    check(explicit_grandmother or (qualifiers.get('source_term') == '外孫'
                          and qualifiers.get('generation_difference') == -2
                          and qualifiers.get('lineage') == 'maternal'
                          and qualifiers.get('mother_person_id') is None
                          and any('外孫' in e.get('quote', '') for e in a['evidence'])),
                          '外孫祖母關係須保留母系兩代與原句未名母親')
                if a['predicate'] == 'grandfathers_brother' or qualifiers.get('source_term') == '兄孫':
                    try: from scripts.received_grandfathers_brother import valid as granduncle_valid
                    except ImportError: from received_grandfathers_brother import valid as granduncle_valid
                    check(granduncle_valid(a, paragraphs, mentions), '兄孫須核兩具名端及原句次序，祖父與父未具名')
                if a['predicate'] == 'kinship_generation' or qualifiers.get('source_term') == '大父行':
                    check(a['predicate'] == 'kinship_generation'
                          and qualifiers.get('source_term') == '大父行'
                          and qualifiers.get('generation_difference') == -2
                          and qualifiers.get('lineage') == 'unspecified'
                          and qualifiers.get('direct_ancestor') is None
                          and qualifiers.get('exact_distance') is None
                          and any('大父行' in e.get('quote', '') for e in a['evidence']),
                          '大父行只記祖父輩，不得補直系祖父或親等')
                if a['predicate'] == 'adoptive_father':
                    try:
                        from scripts.chuji_parentage import chuji_parentage_valid
                    except ImportError:
                        from chuji_parentage import chuji_parentage_valid
                    check((nan23yu_valid and qualifiers.get('nan023_wangyu_reading')=='adoption') or (nan23zhi_valid and qualifiers.get('nan023_wangzhi_reading')=='zhou-adoption') or chuji_parentage_valid(a, paragraphs, d['assertions']),
                          '嗣父須符合具名出繼或無子為嗣的限定來源模型，保留生父及完整連續原文，不得僅據嗣爵')
                if a['predicate'] == 'maternal_role':
                    try:
                        from scripts.maternal_roles import maternal_role_valid
                    except ImportError:
                        from maternal_roles import maternal_role_valid
                    check(pei_valid or n22jian_valid or qi23_valid or (nan24meng_valid and qualifiers.get('nanshi024_wangmeng_reading') == 'mother') or maternal_role_valid(a, paragraphs), '母親稱謂須有原詞及雙人物錨點，不得推生母或父親')
                if a['predicate'] == 'adoptive_mother':
                    check('所母' in qualifiers.get('source_term', '') and any(qualifiers.get('source_term', '') in e.get('quote', '') for e in a['evidence']), '所母關係須保存原詞，不得由一般母稱推定')
                if a['predicate'] == 'stepmother':
                    check(qualifiers.get('source_term') in ('後母', '繼母') and any(qualifiers.get('source_term') in e.get('quote', '') for e in a['evidence']), '繼母或後母關係須有相符原詞證據')
                if 'posthumous_birth' in qualifiers:
                    check(a['predicate'] == 'father' and qualifiers['posthumous_birth'] is True
                          and '遺腹' in qualifiers.get('source_term', ''), '遺腹子欄位須有父親與原詞證據')
                if 'shared_mother' in qualifiers:
                    terms = ('異母',) if qualifiers['shared_mother'] is False else ('同母', '母弟', '母兄')
                    if nan24meng_valid and qualifiers.get('nanshi024_wangmeng_reading') == 'deng-yong' and qualifiers['shared_mother'] is True:
                        terms = (*terms, '同產弟')
                    check(a['predicate'] in ('brother', 'sister') and type(qualifiers['shared_mother']) is bool
                          and any(term in qualifiers.get('source_term', '')
                                  and any(term in e.get('quote', '') for e in a['evidence']) for term in terms),
                          '同母或異母關係須有相符原詞與布林值，不補母親端點')
                if qualifiers.get('shared_father') is not None:
                    terms = ('異父',) if qualifiers['shared_father'] is False else ('同父',)
                    check(a['predicate'] in ('brother', 'sister') and type(qualifiers['shared_father']) is bool
                          and any(term in qualifiers.get('source_term', '')
                                  and any(term in e.get('quote', '') for e in a['evidence']) for term in terms),
                          '同父或異父關係須有相符原詞與布林值，不補父親端點')
                if a['predicate'] == 'kinship_unspecified' and qualifiers.get('kinship_basis') == 'jin044_named_sheng':
                    try: from scripts.jin044_named_sheng import valid as sheng44_valid
                    except ImportError: from jin044_named_sheng import valid as sheng44_valid
                    check(sheng44_valid(a, paragraphs), '石鑒傳駿甥須以本句劭、駿的字位定向')
                elif a['predicate'] == 'kinship_unspecified' and not j44_valid:
                    if qualifiers.get('kinship_basis') == 'song52_sheng_of_named_person':
                        check(wangdan52_valid,'宋書桓脩、王誕的甥稱須留具名雙端及未詳中介，不補世系')
                    elif qualifiers.get('kinship_basis')=='nan23_print_named_sheng':
                        check(nan23p_valid,'殿本桓修與王誕甥稱限所見雙端')
                    elif qualifiers.get('kinship_basis') == 'explicit_clan_member':
                        check(qualifiers.get('source_clause_binding', {}).get('kind') == 'biography_family_clause' and biography_family_clause_valid(a, paragraphs, d['assertions'], chapters), '族人不補世代、親等或共祖')
                    elif qualifiers.get('kinship_basis') == 'jin096_shi_yu_sunquan':
                        try: from scripts.jin076_sun_clan import valid as sun_quan_clan_valid
                        except ImportError: from jin076_sun_clan import valid as sun_quan_clan_valid
                        check(sun_quan_clan_valid(a, paragraphs), '虞潭母為孫權族孫女，須核人名原字與未名中介')
                    elif qualifiers.get('kinship_basis') == 'congzhongbiao_named_pair':
                        try:
                            from scripts.congzhongbiao import valid as congzhongbiao_valid
                        except ImportError:
                            from congzhongbiao import valid as congzhongbiao_valid
                        check(congzhongbiao_valid(a, paragraphs, chapters, root), '從中表須有具名雙端與固定原文，不得補親等世代或父系路徑')
                    elif qualifiers.get('kinship_basis') == 'address_to_named_sheng':
                        try:
                            from scripts.contextual_relations import addressed_sheng_valid
                        except ImportError:
                            from contextual_relations import addressed_sheng_valid
                        check(addressed_sheng_valid(a, paragraphs), '其甥稱屬須綁定顧告者與受話者，不補母親長幼及具體親等')
                    elif qualifiers.get('kinship_basis') == 'explicit_weiqin_pair':
                        try:
                            from scripts.contextual_relations import weiqin_pair_valid
                        except ImportError:
                            from contextual_relations import weiqin_pair_valid
                        check(weiqin_pair_valid(a, paragraphs), '為親須保存原詞雙端、完整引文及未知親等，不得接成父系')
                    elif qualifiers.get('kinship_basis') == 'stepfamily_grandparent_appellation':
                        try:
                            from scripts.song041_source_context import kin_clause_valid
                        except ImportError:
                            from song041_source_context import kin_clause_valid
                        check(kin_clause_valid(a, paragraphs, d['assertions']), '繼室母家外祖稱須有婚配與明父原證，不得作生系')
                    elif qualifiers.get('kinship_basis') == 'external_clan_affiliation':
                        check('外族' in qualifiers.get('source_term', '')
                              and qualifiers.get('lineage') == 'unspecified'
                              and all(key in qualifiers and qualifiers[key] is None for key in
                                      ('generation_difference', 'exact_distance', 'connecting_person_ids'))
                              and not qualifiers.get('kinship_structure')
                              and any(qualifiers.get('source_term', '') in e.get('quote', '') for e in a['evidence']),
                              '外族關係須保留原詞及未知世代、親等與連接人物')
                    else:
                        check(qualifiers.get('source_term') == '有親' and not qualifiers.get('kinship_structure')
                              and any('有親' in e.get('quote', '') for e in a['evidence']),
                              '未定親屬不得補具體親等')
                if a['predicate'] == 'affinity_unspecified':
                    check(qualifiers.get('relationship_basis') == 'marriage_affinity'
                          and qualifiers.get('source_term') and '婚' in qualifiers['source_term']
                          and all(key in qualifiers and qualifiers[key] is None for key in
                                  ('spouse_person_ids', 'connecting_person_ids', 'generation_difference'))
                          and any(qualifiers.get('source_term', '') in e.get('quote', '') for e in a['evidence']),
                          '未明姻親須保存婚原詞，不得補配偶、連接人物或世代')
                if 'kinship_structure' in qualifiers:
                    structure = qualifiers['kinship_structure']
                    if a['predicate'] == 'agnatic_senior_kin':
                        try:
                            from scripts.collateral_kinship import agnatic_senior_kin_valid
                        except ImportError:
                            from collateral_kinship import agnatic_senior_kin_valid
                        check((xiejingren52_valid and qualifiers.get('song052_xiejingren_reading')=='hui-elder') or (wangdan52_valid and qualifiers.get('song052_wangdan_reading')=='xun-collateral') or (nan23p_valid and qualifiers.get('nan023_print_reading')=='xun') or (nan23yu_valid and qualifiers.get('nan023_wangyu_reading') in ('congzi','congshu')) or (qi47rong_valid and qualifiers.get('nanqi047_wangrong_reading')=='congshu') or (q47wyd_valid and a.get('id')=='a-nanqi047-wangrong-wyd-congshu') or (nan24sz_valid and qualifiers.get('nanshi024_wangshaozhi_reading') == 'congsun') or (n24szwyd_valid and a.get('id')=='a-nanshi024-wangshaozhi-wyd-congsun') or (nan24su_valid and qualifiers.get('nanshi024_wangsu_reading')=='clan-nephew') or (n24hong_valid and qualifiers.get('nanshi024_wanghongzhi_reading')=='congshu') or (hongzhi_valid and qualifiers.get('song093_hongzhi_reading')=='congshu') or (s93wyd_valid and qualifiers.get('song093_wyd_reading')=='congshu') or agnatic_senior_kin_valid(a, paragraphs), '父系晚一代稱謂須有從子原詞與雙人物錨點，不得補父親、親等或年齡')
                    elif a['predicate'] == 'maternal_cousin':
                        try:
                            from scripts.maternal_cousins import maternal_cousin_valid
                        except ImportError:
                            from maternal_cousins import maternal_cousin_valid
                        check((nan23liang_valid and qualifiers.get('nan023_wangliang_reading')=='emperor-neidi') or maternal_cousin_valid(a, paragraphs), '姨表旁親須有母系路徑、雙人物錨點及姨弟原詞，不得接成父系')
                    else:
                        check(a['predicate'] == 'agnatic_cousin' and structure.get('lineage') == 'paternal' and structure.get('generation_difference') == 0 and structure.get('collateral') is True, '同世代父系旁親結構無效')
                    if a['predicate'] == 'agnatic_cousin' and 'source_clause_binding' in qualifiers and qualifiers['source_clause_binding'].get('kind') != 'biography_family_clause':
                        try:
                            from scripts.historical_family_clauses import explicit_congdi_valid
                        except ImportError:
                            from historical_family_clauses import explicit_congdi_valid
                        check(explicit_congdi_valid(a, paragraphs), '從弟須有具名雙端、原詞字位與完整引文，不得補親等共祖')
                    precise_congfudi = False
                    if a['predicate'] == 'agnatic_cousin' and qualifiers.get('source_clause_binding', {}).get('kind') == 'biography_head_named_congfudi_of_named_reference':
                        try:
                            from scripts.biography_congfudi import biography_congfudi_valid
                        except ImportError:
                            from biography_congfudi import biography_congfudi_valid
                        precise_congfudi = biography_congfudi_valid(a, paragraphs)
                    check(precise_congfudi or (structure.get('distance') is None and structure.get('common_ancestor_person_id') is None), '未定從親不可補親等或共同祖先')
                    check(structure.get('subject_relative_age') in ('younger', 'older', 'unknown'), '從親長幼欄位無效')
                if qualifiers.get('source_clause_binding', {}).get('kind') in ('speaker_self_report_congdi', 'biography_head_an_reports_to_its_congdi'):
                    try:
                        from scripts.huan_kinship_clauses import cousin_valid
                    except ImportError:
                        from huan_kinship_clauses import cousin_valid
                    check(cousin_valid(a, paragraphs), '話語回指從弟須保完整傳文與雙端，不得按近名或補親等')
                if 'mourning_separation' in qualifiers:
                    separation = qualifiers['mourning_separation']
                    valid_separation = isinstance(separation, dict)
                    if valid_separation:
                        number = separation.get('source_number')
                        valid_separation = (a['predicate'] == 'agnatic_cousin'
                            and type(separation.get('value')) is int
                            and source_age_number(number) == separation['value']
                            and separation.get('source_term') == '絕服' + str(number) + '世'
                            and separation.get('unit') == 'reported_mourning_generations'
                            and 'common_ancestor_distance' in separation and separation['common_ancestor_distance'] is None
                            and any(separation['source_term'] in e.get('quote', '') for e in a['evidence']))
                    check(valid_separation, '絕服世數須保留原詞與數字，不得換成共同祖先距離')
                if 'birth_order' in qualifiers:
                    order = qualifiers['birth_order']
                    check(a['predicate'] in ('father', 'mother') and order.get('parent_person_id') == a['object_person_id'], '排行父母端點不符')
                    check(order.get('scope') in ('sons_of_parent', 'daughters_of_parent', 'children_of_parent'), '排行序列範圍未知')
                    ordinal = order.get('ordinal')
                    check(ordinal is None or type(ordinal) is int and ordinal > 0, '排行序號須為正整數或未知')
                    check(order.get('position') in ('eldest', 'youngest', 'younger_or_youngest', 'unspecified'), '排行位置未知')
                    if order.get('position') == 'eldest': check(ordinal == 1, '長子排行須為一')
                    check(order.get('interpretation_status') in ('source_attested', 'ambiguous'), '排行判讀狀態無效')
                if 'source_sibling_group' in qualifiers or qualifiers.get('relative_birth_order', {}).get('ordinal_scope') == 'reported_sibling_group':
                    try:
                        from scripts.collateral_kinship import source_sibling_group_valid
                    except ImportError:
                        from collateral_kinship import source_sibling_group_valid
                    check(source_sibling_group_valid(a, paragraphs, pids, source_age_number), '來源姊妹群排行須保留人數、逐人稱詞與本群序號，不得補中者或小者序號')
                if 'source_explicit_father_assertion_id' in qualifiers or qualifiers.get('source_clause_binding', {}).get('kind') == 'biography_head_uncle_xiongzi_named_father':
                    try:
                        from scripts.song059_father_brother import explicit_father_elder_brother_valid
                    except ImportError:
                        from song059_father_brother import explicit_father_elder_brother_valid
                    check(explicit_father_elder_brother_valid(a, paragraphs, d['assertions']), '兄子與明示父名須有完整傳首、三端原詞及父子來源，不得補排行或祖父')
                if qualifiers.get('source_clause_binding', {}).get('kind') == 'reported_ancestor_then_named_siblings':
                    try:
                        from scripts.reported_ancestor_siblings import reported_ancestor_siblings_valid
                    except ImportError:
                        from reported_ancestor_siblings import reported_ancestor_siblings_valid
                    check(reported_ancestor_siblings_valid(a, paragraphs, d['assertions'], source_age_number),
                          '遠祖世孫後接兄弟列須連到同段祖先原斷言，不得移作傳主兄弟、反轉長幼或補共同父母')
                if qualifiers.get('source_clause_binding', {}).get('kind') == 'named_parent_sending_numbered_son':
                    try:from scripts.fixed_wikisource_units import unit_numbered_son_valid
                    except ImportError:from fixed_wikisource_units import unit_numbered_son_valid
                    check(unit_numbered_son_valid(a, paragraphs, chapters, root), '遣長子或第幾子須綁同段敘事父親、子名及原序數，不據名單補排行')
                if qualifiers.get('source_clause_binding', {}).get('kind') == 'named_older_di_younger':
                    try:
                        from scripts.named_family_offices import sibling_order_valid
                    except ImportError:
                        from named_family_offices import sibling_order_valid
                    check(sibling_order_valid(a, paragraphs), '明示某弟某的兩端原詞與相對長幼不符')
                if qualifiers.get('source_clause_binding',{}).get('kind')=='has_widowed_older_sister':
                    try:from scripts.punctuated_biography_career import sister_valid
                    except ImportError:from punctuated_biography_career import sister_valid
                    check(sister_valid(a, chapters[d['chapter_id']]), '有寡姊須綁完整同源雙端及姊長弟幼，不推父母婚姻')
                if 'relative_birth_order' in qualifiers:
                    order = qualifiers['relative_birth_order']
                    check(a['predicate'] in ('brother', 'sister', 'agnatic_cousin', 'maternal_cousin'), '相對排行須為同輩親屬')
                    check({order.get('older_person_id'), order.get('younger_person_id')} == {a['subject_person_id'], a['object_person_id']}, '相對排行端點不符')
                    scope = {'agnatic_cousin': 'agnatic_cousins', 'maternal_cousin': 'maternal_cousins'}.get(a['predicate'], 'siblings')
                    check(order.get('operator') == 'lt' and order.get('scope') == scope, '相對排行運算或範圍未知')
                    for key in ('older_ordinal', 'younger_ordinal'):
                        value = order.get(key)
                        check(value is None or type(value) is int and value > 0, '相對排行序號無效')
                context=a.get('context')
                adjacent=None
                quoted_endpoints=[]
                if context is not None:
                    check(isinstance(context,dict),'人物陳述承接格式無效')
                    if isinstance(context,dict):
                        ids=context.get('paragraph_ids')
                        order=[p['id'] for p in chapters.get(d['chapter_id'],{}).get('paragraphs',[])]
                        if context.get('kind')=='chen004_emperor_and_his_named_son':
                            check(nan23hou_valid,'陳廢帝紀傳首與光大元年皇子至澤逐位相符')
                            if nan23hou_valid: adjacent=ids
                        elif context.get('kind') == 'nan023_wangying_ranked_son':
                            check(nan23ying_valid,'王瑩卒後少子實承傳及其排行需按相接原行')
                            if nan23ying_valid: adjacent=ids
                        elif context.get('kind') == 'nan23_yun_sihua_second_son':
                            check(nan23yun_valid,'蕭思話傳末次子惠明須按父段接續與排行')
                            if nan23yun_valid: adjacent=ids
                        elif context.get('kind') == 'nan23_huan_wei71_father':
                            check(nan23huan_valid,'裴叔業傳首和原行父順宗須相符')
                            if nan23huan_valid: adjacent=ids
                        elif context.get('kind') == 'nan23_fen_quan_opening':
                            check(nan23fen_valid,'琳子銓緊承琳娶義興公主及有子九人')
                            if nan23fen_valid: adjacent=ids
                        elif context.get('kind') == 'wangdan_final_son':
                            check(wangdan52_valid,'王誕、王詡須連續前段具名父、傳末卒封及子名')
                            if wangdan52_valid: adjacent=ids
                        elif context.get('kind') == 'regnal_empress_context':
                            try:
                                from scripts.regnal_relationships import regnal_spouse_errors
                            except ImportError:
                                from regnal_relationships import regnal_spouse_errors
                            context_errors = regnal_spouse_errors(a, chapters.get(d['chapter_id'], {}))
                            errors.extend(context_errors)
                            if not context_errors: adjacent=ids
                        elif context.get('kind') == 'inscription_subject_family_list':
                            try:
                                from scripts.inscription_family_lists import valid as inscription_family_valid
                            except ImportError:
                                from inscription_family_lists import valid as inscription_family_valid
                            check(inscription_family_valid(a, chapters[d['chapter_id']]),
                                  '墓誌家屬須繫誌首具名傳主、誌末親稱與實際成員字位')
                            adjacent = ids
                        elif context.get('kind') == 'biographical_children_list':
                            try:
                                from scripts.biographical_children_lists import children_list_errors
                            except ModuleNotFoundError:
                                from biographical_children_lists import children_list_errors
                            context_errors = children_list_errors(a, chapters.get(d['chapter_id'], {}), source_age_number)
                            errors.extend(context_errors)
                            if not context_errors: adjacent = ids
                        elif context.get('kind') == 'nanshi024_printed_child_continuation':
                            check(n24szwyd_valid and qualifiers.get('nanshi024_wangshaozhi_wyd_reading')=='ye','殿本左五至六欄子曄承接原證')
                            if n24szwyd_valid:adjacent=ids
                        elif context.get('kind') == 'biographical_child_continuation':
                            try:
                                from scripts.biographical_kinship import child_continuation_errors
                            except ImportError:
                                from biographical_kinship import child_continuation_errors
                            context_errors = child_continuation_errors(a, chapters.get(d['chapter_id'], {}))
                            errors.extend(context_errors)
                            if not context_errors: adjacent = ids
                        else:
                            valid=(context.get('kind')=='adjacent_paragraphs' and isinstance(ids,list)
                                   and len(ids)==2 and all(isinstance(i,str) and i in order for i in ids)
                                   and ids==[e['paragraph_id'] for e in a['evidence']]
                                   and order.index(ids[1])==order.index(ids[0])+1)
                            if valid:
                                selected = {p['id']: p for p in chapters[d['chapter_id']]['paragraphs']}
                                positions = [selected[i].get('source_position', {}) for i in ids]
                                if all(p.get('editorial_excerpt_boundary') is True
                                       and type(p.get('first_line')) is int and type(p.get('last_line')) is int
                                       for p in positions):
                                    valid = positions[1]['first_line'] <= positions[0]['last_line'] + 1
                            check(valid,'人物陳述承接須為同篇依原序相鄰兩段證據；不可把省略原行的選錄冒作原文相鄰')
                            if valid:adjacent=ids
                for e in a['evidence']:
                    if e.get('kind') == 'table_cell':
                        errors.extend(table_evidence_errors(e, tables, a['subject_person_id'], a['object_person_id'], a['predicate']))
                        check(e.get('chapter_id') == d['chapter_id'] and adjacent is None,
                              '親屬表格證據須屬同一表篇，不得冒作段落承接')
                        term = qualifiers.get('source_term')
                        if e.get('relationship_layout') == 'founder_generation_column':
                            check(term == e.get('generation_source_term')
                                  and type(qualifiers.get('generation_distance')) is int
                                  and qualifiers['generation_distance'] == e.get('generation_distance'),
                                  '原表世代欄題與親屬限定詞、距離不符')
                        else:
                            check(isinstance(term, str) and bool(term) and term in e.get('quote', ''),
                                  '親屬表格證據缺少相符關係原詞')
                        continue
                    hit=paragraphs.get(e['paragraph_id'])
                    check(bool(hit) and hit[0]==d['chapter_id']==e['chapter_id'] and e['quote'] in hit[1]['text'],'人物陳述引句與所屬篇不符')
                    check(chapters.get(e['chapter_id'],{}).get('source_id')==e['source_id'],'人物陳述來源 ID 不符')
                    if hit:
                        local={m['person_id'] for m in hit[1]['mentions'] if m['kind']=='person'}
                        if adjacent is None:
                            if qualifiers.get('reading_basis', {}).get('kind') == 'qi032_petition_names_father':
                                try: from scripts.qi032_petition_kin import valid as qi032_petition_parent
                                except ImportError: from qi032_petition_kin import valid as qi032_petition_parent
                                check(qi032_petition_parent(a, e, chapters[e['chapter_id']]), '王琨表所載父子須對應王嗣、其子與息字')
                                continue
                            if qualifiers.get('reading_basis', {}).get('kind') == 'song080_shian_named_father':
                                try: from scripts.song080_shian_parent import valid as shian_parent
                                except ImportError: from song080_shian_parent import valid as shian_parent
                                check(shian_parent(a, e, chapters[e['chapter_id']]), '始安王劉子真須核父號、王名及第十一子原句')
                                continue
                            if qualifiers.get('reading_basis', {}).get('kind') == 'qi049_contextual_parent':
                                try: from scripts.qi049_zhang_family import valid as qi049_parent
                                except ImportError: from qi049_zhang_family import valid as qi049_parent
                                check(qi049_parent(a, e, chapters[e['chapter_id']]), '張沖所涉父母稱謂須核固定卷句與雙人字位')
                                continue
                            if 'nanshi024_reported_kin' in qualifiers:
                                continue  # Both endpoints, including named roles, were checked above.
                            if j44_valid:continue
                            if qualifiers.get('reading_basis', {}).get('kind') == 'qi040_zixiang_named_father':
                                try: from scripts.qi040_zixiang_parent import valid as zixiang_father_valid
                                except ImportError: from qi040_zixiang_parent import valid as zixiang_father_valid
                                check(zixiang_father_valid(a,e,chapters[e['chapter_id']]),'魚復侯子響須區分世祖第四子與豫章王嶷養子')
                                continue
                            if qualifiers.get('reading_basis', {}).get('kind') == 'qi035_linchuan_ying_named_father':
                                try: from scripts.qi035_linchuan_ying import valid as linchuan_ying_valid
                                except ImportError: from qi035_linchuan_ying import valid as linchuan_ying_valid
                                check(linchuan_ying_valid(a,e,chapters[e['chapter_id']]),'臨川王映的父與行次須依父稱、子名、第三子原文核實')
                                continue
                            if qualifiers.get('reading_basis', {}).get('kind') == 'nanshi060_yuansu_named_family_and_daughter':
                                try: from scripts.nanshi060_yuansu_family import valid as yuansu_family_valid
                                except ImportError: from nanshi060_yuansu_family import valid as yuansu_family_valid
                                check(yuansu_family_valid(a, e, chapters[e['chapter_id']]), '殷元素婚姻與親子須可回讀王僧朗女的原字及三個具名端點')
                                continue
                            if qualifiers.get('stone_reading',{}).get('kind')=='shijian_rubbing_kin':
                                try:from scripts.shijian_rubbings import assertion_valid as shi_stone_kin
                                except ImportError:from shijian_rubbings import assertion_valid as shi_stone_kin
                                check(shi_stone_kin(a,e,chapters[e['chapter_id']],chapters),'石氏兩誌須從物件欄位、具名傳主及親屬稱謂定向')
                                continue
                            if qualifiers.get('source_clause_binding',{}).get('kind') in ('jin067_liukun_wife_wen_maternal_aunt','liuzhu_wenshi_pu_named_daughter','jin067_emperor_yuliang_yuanjiu'):
                                try:from scripts.wenqiao_family_sources import family_valid
                                except ImportError:from wenqiao_family_sources import family_valid
                                check(family_valid(a,e,chapters[e['chapter_id']]),'溫氏傳及古譜的妻／從母／某女稱詞與姓名兩端須能逐字回讀')
                                continue
                            if qualifiers.get('reading_basis', {}).get('kind') == 'qi020_huiduan_marriage_reference':
                                try: from scripts.qi020_huiduan import marriage_valid
                                except ImportError: from qi020_huiduan import marriage_valid
                                check(marriage_valid(a, e, chapters[e['chapter_id']]), '明敬后婚配須核高帝為明帝納之的角色及舊指稱原位')
                                continue
                            if qualifiers.get('source_clause_binding',{}).get('kind') in ('jin067_liukun_wife_wen_maternal_aunt','liuzhu_wenshi_pu_named_daughter','jin067_emperor_yuliang_yuanjiu'):
                                try:from scripts.wenqiao_family_sources import family_valid
                                except ImportError:from wenqiao_family_sources import family_valid
                                check(family_valid(a,e,chapters[e['chapter_id']]),'溫氏傳及古譜的妻／從母／某女稱詞與姓名兩端須能逐字回讀')
                                continue
                            if qualifiers.get('reading_basis', {}).get('kind') == 'huifeng_long_daughter_same_father':
                                try: from scripts.jin096_huifeng import elder_valid as huifeng_elder_valid
                                except ImportError: from jin096_huifeng import elder_valid as huifeng_elder_valid
                                check(huifeng_elder_valid(a,e,chapters[e['chapter_id']]),'太子傳長女須對應長女、衍與同段王衍的實際字位')
                                continue
                            if qualifiers.get('reading_basis', {}).get('kind') == 'jin067_older_sister_husband_with_wang_clan_record':
                                try: from scripts.jin067_older_sister import valid as xifamily_sister_valid
                                except ImportError: from jin067_older_sister import valid as xifamily_sister_valid
                                check(xifamily_sister_valid(a,e,chapters),'郗愔之姊須以姊夫原位及王氏譜姓名核合')
                                continue
                            if qualifiers.get('reading_basis', {}).get('kind') == 'tao_meng_named_source_roles':
                                try: from scripts.tao_meng_family import kin_valid as tao_meng_kin_valid
                                except ImportError: from tao_meng_family import kin_valid as tao_meng_kin_valid
                                check(tao_meng_kin_valid(a,e,chapters[e['chapter_id']],root),'孟府君傳兩女親屬須逐字繫先親、第四女、陶侃第十女')
                                continue
                            if qualifiers.get('reading_basis', {}).get('kind') == 'liang022_nanping_eighth_son':
                                subject = mentions.get(e.get('subject_person_mention_id'))
                                source = chapters[e['chapter_id']]
                                ref = next((r for r in source['annotation'].get('person_reference_occurrences', [])
                                            if r['id'] == e.get('object_person_reference_id')), {})
                                order = qualifiers.get('birth_order', {})
                                check(source['id'] == 'c-liangshu-022-nanping-xiejiqing'
                                      and source['source']['revision_id'] == 1513347
                                      and e['quote'] == hit[1]['text'] == '南平元襄王偉字文達，太祖第八子也。'
                                      and a['predicate'] == 'father' and order.get('ordinal') == 8
                                      and bool(subject) and subject[1] == ref.get('paragraph_id') == e['paragraph_id']
                                      and subject[2]['surface'] == '偉' and ref.get('surface') == '太祖'
                                      and a['subject_person_id'] == subject[2]['person_id'] == 'qvt_eq1_lcf_AF'
                                      and a['object_person_id'] == ref.get('person_id') == 'qvt_eq1_lcf_A',
                                      '南平王偉的父親及排行須同時核原傳太祖與第八子')
                                continue
                            if qualifiers.get('reading_basis', {}).get('kind') == 'wangzhan_wife_and_children':
                                try: from scripts.liang021_wangzhan_kin import wife_valid as zhan_wife_valid
                                except ImportError: from liang021_wangzhan_kin import wife_valid as zhan_wife_valid
                                check(zhan_wife_valid(a, e, chapters[e['chapter_id']]), '王瞻之妻須與同句妻子合稱及丈夫字位相符')
                                continue
                            if qualifiers.get('reading_basis', {}).get('kind') == 'mourning_of_unnamed_mother_while_accompanying_a_prince':
                                try: from scripts.song042_mother_mourning import valid as mourning_mother_valid
                                except ImportError: from song042_mother_mourning import valid as mourning_mother_valid
                                check(mourning_mother_valid(a, e, chapters.get(e['chapter_id']), root), '母憂須核出征敘事的本人、匿名母親及原句')
                                continue
                            if qualifiers.get('reading_basis', {}).get('kind') == 'marriages_and_parents_in_wangkun':
                                try: from scripts.wangkun_marriage_references import valid as wangkun_kin_valid
                                except ImportError: from wangkun_marriage_references import valid as wangkun_kin_valid
                                check(wangkun_kin_valid(a, e, chapters.get(e['chapter_id']), root), '王琨傳婚姻、親子須校對固定原文與姓名或稱謂兩端')
                                continue
                            if qualifiers.get('reading_basis', {}).get('kind') == 'nanshi022_wangci_family_roles':
                                try: from scripts.nanshi022_wangci_family import valid as ci_kin_valid
                                except ImportError: from nanshi022_wangci_family import valid as ci_kin_valid
                                check(ci_kin_valid(a, e, chapters.get(e['chapter_id']), root), '王慈、王泰傳親屬須有各自原句及姓名或稱謂雙端')
                                continue
                            if qualifiers.get('reading_basis', {}).get('kind') == 'nanshi022_wanggui_opening_kin':
                                try: from scripts.nanshi022_wanggui_kin import valid as gui_kin_valid
                                except ImportError: from nanshi022_wanggui_kin import valid as gui_kin_valid
                                check(gui_kin_valid(a, e, chapters, root), '王規傳生母及叔父須在同一傳首核雙端')
                                continue
                            if qualifiers.get('reading_basis', {}).get('kind') == 'nanshi022_wangjian_marriage':
                                try: from scripts.nanshi022_wangjian_marriage import valid as wangjian_marriage
                                except ImportError: from nanshi022_wangjian_marriage import valid as wangjian_marriage
                                check(wangjian_marriage(a, e, chapters[e['chapter_id']], root), '王暕選尚須有淮南長公主原句及傳主')
                                continue
                            if qualifiers.get('reading_basis', {}).get('kind') == 'song041_wang_wangxianyuan_family_named_and_titled_family':
                                try: from scripts.song041_wang_wangxianyuan_family import valid as wang_kin_valid
                                except ImportError: from song041_wang_wangxianyuan_family import valid as wang_kin_valid
                                check(wang_kin_valid(a,e,chapters[d['chapter_id']],root), '王氏婚親稱謂須符合固定正文句及兩人字位')
                                continue
                            if qualifiers.get('reading_basis', {}).get('kind') == 'song041_wang_wangzhenfeng_named_and_titled_family':
                                try: from scripts.song041_wang_wangzhenfeng import valid as wang_kin_valid
                                except ImportError: from song041_wang_wangzhenfeng import valid as wang_kin_valid
                                check(wang_kin_valid(a,e,chapters[d['chapter_id']],root), '王氏婚親稱謂須符合固定正文句及兩人字位')
                                continue
                            if qualifiers.get('reading_basis', {}).get('kind') == 'song066_named_anonymous_family':
                                try: from scripts.song066_readings import kin_valid as song066_kin
                                except ImportError: from song066_readings import kin_valid as song066_kin
                                check(song066_kin(a,e,chapters[d['chapter_id']],root), '王敬弘妻女親屬須合固定全句及稱謂角色')
                                continue
                            if qualifiers.get('reading_basis', {}).get('kind') == 'jin075_xunxian_titled_or_anonymous_kin':
                                try:
                                    from scripts.jin075_reference_evidence import kin_valid
                                except ImportError:
                                    from jin075_reference_evidence import kin_valid
                                check(kin_valid(a, e, chapters.get(e['chapter_id']), root), '荀羨親屬須核固定原文、稱謂與兩端人物')
                                continue
                            if 'royal_kin_frame' in qualifiers:
                                try:
                                    from scripts.nanshi022_royal_kin import valid as royal_kin_valid
                                except ImportError:
                                    from nanshi022_royal_kin import valid as royal_kin_valid
                                check(royal_kin_valid(a, chapters[d['chapter_id']], root), '卷二十二帝女王妃的親屬需核同段稱謂、原字、所屬王及對應親人')
                            elif 'wang_women_kin_frame' in qualifiers:
                                try: from scripts.wang_family_women_sources import kin_valid as wang_women_kin_valid
                                except ImportError: from wang_family_women_sources import kin_valid as wang_women_kin_valid
                                check(wang_women_kin_valid(a, chapters[d['chapter_id']], root), '王氏婚家各傳的姓名與稱呼、父母子女次序及固定原文須一致')
                            elif 'wyd_song063_kin_frame' in qualifiers:
                                check(wyd63_kinship, '王曇首兄弟、從親及子列的原字與人物不符')
                            elif 'liang033_family_reading' in qualifiers:
                                check(liang33_valid, '王筠及謝氏原句的姓名、稱號及親屬端點不合')
                            elif 'liang021_tai_reading' in qualifiers:
                                check(tai21_valid,'王泰關係原字或兩端不符')
                            elif 'liang021_jun_reading' in qualifiers:
                                check(j21_valid,'王峻、琮及齊王之兩端姓名或稱謂有誤')
                            elif 'liang021_fen_reading' in qualifiers:
                                check(wf21_valid,'王份家之兩端姓名或稱謂有誤')
                            elif 'liang021_wangxun_reading' in qualifiers:
                                check(xun21_valid,'本傳親屬的兩端姓名或稱謂有誤')
                            elif 'liang021_wangjiansihui_reading' in qualifiers:
                                check(sih21_valid,'本傳親屬的兩端姓名或稱謂有誤')
                            elif 'song052_xiechun_reading' in qualifiers:
                                check(chun52_valid,'本傳親屬的兩端姓名或稱謂有誤')
                            elif 'song052_xiejingren_reading' in qualifiers:
                                check(xiejingren52_valid,'本傳親屬的兩端姓名或稱謂有誤')
                            elif 'nan023_digital_reading' in qualifiers:
                                check(nan23dan_valid,'本傳親屬的兩端姓名或稱謂有誤')
                            elif 'song052_wangdan_reading' in qualifiers:
                                check(wangdan52_valid,'本傳親屬的兩端姓名或稱謂有誤')
                            elif 'song052_xieshu_reading' in qualifiers:
                                check(xieshu52_valid,'本傳親屬的兩端姓名或稱謂有誤')
                            elif 'nan023_print_reading' in qualifiers:
                                check(nan23p_valid,'本傳親屬的兩端姓名或稱謂有誤')
                            elif 'nan023_wangmao_reading' in qualifiers:
                                check(nan23mao_valid,'本傳親屬的兩端姓名或稱謂有誤')
                            elif 'nan023_jiangxiao_reading' in qualifiers:
                                check(nan23jiang_valid,'本傳親屬的兩端姓名或稱謂有誤')
                            elif 'nan023_chuai_reading' in qualifiers:
                                check(nan23chuai_valid,'本傳親屬的兩端姓名或稱謂有誤')
                            elif 'nan023_heyu_reading' in qualifiers:
                                check(nan23heyu_valid,'本傳親屬的兩端姓名或稱謂有誤')
                            elif 'nan023_wangzao_reading' in qualifiers:
                                check(nan23zao_valid,'本傳親屬的兩端姓名或稱謂有誤')
                            elif 'nan023_wangliang_reading' in qualifiers:
                                check(nan23liang_valid,'本傳親屬的兩端姓名或稱謂有誤')
                            elif 'nan023_wangying_reading' in qualifiers:
                                check(nan23ying_valid,'本傳親屬的兩端姓名或稱謂有誤')
                            elif 'nan023_wanghui_reading' in qualifiers:
                                check(nan23hui_valid,'本傳親屬的兩端姓名或稱謂有誤')
                            elif 'nan023_wangqiu_reading' in qualifiers:
                                check(nan23qiu_valid,'本傳親屬的兩端姓名或稱謂有誤')
                            elif 'nan023_wangxuan_reading' in qualifiers:
                                check(nan23xuan_valid,'本傳親屬的兩端姓名或稱謂有誤')
                            elif 'nan023_wanghui_sons_reading' in qualifiers:
                                check(nan23huiz_valid,'本傳親屬的兩端姓名或稱謂有誤')
                            elif 'nan023_chuzhanzhi_reading' in qualifiers:
                                check(nan23chu_valid,'本傳親屬的兩端姓名或稱謂有誤')
                            elif 'nan023_wangyun_reading' in qualifiers:
                                check(nan23yun_valid,'本傳親屬的兩端姓名或稱謂有誤')
                            elif 'nan023_wanghuan_reading' in qualifiers:
                                check(nan23huan_valid,'本傳親屬的兩端姓名或稱謂有誤')
                            elif 'nan023_wangxi_reading' in qualifiers:
                                check(nan23xi_valid,'本傳親屬的兩端姓名或稱謂有誤')
                            elif 'nan023_wangfen_reading' in qualifiers:
                                check(nan23fen_valid,'本傳親屬的兩端姓名或稱謂有誤')
                            elif 'nan023_wangtong_reading' in qualifiers:
                                check(nan23tong_valid,'本傳親屬的兩端姓名或稱謂有誤')
                            elif 'nan023_wangmai_reading' in qualifiers:
                                check(nan23mai_valid,'本傳親屬的兩端姓名或稱謂有誤')
                            elif 'nan023_wangzhi_reading' in qualifiers:
                                check(nan23zhi_valid,'本傳親屬的兩端姓名或稱謂有誤')
                            elif 'nan023_wanggu_reading' in qualifiers:
                                check(nan23gu_valid,'本傳親屬的兩端姓名或稱謂有誤')
                            elif 'nan023_wanghou_reading' in qualifiers:
                                check(nan23hou_valid,'本傳親屬的兩端姓名或稱謂有誤')
                            elif 'nan023_wangyu_reading' in qualifiers:
                                check(nan23yu_valid,'本傳親屬的兩端姓名或稱謂有誤')
                            elif 'nanqi047_wangrong_reading' in qualifiers:
                                check(qi47rong_valid,'本傳親屬的兩端姓名或稱謂有誤')
                            elif 'liang033_wangsengru_reading' in qualifiers:
                                check(liang33sr_valid,'本傳親屬的兩端姓名或稱謂有誤')
                            elif 'nanshi059_wangsengru_reading' in qualifiers:
                                check(nan59sr_valid,'本傳親屬的兩端姓名或稱謂有誤')
                            elif 'nanqi047_wangrong_wyd_reading' in qualifiers:
                                check(q47wyd_valid,'王融殿本親屬的姓名或稱謂原欄有誤')
                            elif 'nanqi047_xietiao_wife' in qualifiers:
                                check(qi47wife_ok,'王敬則女原人稱不合')
                            elif 'nanshi024_wangshaozhi_reading' in qualifiers:
                                check(nan24sz_valid,'本傳親屬的兩端姓名或稱謂有誤')
                            elif 'nanshi024_wangshaozhi_wyd_reading' in qualifiers:
                                check(n24szwyd_valid,'王韶之殿本親屬的姓名或稱謂原欄有誤')
                            elif 'nanshi024_wangyuezhi_reading' in qualifiers:
                                check(nan24yz_valid,'本傳親屬的兩端姓名或稱謂有誤')
                            elif 'nanshi024_wangzhunzhi_reading' in qualifiers:
                                check(nan24zz_valid,'本傳親屬的兩端姓名或稱謂有誤')
                            elif 'nanshi024_wangjinzhi_reading' in qualifiers:
                                check(nan24jz_valid,'本傳親屬的兩端姓名或稱謂有誤')
                            elif 'nanshi024_wangqing_reading' in qualifiers:
                                check(nan24qing_valid,'本傳親屬的兩端姓名或稱謂有誤')
                            elif 'nanshi024_wangqunzhi_reading' in qualifiers:
                                check(nan24qun_valid,'本傳親屬的兩端姓名或稱謂有誤')
                            elif 'nanshi024_wangsu_reading' in qualifiers:
                                check(nan24su_valid,'本傳親屬的兩端姓名或稱謂有誤')
                            elif 'nanshi024_ruanwanling_reading' in qualifiers:
                                check(nan24rw_valid,'本傳親屬的兩端姓名或稱謂有誤')
                            elif 'nanshi024_wanghongzhi_reading' in qualifiers:
                                check(n24hong_valid,'南史王弘之親屬兩端不符')
                            elif 'song093_hongzhi_reading' in qualifiers:
                                check(hongzhi_valid,'弘之母、外祖與從親的方向錯誤')
                            elif 'song093_wyd_reading' in qualifiers:
                                check(s93wyd_valid,'宋九十三殿本原欄兩端有誤')
                            elif 'nanshi024_wangmeng_reading' in qualifiers:
                                check(nan24meng_valid,'本傳親屬的兩端姓名或稱謂有誤')
                            elif 'xiangshan_m9_epitaphs_reading' in qualifiers:
                                check(xm9_valid,'本傳親屬的兩端姓名或稱謂有誤')
                            elif 'nanshi024_wangyan_reading' in qualifiers:
                                check(nan24yan_valid,'本傳親屬的兩端姓名或稱謂有誤')
                            elif 'nanshi024_wangyan_brothers_reading' in qualifiers:
                                check(nan24wab_valid,'本傳親屬的兩端姓名或稱謂有誤')
                            elif 'nanshi024_guhaozhi_reading' in qualifiers:
                                check(nan24gh_valid,'本傳親屬的兩端姓名或稱謂有誤')
                            elif 'nanshi024_wangsiyuan_reading' in qualifiers:
                                check(nan24siy_valid,'本傳親屬的兩端姓名或稱謂有誤')
                            elif 'wyd_song071_kin_frame' in qualifiers:
                                try: from scripts.wyd_song071_wang import kin_valid as wyd71_kin_valid
                                except ImportError: from wyd_song071_wang import kin_valid as wyd71_kin_valid
                                check(wyd71_kin_valid(a, chapters[d['chapter_id']], root), '宋卷71殿本的兩端必須確合該欄的姓名、稱號及親屬方向')
                            elif 'pei_kin_frame' in qualifiers:
                                check(pei_valid,'具名及稱謂的雙人原字不合')
                            elif 'nan22jian_kin_frame' in qualifiers:
                                check(n22jian_valid,'王儉親屬稱謂的原字方向不合')
                            elif 'qi23_kin_frame' in qualifiers:
                                check(qi23_valid,'王儉親屬陳述的原文端點不合')
                            elif 'ws_song071_kin_frame' in qualifiers:
                                try: from scripts.ws_song071_wang import kin_valid as ws71_kin_valid
                                except ImportError: from ws_song071_wang import kin_valid as ws71_kin_valid
                                check(ws71_kin_valid(a, chapters[d['chapter_id']], root), '宋卷71固定數位本的兩端必須確合原段姓名、稱謂及親屬方向')
                            elif 'reading_basis' in qualifiers and qualifiers['reading_basis'].get('kind') == 'xietiao_named_or_titled_kin':
                                try:
                                    from scripts.xietiao_titled_kin import valid as titled_kin_valid
                                except ImportError:
                                    from xietiao_titled_kin import valid as titled_kin_valid
                                check(titled_kin_valid(a, chapters, root), '謝朓所涉稱謂親屬須核固定原句、指代雙端及明名旁證')
                            elif qualifiers.get('source_clause_binding', {}).get('kind') == 'shishuo_zhenzhi_seventh_uncle':
                                try:
                                    from scripts.jin080_family import named_uncle_valid
                                except ImportError:
                                    from jin080_family import named_uncle_valid
                                check(named_uncle_valid(a, paragraphs), '世說王楨之稱七叔，須以原文及王獻之對讀')
                            elif a.get('qualifiers', {}).get('source_clause_binding', {}).get('kind') == 'zhengao_xumai_wife_named_father':
                                try:
                                    from scripts.jin080_xumai import wife_father_valid
                                except ImportError:
                                    from jin080_xumai import wife_father_valid
                                check(wife_father_valid(a, chapters), '真誥孫宏女須有妻之指代及父親姓名')
                            elif qualifiers.get('annal_context') == 'nanshi_ming_named_prince':
                                try: from scripts.qi020_chulingqu import named_prince_valid
                                except ImportError: from qi020_chulingqu import named_prince_valid
                                check(named_prince_valid(a, chapters[d['chapter_id']], root), '皇子父稱須繫同一帝紀的君名及受冊原句')
                            elif qualifiers.get('reading_basis', {}).get('kind') == 'jin076_shihou':
                                try: from scripts.jin076_shihou import valid as shihou_valid
                                except ImportError: from jin076_shihou import valid as shihou_valid
                                check(shihou_valid(a, chapters[d['chapter_id']], root), '石碏父子須合隱三轉述其子厚與隱四具名原文')
                            else:
                                check(a['subject_person_id'] in local and a['object_person_id'] in local, '人物陳述端點未見於證據段落')
                        else:
                            quote=e['quote'];text=hit[1]['text']
                            starts=[i for i in range(len(text)+1) if text.startswith(quote,i)]
                            quoted={m['person_id'] for m in hit[1]['mentions'] if m['kind']=='person'
                                    and any(i<=m['start'] and m['end']<=i+len(quote) for i in starts)}
                            quoted_endpoints.append(quoted)
                if adjacent is not None and context.get('kind') == 'nan23_huan_wei71_father':
                    try: from scripts.nan023_wanghuan import wei71_father_endpoints
                    except ImportError: from nan023_wanghuan import wei71_father_endpoints
                    check(wei71_father_endpoints(a,chapters[d['chapter_id']],root,adjacent,quoted_endpoints),'魏書裴叔業同一原行須先具傳主、後具父名')
                elif adjacent is not None and context.get('kind') != 'inscription_subject_family_list':
                    check(len(quoted_endpoints)==len(adjacent) and a['object_person_id'] in quoted_endpoints[0]
                          and a['subject_person_id'] in quoted_endpoints[-1],
                          '人物陳述承接的前段客體及後段主體未見於引句')
        proposal_ids = set()
        for chapter in chapters.values():
            for proposal in chapter['annotation'].get('title_proposals', []):
                check(proposal.get('id') and proposal['id'] not in proposal_ids, '稱號提議 ID 缺失或重複')
                proposal_ids.add(proposal.get('id'))
                errors.extend(title_proposal_errors(proposal, chapter, set(pids), title_records))
                if isinstance(proposal.get('source_appointment_context'), dict) and 'normalized_date' in proposal:
                    check(proposal['normalized_date'].get('evidence') == proposal.get('evidence')
                          and proposal['normalized_date'].get('source_expression') == proposal.get('date_expression'), '任命通知紀年須綁同一原句')
                    errors.extend(normalized_date_errors(proposal['normalized_date'], chapters, root, proposal, 'appointment_notice'))

        try:
            from scripts.song041_title_semantics import source_use_errors
        except ImportError:
            from song041_title_semantics import source_use_errors
        for chapter in chapters.values():
            for use in chapter['annotation'].get('source_title_uses', []):
                errors.extend(source_use_errors(use, chapter, pids, title_records))
        age_ids = set(); age_report_groups = {}
        for chapter in chapters.values():
            for age in chapter['annotation'].get('age_assertions', []):
                check(age['id'] not in age_ids, '年齡記錄 ID 重複'); age_ids.add(age['id'])
                number = age.get('source_number'); parsed = source_age_number(number)
                dialogue_anchor = None
                if age.get('source_repeated_age',{}).get('kind')=='reported_by_huan_xuan':
                    try: from scripts.song052_xiejingren import age_valid as sj52_age
                    except ImportError: from song052_xiejingren import age_valid as sj52_age
                    check(sj52_age(age,chapter,root),'桓玄引語中的三十須對應本段先敘年三十、具名謝景仁與著作佐郎')
                elif age.get('issued_xun_elliptical_age'):
                    try: from scripts.liang021_wangxun import age_valid as xun21_age
                    except ImportError: from liang021_wangxun import age_valid as xun21_age
                    check(xun21_age(age,chapter,root),'十六須承同一王訓年十三後召見之句')
                elif 'wang_family_age_reading' in age:
                    try: from scripts.liang021_wangfen_family import age_valid as wf_age_valid
                    except ImportError: from liang021_wangfen_family import age_valid as wf_age_valid
                    check(wf_age_valid(age,chapter,root),'王份、諸子孫的省略歲數或約齡必須與原句相合')
                elif 'reported_dialogue' in age:
                    try: from scripts.nanshi019_dialogue import age_anchor
                    except ImportError: from nanshi019_dialogue import age_anchor
                    dialogue_anchor = age_anchor(age, chapter)
                    check(bool(dialogue_anchor), '引語報齡須綁實際答者或被引者')
                elif 'received_unit_age_binding' in age:
                    try:from scripts.fixed_wikisource_units import unit_group_age_bound_valid
                    except ImportError:from fixed_wikisource_units import unit_group_age_bound_valid
                    check(unit_group_age_bound_valid(age, chapter, root, source_age_number), '具名群體年過須保各人、數詞與嚴格下界，不補生年或改卒齡')
                elif age.get('approximation', {}).get('kind') == 'quoted_kin_age_designation':
                    try:from scripts.fixed_wikisource_units import kin_age_designation_valid
                    except ImportError:from fixed_wikisource_units import kin_age_designation_valid
                    check(kin_age_designation_valid(age, chapter, root), '引語父親約數報齡須綁發言者、父子原證與原數，不推精齡或生年')
                elif 'source_age_answer_binding' in age:
                    try:from scripts.wyd_song044_age import answer_valid
                    except ImportError:from wyd_song044_age import answer_valid
                    check(answer_valid(age,chapter,root),'問年答齡須綁詢問與回答同人、完整原詞，不借他人之齡或造引句')
                elif 'approximation' in age:
                    try:
                        from scripts.age_approximations import age_approximation_errors
                    except ModuleNotFoundError:
                        from age_approximations import age_approximation_errors
                    for evidence in age.get('evidence', []):
                        hit = paragraphs.get(evidence.get('paragraph_id'))
                        if hit:
                            errors.extend(age_approximation_errors(age, hit[1], chapter['annotation'].get('person_reference_occurrences', [])))
                    check(bool(age.get('evidence')), '約數報齡缺少來源證據')
                elif 'bounds' in age:
                    bounds = age.get('bounds'); group = age.get('group_reference')
                    if group is not None:
                        check(age.get('value') is None and parsed is not None and isinstance(bounds, dict)
                              and bounds == {'lower': parsed, 'lower_inclusive': False, 'upper': None, 'upper_inclusive': None}
                              and age.get('source_term') in ('年皆' + str(number) + '有餘', '年' + str(number) + '餘'), '來源年齡界限與有餘原詞不符')
                        keys = set(group) if isinstance(group, dict) else set()
                        ids = group.get('person_ids') if isinstance(group, dict) else None
                        members = ids if isinstance(ids, list) else []
                        complete_four = (keys == {'source_term', 'naming_term', 'person_ids'}
                                         and group.get('source_term') == '四人從太子' and len(members) == 4)
                        named_subset = (keys == {'source_term', 'naming_term', 'person_ids', 'additional_members_unknown'}
                                        and group.get('additional_members_unknown') is True
                                        and isinstance(group.get('source_term'), str) and group['source_term'].endswith('等')
                                        and isinstance(group.get('naming_term'), str) and bool(group['naming_term'])
                                        and group['naming_term'] in group['source_term'])
                        check((complete_four or named_subset) and bool(members)
                              and all(isinstance(i, str) for i in members)
                              and len(set(members)) == len(members) and age['person_id'] in members,
                              '群體報齡具名範圍或未名成員不符')
                        for evidence in age.get('evidence', []):
                            hit = paragraphs.get(evidence.get('paragraph_id'))
                            if isinstance(group, dict) and hit:
                                phrase = group.get('naming_term')
                                starts = [i for i in range(len(hit[1]['text'])) if hit[1]['text'].startswith(phrase, i)] if isinstance(phrase, str) and phrase else []
                                named = {m['person_id'] for m in hit[1]['mentions'] if m['kind'] == 'person'
                                         and any(i <= m['start'] and m['end'] <= i + len(phrase) for i in starts)}
                                check(isinstance(phrase, str) and bool(phrase) and phrase in evidence.get('quote', '')
                                      and isinstance(group.get('source_term'), str) and group['source_term'] in evidence.get('quote', '')
                                      and named == {i for i in members if isinstance(i, str)}, '群體報齡具名名單未見於引句')
                    elif age.get('reporting_status') == 'upper_bound_report':
                        check(age.get('value') is None and parsed is not None
                              and bounds == {'lower': None, 'lower_inclusive': None, 'upper': parsed, 'upper_inclusive': False}
                              and age.get('source_term') in ('年未滿' + str(number), '未滿' + str(number) + '歲', '未滿' + str(number) + '歳')
                              and age.get('source_qualification') is None and not age.get('report_group_id'),
                              '來源未滿報齡須保存開放上界及原詞，不得補確切歲數')
                    elif age.get('reporting_status') == 'direct_report':
                        check(age.get('value') is None and parsed is not None
                              and bounds == {'lower': parsed, 'lower_inclusive': False, 'upper': None, 'upper_inclusive': None}
                              and age.get('source_term') in (str(number) + '餘歲', str(number) + '有餘歲', '年' + str(number) + '餘', '時年已' + str(number) + '餘', '年出' + str(number) + '歲', '年出' + str(number) + '歳')
                              and age.get('source_qualification') is None and not age.get('report_group_id'),
                              '直接報齡餘歲須保存開放下界及原詞，不得補限定詞或傳聞分組')
                    else:
                        check(age.get('value') is None and parsed is not None
                              and bounds == {'lower': parsed, 'lower_inclusive': False, 'upper': None, 'upper_inclusive': None}
                              and age.get('source_term') == str(number) + '餘歲', '個人報齡餘歲界限與原詞不符')
                        marker = age.get('source_qualification')
                        report_id = age.get('report_group_id')
                        if isinstance(report_id, str) and report_id:
                            report_scope = (age.get('person_id'), chapter['id'],
                                tuple(sorted((e.get('source_id', ''), e.get('paragraph_id', '')) for e in age.get('evidence', []))))
                            existing = age_report_groups.setdefault(report_id, {'scope': report_scope, 'statuses': []})
                            check(existing['scope'] == report_scope, '同組報齡須同人物及來源段落')
                            existing['statuses'].append(age.get('reporting_status'))
                        else:
                            check(False, '個人報齡分組ID無效')
                        check(bool(age.get('report_group_id')) and (marker, age.get('reporting_status')) in
                              (('蓋', 'qualified_report'), ('或言', 'alternative_report'))
                              and isinstance(age.get('qualified_source_term'), str)
                              and age['qualified_source_term'].startswith(str(marker))
                              and age['qualified_source_term'].endswith(str(age.get('source_term')))
                              and any(age['qualified_source_term'] in e.get('quote', '') for e in age.get('evidence', [])), '個人報齡缺來源限定詞或傳聞狀態')
                else:
                    epitaph_death_age = (
                        works[chapter['work_id']].get('work_type') == 'single_epitaph'
                        and age.get('age_context', {}).get('kind') == 'at_death'
                        and age.get('source_term') == '春秋' + str(number)
                        and type(age.get('value')) is int and parsed == age['value'])
                    try: from scripts.nanshi022_wangxun_age import valid as xun_continued_age
                    except ImportError: from nanshi022_wangxun_age import valid as xun_continued_age
                    check(direct_source_age_valid(age) or epitaph_death_age
                          or (age.get('elliptical_age_basis', {}).get('kind') == 'same_biography_continued_age' and xun_continued_age(age, chapter, root)),
                          '來源年齡數值與原詞不符')
                check(age.get('counting') == 'unspecified_source_age' and age.get('unit') == 'source_age_years'
                      and age.get('birth_year') is None and age.get('status') == 'source_attested',
                      '來源年齡不得推定計歲方式或出生年')
                check(age['person_id'] in pids and bool(age['evidence']), '來源年齡缺人物或證據')
                for evidence in age['evidence']:
                    hit = paragraphs.get(evidence['paragraph_id']); mention = mentions.get(evidence.get('person_mention_id'))
                    check(bool(hit) and hit[0] == chapter['id'] == evidence['chapter_id']
                          and evidence['source_id'] == chapter['source_id'] and evidence['quote'] in hit[1]['text']
                          and age['source_term'] in evidence['quote'], '來源年齡引句不符')
                    carried_age_subject = False
                    if age.get('source_reference_id') and chapter.get('id') == 'c-nanshi-019-nan19':
                        try:from scripts.nanshi019_zhan_roles import kin_age
                        except ImportError:from nanshi019_zhan_roles import kin_age
                        carried_age_subject = kin_age(age, chapter, evidence)
                    if 'context' in evidence:
                        try:
                            from scripts.subject_continuation import prior_subject_valid
                        except ImportError:
                            from subject_continuation import prior_subject_valid
                        carried_age_subject = prior_subject_valid(evidence['context'], evidence, age['person_id'], chapter)
                        check(carried_age_subject, '來源年齡省略主語承接無效')
                    if evidence.get('person_reference_id') and chapter['id']=='c-songshu-041-wangzhenfeng':
                        try: from scripts.song041_wang_obituaries import valid as royal_obituary
                        except ImportError: from song041_wang_obituaries import valid as royal_obituary
                        carried_age_subject=royal_obituary(age,evidence,chapter,root,age=True)
                    check(dialogue_anchor or carried_age_subject or bool(mention) and mention[1] == evidence['paragraph_id'] and mention[2]['person_id'] == age['person_id'], '來源年齡人物錨點不符')
                if 'report_repetition_of' in age:
                    reports = chapter['annotation']['age_assertions']
                    target = next((r for r in reports[:reports.index(age)] if r['id'] == age['report_repetition_of']), None)
                    check(bool(target) and target['person_id'] == age['person_id']
                          and target.get('value') == age.get('value') and target.get('bounds') == age.get('bounds')
                          and target.get('approximation') == age.get('approximation')
                          and target.get('unit') == age.get('unit') and target.get('counting') == age.get('counting')
                          and bool(age.get('interpretation_note')), '報齡重述須指同篇前筆同人物及相同年數，不得補年齡變化')
                if 'normalized_date_range' in age:
                    try:
                        from scripts.date_ranges import year_range_errors
                    except ImportError:
                        from date_ranges import year_range_errors
                    check('normalized_date' not in age, '來源報齡跨年範圍不得另填確定單年')
                    errors.extend(year_range_errors(age['normalized_date_range'], age['evidence'], age.get('date_expression')))
                    errors.extend(table_regnal_range_errors(age['normalized_date_range'], age.get('date_expression'), tables, mentions))
                if 'normalized_date' in age:
                    errors.extend(normalized_date_errors(age['normalized_date'], chapters, root=root))
                    check(age['normalized_date'].get('original_quote') in [e['quote'] for e in age['evidence']], '來源年齡紀年原句不符')
            for age in chapter['annotation'].get('age_difference_assertions', []):
                check(age['id'] not in age_ids, '年齡差記錄ID重複'); age_ids.add(age['id'])
                parsed = source_age_number(age.get('source_number'))
                check(type(age.get('value')) is int and parsed is not None and age['value'] == parsed and parsed > 0
                      and age.get('comparison') == 'younger_than', '年齡差數值或方向不符')
                check(age.get('person_id') in pids and age.get('reference_person_id') in pids
                      and age.get('person_id') != age.get('reference_person_id'), '年齡差須有兩個不同人物')
                check(age.get('unit') == 'source_age_years' and age.get('counting') == 'unspecified_source_age'
                      and age.get('birth_year') is None and age.get('date_expression') is None
                      and 'normalized_date' not in age and age.get('status') == 'source_attested', '年齡差不得推生年日期或計歲方式')
                check(bool(age.get('evidence')) and bool(age.get('interpretation_note')) and bool(age.get('reviewer'))
                      and age.get('human_reviewed') is False, '年齡差缺來源或判讀')
                for evidence in age.get('evidence', []):
                    hit = paragraphs.get(evidence.get('paragraph_id'))
                    subject = mentions.get(evidence.get('person_mention_id'))
                    reference = mentions.get(evidence.get('reference_person_mention_id'))
                    quote = evidence.get('quote')
                    valid = bool(hit) and hit[0] == chapter['id'] == evidence.get('chapter_id') and evidence.get('source_id') == chapter['source_id']
                    check(valid and isinstance(quote, str) and bool(quote) and quote in hit[1]['text'], '年齡差来源引句不符'.replace('来源','來源'))
                    for anchor, pid in [(subject, age.get('person_id')), (reference, age.get('reference_person_id'))]:
                        check(bool(anchor) and anchor[1] == evidence.get('paragraph_id') and anchor[2].get('person_id') == pid, '年齡差人物錨點不符')
                        if valid and anchor and isinstance(quote, str):
                            check(any(i <= anchor[2]['start'] and anchor[2]['end'] <= i + len(quote)
                                      for i in range(len(hit[1]['text'])) if hit[1]['text'].startswith(quote, i)), '年齡差人物未在引句中')
                    if reference and isinstance(quote, str):
                        terms = ['少' + reference[2]['surface'] + str(age.get('source_number')) + suffix for suffix in ('歲', '歳')]
                        check(age.get('source_term') in terms and age.get('source_term') in quote, '年齡差原詞與參考人物不符')
        for report in age_report_groups.values():
            check('qualified_report' in report['statuses'], '報齡替代傳聞缺同組主報齡')
        try:
            from scripts.song041_source_context import temporal_errors, unresolved_kin_errors
        except ImportError:
            from song041_source_context import temporal_errors, unresolved_kin_errors
        context_events = {e['id']:e for path in (root / 'corpus').glob('*/*-life-events.json') for e in json.loads(path.read_text())['events']}
        for path in (root / 'corpus').glob('*/*-temporal.json'):
            errors.extend(temporal_errors(json.loads(path.read_text()), chapters, pids, normalized_date_errors, context_events))
        for chapter in chapters.values():
            for case in chapter['annotation'].get('unresolved_kinship_references', []):
                errors.extend(unresolved_kin_errors(case, chapters, pids))
        address_ids = set()
        for path in (root / 'corpus').glob('*/*-addresses.json'):
            record = json.loads(path.read_text(encoding='utf-8'))
            check(record['record_type'] == 'person_address_assertion_set' and record['chapter_id'] in chapters, '地址主張集格式或篇不存在')
            for address in record['assertions']:
                if 'received_source_frame' in address:
                    try:from scripts.fixed_received_career import nonholding_valid
                    except ImportError:from fixed_received_career import nonholding_valid
                    check(nonholding_valid(address,chapters[record['chapter_id']],root,'address'),'固定收到地稱須綁原主語，不移籍貫/官地')
                if 'source_address_binding' in address:
                    try:from scripts.layered_biography_titles import address_valid
                    except ImportError:from layered_biography_titles import address_valid
                    check(address_valid(address,chapters[record['chapter_id']]),'地望須逐角色綁原詞與來源，隱居不作卒地、共稱不擴及後人')
                check(address['id'] not in address_ids, '地址主張 ID 重複'); address_ids.add(address['id'])
                check(address['person_id'] in pids and address['status'] == 'source_attested', '地址人物或狀態無效')
                check(address['relation'] in ('biographical_origin', 'ancestral_origin', 'native_place', 'birth_place', 'residence', 'death_place', 'migration_origin', 'migration_destination', 'burial_place', 'capital_location', 'polity_lineage_affiliation', 'source_locality_designation', 'service_location', 'fief'), '地址關係類型未知')
                if address['relation'] == 'fief' or 'fief_kind' in address.get('qualifiers', {}):
                    kind = address.get('qualifiers', {}).get('fief_kind')
                    word = {'tangmu_estate':'湯沐邑', 'maintenance_allocation':'奉', 'territorial_grant':'賜', 'approved_enfeoffment':'許之', 'household_revenue':'食'}.get(kind)
                    if kind == 'household_revenue':
                        check(bool(re.fullmatch(r'食.+[萬千百十〇零一二三四五六七八九兩0-9]+戶', address.get('source_term', ''))), '食戶地望須保存食地名與戶數原語，不得當人口或居處')
                    if kind == 'approved_enfeoffment':
                        check('封' in address.get('source_term', '') and '許之' in address.get('source_term', ''), '准封地望須保存提請與明示允許，不得只據請封記實授')
                    check(address['relation'] == 'fief' and bool(word)
                          and isinstance(address.get('source_term'), str) and word in address['source_term'],
                          '食邑主張須保存湯沐邑或奉原詞及類型，不得改為籍貫')
                if 'reported_duration' in address:
                    duration = address['reported_duration']
                    check(address['relation'] == 'residence' and isinstance(duration, dict)
                          and duration.get('unit') == 'residence_year'
                          and duration.get('counting') == 'unspecified_source_years'
                          and duration.get('status') == 'source_attested'
                          and type(duration.get('value')) is int and duration['value'] > 0
                          and source_age_number(duration.get('source_number')) == duration['value']
                          and isinstance(duration.get('source_term'), str)
                          and duration['source_term'].endswith(duration['source_number'] + '年')
                          and duration.get('evidence') == address['evidence']
                          and all(duration['source_term'] in e['quote'] for e in address['evidence']),
                          '居留來源年數須有數值、原數詞與同項證據，不得當官爵任期或推曆日')
                if address['relation'] == 'source_locality_designation':
                    scope = address.get('qualifiers', {})
                    check(scope.get('designation_kind') == 'geographical_person_reference'
                          and 'origin_or_residence' in scope and scope['origin_or_residence'] is None
                          and address['place']['source_name'] in address['source_term'],
                          '來源地稱須保留未明籍貫或居所，不得轉成出生地')
                if address['relation'] == 'capital_location':
                    scope = address.get('qualifiers', {})
                    check(scope.get('seat_kind') == 'royal_capital'
                          and scope.get('source_action') == '都'
                          and address.get('source_term') == '都' + address['place']['source_name'],
                          '王都須有都與原地名，不得當籍貫或個人居所')
                if address['relation'] == 'service_location':
                    position = address.get('qualifiers', {}).get('source_position')
                    check(bool(position) and position in address['source_term']
                          and address['place']['source_name'] in address['source_term'], '任事地須有來源職位及原地名，不作居所')
                if address['relation'] == 'polity_lineage_affiliation':
                    check(address.get('qualifiers', {}).get('affiliation_kind') == 'royal_lineage'
                          and address['place']['source_name']+'之' in address['source_term']
                          and re.search('公子|公孫|宗室', address['source_term']) is not None, '宗族政體地望須有來源身份詞，不改作出生籍貫')
                if address['relation'] == 'ancestral_origin':
                    scope = address.get('qualifiers', {})
                    check(scope.get('subject_scope') == 'ancestors_unspecified'
                          and scope.get('ancestor_person_id') is None
                          and scope.get('generation_distance') is None, '祖先出身不得暗補具名祖先或世代，須明示範圍')
                check(bool(address['place']['source_name']) and bool(address['evidence']), '地址原地名或證據缺失')
                if 'normalized_date' in address:
                    date = address['normalized_date']
                    errors.extend(normalized_date_errors(date, chapters, root=root))
                    if isinstance(date, dict):
                        for evidence in date.get('evidence', []):
                            hit = paragraphs.get(evidence['paragraph_id'])
                            valid = bool(hit) and hit[0] == evidence['chapter_id']
                            check(valid and evidence['quote'] in hit[1]['text'], '紀年換算證據篇段不符')
                            if valid: check(chapters[hit[0]]['source_id'] == evidence['source_id'], '紀年換算來源 ID 不符')
                        check(any(date.get('original_quote') in e['quote'] for e in date.get('evidence', [])), '紀年換算原句未見於證據')
                for evidence in address['evidence']:
                    hit = paragraphs.get(evidence['paragraph_id'])
                    valid = bool(hit) and hit[0] == record['chapter_id'] == evidence['chapter_id']
                    check(valid and evidence['quote'] in hit[1]['text'], '地址證據篇段不符')
                    if valid:
                        check(address['place']['source_name'] in evidence['quote'] and address['source_term'] in evidence['quote'], '地址原詞不在證據')
                        check(address['date_expression'] is None or address['date_expression'] in evidence['quote'], '地址日期不在證據')
                        context = evidence.get('context'); carried = False
                        if context is not None:
                            previous = paragraphs.get(context.get('paragraph_id')) if isinstance(context, dict) else None
                            anchor = mentions.get(context.get('person_mention_id')) if isinstance(context, dict) else None
                            order = [p['id'] for p in chapters[record['chapter_id']]['paragraphs']]
                            quote = context.get('quote') if isinstance(context, dict) else None
                            ids = context.get('intervening_paragraph_ids') if isinstance(context, dict) else None
                            adjacent = (isinstance(context, dict)
                                and set(context) == {'kind', 'paragraph_id', 'person_mention_id', 'quote'}
                                and context.get('kind') == 'previous_paragraph_subject'
                                and bool(previous) and context['paragraph_id'] in order
                                and order.index(evidence['paragraph_id']) == order.index(context['paragraph_id']) + 1)
                            continuous = (isinstance(context, dict)
                                and set(context) == {'kind', 'paragraph_id', 'person_mention_id', 'quote', 'intervening_paragraph_ids'}
                                and context.get('kind') == 'prior_paragraph_subject' and bool(previous)
                                and context['paragraph_id'] in order and isinstance(ids, list)
                                and order.index(context['paragraph_id']) < order.index(evidence['paragraph_id'])
                                and ids == order[order.index(context['paragraph_id']) + 1:order.index(evidence['paragraph_id'])])
                            carried = ((adjacent or continuous) and bool(anchor)
                                and previous[0] == record['chapter_id']
                                and anchor[1] == context['paragraph_id'] and anchor[2]['person_id'] == address['person_id']
                                and isinstance(quote, str) and bool(quote) and quote in previous[1]['text']
                                and any(i <= anchor[2]['start'] and anchor[2]['end'] <= i + len(quote)
                                        for i in range(len(previous[1]['text'])) if previous[1]['text'].startswith(quote, i))
                                and bool(address.get('interpretation_note')))
                            check(carried, '地址主語承接須有同篇人物錨點、引句及完整中間段落')
                        check(carried or any(m.get('person_id') == address['person_id'] for m in hit[1]['mentions']), '地址人物未見於證據段')
                        check(chapters[hit[0]]['source_id'] == evidence['source_id'], '地址來源 ID 不符')
        life_event_ids = set()
        for path in list((root / 'corpus').glob('*/*-life-events.json')) + list((root / 'corpus').glob('*/*-person-events.json')):
            record = json.loads(path.read_text(encoding='utf-8'))
            if record.get('record_type') == 'table_person_life_event_assertion_set':
                try:
                    from scripts.table_life_events import native_death_errors
                except ImportError:
                    from table_life_events import native_death_errors
                for event in record['events']:
                    check(event['id'] not in life_event_ids, '生卒事件ID重複'); life_event_ids.add(event['id'])
                    check('chinese_civil_year' not in event, '年表原生事件尚不支援段落型中文紀年證據；不可略過驗證')
                    errors.extend(native_death_errors(record, event, tables, pids))
                continue
            check(record.get('record_type') in ('person_life_event_assertion_set', 'person_event_assertion_set') and record.get('chapter_id') in chapters, '生卒事件集類型或篇不存在')
            if record.get('chapter_id') == 'c-songshu-044-wyd1739-xiehui' and record.get('record_type') == 'person_life_event_assertion_set':
                try:from scripts.wyd_song044_life import valid as wyd_life_valid
                except ImportError:from wyd_song044_life import valid as wyd_life_valid
                check(wyd_life_valid(record,root),'武英殿謝晦篇死亡須依具名列舉、主語承接及同段原免，不借日期或刪矛盾')
            if record['chapter_id'] in chapters:
                try: from scripts.liang033_wangyun_witness import side_errors as liang33_side_errors
                except ImportError: from liang033_wangyun_witness import side_errors as liang33_side_errors
                errors.extend(liang33_side_errors(record, chapters[record['chapter_id']], root, 'events'))
            if record['chapter_id'] in chapters:
                try: from scripts.liang021_wangtai_readings import side_errors as tai21_side_errors
                except ImportError: from liang021_wangtai_readings import side_errors as tai21_side_errors
                errors.extend(tai21_side_errors(record,chapters[record['chapter_id']],root,'events'))
            if record['chapter_id'] in chapters:
                try: from scripts.liang021_wangjun import side_errors as j21_side_errors
                except ImportError: from liang021_wangjun import side_errors as j21_side_errors
                errors.extend(j21_side_errors(record,chapters[record['chapter_id']],root,'events'))
            if record['chapter_id'] in chapters:
                try: from scripts.liang021_wangfen_family import side_errors as wf21_side_errors
                except ImportError: from liang021_wangfen_family import side_errors as wf21_side_errors
                errors.extend(wf21_side_errors(record,chapters[record['chapter_id']],root,'events'))
            if record['chapter_id'] in chapters:
                try: from scripts.liang021_wangxun import side_errors as xun21_side_errors
                except ImportError: from liang021_wangxun import side_errors as xun21_side_errors
                errors.extend(xun21_side_errors(record,chapters[record['chapter_id']],root,'events'))
            if record['chapter_id'] in chapters:
                try: from scripts.liang021_wangjiansihui import side_errors as sih21_side_errors
                except ImportError: from liang021_wangjiansihui import side_errors as sih21_side_errors
                errors.extend(sih21_side_errors(record,chapters[record['chapter_id']],root,'events'))
            if record['chapter_id'] in chapters:
                try: from scripts.song052_xiechun import side_errors as chun52_side_errors
                except ImportError: from song052_xiechun import side_errors as chun52_side_errors
                errors.extend(chun52_side_errors(record,chapters[record['chapter_id']],root,'events'))
            if record['chapter_id'] in chapters:
                try: from scripts.song052_xiejingren import side_errors as xiejingren52_side_errors
                except ImportError: from song052_xiejingren import side_errors as xiejingren52_side_errors
                errors.extend(xiejingren52_side_errors(record,chapters[record['chapter_id']],root,'events'))
            if record['chapter_id'] in chapters:
                try: from scripts.nan023_digital import side_errors as nan23dan_side_errors
                except ImportError: from nan023_digital import side_errors as nan23dan_side_errors
                errors.extend(nan23dan_side_errors(record,chapters[record['chapter_id']],root,'events'))
            if record['chapter_id'] in chapters:
                try: from scripts.song052_wangdan import side_errors as wangdan52_side_errors
                except ImportError: from song052_wangdan import side_errors as wangdan52_side_errors
                errors.extend(wangdan52_side_errors(record,chapters[record['chapter_id']],root,'events'))
            if record['chapter_id'] in chapters:
                try: from scripts.song052_xieshu import side_errors as xieshu52_side_errors
                except ImportError: from song052_xieshu import side_errors as xieshu52_side_errors
                errors.extend(xieshu52_side_errors(record,chapters[record['chapter_id']],root,'events'))
            if record['chapter_id'] in chapters:
                try: from scripts.nan023_print import side_errors as nan23p_side_errors
                except ImportError: from nan023_print import side_errors as nan23p_side_errors
                errors.extend(nan23p_side_errors(record,chapters[record['chapter_id']],root,'events'))
            if record['chapter_id'] in chapters:
                try: from scripts.nan023_wangmao import side_errors as nan23mao_side_errors
                except ImportError: from nan023_wangmao import side_errors as nan23mao_side_errors
                errors.extend(nan23mao_side_errors(record,chapters[record['chapter_id']],root,'events'))
            if record['chapter_id'] in chapters:
                try: from scripts.nan023_jiangxiao import side_errors as nan23jiang_side_errors
                except ImportError: from nan023_jiangxiao import side_errors as nan23jiang_side_errors
                errors.extend(nan23jiang_side_errors(record,chapters[record['chapter_id']],root,'events'))
            if record['chapter_id'] in chapters:
                try: from scripts.nan023_chuai import side_errors as nan23chuai_side_errors
                except ImportError: from nan023_chuai import side_errors as nan23chuai_side_errors
                errors.extend(nan23chuai_side_errors(record,chapters[record['chapter_id']],root,'events'))
            if record['chapter_id'] in chapters:
                try: from scripts.nan023_heyu import side_errors as nan23heyu_side_errors
                except ImportError: from nan023_heyu import side_errors as nan23heyu_side_errors
                errors.extend(nan23heyu_side_errors(record,chapters[record['chapter_id']],root,'events'))
            if record['chapter_id'] in chapters:
                try: from scripts.nan023_wangzao import side_errors as nan23zao_side_errors
                except ImportError: from nan023_wangzao import side_errors as nan23zao_side_errors
                errors.extend(nan23zao_side_errors(record,chapters[record['chapter_id']],root,'events'))
            if record['chapter_id'] in chapters:
                try: from scripts.nan023_wangliang import side_errors as nan23liang_side_errors
                except ImportError: from nan023_wangliang import side_errors as nan23liang_side_errors
                errors.extend(nan23liang_side_errors(record,chapters[record['chapter_id']],root,'events'))
            if record['chapter_id'] in chapters:
                try: from scripts.nan023_wangying import side_errors as nan23ying_side_errors
                except ImportError: from nan023_wangying import side_errors as nan23ying_side_errors
                errors.extend(nan23ying_side_errors(record,chapters[record['chapter_id']],root,'events'))
            if record['chapter_id'] in chapters:
                try: from scripts.nan023_wanghui import side_errors as nan23hui_side_errors
                except ImportError: from nan023_wanghui import side_errors as nan23hui_side_errors
                errors.extend(nan23hui_side_errors(record,chapters[record['chapter_id']],root,'events'))
            if record['chapter_id'] in chapters:
                try: from scripts.nan023_wangqiu import side_errors as nan23qiu_side_errors
                except ImportError: from nan023_wangqiu import side_errors as nan23qiu_side_errors
                errors.extend(nan23qiu_side_errors(record,chapters[record['chapter_id']],root,'events'))
            if record['chapter_id'] in chapters:
                try: from scripts.nan023_wangxuan import side_errors as nan23xuan_side_errors
                except ImportError: from nan023_wangxuan import side_errors as nan23xuan_side_errors
                errors.extend(nan23xuan_side_errors(record,chapters[record['chapter_id']],root,'events'))
            if record['chapter_id'] in chapters:
                try: from scripts.nan023_wanghui_sons import side_errors as nan23huiz_side_errors
                except ImportError: from nan023_wanghui_sons import side_errors as nan23huiz_side_errors
                errors.extend(nan23huiz_side_errors(record,chapters[record['chapter_id']],root,'events'))
            if record['chapter_id'] in chapters:
                try: from scripts.nan023_chuzhanzhi import side_errors as nan23chu_side_errors
                except ImportError: from nan023_chuzhanzhi import side_errors as nan23chu_side_errors
                errors.extend(nan23chu_side_errors(record,chapters[record['chapter_id']],root,'events'))
            if record['chapter_id'] in chapters:
                try: from scripts.nan023_wangyun import side_errors as nan23yun_side_errors
                except ImportError: from nan023_wangyun import side_errors as nan23yun_side_errors
                errors.extend(nan23yun_side_errors(record,chapters[record['chapter_id']],root,'events'))
            if record['chapter_id'] in chapters:
                try: from scripts.nan023_wanghuan import side_errors as nan23huan_side_errors
                except ImportError: from nan023_wanghuan import side_errors as nan23huan_side_errors
                errors.extend(nan23huan_side_errors(record,chapters[record['chapter_id']],root,'events'))
            if record['chapter_id'] in chapters:
                try: from scripts.nan023_wangxi import side_errors as nan23xi_side_errors
                except ImportError: from nan023_wangxi import side_errors as nan23xi_side_errors
                errors.extend(nan23xi_side_errors(record,chapters[record['chapter_id']],root,'events'))
            if record['chapter_id'] in chapters:
                try: from scripts.nan023_wangfen import side_errors as nan23fen_side_errors
                except ImportError: from nan023_wangfen import side_errors as nan23fen_side_errors
                errors.extend(nan23fen_side_errors(record,chapters[record['chapter_id']],root,'events'))
            if record['chapter_id'] in chapters:
                try: from scripts.nan023_wangtong import side_errors as nan23tong_side_errors
                except ImportError: from nan023_wangtong import side_errors as nan23tong_side_errors
                errors.extend(nan23tong_side_errors(record,chapters[record['chapter_id']],root,'events'))
            if record['chapter_id'] in chapters:
                try: from scripts.nan023_wangmai import side_errors as nan23mai_side_errors
                except ImportError: from nan023_wangmai import side_errors as nan23mai_side_errors
                errors.extend(nan23mai_side_errors(record,chapters[record['chapter_id']],root,'events'))
            if record['chapter_id'] in chapters:
                try: from scripts.nan023_wangzhi import side_errors as nan23zhi_side_errors
                except ImportError: from nan023_wangzhi import side_errors as nan23zhi_side_errors
                errors.extend(nan23zhi_side_errors(record,chapters[record['chapter_id']],root,'events'))
            if record['chapter_id'] in chapters:
                try: from scripts.nan023_wanggu import side_errors as nan23gu_side_errors
                except ImportError: from nan023_wanggu import side_errors as nan23gu_side_errors
                errors.extend(nan23gu_side_errors(record,chapters[record['chapter_id']],root,'events'))
            if record['chapter_id'] in chapters:
                try: from scripts.nan023_wanghou import side_errors as nan23hou_side_errors
                except ImportError: from nan023_wanghou import side_errors as nan23hou_side_errors
                errors.extend(nan23hou_side_errors(record,chapters[record['chapter_id']],root,'events'))
            if record['chapter_id'] in chapters:
                try: from scripts.nan023_wangyu import side_errors as nan23yu_side_errors
                except ImportError: from nan023_wangyu import side_errors as nan23yu_side_errors
                errors.extend(nan23yu_side_errors(record,chapters[record['chapter_id']],root,'events'))
            if record['chapter_id'] in chapters:
                try: from scripts.nanqi047_wangrong import side_errors as qi47rong_side_errors
                except ImportError: from nanqi047_wangrong import side_errors as qi47rong_side_errors
                errors.extend(qi47rong_side_errors(record,chapters[record['chapter_id']],root,'events'))
            if record['chapter_id'] in chapters:
                try: from scripts.liang033_wangsengru import side_errors as liang33sr_side_errors
                except ImportError: from liang033_wangsengru import side_errors as liang33sr_side_errors
                errors.extend(liang33sr_side_errors(record,chapters[record['chapter_id']],root,'events'))
            if record['chapter_id'] in chapters:
                try: from scripts.nanshi059_wangsengru import side_errors as nan59sr_side_errors
                except ImportError: from nanshi059_wangsengru import side_errors as nan59sr_side_errors
                errors.extend(nan59sr_side_errors(record,chapters[record['chapter_id']],root,'events'))
            if record['chapter_id'] in chapters:
                try: from scripts.nanqi047_wangrong_wyd import side_errors as q47wyd_sides
                except ImportError: from nanqi047_wangrong_wyd import side_errors as q47wyd_sides
                errors.extend(q47wyd_sides(record,chapters[record['chapter_id']],root,'events'))
            if record['chapter_id'] in chapters:
                try: from scripts.nanshi024_wangshaozhi import side_errors as nan24sz_side_errors
                except ImportError: from nanshi024_wangshaozhi import side_errors as nan24sz_side_errors
                errors.extend(nan24sz_side_errors(record,chapters[record['chapter_id']],root,'events'))
            if record['chapter_id'] in chapters:
                try: from scripts.nanshi024_wangshaozhi_wyd import side_errors as n24szwyd_sides
                except ImportError: from nanshi024_wangshaozhi_wyd import side_errors as n24szwyd_sides
                errors.extend(n24szwyd_sides(record,chapters[record['chapter_id']],root,'events'))
            if record['chapter_id'] in chapters:
                try: from scripts.nanshi024_wangyuezhi import side_errors as nan24yz_side_errors
                except ImportError: from nanshi024_wangyuezhi import side_errors as nan24yz_side_errors
                errors.extend(nan24yz_side_errors(record,chapters[record['chapter_id']],root,'events'))
            if record['chapter_id'] in chapters:
                try: from scripts.nanshi024_wangzhunzhi import side_errors as nan24zz_side_errors
                except ImportError: from nanshi024_wangzhunzhi import side_errors as nan24zz_side_errors
                errors.extend(nan24zz_side_errors(record,chapters[record['chapter_id']],root,'events'))
            if record['chapter_id'] in chapters:
                try: from scripts.nanshi024_wangjinzhi import side_errors as nan24jz_side_errors
                except ImportError: from nanshi024_wangjinzhi import side_errors as nan24jz_side_errors
                errors.extend(nan24jz_side_errors(record,chapters[record['chapter_id']],root,'events'))
            if record['chapter_id'] in chapters:
                try: from scripts.nanshi024_wangqing import side_errors as nan24qing_side_errors
                except ImportError: from nanshi024_wangqing import side_errors as nan24qing_side_errors
                errors.extend(nan24qing_side_errors(record,chapters[record['chapter_id']],root,'events'))
            if record['chapter_id'] in chapters:
                try: from scripts.nanshi024_wangqunzhi import side_errors as nan24qun_side_errors
                except ImportError: from nanshi024_wangqunzhi import side_errors as nan24qun_side_errors
                errors.extend(nan24qun_side_errors(record,chapters[record['chapter_id']],root,'events'))
            if record['chapter_id'] in chapters:
                try: from scripts.nanshi024_wangsu import side_errors as nan24su_side_errors
                except ImportError: from nanshi024_wangsu import side_errors as nan24su_side_errors
                errors.extend(nan24su_side_errors(record,chapters[record['chapter_id']],root,'events'))
            if record['chapter_id'] in chapters:
                try: from scripts.nanshi024_ruanwanling import side_errors as nan24rw_side_errors
                except ImportError: from nanshi024_ruanwanling import side_errors as nan24rw_side_errors
                errors.extend(nan24rw_side_errors(record,chapters[record['chapter_id']],root,'events'))
            if record['chapter_id'] in chapters:
                try: from scripts.nanshi024_wanghongzhi import side_errors as n24hong_sides
                except ImportError: from nanshi024_wanghongzhi import side_errors as n24hong_sides
                errors.extend(n24hong_sides(record,chapters[record['chapter_id']],root,'events'))
            if record['chapter_id'] in chapters:
                try: from scripts.song093_wanghongzhi import side_errors as hongzhi_sides
                except ImportError: from song093_wanghongzhi import side_errors as hongzhi_sides
                errors.extend(hongzhi_sides(record,chapters[record['chapter_id']],root,'events'))
            if record['chapter_id'] in chapters:
                try: from scripts.song093_wyd import side_errors as s93wyd_sides
                except ImportError: from song093_wyd import side_errors as s93wyd_sides
                errors.extend(s93wyd_sides(record,chapters[record['chapter_id']],root,'events'))
            if record['chapter_id'] in chapters:
                try: from scripts.nanshi024_wangmeng import side_errors as nan24meng_side_errors
                except ImportError: from nanshi024_wangmeng import side_errors as nan24meng_side_errors
                errors.extend(nan24meng_side_errors(record,chapters[record['chapter_id']],root,'events'))
            if record['chapter_id'] in chapters:
                try: from scripts.xiangshan_m9_epitaphs import side_errors as xm9_side_errors
                except ImportError: from xiangshan_m9_epitaphs import side_errors as xm9_side_errors
                errors.extend(xm9_side_errors(record,chapters[record['chapter_id']],root,'events'))
            if record['chapter_id'] in chapters:
                try: from scripts.nanshi024_wangyan import side_errors as nan24yan_side_errors
                except ImportError: from nanshi024_wangyan import side_errors as nan24yan_side_errors
                errors.extend(nan24yan_side_errors(record,chapters[record['chapter_id']],root,'events'))
            if record['chapter_id'] in chapters:
                try: from scripts.nanshi024_wangyan_brothers import side_errors as nan24wab_side_errors
                except ImportError: from nanshi024_wangyan_brothers import side_errors as nan24wab_side_errors
                errors.extend(nan24wab_side_errors(record,chapters[record['chapter_id']],root,'events'))
            if record['chapter_id'] in chapters:
                try: from scripts.nanshi024_guhaozhi import side_errors as nan24gh_side_errors
                except ImportError: from nanshi024_guhaozhi import side_errors as nan24gh_side_errors
                errors.extend(nan24gh_side_errors(record,chapters[record['chapter_id']],root,'events'))
            if record['chapter_id'] in chapters:
                try: from scripts.nanshi024_wangsiyuan import side_errors as nan24siy_side_errors
                except ImportError: from nanshi024_wangsiyuan import side_errors as nan24siy_side_errors
                errors.extend(nan24siy_side_errors(record,chapters[record['chapter_id']],root,'events'))
            for event in record['events']:
                check(event['id'] not in life_event_ids, '生卒事件ID重複'); life_event_ids.add(event['id'])
                check(event['person_id'] in pids and event['event_type'] in (('birth', 'death') if record.get('record_type') == 'person_life_event_assertion_set' else ('recruitment', 'burial', 'office_non_reinstatement', 'office_restoration', 'diplomatic_service', 'noble_state_abolition', 'noble_title_succession', 'noble_title_restoration')), '生卒事件人物或類型無效')
                check(event.get('status') == 'source_attested' and bool(event.get('evidence')) and bool(event.get('interpretation_note')) and bool(event.get('reviewer')) and event.get('human_reviewed') is False, '生卒事件缺少來源或判讀')
                if 'received_source_frame' in event:
                    try:from scripts.fixed_received_career import nonholding_valid
                    except ImportError:from fixed_received_career import nonholding_valid
                    role='life'if record['record_type']=='person_life_event_assertion_set'else'succession'
                    check(nonholding_valid(event,chapters[record['chapter_id']],root,role),'固定收到生命或承爵事件須綁實際角色，不借他人日期或爵名')
                if event.get('source_death_context',{}).get('kind')=='punctuated_biography_death_report':
                    try:from scripts.punctuated_biography_career import death_valid
                    except ImportError:from punctuated_biography_career import death_valid
                    check(death_valid(event,chapters[record['chapter_id']]), '死亡主體/完整疾病施賜與紀年或後誅原句不符，不借他人年份')
                if 'source_layered_death_report' in event:
                    try:from scripts.layered_biography_titles import explicit_death_report_valid
                    except ImportError:from layered_biography_titles import explicit_death_report_valid
                    check(explicit_death_report_valid(event,chapters[record['chapter_id']]),'明示死亡須綁實際主體與完整死因句，不移給引述/夢中他人或補年月')
                if 'literal_source_binding' in event:
                    try:
                        from scripts.literal_family_reports import death_valid
                    except ImportError:
                        from literal_family_reports import death_valid
                    check(death_valid(event, paragraphs, chapters, root), '死亡敘述須綁主語、原紀年與推薦/召任其他角色，不以鄰名或任終代替')
                if 'reported_reign_interval' in event:
                    try:
                        from scripts.regnal_relationships import accession_death_interval_valid
                    except ModuleNotFoundError:
                        from regnal_relationships import accession_death_interval_valid
                    check(accession_death_interval_valid(event, paragraphs, mentions), '未逾年須連同人立後死亡的原句，不得當生齡或推曆年')
                if record.get('record_type') == 'person_event_assertion_set' and event['event_type'] == 'recruitment':
                    check(any('徵' in e.get('quote', '') for e in event.get('evidence', [])), '徵召事件缺少原文徵召用語')
                if event['event_type'] == 'noble_title_restoration':
                    context = event.get('restoration_context', {})
                    required_unknowns = (
                        (event, ('date_expression', 'title', 'holding_id')),
                        (context, ('petitioning_person_id',)),
                    )
                    check(all(all(key in item and item[key] is None for key in keys)
                              for item, keys in required_unknowns)
                          and 'normalized_date' not in event and 'normalized_date_range' not in event
                          and context.get('restoration_date_status') == 'not_stated',
                          '無明載的復爵日期、施請人及本句爵名須留空')
                    check(event.get('event_group_id') and context.get('petitioning_title') == '齊王'
                          and context.get('result') == 'pardon_and_restoration_of_rank_and_fief'
                          and context.get('contextual_title_status') == 'paternal_line_context'
                          and event.get('source_term') in ('乃啟原之，復其爵土', '乃啓原之復其爵土')
                          and any(event.get('source_term', '\0') in e.get('quote', '')
                                  and '齊王' in e['quote'] for e in event['evidence']),
                          '復爵土須有齊王奏請及原之、復爵土原詞')
                    for key in ('case_evidence', 'collateral_case_evidence', 'paternal_title_evidence'):
                        ref = context.get(key, {})
                        hit = paragraphs.get(ref.get('paragraph_id'))
                        witness = chapters.get(ref.get('chapter_id'), {})
                        check(bool(hit) and hit[0] == ref.get('chapter_id')
                              and all(ref.get(k) == witness.get(k) for k in ('work_id', 'book_id', 'source_id'))
                              and bool(ref.get('quote')) and ref['quote'] in hit[1]['text'],
                              '復爵土須保留元瑾案及父爵各自的原文和見證位置')
                    title_ref = context.get('paternal_title_evidence', {})
                    title_mention = mentions.get(title_ref.get('person_mention_id'))
                    predecessor = context.get('predecessor_person_id')
                    title = context.get('contextual_title')
                    check(bool(title_mention) and title_mention[1] == title_ref.get('paragraph_id')
                          and title_mention[2]['person_id'] == predecessor
                          and isinstance(title, str) and title.endswith('王')
                          and title_mention[2]['surface'].startswith(title[:-1])
                          and title_mention[2]['surface'].endswith('王')
                          and any(a['predicate'] == 'father' and a['subject_person_id'] == event['person_id']
                                  and a['object_person_id'] == predecessor for a in family_relations),
                          '復爵的家系爵名須綁同一生父及其具名爵號證據')
                    check('合門伏法' in context.get('case_evidence', {}).get('quote', '')
                          and '法輪坐叔父瑾' in context.get('collateral_case_evidence', {}).get('quote', ''),
                          '復爵土的案件語境須繫於法輪坐叔父案')
                if event['event_type'] in ('noble_state_abolition', 'noble_title_succession'):
                    try:
                        from scripts.noble_state_abolition import valid as noble_abolition_valid
                    except ImportError:
                        from noble_state_abolition import valid as noble_abolition_valid
                    if 'source_career_role' in event:
                        try:
                            from scripts.received_career_roles import event_valid as career_event_valid
                        except ImportError:
                            from received_career_roles import event_valid as career_event_valid
                        noble_valid = career_event_valid(event, chapters[event['evidence'][0]['chapter_id']])
                    else:
                        noble_valid = noble_abolition_valid(event, paragraphs)
                    if 'received_source_frame' in event:
                        try:from scripts.fixed_received_career import nonholding_valid
                        except ImportError:from fixed_received_career import nonholding_valid
                        noble_valid=nonholding_valid(event,chapters[record['chapter_id']],root,'succession')
                    check(noble_valid, '承爵與國除須綁完整承嗣句的明示端點，不補爵名、前任或日期')
                if event['event_type'] == 'diplomatic_service':
                    duration = event.get('reported_duration', {}); number = duration.get('source_number')
                    place = event.get('polity_source_name'); term = duration.get('source_term')
                    check(isinstance(place, str) and bool(place) and isinstance(number, str)
                          and type(duration.get('value')) is int and duration['value'] > 0
                          and source_age_number(number) == duration['value']
                          and duration.get('unit') == 'service_year'
                          and duration.get('counting') == 'unspecified_source_years'
                          and duration.get('status') == 'source_attested'
                          and term == '事' + str(place) + str(number) + '年'
                          and term in event.get('source_term', '')
                          and duration.get('evidence') == event.get('evidence')
                          and any(event.get('source_term', '') in e.get('quote', '') for e in event.get('evidence', [])),
                          '使外任事年數須有事國原詞、相符數字及任務單位，不作爵位任期')
                if event['event_type'] == 'burial':
                    term = event.get('source_term')
                    check(isinstance(term, str) and ('葬' in term or term in ('窆', '卜窆'))
                          and any(term in e.get('quote', '') for e in event.get('evidence', [])),
                          '埋葬事件須有原文明示葬詞及相符引句')
                if event['event_type'] in ('office_non_reinstatement', 'office_restoration'):
                    term = event.get('source_term')
                    required = '不復官' if event['event_type'] == 'office_non_reinstatement' else '復就故官'
                    restoration = False
                    if event['event_type'] == 'office_restoration' and event.get('restoration_kind') == 'posthumous_restore_unnamed_office':
                        try:
                            from .jin_facts_boundaries import posthumous_restoration_valid
                        except ImportError:
                            from jin_facts_boundaries import posthumous_restoration_valid
                        restoration_deaths = {item['id']: item for life_path in (root / 'corpus').glob('*/*-life-events.json') for item in json.loads(life_path.read_text())['events']}
                        restoration = posthumous_restoration_valid(event, chapters, restoration_deaths)
                    check(isinstance(term, str) and (required in term or restoration)
                          and all(key in event and event[key] is None for key in ('office_title', 'title_holding_id'))
                          and any(term in e.get('quote', '') for e in event.get('evidence', [])),
                          '未名官職不復任或恢復須保留原詞，不得補官名或已知持職連結')
                if 'chinese_civil_year' in event:
                    try:
                        from scripts.chinese_civil_years import civil_year_errors
                    except ImportError:
                        from chinese_civil_years import civil_year_errors
                    errors.extend(civil_year_errors(event, chapters, tables))
                if 'source_date_parts' in event:
                    try:
                        from scripts.source_date_parts import source_date_parts_valid
                    except ImportError:
                        from source_date_parts import source_date_parts_valid
                    check(source_date_parts_valid(event, chapters, source_age_number, root=root), '原文明示曆月須有同死事件日期鏈與逐字月詞錨點，不得補日或西曆月')
                expression = event.get('date_expression')
                check(expression is None or isinstance(expression, str) and bool(expression), '生卒日期表述無效')
                local_death_date = False
                event_date = event.get('normalized_date')
                if isinstance(event_date, dict) and ('event_evidence_binding' in event_date or 'cross_chapter_event_binding' in event_date):
                    try:
                        from scripts.local_death_date_evidence import local_death_date_evidence_valid
                    except ImportError:
                        from local_death_date_evidence import local_death_date_evidence_valid
                    local_death_date = local_death_date_evidence_valid(event_date, event, chapters, source_age_number, root=root)
                    check(local_death_date, '局部死亡與完整紀年證據鏈須有同版同人同事件精確綁定')
                date_context = event.get('date_context')
                continuous_date = False
                if date_context is not None:
                    order = [p['id'] for p in chapters.get(record['chapter_id'], {}).get('paragraphs', [])]
                    ids = date_context.get('paragraph_ids') if isinstance(date_context, dict) else None
                    date_paragraph_id = (date_context.get('date_paragraph_id', ids[0] if isinstance(ids, list) and ids else None)
                                         if isinstance(date_context, dict) else None)
                    continuous_date = (isinstance(date_context, dict)
                        and date_context.get('kind') == 'continuous_paragraphs'
                        and isinstance(ids, list) and 2 <= len(ids) <= 4
                        and ids == [e['paragraph_id'] for e in event['evidence']]
                        and all(pid in order for pid in ids)
                        and all(order.index(ids[i]) + 1 == order.index(ids[i + 1]) for i in range(len(ids) - 1))
                        and isinstance(expression, str) and bool(expression)
                        and date_paragraph_id in ids
                        and expression in next((e['quote'] for e in event['evidence'] if e['paragraph_id'] == date_paragraph_id), '')
                        and bool(date_context.get('rationale')))
                    if isinstance(date_context, dict) and date_context.get('kind') == 'same_event_attestation':
                        primary = event['evidence'][0]
                        continuous_date = (set(date_context) == {'kind', 'paragraph_ids', 'date_paragraph_id', 'rationale'}
                            and isinstance(ids, list) and len(ids) >= 2 and len(set(ids)) == len(ids)
                            and ids == [e['paragraph_id'] for e in event['evidence']]
                            and all(pid in order for pid in ids)
                            and date_context.get('date_paragraph_id') == primary['paragraph_id']
                            and isinstance(expression, str) and bool(expression) and expression in primary['quote']
                            and bool(event.get('source_term')) and event['source_term'] in primary['quote']
                            and bool(date_context.get('rationale')))
                        check(continuous_date, '同一生卒事件回述須以首筆明示事件引句作紀年錨點')
                    else:
                        check(continuous_date, '生卒紀年承接須有連續同篇段落與明示日期段')
                for evidence in event['evidence']:
                    hit = paragraphs.get(evidence['paragraph_id']); mention = mentions.get(evidence.get('person_mention_id'))
                    valid = bool(hit) and hit[0] == evidence['chapter_id'] == record['chapter_id']
                    check(valid and evidence['quote'] in hit[1]['text'] and chapters.get(evidence['chapter_id'], {}).get('source_id') == evidence['source_id'], '生卒事件來源引句不符')
                    carried_subject = False
                    context = evidence.get('context')
                    if context is not None:
                        order = [p['id'] for p in chapters.get(record['chapter_id'], {}).get('paragraphs', [])]
                        previous = paragraphs.get(context.get('paragraph_id')) if isinstance(context, dict) else None
                        anchor = mentions.get(context.get('person_mention_id')) if isinstance(context, dict) else None
                        quote = context.get('quote') if isinstance(context, dict) else None
                        ids = context.get('intervening_paragraph_ids') if isinstance(context, dict) else None
                        carried_subject = (isinstance(context, dict) and set(context) == {'kind', 'paragraph_id', 'person_mention_id', 'quote', 'intervening_paragraph_ids'}
                            and context.get('kind') == 'prior_paragraph_subject' and bool(previous) and bool(anchor)
                            and bool(hit) and previous[0] == hit[0] == record['chapter_id']
                            and context['paragraph_id'] in order and evidence['paragraph_id'] in order
                            and isinstance(ids, list) and len(ids) <= 1
                            and order.index(evidence['paragraph_id']) - order.index(context['paragraph_id']) == len(ids) + 1
                            and ids == order[order.index(context['paragraph_id']) + 1:order.index(evidence['paragraph_id'])]
                            and anchor[1] == context['paragraph_id'] and anchor[2]['person_id'] == event['person_id']
                            and isinstance(quote, str) and bool(quote) and quote in previous[1]['text']
                            and any(i <= anchor[2]['start'] and anchor[2]['end'] <= i + len(quote)
                                    for i in range(len(previous[1]['text'])) if previous[1]['text'].startswith(quote, i))
                            and bool(event.get('source_term')) and event['source_term'] in evidence['quote'])
                        if isinstance(context, dict) and context.get('kind') == 'jin080_biography_end':
                            try: from scripts.jin080_xizhi import end_subject_valid
                            except ImportError: from jin080_xizhi import end_subject_valid
                            carried_subject = end_subject_valid(context, evidence, event['person_id'], chapters[record['chapter_id']])
                        if isinstance(context,dict) and context.get('kind')=='layered_biography_death_continuation':
                            try:from scripts.layered_biography_titles import death_context_valid
                            except ImportError:from layered_biography_titles import death_context_valid
                            carried_subject=death_context_valid(context,event,chapters[record['chapter_id']],evidence)
                        if isinstance(context,dict) and context.get('kind')=='liang033_sengru_resumed_biography':
                            try: from scripts.liang033_wangsengru import resumed_subject as sengru_resumed_subject
                            except ImportError: from liang033_wangsengru import resumed_subject as sengru_resumed_subject
                            carried_subject=sengru_resumed_subject(context,evidence,event['person_id'],chapters[record['chapter_id']])
                        check(carried_subject, '生卒主語承接須有近前同篇人物錨點、引句及完整中間段落')
                    if event['id'] in ('le-nanshi-011-peihuizhao-pei', 'le-nanqishu-020-peihuizhao-pei', 'le-nanqishu-002-peihuizhao-death-pei', 'le-nanshi-042-yuzhang-wangfei-yi', 'le-nanshi-042-yuzhang-wangfei-yu', 'le-songshu-052-yuantan-line-ji'):
                        try: from scripts.pei_royal_biographies import death_valid as pei_death_valid
                        except ImportError: from pei_royal_biographies import death_valid as pei_death_valid
                        carried_subject=pei_death_valid(event,evidence,chapters[record['chapter_id']],root)
                        check(carried_subject,'裴后及其親屬死亡字位與具名或稱謂原證不合')
                    if event['id'] in ('le-nanshi-022-wangjian-sengchuo', 'le-nanshi-022-wangjian-peihuizhao', 'le-nanshi-022-wangjian-taizu', 'le-nanshi-022-wangjian-jinming', 'le-nanshi-022-wangjian-jinjian', 'le-nanshi-022-wangjian-wangjian', 'le-nanshi-022-wangjian-wangxun', 'le-nanqishu-024-liushilong-wangjian-shuzong', 'le-houhanshu-052-cuiyuan-wangjian-cuiyin'):
                        try: from scripts.nanshi022_wangjian_source import death_valid as n22jian_death_valid
                        except ImportError: from nanshi022_wangjian_source import death_valid as n22jian_death_valid
                        carried_subject=n22jian_death_valid(event,evidence,chapters[record['chapter_id']],root)
                        check(carried_subject,'王儉傳及所引親屬生卒的原文字位不合')
                    if event['id'] == 'le-wyd-song063-wangtanshou':
                        try: from scripts.wyd_song063_wangtanshou import death_valid as wyd63_death_valid
                        except ImportError: from wyd_song063_wangtanshou import death_valid as wyd63_death_valid
                        carried_subject = wyd63_death_valid(event, evidence, chapters[record['chapter_id']], root)
                        check(carried_subject, '王曇首殿本卒年須合七年卒及賢者先殞兩處')
                    if event['id'].startswith('le-liang033-wangyun-'):
                        try: from scripts.liang033_wangyun_witness import death_valid as liang33_death_valid
                        except ImportError: from liang033_wangyun_witness import death_valid as liang33_death_valid
                        carried_subject=liang33_death_valid(event,evidence,chapters[record['chapter_id']],root)
                        check(carried_subject,'王筠、筠母與昭明太子的死詞須各核人及相承年號')
                    if event['id'].startswith('le-liang021-wangjun-'):
                        try: from scripts.liang021_wangjun import death_valid as j21_death_valid
                        except ImportError: from liang021_wangjun import death_valid as j21_death_valid
                        carried_subject=j21_death_valid(event,evidence,chapters[record['chapter_id']],root)
                        check(carried_subject,'王峻與其父之卒各繫本人')
                    if event['id'].startswith('le-liang021-wangfen-family-'):
                        try: from scripts.liang021_wangfen_family import death_valid as wf21_death_valid
                        except ImportError: from liang021_wangfen_family import death_valid as wf21_death_valid
                        carried_subject=wf21_death_valid(event,evidence,chapters[record['chapter_id']],root)
                        check(carried_subject,'王份家傳死詞各繫本人')
                    if event['id'].startswith('le-liang021-wangxun-'):
                        try: from scripts.liang021_wangxun import death_valid as xun21_death_valid
                        except ImportError: from liang021_wangxun import death_valid as xun21_death_valid
                        carried_subject=xun21_death_valid(event,evidence,chapters[record['chapter_id']],root)
                        check(carried_subject,'本傳諸卒各繫本人')
                    if event['id'].startswith('le-liang021-wangjiansihui-'):
                        try: from scripts.liang021_wangjiansihui import death_valid as sih21_death_valid
                        except ImportError: from liang021_wangjiansihui import death_valid as sih21_death_valid
                        carried_subject=sih21_death_valid(event,evidence,chapters[record['chapter_id']],root)
                        check(carried_subject,'本傳諸卒各繫本人')
                    if event['id'].startswith('le-song052-xiechun-'):
                        try: from scripts.song052_xiechun import death_valid as chun52_death_valid
                        except ImportError: from song052_xiechun import death_valid as chun52_death_valid
                        carried_subject=chun52_death_valid(event,evidence,chapters[record['chapter_id']],root)
                        check(carried_subject,'本傳諸卒各繫本人')
                    if event['id'].startswith('le-song052-xiejingren-'):
                        try: from scripts.song052_xiejingren import death_valid as xiejingren52_death_valid
                        except ImportError: from song052_xiejingren import death_valid as xiejingren52_death_valid
                        carried_subject=xiejingren52_death_valid(event,evidence,chapters[record['chapter_id']],root)
                        check(carried_subject,'本傳諸卒各繫本人')
                    if event['id'].startswith('le-nan023-digital-'):
                        try: from scripts.nan023_digital import death_valid as nan23dan_death_valid
                        except ImportError: from nan023_digital import death_valid as nan23dan_death_valid
                        carried_subject=nan23dan_death_valid(event,evidence,chapters[record['chapter_id']],root)
                        check(carried_subject,'本傳諸卒各繫本人')
                    if event['id'].startswith('le-song052-wangdan-'):
                        try: from scripts.song052_wangdan import death_valid as wangdan52_death_valid
                        except ImportError: from song052_wangdan import death_valid as wangdan52_death_valid
                        carried_subject=wangdan52_death_valid(event,evidence,chapters[record['chapter_id']],root)
                        check(carried_subject,'本傳諸卒各繫本人')
                    if event['id'].startswith('le-song052-xieshu-'):
                        try: from scripts.song052_xieshu import death_valid as xieshu52_death_valid
                        except ImportError: from song052_xieshu import death_valid as xieshu52_death_valid
                        carried_subject=xieshu52_death_valid(event,evidence,chapters[record['chapter_id']],root)
                        check(carried_subject,'本傳諸卒各繫本人')
                    if event['id'].startswith('le-nan023-print-'):
                        try: from scripts.nan023_print import death_valid as nan23p_death_valid
                        except ImportError: from nan023_print import death_valid as nan23p_death_valid
                        carried_subject=nan23p_death_valid(event,evidence,chapters[record['chapter_id']],root)
                        check(carried_subject,'本傳諸卒各繫本人')
                    if event['id'].startswith('le-nan023-wangmao-'):
                        try: from scripts.nan023_wangmao import death_valid as nan23mao_death_valid
                        except ImportError: from nan023_wangmao import death_valid as nan23mao_death_valid
                        carried_subject=nan23mao_death_valid(event,evidence,chapters[record['chapter_id']],root)
                        check(carried_subject,'本傳諸卒各繫本人')
                    if event['id'].startswith('le-nan023-jiangcontext-'):
                        try: from scripts.nan023_jiangxiao import death_valid as nan23jiang_death_valid
                        except ImportError: from nan023_jiangxiao import death_valid as nan23jiang_death_valid
                        carried_subject=nan23jiang_death_valid(event,evidence,chapters[record['chapter_id']],root)
                        check(carried_subject,'本傳諸卒各繫本人')
                    if event['id'].startswith('le-nan023-chuaicontext-'):
                        try: from scripts.nan023_chuai import death_valid as nan23chuai_death_valid
                        except ImportError: from nan023_chuai import death_valid as nan23chuai_death_valid
                        carried_subject=nan23chuai_death_valid(event,evidence,chapters[record['chapter_id']],root)
                        check(carried_subject,'本傳諸卒各繫本人')
                    if event['id'].startswith('le-nan023-heyucontext-'):
                        try: from scripts.nan023_heyu import death_valid as nan23heyu_death_valid
                        except ImportError: from nan023_heyu import death_valid as nan23heyu_death_valid
                        carried_subject=nan23heyu_death_valid(event,evidence,chapters[record['chapter_id']],root)
                        check(carried_subject,'本傳諸卒各繫本人')
                    if event['id'].startswith('le-nan023-wangzao-'):
                        try: from scripts.nan023_wangzao import death_valid as nan23zao_death_valid
                        except ImportError: from nan023_wangzao import death_valid as nan23zao_death_valid
                        carried_subject=nan23zao_death_valid(event,evidence,chapters[record['chapter_id']],root)
                        check(carried_subject,'本傳諸卒各繫本人')
                    if event['id'].startswith('le-nan023-wangliang-'):
                        try: from scripts.nan023_wangliang import death_valid as nan23liang_death_valid
                        except ImportError: from nan023_wangliang import death_valid as nan23liang_death_valid
                        carried_subject=nan23liang_death_valid(event,evidence,chapters[record['chapter_id']],root)
                        check(carried_subject,'本傳諸卒各繫本人')
                    if event['id'].startswith('le-nan023-wangying-'):
                        try: from scripts.nan023_wangying import death_valid as nan23ying_death_valid
                        except ImportError: from nan023_wangying import death_valid as nan23ying_death_valid
                        carried_subject=nan23ying_death_valid(event,evidence,chapters[record['chapter_id']],root)
                        check(carried_subject,'本傳諸卒各繫本人')
                    if event['id'].startswith('le-nan023-wanghui-'):
                        try: from scripts.nan023_wanghui import death_valid as nan23hui_death_valid
                        except ImportError: from nan023_wanghui import death_valid as nan23hui_death_valid
                        carried_subject=nan23hui_death_valid(event,evidence,chapters[record['chapter_id']],root)
                        check(carried_subject,'本傳諸卒各繫本人')
                    if event['id'].startswith('le-nan023-wangqiu-'):
                        try: from scripts.nan023_wangqiu import death_valid as nan23qiu_death_valid
                        except ImportError: from nan023_wangqiu import death_valid as nan23qiu_death_valid
                        carried_subject=nan23qiu_death_valid(event,evidence,chapters[record['chapter_id']],root)
                        check(carried_subject,'本傳諸卒各繫本人')
                    if event['id'].startswith('le-nan023-wangxuan-'):
                        try: from scripts.nan023_wangxuan import death_valid as nan23xuan_death_valid
                        except ImportError: from nan023_wangxuan import death_valid as nan23xuan_death_valid
                        carried_subject=nan23xuan_death_valid(event,evidence,chapters[record['chapter_id']],root)
                        check(carried_subject,'本傳諸卒各繫本人')
                    if event['id'].startswith('le-nan023-wanghui_sons-'):
                        try: from scripts.nan023_wanghui_sons import death_valid as nan23huiz_death_valid
                        except ImportError: from nan023_wanghui_sons import death_valid as nan23huiz_death_valid
                        carried_subject=nan23huiz_death_valid(event,evidence,chapters[record['chapter_id']],root)
                        check(carried_subject,'本傳諸卒各繫本人')
                    if event['id'].startswith('le-nan023-chuzhanzhi-'):
                        try: from scripts.nan023_chuzhanzhi import death_valid as nan23chu_death_valid
                        except ImportError: from nan023_chuzhanzhi import death_valid as nan23chu_death_valid
                        carried_subject=nan23chu_death_valid(event,evidence,chapters[record['chapter_id']],root)
                        check(carried_subject,'本傳諸卒各繫本人')
                    if event['id'].startswith('le-nan023-wangyun-'):
                        try: from scripts.nan023_wangyun import death_valid as nan23yun_death_valid
                        except ImportError: from nan023_wangyun import death_valid as nan23yun_death_valid
                        carried_subject=nan23yun_death_valid(event,evidence,chapters[record['chapter_id']],root)
                        check(carried_subject,'本傳諸卒各繫本人')
                    if event['id'].startswith('le-nan023-wanghuan-'):
                        try: from scripts.nan023_wanghuan import death_valid as nan23huan_death_valid
                        except ImportError: from nan023_wanghuan import death_valid as nan23huan_death_valid
                        carried_subject=nan23huan_death_valid(event,evidence,chapters[record['chapter_id']],root)
                        check(carried_subject,'本傳諸卒各繫本人')
                    if event['id'].startswith('le-nan023-wangxi-'):
                        try: from scripts.nan023_wangxi import death_valid as nan23xi_death_valid
                        except ImportError: from nan023_wangxi import death_valid as nan23xi_death_valid
                        carried_subject=nan23xi_death_valid(event,evidence,chapters[record['chapter_id']],root)
                        check(carried_subject,'本傳諸卒各繫本人')
                    if event['id'].startswith('le-nan023-wangfen-'):
                        try: from scripts.nan023_wangfen import death_valid as nan23fen_death_valid
                        except ImportError: from nan023_wangfen import death_valid as nan23fen_death_valid
                        carried_subject=nan23fen_death_valid(event,evidence,chapters[record['chapter_id']],root)
                        check(carried_subject,'本傳諸卒各繫本人')
                    if event['id'].startswith('le-nan023-wangtong-'):
                        try: from scripts.nan023_wangtong import death_valid as nan23tong_death_valid
                        except ImportError: from nan023_wangtong import death_valid as nan23tong_death_valid
                        carried_subject=nan23tong_death_valid(event,evidence,chapters[record['chapter_id']],root)
                        check(carried_subject,'本傳諸卒各繫本人')
                    if event['id'].startswith('le-nan023-wangmai-'):
                        try: from scripts.nan023_wangmai import death_valid as nan23mai_death_valid
                        except ImportError: from nan023_wangmai import death_valid as nan23mai_death_valid
                        carried_subject=nan23mai_death_valid(event,evidence,chapters[record['chapter_id']],root)
                        check(carried_subject,'本傳諸卒各繫本人')
                    if event['id'].startswith('le-nan023-wangzhi-'):
                        try: from scripts.nan023_wangzhi import death_valid as nan23zhi_death_valid
                        except ImportError: from nan023_wangzhi import death_valid as nan23zhi_death_valid
                        carried_subject=nan23zhi_death_valid(event,evidence,chapters[record['chapter_id']],root)
                        check(carried_subject,'本傳諸卒各繫本人')
                    if event['id'].startswith('le-nan023-wanggu-'):
                        try: from scripts.nan023_wanggu import death_valid as nan23gu_death_valid
                        except ImportError: from nan023_wanggu import death_valid as nan23gu_death_valid
                        carried_subject=nan23gu_death_valid(event,evidence,chapters[record['chapter_id']],root)
                        check(carried_subject,'本傳諸卒各繫本人')
                    if event['id'].startswith('le-nan023-wanghou-'):
                        try: from scripts.nan023_wanghou import death_valid as nan23hou_death_valid
                        except ImportError: from nan023_wanghou import death_valid as nan23hou_death_valid
                        carried_subject=nan23hou_death_valid(event,evidence,chapters[record['chapter_id']],root)
                        check(carried_subject,'本傳諸卒各繫本人')
                    if event['id'].startswith('le-nan023-wangyu-'):
                        try: from scripts.nan023_wangyu import death_valid as nan23yu_death_valid
                        except ImportError: from nan023_wangyu import death_valid as nan23yu_death_valid
                        carried_subject=nan23yu_death_valid(event,evidence,chapters[record['chapter_id']],root)
                        check(carried_subject,'本傳諸卒各繫本人')
                    if event['id'].startswith('le-nanqi047-wangrong-'):
                        try: from scripts.nanqi047_wangrong import death_valid as qi47rong_death_valid
                        except ImportError: from nanqi047_wangrong import death_valid as qi47rong_death_valid
                        carried_subject=qi47rong_death_valid(event,evidence,chapters[record['chapter_id']],root)
                        check(carried_subject,'本傳諸卒各繫本人')
                    if event['id'].startswith('le-liang033-wangsengru-'):
                        try: from scripts.liang033_wangsengru import death_valid as liang33sr_death_valid
                        except ImportError: from liang033_wangsengru import death_valid as liang33sr_death_valid
                        carried_subject=liang33sr_death_valid(event,evidence,chapters[record['chapter_id']],root)
                        check(carried_subject,'本傳諸卒各繫本人')
                    if event['id'].startswith('le-nanshi059-wangsengru-'):
                        try: from scripts.nanshi059_wangsengru import death_valid as nan59sr_death_valid
                        except ImportError: from nanshi059_wangsengru import death_valid as nan59sr_death_valid
                        carried_subject=nan59sr_death_valid(event,evidence,chapters[record['chapter_id']],root)
                        check(carried_subject,'本傳諸卒各繫本人')
                    if event['id'].startswith('le-nanqi047-wyd-wangrong-'):
                        try: from scripts.nanqi047_wangrong_wyd import death_valid as q47wyd_death
                        except ImportError: from nanqi047_wangrong_wyd import death_valid as q47wyd_death
                        carried_subject=q47wyd_death(event,evidence,chapters[record['chapter_id']],root)
                        check(carried_subject,'王融殿本卒年及死者原證缺失')
                    if event['id'].startswith('le-nanshi024-wangshaozhi-'):
                        try: from scripts.nanshi024_wangshaozhi import death_valid as nan24sz_death_valid
                        except ImportError: from nanshi024_wangshaozhi import death_valid as nan24sz_death_valid
                        carried_subject=nan24sz_death_valid(event,evidence,chapters[record['chapter_id']],root)
                        check(carried_subject,'本傳諸卒各繫本人')
                    if event['id'].startswith('le-nanshi024-wyd-wangshaozhi-'):
                        try: from scripts.nanshi024_wangshaozhi_wyd import death_valid as n24szwyd_death
                        except ImportError: from nanshi024_wangshaozhi_wyd import death_valid as n24szwyd_death
                        carried_subject=n24szwyd_death(event,evidence,chapters[record['chapter_id']],root)
                        check(carried_subject,'王韶之殿本卒年及死者原證缺失')
                    if event['id'].startswith('le-nanshi024-wangyuezhi-'):
                        try: from scripts.nanshi024_wangyuezhi import death_valid as nan24yz_death_valid
                        except ImportError: from nanshi024_wangyuezhi import death_valid as nan24yz_death_valid
                        carried_subject=nan24yz_death_valid(event,evidence,chapters[record['chapter_id']],root)
                        check(carried_subject,'本傳諸卒各繫本人')
                    if event['id'].startswith('le-nanshi024-wangzhunzhi-'):
                        try: from scripts.nanshi024_wangzhunzhi import death_valid as nan24zz_death_valid
                        except ImportError: from nanshi024_wangzhunzhi import death_valid as nan24zz_death_valid
                        carried_subject=nan24zz_death_valid(event,evidence,chapters[record['chapter_id']],root)
                        check(carried_subject,'本傳諸卒各繫本人')
                    if event['id'].startswith('le-nanshi024-wangjinzhi-'):
                        try: from scripts.nanshi024_wangjinzhi import death_valid as nan24jz_death_valid
                        except ImportError: from nanshi024_wangjinzhi import death_valid as nan24jz_death_valid
                        carried_subject=nan24jz_death_valid(event,evidence,chapters[record['chapter_id']],root)
                        check(carried_subject,'本傳諸卒各繫本人')
                    if event['id'].startswith('le-nanshi024-wangqing-'):
                        try: from scripts.nanshi024_wangqing import death_valid as nan24qing_death_valid
                        except ImportError: from nanshi024_wangqing import death_valid as nan24qing_death_valid
                        carried_subject=nan24qing_death_valid(event,evidence,chapters[record['chapter_id']],root)
                        check(carried_subject,'本傳諸卒各繫本人')
                    if event['id'].startswith('le-nanshi024-wangqunzhi-'):
                        try: from scripts.nanshi024_wangqunzhi import death_valid as nan24qun_death_valid
                        except ImportError: from nanshi024_wangqunzhi import death_valid as nan24qun_death_valid
                        carried_subject=nan24qun_death_valid(event,evidence,chapters[record['chapter_id']],root)
                        check(carried_subject,'本傳諸卒各繫本人')
                    if event['id'].startswith('le-nanshi024-wangsu-'):
                        try: from scripts.nanshi024_wangsu import death_valid as nan24su_death_valid
                        except ImportError: from nanshi024_wangsu import death_valid as nan24su_death_valid
                        carried_subject=nan24su_death_valid(event,evidence,chapters[record['chapter_id']],root)
                        check(carried_subject,'本傳諸卒各繫本人')
                    if event['id'].startswith('le-nanshi024-ruanwanling-'):
                        try: from scripts.nanshi024_ruanwanling import death_valid as nan24rw_death_valid
                        except ImportError: from nanshi024_ruanwanling import death_valid as nan24rw_death_valid
                        carried_subject=nan24rw_death_valid(event,evidence,chapters[record['chapter_id']],root)
                        check(carried_subject,'本傳諸卒各繫本人')
                    if event['id'].startswith('le-song093-wyd-'):
                        try: from scripts.song093_wyd import death_valid as s93wyd_death
                        except ImportError: from song093_wyd import death_valid as s93wyd_death
                        carried_subject=s93wyd_death(event,evidence,chapters[record['chapter_id']],root)
                        check(carried_subject,'宋書殿本卒年與人名須同一原欄')
                    if event['id'].startswith('le-nanshi024-wangmeng-'):
                        try: from scripts.nanshi024_wangmeng import death_valid as nan24meng_death_valid
                        except ImportError: from nanshi024_wangmeng import death_valid as nan24meng_death_valid
                        carried_subject=nan24meng_death_valid(event,evidence,chapters[record['chapter_id']],root)
                        check(carried_subject,'本傳諸卒各繫本人')
                    if event['id'].startswith('le-xiangshan-m9-'):
                        try: from scripts.xiangshan_m9_epitaphs import death_valid as xm9_death_valid
                        except ImportError: from xiangshan_m9_epitaphs import death_valid as xm9_death_valid
                        carried_subject=xm9_death_valid(event,evidence,chapters[record['chapter_id']],root)
                        check(carried_subject,'本傳諸卒各繫本人')
                    if record['chapter_id'] in ('c-nanshi-024-wangyan','c-nanqishu-006-wangyan-jianwu-four') and event['id'].startswith('le-nanshi024-wangyan-'):
                        try: from scripts.nanshi024_wangyan import death_valid as nan24yan_death_valid
                        except ImportError: from nanshi024_wangyan import death_valid as nan24yan_death_valid
                        carried_subject=nan24yan_death_valid(event,evidence,chapters[record['chapter_id']],root)
                        check(carried_subject,'本傳諸卒各繫本人')
                    if event['id'].startswith('le-nanshi024-wangyan-brothers-'):
                        try: from scripts.nanshi024_wangyan_brothers import death_valid as nan24wab_death_valid
                        except ImportError: from nanshi024_wangyan_brothers import death_valid as nan24wab_death_valid
                        carried_subject=nan24wab_death_valid(event,evidence,chapters[record['chapter_id']],root)
                        check(carried_subject,'本傳諸卒各繫本人')
                    if event['id'].startswith('le-nanshi024-guhaozhi-'):
                        try: from scripts.nanshi024_guhaozhi import death_valid as nan24gh_death_valid
                        except ImportError: from nanshi024_guhaozhi import death_valid as nan24gh_death_valid
                        carried_subject=nan24gh_death_valid(event,evidence,chapters[record['chapter_id']],root)
                        check(carried_subject,'本傳諸卒各繫本人')
                    if event['id'].startswith('le-nanshi024-wangsiyuan-'):
                        try: from scripts.nanshi024_wangsiyuan import death_valid as nan24siy_death_valid
                        except ImportError: from nanshi024_wangsiyuan import death_valid as nan24siy_death_valid
                        carried_subject=nan24siy_death_valid(event,evidence,chapters[record['chapter_id']],root)
                        check(carried_subject,'本傳諸卒各繫本人')
                    if event['id']=='le-nanqi023-taizu':
                        try: from scripts.qi023_wangjian_witnesses import death_subject_valid as qi23_death_subject_valid
                        except ImportError: from qi023_wangjian_witnesses import death_subject_valid as qi23_death_subject_valid
                        carried_subject=qi23_death_subject_valid(event,evidence,chapters[record['chapter_id']],root)
                    if 'relative_assertion_id' in evidence:
                        try: from scripts.jin033_relative_death import valid as jin033_relative_death_valid
                        except ImportError: from jin033_relative_death import valid as jin033_relative_death_valid
                        carried_subject = jin033_relative_death_valid(event,evidence,chapters[record['chapter_id']],root)
                        check(carried_subject, '所喪父母須有同句親稱與同人的親屬斷言')
                    if evidence.get('person_reference_id') and record['chapter_id']=='c-songshu-041-wangzhenfeng':
                        try: from scripts.song041_wang_obituaries import valid as royal_obituary
                        except ImportError: from song041_wang_obituaries import valid as royal_obituary
                        carried_subject=royal_obituary(event,evidence,chapters[record['chapter_id']],root)
                    if evidence.get('subject_binding') == 'immediately_preceding_reference':
                        try: from scripts.adjacent_death_reference import valid as adjacent_death_valid
                        except ImportError: from adjacent_death_reference import valid as adjacent_death_valid
                        carried_subject = adjacent_death_valid(event, evidence, chapters[record['chapter_id']])
                        check(carried_subject, '卒事之人稱及所接卒字須同人、同段、字位相連')
                    if evidence.get('document_subject', {}).get('kind') == 'tao_meng_death_subject':
                        try: from scripts.tao_meng_family import context_valid as tao_meng_context_valid
                        except ImportError: from tao_meng_family import context_valid as tao_meng_context_valid
                        carried_subject=tao_meng_context_valid(evidence['document_subject'],evidence,event['person_id'],chapters[record['chapter_id']])
                        check(carried_subject,'孟府君傳卒齡須回到本傳諱嘉及同句君字')
                    check(carried_subject or bool(mention) and mention[1] == evidence['paragraph_id'] and mention[2]['person_id'] == event['person_id'], '生卒事件人物錨點不符')
                    if valid and mention and not carried_subject:
                        starts = [i for i in range(len(hit[1]['text'])) if hit[1]['text'].startswith(evidence['quote'], i)]
                        check(any(i <= mention[2]['start'] and mention[2]['end'] <= i + len(evidence['quote']) for i in starts), '生卒人物錨點不在引句中')
                    check(expression is None or continuous_date or local_death_date or expression in evidence['quote'], '生卒日期未見於事件引句')
                if 'normalized_date_range' in event:
                    try:
                        from scripts.date_ranges import year_range_errors
                    except ImportError:
                        from date_ranges import year_range_errors
                    check('normalized_date' not in event, '生卒或事件跨年範圍不得另填確定單年')
                    year_window = event['normalized_date_range']
                    range_expression = expression
                    if isinstance(year_window, dict) and 'parallel_event' in year_window:
                        parallel = dict(year_window, basis=year_window['parallel_event'])
                        valid = expression is None and parallel_event_date(parallel)
                        check(valid, '生卒跨年範圍平行事件對讀無效')
                        if valid:
                            range_expression = year_window['parallel_event']['source_event_quote']
                    errors.extend(year_range_errors(year_window, event['evidence'], range_expression))
                    errors.extend(table_regnal_range_errors(year_window, expression, tables, mentions))
                if 'normalized_date' in event:
                    date = event['normalized_date']; errors.extend(normalized_date_errors(date, chapters, root=root, bound_record=event, bound_role='life_event'))
                    check(binding_valid(date, event, 'life_event'), '初中末年號紀年須綁實際同人死亡事件')
                    check(isinstance(expression, str) and bool(expression) or parallel_event_date(date), '生卒數字紀年缺原日期表述')
                    if isinstance(date, dict):
                        check(local_death_date or date.get('original_quote') in [e['quote'] for e in event['evidence']], '生卒數字紀年原句不符')
                        date_evidence = date.get('evidence', [])
                        inherited_burial_era = (
                            event['event_type'] == 'burial'
                            and date.get('relative_year_reference', {}).get('kind') == 'omitted_era_regnal_year'
                            and len(date_evidence) == 2 and date_evidence[1:] == event['evidence']
                            and date_evidence[0].get('paragraph_id')
                                in event['evidence'][0].get('context', {}).get('intervening_paragraph_ids', [])
                            and date_evidence[0].get('person_mention_id') == event['evidence'][0].get('person_mention_id')
                            and date_evidence[0].get('chapter_id') == record['chapter_id']
                            and date_evidence[0].get('quote')
                                == paragraphs.get(date_evidence[0].get('paragraph_id'), (None, {}))[1].get('text'))
                        check(local_death_date or inherited_burial_era or date_evidence == event['evidence'],
                              '生卒數值證據與事件不符')
        try:
            from scripts.life_event_dates import date_decision_errors, date_record_scope_errors
        except ImportError:
            from life_event_dates import date_decision_errors, date_record_scope_errors
        dated_events = {e['id']: e for path in (root / 'corpus').glob('*/*-life-events.json')
                        for e in json.loads(path.read_text())['events']}
        try:
            from scripts.age_context import age_context_valid
        except ImportError:
            from age_context import age_context_valid
        family_count_ids = set()
        for chapter in chapters.values():
            for report in chapter['annotation'].get('family_count_reports', []):
                try:
                    from scripts.literal_family_reports import count_valid
                except ImportError:
                    from literal_family_reports import count_valid
                check(isinstance(report.get('id'), str) and report['id'] and report['id'] not in family_count_ids, '來源子數ID缺失或重複')
                family_count_ids.add(report.get('id'))
                check(report.get('parent_person_id') in pids and count_valid(report, paragraphs, chapters, root, source_age_number), '來源有子數須綁父名與數詞，已具名範圍不得當完整子女名單')
            for age in chapter['annotation'].get('age_assertions', []):
                if 'age_context' in age:
                    check(age_context_valid(age, dated_events), '報齡時點須區分生前與同人同段死亡事件，不得把生前年齡充享年')
        date_equivalences = [e for path in (root / 'corpus').glob('*/*-equivalences.json')
                             for e in json.loads(path.read_text())['decisions']]
        date_decision_ids = set(); date_candidate_scopes = set()
        for path in (root / 'corpus').glob('*/*-date-decisions.json'):
            record = json.loads(path.read_text())
            check(record['record_type'] == 'life_event_date_decision_set' and record['work_id'] in works,
                  '生卒紀年取捨集格式或著作無效')
            errors.extend(date_record_scope_errors(record, chapters, works))
            for decision in record['decisions']:
                check(decision['id'] not in date_decision_ids, '生卒紀年取捨 ID 重複')
                date_decision_ids.add(decision['id'])
                errors.extend(date_decision_errors(decision, dated_events, date_equivalences, pids))
                candidates = set(decision['candidate_event_ids'])
                check(not date_candidate_scopes.intersection(candidates), '同一生卒事件不得有多項紀年預設')
                date_candidate_scopes.update(candidates)
        try:
            from .family_assemblies import load_assemblies
            from .person_bundle import load_catalog
        except ImportError:
            try:
                from scripts.family_assemblies import load_assemblies
                from scripts.person_bundle import load_catalog
            except ModuleNotFoundError:
                from family_assemblies import load_assemblies
                from person_bundle import load_catalog
        catalog = load_catalog(root)
        try:
            from scripts.biographical_appointment_sequence import errors as appointment_sequence_errors
        except ImportError:
            from biographical_appointment_sequence import errors as appointment_sequence_errors
        errors.extend(appointment_sequence_errors(chapters, catalog[1], root=root))
        try:
            from scripts.surname_from_father import validate as validate_inferred_surname
        except ImportError:
            from surname_from_father import validate as validate_inferred_surname
        all_name_records = [n for r in catalog[1] if r.get('record_type') == 'person_name_component_set' for n in r['records']]
        for n in all_name_records:
            if 'component_source_binding' in n:
                try:from scripts.received_family_names import source_component_valid
                except ImportError:from received_family_names import source_component_valid
                check(source_component_valid(n,chapters.get(n['chapter_id'],{}),root),'收到姓名構件須綁原人物、固定見證及各自字詞，不以同段出現混填')
            validate_inferred_surname(n, all_name_records, chapters, family_relations, root=root)
        try:
            from scripts.epitaph_family_facts import errors as epitaph_fact_errors
        except ImportError:
            from epitaph_family_facts import errors as epitaph_fact_errors
        errors.extend(epitaph_fact_errors(chapters, catalog[1]))
        try:
            from scripts.biography_source_details import errors as biography_detail_errors
        except ImportError:
            from biography_source_details import errors as biography_detail_errors
        errors.extend(biography_detail_errors(chapters, catalog[1], root))

        try:
            from scripts.preferred_name_components import validated_readings
        except ImportError:
            from preferred_name_components import validated_readings
        validated_readings(catalog[1],
            [n for r in catalog[1] if r.get('record_type') == 'person_name_component_set' for n in r['records']],
            {r['id']:r for r in catalog[1] if r.get('record_type') == 'marked_chapter'})
        try:
            from scripts.cross_chapter_references import errors as cross_reference_errors
        except ImportError:
            from cross_chapter_references import errors as cross_reference_errors
        errors.extend(cross_reference_errors(chapters, root))
        load_assemblies(root, catalog)
        def citation_dimensions(value):
            if isinstance(value, dict):
                if all(key in value for key in ('paragraph_id','chapter_id','source_id')):
                    hit = paragraphs.get(value['paragraph_id'])
                    if hit:
                        chapter = chapters[hit[0]]
                        check(all(value[key] == chapter[key] for key in ('work_id','book_id') if key in value),
                              '引文著作卷ID與實際來源不符')
                for item in value.values(): citation_dimensions(item)
            elif isinstance(value, list):
                for item in value: citation_dimensions(item)
        for record in catalog[1]: citation_dimensions(record)
        check(progress['active_work_id'] in works,'進度的著作不存在')
        for b in progress['books']:
            check(chapter_books.get(b['chapter_id'])==b['book_id'],'進度卷篇不符')
            chapter=chapters.get(b['chapter_id'],{})
            if any(p.get('annotation_status') in ('pending','in_progress') for p in chapter.get('paragraphs',[])):
                check(b['person_status']=='in_progress' and not b['complete'],'有待標註段落的進度不得標為完成或首輪完成')
            if b['complete']: check(b['person_status']=='reviewed','初步標註不得宣稱完成')
    except (KeyError,ValueError,TypeError,OSError,ET.ParseError) as exc:
        errors.append(f'資料結構或 XML 無效：{exc}')
    try:
        from scripts import calendar_contexts
    except ImportError:
        import calendar_contexts
    errors.extend(calendar_contexts.validate(root))
    try:
        from scripts import calendar_wiring
    except ImportError:
        import calendar_wiring
    errors.extend(calendar_wiring.validate(root))
    try:
        from scripts.pending_research import validate as validate_pending_research
    except ImportError:
        from pending_research import validate as validate_pending_research
    errors.extend(validate_pending_research(root))
    try:
        from scripts.occurrence_concordance import validate as validate_occurrence_concordance
    except ImportError:
        from occurrence_concordance import validate as validate_occurrence_concordance
    errors.extend(validate_occurrence_concordance(root))
    try:
        from scripts.reading_layout import validate as validate_reading_layout
    except ImportError:
        from reading_layout import validate as validate_reading_layout
    errors.extend(validate_reading_layout(root))
    try:
        from scripts.name_xiaoming import validate_records as validate_xiaoming_records
    except ImportError:
        from name_xiaoming import validate_records as validate_xiaoming_records
    errors.extend(validate_xiaoming_records(root))
    return errors

def main():
    errors=validate()
    if errors:
        print('\n'.join(errors),file=sys.stderr);return 1
    print('卷篇標註驗證通過：人物與文字引用一致。');return 0
if __name__=='__main__':sys.exit(main())
