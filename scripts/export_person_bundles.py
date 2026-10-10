#!/usr/bin/env python3
"""從來源資料重建每人 JSON 與索引，執行時不使用 AI。"""
import json
from pathlib import Path
from person_bundle import ROOT, bundle, load_catalog


def export(root=ROOT):
    catalog = load_catalog(root)
    destination = root / 'exports/persons'
    destination.mkdir(parents=True, exist_ok=True)
    rows = []
    for pid, person in sorted(catalog[0].items()):
        result = bundle(pid, root=root, include_provisional=True, catalog=catalog)
        filename = pid + '.json'
        (destination / filename).write_text(json.dumps(result, ensure_ascii=False, separators=(',', ':')) + '\n')
        rows.append({'person_id': pid, 'label': person['label'], 'path': filename,
                     'identity_policy': result['identity_policy'],
                     'mention_count': len(result['mentions']), 'source_count': len(result['sources']),
                     'most_mentioned_source_ids': result['most_mentioned_source_ids']})
    (destination / 'index.json').write_text(json.dumps({'format_version': '0.1', 'persons': rows}, ensure_ascii=False, indent=2) + '\n')
    lines = ['# 人物 JSON 索引', '', '可重建匯出，涵蓋目前已標註資料，包含明示選用的暫定跨篇同指；原 ID、證據與判讀均保留。並非全部史料或完整覆核。', '',
             '程式可讀取 [index.json](index.json)，再依各筆 `path` 取得人物資料。重新產生：`python3 scripts/export_person_bundles.py`。', '',
             '出生排行與籍貫結構化欄位仍在逐篇回填；缺欄位不代表來源沒有此資訊。', '', '| 人物 ID | 標籤 | JSON |', '|---|---|---|']
    lines.extend(f"| {v['person_id']} | {v['label'].replace('|', '／')} | [JSON]({v['path']}) |" for v in rows)
    (destination / 'README.md').write_text('\n'.join(lines) + '\n')
    print('人物 JSON：', len(rows))


if __name__ == '__main__':
    export()
