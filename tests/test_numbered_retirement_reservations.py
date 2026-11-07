"""Synthetic reservation contracts and coverage of the repository's real receipts."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts.person_ids import allocate_person_id
from scripts.retired_person_ids import retired_person_ids

ROOT = Path(__file__).resolve().parents[1]


class NumberedRetirementReservations(unittest.TestCase):
    def fixture(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        records = {
            'registry/persons.json': {'persons': [{'id': 'new_abc_123'}]},
            'corpus/synthetic/001-identities.json': {
                'record_type': 'person_identity_decision_set',
                'decisions': [{
                    'id': 'd-synthetic-reservation',
                    'person_id': 'new_abc_123',
                    'scope': 'cross_chapter',
                    'status': 'contextual_provisional',
                    'evidence': [{'quote': 'Synthetic fixture, not historical evidence.'}],
                    'rationale': 'Synthetic identity binding for the reservation contract.',
                }],
            },
            'source-evidence/synthetic/retirement-01.json': {
                'record_type': 'editorial_annotation_rekey_receipt',
                'identity_decision_id': 'd-synthetic-reservation',
                'retired_person_ids': ['abc_def_123'],
                'retirement_policy': 'audit_only_not_canonical_not_alias_not_reusable',
                'person_aliases_created': False,
            },
        }
        for relative, record in records.items():
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(record))
        return root

    def test_numbered_identity_receipt_reserves_id(self):
        self.assertEqual(retired_person_ids(self.fixture()), {'abc_def_123'})

    def test_allocator_retries_numbered_retired_root(self):
        root = self.fixture()
        with patch('scripts.person_ids.secrets.choice', side_effect=list('abcdef123xyzabc789')):
            self.assertEqual(allocate_person_id([], root=root), 'xyz_abc_789')

    def test_numbered_receipt_cannot_relax_identity_validation(self):
        for change in ({'scope': 'chapter'}, {'status': 'rejected'},
                       {'person_id': 'abs_ent_123'}, {'evidence': []}, {'rationale': ''}):
            with self.subTest(change=change):
                root = self.fixture()
                path = root / 'corpus/synthetic/001-identities.json'
                data = json.loads(path.read_text())
                data['decisions'][0].update(change)
                path.write_text(json.dumps(data))
                with self.assertRaises(ValueError):
                    retired_person_ids(root)

    def test_changed_decision_is_read_on_next_call(self):
        root = self.fixture()
        self.assertEqual(retired_person_ids(root), {'abc_def_123'})
        path = root / 'corpus/synthetic/001-identities.json'
        data = json.loads(path.read_text())
        data['decisions'][0]['person_id'] = 'abs_ent_123'
        path.write_text(json.dumps(data))
        with self.assertRaises(ValueError):
            retired_person_ids(root)

    def test_new_receipt_is_read_on_next_call(self):
        root = self.fixture()
        self.assertEqual(retired_person_ids(root), {'abc_def_123'})
        folder = root / 'source-evidence/synthetic'
        receipt = copy.deepcopy(json.loads((folder / 'retirement-01.json').read_text()))
        receipt['retired_person_ids'] = ['old_def_456']
        (folder / 'retirement-stage2-02.json').write_text(json.dumps(receipt))
        self.assertEqual(retired_person_ids(root), {'abc_def_123', 'old_def_456'})

    def test_every_real_receipt_is_discovered(self):
        root = ROOT
        expected = set()
        numbered = set()
        for path in (root / 'source-evidence').rglob('*.json'):
            data = json.loads(path.read_text())
            if not isinstance(data, dict) or data.get('record_type') not in (
                    'editorial_annotation_rekey_receipt', 'source_non_person_retirement_receipt'):
                continue
            ids = set(data.get('retired_person_ids', data.get('historical_rekey_mapping', {})))
            expected.update(ids)
            if path.name.startswith('retirement-'):
                numbered.update(ids)
        self.assertTrue(numbered)
        self.assertEqual(retired_person_ids(root), expected)
        current = {p['id'] for p in json.loads((root / 'registry/persons.json').read_text())['persons']}
        self.assertFalse(current.intersection(expected))

    def test_nonperson_receipt_cannot_spoof_an_unknown_owner(self):
        root = self.fixture()
        receipt = {
            'record_type': 'source_non_person_retirement_receipt',
            'non_person_review_id': 'nr-synthetic-not-a-real-source',
            'review_path': 'source-evidence/synthetic/review.json',
            'review_sha256': '0' * 64,
            'retired_person_ids': ['old_def_456'],
            'retirement_policy': 'audit_only_not_person_not_alias_not_reusable',
            'person_aliases_created': False,
        }
        (root / 'source-evidence/synthetic/retirement-nonperson.json').write_text(json.dumps(receipt))
        with self.assertRaisesRegex(ValueError, 'Unknown non-person reservation owner'):
            retired_person_ids(root)
