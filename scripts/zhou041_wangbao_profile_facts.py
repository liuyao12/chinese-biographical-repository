"""Finite Wang Bao profile basics; received source proof supplies mutable roles.

No name, date, parent or place is inferred from a PID, label, office or succession.
The original complete-unit contract and raw captures remain byte-identical.
"""
import copy
import hashlib
import json
from pathlib import Path

REF = 'source-evidence/zhou041-wangbao-ws2432538/profile-facts-contract.json'
SHA = 'e3ed24896ad49c71e55697d65dafc8cf0c4bd6788c8b3bbabbb3ddb4aea65207'
CID = 'c-zhoushu-041-wangbao-ws2432538'


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


def source_records(root, chapter, roles):
    root = Path(root).resolve()
    def local(relative):
        p = Path(relative)
        assert not p.is_absolute() and '..' not in p.parts
        path = root / p
        assert path.is_file() and not path.is_symlink() and path.resolve().is_relative_to(root)
        return path
    raw = local(REF).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == SHA
    contract = json.loads(raw)
    assert chapter['id'] == contract['chapter_id'] == CID
    assert hashlib.sha256(local(contract['base_source_contract']).read_bytes()).hexdigest() == contract['base_source_contract_sha256']
    anchors = {m['id']: m for p in chapter['paragraphs'] for m in p['mentions']}
    for role, mid in contract['role_mids'].items():
        assert anchors[mid]['kind'] == 'person' and anchors[mid]['person_id'] == roles['$' + role]
    for key, template in contract['annotation_templates'].items():
        assert same(chapter['annotation'].get(key), expand(template, roles))
    expected = {rel: expand(template, roles) for rel, template in contract['sidecar_templates'].items()}
    for rel, record in expected.items():
        assert same(json.loads(local(rel).read_bytes()), record)
    return expected


def base_chapter(root, chapter, roles):
    """Validate the exact extension before comparing the old immutable template."""
    source_records(root, chapter, roles)
    try:
        from scripts.zhou041_wangbao_noble_ranks import source_record as noble_record
    except ImportError:
        from zhou041_wangbao_noble_ranks import source_record as noble_record
    noble_record(root, chapter, roles)
    base = copy.deepcopy(chapter)
    del base['annotation']['age_assertions']
    del base['annotation']['profile_facts_ref']
    return base


def guard_catalog(root, person_id, people, records, chapter, roles):
    # Roles have just been reconstructed by the complete source proof from disk
    # MIDs and checked against caller people/reverse, never caller evidence alone.
    if person_id not in (roles['$bao'], roles['$zi']):
        return
    for expected in source_records(root, chapter, roles).values():
        assert sum(same(row, expected) for row in records) == 1
    try:
        from scripts.zhou041_wangbao_noble_ranks import guard_catalog as guard_nobles
    except ImportError:
        from zhou041_wangbao_noble_ranks import guard_catalog as guard_nobles
    guard_nobles(root, person_id, records, chapter, roles)
