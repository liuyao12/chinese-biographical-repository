# coding: utf-8
import copy
import json
import unittest
from pathlib import Path
from scripts.ancestor_reference import ancestor_reference_valid

ROOT = Path(__file__).resolve().parents[1]


class AncestorReference(unittest.TestCase):
    def setUp(self):
        self.chapters = {}
        self.assertions = {}
        for path in (ROOT / 'corpus').glob('*/*.json'):
            d = json.loads(path.read_text())
            if d.get('record_type') == 'marked_chapter':
                self.chapters[d['id']] = d
            if d.get('record_type') == 'person_assertion_set':
                self.assertions.update({a['id']: a for a in d['assertions']})
        self.families = json.loads((ROOT / 'registry/family-assemblies.json').read_text())['assemblies']
        self.d = next(d for d in json.loads((ROOT / 'corpus/nanshi/024-identities.json').read_text())['decisions']
                      if 'ancestor_reference' in d)

    def valid(self, d=None, families=None):
        return ancestor_reference_valid(d or self.d, self.chapters, self.assertions,
                                        families or self.families)

    def test_speaker_specific_three_sourced_generations(self):
        self.assertTrue(self.valid())
        a = self.assertions['a-nanshi024-jinghong-maternal-grandfather']
        self.assertEqual(a['subject_person_id'], self.d['person_id'])
        self.assertEqual(a['qualifiers']['lineage'], 'maternal')
        self.assertIsNone(a['qualifiers']['mother_person_id'])

    def test_son_cannot_replace_actual_speaker(self):
        d = copy.deepcopy(self.d)
        d['ancestor_reference']['speaker_person_id'] = self.assertions['a-nanshi024-cong-father']['subject_person_id']
        self.assertFalse(self.valid(d))

    def test_fabricated_path_or_wrong_generation_is_rejected(self):
        d = copy.deepcopy(self.d)
        d['ancestor_reference']['person_path'][1] = self.d['person_id']
        self.assertFalse(self.valid(d))
        d = copy.deepcopy(self.d)
        d['ancestor_reference']['generation_distance'] = 2
        self.assertFalse(self.valid(d))

    def test_parent_ids_do_not_suffice_without_matching_source_edges(self):
        d = copy.deepcopy(self.d)
        d['ancestor_reference']['steps'][0]['assertion_id'] = 'a-nanshi024-xin-father'
        self.assertFalse(self.valid(d))
        families = copy.deepcopy(self.families)
        f = next(f for f in families if f['id'] == 'family-langye-wang-dao')
        member = next(m for m in f['members'] if m['person_id'] == self.d['ancestor_reference']['person_path'][2])
        member['parent_connection']['farther_ancestor_assertion_id'] = 'missing'
        self.assertFalse(self.valid(families=families))

    def test_ancestor_and_speaker_anchors_are_not_interchangeable(self):
        d = copy.deepcopy(self.d)
        d['ancestor_reference']['ancestor_mention_id'] = d['ancestor_reference']['speaker_mention_id']
        self.assertFalse(self.valid(d))


if __name__ == '__main__':
    unittest.main()
