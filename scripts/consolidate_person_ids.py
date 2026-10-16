"""Apply recorded identity decisions only after a validated reference migration."""
import argparse
import copy
import json
import re
import shutil
import tempfile
from pathlib import Path

from .family_assemblies import load_assemblies
from .person_bundle import ROOT, load_catalog
from .person_ids import allocate_descendant_id, family_path_errors
from .render_corpus import render
from .validate_corpus import validate


def unique(values):
    out = []
    for value in values:
        if value not in out:
            out.append(value)
    return out


def plan(root=ROOT):
    people, records = load_catalog(root)
    source_map, assemblies = load_assemblies(root, (people, records))
    links = {}
    for record in records:
        if record.get('record_type') != 'person_equivalence_set':
            continue
        for decision in record['decisions']:
            for pid in decision['person_ids']:
                if pid != decision['canonical_person_id']:
                    target = decision['canonical_person_id']
                    if pid in links and links[pid] != target:
                        raise ValueError('Identity representatives conflict')
                    links[pid] = target

    def resolve(pid, mapping=links):
        seen = set()
        while pid in mapping:
            if pid in seen:
                raise ValueError('Identity cycle')
            seen.add(pid)
            pid = mapping[pid]
        return pid

    components = {}
    for pid in people:
        components.setdefault(resolve(pid), []).append(pid)
    mapping, merged = {}, []
    for canonical, ids in components.items():
        family_ids = {source_map[i]['person_id'] for i in ids if i in source_map}
        if len(family_ids) > 1:
            raise ValueError('Conflicting family assemblies')
        target = next(iter(family_ids)) if family_ids else canonical
        representative = assemblies[target]['representative_source_person_id'] if family_ids else canonical
        person = copy.deepcopy(people[representative])
        person['id'] = target
        aliases = {}
        for pid in ids:
            for alias in people[pid]['aliases']:
                aliases.setdefault(alias['surface'], []).extend(alias['mention_ids'])
            if pid != target:
                mapping[pid] = target
        person['aliases'] = [{'surface': surface, 'mention_ids': unique(mids)} for surface, mids in aliases.items()]
        person['evidence'] = unique([e for pid in ids for e in people[pid].get('evidence', [])])
        person.pop('id_aliases', None)
        merged.append(person)

    # An assembled path is already evidenced separately; do not fabricate a
    # direct father assertion merely to give its registry entry a family_path.
    reserved = set(people) | set(assemblies)
    for person in merged:
        path = person.get('family_path')
        if not path or person['id'] not in assemblies:
            continue
        translated = copy.deepcopy(path)
        for key in ('parent_person_id', 'ancestor_person_id'):
            if translated.get(key):
                translated[key] = resolve(translated[key], mapping)
        if family_path_errors(person['id'], translated):
            person.pop('family_path')

    for _ in range(len(merged) + 1):
        changed = False
        for person in merged:
            path = person.get('family_path')
            if not path:
                continue
            translated = copy.deepcopy(path)
            for key in ('parent_person_id', 'ancestor_person_id'):
                if translated.get(key):
                    translated[key] = resolve(translated[key], mapping)
            if family_path_errors(person['id'], translated):
                ancestor = translated.get('ancestor_person_id') or translated.get('parent_person_id')
                distance = translated.get('generation_distance', 1)
                target = allocate_descendant_id(ancestor, distance, reserved)
                reserved.add(target)
                mapping[person['id']] = target
                person['id'] = target
                changed = True
        if not changed:
            break
    else:
        raise ValueError('Family paths did not converge')
    mapping = {pid: resolve(pid, mapping) for pid in mapping}
    return merged, mapping


def rewrite(value, mapping, key='', pattern=None):
    if pattern is None:
        pattern = re.compile(r'(?<![\w*])(?:' + '|'.join(re.escape(pid) for pid in sorted(mapping, key=len, reverse=True)) + r')(?![\w*])') if mapping else None
    if isinstance(value, dict):
        out = {}
        for k, v in value.items():
            target = mapping.get(k, k)
            rewritten = rewrite(v, mapping, k, pattern)
            if target in out:
                if not isinstance(out[target], list) or not isinstance(rewritten, list):
                    raise ValueError('Mapped dictionary keys collide')
                out[target] = unique(out[target] + rewritten)
            else:
                out[target] = rewritten
        if out.get('record_type') == 'person_equivalence_set':
            for decision in out['decisions']:
                if len(decision['person_ids']) == 1:
                    decision['identity_materialized'] = True
        return out
    if isinstance(value, list):
        out = [rewrite(v, mapping, key, pattern) for v in value]
        return unique(out) if (key == 'person_ids' or key.endswith('_person_ids')) and all(isinstance(x, str) for x in out) else out
    if isinstance(value, str):
        if value in mapping:
            if key in {'text', 'quote', 'original_quote'}:
                raise ValueError('Source text must remain unchanged')
            return mapping[value]
        if pattern and pattern.search(value):
            if key in {'text', 'quote', 'original_quote'}:
                raise ValueError('Source text must remain unchanged')
            return pattern.sub(lambda m: mapping[m.group()], value)
    return value


def reference_files(root):
    """Editable reference layers, excluding regenerated chapter/person exports."""
    paths = list((root / 'registry').glob('*.json'))
    paths += list((root / 'corpus').glob('*/*.json'))
    paths += list((root / 'data/historical-tables').glob('*.json'))
    names = root / 'data/corpus/profile-names.json'
    if names.exists():
        paths.append(names)
    return sorted(paths)


def stage(root, destination):
    people, mapping = plan(root)
    _, records = load_catalog(root)
    decisions = [d for r in records if r.get('record_type') == 'person_equivalence_set' for d in r['decisions']]
    for directory in ('registry', 'corpus'):
        shutil.copytree(root / directory, destination / directory)
    for original in reference_files(root):
        path = destination / original.relative_to(root)
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            shutil.copyfile(original, path)
        data = json.loads(path.read_text())
        if path.name == 'persons.json' and path.parent.name == 'registry':
            data['persons'] = people
        data = rewrite(data, mapping)
        annotation = data.get('annotation', {})
        remaining, resolved = [], annotation.get('resolved_identity_cases', [])
        for case in annotation.get('unresolved_identity_cases', []):
            if len(case['candidate_person_ids']) != 1 or case.get('unknown_identity_possible') is True:
                remaining.append(case)
                continue
            pid = case['candidate_person_ids'][0]
            case['person_id'] = pid
            case.pop('candidate_person_ids')
            case['status'] = 'contextual_provisional'
            case['identity_equivalence_decision_ids'] = [d['id'] for d in decisions if pid in {mapping.get(i, i) for i in d['person_ids']}]
            case['note'] += ' 此案曾列未決；本批按已保存的逐項同指證據整併至唯一人物 ID，來源名稱、引文與暫定狀態保留。'
            resolved.append(case)
        if resolved:
            annotation['resolved_identity_cases'] = resolved
            annotation['unresolved_identity_cases'] = remaining
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
        if data.get('record_type') == 'marked_chapter':
            path.with_suffix('.xml').write_text(render(data))
    return mapping


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix='cbr-identity-preflight-') as tmp:
        destination = Path(tmp)
        mapping = stage(args.root, destination)
        errors = validate(destination)
        report = {'rewritten_ids': len(mapping), 'validation_errors': errors, 'applied': False}
        if args.apply and not errors:
            for path in destination.rglob('*'):
                if path.is_file():
                    target = args.root / path.relative_to(destination)
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(path, target)
            report['applied'] = True
        print(json.dumps(report, ensure_ascii=False, indent=2))
        if errors:
            raise SystemExit(1)


if __name__ == '__main__':
    main()
