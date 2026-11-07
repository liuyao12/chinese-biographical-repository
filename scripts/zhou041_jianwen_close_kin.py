"""Finite Liang Jianwen reuse and three literal Zhou041 family roles.

Original capture/contract stays opaque; current endpoints come from actual MIDs.
"""
import copy
import hashlib
import json
from pathlib import Path

REF = 'source-evidence/zhou041-wangbao-ws2432538/jianwen-close-kin-contract.json'
SHA = '8975a9550fd0e83d0ce1eda82f4d23a418aba81b6ecfcb6b08f9d8c4f3b859c7'
CH = 'corpus/zhoushu/041-wangbao-ws2432538.json'
CID = 'c-zhoushu-041-wangbao-ws2432538'
KIND = 'fixed_zhou041_jianwen_close_kin'


def same(a, b):
    if type(a) is not type(b): return False
    if isinstance(a, dict): return a.keys() == b.keys() and all(same(a[k], b[k]) for k in a)
    if isinstance(a, list): return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    return a == b


def expand(x, roles):
    if isinstance(x, str): return roles.get(x, x)
    if isinstance(x, list): return [expand(v, roles) for v in x]
    if isinstance(x, dict): return {k: expand(v, roles) for k, v in x.items()}
    return x


def read(root, rel):
    root = Path(root).resolve(); p = Path(rel)
    assert not p.is_absolute() and '..' not in p.parts
    p = root / p
    assert p.is_file() and not p.is_symlink() and p.resolve().is_relative_to(root)
    return p.read_bytes()


def contract(root):
    raw = read(root, REF); assert hashlib.sha256(raw).hexdigest() == SHA
    c = json.loads(raw)
    for rel, expected in [(c['source_contract_path'], c['source_contract_sha256']),
                          (c['readings_path'], c['readings_sha256']),
                          (c['existing_primary_path'], c['existing_primary_sha256'])]:
        assert hashlib.sha256(read(root, rel)).hexdigest() == expected
    r = json.loads(read(root, c['readings_path']))
    assert r['fixed_raw_obtained'] is False and r['fixed_link_fetch'] == 'Cache miss'
    assert r['image_verified'] is False and r['human_reviewed'] is False
    assert r['actual_print_edition_verified'] is False
    assert '太宗簡文皇帝諱綱' in r['quotes'][0]
    assert '封晉安王' in r['quotes'][1]
    assert '雲麾將軍、南徐州刺史' in r['quotes'][2]
    assert '晉安王綱' in r['quotes'][3] and '可立為皇太子' in r['quotes'][3]
    return c


def installed(root, ch, people, roles):
    if not (Path(root) / REF).exists(): return None
    c = contract(root)
    assert same(ch, json.loads(read(root, CH)))
    seed = c['seed']; source = json.loads(read(root, seed['path']))
    assert source['id'] == seed['chapter_id'] and same(source['source'], seed['source'])
    sp, = [p for p in source['paragraphs'] if p['id'] == seed['paragraph_id']]
    sm, = [m for m in sp['mentions'] if m['id'] == seed['marker']['id']]
    assert sp['text'] == seed['quote'] and same({k:v for k,v in sm.items() if k != 'person_id'}, seed['marker'])
    assert sm['kind'] == 'person' and sp['text'][sm['start']:sm['end']] == '晉安王綱'
    pid = sm['person_id']; assert pid in people
    assert [e for e in people[pid]['evidence'] if e.get('mention_id') == sm['id']] == [seed['reverse']]
    assert any(a['surface'] == sm['surface'] and sm['id'] in a['mention_ids'] for a in people[pid]['aliases'])
    roles['$liangjian'] = pid
    anchors = {m['id']:m for p in ch['paragraphs'] for m in p['mentions']}
    for role, mid in c['role_mids'].items():
        assert anchors[mid]['kind'] == 'person' and anchors[mid]['person_id'] == roles['$'+role]
    m = anchors[c['target_mid']]
    assert same(m, expand(c['native_marker_template'], roles))
    assert not any(v['id'] == c['original_unresolved_case']['id'] for v in ch['annotation']['unresolved_identity_cases'])
    p, = [p for p in ch['paragraphs'] if any(v['id'] == m['id'] for v in p['mentions'])]
    assert p['text'][m['start']:m['end']] == '簡文帝'
    assert '宣成王大器，簡文帝之冢嫡，即襃之姑子也' in p['text']
    assert '梁武帝喜其才藝，遂以弟鄱陽王恢之女妻之' in p['text']
    reverse = c['native_reverse']
    assert [e for e in people[pid]['evidence'] if e.get('mention_id') == m['id']] == [reverse]
    assert [a for a in people[pid]['aliases'] if m['id'] in a.get('mention_ids', [])] == [{'surface':'簡文帝','mention_ids':[m['id']]}]
    side = expand(c['sidecar_template'], roles)
    assert same(json.loads(read(root, c['sidecar_path'])), side)
    return c, side


def source_projection(ch, state, base_contract, roles):
    if state is None: return ch
    c, _ = state; out = copy.deepcopy(ch)
    for p in out['paragraphs']:
        for i, m in enumerate(p['mentions']):
            if m['id'] == c['target_mid']: p['mentions'][i] = copy.deepcopy(next(v for op in expand(base_contract['chapter_template'], roles)['paragraphs'] for v in op['mentions'] if v['id'] == c['target_mid']))
    original = base_contract['chapter_template']['annotation']['unresolved_identity_cases']
    i = next(i for i,v in enumerate(original) if v['id'] == c['original_unresolved_case']['id'])
    out['annotation']['unresolved_identity_cases'].insert(i, copy.deepcopy(expand(original[i], roles)))
    return out


def augment_reverse(state, roles, expected_reverse, expected_alias):
    if state is None: return
    c, _ = state; pid = roles['$liangjian']
    assert pid not in expected_reverse and pid not in expected_alias
    expected_reverse[pid] = [c['native_reverse']]
    expected_alias[pid] = [{'surface':'簡文帝','mention_ids':[c['target_mid']]}]


def applies(a):
    return a.get('qualifiers', {}).get('source_clause_binding', {}).get('kind') == KIND


def family_valid(a, paragraphs, root):
    if not applies(a): return False
    try:
        try: from scripts.fixed_zhou041_wangbao import proof
        except ImportError: from fixed_zhou041_wangbao import proof
        ch, _, roles = proof(root)
        c = contract(root); side = expand(c['sidecar_template'], roles)
        assert sum(same(a, row) for row in side['assertions']) == 1
        e, = a['evidence']; _, p = paragraphs[e['paragraph_id']]
        assert same(p, next(v for v in ch['paragraphs'] if v['id'] == p['id']))
        return True
    except (AssertionError, KeyError, TypeError, ValueError, OSError, StopIteration):
        return False


def guard_catalog(root, pid, records, state, roles):
    if state is None: return
    c, side = state
    owners = {row[k] for row in side['assertions'] for k in ('subject_person_id','object_person_id')}
    if pid in owners:
        assert sum(same(r, side) for r in records) == 1
