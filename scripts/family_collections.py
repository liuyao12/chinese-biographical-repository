"""Rootless visible family groupings; these never create pedigree edges."""
from pathlib import Path
import argparse
import json
from functools import lru_cache

try:
    from .person_bundle import load_catalog
except ImportError:
    from person_bundle import load_catalog

PATH = 'registry/family-collections.json'
PUBLIC_PATH = 'data/corpus/family-collections.json'
INDEX_PATH = 'data/corpus/family-collection-index.json'


def _record_indexes(records):
    assertions = {}
    chapters = {}
    for record in records:
        if record.get('record_type') == 'person_assertion_set':
            for assertion in record['assertions']:
                if assertion['id'] in assertions:
                    raise AssertionError(f"duplicate assertion id: {assertion['id']}")
                assertions[assertion['id']] = assertion
        elif record.get('record_type') == 'marked_chapter':
            chapters[record['id']] = record
    return assertions, chapters


def validate(data, root):
    try:
        from .validate import schema_errors
    except ImportError:
        from validate import schema_errors
    schema = json.loads((Path(root) / 'schema/family-collections.schema.json').read_text(encoding='utf-8'))
    errors = schema_errors(data, schema, schema)
    assert not errors, 'schema: ' + '; '.join(errors)
    assert set(data) == {'schema_version', 'record_type', 'human_reviewed', 'collections'}
    assert type(data['schema_version']) is int and data['schema_version'] == 1
    assert data['record_type'] == 'rootless_family_collections'
    assert data['human_reviewed'] is False
    assert isinstance(data['collections'], list)

    people, records = load_catalog(Path(root))
    assertions, chapters = _record_indexes(records)
    assembly_path = Path(root) / 'registry/family-assemblies.json'
    assemblies_doc = json.loads(assembly_path.read_text(encoding='utf-8'))
    assemblies = {a['id']: a for a in assemblies_doc['assemblies']
                  if a.get('schema_mode') != 'personless_namespace'}
    assembled_sources = {
        source_id
        for assembly in assemblies.values()
        for member in assembly['members']
        for source_id in member['source_person_ids']
    }

    collection_ids = set()
    for collection in data['collections']:
        assert set(collection) == {'id', 'label', 'status', 'human_reviewed', 'branches',
                                   'standalone_members', 'relationships', 'rationale'}
        cid = collection['id']
        assert cid not in collection_ids, f'{cid}: duplicate collection id'
        collection_ids.add(cid)
        assert cid.startswith('family-collection-') and cid not in people, f'{cid}: collection id is not a person'
        assert collection['status'] in ('contextual_provisional', 'editorial_preferred')
        assert collection['human_reviewed'] is False and collection['label'] and collection['rationale']
        assert collection['branches'] and collection['standalone_members'] and collection['relationships']

        branch_ids = set()
        contained_ids = set()
        for branch in collection['branches']:
            assert set(branch) == {'assembly_id', 'entry_person_id'}
            aid = branch['assembly_id']
            assert aid not in branch_ids, f'{cid}: duplicate branch assembly'
            branch_ids.add(aid)
            assembly = assemblies.get(aid)
            assert assembly is not None, f'{cid}: unknown or non-tree assembly {aid}'
            rows = {m['person_id']: m for m in assembly['members']}
            assert assembly['root_person_id'] in rows, f'{cid}: branch has no real tree root'
            assert branch['entry_person_id'] in rows, f'{cid}: branch entry is not an assembly member'
            contained_ids.update(rows)
            contained_ids.update(sid for row in rows.values() for sid in row['source_person_ids'])

        standalone_ids = set()
        for member in collection['standalone_members']:
            assert set(member) == {'person_id', 'role', 'parent_person_id', 'father_person_id',
                                   'mother_person_id', 'common_ancestor_person_id'}
            pid = member['person_id']
            assert pid in people, f'{cid}: unknown standalone person {pid}'
            assert pid not in standalone_ids and pid not in contained_ids, f'{cid}: duplicate or already assembled standalone person {pid}'
            assert member['role'] == 'unplaced_paternal_collateral'
            assert all(member[field] is None for field in (
                'parent_person_id', 'father_person_id', 'mother_person_id', 'common_ancestor_person_id'))
            assert pid not in assembled_sources, f'{cid}: standalone person already belongs to a tree assembly'
            standalone_ids.add(pid)
            contained_ids.add(pid)

        relation_ids = set()
        for relation in collection['relationships']:
            assert set(relation) == {'assertion_id', 'subject_person_id', 'object_person_id',
                                     'predicate', 'source_term', 'lineage', 'generation_difference',
                                     'relative_age', 'older_person_id', 'younger_person_id',
                                     'distance', 'common_ancestor_person_id', 'parent_edge'}
            aid = relation['assertion_id']
            assert aid not in relation_ids, f'{cid}: duplicate relation assertion {aid}'
            relation_ids.add(aid)
            assertion = assertions.get(aid)
            assert assertion is not None, f'{cid}: unknown source assertion {aid}'
            assert assertion['status'] == 'source_attested'
            assert relation['subject_person_id'] == assertion['subject_person_id']
            assert relation['object_person_id'] == assertion['object_person_id']
            assert relation['predicate'] == assertion['predicate'] == 'agnatic_cousin'
            assert relation['subject_person_id'] in contained_ids and relation['object_person_id'] in contained_ids, (
                f'{cid}: relation endpoint is outside the visible collection'
            )
            q = assertion['qualifiers']
            kinship = q['kinship_structure']
            birth_order = q['relative_birth_order']
            assert relation['source_term'] == q['source_term'] and relation['source_term']
            assert relation['lineage'] == kinship['lineage'] == 'paternal'
            assert relation['generation_difference'] == kinship['generation_difference'] == 0
            assert relation['relative_age'] == kinship['subject_relative_age']
            assert relation['distance'] is None and kinship['distance'] is None
            assert relation['common_ancestor_person_id'] is None
            assert kinship['common_ancestor_person_id'] is None
            assert relation['older_person_id'] == birth_order['older_person_id']
            assert relation['younger_person_id'] == birth_order['younger_person_id']
            assert birth_order['operator'] == 'lt'
            assert birth_order['scope'] == 'agnatic_cousins'
            assert birth_order['older_ordinal'] is None and birth_order['younger_ordinal'] is None
            assert relation['parent_edge'] is False
            assert relation['older_person_id'] in contained_ids and relation['younger_person_id'] in contained_ids

            assert assertion['evidence'], f'{cid}: source assertion has no evidence'
            for evidence in assertion['evidence']:
                chapter = chapters.get(evidence['chapter_id'])
                assert chapter is not None, f'{cid}: relation evidence chapter is missing'
                paragraph = next((p for p in chapter['paragraphs'] if p['id'] == evidence['paragraph_id']), None)
                assert paragraph is not None and evidence['quote'] == paragraph['text'], (
                    f'{cid}: relation quote does not match its paragraph'
                )
                assert chapter['source_id'] == evidence['source_id']
                assert relation['source_term'] in evidence['quote'], f'{cid}: source term absent from quote'
                for pid in (assertion['subject_person_id'], assertion['object_person_id']):
                    assert any(m.get('kind') == 'person' and m.get('person_id') == pid
                               and m.get('surface') in evidence['quote']
                               for m in paragraph['mentions']), f'{cid}: endpoint lacks a person mention'
    return data


def collection_person_ids(data, root, collection_id):
    """Resolve a collection to its existing assembled IDs plus direct members."""
    collection = next(c for c in data['collections'] if c['id'] == collection_id)
    assemblies_doc = json.loads((Path(root) / 'registry/family-assemblies.json').read_text(encoding='utf-8'))
    assemblies = {a['id']: a for a in assemblies_doc['assemblies']}
    ids = {member['person_id'] for member in collection['standalone_members']}
    for branch in collection['branches']:
        ids.update(m['person_id'] for m in assemblies[branch['assembly_id']]['members'])
    return ids


@lru_cache(maxsize=8)
def _loaded(root_text):
    root = Path(root_text)
    if not (root / PATH).exists() or not (root / 'registry/family-assemblies.json').exists():
        return {'schema_version': 1, 'record_type': 'rootless_family_collections',
                'human_reviewed': False, 'collections': []}, {}
    data = json.loads((root / PATH).read_text(encoding='utf-8'))
    assemblies_doc = json.loads((root / 'registry/family-assemblies.json').read_text(encoding='utf-8'))
    assemblies = {a['id']: a for a in assemblies_doc['assemblies']}
    memberships = {}
    for collection in data['collections']:
        ids = {m['person_id'] for m in collection['standalone_members']}
        for branch in collection['branches']:
            assembly = assemblies[branch['assembly_id']]
            for member in assembly['members']:
                ids.add(member['person_id'])
                ids.update(member['source_person_ids'])
        memberships[collection['id']] = ids
    return data, memberships


def collections_for_person(person_ids, root):
    """Return rootless collection context for a person without adding parent edges."""
    data, memberships = _loaded(str(Path(root).resolve()))
    person_ids = set(person_ids)
    result = []
    for collection in data['collections']:
        members = memberships[collection['id']]
        if person_ids.intersection(members):
            result.append(dict(collection, person_ids=sorted(members)))
    return result


def write_public_index(root):
    """Publish the registry and a reverse person-to-collection lookup for static/API clients."""
    root = Path(root)
    data, memberships = _loaded(str(root.resolve()))
    validate(data, root)
    public = root / PUBLIC_PATH
    index = root / INDEX_PATH
    public.parent.mkdir(parents=True, exist_ok=True)
    public.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    by_person = {}
    rows = []
    for collection in data['collections']:
        ids = sorted(memberships[collection['id']])
        rows.append({'collection_id': collection['id'], 'label': collection['label'],
                     'status': collection['status'], 'person_ids': ids})
        for pid in ids:
            by_person.setdefault(pid, []).append(collection['id'])
    payload = {'schema_version': 1, 'record_type': 'family_collection_index',
               'source_path': PUBLIC_PATH, 'runtime_ai_required': False,
               'collections': rows, 'by_person_id': by_person}
    index.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return public, index


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    data = json.loads((args.root / PATH).read_text(encoding='utf-8'))
    validate(data, args.root)
    write_public_index(args.root)
    print('家族集合：', len(data['collections']), '筆')
