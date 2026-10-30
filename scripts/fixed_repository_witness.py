"""Finite reviewed repository projections; receipt integrity is not glyph certification."""
import hashlib
import json
from pathlib import Path
try:
    from .witness_projection import repository_positions
except ImportError:
    from witness_projection import repository_positions

# Only a code-reviewed receipt can activate this gate. Data ownership tags grant nothing.
RECEIPTS = {'c-jinshu-043-wyd1739-wangrong': (
    's-jinshu-043-wyd1739-wangrong',
    'source-evidence/jin043-wyd1739-wangrong/ner-witness-contract.json',
    'db860c122a9b32753f4a1068ee37cfbf6948fc968c8c35b3d0bff6a22f90a14f')}

def need(ok, message):
    if not ok:
        raise ValueError('固定儲存庫見證：' + message)

def same(a, b):
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(same(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    return a == b

def expand(value, roles):
    if isinstance(value, str) and value.startswith('$'):
        need(value in roles, '未知來源角色')
        return roles[value]
    if isinstance(value, list):
        return [expand(x, roles) for x in value]
    if isinstance(value, dict):
        return {k: expand(v, roles) for k, v in value.items()}
    return value

def inside(root, rel):
    rel = Path(rel)
    need(not rel.is_absolute() and '..' not in rel.parts, '路徑不可攜')
    path = (root / rel).resolve()
    need(path.is_relative_to(root), '路徑越界')
    return path

def validate_source(chapter, root, people=None, records=None):
    root = Path(root).resolve()
    cid = chapter['id']
    need(cid in RECEIPTS, '未登記來源')
    sid, rel, sha = RECEIPTS[cid]
    raw_receipt = inside(root, rel).read_bytes()
    need(hashlib.sha256(raw_receipt).hexdigest() == sha, '完整契約SHA不符')
    receipt = json.loads(raw_receipt)
    def read(path):
        return json.loads(inside(root, path).read_bytes())
    need(chapter.get('source_id') == sid == receipt['source_id'], '來源維度不符')
    need(same(read(receipt['chapter_path']), chapter), '現役章與傳入章不一致')
    if people is None:
        people = {p['id']: p for p in read('registry/persons.json')['persons']}
    if records is not None:
        supplied = [r for r in records if r.get('record_type') == 'marked_chapter' and r.get('id') == cid]
        need(len(supplied) == 1 and same(supplied[0], chapter), 'catalog缺完整現役章')
    seed = read(receipt['seed_path'])
    mids = {m['id']: (p, m) for p in seed['paragraphs'] for m in p['mentions']}
    roles = {}
    for role in receipt['roles']:
        spec = role['seed']
        need(all(seed.get(k) == spec[k] for k in ('work_id', 'book_id', 'source_id'))
             and seed['id'] == spec['chapter_id'] and same(seed['source'], spec['source']), 'seed完整來源漂移')
        p, m = mids[spec['marker']['id']]
        need(p['id'] == spec['paragraph_id'] and p['text'] == spec['quote']
             and all(same(m.get(k), v) for k, v in spec['marker'].items()), 'seed全段／錨漂移')
        pid = m.get('person_id')
        need(m.get('kind') in ('person', 'pronoun') and pid in people and people[pid].get('status') != 'retired', 'seed非現役人物')
        person = people[pid]
        need(same([e for e in person.get('evidence', []) if e.get('mention_id') == m['id']], [spec['reverse_evidence']]), 'seed反向引文不符')
        need(m.get('kind') == 'pronoun' or any(a.get('surface') == m['surface'] and m['id'] in a.get('mention_ids', []) for a in person.get('aliases', [])), 'seed alias反查不符')
        need(all(mids[mid][1].get('kind') in ('person', 'pronoun') and mids[mid][1].get('person_id') == pid for mid in role['all_seed_mids']), '同角色來源端點不一致')
        roles['$' + role['key']] = pid
    # Do not require distinct PIDs: a later evidenced cross-role reconciliation can be legitimate.
    need(same(chapter, expand(receipt['chapter_template'], roles)), '完整正文／NER／資格不符')
    for p in chapter['paragraphs']:
        for m in p['mentions']:
            if m['kind'] not in ('person', 'pronoun'):
                continue
            person = people[m['person_id']]
            expected = {k: chapter[k] for k in ('work_id', 'book_id', 'source_id')}
            expected.update(chapter_id=cid, paragraph_id=p['id'], mention_id=m['id'], quote=m['surface'])
            need(same([e for e in person.get('evidence', []) if e.get('mention_id') == m['id']], [expected]), '新章反向引文不符')
            need(m.get('kind') == 'pronoun' or any(a.get('surface') == m['surface'] and m['id'] in a.get('mention_ids', []) for a in person.get('aliases', [])), '新章alias反查不符')
    for path, template in receipt['sidecars'].items():
        expected = expand(template, roles)
        need(same(read(path), expected), '姓名／同指側檔不符')
        if records is not None:
            need(sum(same(r, expected) for r in records) == 1, 'catalog缺完整側檔')
    for path, digest in receipt['fixed_files'].items():
        need(hashlib.sha256(inside(root, path).read_bytes()).hexdigest() == digest, '固定轉錄文件SHA不符')
    raw = inside(root, receipt['raw_path']).read_bytes()
    lines = raw.decode().splitlines()
    need(len(lines) == receipt['line_count'] and sum(map(len, lines)) == receipt['character_count']
         and sum(t.count('〓') for t in lines) == receipt['unknown_count'], '原列／字數／疑字不符')
    points = []
    for p in chapter['paragraphs']:
        projected, digest = repository_positions(root, p, lines)
        need(digest == hashlib.sha256(raw).hexdigest(), '投影raw SHA不符')
        points.extend(projected)
    need(points == [(n, i) for n, t in enumerate(lines, 1) for i in range(len(t))], '轉錄投影非完整唯一順序')
    return roles

def source_errors(chapter, root, source_path=None):
    if not isinstance(chapter, dict):
        return []
    at_owned_path = source_path is not None and Path(source_path).resolve() == (Path(root) / 'corpus/jinshu/043-wyd1739-wangrong.json').resolve()
    if not at_owned_path and chapter.get('id') not in RECEIPTS and chapter.get('source_id') not in {s[0] for s in RECEIPTS.values()}:
        return []
    try:
        validate_source(chapter, root)
        return []
    except (ValueError, TypeError, KeyError, OSError, UnicodeError, StopIteration, IndexError) as exc:
        return ['固定儲存庫見證：' + str(exc)]

def guard_bundle(root, person_id, people, records):
    for cid in RECEIPTS:
        chapter = [r for r in records if r.get('record_type') == 'marked_chapter' and r.get('id') == cid]
        referenced = any(e.get('chapter_id') == cid for e in people.get(person_id, {}).get('evidence', []))
        if not chapter:
            # A caller cannot erase both catalog rows and its supplied reverse evidence.
            # Consult only the finite installed witness, never infer by person label/ID.
            root_path = Path(root).resolve()
            source_path = root_path / 'corpus/jinshu/043-wyd1739-wangrong.json'
            receipt_path = root_path / RECEIPTS[cid][1]
            need(not receipt_path.exists() or source_path.is_file(), '已安裝契約缺現役來源檔')
            disk = json.loads(source_path.read_bytes()) if source_path.is_file() else None
            disk_involved = isinstance(disk, dict) and any(
                m.get('kind') in ('person', 'pronoun') and m.get('person_id') == person_id
                for p in disk.get('paragraphs', []) for m in p.get('mentions', []))
            need(not referenced and not disk_involved, '人物catalog缺現役來源')
            continue
        need(len(chapter) == 1, '重複來源章')
        c = chapter[0]
        involved = any(m.get('kind') in ('person', 'pronoun') and m.get('person_id') == person_id for p in c['paragraphs'] for m in p['mentions'])
        if referenced or involved:
            validate_source(c, root, people, records)
