#!/usr/bin/env python3
"""離線驗證格式、來源錨點、指紋、身份比對與有範圍的證據取捨。"""
from pathlib import Path
import hashlib
import json
import sys
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DATA_DIRS = ('sources', 'assertions', 'decisions', 'catalogues')


def schema_errors(value, spec, schema, path='$'):
    """本庫 schema 所用 JSON Schema 關鍵字的無相依套件驗證器。"""
    if '$ref' in spec:
        target = schema
        for token in spec['$ref'].split('/')[1:]:
            target = target[token]
        return schema_errors(value, target, schema, path)
    errors = []
    if 'oneOf' in spec:
        results = [schema_errors(value, option, schema, path) for option in spec['oneOf']]
        if sum(not result for result in results) != 1:
            errors.append(f'{path}: oneOf 必須符合且只符合一種格式')
            errors.extend(min(results, key=len))
        return errors
    if 'const' in spec and value != spec['const']:
        errors.append(f'{path}: 必須為 {spec["const"]!r}')
    if 'enum' in spec and value not in spec['enum']:
        errors.append(f'{path}: 未知值 {value!r}')
    kinds = spec.get('type')
    if kinds:
        kinds = [kinds] if isinstance(kinds, str) else kinds
        checks = {'object': isinstance(value, dict), 'array': isinstance(value, list),
                  'string': isinstance(value, str), 'boolean': isinstance(value, bool),
                  'integer': isinstance(value, int) and not isinstance(value, bool), 'null': value is None}
        if not any(checks[kind] for kind in kinds):
            return errors + [f'{path}: 型別不符 {kinds}']
    if isinstance(value, dict):
        for key in spec.get('required', []):
            if key not in value:
                errors.append(f'{path}: 缺少 {key}')
        props = spec.get('properties', {})
        for key, child in value.items():
            if key in props:
                errors.extend(schema_errors(child, props[key], schema, path + '.' + key))
            elif spec.get('additionalProperties') is False:
                errors.append(f'{path}: 未知欄位 {key}')
    if isinstance(value, list):
        if len(value) < spec.get('minItems', 0):
            errors.append(f'{path}: 項目不足')
        if 'items' in spec:
            for i, child in enumerate(value):
                errors.extend(schema_errors(child, spec['items'], schema, f'{path}[{i}]'))
    if isinstance(value, str) and len(value) < spec.get('minLength', 0):
        errors.append(f'{path}: 不得為空')
    return errors


def load_records(root=ROOT):
    schema = json.loads((root / 'schema/records.schema.json').read_text(encoding='utf-8'))
    records = []
    errors = []
    for folder in DATA_DIRS:
        for path in sorted((root / folder).glob('*.json')):
            try:
                record = json.loads(path.read_text(encoding='utf-8'))
            except (ValueError, UnicodeError) as exc:
                errors.append(f'{path.name}: JSON 無效：{exc}')
                continue
            errs = schema_errors(record, schema, schema)
            errors.extend(f'{path.name}: {e}' for e in errs)
            records.append(record)
    return records, errors


def validate_records(records):
    errors = []
    sources = {}
    segments = {}
    assertions = {}
    groups = {}
    mentions = set()
    record_ids = set()

    def unique(value, seen, label):
        if value in seen:
            errors.append(f'{label}: 重複識別碼 {value}')
        seen.add(value)

    def url(value, label):
        parts = urlparse(value)
        if parts.scheme not in ('http', 'https') or not parts.netloc:
            errors.append(f'{label}: 網址無效')

    for record in records:
        if 'id' in record:
            unique(record['id'], record_ids, 'record')
        kind = record['record_type']
        if kind == 'source':
            sid = record['id']
            sources[sid] = record
            text = record['text']
            digest = hashlib.sha256('\n\n'.join(s['text'] for s in text['segments']).encode('utf-8')).hexdigest()
            if digest != text['sha256']:
                errors.append(f'{sid}: 文本 SHA-256 不符')
            url(record['witness']['url'], sid)
            url(record['witness']['permalink'], sid)
            for image in record['images']:
                url(image.get('url', ''), sid + ' image')
                if image.get('file_url'):
                    url(image['file_url'], sid + ' image file')
                if image.get('image_verified') and not image.get('exact_page'):
                    errors.append(f'{sid}: 已核讀影像必須列具體頁位')
            for segment in text['segments']:
                if segment['id'] in segments:
                    errors.append(f'{sid}: 段落識別碼重複')
                if not segment['id'].startswith(sid + ':'):
                    errors.append(f'{sid}: 段落識別碼不屬於來源')
                segments[segment['id']] = (sid, segment['text'])
        elif kind == 'assertion_set':
            for a in record['assertions']:
                if a['id'] in assertions:
                    errors.append(f'{a["id"]}: 陳述識別碼重複')
                assertions[a['id']] = a
                if a['predicate'] == 'name':
                    mentions.add(a['subject'])
                if not any(e['source_id'] == record['source_id'] for e in a['evidence']):
                    errors.append(f'{a["id"]}: 陳述未引用所屬來源')
        elif kind == 'identity_decision':
            for group in record['groups']:
                if group['id'] in groups:
                    errors.append(f'{group["id"]}: 身份組識別碼重複')
                groups[group['id']] = group

    for record in records:
        if record['record_type'] == 'assertion_set' and record['source_id'] not in sources:
            errors.append(f'{record["source_id"]}: 陳述集來源不存在')
    for aid, a in assertions.items():
        if a['subject'] not in mentions:
            errors.append(f'{aid}: 主體沒有來源內姓名／氏稱記錄')
        owner = a['subject'].split('#', 1)[0]
        if owner not in sources or '#' not in a['subject']:
            errors.append(f'{aid}: 主體來源不存在')
        if a['object']['kind'] == 'mention' and a['object']['id'] not in mentions:
            errors.append(f'{aid}: 關係對象提及不存在')
        if a['object']['kind'] == 'mention' and a['object']['id'] == a['subject']:
            errors.append(f'{aid}: 關係自環')
        for e in a['evidence']:
            entry = segments.get(e['segment_id'])
            if not entry or entry[0] != e['source_id']:
                errors.append(f'{aid}: 證據段落不存在或來源不符')
            elif e['quote'] not in entry[1]:
                errors.append(f'{aid}: 證據引句不在原文中')

    assigned = {}
    for gid, g in groups.items():
        if len(g['members']) != len(set(g['members'])):
            errors.append(f'{gid}: 身份組提及重複')
        for member in g['members']:
            if member not in mentions:
                errors.append(f'{gid}: 身份提及不存在')
            if member in assigned:
                errors.append(f'{gid}: 提及已屬於另一身份組')
            assigned[member] = gid
        cited_names = set()
        for aid in g['evidence_assertion_ids']:
            a = assertions.get(aid)
            if not a:
                errors.append(f'{gid}: 身份證據不存在')
            elif a['predicate'] == 'name':
                cited_names.add(a['subject'])
        if not set(g['members']).issubset(cited_names):
            errors.append(f'{gid}: 每個身份提及均須有姓名證據')

    scopes = set()
    for record in records:
        kind = record['record_type']
        if kind == 'precedence_decision':
            rid = record['id']
            gid = record['scope']['identity_group']
            predicate = record['scope']['predicate']
            scope = (gid, predicate)
            if scope in scopes:
                errors.append(f'{rid}: 同範圍存在多個現行決定')
            scopes.add(scope)
            group = groups.get(gid)
            if not group:
                errors.append(f'{rid}: 決定的身份組不存在')
            candidates = record['candidates']
            if len(candidates) != len(set(candidates)):
                errors.append(f'{rid}: 候選重複')
            preferred = record['preferred_assertion_id']
            if record['status'] == 'unresolved' and preferred is not None:
                errors.append(f'{rid}: 未解決定不得選擇優先值')
            if record['status'] == 'provisional' and preferred not in candidates:
                errors.append(f'{rid}: 暫定優先值必須是候選')
            expected_alternatives = set(candidates) - ({preferred} if preferred else set())
            if set(record['alternative_assertion_ids']) != expected_alternatives:
                errors.append(f'{rid}: 替代值必須完整保留其他候選')
            for aid in candidates + record['supporting_assertion_ids']:
                if aid not in assertions:
                    errors.append(f'{rid}: 引用陳述不存在 {aid}')
            for aid in candidates:
                a = assertions.get(aid)
                if a and (a['predicate'] != predicate or (group and a['subject'] not in group['members'])):
                    errors.append(f'{rid}: 候選超出決定範圍')
        elif kind == 'source_catalogue':
            entries = record['sources']
            if len(entries) != len({e['id'] for e in entries}):
                errors.append('catalogue: 來源條目重複')
            if {e['id'] for e in entries} != set(sources):
                errors.append('catalogue: 來源清單不完整')
            for e in entries:
                source = sources.get(e['id'])
                if source and (e['path'] != f'sources/{e["id"]}.json' or
                               e['text_sha256'] != source['text']['sha256'] or
                               e['title'] != source['title'] or e['genre'] != source['genre'] or
                               e['extent'] != source['text']['extent'] or
                               e['image_verified'] != source['witness']['image_verified'] or
                               e['segment_count'] != len(source['text']['segments'])):
                    errors.append(f'{e["id"]}: 目錄與來源不符')
    return errors


def main():
    records, errors = load_records()
    if not errors:
        errors.extend(validate_records(records))
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    count = sum(len(r['assertions']) for r in records if r['record_type'] == 'assertion_set')
    print(f'驗證通過：{sum(r["record_type"] == "source" for r in records)} 項史料、{count} 項來源陳述。')
    return 0


if __name__ == '__main__':
    sys.exit(main())
