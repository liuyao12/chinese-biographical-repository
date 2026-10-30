"""Finite reviewed repository projections; receipt integrity is not glyph certification."""
import hashlib
import copy
import json
from pathlib import Path
try:
    from .witness_projection import repository_positions
except ImportError:
    from witness_projection import repository_positions

# Only a code-reviewed receipt can activate this gate. Data ownership tags grant nothing.
RECEIPTS = {'c-jinshu-043-wyd1739-wangrong': ('s-jinshu-043-wyd1739-wangrong', 'source-evidence/jin043-wyd1739-wangrong/ner-witness-contract.json', 'db860c122a9b32753f4a1068ee37cfbf6948fc968c8c35b3d0bff6a22f90a14f'), 'c-xintangshu-072zhong-wyd1739-wang-preface': ('s-xintangshu-072zhong-wyd1739-wang-preface', 'source-evidence/xintang072zhong-wyd1739-wang-preface/ner-role-contract.json', '1b54d06e4561a3e2ca77b9ed9f6f860de345aa3f723400436690d5b720d5f835')}
OWNED_PATHS = {'c-jinshu-043-wyd1739-wangrong': 'corpus/jinshu/043-wyd1739-wangrong.json', 'c-xintangshu-072zhong-wyd1739-wang-preface': 'corpus/xintangshu/072zhong-wyd1739-wang-preface.json'}

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
    seeds = {}
    roles = {}
    for role in receipt['roles']:
        seed_path = role.get('seed_path', receipt.get('seed_path'))
        need(isinstance(seed_path, str), '角色缺固定seed路徑')
        if seed_path not in seeds: seeds[seed_path] = read(seed_path)
        seed = seeds[seed_path]
        mids = {m['id']: (p, m) for p in seed['paragraphs'] for m in p['mentions']}
        spec = role['seed']
        need(all(seed.get(k) == spec[k] for k in ('work_id', 'book_id', 'source_id'))
             and seed['id'] == spec['chapter_id'] and same(seed['source'], spec['source']), 'seed完整來源漂移')
        p, m = mids[spec['marker']['id']]
        need(p['id'] == spec['paragraph_id'] and p['text'] == spec['quote']
             and all(same(m.get(k), v) for k, v in spec['marker'].items()), 'seed全段／錨漂移')
        if 'paragraph_template' in spec:
            projected = copy.deepcopy(p)
            for marker in projected['mentions']: marker.pop('person_id', None)
            need(same(projected, spec['paragraph_template']), 'seed完整段落結構漂移')
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
    if receipt.get('closed_registry_source_reverse') is True:
        wanted = {}
        links = {}
        for paragraph in chapter['paragraphs']:
            for marker in paragraph['mentions']:
                if marker.get('kind') not in ('person', 'pronoun'): continue
                pid = marker['person_id']
                evidence = {k: chapter[k] for k in ('work_id', 'book_id', 'source_id')}
                evidence.update(chapter_id=cid, paragraph_id=paragraph['id'], mention_id=marker['id'], quote=marker['surface'])
                wanted.setdefault(pid, []).append(evidence)
                if marker['kind'] == 'person': links.setdefault(pid, []).append((marker['surface'], marker['id']))
        for key, expected_path in receipt.get('new_role_family_paths', {}).items():
            need(same(people[roles['$' + key]].get('family_path'), expand(expected_path, roles)), '新角色父系路徑非完整有限來源槽')
        for pid, person in people.items():
            observed = [e for e in person.get('evidence', []) if e.get('chapter_id') == cid]
            aliases = [(a.get('surface'), mid) for a in person.get('aliases', []) for mid in a.get('mention_ids', []) if mid.startswith(cid + ':')]
            need(same(sorted(observed, key=lambda e: e['mention_id']), sorted(wanted.get(pid, []), key=lambda e: e['mention_id'])), '本源反向引文非完整聯集')
            need(sorted(aliases) == sorted(links.get(pid, [])), '本源姓名alias非完整聯集')
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
    at_owned_path = source_path is not None and Path(source_path).resolve() in {(Path(root) / rel).resolve() for rel in OWNED_PATHS.values()}
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
            source_path = root_path / OWNED_PATHS[cid]
            receipt_path = root_path / RECEIPTS[cid][1]
            need(not receipt_path.exists() or source_path.is_file(), '已安裝契約缺現役來源檔')
            disk = json.loads(source_path.read_bytes()) if source_path.is_file() else None
            disk_involved = isinstance(disk, dict) and any(
                m.get('kind') in ('person', 'pronoun') and m.get('person_id') == person_id
                for p in disk.get('paragraphs', []) for m in p.get('mentions', []))
            registry_path = root_path / 'registry/persons.json'
            need(not receipt_path.exists() or registry_path.is_file(), '已安裝契約缺人物登記')
            actual_people = json.loads(registry_path.read_bytes())['persons'] if registry_path.is_file() else []
            disk_reverse = any(p.get('id') == person_id and any(e.get('chapter_id') == cid for e in p.get('evidence', [])) for p in actual_people)
            need(not referenced and not disk_involved and not disk_reverse, '人物catalog缺現役來源')
            continue
        need(len(chapter) == 1, '重複來源章')
        c = chapter[0]
        involved = any(m.get('kind') in ('person', 'pronoun') and m.get('person_id') == person_id for p in c['paragraphs'] for m in p['mentions'])
        if referenced or involved:
            validate_source(c, root, people, records)


def record_valid(record, root, record_type):
    """Exact finite sidecar member after complete source and reverse validation."""
    try:
        cid = record.get('chapter_id') or record['evidence'][0]['chapter_id']
        if cid not in RECEIPTS: return False
        root = Path(root).resolve()
        receipt = json.loads(inside(root, RECEIPTS[cid][1]).read_bytes())
        chapter = json.loads(inside(root, receipt['chapter_path']).read_bytes())
        roles = validate_source(chapter, root)
        for template in receipt['sidecars'].values():
            sidecar = expand(template, roles)
            if sidecar.get('record_type') == record_type:
                rows = sidecar.get('records', sidecar.get('assertions', []))
                if sum(same(record, row) for row in rows) == 1: return True
        return False
    except (ValueError, TypeError, KeyError, OSError, UnicodeError, StopIteration, IndexError):
        return False

def glyph_person_valid(chapter, marker, root):
    """An uncertain glyph can have a contextual identity; no arbitrary punctuation."""
    try:
        cid = chapter['id']
        if cid not in RECEIPTS: return False
        root = Path(root).resolve()
        receipt = json.loads(inside(root, RECEIPTS[cid][1]).read_bytes())
        if marker.get('id') not in receipt.get('glyph_person_mention_ids', []): return False
        validate_source(chapter, root)
        return any(same(marker, m) for p in chapter['paragraphs'] for m in p['mentions'])
    except (ValueError, TypeError, KeyError, OSError, UnicodeError, StopIteration, IndexError):
        return False
