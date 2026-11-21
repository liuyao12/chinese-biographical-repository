"""明敬皇后的婚配、身後贈號及同句父母受贈。"""

WIFE = 'gjl_f5h_2a6_A'
EMPEROR = 'w4m_9tw_147'
FATHER = 'gjl_f5h_2a6'
MOTHER = 'q20_pas_ain'
CHAPTERS = {
    'c-nanqishu-020-xietiao-jing': ('太祖', '高宗'),
    'c-nanqishu-020-xietiao-jing-wyd': ('太祖', '高宗'),
    'c-nanshi-011-liuhuiduan': ('高帝', '明帝'),
    'c-nanshi-011-liuhuiduan-izumo': ('高帝', '明帝'),
}


def marriage_valid(assertion, evidence, chapter):
    try:
        high, ming = CHAPTERS[chapter['id']]
        term = high + '為' + ming + '納之'
        paragraph, = chapter['paragraphs']
        text = paragraph['text']
        wife = next(m for m in paragraph['mentions'] if m['id'] == evidence['subject_person_mention_id'])
        spouse = next(r for r in chapter['annotation']['person_reference_occurrences']
                      if r['id'] == evidence['object_person_reference_id'])
        start = text.index(term) + len(high + '為')
        return (assertion['predicate'] == 'spouse' and assertion['subject_person_id'] == wife['person_id'] == WIFE
                and assertion['object_person_id'] == spouse['person_id'] == EMPEROR
                and assertion['qualifiers']['source_term'] == term and assertion['evidence'] == [evidence]
                and evidence['chapter_id'] == chapter['id'] and evidence['source_id'] == chapter['source_id']
                and evidence['paragraph_id'] == spouse['paragraph_id'] == paragraph['id']
                and evidence['quote'] == text and wife['surface'] == text[wife['start']:wife['end']] == '惠端'
                and (spouse['start'], spouse['end'], spouse['surface']) == (start, start + len(ming), ming))
    except (IndexError, KeyError, StopIteration, TypeError, ValueError):
        return False


def grant_valid(holding, paragraphs, mentions):
    try:
        basis = holding['posthumous_basis']
        evidence, = basis['evidence']
        attestation, = holding['attestations']
        cid, p = paragraphs[evidence['paragraph_id']]
        high, ming = CHAPTERS[cid]
        text = p['text']
        father_grant = '贈父通直郎景猷' + ('為' if ming == '明帝' else '') + '金紫光祿大夫'
        grants = {
            '宣城王妃': (WIFE, '惠端', '贈宣城王妃'),
            '金紫光祿大夫': (FATHER, '景猷', father_grant),
            '平陽鄉君': (MOTHER, '王氏', '母王氏平陽鄉君'),
        }
        pid, name, term = grants[holding['title']]
        owner_cid, owner_pid, owner = mentions[attestation['person_mention_id']]
        start = text.index(term) + term.index(holding['title'])
        period = holding['effective_period']['start']
        return (holding['mode'] == 'posthumous_grant' and holding['person_id'] == pid == owner['person_id']
                and owner_cid == evidence['chapter_id'] == cid and owner_pid == attestation['paragraph_id'] == p['id']
                and evidence['source_id'] == holding['evidence'][0]['source_id']
                and owner['surface'] == text[owner['start']:owner['end']] == name
                and basis['kind'] == 'qi020_huiduan_named_gifts' and basis['source_term'] == evidence['quote'] == term
                and period['status'] == 'source_event' and period['event_type'] == 'posthumous_grant'
                and period['evidence'] == [evidence]
                and (attestation['start'], attestation['end'], attestation['surface']) ==
                    (start, start + len(holding['title']), holding['title'])
                and text.index('永明七年') < text.index('卒') < text.index('延興元年') < text.index('贈宣城王妃')
                and father_grant + '母王氏平陽鄉君' in text.replace('，', ''))
    except (IndexError, KeyError, TypeError, ValueError):
        return False


def wenxuan_errors(chapter, root):
    """以同一印頁的署名、小行與兩個數位原層核對哀策題注。"""
    import hashlib
    import json
    from pathlib import Path

    prefix = 'c-wenxuan-058-huiduan-'
    if not chapter['id'].startswith(prefix):
        return []
    layer = chapter['id'][len(prefix):]
    directory = Path('source-evidence/qi020-liuhuiduan')
    digests = {
        'shan': 'cfed372a11a77cb11a9d838d6d319e64dc267fb00441c8d42561b07ad12e1eca',
        'liang': '9ead9b60cdd11b77661c4b2cb1200b2e81994ac13fe81be811c923bce025b2e4',
        'received': '0513e28748db941c92e346d211056a8bc96823016897b9c435ba16be741221e0',
        'aice': '0513e28748db941c92e346d211056a8bc96823016897b9c435ba16be741221e0',
    }
    try:
        source = chapter['source']
        printed = layer in ('shan', 'liang')
        raw_path = directory / (f'1574-{layer}-columns.txt' if printed else 'ws2004220.wikitext')
        data = (root / raw_path).read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        if (source['raw_path'] != str(raw_path) or digest != digests[layer]
                or source['raw_file_sha256'] != digest or source['image_verified'] is not printed):
            return ['哀策正文及兩家題注須連到各自的固定本。']
        receipt = json.loads((root / directory / 'wenxuan-witnesses.json').read_bytes())
        witness = receipt['witnesses'][chapter['id']]
        if witness['raw_sha256'] != digest or witness['raw_path'] != str(raw_path):
            return ['哀策題注原件紀錄與該層不符。']
        paragraphs = chapter['paragraphs']
        if printed:
            paragraph, = paragraphs
            image = receipt['image']
            photo_hash = 'd0f3b01eb815e62131b21ee22c9ad1d5be91a3ad6f06e285448521de40b42bf3'
            if (image != dict(pdf_page=47, source_url=receipt['pdf_url'] + '#page=47',
                              capture_sha256=photo_hash, catalogue_url=source['permalink'])
                    or receipt['pdf_url'] != source['url']
                    or receipt['file_description_revision'] != 1130546999):
                return ['六臣本須指明國家圖書館藏本第47面原影。']
            columns = []
            for row in data.decode().splitlines():
                page, half, column, small, text = row.split()
                columns.append(dict(pdf_page=int(page), half=half, column_from_right=int(column),
                                    small_column=small, text=text))
            if (paragraph['source_position']['column_projection'] != columns
                    or paragraph['text'] != ''.join(col['text'] for col in columns)):
                return ['六臣本文字或雙行次序與原欄不合。']
        else:
            raw = data.decode()
            lines = raw.splitlines(keepends=True)
            expected_lines = [53, 55] if layer == 'aice' else [49]
            if len(paragraphs) != len(expected_lines):
                return ['哀策篇首須分存署名、正文與篇題注文。']
            for p, line in zip(paragraphs, expected_lines):
                pos = p['source_position']
                offsets = pos['raw_character_offsets']
                first = sum(map(len, lines[:line - 1]))
                if (pos['first_line'] != line or pos['last_line'] != line
                        or offsets != sorted(set(offsets)) or offsets[0] < first
                        or offsets[-1] >= first + len(lines[line - 1])
                        or ''.join(raw[n] for n in offsets) != p['text']):
                    return ['哀策人物、正文或夾注的原始字位錯置。']
        if layer == 'aice':
            if (paragraphs[0]['text'] != '謝玄暉' or paragraphs[1]['text'] !=
                    '惟永泰元年。秋九月朔日，敬皇后梓宮啟自先塋，將祔于某陵。'):
                return ['須保存謝玄暉署名、秋九月朔啟梓宮與「將祔」之原文。']
            return []
        stem = '058-huiduan-' + layer
        kin, = json.loads((root / 'corpus/wenxuan' / (stem + '-assertions.json')).read_bytes())['assertions']
        paragraph, = paragraphs
        evidence, = kin['evidence']
        marks = {m['id']: m for m in paragraph['mentions']}
        named = marks[evidence['subject_person_mention_id']]
        relative = marks[evidence['object_person_mention_id']]
        name, ancestor, term, role = (('端惠', '弘道', '孫', 'grandfather') if layer == 'liang'
                                      else ('惠端', '道弘', '女', 'father'))
        if (kin['subject_person_id'] != named['person_id'] or named['person_id'] != WIFE
                or kin['object_person_id'] != relative['person_id'] or relative['person_id'] != 'vus_7f1_rrz'
                or kin['predicate'] != role or kin['qualifiers']['source_term'] != ancestor + term
                or named['surface'] != name or relative['surface'] != ancestor
                or not paragraph['text'][relative['start']:].startswith(ancestor + term)
                or evidence['chapter_id'] != chapter['id'] or evidence['paragraph_id'] != paragraph['id']
                or evidence['source_id'] != chapter['source_id'] or evidence['quote'] != paragraph['text']):
            return ['兩家注文的親稱、所指及原字必須各守本層。']
    except (IndexError, KeyError, OSError, TypeError, ValueError):
        return ['哀策見證缺固定原件、欄位或具名端點。']
    return []
