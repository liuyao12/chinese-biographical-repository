"""《列女傳》謝道韞的傳首稱謂及封、胡、羯、末兩本異讀。"""
import hashlib
import json
import re
from pathlib import Path

DIGITAL = 'c-jinshu-096-xiedaoyun'
PRINT = DIGITAL + '-wyd'
SOURCE = Path('source-evidence/jin096-daoyun')
PHOTO = Path('source-evidence/jin096-daoyun-wyd')
DAO = 'aa6_83c_juy_CE'
AN = 'aa6_83c_juy_B'


def uncle_valid(assertion, paragraphs):
    try:
        evidence = assertion['evidence'][0]
        cid, paragraph = paragraphs[evidence['paragraph_id']]
        mentions = {m['id']: m for m in paragraph['mentions']}
        niece = mentions[evidence['subject_person_mention_id']]
        uncle = mentions[evidence['object_person_mention_id']]
        text = paragraph['text']
        return (cid == evidence['chapter_id'] and paragraph['id'] == cid + ':p001'
                and text == evidence['quote'] and assertion['predicate'] == 'paternal_uncle'
                and niece['person_id'] == assertion['subject_person_id'] == DAO
                and uncle['person_id'] == assertion['object_person_id'] == AN
                and niece['surface'] == '道韞' and uncle['surface'] == '安'
                and text[:niece['end']].replace('，', '') == '王凝之妻謝氏字道韞'
                and text[niece['end']:uncle['end']].replace('，', '').replace('。', '') ==
                    '安西將軍奕之女也聰識有才辯叔父安')
    except (KeyError, IndexError, TypeError):
        return False


def errors(chapter, root):
    cid = chapter['id']
    if cid not in (DIGITAL, PRINT):
        return []
    try:
        paragraphs = chapter['paragraphs']
        if len(paragraphs) != 4:
            return ['謝道韞傳須覆蓋四原段']
        expected = ([('封', 'xq1_fn8_dol'), ('謝歆', 'xq1_fn8_dol')] if cid == PRINT
                    else [('封', 'aa6_83c_juy_DB'), ('謝韶', 'aa6_83c_juy_DB')])
        actual = [(m['surface'], m['person_id']) for m in paragraphs[1]['mentions']
                  if m['surface'] in ('封', '謝韶', '謝歆')]
        if actual != [expected[0], *expected]:
            return ['原書兩處封及所解姓名應同指，分別按數位本韶、殿本歆錄']
        if cid == PRINT:
            proof = json.loads((root / PHOTO / 'wuying-reading.json').read_text())
            if [e['pdf_page'] for e in proof['images']] != [50, 51, 52]:
                return ['謝道韞殿本須有三面連續書影']
            leaves = {(c['pdf_page'], c['half'], c['leaf']) for c in proof['columns']}
            if leaves != {(50, '左', '九上'), (51, '右', '九下'), (51, '左', '十上'), (52, '右', '十下')}:
                return ['殿本版心第九、十葉與 PDF 第50至52面不合']
            if proof['pdf_url'] != chapter['source']['url'] or proof['catalog_permalink'] != chapter['source']['permalink']:
                return ['謝道韞殿本書影須連到所核館藏冊及其目錄']
            for row in proof['images']:
                page_url = f"{proof['pdf_url']}#page={row['pdf_page']}"
                if (row['source_url'] != page_url or row['source'] != proof['catalog_permalink']
                        or not re.fullmatch('[0-9a-f]{64}', row['capture_sha256'])):
                    return ['謝道韞殿本缺逐頁書影連結或擷取指紋']
            if '封謂謝歆' not in paragraphs[1]['text'] or '又嘗議玄學植不進' not in paragraphs[1]['text']:
                return ['殿本九下第四、五欄分作歆、議']
        else:
            proof = json.loads((root / SOURCE / 'xiedaoyun-reading.json').read_text())
            data = (root / proof['raw_path']).read_bytes()
            if hashlib.sha256(data).hexdigest() != proof['sha256']:
                return ['謝道韞原書雜湊不合']
            raw = data.decode()
            for n, p in zip((71, 73, 75, 77), paragraphs):
                pos = p['source_position']
                if (pos['first_line'] != n or pos['last_line'] != n
                        or ''.join(raw[i] for i in pos['raw_character_offsets']) != p['text']):
                    return ['謝道韞本傳行號與原字位不合']
            cases = chapter['annotation']['source_reading_cases']
            citations = proof['external_comparisons']
            if len(cases) != len(citations):
                return ['謝道韞引文與固定外證條數不合']
            for case, row in zip(cases, citations):
                b = (root / row['path']).read_bytes()
                t = b.decode()
                offsets = row['raw_character_offsets']
                start = sum(len(l) for l in t.splitlines(keepends=True)[:row['source_line']-1])
                if (hashlib.sha256(b).hexdigest() != row['sha256'] or offsets != sorted(set(offsets))
                        or not start <= offsets[0] <= offsets[-1] < start + len(t.splitlines()[row['source_line']-1])
                        or row['raw_quote'] != t[offsets[0]:offsets[-1]+1]
                        or case['reading'] != ''.join(t[i] for i in offsets) or row['reading'] != case['reading']):
                    return ['謝道韞的跨書見證、劉注或引詩與指定字位不合']
    except (KeyError, ValueError, IndexError, TypeError, OSError):
        return ['謝道韞校讀缺原件、段落或人物錨點']
    return []
