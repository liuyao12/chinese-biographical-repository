"""作品年代與版本履歷不能混用數位修訂日或他書底本。"""
import copy
import json
from pathlib import Path
import unittest
from scripts.work_provenance import validate, inventory, source_inventory

ROOT = Path(__file__).resolve().parents[1]


class WorkProvenanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / 'registry/work-provenance.json').read_text())

    def test_complete_native_and_legacy_inventory(self):
        validate(self.data, ROOT)
        self.assertEqual(set(self.data['works']), set(inventory(ROOT)))
        self.assertEqual(len(self.data['text_bases']), len(source_inventory(ROOT)))

    def test_wangminzhi_death_not_composition_or_burial(self):
        work = self.data['works']['w-epitaph-wangminzhi']
        self.assertEqual(work['composition']['status'], 'unknown')
        self.assertEqual(work['burial']['status'], 'unknown')
        event = work['excavation']['assertions'][0]
        self.assertEqual(event['date']['start_year'], 1965)
        self.assertEqual(event['date']['day'], 21)
        self.assertEqual(event['place_as_reported'], '南京新民門外象山')
        self.assertEqual(event['event_kind'], 'reported_unearthing')

    def test_songshu_seventy_juan_not_all_hundred(self):
        events = self.data['works']['w-songshu']['composition']['assertions']
        dated = [e for e in events if e.get('date') and e['date']['start_year'] == 488]
        self.assertEqual(len(dated), 1)
        self.assertIn('70', dated[0]['qualification'])
        self.assertEqual(dated[0]['date']['month'], 2)
        self.assertTrue(any(e['event_kind'] == 'treatises_completion' and e['date'] is None for e in events))

    def test_nanshi_submission_not_exact_completion(self):
        events = self.data['works']['w-nanshi']['composition']['assertions']
        event = next(e for e in events if e['event_kind'] == 'submission')
        self.assertEqual(event['date']['start_year'], 659)
        bound = next(e for e in events if e['event_kind'] == 'completion_upper_bound')
        self.assertEqual(bound['not_after_year'], 659)
        self.assertIsNone(bound['date'])

    def test_digital_revision_not_composition(self):
        data = copy.deepcopy(self.data)
        data['works']['w-jinshu']['composition']['assertions'][0]['event_kind'] = 'digital_revision'
        with self.assertRaises(AssertionError):
            validate(data)

    def test_pei_commentary_submission_not_original_history(self):
        events = self.data['works']['w-sanguozhi']['composition']['assertions']
        event = next(e for e in events if e['attribution'] == '裴松之')
        self.assertEqual(event['layer'], 'commentary')
        self.assertEqual(event['event_kind'], 'submission')
        self.assertEqual(event['date']['start_year'], 429)
        self.assertEqual((event['date']['month'], event['date']['day']), (7, 24))
        self.assertTrue(all(e['event_kind'] != 'completion' for e in events if e['attribution'] == '陳壽'))

    def test_tongjian_submission_month_preserves_other_reading(self):
        record = self.data['works']['w-zizhitongjian']['composition']
        self.assertEqual(record['assertions'][0]['date']['month'], 11)
        self.assertEqual(record['alternative_readings'][0]['source_expression'], '元豐七年十二月戊辰')

    def test_unresearched_basis_does_not_claim_edition(self):
        data = copy.deepcopy(self.data)
        next(iter(data['text_bases'].values()))['edition_id'] = 'pretend'
        with self.assertRaises(AssertionError):
            validate(data)

    def test_assertion_without_evidence_rejected(self):
        data = copy.deepcopy(self.data)
        data['works']['w-epitaph-wangminzhi']['excavation']['assertions'][0]['reference_ids'] = []
        with self.assertRaises(AssertionError):
            validate(data)

    def test_unknown_with_assertion_rejected(self):
        data = copy.deepcopy(self.data)
        data['works']['w-epitaph-wangminzhi']['excavation']['status'] = 'unknown'
        with self.assertRaises(AssertionError):
            validate(data)

    def test_calendar_is_explicit(self):
        data = copy.deepcopy(self.data)
        data['works']['w-epitaph-wangminzhi']['excavation']['assertions'][0]['date']['calendar'] = 'unspecified'
        with self.assertRaises(AssertionError):
            validate(data)

    def test_missing_location_field_rejected(self):
        data = copy.deepcopy(self.data)
        del data['works']['w-epitaph-wangminzhi']['excavation']['assertions'][0]['place_as_reported']
        with self.assertRaises(AssertionError):
            validate(data)

    def test_unrelated_work_edition_rejected(self):
        data = copy.deepcopy(self.data)
        ref = 'r-ntu2009-wangminzhi'
        data['editions']['wrong'] = {'id':'wrong', 'work_id':'w-hanshu',
            'extent':'fragment', 'reference_ids':[ref]}
        basis = next(b for b in data['text_bases'].values() if b['work_id'] == 'w-shiji')
        basis.update(status='documented', edition_id='wrong', reference_ids=[ref])
        with self.assertRaises(AssertionError):
            validate(data)


if __name__ == '__main__':
    unittest.main()
