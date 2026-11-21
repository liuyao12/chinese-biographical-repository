"""逐字核王筠的家世外證、昭明太子哀冊與保誌墓所碑銘。"""
from hashlib import sha256
from pathlib import Path
import json

UNITS = 'source-evidence/wangyun-external/units.json'
DIGEST = 'f70a20d9f0e9ed32020180210c47bdfdfc51f2c4c1ee252f947495d29c31e583'
CHAPTERS = ('c-suishu-076-wangzhou-wangyun', 'c-liangshu-021-wangtai-wangyun', 'c-liangshu-008-xiaotong-wangyun', 'c-gaosengzhuan-010-baozhi-wangyun')


def checked(root, name, digest):
    root = Path(root).resolve()
    path = root / name
    if path.resolve() != path or not path.is_relative_to(root):
        raise ValueError('憑據路徑')
    raw = path.read_bytes()
    if sha256(raw).hexdigest() != digest:
        raise ValueError('固定見證指紋')
    return raw.decode('utf-8')


def evidence(ch, p):
    return dict(work_id=ch['work_id'], book_id=ch['book_id'], source_id=ch['source_id'],
                chapter_id=ch['id'], paragraph_id=p['id'], quote=p['text'])


def exact(p, a):
    i, j = a['start'], a['end']
    return (a['paragraph_id'] == p['id'] and type(i) == type(j) == int
            and 0 <= i < j <= len(p['text']) and p['text'][i:j] == a['surface'])


def errors(ch, root):
    if ch['id'] not in CHAPTERS:
        return []
    try:
        entry = json.loads(checked(root, UNITS, DIGEST))[ch['id']]
        s = ch['source']
        if ((s['revision_id'], s['raw_path'], s['raw_file_sha256'], ch['source_id']) !=
                (entry['revision'], entry['raw_path'], entry['raw_sha256'], entry['source_id'])
                or s['image_verified'] is not False):
            raise ValueError('版本與來源')
        raw = checked(root, entry['raw_path'], entry['raw_sha256'])
        ps = ch['paragraphs']
        positions = [p['source_position'] for p in ps]
        dump = json.dumps(positions, indent=2, ensure_ascii=False) + '\n'
        if sha256(dump.encode()).hexdigest() != entry['source_position_sha256']:
            raise ValueError('原始行界')
        for i, p in enumerate(ps, 1):
            ix = p['source_position']['raw_character_offsets']
            if (p['id'] != ch['id'] + f':p{i:03}' or ix != sorted(set(ix))
                    or ''.join(raw[n] for n in ix) != p['text']):
                raise ValueError('原字序')
        text = '\n\n'.join(p['text'] for p in ps)
        if sha256(text.encode()).hexdigest() != ch['text_sha256'] or ch['text_sha256'] != entry['text_sha256']:
            raise ValueError('篇文')
        items = ch['annotation'].get('commemorative_writing_events', [])
        if items != entry['writing_events']:
            raise ValueError('冊碑銘的作者、受文者、地點或角色')
        for item in items:
            p, = (p for p in ps if p['id'] == item['source_anchor']['paragraph_id'])
            if item['evidence'] != [evidence(ch, p)]:
                raise ValueError('書寫所據原段')
            anchors = [item['source_anchor'], item['work_form_anchor'], item['location_anchor']]
            if not all(exact(p, a) for a in anchors if a is not None):
                raise ValueError('書寫動詞、文體與置所')
            for role in item['roles'].values():
                if role is None:
                    continue
                if 'person_mention_id' in role:
                    mid = role['person_mention_id']
                    candidates = (m for m in p['mentions'] if m['kind'] == 'person')
                else:
                    mid = role['person_reference_id']
                    candidates = (r for r in ch['annotation']['person_reference_occurrences']
                                  if r['paragraph_id'] == p['id'] and r['referent_role'] == 'third_person')
                m, = (m for m in candidates if m['id'] == mid)
                if m['person_id'] != role['person_id'] or not exact(p, dict(m, paragraph_id=p['id'])):
                    raise ValueError('角色姓名或稱謂')
            for other in item.get('parallel_evidence', []):
                line = checked(root, other['raw_path'], other['raw_sha256']).splitlines()[other['source_line']-1]
                if line[other['line_start']:other['line_end']] != other['quote']:
                    raise ValueError('南史對讀段')
        if ch['work_id'] == 'w-gaosengzhuan':
            end = raw.index('</teiHeader>') + len('</teiHeader>')
            if (s['original_header_sha256'] != sha256(raw[:end].encode()).hexdigest()
                    or s['rights'] != 'Available for non-commercial use when distributed with this header intact.'
                    or s['rights'] not in raw[:end] or s['complete_source_sha256'] != '9ee19e1a9706692b1ace92e84188b036e95d8592d73e13a8b2ae886c47717a7e'):
                raise ValueError('CBETA 原始檔、授權聲明或完整檔頭')
        return []
    except (IndexError, KeyError, TypeError, ValueError, OSError):
        return ['王筠家世、詔撰哀冊或保誌碑銘的固定原字、角色、置所及引用來源不符']


def kinship_errors(rows, ch, root):
    if ch['id'] not in CHAPTERS:
        return []
    try:
        frame = json.loads(checked(root, UNITS, DIGEST))[ch['id']]['relations']
        if rows != frame or errors(ch, root):
            raise ValueError('親屬陳述被交換或混入')
        for a in rows:
            e, = a['evidence']
            p, = (p for p in ch['paragraphs'] if p['id'] == e['paragraph_id'])
            if a['qualifiers']['source_term'] not in p['text']:
                raise ValueError('親屬字')
            for key in ('subject', 'object'):
                m, = (m for m in p['mentions'] if m['id'] == e[key+'_person_mention_id'])
                if m['person_id'] != a[key+'_person_id'] or not exact(p, dict(m, paragraph_id=p['id'])):
                    raise ValueError('親屬兩端')
        return []
    except (IndexError, KeyError, TypeError, ValueError, OSError):
        return ['王胄傳所述祖、父及王泰之父、慈與志長幼須逐句繫於具名端點']
