"""武英殿本《南史》兩傳逐欄轉寫、完整取段與人文覆核的固定出處。"""
from hashlib import sha256
import json
from pathlib import Path

RAW = 'source-evidence/nanshi022-wang/wyd-columns.txt'
RAW_SHA = 'e230275bc589cf0c3e2f9aea984d7dbf5508b56aee6f973e8c91095ece6481d6'
PDF_SHA = 'c6b0632b046a75b94b3979d129f2efae5a478386f132326bce47db46b81105b2'
READING = 'source-evidence/nanshi022-wang/wyd-reading.json'
TEXTS = {
    'c-nanshi-022-wangtanshou-wyd': '2340786c6a2794127578203daf587d5e51d03db5e7d0dc14799947a7d2cea2a5',
    'c-nanshi-022-wangsengchuo-wyd': '3657f2ff8aa1065bbd713553a37c1ea95fcf03f196f2676239952004ae796851',
}


def errors(ch, root):
    if ch['id'] not in TEXTS:
        return []
    try:
        root = Path(root).resolve()
        s = ch['source']
        if any((root / rel).resolve() != root / rel for rel in (RAW, READING)):
            raise ValueError('path')
        raw = (root / RAW).read_bytes()
        contract = json.loads((root / READING).read_text())
        assert sha256(raw).hexdigest() == RAW_SHA == s['raw_file_sha256']
        assert s['raw_path'] == RAW and s['image_verified'] is True
        assert s['revision_id'] == 'cbr-ai-transcription-sha256:' + RAW_SHA
        assert ch['annotation']['print_projection_ref'] == READING
        assert ch['annotation']['human_reviewed'] is False and contract['pdf_sha256'] == PDF_SHA
        cols = dict(row.split(maxsplit=1) for row in raw.decode().splitlines())
        full = ''.join(cols.values())
        split = full.index('僧綽幼有大成之度')
        start, stop = (0, split) if 'wangtanshou' in ch['id'] else (split, len(full))
        positions = {}
        pos = 0
        for key, column in cols.items():
            positions[key] = pos
            pos += len(column)
        words = []
        for p in ch['paragraphs']:
            projected = []
            for row in p['source_position']['column_projection']:
                col = cols[row['column']]
                a, b = row['start'], row['end']
                assert 0 <= a < b <= len(col) and col[a:b] == row['text']
                assert positions[row['column']] + a == start
                start += b - a
                projected.append(row['text'])
            assert ''.join(projected) == p['text'] and p['source_position']['revision_id'] == s['revision_id']
            words.append(p['text'])
        assert start == stop
        assert contract['folios'] == '卷二十二一上至四下，即PDF第62面左半至第66面右半。'
        assert sha256('\n\n'.join(words).encode()).hexdigest() == TEXTS[ch['id']] == ch['text_sha256']
        assert contract['biographies'][ch['id']]['paragraphs'] == [p['id'] for p in ch['paragraphs']]
    except (AssertionError, KeyError, ValueError, TypeError, OSError):
        return ['武英殿本南史卷22逐欄轉寫、分傳範圍或原始書影憑據不符']
    return []
