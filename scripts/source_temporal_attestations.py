# coding: utf-8
"""Generic source-bound validation for temporal context and duration records."""

BASE_KEYS = {
    'id', 'person_id', 'source_term', 'source_anchor', 'event_context', 'date_role',
    'status', 'evidence', 'kind', 'normalized_date', 'duration', 'prospective',
    'human_reviewed', 'reviewer', 'model'
}
OPTIONAL_KEYS = {
    'reference_life_event_id', 'reference_temporal_attestation_id', 'references',
    'regnal_year_mapping', 'rationale'
}
EVIDENCE_BASE_KEYS = {'work_id', 'book_id', 'source_id', 'chapter_id', 'paragraph_id', 'quote'}
ANCHOR_KEYS = {'paragraph_id', 'start', 'end', 'surface'}


def source_integer(number):
    digits = '一二三四五六七八九'
    if not isinstance(number, str):
        return None
    if number in digits:
        return digits.index(number) + 1
    if '十' in number and number.count('十') == 1:
        tens, ones = number.split('十')
        if (not tens or tens in digits) and (not ones or ones in digits):
            return (digits.index(tens) + 1 if tens else 1) * 10 + (digits.index(ones) + 1 if ones else 0)
    return None


def source_temporal_attestation_errors(record, chapters, person_ids, events, normalize):
    errors = []
    if (record.get('format_version') not in ('0.1', '0.2')
            or record.get('record_type') != 'source_temporal_attestation_set'
            or record.get('chapter_id') not in chapters
            or not isinstance(record.get('records'), list)
            or not record['records']):
        return ['來源時間集標頭、篇章或記錄無效']
    chapter_id = record['chapter_id']
    chapter = chapters[chapter_id]
    paragraphs = {p['id']: p for p in chapter['paragraphs']}
    by_id = {r.get('id'): r for r in record['records'] if isinstance(r, dict)}
    seen = set()
    for item in record['records']:
        try:
            if not isinstance(item, dict):
                raise ValueError('時間記錄須為物件')
            allowed = BASE_KEYS | OPTIONAL_KEYS
            if (not BASE_KEYS.issubset(item) or not set(item).issubset(allowed)
                    or not isinstance(item['id'], str) or not item['id'] or item['id'] in seen
                    or item['person_id'] not in person_ids
                    or item['status'] != 'source_attested'
                    or item['date_role'] != 'source_context_not_title_boundary'
                    or type(item['human_reviewed']) is not bool or item['human_reviewed']
                    or not isinstance(item['reviewer'], str) or not item['reviewer']
                    or type(item['prospective']) is not bool
                    or not isinstance(item['event_context'], str) or not item['event_context']):
                raise ValueError('時間記錄身份、審閱或欄位狀態無效')
            seen.add(item['id'])
            kind = item['kind']
            if kind not in ('calendar_context', 'reported_duration', 'elapsed_since_death', 'prospective_formula'):
                raise ValueError('時間記錄類型未知')
            if kind == 'elapsed_since_death' and 'reference_life_event_id' not in item:
                raise ValueError('卒後時長缺少所據死亡事件')
            anchor = item['source_anchor']
            if not isinstance(anchor, dict) or set(anchor) != ANCHOR_KEYS:
                raise ValueError('原詞錨點欄位無效')
            paragraph = paragraphs.get(anchor['paragraph_id'])
            start, end = anchor['start'], anchor['end']
            if (not paragraph or type(start) is not int or type(end) is not int
                    or not 0 <= start < end <= len(paragraph['text'])
                    or paragraph['text'][start:end] != anchor['surface']
                    or anchor['surface'] != item['source_term']):
                raise ValueError('時間原詞位置與段落不符')
            evidence = item['evidence']
            if not isinstance(evidence, list) or len(evidence) != 1 or not isinstance(evidence[0], dict):
                raise ValueError('時間來源須有一筆固定證據')
            ev = evidence[0]
            anchor_id_keys = set(ev) & {'person_mention_id', 'person_reference_id'}
            if set(ev) != EVIDENCE_BASE_KEYS | anchor_id_keys or len(anchor_id_keys) != 1:
                raise ValueError('時間證據欄位須包含一個人物錨點')
            if (ev['chapter_id'] != chapter_id or ev['work_id'] != chapter['work_id']
                    or ev['book_id'] != chapter['book_id'] or ev['source_id'] != chapter['source_id']
                    or ev['paragraph_id'] != paragraph['id'] or ev['quote'] != paragraph['text']):
                raise ValueError('時間證據來源或逐字段落不符')
            if 'person_mention_id' in ev:
                person_anchor = next((m for m in paragraph['mentions'] if m['id'] == ev['person_mention_id']), None)
                if not person_anchor or person_anchor.get('kind') != 'person' or person_anchor.get('person_id') != item['person_id']:
                    raise ValueError('時間證據姓名錨點人物不符')
            else:
                person_anchor = next((r for r in chapter.get('annotation', {}).get('person_reference_occurrences', [])
                                      if r.get('id') == ev['person_reference_id']), None)
                if (not person_anchor or person_anchor.get('paragraph_id') != paragraph['id']
                        or person_anchor.get('person_id') != item['person_id']):
                    raise ValueError('時間證據指涉錨點人物不符')
            duration = item['duration']
            normalized = item['normalized_date']
            if normalized is not None:
                if kind != 'calendar_context' or item['prospective'] or duration is not None:
                    raise ValueError('絕對紀年不得冒充時長或預期日期')
                if normalized.get('evidence') != evidence or normalize(normalized, chapters):
                    raise ValueError('時間上下文紀年未綁定原證')
            if kind in ('reported_duration', 'elapsed_since_death'):
                if normalized is not None or item['prospective'] or not isinstance(duration, dict):
                    raise ValueError('時長不得冒充絕對紀年或預期日期')
                if (set(duration) != {'value', 'unit', 'source_number', 'operator', 'counting'}
                        or type(duration['value']) is not int or duration['value'] < 0
                        or not isinstance(duration['unit'], str) or not duration['unit']
                        or not isinstance(duration['source_number'], str) or not duration['source_number']
                        or duration['operator'] not in ('eq', 'gt', 'gte', 'lt', 'lte')
                        or duration['counting'] != 'unspecified_source_years'
                        or duration['source_number'] not in item['source_term']):
                    raise ValueError('原生時長缺精確數詞或比較方式')
                if source_integer(duration['source_number']) != duration['value']:
                    raise ValueError('原生時長數字與原數詞不符')
            elif duration is not None:
                raise ValueError('非時長記錄不得帶時長值')
            if kind == 'prospective_formula' and not item['prospective']:
                raise ValueError('預期式記錄須標明prospective')
            if 'reference_life_event_id' in item:
                event = events.get(item['reference_life_event_id'])
                if (not event or event.get('event_type') != 'death'
                        or event.get('person_id') != item['person_id']
                        or event.get('status') != 'source_attested'):
                    raise ValueError('卒後時長所據死亡事件無效')
            if 'reference_temporal_attestation_id' in item:
                referenced = by_id.get(item['reference_temporal_attestation_id'])
                if not referenced or referenced.get('id') == item['id']:
                    raise ValueError('相對時長所據時間事件不存在或自我引用')
        except (KeyError, TypeError, ValueError, AttributeError) as exc:
            errors.append(f"{item.get('id', 'unknown') if isinstance(item, dict) else 'unknown'}: 時間記錄未綁定原文：{exc}")
    return errors
