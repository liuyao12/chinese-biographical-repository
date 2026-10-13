"""匯入與驗證有來源的史料表；不猜測年份或跨頁接續。"""
from html.parser import HTMLParser
from pathlib import Path
import argparse
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / 'data/historical-tables/index.json'


class TableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tables, self.depth, self.cell = [], 0, None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'table':
            if self.depth == 0:
                self.table = {'attrs': attrs, 'rows': []}
                self.tables.append(self.table)
            self.depth += 1
        if self.depth == 1 and tag == 'tr':
            self.row = []
            self.table['rows'].append(self.row)
        if self.depth == 1 and tag in ('td', 'th'):
            self.cell = {'tag': tag, 'attrs': attrs, 'text': ''}
            self.row.append(self.cell)
        if self.cell is not None and tag == 'br':
            self.cell['text'] += '\n'

    def handle_endtag(self, tag):
        if tag == 'table':
            self.depth -= 1
        if tag in ('td', 'th'):
            self.cell = None

    def handle_data(self, text):
        if self.cell is not None:
            self.cell['text'] += text


def import_table(path, number, title):
    raw = path.read_bytes()
    html = raw.decode('utf-8')
    parser = TableParser()
    parser.feed(html)
    tables = [t for t in parser.tables if 'wikitable' in t['attrs'].get('class', '').split()]
    if len(tables) != 1:
        raise ValueError('須逐一指定來源表格，不可猜測接續')
    table = tables[0]
    revision = re.findall(r'oldid=(\d+)', html)[-1]
    tid = 'shiji-' + number
    source = {
        'id': 'table-witness-' + tid, 'work_id': 'w-shiji',
        'book_id': 'b-shiji-' + number, 'chapter_id': 'table-chapter-shiji-' + number,
        'url': 'https://zh.wikisource.org/wiki/史記/卷' + number,
        'revision_url': 'https://zh.wikisource.org/w/index.php?title=史記/卷' + number + '&oldid=' + revision,
        'revision': revision, 'accessed': '2026-10-12',
        'response_sha256': hashlib.sha256(raw).hexdigest(),
        'edition': None, 'image_verified': False,
        'rights': '古籍正文公有領域；維基文庫轉錄及編輯內容依 CC BY-SA 條款，署名維基文庫貢獻者。',
        'rights_url': 'https://zh.wikisource.org/wiki/Wikisource:版權信息',
        'review_status': 'structural_import',
        'note': '完整數位表格結構匯入，未逐格學術覆核。未核讀印本影像，原印本頁碼未知。西元欄沿用此數位轉錄的編者對照，不是古籍原有西元紀年，也不引用其維基百科外連。'
    }
    columns = []
    for i, c in enumerate(table['rows'][0]):
        assert c['tag'] == 'th' and not c['attrs'].get('colspan')
        columns.append({'id': tid + '-column-' + str(i), 'text': c['text'].strip(),
                        'kind': 'western_year' if i == 0 else 'source_column'})
    assert columns[0]['text'] == '公元前'
    rows = []
    for r, row in enumerate(table['rows'][1:], 1):
        assert row[0]['text'].strip().isdigit()
        year = int(row[0]['text'].strip())
        cells, col = [], 0
        for c in row:
            assert c['tag'] == 'td'
            rowspan, colspan = int(c['attrs'].get('rowspan', 1)), int(c['attrs'].get('colspan', 1))
            assert rowspan == 1, '此匯入器不推測跨列位置'
            cells.append({'id': f'{tid}-r{r:03d}-c{col:02d}', 'column': col,
                          'rowspan': rowspan, 'colspan': colspan, 'text': c['text'].strip(),
                          'source_row': r + 1, 'source_column': len(cells) + 1,
                          'printed_page': None, 'person_mentions': []})
            col += colspan
        assert col == len(columns), (r, col)
        rows.append({'id': f'{tid}-r{r:03d}', 'year': {
            'era': 'BCE', 'value': year, 'astronomical_year': 1 - year,
            'precision': 'year', 'status': 'digital_editorial_equivalence',
            'source_quote': row[0]['text'].strip(), 'source_cell_id': cells[0]['id']}, 'cells': cells})
    fragment = {'id': tid + '-digital-table-1', 'source_id': source['id'],
                'printed_page': None, 'source_header': [c['text'] for c in columns],
                'rows': rows, 'continuation': None}
    return {'schema_version': 1, 'id': tid, 'title': title, 'source': source,
            'columns': columns, 'fragments': [fragment]}


def import_general_table(path, number, title):
    raw = path.read_bytes(); html = raw.decode('utf-8')
    parser = TableParser(); parser.feed(html)
    tables = [t for t in parser.tables if 'wikitable' in t['attrs'].get('class', '').split()]
    if not tables: raise ValueError('來源沒有正文表格')
    revision = re.findall(r'oldid=(\d+)', html)[-1]
    tid = 'shiji-' + number
    source = {'id': 'table-witness-' + tid, 'work_id': 'w-shiji', 'book_id': 'b-shiji-' + number,
              'chapter_id': 'table-chapter-shiji-' + number,
              'url': 'https://zh.wikisource.org/wiki/史記/卷' + number,
              'revision_url': 'https://zh.wikisource.org/w/index.php?title=史記/卷' + number + '&oldid=' + revision,
              'revision': revision, 'accessed': '2026-10-13', 'response_sha256': hashlib.sha256(raw).hexdigest(),
              'edition': None, 'image_verified': False,
              'rights': '古籍正文公有領域；維基文庫數位轉錄依CC BY-SA，保留貢獻者署名。',
              'rights_url': 'https://zh.wikisource.org/wiki/Wikisource:版權信息', 'review_status': 'structural_import',
              'note': '各組表保留原欄題、原文、空格及合欄，不推不同欄題的接續。西元欄為數位編者增補；未明年份留空，不推世系曆年。未核底本影像，人物標註仍待逐處覆核。'}
    fragments = []
    for k, table in enumerate(tables, 1):
        original = table['rows']; header = original[0] if original and all(c['tag'] == 'th' for c in original[0]) else []
        body = original[1:] if header else original
        width = max(sum(int(c['attrs'].get('colspan', 1)) for c in row) for row in original)
        labels = []
        for c in header: labels += [c['text'].strip()] + [''] * (int(c['attrs'].get('colspan', 1)) - 1)
        labels += [''] * (width - len(labels))
        western = bool(header and labels[0] in ('公元前', '元前'))
        columns = [{'id': f'{tid}-t{k}-column-{i}', 'text': label,
                    'kind': 'western_year' if western and i == 0 else 'source_column'} for i, label in enumerate(labels)]
        rows = []
        for i, row in enumerate(body, 1):
            col = 0; cells = []
            for j, c in enumerate(row, 1):
                span = int(c['attrs'].get('colspan', 1)); rowspan = int(c['attrs'].get('rowspan', 1))
                if rowspan != 1: raise ValueError('跨列位置須先核對，不猜測')
                cells.append({'id': f'{tid}-t{k}-r{i:03d}-c{col:02d}', 'column': col, 'rowspan': rowspan,
                              'colspan': span, 'text': c['text'].strip(), 'source_row': i + bool(header),
                              'source_column': j, 'printed_page': None, 'person_mentions': []})
                col += span
            year = None
            if western and cells and cells[0]['text'].isdigit():
                value = int(cells[0]['text'])
                year = {'era': 'BCE', 'value': value, 'astronomical_year': 1-value, 'precision': 'year',
                        'status': 'digital_editorial_equivalence', 'source_quote': cells[0]['text'], 'source_cell_id': cells[0]['id']}
            rows.append({'id': f'{tid}-t{k}-r{i:03d}', 'year': year, 'cells': cells})
        fragments.append({'id': f'{tid}-digital-table-{k}', 'source_id': source['id'], 'printed_page': None,
                          'source_header': labels, 'columns': columns, 'rows': rows, 'continuation': None})
    return {'schema_version': 2, 'id': tid, 'title': title, 'source': source, 'independent_sections': True,
            'columns': fragments[0]['columns'], 'fragments': fragments}


def validate_identity_evidence(mention, root=ROOT, cache=None, allow_legacy=False):
    """核對表中同指判讀的篇文、固定版本、引句及來源人物錨點。"""
    cache = {} if cache is None else cache
    for evidence in mention.get('identity_evidence', []):
        legacy = set(evidence) == {'chapter_id', 'paragraph_id', 'source_id', 'quote'}
        assert not legacy or allow_legacy, '新增表的同指證據不得省略版本與來源人物'
        assert legacy or set(evidence) == {'work_id', 'book_id', 'chapter_id', 'paragraph_id', 'source_id', 'source_revision', 'person_id', 'quote'}
        chapter_match = re.match(r'c-shiji-(\d{3})-', evidence['chapter_id'])
        assert chapter_match
        book = 'b-shiji-' + chapter_match[1] if legacy else evidence['book_id']
        assert re.fullmatch(r'b-shiji-\d{3}', book)
        if book not in cache:
            cache[book] = json.loads((root / ('data/corpus/shiji/' + book[-3:] + '.json')).read_text())
        chapter = cache[book]
        for key, source_key in [('work_id', 'work_id'), ('book_id', 'book_id'), ('chapter_id', 'id'), ('source_id', 'source_id')]:
            if key in evidence:
                assert evidence[key] == chapter[source_key]
        if not legacy:
            assert evidence['source_revision'] == chapter['source']['revision_id']
        paragraph = next(p for p in chapter['paragraphs'] if p['id'] == evidence['paragraph_id'])
        quote = evidence['quote']
        assert quote and quote in paragraph['text'], '同指判讀引句不見於指定篇文'
        start = paragraph['text'].index(quote)
        end = start + len(quote)
        if legacy:
            continue
        person = evidence['person_id']
        allowed = [mention['person_id']] if mention.get('person_id') else mention.get('candidate_person_ids', [])
        assert person in allowed, '判讀證據與所連人物不一致'
        assert any(m.get('person_id') == person and m['start'] < end and start < m['end'] for m in paragraph['mentions']), '引句未包含指定人物的來源錨點'


def validate():
    index = json.loads(INDEX.read_text())
    count = 0
    evidence_cache = {}
    persons = json.loads((ROOT/'data/corpus/persons.json').read_text())
    candidate_path = ROOT/'data/historical-tables/person-candidates.json'
    if candidate_path.exists():
        candidates = json.loads(candidate_path.read_text())['persons']
        assert len({p['id'] for p in candidates}) == len(candidates)
        assert not {p['id'] for p in candidates}.intersection(persons)
        for p in candidates:
            assert re.fullmatch('[a-z0-9]{3}_[a-z0-9]{3}_[a-z0-9]{3}', p['id'])
            assert p['status'] == 'source_local_candidate' and p['evidence']
        persons.update({p['id']:p for p in candidates})
    for entry in index['tables']:
        path = ROOT / entry['path']
        table = json.loads(path.read_text())
        assert table['id'] == entry['id']
        ids, previous = set(), None
        general = table.get('schema_version') == 2
        if general: assert table.get('independent_sections') is True
        width = len(table['columns'])
        source = table['source']
        assert source['revision_url'].startswith('https://zh.wikisource.org/w/index.php?')
        assert not source['image_verified'] and source['edition'] is None
        assert re.fullmatch('[0-9a-f]{64}', source['response_sha256'])
        for f in table['fragments']:
            if general:
                width = len(f['columns'])
                assert f['source_header'] == [c['text'] for c in f['columns']]
            columns = f['columns'] if general else table['columns']
            assert f['source_id'] == source['id']
            assert f['continuation'] is None, '目前匯入只含一個完整數位表格'
            for row in f['rows']:
                year = row['year']
                if year is not None:
                    assert year['era'] == 'BCE' and type(year['value']) is int and year['value'] > 0
                    assert year['astronomical_year'] == 1 - year['value']
                    assert year['status'] == 'digital_editorial_equivalence' and year['precision'] == 'year'
                    assert year['source_quote'] == str(year['value'])
                    assert year['source_cell_id'] == row['cells'][0]['id']
                    if not general:
                        assert previous is None or year['value'] == previous - 1
                        previous = year['value']
                else:
                    assert general
                col = 0
                for c in row['cells']:
                    assert c['id'] not in ids
                    ids.add(c['id'])
                    assert c['column'] == col and c['rowspan'] == 1 and c['colspan'] > 0
                    assert c['printed_page'] is None
                    end = 0
                    for m in c['person_mentions']:
                        assert columns[c['column']]['kind'] != 'western_year', '編者西元欄不加原文人名標記'
                        assert 0 <= end <= m['start'] < m['end'] <= len(c['text'])
                        assert c['text'][m['start']:m['end']] == m['surface'], '人物錨點原文不符'
                        assert m['person_id'] in persons and m['status'] == 'contextual_provisional'
                        assert m['id'] not in ids
                        validate_identity_evidence(m, cache=evidence_cache, allow_legacy=table['id'] == 'shiji-015')
                        ids.add(m['id']); end = m['end']
                    combined = sorted(c['person_mentions'] + c.get('unresolved_mentions', []), key=lambda m:m['start'])
                    assert not combined or columns[c['column']]['kind'] != 'western_year', '編者西元欄不加原文指稱'
                    end = 0
                    for m in combined:
                        assert end <= m['start'] < m['end'] <= len(c['text']) and c['text'][m['start']:m['end']] == m['surface']
                        end = m['end']
                        if not m.get('person_id'):
                            assert m['kind'] == 'unresolved_reference' and m['status'] == 'awaiting_collation'
                            validate_identity_evidence(m, cache=evidence_cache, allow_legacy=table['id'] == 'shiji-015')
                    col += c['colspan']
                assert col <= width if general else col == width
                count += 1
    if candidate_path.exists():
        tables = {x['id']:json.loads((ROOT/x['path']).read_text()) for x in index['tables']}
        for person in candidates:
            for e in person['evidence']:
                table = tables[e['table_id']]
                cell = next(c for f in table['fragments'] for row in f['rows'] for c in row['cells'] if c['id'] == e['cell_id'])
                assert e['quote'] == cell['text'] and person['source_surface'] in cell['text']
                assert e['source_id'] == table['source']['id'] and e['source_revision'] == table['source']['revision']
                assert any(m['person_id'] == person['id'] and m['surface'] == person['source_surface'] for m in cell['person_mentions'])
    print('史料表格驗證通過：' , len(index['tables']), '表，', count, '表列')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['validate', 'import'])
    parser.add_argument('--html', type=Path)
    parser.add_argument('--number')
    parser.add_argument('--title')
    parser.add_argument('--independent-sections', action='store_true', help='保留異欄題分組，允許無西元紀年的世系／侯表')
    args = parser.parse_args()
    if args.command == 'validate':
        validate()
    else:
        importer = import_general_table if args.independent_sections else import_table
        table = importer(args.html, args.number, args.title)
        out = ROOT / ('data/historical-tables/' + table['id'] + '.json')
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(table, ensure_ascii=False, indent=2) + '\n')
        print(out)
