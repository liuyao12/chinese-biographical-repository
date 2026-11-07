"""Deterministic complete unittest discovery, execution ledgers, and strict coverage.

No changed-file selection: occurrences from ordinary ``discover -s tests``
retain serial order and are assigned round-robin. A missing/failed/foreign report
cannot pass aggregation.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict, deque
import hashlib
import io
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = 1
POLICY = 'tests/python-skip-policy.json'
OUTPUT_DIRS = {'.git', '.ci-results', 'build', '_site', 'node_modules', '.venv', 'venv'}
CACHE_DIRS = {'__pycache__', '.pytest_cache'}

class CoverageError(ValueError):
    pass


def require(ok, message):
    if not ok:
        raise CoverageError(message)


def canonical(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')) + '\n').encode()


def digest(value):
    return hashlib.sha256(value).hexdigest()


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix='.unittest-manifest-', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(canonical(value))
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def check_commit(root, commit, require_head=False):
    require(isinstance(commit, str) and re.fullmatch(r'[0-9a-f]{40}|[0-9a-f]{64}', commit), 'invalid source commit')
    if require_head:
        found = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip()
        require(found == commit, 'checkout commit differs from plan/source commit')
        result = subprocess.run(['git', 'diff', '--quiet', 'HEAD', '--'], cwd=root, check=False)
        require(result.returncode == 0, 'tracked checkout inputs changed')
        # Include ignored files in this query too: an ignored corpus JSON could
        # otherwise affect discovery/validation while absent from the commit.
        untracked = subprocess.check_output(['git', 'ls-files', '--others', '-z'], cwd=root).decode().split('\0')
        require(not any(path and source_path(Path(path)) for path in untracked), 'untracked source inputs present')


def source_path(relative):
    return bool(relative.parts) and relative.parts[0] not in OUTPUT_DIRS and not any(
        part in CACHE_DIRS or part == '.DS_Store' for part in relative.parts)


def fingerprint(root):
    root = Path(root)
    paths = []
    for current, directories, files in os.walk(root):
        parent = Path(current)
        directories[:] = [name for name in directories if source_path((parent / name).relative_to(root))]
        for name in directories:
            require(not (parent / name).is_symlink(), 'source directory symlink is not a pinned input')
        for name in files:
            path = parent / name
            if source_path(path.relative_to(root)):
                require(not path.is_symlink(), 'source file symlink is not a pinned input')
                paths.append(path)
    entries = [{'path': p.relative_to(root).as_posix(), 'sha256': digest(p.read_bytes())}
               for p in sorted(paths) if p.is_file()]
    return digest(canonical(entries))


def flatten(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from flatten(item)
        else:
            require(isinstance(item, unittest.TestCase), 'discovery returned a non-TestCase')
            yield item


def discover(root):
    root = Path(root).resolve()
    loader = unittest.TestLoader()
    # Match python -m unittest discover -s tests: default pattern/top-level rules.
    suite = loader.discover(str(root / 'tests'), pattern='test*.py')
    require(not loader.errors, 'unittest discovery errors:\n' + '\n'.join(loader.errors))
    tests = list(flatten(suite))
    require(not any(isinstance(test, unittest.loader._FailedTest) for test in tests), 'discovery returned a failed-loader sentinel')
    ids = [test.id() for test in tests]
    require(ids and all(isinstance(item, str) and item for item in ids), 'empty/invalid discovered test inventory')
    # Ordinary unittest can collect an imported TestCase more than once. Keep
    # every serial occurrence; never deduplicate it or rewrite TestCase.id().
    return tests


def instances(tests):
    seen = Counter()
    rows = []
    for test in tests:
        test_id = test.id()
        seen[test_id] += 1
        ordinal = seen[test_id]
        rows.append({'test_id': test_id, 'occurrence_ordinal': ordinal,
                     'execution_key': json.dumps([test_id, ordinal], separators=(',', ':'))})
    return rows


def skip_rules(root, tests, descriptors):
    allowed = {}
    expected_failures = []
    policy_path = Path(root) / POLICY
    policy = json.loads(policy_path.read_text()) if policy_path.exists() else {
        'schema_version': SCHEMA, 'static_skips': [], 'dynamic_skips': [], 'expected_failures': []}
    require(policy.get('schema_version') == SCHEMA, 'invalid skip policy schema')
    known_ids = {row['test_id'] for row in descriptors}
    def baseline(rows, label):
        result = {}
        for row in rows:
            test_id = row['test_id']
            require(test_id in known_ids and test_id not in result, 'unknown/duplicate ' + label + ' policy test')
            require(isinstance(row['reason'], str) and row['reason'], 'policy needs an exact reason')
            result[test_id] = row
        return result
    static = baseline(policy.get('static_skips', []), 'static skip')
    dynamic = baseline(policy.get('dynamic_skips', []), 'dynamic skip')
    expected = baseline(policy.get('expected_failures', []), 'expected failure')
    def capability(condition):
        if set(condition) == {'platform_not'}:
            require(condition['platform_not'] in ('darwin', 'linux', 'win32'), 'unsupported baseline platform')
            return sys.platform != condition['platform_not']
        require(set(condition) == {'missing_os_attribute'} and condition['missing_os_attribute'] == 'symlink', 'unsupported static skip capability')
        return not hasattr(os, 'symlink')
    active_static = {test_id: capability(row['condition']) for test_id, row in static.items()}
    for test, descriptor in zip(tests, descriptors):
        key, test_id = descriptor['execution_key'], descriptor['test_id']
        cls = test.__class__
        method = getattr(test, test._testMethodName)
        if getattr(cls, '__unittest_skip__', False) or getattr(method, '__unittest_skip__', False):
            reason = (getattr(cls, '__unittest_skip_why__', '') or getattr(method, '__unittest_skip_why__', ''))
            require(test_id in static and active_static[test_id] and reason == static[test_id]['reason'], 'unapproved decorator skip: ' + test_id)
            allowed[key] = reason
        if getattr(cls, '__unittest_expecting_failure__', False) or getattr(method, '__unittest_expecting_failure__', False):
            require(test_id in expected, 'unapproved expectedFailure decorator: ' + test_id)
            expected_failures.append(key)
    for test_id, row in dynamic.items():
        condition = row['condition']
        require(set(condition) == {'path_missing'}, 'unsupported dynamic skip condition')
        relative = Path(condition['path_missing'])
        require(not relative.is_absolute() and '..' not in relative.parts, 'unsafe skip-policy path')
        if not (Path(root) / relative).exists():
            for descriptor in descriptors:
                if descriptor['test_id'] != test_id:
                    continue
                key = descriptor['execution_key']
                require(key not in allowed or allowed[key] == row['reason'], 'conflicting skip reasons')
                allowed[key] = row['reason']
    return allowed, sorted(expected_failures)


def discovery_snapshot(root, commit, shards=8, require_head=False):
    require(type(shards) is int and shards > 0, 'invalid shard count')
    check_commit(root, commit, require_head)
    tests = discover(root)
    descriptors = instances(tests)
    allowed_skips, expected_failures = skip_rules(root, tests, descriptors)
    ids = [row['test_id'] for row in descriptors]
    plan = {'schema_version': SCHEMA, 'record_type': 'complete_unittest_plan',
            'source_commit': commit, 'shard_count': shards,
            'discovery': {'start_dir': 'tests', 'pattern': 'test*.py', 'top_level_dir': None},
            'python_major_minor': list(sys.version_info[:2]), 'platform': sys.platform,
            'test_instances': descriptors, 'original_discovery_test_ids': ids,
            'execution_keys': [row['execution_key'] for row in descriptors],
            'original_id_multiplicities': dict(Counter(ids)),
            'inventory_sha256': digest(canonical(descriptors)),
            'test_sources_sha256': fingerprint(root), 'allowed_skips': allowed_skips,
            'allowed_expected_failures': expected_failures}
    return plan, tests


def make_plan(root, commit, shards=8, require_head=False):
    return discovery_snapshot(root, commit, shards, require_head)[0]


def validate_plan(plan):
    require(plan.get('schema_version') == SCHEMA and plan.get('record_type') == 'complete_unittest_plan', 'invalid plan schema')
    require(type(plan.get('shard_count')) is int and plan['shard_count'] > 0, 'invalid plan shard count')
    descriptors = plan.get('test_instances')
    require(isinstance(descriptors, list) and descriptors, 'empty plan inventory')
    seen = Counter()
    for row in descriptors:
        require(isinstance(row, dict) and isinstance(row.get('test_id'), str) and row['test_id'], 'invalid test instance')
        seen[row['test_id']] += 1
        require(type(row.get('occurrence_ordinal')) is int and row['occurrence_ordinal'] == seen[row['test_id']], 'invalid discovery occurrence ordinal')
        require(row.get('execution_key') == json.dumps([row['test_id'], seen[row['test_id']]], separators=(',', ':')), 'invalid execution key')
    keys = [row['execution_key'] for row in descriptors]
    require(len(keys) == len(set(keys)) and plan.get('execution_keys') == keys, 'duplicate/different execution keys')
    require(plan.get('original_discovery_test_ids') == [row['test_id'] for row in descriptors], 'original discovery order differs')
    require(plan.get('original_id_multiplicities') == dict(seen), 'original test ID multiplicity differs')
    require(plan['inventory_sha256'] == digest(canonical(descriptors)), 'plan inventory digest differs')
    require(set(plan['allowed_skips']) <= set(keys), 'skip policy outside inventory')
    require(set(plan['allowed_expected_failures']) <= set(keys), 'expected failure outside inventory')
    return plan


class LedgerResult(unittest.TextTestResult):
    def __init__(self, *args, descriptors, **kwargs):
        super().__init__(*args, **kwargs)
        self.descriptors = {row['execution_key']: row for row in descriptors}
        self.queues = defaultdict(deque)
        for row in descriptors:
            self.queues[row['test_id']].append(row['execution_key'])
        self.active = {}
        self.started_ids = []
        self.started_keys = []
        self.rows = {}
        self.subtest_skips = []

    def row(self, test):
        parent = getattr(test, 'test_case', test)
        key = self.active.get(id(parent), 'unplanned:' + parent.id())
        descriptor = self.descriptors.get(key, {'execution_key': key, 'test_id': parent.id(), 'occurrence_ordinal': None})
        return self.rows.setdefault(key, {**descriptor, 'status': 'incomplete'})

    def startTest(self, test):
        key = self.queues[test.id()].popleft() if self.queues[test.id()] else 'unplanned:' + test.id()
        self.active[id(test)] = key
        self.started_ids.append(test.id())
        self.started_keys.append(key)
        self.row(test)
        super().startTest(test)

    def stopTest(self, test):
        super().stopTest(test)
        self.active.pop(id(test), None)

    def addSuccess(self, test):
        row = self.row(test)
        if row['status'] == 'incomplete':
            row['status'] = 'success'
        super().addSuccess(test)

    def addFailure(self, test, err):
        self.row(test).update(status='failure', detail=self._exc_info_to_string(err, test))
        super().addFailure(test, err)

    def addError(self, test, err):
        self.row(test).update(status='error', detail=self._exc_info_to_string(err, test))
        super().addError(test, err)

    def addSkip(self, test, reason):
        if hasattr(test, 'test_case'):
            self.subtest_skips.append({'test_id': test.test_case.id(), 'execution_key': self.row(test)['execution_key'],
                                      'subtest_id': test.id(), 'reason': reason})
        else:
            self.row(test).update(status='skipped', reason=reason)
        super().addSkip(test, reason)

    def addExpectedFailure(self, test, err):
        self.row(test).update(status='expected_failure')
        super().addExpectedFailure(test, err)

    def addUnexpectedSuccess(self, test):
        self.row(test).update(status='unexpected_success')
        super().addUnexpectedSuccess(test)

    def addSubTest(self, test, subtest, err):
        if err is not None:
            self.row(test).update(status='failure' if issubclass(err[0], test.failureException) else 'error',
                                  detail=self._exc_info_to_string(err, test))
        super().addSubTest(test, subtest, err)


def report_errors(plan, report, index):
    errors = []
    def ck(ok, message):
        if not ok:
            errors.append(message)
    descriptors = plan['test_instances'][index::plan['shard_count']]
    assigned = [row['execution_key'] for row in descriptors]
    raw_ids = [row['test_id'] for row in descriptors]
    by_key = {row['execution_key']: row for row in descriptors}
    ck(report.get('schema_version') == SCHEMA and report.get('record_type') == 'unittest_shard_result', 'invalid result schema')
    for key in ['source_commit', 'shard_count', 'inventory_sha256', 'test_sources_sha256', 'python_major_minor', 'platform']:
        ck(report.get(key) == plan.get(key), 'mixed result ' + key)
    ck(report.get('shard_index') == index, 'shard index differs')
    ck(report.get('assigned_execution_keys') == assigned and report.get('assigned_test_ids') == raw_ids, 'shard assignment differs')
    started = report.get('started_execution_keys', [])
    ck(isinstance(started, list) and len(started) == len(set(started)) and started == assigned, 'missing/duplicate/extra or reordered started test occurrences')
    ck(report.get('started_test_ids') == raw_ids, 'started original test IDs/order differ')
    rows = report.get('results', [])
    row_ids = [r.get('execution_key') for r in rows if isinstance(r, dict)]
    ck(len(row_ids) == len(rows) == len(set(row_ids)) and set(row_ids) == set(assigned), 'missing/duplicate/extra result records')
    for row in rows:
        if not isinstance(row, dict):
            continue
        status, test_id, key = row.get('status'), row.get('test_id'), row.get('execution_key')
        expected = by_key.get(key)
        ck(bool(expected) and all(row.get(field) == expected[field] for field in ('test_id', 'occurrence_ordinal', 'execution_key')), 'result original ID/occurrence differs')
        if status == 'skipped':
            ck(key in plan['allowed_skips'] and row.get('reason') == plan['allowed_skips'][key], 'unexpected skip: ' + str(test_id))
        elif status == 'expected_failure':
            ck(key in plan['allowed_expected_failures'], 'unplanned expected failure: ' + str(test_id))
        else:
            ck(status == 'success', 'unsuccessful/incomplete test: ' + str(test_id))
    ck(not report.get('subtest_skips'), 'unexpected skipped subtest')
    ck(report.get('failures') == 0 and report.get('errors') == 0 and report.get('unexpected_successes') == 0, 'unittest failure/error/unexpected-success count')
    ck(report.get('tests_run') == len(assigned), 'unittest execution count differs')
    ck(report.get('complete') is True and report.get('unittest_successful') is True, 'incomplete or unsuccessful shard')
    return errors


def run_shard(root, plan, index, plan_sha256, commit, require_head=False, output=None, stream=None):
    validate_plan(plan)
    require(type(index) is int and 0 <= index < plan['shard_count'], 'invalid shard index')
    check_commit(root, commit, require_head)
    require(commit == plan['source_commit'], 'requested commit differs from plan')
    current, tests = discovery_snapshot(root, commit, plan['shard_count'], require_head)
    require(current == plan, 'fresh full discovery/source/skip policy differs from plan')
    descriptors = plan['test_instances'][index::plan['shard_count']]
    selected = tests[index::plan['shard_count']]
    ids = [row['test_id'] for row in descriptors]
    keys = [row['execution_key'] for row in descriptors]
    base = {key: plan[key] for key in ['source_commit', 'shard_count', 'inventory_sha256', 'test_sources_sha256', 'python_major_minor', 'platform']}
    base.update(schema_version=SCHEMA, record_type='unittest_shard_result', shard_index=index,
                plan_sha256=plan_sha256, assigned_test_ids=ids, assigned_execution_keys=keys, complete=False)
    if output:
        write_json(output, base)
    def result_class(*args, **kwargs):
        return LedgerResult(*args, descriptors=descriptors, **kwargs)
    result = unittest.TextTestRunner(verbosity=2, resultclass=result_class, stream=stream or sys.stderr).run(
        unittest.TestSuite(selected))
    base.update(started_test_ids=result.started_ids, started_execution_keys=result.started_keys, results=list(result.rows.values()),
                subtest_skips=result.subtest_skips, tests_run=result.testsRun,
                failures=len(result.failures), errors=len(result.errors),
                unexpected_successes=len(result.unexpectedSuccesses), unittest_successful=result.wasSuccessful(), complete=True)
    # A test cannot silently alter the next shard's source inputs or tracked checkout.
    source_errors = []
    if fingerprint(root) != plan['test_sources_sha256']:
        source_errors.append('test source files changed during execution')
    try:
        check_commit(root, commit, require_head)
    except (CoverageError, subprocess.SubprocessError) as error:
        source_errors.append(str(error))
    base['integrity_errors'] = source_errors + report_errors(plan, base, index)
    base['exit_code'] = 1 if base['integrity_errors'] else 0
    if output:
        write_json(output, base)
    return base


def aggregate(plan, reports, plan_sha256, commit):
    validate_plan(plan)
    require(commit == plan['source_commit'], 'aggregate commit differs from plan')
    require(len(reports) == plan['shard_count'], 'missing or extra shard reports')
    indices = [r.get('shard_index') for r in reports]
    require(all(type(i) is int for i in indices) and sorted(indices) == list(range(plan['shard_count'])), 'missing/duplicate/extra shard index')
    issues = []
    for report in reports:
        index = report['shard_index']
        if report.get('plan_sha256') != plan_sha256:
            issues.append('mixed plan digest')
        issues.extend(report_errors(plan, report, index))
        if report.get('integrity_errors') or report.get('exit_code') != 0:
            issues.append('shard reports unsuccessful integrity/exit')
    seen = [key for report in reports for key in report.get('started_execution_keys', [])]
    raw_seen = [test_id for report in reports for test_id in report.get('started_test_ids', [])]
    require(len(seen) == len(set(seen)) and set(seen) == set(plan['execution_keys']), 'overall missing/duplicate/extra executed occurrences')
    require(dict(Counter(raw_seen)) == plan['original_id_multiplicities'], 'overall original test ID multiplicity differs')
    require(not issues, '; '.join(issues))
    return {'schema_version': SCHEMA, 'record_type': 'complete_unittest_coverage',
            'source_commit': commit, 'plan_sha256': plan_sha256,
            'inventory_sha256': plan['inventory_sha256'], 'shard_count': plan['shard_count'],
            'tests': len(seen), 'covered_execution_keys': plan['execution_keys'],
            'original_id_multiplicities': plan['original_id_multiplicities'],
            'skipped': [r for report in reports for r in report['results'] if r['status'] == 'skipped'],
            'expected_failures': [r for report in reports for r in report['results'] if r['status'] == 'expected_failure'],
            'complete': True, 'successful': True}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for command in ['plan', 'run', 'aggregate']:
        p = sub.add_parser(command)
        p.add_argument('--root', type=Path, default=ROOT)
        p.add_argument('--commit', required=True)
        p.add_argument('--require-head-commit', action='store_true')
        p.add_argument('--output', type=Path, required=True)
        if command == 'plan':
            p.add_argument('--shards', type=int, default=8)
        else:
            p.add_argument('--plan', type=Path, required=True)
        if command == 'run':
            p.add_argument('--index', type=int, required=True)
        if command == 'aggregate':
            p.add_argument('--reports', type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == 'plan':
            value = make_plan(args.root, args.commit, args.shards, args.require_head_commit)
        else:
            raw = args.plan.read_bytes()
            plan = json.loads(raw)
            if args.command == 'run':
                value = run_shard(args.root, plan, args.index, digest(raw), args.commit,
                                  args.require_head_commit, args.output)
            else:
                check_commit(args.root, args.commit, args.require_head_commit)
                require(make_plan(args.root, args.commit, plan['shard_count'], args.require_head_commit) == plan, 'aggregate fresh full discovery/source/skip policy differs from plan')
                reports = [json.loads(path.read_text()) for path in sorted(args.reports.glob('shard-*.json'))]
                value = aggregate(plan, reports, digest(raw), args.commit)
        write_json(args.output, value)
        print(json.dumps({'command': args.command, 'tests': len(value.get('execution_keys', value.get('assigned_execution_keys', value.get('covered_execution_keys', [])))), 'successful': value.get('successful', value.get('exit_code', 0) == 0)}))
        return value.get('exit_code', 0)
    except (CoverageError, OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as error:
        write_json(args.output, {'schema_version': SCHEMA, 'record_type': 'unittest_sharding_error',
                                 'complete': False, 'successful': False, 'source_commit': args.commit,
                                 'error': str(error)})
        print(str(error), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
