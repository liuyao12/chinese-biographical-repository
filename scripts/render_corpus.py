#!/usr/bin/env python3
"""由卷篇 JSON 產生原文不變的行內 XML；不判定人物身份。"""
import argparse
import html
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]


def render(chapter):
    escape = lambda value: html.escape(value, quote=True)
    attributes = ' '.join(f'{name}="{escape(chapter[key])}"' for name, key in (
        ('work-id', 'work_id'), ('book-id', 'book_id'),
        ('chapter-id', 'id'), ('source-id', 'source_id')))
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             f'<text format-version="0.2" {attributes}>']
    for paragraph in chapter['paragraphs']:
        text = paragraph['text']; fragments = []; end = 0
        for mention in paragraph['mentions']:
            start, stop = mention['start'], mention['end']
            if not (end <= start < stop <= len(text)) or text[start:stop] != mention['surface']:
                raise ValueError(f'{mention["id"]}: 無效或重疊字元錨點')
            fragments.append(escape(text[end:start]))
            attributes = f'id="{escape(mention["id"])}"'
            if mention['kind'] == 'person' and mention['person_id']:
                tag = 'persName'; attributes += f' ref="{escape(mention["person_id"])}"'
            elif mention['kind'] == 'unresolved' and mention['person_id'] is None:
                tag = 'rs'; attributes += ' type="unresolved"'
            else:
                raise ValueError(f'{mention["id"]}: 無效人物或未定類型')
            fragments.append(f'<{tag} {attributes}>{escape(mention["surface"])}</{tag}>')
            end = stop
        fragments.append(escape(text[end:]))
        status = f' annotation-status="{escape(paragraph["annotation_status"])}"' if 'annotation_status' in paragraph else ''
        lines.append(f'  <p id="{escape(paragraph["id"])}"{status}>'+''.join(fragments)+'</p>')
    return '\n'.join(lines+['</text>'])+'\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('paths', nargs='*'); parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    paths = [Path(p) for p in args.paths] if args.paths else sorted((ROOT/'corpus').glob('*/*.json'))
    count = 0
    for path in paths:
        chapter = json.loads(path.read_text(encoding='utf-8'))
        if chapter.get('record_type') != 'marked_chapter': continue
        output = render(chapter); target = path.with_suffix('.xml')
        if args.check:
            if not target.exists() or target.read_text(encoding='utf-8') != output:
                raise SystemExit(f'{target}: XML 尚未同步')
        else: target.write_text(output, encoding='utf-8')
        count += 1
    print(f'XML {"同步檢查" if args.check else "產生"}：{count} 篇。')

if __name__ == '__main__': main()
