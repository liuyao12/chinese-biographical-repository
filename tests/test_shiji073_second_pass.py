import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class BaiWangEvidenceTests(unittest.TestCase):
    def read(self, suffix, key):
        return json.loads((ROOT / ('corpus/shiji/073-' + suffix + '.json')).read_text())[key]

    def test_already_dead_does_not_become_death_in_ershi_reign(self):
        events = self.read('life-events', 'events')
        for pid in ('gdj_k53_v1x', 'gdj_k53_v1x_A'):
            event = next(e for e in events if e['person_id'] == pid)
            self.assertEqual(event['source_term'], '皆已死')
            self.assertIsNone(event['date_expression'])
            self.assertNotIn('normalized_date', event)
        self.assertFalse(any(e['person_id'] == 'gdj_k53_v1x_*A' for e in events))

    def test_rank_demotion_and_death_keep_separate_boundaries(self):
        titles = {h['id']: h for h in self.read('titles', 'holdings')}
        rank = titles['th-shiji073-005']
        self.assertEqual(rank['effective_period']['end']['event_type'], 'explicit_end')
        self.assertNotIn('normalized_date', rank['effective_period']['end'])
        for key, year in [('th-shiji073-001', 294), ('th-shiji073-002', 293), ('th-shiji073-006', 260)]:
            holding = titles[key]
            self.assertEqual(holding['effective_period']['start']['normalized_date']['era_year'], year)
            self.assertEqual(holding['effective_period']['end']['status'], 'unknown')
        death = next(e for e in self.read('life-events', 'events') if e['person_id'] == rank['person_id'])
        self.assertEqual(death['date_expression'], '秦昭王五十年十一月')
        self.assertEqual(death['normalized_date']['era_year'], 257)
        variants = [r for r in death['normalized_date']['references'] if r['scope'] == 'received_chronological_variant']
        self.assertEqual(len(variants), 1)
        self.assertIn('十二月', variants[0]['quote'])


if __name__ == '__main__':
    unittest.main()
