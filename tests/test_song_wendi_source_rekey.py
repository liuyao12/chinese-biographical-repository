import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / 'source-evidence' / 'song-wendi-identity'


class SongWendiSourceRekey(unittest.TestCase):
    def test_emperor_keeps_source_occurrences_and_existing_child(self):
        report = json.loads((EVIDENCE / 'migration-audit.json').read_text())
        receipt = json.loads((ROOT / report['retirement_receipt']).read_text())
        people = {p['id']: p for p in json.loads((ROOT / 'registry/persons.json').read_text())['persons']}
        kept = people[report['canonical_person_id']]
        self.assertIn(report['preserved_issued_child'], people)
        for old in receipt['retired_person_ids']:
            self.assertNotIn(old, people)
            self.assertNotIn(old, kept.get('id_aliases', []))
        sources = json.loads((EVIDENCE / 'review.json').read_text())
        recorded = {row['mention_id'] for row in kept['evidence']}
        self.assertTrue({row['original_mid'] for row in sources['occurrences']} <= recorded)

    def test_fixed_historical_captures_remain_verifiable(self):
        audit = json.loads((EVIDENCE / 'migration-audit.json').read_text())
        for record in audit['historical_captures']:
            path = ROOT / record['path']
            with self.subTest(path=path):
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), record['sha256'])
