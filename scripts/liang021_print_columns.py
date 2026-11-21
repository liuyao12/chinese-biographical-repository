"""Check native Wuyingdian chapters against their independently transcribed columns."""
import hashlib
import json
import re
from pathlib import Path


WITNESSES = {
    'c-liangshu-021-wangzhi-wyd': ('liang021-wangzhi', '6cb11d29f5f1b17fccce41c7ab1b3a1a9407ce97bd0b109ce070c05ba50e8550'),
    'c-liangshu-021-wangzhan-wyd': ('liang021-wangzhan', '590434796825e6c8212ce54153d2f891874b28625aadf377aa69ef53f6734473'),
    'c-nanshi-022-wangyun-family-wyd': ('nanshi022-wangyun', '926ceb18b937c6612202ae0e975b51816ffe9fa93ccf09573b64985563a56669'),
}


def errors(chapter, root):
    if chapter['id'] not in WITNESSES:
        return []
    try:
        slug, digest = WITNESSES[chapter['id']]
        directory = Path('source-evidence') / slug
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
        if chapter['id'] == 'c-nanshi-022-wangyun-family-wyd':
            notes = chapter['annotation']['printed_phonetic_glosses']
            if notes != ledger['printed_phonetic_glosses'] or len(notes) != 2:
                return ['王筠傳兩處反切與書影校記不合']
            paragraph = chapter['paragraphs'][2]
            paragraph_cells = [(part['pdf_page'], part['half'], part['column_from_right'], index, char)
                               for part in paragraph['source_position']['column_projection']
                               for index, char in enumerate(part['text'], part['start'])]
            for note, (column, gloss) in zip(notes, [(9, '五的反'), (10, '五兮反')]):
                location = [(p, h, col, index, char) for p, h, _, col, index, char in observations
                            if p == 84 and h == '左' and col == column and char == '霓']
                _, _, _, index, _ = location[0]
                if (len(location) != 1 or note['pdf_page'] != 84 or note['half'] != '左'
                        or note['leaf'] != '二十三上' or note['column_from_right'] != column
                        or note['headword_column_offset'] != index or note['headword'] != '霓'
                        or note['text_layer'] != 'printed_small_type' or note['gloss'] != gloss
                        or note['paragraph_id'] != paragraph['id']
                        or paragraph_cells[note['headword_start']] != location[0]):
                    return ['王筠傳反切須繫原欄的霓字']
            if [entry['pdf_page'] for entry in ledger['images']] != [84, 85, 86]:
                return ['王筠傳須附連續三頁原影']
            if ledger['pdf_url'] != source['url'] or ledger['catalog_permalink'] != source['permalink']:
                return ['王筠傳書影須連到所核館藏冊及其目錄']
            for entry in ledger['images']:
                page_url = f"{ledger['pdf_url']}#page={entry['pdf_page']}"
                if (entry['source_url'] != page_url or entry['source'] != ledger['catalog_permalink']
                        or not re.fullmatch('[0-9a-f]{64}', entry['capture_sha256'])):
                    return ['王筠傳缺原影逐頁連結或擷取指紋']
    except (KeyError, IndexError, ValueError, TypeError, OSError):
        return ['梁書殿本缺轉寫、葉欄或逐字校記']
    return []
