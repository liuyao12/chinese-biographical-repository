import copy
import json
import unittest
from pathlib import Path

from scripts.name_xiaoming import validate_xiaoming

ROOT = Path(__file__).resolve().parents[1]


class BiographicalXiaomingTests(unittest.TestCase):
    def setUp(self):
        chapter = json.loads((ROOT / 'corpus/songshu/001-parents-reference.json').read_text())
        self.paragraph = chapter['paragraphs'][0]
        names = json.loads((ROOT / 'corpus/songshu/001-parents-reference-name-components.json').read_text())
        self.name = next(n for n in names['records'] if n.get('id') == 'name-song001-liuyu-explicit')

    def test_explicit_biographical_sequence_does_not_require_a_father_clause(self):
        validate_xiaoming(self.name, self.paragraph)
        self.assertNotIn('father_name_anchor', self.name['xiaoming_basis'])

    def test_different_person_or_untyped_value_cannot_supply_xiaoming(self):
        for field, value in [('person_id', 'different-person'), ('ming', '寄奴'),
                             ('zi', '寄奴'), ('xiaoming', '徳輿'), ('quote', '寄奴')]:
            with self.subTest(field=field):
                name = copy.deepcopy(self.name)
                name[field] = value
                with self.assertRaises(ValueError):
                    validate_xiaoming(name, self.paragraph)

    def test_all_four_mentions_must_bind_the_same_person_and_exact_offsets(self):
        for key in ['subject_anchor', 'ming_anchor', 'zi_anchor', 'xiaoming_anchor']:
            with self.subTest(anchor=key):
                name = copy.deepcopy(self.name)
                name['xiaoming_basis'][key]['person_mention_id'] = 'unavailable'
                with self.assertRaises(ValueError):
                    validate_xiaoming(name, self.paragraph)
        paragraph = copy.deepcopy(self.paragraph)
        paragraph['mentions'][-1]['person_id'] = 'different-person'
        with self.assertRaises(ValueError):
            validate_xiaoming(self.name, paragraph)

    def test_name_markers_scope_and_review_status_cannot_be_swapped(self):
        for key in ['ming_marker_anchor', 'zi_marker_anchor', 'xiaoming_marker_anchor', 'clause_anchor']:
            with self.subTest(anchor=key):
                name = copy.deepcopy(self.name)
                name['xiaoming_basis'][key]['start'] += 1
                with self.assertRaises(ValueError):
                    validate_xiaoming(name, self.paragraph)
        name = copy.deepcopy(self.name)
        name['xiaoming_basis']['human_reviewed'] = True
        with self.assertRaises(ValueError):
            validate_xiaoming(name, self.paragraph)


if __name__ == '__main__':
    unittest.main()
