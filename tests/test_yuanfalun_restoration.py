import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class YuanFalunRestorationTests(unittest.TestCase):
    def test_public_bundle_groups_restoration_without_inventing_a_holding(self):
        bundle = json.loads((ROOT / 'exports/persons/2a3_ci1_y4y_A.json').read_text())
        events = bundle['person_events']
        passages = {passage['id']: passage['text'] for passage in bundle['passages']}
        self.assertEqual(len(events), 3)
        self.assertEqual({e['event_type'] for e in events}, {'noble_title_restoration'})
        self.assertEqual(len({e['event_group_id'] for e in events}), 1)
        self.assertEqual({e['evidence'][0]['work_id'] for e in events},
                         {'w-weishu-weishou', 'w-beishi', 'w-cefu-yuangui'})
        for event in events:
            self.assertIsNone(event['date_expression'])
            self.assertIsNone(event['title'])
            self.assertIsNone(event['holding_id'])
            context = event['restoration_context']
            self.assertIsNone(context['petitioning_person_id'])
            self.assertEqual(context['contextual_title'], '廣陽王')
            self.assertEqual(context['predecessor_person_id'], '2a3_ci1_y4y')
            for key in ('case_evidence', 'collateral_case_evidence', 'paternal_title_evidence'):
                evidence = context[key]
                self.assertIn(evidence['quote'], passages[evidence['paragraph_id']])
        self.assertFalse(bundle['title_holdings'])

    def test_all_restoration_records_use_the_validated_event_filename(self):
        paths = list((ROOT / 'corpus').glob('*/*falun-person-events.json'))
        self.assertEqual(len(paths), 3)
        for path in paths:
            records = json.loads(path.read_text())
            self.assertEqual(records['record_type'], 'person_event_assertion_set')
            self.assertEqual(len(records['events']), 1)
            self.assertEqual(records['events'][0]['event_type'], 'noble_title_restoration')
