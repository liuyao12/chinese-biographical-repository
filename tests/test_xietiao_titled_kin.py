"""Fixed readings of kin identified by name in one place and title in another."""
import json
import unittest
from copy import deepcopy
from pathlib import Path

from scripts.xietiao_titled_kin import CASES, valid

ROOT = Path(__file__).resolve().parents[1]


class TitledKinTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapters = {}
        cls.claims = {}
        for path in (ROOT / 'corpus').glob('*/*xietiao*.json'):
            data = json.loads(path.read_text())
            if data.get('record_type') == 'marked_chapter':
                cls.chapters[data['id']] = data
            cls.claims.update({a['id']: a for a in data.get('assertions', [])})

    def test_all_ordered_pairs(self):
        for aid in CASES:
            with self.subTest(aid=aid):
                original = self.claims[aid]
                self.assertTrue(valid(original, self.chapters, ROOT))
                changed = deepcopy(original)
                changed['subject_person_id'], changed['object_person_id'] = (
                    changed['object_person_id'], changed['subject_person_id'])
                self.assertFalse(valid(changed, self.chapters, ROOT))

    def test_distinct_princesses(self):
        married = self.claims['a-nanshi019-tiao-wan-marriage']
        sister = self.claims['a-nanshi019-tiao-yao-marriage']
        for field in ('subject_person_id', 'object_person_id'):
            changed = deepcopy(married)
            changed[field] = sister[field]
            self.assertFalse(valid(changed, self.chapters, ROOT))

    def test_exact_wording_and_revision(self):
        for aid in CASES:
            with self.subTest(aid=aid):
                changed = deepcopy(self.claims[aid])
                support = changed['qualifiers']['reading_basis']['support'][0]
                support['start'] += 1
                self.assertFalse(valid(changed, self.chapters, ROOT))
                changed = deepcopy(self.claims[aid])
                changed['qualifiers']['reading_basis']['source_revision'] = 1
                self.assertFalse(valid(changed, self.chapters, ROOT))

    def test_named_external_witness(self):
        aid = 'a-nanshi019-tiao-wan-marriage'
        chapters = deepcopy(self.chapters)
        proof = chapters['c-liangshu-007-xietiao-princesses']
        for para in proof['paragraphs']:
            para['mentions'] = [m for m in para['mentions'] if m['surface'] != '玉婉']
        self.assertFalse(valid(self.claims[aid], chapters, ROOT))
