"""Synthetic metadata fixtures; these are not historical source records."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from scripts.reading_witness_preferences import enrich_outputs


def encoded(value):
    return json.dumps(value, ensure_ascii=False).encode()


class ReadingWitnessPreferences(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / 'registry').mkdir()
        (self.root / 'data/historical-tables').mkdir(parents=True)
        (self.root / 'data/historical-tables/index.json').write_bytes(encoded({'tables': []}))
        self.policy = {'schema_version': 1, 'application_scope': 'reading_display_only',
            'unselected_role': 'comparison_transcription', 'human_reviewed': False,
            'model': None, 'policy_note': '合成測試的明確閱讀選擇。', 'preferences': [{
                'source_id': 's-preferred', 'work_id': 'w-test', 'book_id': 'b-test-001',
                'chapter_id': 'c-z-preferred', 'edition_id': 'edition-test',
                'role': 'preferred_received_selection', 'scope': 'source_extent_only',
                'selection_label': '合成選錄',
                'reference_ids': ['ref-test'], 'rationale': '合成測試，僅排序閱讀入口。'}]}
        self.provenance = {'references': {'ref-test': {'url': 'https://example.invalid/edition'}},
            'editions': {'edition-test': {'work_id': 'w-test', 'label': '合成版名'}},
            'text_bases': {'s-preferred': {'work_id': 'w-test', 'status': 'documented',
                'edition_id': 'edition-test', 'reference_ids': ['ref-test']},
                's-old': {'work_id': 'w-test', 'status': 'not_researched', 'edition_id': None}}}
        self.index_path = self.root / 'data/corpus/test/index.json'
        self.generated = {self.root / 'data/corpus/works.json': encoded({'works': [
            {'catalog_path': 'data/corpus/test/index.json'}]}),
            self.root / 'data/corpus/work-provenance.json': encoded(self.provenance)}
        entries = []
        for chapter_id, source_id in [('c-a-old', 's-old'), ('c-z-preferred', 's-preferred')]:
            path = f'data/corpus/test/{chapter_id}.json'
            chapter = {'id': chapter_id, 'source_id': source_id,
                       'work_id': 'w-test', 'book_id': 'b-test-001'}
            self.generated[self.root / path] = encoded(chapter)
            entries.append({'number': 1, 'chapter_id': chapter_id,
                'book_id': 'b-test-001', 'available': 'marked_text', 'path': path})
        self.generated[self.index_path] = encoded({'work_id': 'w-test', 'chapters': entries})

    def run_policy(self):
        (self.root / 'registry/reading-witness-preferences.json').write_bytes(encoded(self.policy))
        return enrich_outputs(self.generated, self.root)

    def test_explicit_choice_sorts_first_and_keeps_unknown_base_as_comparison(self):
        before = copy.deepcopy(self.generated)
        result = self.run_policy()
        first, second = json.loads(result[self.index_path])['chapters']
        self.assertEqual(first['source_id'], 's-preferred')
        self.assertEqual(first['edition_label'], '合成版名')
        self.assertEqual(first['reading_role'], 'preferred_received_selection')
        self.assertEqual(first['selection_label'], '合成選錄')
        self.assertEqual(second['source_id'], 's-old')
        self.assertEqual(second['reading_role'], 'comparison_transcription')
        self.assertIsNone(second['edition_id'])
        self.assertEqual(second['text_base_status'], 'not_researched')
        self.assertEqual(self.generated, before)
        self.assertIn(self.root / 'data/corpus/reading-witness-preferences.json', result)

    def test_absent_policy_preserves_older_export_bytes(self):
        self.assertIs(enrich_outputs(self.generated, self.root), self.generated)

    def test_missing_actual_edition_cannot_be_presented_as_preferred(self):
        self.provenance['text_bases']['s-preferred']['edition_id'] = None
        self.generated[self.root / 'data/corpus/work-provenance.json'] = encoded(self.provenance)
        with self.assertRaises(ValueError):
            self.run_policy()

    def test_wrong_work_book_chapter_edition_or_reference_rejected(self):
        original = copy.deepcopy(self.policy)
        for key in ['work_id', 'book_id', 'chapter_id', 'edition_id', 'reference_ids']:
            with self.subTest(key=key):
                self.policy = copy.deepcopy(original)
                self.policy['preferences'][0][key] = ['ref-other'] if key == 'reference_ids' else 'wrong'
                with self.assertRaises(ValueError):
                    self.run_policy()

    def test_duplicate_unscoped_or_unexplained_choice_rejected(self):
        original = copy.deepcopy(self.policy)
        self.policy['preferences'] *= 2
        with self.assertRaises(ValueError):
            self.run_policy()
        for key, value in [('scope', 'whole_book'), ('rationale', '')]:
            self.policy = copy.deepcopy(original)
            self.policy['preferences'][0][key] = value
            with self.assertRaises(ValueError):
                self.run_policy()

    def test_bad_types_cannot_be_coerced_into_valid_policy(self):
        original = copy.deepcopy(self.policy)
        self.policy['schema_version'] = True
        with self.assertRaises(ValueError):
            self.run_policy()
        for key, value in [('source_id', []), ('reference_ids', [{}])]:
            self.policy = copy.deepcopy(original)
            self.policy['preferences'][0][key] = value
            with self.assertRaises(ValueError):
                self.run_policy()
