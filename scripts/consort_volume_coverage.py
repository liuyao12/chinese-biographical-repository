"""核卷十二、卷七受核諸傳之固定修訂正文，包括模板的原始碼點。"""

def verify_covered_consorts(inventory, witnesses):
    for book_id, first, last, revision in (
        ('b-nanshi-012', 16, 112, 2060595),
        ('b-chenshu-007', 14, 58, 2015446),
    ):
        survey, lines = witnesses[book_id]
        if survey.get('embedded_account_survey') != 'complete':
            continue
        assert survey['revision'] == revision and not survey['pending_boundaries'], book_id
        rows = [row for row in inventory['biographies'] if row['book_id'] == book_id]
        coverage = {
            n: [0] * len(lines[n - 1]) for n in range(first, last + 1)
            if lines[n - 1].strip() and not lines[n - 1].lstrip().startswith('=')
        }
        for row in rows:
            assert row['item_reviewed'] and row['chapter_id'], (book_id, row['title'])
            for span in [row, *row.get('continuation_spans', [])]:
                start_line, end_line = span['first_line'], span['last_line']
                assert first <= start_line <= end_line <= last, (book_id, row['title'])
                for n in range(start_line, end_line + 1):
                    if n not in coverage:
                        continue
                    counts = coverage[n]
                    start = span['start_codepoint'] if n == start_line else 0
                    end = span['end_codepoint'] if n == end_line else len(counts)
                    for offset in range(start, end):
                        counts[offset] += 1
        for n, counts in coverage.items():
            for offset, count in enumerate(counts):
                assert count == 1 or lines[n - 1][offset].isspace(), (book_id, n, offset)
