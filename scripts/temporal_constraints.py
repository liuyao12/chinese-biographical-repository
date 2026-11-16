# coding: utf-8
"""Validate source-bound mathematical temporal constraints."""

CONSTRAINT_KEYS = {
    'id', 'person_id', 'target', 'operator', 'value', 'derivation',
    'evidence', 'status', 'human_reviewed', 'reviewer'
}
EVIDENCE_KEYS = {
    'work_id', 'book_id', 'source_id', 'chapter_id', 'paragraph_id', 'quote',
    'person_mention_id', 'anchor'
}
ANCHOR_KEYS = {'start', 'end', 'surface'}
DERIVATION_KEYS = {'kind', 'source_term', 'rationale'}
OPERATORS = {'eq', 'lt', 'lte', 'gt', 'gte'}
STATUS = {'source_attested', 'source_entailed', 'editorial_provisional'}
DERIVATIONS = {'explicit_date', 'named_era_span', 'alive_at_date', 'reported_age', 'reported_duration'}


def collect_temporal_constraints(records, person_ids):
    """Return original constraint objects for the requested IDs, without merging them."""
    return [constraint for record in records
            if record.get('record_type') == 'person_temporal_constraint_set'
            for constraint in record.get('constraints', [])
            if constraint.get('person_id') in person_ids]


TARGET_KEYS = {'entity_type', 'entity_id', 'property'}
TARGET_PROPERTIES = {
    'person': {'birth_year', 'death_year'},
    'life_event': {'year'},
    'title_holding': {'start_year', 'end_year'},
    'age_assertion': {'value'},
    'temporal_attestation': {'duration_years', 'elapsed_years'},
}
YEAR_PROPERTIES = {'birth_year', 'death_year', 'year', 'start_year', 'end_year'}


def temporal_constraint_errors(record, chapters, person_ids, target_entities):
    errors = []
    if (record.get('format_version') != '0.1'
            or record.get('record_type') != 'person_temporal_constraint_set'
            or set(record) != {'format_version', 'record_type', 'chapter_id', 'constraints'}
            or record.get('chapter_id') not in chapters
            or not isinstance(record.get('constraints'), list)
            or not record['constraints']):
        return ['來源時間約束集格式或篇不存在']
    chapter_id = record['chapter_id']
    chapter = chapters[chapter_id]
    paragraphs = {p['id']: p for p in chapter['paragraphs']}
    seen = set()
    for item in record['constraints']:
        try:
            if set(item) != CONSTRAINT_KEYS:
                raise ValueError('時間約束欄位不符')
            if (not isinstance(item['id'], str) or item['id'] in seen
                    or item['person_id'] not in person_ids or item['operator'] not in OPERATORS
                    or item['status'] not in STATUS or type(item['human_reviewed']) is not bool
                    or not isinstance(item['reviewer'], str) or not item['reviewer']):
                raise ValueError('時間約束識別、型別或審閱狀態無效')
            seen.add(item['id'])
            target = item['target']
            if (not isinstance(target, dict) or set(target) != TARGET_KEYS
                    or target['entity_type'] not in TARGET_PROPERTIES
                    or target['property'] not in TARGET_PROPERTIES[target['entity_type']]
                    or not isinstance(target['entity_id'], str) or not target['entity_id']
                    or target_entities.get((target['entity_type'], target['entity_id'])) != item['person_id']):
                raise ValueError('時間約束目標不存在、人物不符或屬性不相容')
            value = item['value']
            if not isinstance(value, dict):
                raise ValueError('時間約束值無效')
            if value.get('kind') == 'chinese_regnal_year':
                if (set(value) != {'kind', 'era_name', 'year'} or not value['era_name']
                        or type(value['year']) is not int or value['year'] < 1):
                    raise ValueError('年號年界限無效')
            elif value.get('kind') == 'chinese_civil_year':
                if (set(value) != {'kind', 'year', 'year_numbering'}
                        or type(value['year']) is not int
                        or value['year_numbering'] not in ('astronomical', 'historical')):
                    raise ValueError('中國曆年界限無效')
            elif value.get('kind') == 'integer':
                if (set(value) != {'kind', 'value', 'unit'} or type(value['value']) is not int
                        or not isinstance(value['unit'], str) or not value['unit']):
                    raise ValueError('整數界限及單位無效')
            else:
                raise ValueError('未知時間軸')
            is_year_property = target['property'] in YEAR_PROPERTIES
            if is_year_property == (value['kind'] == 'integer'):
                raise ValueError('變數與時間值單位不相容')
            derivation = item['derivation']
            if (not isinstance(derivation, dict) or set(derivation) != DERIVATION_KEYS
                    or derivation['kind'] not in DERIVATIONS
                    or not derivation['source_term'] or not derivation['rationale']):
                raise ValueError('時間約束推導說明不完整')
            if item['status'] == 'source_attested' and derivation['kind'] not in ('explicit_date', 'reported_age', 'reported_duration'):
                raise ValueError('來源明載狀態與推導方式不符')
            if not isinstance(item['evidence'], list) or not item['evidence']:
                raise ValueError('時間約束缺來源證據')
            for evidence in item['evidence']:
                if set(evidence) != EVIDENCE_KEYS or evidence['chapter_id'] != chapter_id:
                    raise ValueError('時間約束證據欄位或篇章不符')
                paragraph = paragraphs.get(evidence['paragraph_id'])
                if (not paragraph or evidence['work_id'] != chapter['work_id']
                        or evidence['book_id'] != chapter['book_id']
                        or evidence['source_id'] != chapter['source_id']
                        or evidence['quote'] != paragraph['text']):
                    raise ValueError('時間約束引句或來源位置不符')
                anchor = evidence['anchor']
                if set(anchor) != ANCHOR_KEYS:
                    raise ValueError('時間約束原詞字位欄位不符')
                start, end = anchor['start'], anchor['end']
                if (type(start) is not int or type(end) is not int or not 0 <= start < end <= len(paragraph['text'])
                        or paragraph['text'][start:end] != anchor['surface']
                        or derivation['source_term'] != anchor['surface']):
                    raise ValueError('時間約束原詞字位不符')
                mention = next((m for m in paragraph['mentions'] if m['id'] == evidence['person_mention_id']), None)
                if (not mention or mention.get('kind') != 'person'
                        or mention.get('person_id') != item['person_id']):
                    raise ValueError('時間約束人物錨點不符')
        except (KeyError, TypeError, ValueError) as exc:
            errors.append(f"{item.get('id', 'unknown')}: 時間約束未綁定來源證據：{exc}")
    return errors
