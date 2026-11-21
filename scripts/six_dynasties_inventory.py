"""以固定卷目及原文校驗逐傳清冊，分報卷目與逐傳進度。"""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAGES = ('entry_checked', 'full_text', 'first_pass', 'item_reviewed')


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
    counts = dict.fromkeys(STAGES, 0)
    for entry in inventory['biographies']:
        book, title = entry['book_id'], entry['title']
        survey, lines = witnesses[book]
        first, last = entry['first_line'], entry['last_line']
        start, end = entry['start_codepoint'], entry['end_codepoint']
        assert 1 <= first <= last <= len(lines) and 0 <= start < len(lines[first-1])
        assert 0 < end <= len(lines[last-1]) and (first < last or start < end)
        key = (book, first, start, last, end)
        assert key not in ids, title
        ids.add(key)
        selected = lines[first-1:last]
        selected[-1] = selected[-1][:end]
        selected[0] = selected[0][start:]
        assert selected[0].startswith(entry['opening']) and selected[-1].endswith(entry['closing']), title
        flags = [entry[s] for s in STAGES]
        assert all(type(f) is bool for f in flags) and flags == sorted(flags, reverse=True), title
        for stage in STAGES:
            counts[stage] += entry[stage]
        cid = entry['chapter_id']
        if not cid:
            assert not entry['full_text'], title
            continue
        assert progress[cid]['book_id'] == book and entry['item_reviewed'] == progress[cid]['complete'], cid
        if entry['full_text']:
            work, filename = cid[2:].split('-', 1)
            chapter = load(f'corpus/{work}/{filename}.json')
            assert chapter['id'] == cid and chapter['source']['revision_id'] == survey['revision']
            paragraphs = [re.sub(r'<ref>[^<>]*</ref>', '', line) for line in selected if line.strip()]
            assert paragraphs == [p['text'] for p in chapter['paragraphs']], title
            if entry['item_reviewed']:
                assert all(p['annotation_status'] == 'reviewed' for p in chapter['paragraphs'])
    return candidates, counts


if __name__ == '__main__':
    books, counts = verify()
    print(f'六朝候選卷 {len(books)}。已登記傳目的各階段：', counts)
