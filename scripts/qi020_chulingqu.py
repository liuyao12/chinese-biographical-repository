"""核對褚令璩、皇子誦的本紀原句與宋本《建康實錄》原欄。"""
import hashlib
import json
from pathlib import Path


def named_prince_valid(assertion, chapter, root):
    try:
        if (chapter['id'] != 'c-nanshi-005-song-emperor-and-mother'
                or chapter['source']['revision_id'] != 2027696):
            return False
        path = Path('source-evidence/qi020-chulingqu/ws2027696.wikitext')
        data = (root / path).read_bytes()
        digest = 'af8387bb9e9b512cf1762d50502f1da2d79128e759128314322c107df6ab2065'
        if (chapter['source']['raw_path'] != str(path) or chapter['source']['raw_file_sha256'] != digest
                or hashlib.sha256(data).hexdigest() != digest):
            return False
        raw = data.decode()
        lines = raw.splitlines(keepends=True)
        if lines[122].strip() != '==廢帝東昏侯==' or any(s.startswith('==') for s in lines[123:138]):
            return False
        accession, son, _ = chapter['paragraphs']
        child_evidence, father_evidence = assertion['evidence']
        for line, p, e, role, label, pid, context in [
                (124, accession, father_evidence, 'object', '寶卷', 'w4m_9tw_147_A', '廢帝東昏侯諱寶卷'),
                (138, son, child_evidence, 'subject', '誦', 'w4m_9tw_147_AA', '立皇子誦為皇太子')]:
            pos = p['source_position']
            offsets = pos['raw_character_offsets']
            base = sum(map(len, lines[:line - 1]))
            mark, = [m for m in p['mentions'] if m['id'] == e[role + '_person_mention_id']]
            start = p['text'].index(context) + context.index(label)
            if (pos['first_line'] != line or pos['last_line'] != line or len(offsets) != len(p['text'])
                    or offsets != sorted(set(offsets)) or offsets[0] < base
                    or offsets[-1] >= base + len(lines[line - 1])
                    or ''.join(raw[i] for i in offsets) != p['text']
                    or e['source_id'] != chapter['source_id'] or e['chapter_id'] != chapter['id']
                    or e['paragraph_id'] != p['id'] or e['quote'] != p['text']
                    or mark['person_id'] != pid or assertion[role + '_person_id'] != pid
                    or (mark['start'], mark['end'], mark['surface']) != (start, start + len(label), label)):
                return False
        return (assertion['predicate'] == 'father' and assertion['status'] == 'source_attested'
                and assertion['qualifiers'] == dict(source_term='立皇子誦為皇太子', lineage='paternal',
                                                     annal_context='nanshi_ming_named_prince')
                and son['text'].startswith('夏四月丙午朔，魏孝文皇帝崩。己巳，立皇子誦為皇太子'))
    except (IndexError, KeyError, OSError, TypeError, ValueError):
        return False


def shaoxing_witness_errors(chapter, root):
    if chapter['id'] != 'c-jiankang-shilu-015-chulingqu-shaoxing':
        return []
    directory = Path('source-evidence/qi020-chulingqu')
    columns = directory / 'shaoxing-columns.txt'
    ledger = directory / 'jiankang-print.json'
    digest = '5b91ebec69e688b2d5edf7432d8db720206bcdc9a26993d5e3b3793174d7161d'
    ledger_digest = '9622bbabdbaf694fa227e84a3af041e6d39975528c05614cf6197e49bee7ba06'
    revision = 'cbr-ai-transcription-sha256:' + digest
    try:
        raw = (root / columns).read_bytes()
        data = (root / ledger).read_bytes()
        source = chapter['source']
        if (hashlib.sha256(data).hexdigest() != ledger_digest or hashlib.sha256(raw).hexdigest() != digest
                or source['raw_path'] != str(columns) or source['raw_file_sha256'] != digest
                or source['revision_id'] != revision):
            return ['宋刊《建康實錄》原欄或校讀底本不合']
        receipt = json.loads(data)
        if (source['permalink'] != receipt['catalogue_permalink'] or source['url'] != receipt['pdf_url']
                or source['edition'] != receipt['edition']
                or chapter['annotation']['biography_source_reviews']['國圖原頁'] != str(ledger)):
            return ['宋刊《建康實錄》所屬版本及冊次不合']
        rows = []
        for page in receipt['images']:
            if (page['source_url'] != f"{receipt['pdf_url']}#page={page['pdf_page']}"
                    or page['catalogue_url'] != receipt['catalogue_permalink']):
                return ['宋刊《建康實錄》所附書影不合']
            rows.extend(dict(pdf_page=page['pdf_page'], half=page['half'], **c) for c in page['columns'])
        lines = [f"{r['pdf_page']} {r['half']} {r['column_from_right']} {r['portion']} {r['text']}" for r in rows]
        if lines != raw.decode().splitlines():
            return ['宋刊《建康實錄》逐欄校記與原欄轉寫不合']
        for p, group in zip(chapter['paragraphs'], [rows[:2], rows[2:4], rows[4:]], strict=True):
            pos = p['source_position']
            text = ''.join(r['text'] for r in group)
            if (p['text'] != text or pos['column_projection'] != group or pos['revision_id'] != revision
                    or pos['projection_sha256'] != hashlib.sha256(text.encode()).hexdigest()):
                return ['宋刊《建康實錄》段落與書影的面、欄、字序不合']
    except (KeyError, OSError, TypeError, ValueError) as exc:
        return [f'宋刊《建康實錄》原欄資料不全（{exc}）']
    return []
