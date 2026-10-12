#!/usr/bin/env python3
"""從來源資料重建每人 JSON 與索引，執行時不使用 AI。"""
import json
import html
import re
from urllib.parse import quote
from pathlib import Path
try:
    from .person_bundle import ROOT, bundle, load_catalog
    from .family_assemblies import load_assemblies
except ImportError:
    from person_bundle import ROOT, bundle, load_catalog
    from family_assemblies import load_assemblies


def write_reading_pages(destination, first_path, continuation_prefix, heading, introduction, blocks, references):
    """按完整表格區塊分頁；入口不改名，來源註只帶入本頁使用者。"""
    pages = [[]]
    size = 0
    for block in blocks:
        block_size = len(block.encode('utf-8'))
        if block_size > 240_000:
            raise ValueError('人物索引區塊過大，須按同族分段，而非省略人物。')
        if pages[-1] and size + block_size > 240_000:
            pages.append([]); size = 0
        pages[-1].append(block); size += block_size
    filenames = [first_path] + [f'{continuation_prefix}-{i:03}.md' for i in range(2, len(pages) + 1)]
    navigation = ' · '.join(f'[第{i}頁]({name})' for i, name in enumerate(filenames, 1))
    for filename, content in zip(filenames, pages):
        body = '\n\n'.join(content)
        used = {int(number) for number in re.findall(r'\[《[^]]+》\]\[(\d+)\]', body)}
        definitions = [reference for i, reference in enumerate(references, 1) if i in used]
        text = '\n\n'.join([heading, introduction, navigation, body, '\n'.join(definitions)]) + '\n'
        if len(text.encode('utf-8')) >= 500_000:
            raise ValueError('人物索引頁含導覽仍過大，不能發布截斷頁。')
        (destination / filename).write_text(text)
    for path in destination.glob(continuation_prefix + '-*.md'):
        if re.fullmatch(re.escape(continuation_prefix) + r'-\d{3,}\.md', path.name) and path.name not in filenames:
            path.unlink()
    return filenames


def table_blocks(rows):
    """長表依列分段，保留所有列及原有次序。"""
    header = '| 人物 ID | 人物 | 最多提及來源 | JSON |\n|---|---|---|---|\n'
    blocks = []; current = []; size = len(header.encode('utf-8'))
    for row in rows:
        row_size = len((row + '\n').encode('utf-8'))
        if current and size + row_size > 220_000:
            blocks.append(header + '\n'.join(current)); current = []; size = len(header.encode('utf-8'))
        current.append(row); size += row_size
    if current: blocks.append(header + '\n'.join(current))
    return blocks


def export(root=ROOT):
    catalog = load_catalog(root)
    destination = root / 'exports/persons'
    destination.mkdir(parents=True, exist_ok=True)
    works = {w['id']: w['title'] for w in json.loads((root / 'registry/works.json').read_text())['works']}
    source_labels = {}
    source_references = []
    for record in catalog[1]:
        if record.get('record_type') != 'marked_chapter':
            continue
        title = re.sub(r'第[一二三四五六七八九十百千〇零]+$', '', record['title'])
        label = '《' + works[record['work_id']] + '・' + title + '》'
        url = record['source'].get('permalink') or record['source']['url']
        number = len(source_references) + 1
        source_labels[record['source_id']] = f'[{label}][{number}]'
        source_references.append(f'[{number}]: {url}')
    def source_column(row):
        return '、'.join(source_labels[sid] for sid in row['most_mentioned_source_ids']) or '—'
    def person_label(row):
        label = re.sub(r'（[^（）]*候選）$', '', row['label']).replace('|', '／')
        if row.get('preferred_parent_status') == 'unresolved':
            label += '（來源候選；預設不接父系）'
        return label
    source_map, assemblies = load_assemblies(root, catalog)
    rows = []
    for pid, person in sorted(catalog[0].items()):
        result = bundle(pid, root=root, include_provisional=True, catalog=catalog)
        assembly = source_map.get(pid)
        if assembly:
            result['assembled_identity'] = assembly
        filename = pid + '.json'
        (destination / filename).write_text(json.dumps(result, ensure_ascii=False, separators=(',', ':')) + '\n')
        if assembly and pid != assembly['representative_source_person_id']:
            continue
        output_id = assembly['person_id'] if assembly else pid
        if output_id != pid:
            (destination / (output_id + '.json')).write_text(json.dumps(result, ensure_ascii=False, separators=(',', ':')) + '\n')
        rows.append({'person_id': output_id, 'label': person['label'], 'path': output_id + '.json',
                     'id_aliases': person.get('id_aliases', []),
                     'identity_policy': result['identity_policy'],
                     'mention_count': len(result['mentions']), 'source_count': len(result['sources']),
                     'most_mentioned_source_ids': result['most_mentioned_source_ids']})
        omitted_parent_decisions = [decision['id'] for decision in result['family_tree_decisions']
            if decision['default_view'] == 'omit_unproven_biological_parent_edge'
            and set(result['person_ids']).intersection(decision.get('subject_person_ids', [decision['subject_person_id']]))]
        if omitted_parent_decisions:
            rows[-1].update(preferred_parent_status='unresolved', parent_decision_ids=omitted_parent_decisions)
        if assembly:
            rows[-1].update(source_person_id=pid, assembled_identity=assembly)
    aliases = {alias: source_map.get(pid, {}).get('person_id', pid) for pid, person in catalog[0].items() for alias in person.get('id_aliases', [])}
    aliases.update({pid: row['person_id'] for pid, row in source_map.items() if pid != row['person_id']})
    for alias in sorted(aliases):
        source_id = next((pid for pid, person in catalog[0].items() if alias == pid or alias in person.get('id_aliases', [])), None)
        result = bundle(source_id, root=root, include_provisional=True, catalog=catalog)
        result['requested_person_id'] = alias
        if source_id in source_map:
            result['assembled_identity'] = source_map[source_id]
        (destination / (alias + '.json')).write_text(json.dumps(result, ensure_ascii=False, separators=(',', ':')) + '\n')
    lines = ['# 人物 JSON 索引', '', '可重建匯出，涵蓋目前已標註資料，包含明示選用的暫定跨篇同指；原 ID、證據與判讀均保留。並非全部史料或完整覆核。', '',
             '程式可讀取 [index.json](index.json)，再依各筆 `path` 取得人物資料。重新產生：`python3 scripts/export_person_bundles.py`。', '',
             '出生排行與籍貫結構化欄位仍在逐篇回填；缺欄位不代表來源沒有此資訊。', '',
             '已接合父系見 [家族組裝資料](../../registry/family-assemblies.json)。`assembled_identity.person_id` 是共用家族根的組裝 ID，`source_person_ids` 保留各篇候選；父子及同指證據可由記錄 ID 回查。缺代節點另有 `ancestor_person_id`、`generation_distance` 與空值中間世代；父親空值不表示它另成一族。', '',
             '點選家族標題可展開或收起後代。`*` 表示缺名世代，不建立人物，也不表示不同缺名位置是同一人。表內只列家族根後的 ID 尾碼；根人物以「根」表示，完整 ID 保留於家族標題及 JSON。最多提及來源另列一欄，同數並列；提及次數不代表史料優先權。舊 ID 與 JSON 入口保留為別名；索引只計現行人物。', '', '尚未連入同族的人物見 [獨立人物索引](unconnected.md)。', '', '## 可展開家族', '']
    family_blocks = []
    families = {}
    for row in rows:
        families.setdefault(row['person_id'][:11], []).append(row)
    singles = []
    for family, members in sorted(families.items()):
        if len(members) == 1:
            singles.extend(members)
            continue
        members.sort(key=lambda row: row['person_id'])
        root_row = next(v for v in members if v['person_id'] == family)
        member_rows = [f"| `{v['person_id'][12:] or '根'}` | {person_label(v)} | {source_column(v)} | [JSON]({quote(v['path'], safe='_.-')}) |" for v in members]
        # 大家族可以跨頁，家族根、完整 ID 與表列尾碼仍保持一致。
        for part, table in enumerate(table_blocks(member_rows), 1):
            table = table.replace('| 人物 ID |', '| ID 尾碼 |', 1)
            suffix = f'，第{part}段' if part > 1 else ''
            family_blocks.append(f'<details><summary><code>{family}</code> {html.escape(root_row["label"])}（{len(members)} 名{suffix}）</summary>\n\n{table}\n\n</details>')
    family_pages = write_reading_pages(destination, 'README.md', 'families', lines[0], '\n'.join(lines[2:]), family_blocks, source_references)
    single_rows = [f"| `{v['person_id']}` | {person_label(v)} | {source_column(v)} | [JSON]({quote(v['path'], safe='_.-')}) |" for v in singles]
    single_pages = write_reading_pages(destination, 'unconnected.md', 'unconnected', '# 尚未連入同族的人物', '返回 [可展開家族索引](README.md)。以下人物尚未依已記錄的父系資料連入其他節點；同姓不表示同族。索引分頁不改人物 ID 或 JSON 入口。', table_blocks(single_rows), source_references)
    (destination / 'index.json').write_text(json.dumps({'format_version': '0.1', 'persons': rows, 'id_aliases': aliases,
        'reading_indexes': {'family_pages': family_pages, 'unconnected_pages': single_pages}}, ensure_ascii=False, indent=2) + '\n')
    candidate_path = root / 'data/historical-tables/person-candidates.json'
    if candidate_path.exists():
        try:
            from .table_person_profiles import build as build_table_person_profiles
        except ImportError:
            from table_person_profiles import build as build_table_person_profiles
        build_table_person_profiles(root)
    print('人物 JSON：', len(rows))


if __name__ == '__main__':
    export()
    try:
        from .reading_catalog import run as export_reading_catalog
    except ImportError:
        from reading_catalog import run as export_reading_catalog
    export_reading_catalog()
