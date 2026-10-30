"""Three source-qualified Xiao surname restorations, never a rank-to-surname rule."""
import hashlib
import json
from pathlib import Path

REF = 'source-evidence/zhou041-wangbao-ws2432538/imperial-name-components-contract.json'
SHA = '0110f4879214ef8b50870b3d31c105ee2f4768ca2081288280b5feafe56752dc'
CH = 'corpus/zhoushu/041-wangbao-ws2432538.json'
KIND = 'contextual_surname_from_fixed_zhou041_imperial_roles'


def same(a, b):
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(same(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    return a == b


def expand(value, roles):
    if isinstance(value, str):
        return roles.get(value, value)
    if isinstance(value, list):
        return [expand(v, roles) for v in value]
    if isinstance(value, dict):
        return {k: expand(v, roles) for k, v in value.items()}
    return value


def source_record(root, chapter, roles):
    root = Path(root).resolve()
    def local(relative):
        p = Path(relative)
        assert not p.is_absolute() and '..' not in p.parts
        q = root / p
        assert q.is_file() and not q.is_symlink() and q.resolve().is_relative_to(root)
        return q
    raw = local(REF).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == SHA
    c = json.loads(raw)
    assert same(chapter, json.loads(local(CH).read_bytes()))
    assert hashlib.sha256(local('source-evidence/zhou041-wangbao-ws2432538/source-ner-contract.json').read_bytes()).hexdigest() == c['source_ner_contract_sha256']
    readings = local(c['readings_path']).read_bytes()
    assert hashlib.sha256(readings).hexdigest() == c['readings_sha256']
    primary = json.loads(readings)
    for reading in primary.values():
        assert reading['human_reviewed'] is False and reading['image_verified'] is False
        for key, value in reading.items():
            if key == 'quote' or key.endswith('_quote'):
                assert hashlib.sha256(value.encode()).hexdigest() == reading[key + '_sha256']
    # Actual observed ancient text, not Wikipedia page headers or dynasty labels.
    assert '梁高祖武皇帝諱衍' in primary['nanshi006_surname']['quote']
    assert '姓蕭氏' in primary['nanshi006_surname']['quote']
    assert primary['nanshi006_surname']['fixed_permalink_body_read'] is True
    assert primary['nanshi006_surname']['full_raw_captured'] is False
    for key in ('liang004_taizong', 'liang008_daqi', 'liang055_ji'):
        assert primary[key]['fixed_permalink_body_read'] is False and primary[key]['full_raw_captured'] is False
        assert 'Cache miss' in primary[key]['fixed_permalink_limitation']
    assert '太宗簡文皇帝諱綱' in primary['liang004_taizong']['quote']
    assert '高祖第三子' in primary['liang004_taizong']['quote']
    assert '大器，字仁宗，太宗嫡長子也' in primary['liang008_daqi']['quote']
    assert '封宣城郡王' in primary['liang008_daqi']['quote']
    hui = primary['liang022_hui']
    fixed = local(hui['existing_raw_path']).read_bytes()
    assert hashlib.sha256(fixed).hexdigest() == hui['existing_raw_sha256']
    assert hui['quote'] in fixed.decode()[hui['selected_raw_codepoint_start']:hui['selected_raw_codepoint_end']]
    assert '鄱陽忠烈王恢字弘達，太祖第九子也。' == hui['quote']
    assert '武陵王紀字世詢，高祖第八子也' in primary['liang055_ji']['quote']
    assert '蕭紀' in primary['liang055_ji']['direct_full_name_quote']
    assert '俱殺之' in primary['liang055_ji']['punitive_surname_quote']
    assert '賜姓饕餮氏' in primary['liang055_ji']['punitive_surname_quote']
    paragraphs = {p['id']: p for p in chapter['paragraphs']}
    anchors = {m['id']: (p, m) for p in chapter['paragraphs'] for m in p['mentions']}
    for role, mid in c['role_mids'].items():
        p, m = anchors[mid]
        assert m['kind'] == 'person' and m['person_id'] == roles['$' + role]
    native = paragraphs[chapter['id'] + ':p002']['text']
    assert '宣成王大器，簡文帝之冢嫡' in native
    assert '梁武帝喜其才藝，遂以弟鄱陽王恢之女妻之' in native
    assert anchors[chapter['id'] + ':p002:m0078'][1]['person_id'] == roles['$liangwu']
    expected = expand(c['name_set_template'], roles)
    for n in expected['records']:
        p, m = anchors[n['person_mention_id']]
        assert n['quote'] == p['text'] and n['surname'] == '蕭' and 'zi' not in n
        assert n['title'] + n['ming'] == m['surface']
        assert n['source_anchor'] == {k: m[k] for k in ('start', 'end', 'surface')}
        for key in ('ming_anchor', 'title_anchor'):
            a = n['name_source_binding'][key]
            assert p['text'][a['start']:a['end']] == a['surface'] and a['paragraph_id'] == p['id']
        assert n['surname_basis']['literal_in_current_mention'] is False
    ji = next(n for n in expected['records'] if n['person_mention_id'] == c['role_mids']['ji'])
    assert ji['surname_basis']['scope'] == 'biographical_original_surname_not_exclusive_lifetime_surname'
    assert ji['surname_basis']['reported_later_surname'] == '饕餮氏'
    assert same(json.loads(local(c['name_path']).read_bytes()), expected)
    return expected


def guard_catalog(root, person_id, records, chapter, roles):
    expected = source_record(root, chapter, roles)
    owners = {row['person_id'] for row in expected['records']}
    if person_id in owners:
        assert sum(same(row, expected) for row in records) == 1


def validate_surname(name, names, chapters, assertions, root=None):
    try:
        try:
            from scripts.fixed_zhou041_wangbao import proof
        except ImportError:
            from fixed_zhou041_wangbao import proof
        chapter, _, roles = proof(root)
        assert same(chapters[chapter['id']], chapter)
        expected = source_record(root, chapter, roles)['records']
        assert sum(same(name, n) for n in expected) == 1
        assert sum(same(name, n) for n in names) == 1
    except (AssertionError, KeyError, ValueError, TypeError, OSError, StopIteration) as error:
        raise ValueError('周041三姓名須依固定角色/原王號、外源明姓、近系或本傳全名及原取得資格復姓；不得補字或抹後賜姓') from error
