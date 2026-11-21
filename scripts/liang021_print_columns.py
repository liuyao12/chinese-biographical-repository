"""Check printed chapters against their independently transcribed columns."""
import hashlib
import json
from pathlib import Path


IZUMO_WITNESSES = {
    'c-nanshi-011-wangshunhua-izumo': ('nan011-wangshunhua-izumo', '77d2f1a21c48c878d87f900fd03d3156b7f639e67b37468be5bcefcfac38b621'),
    'c-nanshi-011-wangshaoming-izumo': ('nan011-wangshaoming-izumo', '9e3a8e0b880a45ceadf7a322833788837d9d9257f126eb2567789747a029821a'),
}


WITNESSES = {
    'c-nanqishu-020-wangshunhua-wyd': ('qi020-wangshunhua-wyd', 'c559ccf10d0a5afee67b34cfea4f7f25580140a7950af68fcf8eb9bd4bae13a0'),
    'c-nanqishu-020-wangshaoming-wyd': ('qi020-wangshaoming-wyd', '71d0ab489a03b2bad731f5530bb77007165b996fdd9fdcfd43778dbf5efc850b'),
    'c-songshu-041-xiefanjing-wyd': ('song041-xiefanjing-wyd', '70b06cb997968a23e1aa48bc19d117d96aea587354162371dd5c7c10512c2677'),
    'c-jinshu-096-wangguangnu-wyd': ('jin096-wangguang-wyd', '0ef664a042b38875b8756d1bc58ca37de3c6a6895235613fe1b0b2409f16abb9'),
    'c-jinshu-096-wanghuifeng-wyd': ('jin096-wanghuifeng', 'ead71c226112cad4ca3c9f31cb6030aacc346cd188ac683cc4104ce0e10dbf4b'),
    'c-jinshu-096-xunguan-wyd': ('jin096-zhong-and-guan/xun', '8ec2790f6e17b3cf89a29ab6602e98bdd26f0eef8e9ce8a35fcdf63b3b97392f'),
    'c-jinshu-096-zhongyan-wyd': ('jin096-zhong-and-guan/zhong', 'e3f85ab24772f58e5e2db1a9e8c9c8085493fe8ae46082be1771111997bc5320'),
    'c-jinshu-096-xiedaoyun-wyd': ('jin096-daoyun-wyd', '505fb3b94d3ff23f1894b6d47f41de271453de9bd7574c3e2c60333ec3e61159'),
    'c-liangshu-050-xiezheng-wyd': ('liang050-xiezheng-wyd', '93d3d6c680a33b42bc9b39b58d3f320f659e9644cabc08c3601ab1bacf910fe8'),
    'c-liangshu-050-xiejiqing-family-intro-wyd': ('liang050-jiqing-wyd', 'fe27f7f79551ac89948ed19bb99252ef8e05cc5b72cd62907e1d87c4b78e3227'),
    'c-nanqishu-036-xiechaozong-wyd': ('nanqi036-xiechaozong', 'd752793ccca569b28429b050d8c65fdbf97b11cc0c1a900dea28b4c8bc588dcc'),
    'c-songshu-063-wanghua-wyd': ('song063-wanghua', 'af25bb8b41b9b5bd5d64b33097ec10c46becee267940bbdb2789a8e5effc297a'),
    'c-liangshu-021-wangzhi-wyd': ('liang021-wangzhi', '6cb11d29f5f1b17fccce41c7ab1b3a1a9407ce97bd0b109ce070c05ba50e8550'),
    'c-liangshu-021-wangzhan-wyd': ('liang021-wangzhan', '590434796825e6c8212ce54153d2f891874b28625aadf377aa69ef53f6734473'),
    'c-nanshi-022-wangyun-family-wyd': ('nanshi022-wangyun', '926ceb18b937c6612202ae0e975b51816ffe9fa93ccf09573b64985563a56669'),
}


def errors(chapter, root):
    izumo = chapter['id'] in IZUMO_WITNESSES
    witnesses = IZUMO_WITNESSES if izumo else WITNESSES
    if chapter['id'] not in witnesses:
        return []
    try:
        slug, digest = witnesses[chapter['id']]
        directory = Path('source-evidence') / slug
        transcription = directory / ('izumo-columns.txt' if izumo else 'wyd-columns.txt')
        raw = (root / transcription).read_bytes()
        source = chapter['source']
        revision = 'cbr-ai-transcription-sha256:' + digest
        if (hashlib.sha256(raw).hexdigest() != digest or source['raw_path'] != str(transcription)
                or source['raw_file_sha256'] != digest or source['revision_id'] != revision
                or source['image_verified'] is not True):
            return ['刊本轉寫與固定來源不合']
        ledger_path = directory / ('izumo-reading.json' if izumo else 'wuying-reading.json')
        if chapter['annotation']['print_projection_ref'] != str(ledger_path):
            return ['刊本未連逐欄校記']
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
                return ['刊本段文與欄位不合']
            for part in parts:
                if len(part['text']) != part['end'] - part['start']:
                    return ['刊本欄內字數不合']
                projected.extend((part['pdf_page'], part['half'], part['leaf'],
                                  part['column_from_right'], i, char)
                                 for i, char in enumerate(part['text'], part['start']))
        if projected != observations:
            return ['刊本投影有缺字、改字、重字或葉欄錯置']
        if len(ledger['columns']) != len(rows):
            return ['刊本校記未覆蓋全部欄位']
        offset = 0
        for (page, half, leaf, column, text), record in zip(rows, ledger['columns']):
            if record != dict(pdf_page=int(page), half=half, leaf=leaf, column_from_right=int(column),
                              start_codepoint=offset, end_codepoint=offset + len(text), reading=text):
                return ['刊本校記之葉欄字序不合']
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
            for entry in ledger['images']:
                path = directory / ('print-' + str(entry['pdf_page']) + '.jpg')
                if str(path) != entry['path'] or hashlib.sha256((root / path).read_bytes()).hexdigest() != entry['sha256']:
                    return ['王筠傳所校書影與固定影檔不合']
    except (KeyError, IndexError, ValueError, TypeError, OSError):
        return ['刊本缺轉寫、葉欄或逐字校記']
    return []
