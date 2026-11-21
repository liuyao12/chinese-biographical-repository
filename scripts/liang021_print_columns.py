"""Check the complete Wang Zhi witness against the recorded Wuyingdian columns."""
import hashlib
import json
from pathlib import Path


CHAPTER = 'c-liangshu-021-wangzhi-wyd'
DIRECTORY = Path('source-evidence/liang021-wangzhi')
TRANSCRIPTION = DIRECTORY / 'wyd-columns.txt'
DIGEST = '6cb11d29f5f1b17fccce41c7ab1b3a1a9407ce97bd0b109ce070c05ba50e8550'


def errors(chapter, root):
    if chapter['id'] != CHAPTER:
        return []
    try:
        raw = (root / TRANSCRIPTION).read_bytes()
        source = chapter['source']
        revision = 'cbr-ai-transcription-sha256:' + DIGEST
        if (hashlib.sha256(raw).hexdigest() != DIGEST or source['raw_path'] != str(TRANSCRIPTION)
                or source['raw_file_sha256'] != DIGEST or source['revision_id'] != revision
                or source['image_verified'] is not True):
            return ['王志殿本轉寫與固定來源不合']
        ledger_path = DIRECTORY / 'wuying-reading.json'
        if chapter['annotation']['print_projection_ref'] != str(ledger_path):
            return ['王志殿本未連逐欄校記']
        ledger = json.loads((root / ledger_path).read_text())
        rows = [line.split() for line in raw.decode().splitlines()]
        observations = [(int(page), half, leaf, int(column), i, char)
                        for page, half, leaf, column, text in rows for i, char in enumerate(text)]
        projected = []
        for paragraph in chapter['paragraphs']:
            position = paragraph['source_position']
            parts = position['column_projection']
            if (position['revision_id'] != revision
                    or paragraph['text'] != ''.join(part['text'] for part in parts)):
                return ['王志殿本段文與欄位不合']
            for part in parts:
                if len(part['text']) != part['end'] - part['start']:
                    return ['王志殿本欄內字數不合']
                projected.extend((part['pdf_page'], part['half'], part['leaf'],
                                  part['column_from_right'], i, char)
                                 for i, char in enumerate(part['text'], part['start']))
        if projected != observations:
            return ['王志殿本投影有缺字、改字、重字或葉欄錯置']
        if len(ledger['columns']) != len(rows):
            return ['王志殿本校記未覆蓋全部欄位']
        offset = 0
        for (page, half, leaf, column, text), record in zip(rows, ledger['columns']):
            if record != dict(pdf_page=int(page), half=half, leaf=leaf, column_from_right=int(column),
                              start_codepoint=offset, end_codepoint=offset + len(text), reading=text):
                return ['王志殿本校記之葉欄字序不合']
            offset += len(text)
    except (KeyError, IndexError, ValueError, TypeError, OSError):
        return ['王志殿本缺轉寫、葉欄或逐字校記']
    return []
