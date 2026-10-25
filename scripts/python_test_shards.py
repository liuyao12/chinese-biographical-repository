#!/usr/bin/env python3
"""Complete unittest discovery, deterministic case shards, fail-closed manifests."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import unittest

SCHEMA = 1


def flatten(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from flatten(item)
        else:
            yield item


def selection(ids, index, count):
    if type(count) is not int or count < 1 or type(index) is not int or not 0 <= index < count:
        raise ValueError('invalid shard index/count')
    if not ids or any(not isinstance(x, str) or not x for x in ids) or len(ids) != len(set(ids)):
        raise ValueError('empty suite or duplicate/invalid test IDs')
    return [x for x in ids if int.from_bytes(hashlib.sha256(x.encode('utf-8')).digest(), 'big') % count == index]


def revision(value):
    if not isinstance(value, str) or not re.fullmatch(r'[0-9a-fA-F]{40}', value):
        raise ValueError('revision must be a full checkout SHA')
    return value.lower()


def write_manifest(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + '.tmp')
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    os.replace(temp, path)


def discover_cases(start, pattern):
    # Each CLI invocation imports from its checkout, as python -m unittest does.
    if os.getcwd() not in sys.path:
        sys.path.insert(0, os.getcwd())
    loader = unittest.TestLoader()
    cases = list(flatten(loader.discover(start_dir=start, pattern=pattern)))
    if loader.errors or any(isinstance(case, unittest.loader._FailedTest) for case in cases):
        raise ValueError('unittest discovery/import error: ' + '\n'.join(loader.errors))
    ids = [case.id() for case in cases]
    selection(ids, 0, 1)  # validate nonempty, unique IDs without running cases
    return cases, ids


def run_shard(start, pattern, index, count, sha, output, list_only=False):
    sha = revision(sha)
    # Match python -m unittest: checkout cwd is importable, even from scripts/.
    if os.getcwd() not in sys.path:
        sys.path.insert(0, os.getcwd())
    # Persist an incomplete receipt before discovery/run, including import failure.
    data = dict(schema=SCHEMA, revision=sha, shard_index=index, shard_count=count,
                all_ids=[], selected_ids=[], complete=False, success=False, list_only=list_only,
                tests_run=0)
    write_manifest(output, data)
    try:
        cases, ids = discover_cases(start, pattern)
        data.update(all_ids=ids, discovery_scope=dict(start_directory=start, pattern=pattern))
        chosen = selection(ids, index, count)
        if not chosen:
            raise ValueError('empty shard')
        data.update(selected_ids=chosen)
        write_manifest(output, data)
        if list_only:
            # Discovery proof is intentionally not a successful execution receipt.
            data['discovery_complete'] = True
            write_manifest(output, data)
            return 0
        wanted = set(chosen)
        selected = unittest.TestSuite(case for case in cases if case.id() in wanted)
        result = unittest.TextTestRunner(verbosity=2).run(selected)
        data.update(tests_run=result.testsRun, failures=len(result.failures), errors=len(result.errors),
                    skipped=len(result.skipped), expected_failures=len(result.expectedFailures),
                    unexpected_successes=len(result.unexpectedSuccesses),
                    complete=result.testsRun == len(chosen),
                    success=result.wasSuccessful() and result.testsRun == len(chosen))
        write_manifest(output, data)
        return 0 if data['complete'] and data['success'] else 1
    except BaseException as exc:
        data.update(complete=False, success=False, exception=type(exc).__name__ + ': ' + str(exc))
        write_manifest(output, data)
        print(data['exception'], file=sys.stderr)
        return 1


def verify(paths, sha, count, expected_ids):
    sha = revision(sha)
    if type(count) is not int or count < 1 or len(paths) != count:
        raise ValueError('missing/extra shard manifests')
    rows = [json.loads(Path(p).read_text(encoding='utf-8')) for p in paths]
    if any(type(r.get('shard_index')) is not int for r in rows):
        raise ValueError('invalid shard index')
    if sorted(r['shard_index'] for r in rows) != list(range(count)):
        raise ValueError('duplicate/missing shard index')
    selection(expected_ids, 0, 1)
    all_ids = expected_ids
    seen = set()
    for r in rows:
        if (r.get('schema') != SCHEMA or r.get('revision') != sha or r.get('shard_count') != count
                or r.get('all_ids') != all_ids or r.get('list_only') is not False
                or r.get('complete') is not True or r.get('success') is not True):
            raise ValueError('inconsistent, incomplete, unsuccessful or wrong-revision shard')
        expected = selection(all_ids, r['shard_index'], count)
        if not expected or r.get('selected_ids') != expected or type(r.get('tests_run')) is not int or r['tests_run'] != len(expected):
            raise ValueError('shard selection/count mismatch')
        if any(type(r.get(k)) is not int or r[k] != 0 for k in ('failures', 'errors', 'unexpected_successes')):
            raise ValueError('failed shard result')
        if seen.intersection(expected):
            raise ValueError('overlapping shards')
        seen.update(expected)
    if seen != set(all_ids):
        raise ValueError('incomplete test union')
    return len(all_ids)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    run = sub.add_parser('run')
    run.add_argument('--start-directory', default='tests')
    run.add_argument('--pattern', default='test*.py')
    run.add_argument('--index', type=int, required=True)
    run.add_argument('--count', type=int, required=True)
    run.add_argument('--revision', default=os.environ.get('GITHUB_SHA'))
    run.add_argument('--manifest', required=True)
    run.add_argument('--list', action='store_true')
    check = sub.add_parser('verify')
    check.add_argument('--start-directory', default='tests')
    check.add_argument('--pattern', default='test*.py')
    check.add_argument('--revision', default=os.environ.get('GITHUB_SHA'))
    check.add_argument('--count', type=int, required=True)
    check.add_argument('manifests', nargs='+')
    args = parser.parse_args(argv)
    try:
        if args.command == 'run':
            return run_shard(args.start_directory, args.pattern, args.index, args.count,
                             args.revision, args.manifest, args.list)
        _, expected_ids = discover_cases(args.start_directory, args.pattern)
        print(f'PASS checkout-discovered complete test union: {verify(args.manifests, args.revision, args.count, expected_ids)} cases')
        return 0
    except (ValueError, OSError, TypeError, KeyError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
