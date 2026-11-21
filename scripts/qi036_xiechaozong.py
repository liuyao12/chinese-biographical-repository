"""覆核謝超宗傳的原字投影、奏案角色與樂志對讀。"""
import hashlib
import json
from pathlib import Path

DIGITAL = 'c-nanqishu-036-xiechaozong'
PRINT = DIGITAL + '-wyd'
DIRECTORY = Path('source-evidence/nanqi036-xiechaozong')


def errors(chapter, root):
    if chapter.get('id') not in (DIGITAL, PRINT):
        return []
    try:
        paragraphs = chapter['paragraphs']
        by_id = {p['id']: p for p in paragraphs}
        if len(paragraphs) != 18:
            return ['謝超宗全傳應含兩奏及王永先告才卿附敘共十八段']
        evidence = root / DIRECTORY
        annotations = chapter['annotation']
        if chapter['id'] == DIGITAL:
            proof = json.loads((evidence / 'reading.json').read_text())
            raw = (root / proof['source']).read_bytes()
            if hashlib.sha256(raw).hexdigest() != proof['sha256']:
                return ['謝超宗數位見證原檔不合']
            lines = raw.decode().splitlines(keepends=True)
            text = raw.decode()
            for line, p, entry in zip(range(12, 47, 2), paragraphs, proof['paragraphs'], strict=True):
                position = p['source_position']
                offsets = position['raw_character_offsets']
                line_start = sum(map(len, lines[:line-1]))
                if (offsets != sorted(set(offsets)) or offsets != entry['character_offsets']
                        or position['first_line'] != line or position['last_line'] != line
                        or entry['paragraph_id'] != p['id'] or entry['source_line'] != line
                        or not line_start <= offsets[0] <= offsets[-1] < line_start + len(lines[line-1])
                        or ''.join(text[i] for i in offsets) != p['text']):
                    return ['謝超宗數位本段落、固定行號或逐字位不合']
            for entry, case in zip(proof['external_comparisons'], annotations['source_reading_cases'], strict=True):
                witness = (root / entry['path']).read_bytes()
                if (hashlib.sha256(witness).hexdigest() != entry['sha256']
                        or case['reading'] != entry['reading']
                        or case['reading'] not in witness.decode().splitlines()[entry['source_line'] - 1]):
                    return ['謝超宗對讀須回到固定見證的指定行']
        else:
            proof = json.loads((evidence / 'wuying-reading.json').read_text())
            if [r['pdf_page'] for r in proof['images']] != list(range(102, 107)):
                return ['謝超宗武英殿本缺實校書影']
            for r in proof['images']:
                f = DIRECTORY / f"print-{r['pdf_page']}.jpg"
                if str(f) != r['path'] or hashlib.sha256((root / f).read_bytes()).hexdigest() != r['sha256']:
                    return ['謝超宗武英殿本書影與校記不合']
            if '以彰深諐' not in paragraphs[12]['text'] or '\uf039' in paragraphs[12]['text']:
                return ['殿本王逡之奏須依第四葉上第七欄錄諐字']
        for case in annotations['source_reading_cases']:
            p = by_id[case['paragraph_id']]
            if p['text'][case['start_codepoint']:case['end_codepoint']] != case['source_quote']:
                return ['謝超宗對讀的本傳原字失去定位']
        events = annotations['narrative_readings']
        for event in events:
            a = event['source_anchor']
            if by_id[a['paragraph_id']]['text'][a['start']:a['end']] != a['surface']:
                return ['謝超宗敘事錨點與本文不合']
        chao, yuan, yong, cai = 'aa6_83c_juy_CDAABA', 'x6r_6az_6zn', 'tfp_yjk_ts4', 'aa6_83c_juy_CDAABAA'
        punishments = [e['person_ids'][0] for e in events if e['event_type'] == 'disqualification']
        final_reports = {e['event_type']: e['person_ids'][0] for e in events
                         if e['event_type'] in ('death_order', 'exoneration', 'death_in_custody')}
        if punishments != [chao, yuan] or final_reports != dict(death_order=chao, exoneration=cai, death_in_custody=yong):
            return ['兩處禁錮及案末賜盡、見原、獄中自盡須各繫當事人']
    except (KeyError, TypeError, ValueError, IndexError, OSError):
        return ['謝超宗兩本缺段、字位、對讀原件或書影']
    return []
