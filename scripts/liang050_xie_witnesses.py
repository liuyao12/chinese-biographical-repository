"""《梁書》謝幾卿、謝徵兩傳的逐行見證及殿本異文。"""
import hashlib
import json
import re
from pathlib import Path

JI = 'c-liangshu-050-xiejiqing-family-intro'
ZHENG = 'c-liangshu-050-xiezheng'
VOLUME_SHA = '46f17adb85a40252096bb10bb6b90ba40178ae6da293368629eded0273320cf8'
READINGS = Path('source-evidence/liang050-family')


def digital_errors(chapter, root, slug, lines):
    source = chapter['source']
    receipt = json.loads((root / READINGS / (slug + '-reading.json')).read_text())
    raw = (root / source['raw_path']).read_bytes()
    if (source['raw_path'] != receipt['raw_path'] or receipt['revision'] != 1514482
            or hashlib.sha256(raw).hexdigest() != receipt['sha256'] or receipt['sha256'] != VOLUME_SHA):
        return ['梁書卷五十數位修訂及來源雜湊不合']
    text = raw.decode()
    raw_lines = text.splitlines(keepends=True)
    for number, paragraph, review in zip(lines, chapter['paragraphs'], receipt['paragraphs'], strict=True):
        position = paragraph['source_position']
        offsets = position['raw_character_offsets']
        lower = sum(map(len, raw_lines[:number-1]))
        if (position['first_line'] != number or position['last_line'] != number
                or number != review['line'] or review['id'] != paragraph['id']
                or offsets != sorted(set(offsets)) or not lower <= offsets[0] <= offsets[-1] < lower + len(raw_lines[number-1])
                or ''.join(text[i] for i in offsets) != paragraph['text']
                or hashlib.sha256(paragraph['text'].encode()).hexdigest() != review['text_sha256']):
            return ['梁書卷五十傳文須由固定原行逐字重建']
    for case, record in zip(chapter['annotation']['source_reading_cases'], receipt['external_comparisons'], strict=True):
        witness = (root / record['path']).read_bytes()
        if (any(record[k] != v for k, v in case.items())
                or hashlib.sha256(witness).hexdigest() != record['sha256']
                or case['reading'] not in witness.decode().splitlines()[record['source_line'] - 1]):
            return ['謝氏兩傳的對讀須可回查固定見證原行']
    return []


def print_errors(chapter, root, slug, pages):
    folder = Path('source-evidence') / ('liang050-' + slug + '-wyd')
    proof = json.loads((root / folder / 'wuying-reading.json').read_text())
    if [r['pdf_page'] for r in proof['images']] != pages:
        return ['謝氏武英殿本缺實校書影']
    source = chapter['source']
    if proof['pdf_url'] != source['url'] or proof['catalog_permalink'] != source['permalink']:
        return ['謝氏武英殿本須連到所核館藏冊及其目錄']
    for image in proof['images']:
        page_url = f"{proof['pdf_url']}#page={image['pdf_page']}"
        if (image['source_url'] != page_url or image['source'] != proof['catalog_permalink']
                or not re.fullmatch('[0-9a-f]{64}', image['capture_sha256'])):
            return ['謝氏武英殿本缺逐頁書影連結或擷取指紋']
    if slug == 'jiqing':
        marks = proof['printed_lacuna_signs']
        if [(m['pdf_page'], m['half'], m['leaf'], m['column_from_right'], m['column_offset'], m['surface'],
             m['text_layer']) for m in marks] != [
                (59, '右', '九下', 7, 17, '缺', 'printed_small_type'),
                (59, '右', '九下', 8, 0, '缺', 'printed_small_type')]:
            return ['謝幾卿答書兩處缺文須依原欄小字分記']
        if '豈云栖缺匪商官缺理就一廛' not in chapter['paragraphs'][3]['text']:
            return ['謝幾卿殿本缺文與匪商官三字須照原影']
    return []


def errors(chapter, root):
    source_id = chapter['id'].removesuffix('-wyd')
    if source_id not in (JI, ZHENG):
        return []
    try:
        slug, lines, pages = ('jiqing', range(41, 52, 2), [57, 58, 59]) if source_id == JI else (
            'xiezheng', range(108, 115, 2), [67, 68])
        problems = (digital_errors(chapter, root, slug, lines) if source_id == chapter['id']
                    else print_errors(chapter, root, slug, pages))
        ann = chapter['annotation']
        paragraphs = {p['id']: p['text'] for p in chapter['paragraphs']}
        for case in ann['source_reading_cases']:
            if paragraphs[case['paragraph_id']][case['start_codepoint']:case['end_codepoint']] != case['source_quote']:
                return ['梁書謝氏對讀字位不合']
        for event in ann['narrative_readings']:
            anchor = event['source_anchor']
            if (paragraphs[anchor['paragraph_id']][anchor['start']:anchor['end']] != anchor['surface']
                    or event['evidence']['quote'] != anchor['surface']):
                return ['梁書謝氏敘事與引文字位不合']
        if source_id == ZHENG:
            ancestors = [r['person_id'] for r in ann['person_reference_occurrences'] if r['surface'] == '高祖']
            if ancestors != ['684_eaa_511'] + ['fo7_f8v_rmf'] * 5:
                return ['傳首高祖景仁與後文五處梁高祖須各繫其人']
            collection = next(e for e in ann['narrative_readings'] if e['event_type'] == 'collection')
            if collection['person_ids'] != ['p93_tgr_t8r_AA', '684_eaa_511_AAAA']:
                return ['王籍為編者，二十卷為謝徵文']
        return problems
    except (KeyError, IndexError, TypeError, ValueError, StopIteration, OSError):
        return ['梁書謝氏兩傳缺原行、葉欄、對讀或人物分指']
