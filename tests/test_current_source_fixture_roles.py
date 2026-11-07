"""Finite received-source fixtures must tolerate coherent rekeys, not broken ownership."""
import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.current_source_fixture_roles import project_fixture_roles, REF
DATA = json.loads((ROOT / 'tests/fixtures/current-source-fixture-roles.json').read_text())

class CurrentSourceFixtureRoles(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        c = DATA['contract']
        for rel, content in [(REF, json.dumps(c, ensure_ascii=False, indent=2) + '\n'), (c['historical_capture'], DATA['historical_capture_utf8'])]:
            p = self.root / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content)
        self.expected = copy.deepcopy(DATA['expected'])
        self.people = copy.deepcopy(DATA['people'])
        self.chapters = copy.deepcopy(DATA['chapters'])
    def call(self, path=None):
        return project_fixture_roles(self.expected, path or DATA['contract']['fixture_path'], self.root, self.people, self.chapters)
    def marker(self, role='xiezong', index=0):
        s = DATA['contract']['roles'][role]
        p = next(p for p in self.chapters[s['source_path']]['paragraphs'] if p['id'] == s['paragraph_id'])
        return next(m for m in p['mentions'] if m['id'] == s['markers'][index]['id'])
    def test_original_and_private_return(self):
        out = self.call()
        self.assertEqual(out, self.expected)
        out['xiezong'] = 'changed'
        self.assertNotEqual(out, self.expected)
    def test_coherent_rekey_uses_current_mid_not_saved_id(self):
        old = self.marker()['person_id']; new = 'abc_def_123_A'
        self.people[new] = self.people.pop(old); self.people[new]['id'] = new
        self.marker()['person_id'] = new; self.marker(index=1)['person_id'] = new
        out = self.call()
        self.assertEqual(out['xiezong'], new)
        self.assertEqual({k:v for k,v in out.items() if k!='xiezong'}, {k:v for k,v in self.expected.items() if k!='xiezong'})
    def test_distinct_source_roles_cannot_collapse_to_one_owner(self):
        old = self.expected['donghun']; target = self.expected['xiezong']
        second = self.people.pop(old); self.people[target]['evidence'] += second['evidence']; self.people[target]['aliases'] += second['aliases']
        self.marker('donghun')['person_id'] = target
        with self.assertRaises(AssertionError): self.call()
    def test_split_same_person_markers_rejected(self):
        self.marker(index=1)['person_id'] = self.expected['donghun']
        with self.assertRaises(AssertionError): self.call()
    def test_missing_reverse_rejected(self):
        p = self.people[self.marker()['person_id']]
        p['evidence'] = [e for e in p['evidence'] if e.get('mention_id') != self.marker()['id']]
        with self.assertRaises(AssertionError): self.call()
    def test_duplicate_reverse_owner_rejected(self):
        p = copy.deepcopy(self.people[self.marker()['person_id']]);p['id'] = 'abc_def_123_B';self.people[p['id']] = p
        with self.assertRaises(AssertionError): self.call()
    def test_wrong_alias_surface_rejected(self):
        p = self.people[self.marker()['person_id']]
        for a in p['aliases']:
            if self.marker()['id'] in a['mention_ids']:a['surface'] = 'wrong'
        with self.assertRaises(AssertionError): self.call()
    def test_marker_kind_change_rejected(self):
        self.marker()['kind'] = 'pronoun'
        with self.assertRaises(AssertionError): self.call()
    def test_source_identity_required(self):
        s = DATA['contract']['roles']['xiezong'];self.chapters[s['source_path']]['source']['revision_id'] = 'other'
        with self.assertRaises(AssertionError): self.call()
    def test_paragraph_bytes_required(self):
        s = DATA['contract']['roles']['xiezong'];p = next(p for p in self.chapters[s['source_path']]['paragraphs'] if p['id'] == s['paragraph_id']);p['text'] += '改'
        with self.assertRaises(AssertionError): self.call()
    def test_changed_historical_capture_rejected(self):
        p = self.root / DATA['contract']['historical_capture'];p.write_text(p.read_text() + ' ')
        with self.assertRaises(AssertionError): self.call()
    def test_arbitrary_expected_endpoint_rejected(self):
        self.expected['xiezong'] = self.expected['donghun']
        with self.assertRaises(AssertionError): self.call()
    def test_unrelated_path_unchanged(self):
        self.assertIs(self.call('unrelated.json'), self.expected)

if __name__ == '__main__':unittest.main()
