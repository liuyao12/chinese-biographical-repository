import json
import tempfile
import unittest
from pathlib import Path
from scripts.consolidate_person_ids import reference_files, rewrite


class ConsolidationReferenceTests(unittest.TestCase):
    def setUp(self):
        self.old = 'abc_def_123_A'
        self.new = 'ghi_jkl_456_B'
        self.mapping = {self.old: self.new}

    def test_source_quotes_and_text_cannot_be_rewritten(self):
        for field in ('text', 'quote', 'original_quote'):
            with self.assertRaises(ValueError):
                rewrite({field: 'Evidence ' + self.old}, self.mapping)

    def test_missing_generations_are_preserved(self):
        data = {'intermediate_person_ids': [None, None],
                'person_ids': [self.old, self.new]}
        result = rewrite(data, self.mapping)
        self.assertEqual(result['intermediate_person_ids'], [None, None])
        self.assertEqual(result['person_ids'], [self.new])

    def test_decision_keeps_evidence_and_mention_anchors(self):
        data = {'record_type': 'person_equivalence_set', 'decisions': [{
            'id': 'synthetic-decision', 'person_ids': [self.old, self.new],
            'canonical_person_id': self.new,
            'evidence': [{'mention_id': 'synthetic-mention', 'quote': '甲'}]}]}
        result = rewrite(data, self.mapping)['decisions'][0]
        self.assertTrue(result['identity_materialized'])
        self.assertEqual(result['evidence'], data['decisions'][0]['evidence'])
        self.assertEqual(result['id'], 'synthetic-decision')

    def test_tables_and_profile_names_are_staged_but_exports_are_not(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            files = ['registry/persons.json', 'corpus/book/chapter.json',
                     'data/historical-tables/table.json',
                     'data/corpus/profile-names.json',
                     'data/corpus/persons/stale.json']
            for name in files:
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(json.dumps({}))
            actual = {str(p.relative_to(root)) for p in reference_files(root)}
            self.assertEqual(actual, set(files[:-1]))

    def test_child_id_is_not_changed_by_parent_substring(self):
        child = self.old + 'A'
        self.assertEqual(rewrite({'person_id': child}, self.mapping)['person_id'], child)
