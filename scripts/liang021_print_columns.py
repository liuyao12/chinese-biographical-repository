"""Check the Liang juan 21 witnesses against their recorded Wuyingdian columns."""
import hashlib
import json
from pathlib import Path


WITNESSES = {
    'c-liangshu-021-wangzhi-wyd': ('wangzhi', '6cb11d29f5f1b17fccce41c7ab1b3a1a9407ce97bd0b109ce070c05ba50e8550'),
    'c-liangshu-021-wangzhan-wyd': ('wangzhan', '590434796825e6c8212ce54153d2f891874b28625aadf377aa69ef53f6734473'),
}


def errors(chapter, root):
    if chapter['id'] not in WITNESSES:
        return []
    try:
        slug, digest = WITNESSES[chapter['id']]
        directory = Path('source-evidence') / ('liang021-' + slug)
        transcription = directory / 'wyd-columns.txt'
        raw = (root / transcription).read_bytes()
        source = chapter['source']
        revision = 'cbr-ai-transcription-sha256:' + digest
        if (hashlib.sha256(raw).hexdigest() != digest or source['raw_path'] != str(transcription)
                or source['raw_file_sha256'] != digest or source['revision_id'] != revision
                or source['image_verified'] is not True):
            return ['梁書殿本轉寫與固定來源不合']
        ledger_path = directory / 'wuying-reading.json'
        if chapter['annotation']['print_projection_ref'] != str(ledger_path):
            return ['梁書殿本未連逐欄校記']
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
                return ['梁書殿本段文與欄位不合']
            for part in parts:
                if len(part['text']) != part['end'] - part['start']:
                    return ['梁書殿本欄內字數不合']
                projected.extend((part['pdf_page'], part['half'], part['leaf'],
                                  part['column_from_right'], i, char)
                                 for i, char in enumerate(part['text'], part['start']))
        if projected != observations:
            return ['梁書殿本投影有缺字、改字、重字或葉欄錯置']
        if len(ledger['columns']) != len(rows):
            return ['梁書殿本校記未覆蓋全部欄位']
        offset = 0
        for (page, half, leaf, column, text), record in zip(rows, ledger['columns']):
            if record != dict(pdf_page=int(page), half=half, leaf=leaf, column_from_right=int(column),
                              start_codepoint=offset, end_codepoint=offset + len(text), reading=text):
                return ['梁書殿本校記之葉欄字序不合']
            offset += len(text)
    except (KeyError, IndexError, ValueError, TypeError, OSError):
        return ['梁書殿本缺轉寫、葉欄或逐字校記']
    return []
