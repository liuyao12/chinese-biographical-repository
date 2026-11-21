"""以固定卷目及原文校驗逐傳清冊，分報卷目與逐傳進度。"""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAGES = ('entry_checked', 'full_text', 'first_pass', 'item_reviewed')


def received_text(line):
    """投影已核的文庫排版標記，保留字形、引文及標點。"""
    text = re.sub(r'<ref>[^<>]*</ref>', '', line)
    text = re.sub(r'-\{([^{}|:;<>\s])\}-', r'\1', text)
    text = re.sub(r'\[\[(?:[^\[\]|]+\|)?([^\[\]|]+)\]\]', r'\1', text)
    text = re.sub(r'\{\{YL\|([^{}|]+)\}\}', r'\1', text)
    return text.replace('{{!|𠴲|⿰口沓}}', '𠴲')


def source_paragraphs(lines, layout=None):
    """核對固定轉錄選用的首行空格及跨段引文模板。"""
    lines = [line for line in lines if line.strip()]
    if layout is None:
        return [received_text(line) for line in lines]
    if layout == 'wikisource_blockquote_colon':
        return [received_text(line.removeprefix(':')) for line in lines]
    if layout == 'jin065_indented_text':
        paragraphs = []
        for line in lines:
            if line.startswith(':　　'):
                line = line[1:]
            assert line.startswith('　　')
            text = received_text(line[2:])
            emphasis = "'" * 3
            if text.count(emphasis) == 2:
                text = text.replace(emphasis, '')
            paragraphs.append(text)
        return paragraphs
    assert layout == 'wikisource_indented_quote'
    paragraphs = []
    in_quote = False
    for line in lines:
        if line.startswith('{{quote|'):
            assert not in_quote
            in_quote = True
            line = line.removeprefix('{{quote|')
        assert line.startswith('　　')
        text = received_text(line[2:])
        if in_quote and text.endswith('}}'):
            text = text[:-2]
            in_quote = False
        paragraphs.append(text)
    assert not in_quote
    return paragraphs


def source_passage(entry, lines, located_headings, ranges):
    """同一傳可隔著附傳另起續題；按各段實際起訖核原文。"""
    selected = []
    previous = (0, 0)
    for span in [entry, *entry.get('continuation_spans', [])]:
        first, last = span['first_line'], span['last_line']
        start, end = span['start_codepoint'], span['end_codepoint']
        title = entry['title']
        assert 1 <= first <= last <= len(lines) and 0 <= start < len(lines[first - 1]), title
        assert 0 < end <= len(lines[last - 1]) and (first < last or start < end), title
        assert previous <= (first, start), title
        if 'heading_line' in span:
            head = span['heading_line']
            assert previous[0] <= head < first and head >= 1, title
            assert lines[head - 1] == span['heading_raw'], title
            assert re.fullmatch(r'=+.+?=+\s*', span['heading_raw']) and head not in located_headings, title
            located_headings.add(head)
        key = (entry['book_id'], first, start, last, end)
        assert key not in ranges, title
        ranges.add(key)
        raw = lines[first - 1:last]
        raw[-1] = raw[-1][:end]
        raw[0] = raw[0][start:]
        assert raw[0].startswith(span['opening']) and raw[-1].endswith(span['closing']), title
        selected.extend(raw)
        previous = (last, end)
    return selected


def chapter_passage(entry, chapter):
    paragraphs = chapter['paragraphs']
    ids = entry.get('paragraph_ids')
    slices = entry.get('paragraph_slices', {})
    if ids is not None:
        assert ids and len(set(ids)) == len(ids), entry['title']
        requested = set(ids)
        paragraphs = [p for p in paragraphs if p['id'] in requested]
        assert [p['id'] for p in paragraphs] == ids, entry['title']
    assert set(slices) <= {p['id'] for p in paragraphs}, entry['title']
    text = []
    for p in paragraphs:
        part = p['text']
        if p['id'] in slices:
            a, z = (slices[p['id']][k] for k in ('start', 'end'))
            assert type(a) is int and type(z) is int and 0 <= a < z <= len(part), p['id']
            part = part[a:z]
        text.append(part)
    return paragraphs, text


def verify(root=ROOT):
    def load(path):
        return json.loads((root / path).read_text(encoding='utf-8'))

    inventory = load('data/corpus/six-dynasties-biographies.json')
    directory = {w['work_id']: w for w in load(inventory['directory_path'])['works']}
    candidates = set()
    for group in inventory['scope']:
        work = directory[group['work_id']]
        assert group['directory_revision'] == work['source']['revision'], work['title']
        for first, last in group['candidate_book_ranges']:
            books = [b for b in work['books'] if first <= b['number'] <= last]
            assert len(books) == last - first + 1 and first <= last
            for book in books:
                assert book['book_id'] not in candidates
                candidates.add(book['book_id'])

    witnesses = {}
    for survey in inventory['volume_surveys']:
        book = survey['book_id']
        assert book in candidates and book not in witnesses, book
        raw = (root / survey['raw_path']).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == survey['sha256'], book
        witnesses[book] = (survey, raw.decode('utf-8').splitlines())

    progress = {p['chapter_id']: p for p in load('corpus/progress.json')['books']}
    ids = set()
    located_headings = {book: set() for book in witnesses}
    counts = dict.fromkeys(STAGES, 0)
    for entry in inventory['biographies']:
        book, title = entry['book_id'], entry['title']
        survey, lines = witnesses[book]
        selected = source_passage(entry, lines, located_headings[book], ids)
        flags = [entry[s] for s in STAGES]
        assert all(type(f) is bool for f in flags) and flags == sorted(flags, reverse=True), title
        for stage in STAGES:
            counts[stage] += entry[stage]
        cid = entry['chapter_id']
        if not cid:
            assert not entry['full_text'], title
            continue
        assert progress[cid]['book_id'] == book, cid
        if 'paragraph_ids' not in entry and not entry.get('mixed_chapter'):
            assert entry['item_reviewed'] == progress[cid]['complete'], cid
        if entry.get('mixed_chapter') and entry['full_text']:
            assert entry.get('paragraph_ids'), title
        if entry['full_text']:
            work, filename = cid[2:].split('-', 1)
            path = Path(entry.get('chapter_path', f'corpus/{work}/{filename}.json'))
            assert path.parent == Path('corpus') / work and path.suffix == '.json', title
            chapter = load(path)
            assert chapter['id'] == cid and chapter['source']['revision_id'] == survey['revision']
            paragraphs, text = chapter_passage(entry, chapter)
            assert source_paragraphs(selected, entry.get('source_layout')) == text, title
            if entry['item_reviewed']:
                assert all(p['annotation_status'] == 'reviewed' for p in paragraphs), title
    for book, (survey, lines) in witnesses.items():
        if survey.get('heading_locator_scheme') == 'wikisource_header_section':
            header = lines[survey['header_line'] - 1]
            assert header == survey['header_raw'], book
            assert re.fullmatch(r'\|\s*section\s*=\s*列傳[^\s]+\s+' + re.escape(survey['headed_title']), header), book
            titles = [row['title'] for row in inventory['biographies']
                      if row['book_id'] == book and row['unit_kind'] == 'headed_account']
            assert titles == [survey['headed_title']], book
            for section in survey['excluded_sections']:
                assert lines[section['first_line'] - 1].startswith(section['opening']) and section['reason'], book
        if survey.get('heading_locator_scheme') == 'wikisource_equals_lines':
            exclusions = set()
            for skip in survey.get('excluded_sections', []):
                i = skip['heading_line']
                assert lines[i-1].strip('= ') == skip['heading'] and skip['reason'], book
                exclusions.add(i)
            headings = {i for i, line in enumerate(lines, 1) if re.fullmatch(r'=+.+?=+\s*', line)}
            assert located_headings[book].isdisjoint(exclusions), book
            if survey['heading_survey'] == 'complete':
                assert headings == located_headings[book] | exclusions, book
    return candidates, counts


if __name__ == '__main__':
    books, counts = verify()
    print(f'六朝候選卷 {len(books)}。已登記傳目的各階段：', counts)
