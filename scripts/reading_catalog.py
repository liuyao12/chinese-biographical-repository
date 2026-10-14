"""為靜態閱讀器匯出分類目錄與原樣標註文本；不重新識別人物。"""
from pathlib import Path
import argparse
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
CATEGORIES = [(1, 12, 'benji', '本紀'), (13, 22, 'biao', '表'),
              (23, 30, 'shu', '書'), (31, 60, 'shijia', '世家'), (61, 130, 'liezhuan', '列傳')]


def outputs():
    directory = ROOT / 'data/corpus'
    contents = json.loads((directory / 'shiji-contents.json').read_text())
    progress = {b['book_id']: b for b in json.loads((ROOT / 'corpus/progress.json').read_text())['books']}
    chapters = {int(p.stem): (p, json.loads(p.read_text())) for p in (ROOT / 'corpus/shiji').glob('*.json') if p.stem.isdigit()}
    table_index = json.loads((ROOT / 'data/historical-tables/index.json').read_text())
    table_numbers = {int(t['id'].split('-')[-1]) for t in table_index['tables']}
    result, entries = {}, []
    for item in contents['chapters']:
        number = item['number']
        category = next(c for c in CATEGORIES if c[0] <= number <= c[1])
        entry = {**item, 'category': category[2], 'category_label': category[3]}
        if number in chapters:
            path, chapter = chapters[number]
            public = 'data/corpus/shiji/' + path.name
            result[ROOT / public] = path.read_bytes()
            entry.update({'path': public, 'chapter_id': chapter['id'], 'book_id': chapter['book_id'],
                          'paragraph_count': len(chapter['paragraphs']),
                          'annotation_status': progress[chapter['book_id']]['person_status'], 'available': 'marked_text'})
        elif number in table_numbers:
            entry.update({'available': 'table', 'table_id': f'shiji-{number:03d}', 'annotation_status': 'structural_import'})
        else:
            entry.update({'available': 'pending', 'annotation_status': 'not_imported'})
        entries.append(entry)
    index = {'schema_version': 1, 'work_id': 'w-shiji', 'title': '史記', 'author': '司馬遷',
             'categories': [{'id': c[2], 'label': c[3], 'expected_chapters': c[1] - c[0] + 1} for c in CATEGORIES],
             'chapters': entries, 'contents_source': contents['source'],
             'policy': '已匯入標註文本不表示逐項審訂完成；未匯入篇目仍列目，不補造正文。'}
    result[directory / 'index.json'] = (json.dumps(index, ensure_ascii=False, indent=2) + '\n').encode()
    people = json.loads((ROOT / 'registry/persons.json').read_text())['persons']
    summaries = {p['id']: {'id': p['id'], 'label': p['label'], 'status': p['status'],
                          'historicity': p.get('historicity'), 'identity_note': p.get('identity_note'),
                          'aliases': list(dict.fromkeys(a['surface'] for a in p['aliases']))[:8],
                          'review': p.get('review'), 'human_reviewed': False} for p in people}
    result[directory / 'persons.json'] = (json.dumps(summaries, ensure_ascii=False, separators=(',', ':')) + '\n').encode()
    return result


def run(check=False):
    generated = outputs()
    for path, data in generated.items():
        if check:
            assert path.exists() and path.read_bytes() == data, '閱讀器匯出不同步：' + str(path)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
    print('閱讀分類及正文匯出' + ('同步檢查' if check else '') + '：', len(generated), '檔')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    run(parser.parse_args().check)
