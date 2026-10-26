"""Export explicit editorial reading choices, without inferring editions from text."""
import json
from pathlib import Path


POLICY_PATH = 'registry/reading-witness-preferences.json'


def _json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()


def enrich_outputs(generated, root):
    root = Path(root)
    path = root / POLICY_PATH
    if not path.exists():
        return generated
    policy = json.loads(path.read_bytes())
    if (not isinstance(policy, dict)
            or set(policy) != {'schema_version', 'application_scope', 'unselected_role',
                               'human_reviewed', 'model', 'policy_note', 'preferences'}
            or type(policy.get('schema_version')) is not int or policy['schema_version'] != 1
            or policy.get('application_scope') != 'reading_display_only'
            or policy.get('unselected_role') != 'comparison_transcription'
            or type(policy.get('human_reviewed')) is not bool
            or policy.get('model') is not None
            or not isinstance(policy.get('policy_note'), str) or not policy['policy_note'].strip()
            or not isinstance(policy.get('preferences'), list)):
        raise ValueError('Invalid explicit reading-witness policy')
    provenance_key = root / 'data/corpus/work-provenance.json'
    if provenance_key not in generated:
        raise ValueError('Reading preferences require actual source-edition provenance')
    provenance = json.loads(generated[provenance_key])
    manifest = json.loads(generated[root / 'data/corpus/works.json'])
    table_index = json.loads((root / 'data/historical-tables/index.json').read_bytes())
    table_paths = {item['id']: item['path'] for item in table_index['tables']}
    indexes, views = {}, []
    for work in manifest['works']:
        key = root / work['catalog_path']
        index = json.loads(generated[key])
        indexes[key] = index
        for entry in index['chapters']:
            if entry.get('available') == 'marked_text':
                chapter = json.loads(generated[root / entry['path']])
                if chapter['id'] != entry['chapter_id'] or chapter['work_id'] != index['work_id']:
                    raise ValueError('Reading witness chapter/work mismatch')
                view = {k: chapter[k] for k in ('work_id', 'book_id', 'source_id')}
                view['chapter_id'] = chapter['id']
            elif entry.get('available') == 'table':
                target = (root / table_paths[entry['table_id']]).resolve()
                if not target.is_relative_to((root / 'data/historical-tables').resolve()):
                    raise ValueError('Reading table source outside historical tables')
                source = json.loads(target.read_bytes())['source']
                view = {k: source[k] for k in ('work_id', 'book_id', 'chapter_id')}
                view['source_id'] = source['id']
            else:
                continue
            if (view['work_id'] != index['work_id']
                    or entry.get('book_id', view['book_id']) != view['book_id']
                    or entry.get('chapter_id', view['chapter_id']) != view['chapter_id']):
                raise ValueError('Reading witness belongs to a different work')
            views.append((view, entry))
    choices = {}
    required = {'source_id', 'work_id', 'book_id', 'chapter_id', 'edition_id',
                'role', 'scope', 'selection_label', 'reference_ids', 'rationale'}
    for row in policy['preferences']:
        if not isinstance(row, dict) or set(row) != required:
            raise ValueError('Unknown reading preference fields')
        if not all(type(row[k]) is str and row[k] for k in
                   ('source_id', 'work_id', 'book_id', 'chapter_id', 'edition_id')):
            raise ValueError('Reading preference identifiers must be strings')
        if (row['source_id'] in choices or row['role'] != 'preferred_received_selection'
                or row['scope'] != 'source_extent_only'
                or not isinstance(row['selection_label'], str) or not row['selection_label'].strip()
                or not isinstance(row['rationale'], str) or not row['rationale'].strip()):
            raise ValueError('Duplicate, unscoped or unexplained reading choice')
        matches = [v for v, _ in views if all(v[k] == row[k]
                   for k in ('source_id', 'work_id', 'book_id', 'chapter_id'))]
        if len(matches) != 1:
            raise ValueError('Reading preference must identify one actual source selection')
        basis = provenance['text_bases'].get(row['source_id'], {})
        edition = provenance['editions'].get(row['edition_id'], {})
        refs = row['reference_ids']
        if (basis.get('status') != 'documented' or basis.get('edition_id') != row['edition_id']
                or basis.get('work_id') != row['work_id'] or edition.get('work_id') != row['work_id']
                or not isinstance(edition.get('label'), str) or not edition['label'].strip()
                or not isinstance(refs, list) or not refs or not all(type(r) is str for r in refs)
                or len(set(refs)) != len(refs)
                or any(r not in basis.get('reference_ids', []) or r not in provenance['references'] for r in refs)):
            raise ValueError('Preferred reading lacks its documented actual edition and references')
        choices[row['source_id']] = row
    for view, entry in views:
        source_id = view['source_id']
        basis = provenance['text_bases'].get(source_id, {})
        edition_id = basis.get('edition_id')
        edition = provenance['editions'].get(edition_id, {})
        if ((basis and basis.get('work_id') != view['work_id'])
                or (edition_id and edition.get('work_id') != view['work_id'])):
            raise ValueError('Reading edition metadata belongs to a different work')
        choice = choices.get(source_id)
        entry.update(source_id=source_id,
                     reading_role=choice['role'] if choice else policy['unselected_role'],
                     text_base_status=basis.get('status', 'not_researched'),
                     edition_id=edition_id, edition_label=edition.get('label'))
        if choice:
            entry['reading_preference_note'] = choice['rationale']
            entry['selection_label'] = choice['selection_label']
    result = dict(generated)
    for key, index in indexes.items():
        if index['work_id'] != 'w-shiji':
            index['chapters'].sort(key=lambda e: (e['number'],
                0 if e.get('reading_role') == 'preferred_received_selection' else 1,
                e['chapter_id']))
        result[key] = _json_bytes(index)
    result[root / 'data/corpus/reading-witness-preferences.json'] = _json_bytes(policy)
    return result
