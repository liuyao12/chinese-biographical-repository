"""核對《列女傳》鍾氏、荀灌兩傳的固定數位本及影印殿本。"""
import hashlib
import json
from pathlib import Path


DIRECTORY = Path('source-evidence/jin096-zhong-and-guan')
DIGITAL = 'c-jinshu-096-lienv'
PRINT = {
    'c-jinshu-096-zhongyan-wyd': ('zhong', [(45, '右', '三下', [10]),
                                       (45, '左', '四上', range(1, 11)),
                                       (46, '右', '四下', [1, 2])]),
    'c-jinshu-096-xunguan-wyd': ('xun', [(50, '右', '八下', [10]),
                                        (50, '左', '九上', range(1, 6))]),
}


def load(root, path):
    return json.loads((root / path).read_text(encoding='utf-8'))


def digest(data):
    return hashlib.sha256(data).hexdigest()


def errors(chapter, root):
    cid = chapter['id']
    if cid != DIGITAL and cid not in PRINT:
        return []
    try:
        paragraphs = chapter['paragraphs']
        if cid == DIGITAL:
            proof = load(root, DIRECTORY / 'digital-reading.json')
            data = (root / proof['path']).read_bytes()
            if digest(data) != proof['sha256']:
                return ['荀灌與鍾氏數位本修訂雜湊不合']
            raw = data.decode()
            if len(paragraphs) != 4:
                return ['荀灌一段、鍾氏三個既發段號須齊備']
            for p, line in zip(paragraphs, (68, 26, 26, 28)):
                pos = p['source_position']
                offsets = pos['raw_character_offsets']
                if (pos['first_line'] != line or offsets != sorted(set(offsets))
                        or ''.join(raw[j] for j in offsets) != p['text']):
                    return ['荀灌、鍾氏固定行及投影字位不合']
            cases = {v['id']: v for v in chapter['annotation']['source_reading_cases']}
            for v in proof['comparisons']:
                case = cases[v['id']]
                b = (root / v['path']).read_bytes()
                text = b.decode()
                first, last = v['raw_start'], v['raw_end']
                lines = text.splitlines(keepends=True)
                beginning = sum(map(len, lines[:v['raw_line'] - 1]))
                if (digest(b) != v['sha256'] or v['reading'] != case['reading']
                        or not beginning <= first < last <= beginning + len(lines[v['raw_line'] - 1])
                        or text[first:last] != v['reading']):
                    return ['鍾氏外證未對應其原句與行位']
            return []
        slug, parts = PRINT[cid]
        proof = load(root, DIRECTORY / slug / 'wuying-reading.json')
        data = (root / proof['column_file']).read_bytes()
        if digest(data) != proof['column_file_sha256'] or digest(data) != chapter['source']['raw_file_sha256']:
            return ['殿本欄錄雜湊與原生篇不合']
        expected = [(page, side, leaf, col) for page, side, leaf, cols in parts for col in cols]
        columns = proof['columns']
        coords = [(r['pdf_page'], r['half'], r['leaf'], r['column_from_right']) for r in columns]
        lines = [f"{page} {side} {leaf} {col} {r['reading']}" for (page, side, leaf, col), r in zip(coords, columns)]
        full = ''.join(p['text'] for p in paragraphs)
        if coords != expected or data.decode().splitlines() != lines or full != ''.join(r['reading'] for r in columns):
            return ['殿本欄次、葉碼或正文與逐欄稿不合']
        for img in proof['images']:
            if digest((root / img['path']).read_bytes()) != img['sha256']:
                return ['殿本書影與逐欄校記不合']
        if {img['pdf_page'] for img in proof['images']} != {page for page, *_ in expected}:
            return ['原生篇所據書影缺面']
        if slug == 'xun' and not all(term in full for term in ('年十三乃率勇士數十人', '子撫率三千人')):
            return ['荀灌所率與周撫援軍人數須各從原欄']
        if slug == 'zhong' and '鍾夫人之禮郝夫人之法' not in full:
            return ['殿本四下夫人之姓作鍾']
    except (KeyError, IndexError, TypeError, ValueError, OSError):
        return ['荀灌、鍾氏數位本或殿本缺核對原件']
    return []
