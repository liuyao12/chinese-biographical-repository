import copy
import json
import unittest
from pathlib import Path

from scripts.person_bundle import validate_courtesy_name


class Song052CalledByCourtesy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path(__file__).resolve().parents[1]
        cls.chapter = json.loads((root / 'corpus/songshu/052-xiejingren.json').read_text())
        names = json.loads((root / 'corpus/songshu/052-xiejingren-name-components.json').read_text())
        cls.name = next(n for n in names['records'] if n['id'] == 'name-song052-literal-001')

    def test_received_called_by_courtesy_has_unknown_ming_and_exact_source(self):
        n = self.name
        p = next(p for p in self.chapter['paragraphs'] if p['id'] == n['paragraph_id'])
        m = next(m for m in p['mentions'] if m['id'] == n['person_mention_id'])
        self.assertEqual(n['quote'], p['text'])
        self.assertEqual(m['person_id'], n['person_id'])
        self.assertEqual(m['surface'], n['surname'] + n['zi'])
        self.assertIsNone(n['ming'])
        self.assertEqual(n['zi'], '景仁')
        self.assertIsNone(validate_courtesy_name(n))

    def test_missing_basis_cannot_pass_as_literal_zi_sequence(self):
        n = copy.deepcopy(self.name)
        n.pop('zi_basis')
        self.assertRaises(ValueError, validate_courtesy_name, n)

    def test_courtesy_cannot_become_given_name(self):
        n = copy.deepcopy(self.name)
        n['ming'] = n['zi']
        self.assertRaises(ValueError, validate_courtesy_name, n)

    def test_wrong_subject_or_marker_is_rejected(self):
        for field in ('subject_anchor', 'marker_anchor'):
            n = copy.deepcopy(self.name)
            n['zi_basis'][field]['start'] += 1
            self.assertRaises(ValueError, validate_courtesy_name, n)

    def test_same_label_elsewhere_does_not_replace_biography_head(self):
        n = copy.deepcopy(self.name)
        n['zi_basis']['subject_anchor']['start'] = n['quote'].rfind('景仁')
        self.assertRaises(ValueError, validate_courtesy_name, n)

    def test_other_source_wording_cannot_be_used_as_called_by_zi(self):
        n = copy.deepcopy(self.name)
        n['quote'] = n['quote'].replace('故稱字', '故稱名')
        self.assertRaises(ValueError, validate_courtesy_name, n)

    def test_ai_record_does_not_acquire_human_review(self):
        n = copy.deepcopy(self.name)
        n['zi_basis']['human_reviewed'] = True
        self.assertRaises(ValueError, validate_courtesy_name, n)

    def test_orphan_basis_requires_zi(self):
        n = copy.deepcopy(self.name)
        n.pop('zi')
        self.assertRaises(ValueError, validate_courtesy_name, n)

    def test_existing_explicit_zi_form_remains_supported(self):
        self.assertIsNone(validate_courtesy_name({'ming': '甲', 'zi': '乙', 'quote': '甲字乙'}))


if __name__ == '__main__':
    unittest.main()
