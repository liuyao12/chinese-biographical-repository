"""Factor repeated historical contexts without changing the fixed evidence snapshot."""
import argparse
import hashlib
import json
from pathlib import Path


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()


def intern(value, records):
    # Order matters here because historical receipts hash the original JSON bytes.
    key = hashlib.sha256(encoded(value)).hexdigest()
    if key in records and records[key] != value:
        raise ValueError('Conflicting evidence record')
    records[key] = value
    return key


def compact(rows):
    sources, contexts, people = {}, {}, []
    for row in rows:
        person = dict(row)
        if 'existing_source_contexts' in row:
            refs = []
            for original in row['existing_source_contexts']:
                context = dict(original)
                context['source'] = intern(context['source'], sources)
                refs.append(intern(context, contexts))
            person['existing_source_contexts'] = refs
        people.append(person)
    return {'format': 'parallel-evidence-refs-v1', 'legacy_sha256': hashlib.sha256(encoded(rows)).hexdigest(),
            'sources': sources, 'contexts': contexts, 'records': people}


def expand(snapshot):
    if snapshot['format'] != 'parallel-evidence-refs-v1':
        raise ValueError('Unknown parallel evidence format')
    rows = []
    for row in snapshot['records']:
        person = dict(row)
        if 'existing_source_contexts' in row:
            contexts = []
            for key in row['existing_source_contexts']:
                context = dict(snapshot['contexts'][key])
                context['source'] = snapshot['sources'][context['source']]
                contexts.append(context)
            person['existing_source_contexts'] = contexts
        rows.append(person)
    if hashlib.sha256(encoded(rows)).hexdigest() != snapshot['legacy_sha256']:
        raise ValueError('Historical evidence digest mismatch')
    return rows


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('compact', 'expand', 'check'))
    parser.add_argument('path', type=Path)
    args = parser.parse_args()
    value = json.loads(args.path.read_bytes())
    if args.action == 'compact':
        snapshot = compact(value)
        if encoded(expand(snapshot)) != args.path.read_bytes():
            raise ValueError('Existing bytes cannot be reconstructed')
        print(encoded(snapshot).decode(), end='')
    elif args.action == 'expand':
        print(encoded(expand(value)).decode(), end='')
    else:
        expand(value)
        print(value['legacy_sha256'])
