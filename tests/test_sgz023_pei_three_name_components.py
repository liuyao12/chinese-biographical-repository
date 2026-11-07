# coding: utf-8
"""Received Pei names, caller ownership, and source-qualified endpoint moves."""
import copy
import hashlib
import json
import unittest
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch

from scripts.person_bundle import bundle, load_catalog, validate_full_name
from scripts.sgz023_pei_name_components import (
    CID, MIDS, applies, guard_bundle, name_valid, proof,
)

ROOT = Path(__file__).resolve().parents[1]
CHAPTER = 'corpus/sanguozhi/023-peiqian-ws2376966.json'
ASSERTIONS = 'corpus/sanguozhi/023-peiqian-ws2376966-assertions.json'


@contextmanager
def current_json_views(changes):
    """Change only specified current JSON reads, through both production readers."""
    original_bytes, original_text = Path.read_bytes, Path.read_text
    data = {(ROOT / rel).resolve(): json.dumps(value, ensure_ascii=False).encode()
            for rel, value in changes.items()}

    def read_bytes(path, *args, **kwargs):
        return data[path.resolve()] if path.resolve() in data else original_bytes(path, *args, **kwargs)

    def read_text(path, *args, **kwargs):
        return data[path.resolve()].decode() if path.resolve() in data else original_text(path, *args, **kwargs)

    with patch.object(Path, 'read_bytes', read_bytes), patch.object(Path, 'read_text', read_text):
        yield


def current_endpoints(value, old, new):
    """Never rewrite opaque IDs, free text, contract captures, or ID substrings."""
    if isinstance(value, list):
        return [current_endpoints(v, old, new) for v in value]
    if not isinstance(value, dict):
        return value
    result = {}
    for key, item in value.items():
        if key == 'person_id' or key.endswith('_person_id'):
            result[key] = new if item == old else item
        elif key.endswith('_person_ids') and isinstance(item, list):
            result[key] = [new if v == old else v for v in item]
        else:
            result[key] = current_endpoints(item, old, new)
    return result


def opaque_ids(value, path=()):
    if isinstance(value, dict):
        return ([(path + ('id',), value['id'])] if 'id' in value else []) + [
            row for key, item in value.items() for row in opaque_ids(item, path + (key,))]
    if isinstance(value, list):
        return [row for index, item in enumerate(value) for row in opaque_ids(item, path + (index,))]
    return []


class PeiThreeNameComponents(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.people, cls.records = load_catalog(ROOT)
        cls.names = proof(ROOT)['records']
        cls.chapter = json.loads((ROOT / CHAPTER).read_bytes())
        cls.paragraph = next(p for p in cls.chapter['paragraphs'] if p['id'] == CID + ':p009')
        cls.markers = {m['id']: m for m in cls.paragraph['mentions']}
        cls.by_ming = {n['ming']: n for n in cls.names}

    def test_received_ming_zi_and_yan_are_distinct_with_unknown_print(self):
        self.assertIsNone(self.chapter['source']['edition'])
        self.assertFalse(self.chapter['source']['image_verified'])
        self.assertFalse(self.chapter['annotation']['human_reviewed'])
        for ming, zi, extra in [('黎', '伯宗', ['演']), ('康', '仲豫', []), ('綽', '季舒', [])]:
            with self.subTest(ming=ming):
                n = self.by_ming[ming]
                m = self.markers[n['person_mention_id']]
                z = self.markers[n['component_binding']['zi_mention_id']]
                self.assertEqual((m['surface'], z['surface'], n['zi'], n['additional_names']),
                                 (ming, zi, zi, extra))
                self.assertEqual(self.paragraph['text'][m['end']:z['start']], '，字')
                self.assertEqual(m['person_id'], z['person_id'])
                self.assertIsNone(n['surname_basis']['literal_source_components']['surname'])
                self.assertEqual(n['surname'], '裴')
                self.assertFalse(n['human_reviewed'])
                if extra:
                    a, = [self.markers[mid] for mid in n['component_binding']['additional_name_mention_ids']]
                    self.assertEqual(self.paragraph['text'][z['end']:a['start']], '，一名')
                    self.assertEqual((a['surface'], a['person_id']), ('演', n['person_id']))

    def test_wrong_name_components_and_calendar_anchor_are_refused(self):
        cases = [
            ('黎', lambda n: n.update(surname='王')),
            ('黎', lambda n: n.update(ming='演')),
            ('黎', lambda n: n.update(zi='仲豫')),
            ('康', lambda n: n.update(additional_names=['演'])),
            ('康', lambda n: n.update(person_mention_id=CID + ':p009:m0244')),
            ('康', lambda n: n['source_anchor'].update(surface='裴康')),
        ]
        for index, (ming, mutate) in enumerate(cases):
            with self.subTest(case=index):
                n = copy.deepcopy(self.by_ming[ming]); mutate(n)
                self.assertFalse(name_valid(n, ROOT))

    def test_changed_father_or_missing_real_source_reverse_is_refused(self):
        assertions = json.loads((ROOT / ASSERTIONS).read_bytes())
        a = next(a for a in assertions['assertions'] if a['id'] == 'a-sgz023-peiqian-kang-father-hui')
        a['object_person_id'] = self.markers[CID + ':p009:m0414']['person_id']
        with current_json_views({ASSERTIONS: assertions}):
            self.assertFalse(name_valid(self.by_ming['康'], ROOT))
        n = self.by_ming['黎']
        for field in ('evidence', 'aliases'):
            with self.subTest(field=field):
                registry = json.loads((ROOT / 'registry/persons.json').read_bytes())
                actor = next(p for p in registry['persons'] if p['id'] == n['person_id'])
                if field == 'evidence':
                    actor[field] = [e for e in actor[field] if e.get('mention_id') != n['person_mention_id']]
                else:
                    for alias in actor[field]:
                        alias['mention_ids'] = [mid for mid in alias['mention_ids'] if mid != n['person_mention_id']]
                with current_json_views({'registry/persons.json': registry}):
                    self.assertFalse(name_valid(n, ROOT))

    def test_all_three_normal_APIs_and_existing_four_name_consumers(self):
        for n in self.names:
            with self.subTest(name=n['ming']):
                result = bundle(n['person_id'], root=ROOT, include_provisional=True,
                                catalog=(self.people, self.records))
                actual = next(x for x in result['name_components'] if x.get('id') == n['id'])
                self.assertEqual(tuple(actual[k] for k in ('surname', 'ming', 'zi', 'additional_names')),
                                 tuple(n[k] for k in ('surname', 'ming', 'zi', 'additional_names')))
        existing = [n for r in self.records if r.get('record_type') == 'person_name_component_set'
                    for n in r['records'] if str(n.get('id', '')).startswith('name-sgz023-four-')]
        self.assertEqual(len(existing), 4)
        for n in existing:
            self.assertFalse(applies(n))
            validate_full_name(n, root=ROOT)

    def test_owner_cannot_hide_by_stripping_reverse_or_omitting_names(self):
        pid = self.by_ming['黎']['person_id']
        stripped = copy.deepcopy(self.people)
        stripped[pid]['evidence'] = [e for e in stripped[pid]['evidence'] if e.get('mention_id') not in MIDS]
        omitted = [r for r in self.records if not (r.get('record_type') == 'person_name_component_set'
                   and any(applies(n) for n in r['records']))]
        for label, people, records in [('both', stripped, omitted),
                                      ('reverse', stripped, self.records),
                                      ('names', self.people, omitted)]:
            with self.subTest(missing=label):
                with self.assertRaises((AssertionError, ValueError, KeyError)):
                    guard_bundle(ROOT, pid, people, records)
                with self.assertRaises((AssertionError, ValueError, KeyError)):
                    bundle(pid, root=ROOT, include_provisional=True, catalog=(people, records))

    def test_coherent_endpoint_move_preserves_opaque_ids_and_captured_bytes(self):
        old = self.by_ming['黎']['person_id']; new = 'abc_def_987'
        self.assertNotIn(new, self.people)
        registry = current_endpoints(json.loads((ROOT / 'registry/persons.json').read_bytes()), old, new)
        for person in registry['persons']:
            if person['id'] == old:
                person['id'] = new
        changes = {'registry/persons.json': registry}
        for path in list((ROOT / 'corpus').glob('*/*.json')) + [ROOT / 'registry/family-assemblies.json']:
            original = json.loads(path.read_bytes()); moved = current_endpoints(original, old, new)
            if moved != original:
                self.assertEqual(opaque_ids(moved), opaque_ids(original))
                changes[str(path.relative_to(ROOT))] = moved
        self.assertTrue(all(p.startswith('corpus/') or p in ('registry/persons.json',
                            'registry/family-assemblies.json') for p in changes))
        current = changes[CHAPTER]
        before = {m['id']: m for p in self.chapter['paragraphs'] for m in p['mentions']}
        after = {m['id']: m for p in current['paragraphs'] for m in p['mentions']}
        self.assertEqual(before.keys(), after.keys())
        for mid, m in before.items():
            self.assertEqual({k: v for k, v in m.items() if k != 'person_id'},
                             {k: v for k, v in after[mid].items() if k != 'person_id'})
        paths = list((ROOT / 'source-evidence/sgz023-peiqian-ws2376966').glob('*.json'))
        paths.append(ROOT / self.chapter['source']['raw_path'])
        captures = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
        with current_json_views(changes):
            people, records = load_catalog(ROOT)
            result = bundle(new, root=ROOT, include_provisional=True, catalog=(people, records))
            self.assertEqual(result['canonical_person_id'], new)
            self.assertTrue(any(n['person_id'] == new and n['ming'] == '黎' for n in result['name_components']))
            for path, expected in captures.items():
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), expected)
            wrong = copy.deepcopy(records)
            c = next(r for r in wrong if r.get('id') == CID)
            next(m for p in c['paragraphs'] for m in p['mentions'] if m['id'] == CID + ':p009:m0458')['person_id'] = old
            missing = copy.deepcopy(people)
            missing[new]['evidence'] = [e for e in missing[new]['evidence'] if e.get('mention_id') not in MIDS]
            for supplied_people, supplied_records in [(people, wrong), (missing, records)]:
                with self.assertRaises((AssertionError, ValueError, KeyError)):
                    guard_bundle(ROOT, new, supplied_people, supplied_records)
                with self.assertRaises((AssertionError, ValueError, KeyError)):
                    bundle(new, root=ROOT, include_provisional=True,
                           catalog=(supplied_people, supplied_records))
        for path, expected in captures.items():
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), expected)


if __name__ == '__main__':
    unittest.main()
