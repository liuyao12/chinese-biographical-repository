# coding: utf-8
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class FanCaiLifeReviewTests(unittest.TestCase):
    def load(self, suffix):
        return json.loads((ROOT / f'corpus/shiji/079-{suffix}.json').read_text())

    def test_prediction_feigned_death_and_last_service_are_not_deaths(self):
        events = self.load('life-events')['events']
        self.assertTrue(events)
        self.assertFalse({'zus_do8_z1q', 'shd_1wc_uva'} & {e['person_id'] for e in events})
        for event in events:
            self.assertNotIn('詳死', event['source_term'])
            self.assertNotIn('卒事', event['source_term'])
            self.assertNotIn('四十三', event['source_term'])

    def test_origin_residence_and_execution_office_are_distinct(self):
        addresses = self.load('addresses')['assertions']
        self.assertEqual([(a['relation'], a['place']['source_name']) for a in addresses
                          if a['person_id'] == 'shd_1wc_uva'],
                         [('biographical_origin', '燕'), ('residence', '秦')])
        self.assertFalse(any(a['person_id'] == 'rmu_iss_4in' for a in addresses))
        self.assertFalse(any(a['relation'] == 'burial_place' for a in addresses))
        self.assertTrue(all(a['place']['modern_identification'] is None for a in addresses))
        residence = next(a for a in addresses if a['relation'] == 'residence')
        self.assertNotIn('reported_duration', residence)
        self.assertEqual(residence['source_term'], '居秦十餘年')

    def test_wangji_uses_same_event_not_relative_year_arithmetic(self):
        event = next(e for e in self.load('life-events')['events'] if e['person_id'] == 'rmu_iss_4in')
        self.assertEqual(event['date_expression'], '後二歲')
        date = event['normalized_date']
        self.assertEqual((date['era_year'], date['year']), (255, -254))
        self.assertEqual(date['basis']['kind'], 'parallel_event')
        self.assertIn('王稽棄市', date['basis']['reference_event_quote'])
        self.assertTrue(all(r['image_verified'] is False for r in date['references']))

    def test_grant_start_does_not_supply_unattested_end(self):
        holding = next(h for h in self.load('titles')['holdings'] if h['id'] == 'th-shiji079-014')
        self.assertEqual(holding['effective_period']['start']['normalized_date']['era_year'], 266)
        self.assertEqual(holding['effective_period']['end']['status'], 'unknown')
        self.assertNotIn('normalized_date', holding['effective_period']['end'])
