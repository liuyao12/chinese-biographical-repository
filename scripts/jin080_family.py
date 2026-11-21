"""核《世說》劉注自案的字位與引文邊界，及王楨之問答所指叔。"""
import hashlib


def liu_note_valid(paragraph, chapter, root):
    try:
        passages = {
            'c-shishuoxinyu-008-jin067-xichao:courtesy': (
                '嘉賓，郗超小字也。阿源，殷浩也。', '朝廷用違其才耳。」{{*|', '}}'),
            'c-shishuoxinyu-008-jin098-wang-family:note': (
                '舒、邃並敦從弟。', '累遷中領軍、尚書左僕射。」', '}}最是臣少所知拔'),
            'c-shishuoxinyu-026-jin076-wangpeng:nickname': (
                '虎㹠，王彭之小字也。', '。」{{*|', '王氏譜曰：「'),
            'c-shishuoxinyu-009-wang080-short:liunote': (
                '第七叔，獻之也。', '。歷侍中、大司馬長史。」', '}}于時賓客'),
            'c-shishuoxinyu-017-wang080-short:liunote': (
                '獻之以泰元十三年卒，年四十五。', '而子敬先亡。{{*|', '}}子猷問左右'),
        }
        text, before, after = passages[paragraph['id']]
        q, s = paragraph['source_quote'], chapter['source']
        raw = (root / s['raw_path']).read_bytes()
        source = raw.decode('utf-8')
        a, b = q['raw_start'], q['raw_end']
        return (chapter['work_id'] == 'w-shishuoxinyu' and paragraph['id'].startswith(chapter['id'] + ':')
                and paragraph['text_layer'] == 'witness_appended_liuxiaobiao_note'
                and paragraph['attribution'] == {'annotator': '劉孝標', 'quoted_work': None}
                and q['source_layer'] == '劉孝標注' and s['raw_file_sha256'] == hashlib.sha256(raw).hexdigest()
                and 0 <= a < b <= len(source) and q['raw_line'] == source[:a].count('\n') + 1
                and source[:a].endswith(before) and source[b:].startswith(after)
                and paragraph['text'] == text == source[a:b] == q['quote'])
    except (KeyError, TypeError, ValueError, OSError):
        return False


def named_uncle_valid(assertion, paragraphs):
    try:
        e, note = assertion['evidence']
        cid, p = paragraphs[e['paragraph_id']]
        ncid, n = paragraphs[note['paragraph_id']]
        named = {m['id']: m for m in p['mentions'] + n['mentions'] if m['kind'] == 'person'}
        child, uncle = named[e['subject_person_mention_id']], named[note['object_person_mention_id']]
        return (cid == ncid == 'c-shishuoxinyu-009-wang080-short'
                and e['chapter_id'] == note['chapter_id'] == cid
                and assertion['predicate'] == 'paternal_uncle'
                and e['quote'] == p['text'] and note['quote'] == n['text']
                and p['text_layer'] == 'received_chapter' and n['text_layer'] == 'witness_appended_liuxiaobiao_note'
                and p['text'][child['start']:child['end']] == child['surface'] == '王楨之'
                and p['text'][child['end']:] == '曰：「我何如卿第七叔？」'
                and n['text'] == '第七叔，獻之也。' and n['text'][uncle['start']:uncle['end']] == uncle['surface'] == '獻之'
                and assertion['subject_person_id'] == child['person_id'] and assertion['object_person_id'] == uncle['person_id']
                and child['person_id'] != uncle['person_id'] and assertion['qualifiers']['source_term'] == '第七叔')
    except (KeyError, TypeError, ValueError, IndexError):
        return False
