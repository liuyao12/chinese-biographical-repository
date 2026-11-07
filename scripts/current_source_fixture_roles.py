"""Project two finite fixture roles through unchanged received-source MIDs.
Historical captures stay byte-exact. Current person IDs are never allowlisted.
"""
import copy
import hashlib
import json
from pathlib import Path
REF = 'source-evidence/current-source-fixture-roles/source-contract.json'
SHA = '67c3e4e2f682b02eade0afa96fbd3020ae15d3f5ab8bbd7e41a1613e2b3ef4bf'

def project_fixture_roles(expected, path, root, people=None, chapters=None):
    root = Path(root)
    raw = (root / REF).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == SHA
    contract = json.loads(raw)
    if path != contract['fixture_path']:
        return expected
    capture = (root / contract['historical_capture']).read_bytes()
    assert hashlib.sha256(capture).hexdigest() == contract['historical_sha256']
    historical = json.loads(capture)
    if people is None:
        people = {p['id']: p for p in json.loads((root / 'registry/persons.json').read_bytes())['persons']}
    chapters = chapters if chapters is not None else {}
    out = copy.deepcopy(expected)
    resolved = {}
    for role, seed in contract['roles'].items():
        ch = chapters.get(seed['source_path'])
        if ch is None:
            ch = json.loads((root / seed['source_path']).read_bytes())
        assert {k: ch[k] for k in seed['dimensions']} == seed['dimensions']
        assert {k: ch['source'][k] for k in seed['source_identity']} == seed['source_identity']
        p, = [p for p in ch['paragraphs'] if p['id'] == seed['paragraph_id']]
        assert p.get('text_layer') == 'received_chapter'
        assert hashlib.sha256(p['text'].encode()).hexdigest() == seed['paragraph_sha256']
        ids = []
        for old_marker in seed['markers']:
            m, = [m for m in p['mentions'] if m['id'] == old_marker['id']]
            assert {k: v for k, v in m.items() if k != 'person_id'} == old_marker
            assert p['text'][m['start']:m['end']] == m['surface']
            pid = m['person_id']
            assert pid in people and people[pid]['id'] == pid
            reverse = dict(work_id=ch['work_id'], book_id=ch['book_id'], source_id=ch['source_id'], chapter_id=ch['id'], paragraph_id=p['id'], mention_id=m['id'], quote=m['surface'])
            owners = [(q['id'], e) for q in people.values() for e in q.get('evidence', []) if e.get('mention_id') == m['id']]
            assert owners == [(pid, reverse)]
            aliases = [(q['id'], a['surface']) for q in people.values() for a in q.get('aliases', []) if m['id'] in a.get('mention_ids', [])]
            assert aliases == [(pid, m['surface'])]
            ids.append(pid)
        assert len(set(ids)) == 1
        assert isinstance(expected.get(role), str) and expected[role] in (historical[role], ids[0])
        out[role] = ids[0]
        resolved[role] = ids[0]
    for group in contract['distinct_role_groups']:
        assert len({resolved[role] for role in group}) == len(group)
    return out
