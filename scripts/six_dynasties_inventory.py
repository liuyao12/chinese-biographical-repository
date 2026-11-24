"""以固定卷目及原文校驗逐傳清冊，分報卷目與逐傳進度。"""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAGES = ('entry_checked', 'full_text', 'first_pass', 'item_reviewed')
NANQI_FIXED_LAYOUTS = (
    'nanqi041_fixed_text', 'nanqi042_fixed_text', 'nanqi043_fixed_text',
    'nanqi044_fixed_text', 'nanqi045_fixed_text', 'nanqi046_fixed_text', 'nanqi046_legacy_text',
    'nanqi048_fixed_text', 'nanqi050_fixed_text', 'nanqi051_fixed_text', 'nanqi052_fixed_text', 'nanqi053_fixed_text',
    'nanqi054_fixed_text',
)


def received_text(line):
    """投影已核的文庫排版標記，保留字形、引文及標點。"""
    text = re.sub(r'<ref>[^<>]*</ref>', '', line)
    text = re.sub(r'-\{([^{}|:;<>\s])\}-', r'\1', text)
    text = re.sub(r'\[\[(?:[^\[\]|]+\|)?([^\[\]|]+)\]\]', r'\1', text)
    text = re.sub(r'\{\{YL\|([^{}|]+)\}\}', r'\1', text)
    return text.replace('{{!|𠴲|⿰口沓}}', '𠴲').replace('{{!|𩦎|⿰馬斐}}', '𩦎')


def source_paragraphs(lines, layout=None):
    """核對固定轉錄選用的首行空格及跨段引文模板。"""
    lines = [line for line in lines if line.strip()]
    if layout == 'qi040_ziliang_annotated_jianyuan':
        year = '{{YL|建元二年|480年}}'
        assert sum(line.count(year) for line in lines) == 1
        return [received_text(line.replace(year, '建元二年')) for line in lines]
    if layout == 'qi040_zhaozhou_annotated_years':
        years={'{{YL|建武三年|496年}}':'建武三年','{{YL|永元元年|499年}}':'永元元年'}
        for year in years:
            assert sum(line.count(year) for line in lines)==1
            lines=[line.replace(year,years[year]) for line in lines]
        return [received_text(line) for line in lines]
    if layout == 'qi040_ziqing_annotated_jianyuan':
        year='{{YL|建元元年|479年}}'
        assert sum(line.count(year) for line in lines)==1
        return [received_text(line.replace(year,'建元元年')) for line in lines]
    if layout == 'qi040_zijing_jiujiang':
        assert len(lines)==1 and lines[0].count('{{*|征九江}}')==1
        return [received_text(lines[0].replace('{{*|征九江}}','征九江'))]
    if layout == 'qi040_ziming_yanxing_year':
        assert len(lines)==1 and lines[0].count('{{YL|延興元年|494年}}')==1
        return [received_text(lines[0].replace('{{YL|延興元年|494年}}','延興元年'))]
    if layout == 'qi040_five_prince_heading':
        headings = ('西陽王子文', '衡陽王子峻', '南康王子琳', '湘東王子建', '南郡王子夏')
        assert len(lines) in (1, 2)
        assert any(lines[0].startswith("'''" + title + "'''") for title in headings)
        assert sum(line.count("'''") for line in lines) == 2
        return [received_text(line.replace("'''", '').replace('{{YL|永泰元年|498年}}', '永泰元年')) for line in lines]
    if layout == 'zhanglihua_annotated_zhide_year':
        raw_year = '{{YL|至德二年|584年}}'
        assert sum(t.count(raw_year) for t in lines) == 1
        return [received_text(t.replace(raw_year, '至德二年')) for t in lines]
    if layout == 'wanglingbin_annotated_dabao_year':
        assert len(lines)==1 and lines[0].count('{{YL|大寶元年|550年}}')==1
        return [received_text(lines[0].replace('{{YL|大寶元年|550年}}','大寶元年'))]
    if layout == 'ruanlingying_annotated_datong_year':
        assert len(lines)==1 and lines[0].count('{{YL|大同九年|543年}}')==1
        return [received_text(lines[0].replace('{{YL|大同九年|543年}}','大同九年'))]
    if layout == 'xihui_annotated_zhongxing_year':
        assert len(lines)>0 and sum(l.count('{{YL|中興二年|502年}}')for l in lines)==1 and next(l for l in lines if '{{YL|中興二年|502年}}'in l).count('{{YL|中興二年|502年}}')==1
        return [received_text(l.replace('{{YL|中興二年|502年}}','中興二年')) for l in lines if l.strip()]
    if layout == 'zhangyaoer_annotated_yongding_year':
        assert sum(t.count('{{YL|永定元年|557年}}')for t in lines)==1
        return [received_text(t.replace('{{YL|永定元年|557年}}','永定元年'))for t in lines if t.strip()]
    if layout == 'nanqi043_xieyue_glyph':
        return [received_text(line.removeprefix('　　').replace('{{!|𤅢|左「氵」右「𦿈」}}', '𤅢')) for line in lines]
    if layout == 'wikisource_inline_phonetic_glosses':
        return [received_text(re.sub(r'\{\{\*\|[^{}|]+反\}\}', '', line)) for line in lines]
    if layout == 'wikisource_indented_blue_and_quote':
        projected = []
        for line in lines:
            if line.startswith(':{{blue|　　'):
                assert line.endswith('}}')
                line = line[len(':{{blue|'):-2]
            projected.append(line)
        return source_paragraphs(projected, 'wikisource_indented_quote')
    if layout == 'wikisource_unindented_quote':
        result = []
        inside_quote = False
        for line in lines:
            if line.startswith('{{quote|'):
                assert not inside_quote
                inside_quote = True
                line = line.removeprefix('{{quote|')
            if line.endswith('}}') and inside_quote:
                inside_quote = False
                line = line.removesuffix('}}')
            result.append(received_text(line))
        assert not inside_quote
        return result
    if layout is None:
        return [received_text(line) for line in lines]
    if layout == 'jin096_split_issued_zhongyan':
        first, second = [received_text(line) for line in lines]
        opening, continuation, rest = first.partition('渾嘗共琰坐')
        assert opening.endswith('既適渾，生濟。') and continuation and rest
        return [opening, continuation + rest, second]
    if layout == 'wikisource_private_use_glyphs':
        lines = [re.sub(r'\{\{PUA\|([\ue000-\uf8ff])\}\}', r'\1', line) for line in lines]
        return source_paragraphs(lines, 'wikisource_mixed_indented_prose')
    if layout == 'wikisource_mixed_indented_prose':
        return [received_text(line.removeprefix(':').removeprefix('　　')) for line in lines]
    if layout == 'wikisource_blockquote_colon':
        return [received_text(line.removeprefix(':')) for line in lines]
    if layout == 'liang021_split_issued_wangxi_death':
        parts=source_paragraphs(lines,'jin065_indented_text')
        head,mark,tail=parts[-1].partition('中大通六年正月，卒')
        end,closing,rest=(mark+tail).partition('子泛、湜。')
        assert head and mark and closing and not rest
        return parts[:-1]+[head,end,closing]
    if layout == 'liang021_split_issued_wangjian_sons':
        first,second=source_paragraphs(lines,'jin065_indented_text')
        prefix,opener,end=second.partition('暕名公子，少致美稱')
        assert prefix and opener and end
        return [first,prefix,opener+end]
    if layout == 'sanguozhi052_received_with_pei_notes':
        try:
            from scripts.sanguozhi052_layers import project_line
        except ImportError:
            from sanguozhi052_layers import project_line
        return [project_line(line)[0] for line in lines]
    if layout == 'sanguozhi052_remaining_with_print_alternatives':
        try:
            from scripts.sanguozhi052_remaining_layers import passage
        except ImportError:
            from sanguozhi052_remaining_layers import passage
        return passage(lines)
    if layout == 'sanguozhi058_received_with_pei_notes':
        try:
            from scripts.sanguozhi058_layers import project_line
        except ImportError:
            from sanguozhi058_layers import project_line
        return [project_line(line)[0] for line in lines]
    if layout == 'sanguozhi057_received_with_pei_notes':
        try:
            from scripts.sanguozhi057_layers import project_line
        except ImportError:
            from sanguozhi057_layers import project_line
        return [body for line in lines if (body:=project_line(line)[0])]
    if layout == 'sanguozhi050_received_with_pei_notes':
        try:
            from scripts.sanguozhi050_layers import project_line
        except ImportError:
            from sanguozhi050_layers import project_line
        return [body for line in lines if (body:=project_line(line)[0])]
    if layout == 'sanguozhi059_received_with_pei_notes':
        try:
            from scripts.sanguozhi059_layers import project_line
        except ImportError:
            from sanguozhi059_layers import project_line
        return [body for line in lines if (body:=project_line(line)[0])]
    if layout=='sanguozhi051_contiguous_slice':
        try: from scripts.sanguozhi051_slices import slice_text
        except ImportError: from sanguozhi051_slices import slice_text
        return [slice_text(line) for line in lines if line]
    if layout == 'sanguozhi051_received_with_pei_notes':
        try:
            from scripts.sanguozhi051_layers import project_line
        except ImportError:
            from sanguozhi051_layers import project_line
        return [body for line in lines if (body:=project_line(line)[0])]
    if layout=='sanguozhi053_contiguous_slice':
        try: from scripts.sanguozhi053_slices import slice_text
        except ImportError: from sanguozhi053_slices import slice_text
        return [slice_text(line) for line in lines if line]
    if layout == 'sanguozhi053_received_with_pei_notes':
        try:
            from scripts.sanguozhi053_layers import project_line
        except ImportError:
            from sanguozhi053_layers import project_line
        return [body for line in lines if (body:=project_line(line)[0])]
    if layout=='sanguozhi054_contiguous_slice':
        try: from scripts.sanguozhi054_slices import slice_text
        except ImportError: from sanguozhi054_slices import slice_text
        return [slice_text(line) for line in lines if line]
    if layout == 'sanguozhi054_received_with_pei_notes':
        try:
            from scripts.sanguozhi054_layers import project_line
        except ImportError:
            from sanguozhi054_layers import project_line
        return [body for line in lines if (body:=project_line(line)[0])]
    if layout=='sanguozhi055_contiguous_slice':
        try: from scripts.sanguozhi055_slices import slice_text
        except ImportError: from sanguozhi055_slices import slice_text
        return [slice_text(line) for line in lines if line]
    if layout == 'sanguozhi055_received_with_pei_notes':
        try:
            from scripts.sanguozhi055_layers import project_line
        except ImportError:
            from sanguozhi055_layers import project_line
        return [body for line in lines if (body:=project_line(line)[0])]
    if layout=='sanguozhi056_contiguous_slice':
        try: from scripts.sanguozhi056_slices import slice_text
        except ImportError: from sanguozhi056_slices import slice_text
        return [slice_text(line) for line in lines if line]
    if layout == 'sanguozhi056_received_with_pei_notes':
        try:
            from scripts.sanguozhi056_layers import project_line
        except ImportError:
            from sanguozhi056_layers import project_line
        return [body for line in lines if (body:=project_line(line)[0])]
    if layout=='sanguozhi060_contiguous_slice':
        try: from scripts.sanguozhi060_slices import slice_text
        except ImportError: from sanguozhi060_slices import slice_text
        return [slice_text(line) for line in lines if line]
    if layout == 'sanguozhi060_received_with_pei_notes':
        try:
            from scripts.sanguozhi060_layers import project_line
        except ImportError:
            from sanguozhi060_layers import project_line
        return [body for line in lines if (body:=project_line(line)[0])]
    if layout=='sanguozhi061_contiguous_slice':
        try: from scripts.sanguozhi061_slices import slice_text
        except ImportError: from sanguozhi061_slices import slice_text
        return [slice_text(line) for line in lines if line]
    if layout == 'sanguozhi061_received_with_pei_notes':
        try:
            from scripts.sanguozhi061_layers import project_line
        except ImportError:
            from sanguozhi061_layers import project_line
        return [body for line in lines if (body:=project_line(line)[0])]
    if layout=='sanguozhi062_contiguous_slice':
        try: from scripts.sanguozhi062_slices import slice_text
        except ImportError: from sanguozhi062_slices import slice_text
        return [slice_text(line) for line in lines if line]
    if layout == 'sanguozhi062_received_with_pei_notes':
        try:
            from scripts.sanguozhi062_layers import project_line
        except ImportError:
            from sanguozhi062_layers import project_line
        return [body for line in lines if (body:=project_line(line)[0])]
    if layout=='sanguozhi063_contiguous_slice':
        try: from scripts.sanguozhi063_slices import slice_text
        except ImportError: from sanguozhi063_slices import slice_text
        return [slice_text(line) for line in lines if line]
    if layout == 'sanguozhi063_received_with_pei_notes':
        try:
            from scripts.sanguozhi063_layers import project_line
        except ImportError:
            from sanguozhi063_layers import project_line
        return [body for line in lines if (body:=project_line(line)[0])]
    if layout in ('sanguozhi049_contiguous_slice', 'sanguozhi064_contiguous_slice',
                  'sanguozhi065_contiguous_slice'):
        try:
            from scripts.sanguozhi064_slices import slice_text
        except ImportError:
            from sanguozhi064_slices import slice_text
        volume = int(layout[9:12])
        return [slice_text(line, volume) for line in lines]
    if layout in NANQI_FIXED_LAYOUTS:
        try:
            from scripts.nanqi041_projection import decode_line
        except ImportError:
            from nanqi041_projection import decode_line
        paragraphs = [text for line in lines if (text := decode_line(line)[0])]
        if layout == 'nanqi046_legacy_text':
            return [text.removeprefix('　　') for text in paragraphs]
        return paragraphs
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
    indent_lines = set(entry.get('verse_indent_lines', []))
    used_indents = set()
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
        for offset, line in enumerate(raw):
            line_number = first + offset
            if line_number in indent_lines:
                assert (offset or start == 0) and line.startswith(':'), title
                raw[offset] = line[1:]
                used_indents.add(line_number)
        selected.extend(raw)
        previous = (last, end)
    assert used_indents == indent_lines, entry['title']
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
            selection = slices[p['id']]
            sections = selection if isinstance(selection, list) else [selection]
            assert sections, p['id']
            previous_end = 0
            for section in sections:
                a, z = (section[k] for k in ('start', 'end'))
                assert type(a) is int and type(z) is int and previous_end <= a < z <= len(part), p['id']
                text.append(part[a:z])
                previous_end = z
        else:
            text.append(part)
    return paragraphs, text


def reviewed_slices(paragraph, entry, chapter):
    """A house-shared paragraph may contain independently reviewed portions."""
    if paragraph.get('annotation_status') == 'reviewed':
        return True
    slices = entry.get('paragraph_slices', {}).get(paragraph['id'], [])
    cases = [row for row in chapter['annotation'].get('source_reading_cases', [])
             if row.get('paragraph_id') == paragraph['id'] and row.get('kind') == 'received_sentence']
    for span in slices:
        start, end = span['start'], span['end']
        cursor = start
        for case in sorted(cases, key=lambda row: row['start_codepoint']):
            a, b = case['start_codepoint'], case['end_codepoint']
            if b <= start or a >= end:
                continue
            if a != cursor or b > end or paragraph['text'][a:b] != case.get('source_quote') or not case.get('reading'):
                return False
            cursor = b
        if cursor != end:
            return False
    return bool(slices)


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
            if entry.get('source_layout') in NANQI_FIXED_LAYOUTS:
                try:
                    from scripts.nanqi041_projection import verify_positions
                except ImportError:
                    from nanqi041_projection import verify_positions
                verify_positions(
                    chapter, (root / survey['raw_path']).read_text(),
                    omit_leading_indent=entry['source_layout'] == 'nanqi046_legacy_text',
                )
            if entry['item_reviewed']:
                assert all(reviewed_slices(p, entry, chapter) for p in paragraphs), title
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
    try:
        from scripts.consort_volume_coverage import verify_covered_consorts
    except ImportError:
        from consort_volume_coverage import verify_covered_consorts
    verify_covered_consorts(inventory, witnesses)
    try: from scripts.qi020_consort_witnesses import cover as cover_qi_consorts
    except ImportError: from qi020_consort_witnesses import cover as cover_qi_consorts
    cover_qi_consorts(inventory,witnesses)
    return candidates, counts


if __name__ == '__main__':
    books, counts = verify()
    print(f'六朝候選卷 {len(books)}。已登記傳目的各階段：', counts)
