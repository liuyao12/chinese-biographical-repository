import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class RanghouSourceTests(unittest.TestCase):
    def read(self, suffix, key):
        path = ROOT / ('corpus/shiji/072-' + suffix + '.json')
        return json.loads(path.read_text(encoding='utf-8'))[key]

    def test_repeated_offices_do_not_absorb_unappointed_gap(self):
        titles = {h['id']: h for h in self.read('titles', 'holdings')}
        six = titles['th-shiji072-015']
        four = titles['th-shiji072-016']
        self.assertEqual(six['reported_duration']['value'], 6)
        self.assertEqual(four['reported_duration']['value'], 4)
        self.assertEqual(six['effective_period']['end']['event_type'], 'explicit_end')
        self.assertEqual(four['effective_period']['end']['status'], 'unknown')
        self.assertEqual(four['effective_period']['start']['normalized_date']['era_year'], 281)
        self.assertEqual(titles['th-shiji072-013']['reported_duration']['value'], 4)
        self.assertFalse(any(h.get('reported_duration', {}).get('value') == 2
                             for h in titles.values()))
        emperor = titles['th-shiji072-023']
        self.assertEqual(emperor['title'], '西帝')
        self.assertEqual(emperor['effective_period']['start']['date_expression'], '昭王十九年')
        self.assertEqual(emperor['effective_period']['end']['event_type'], 'explicit_end')
        self.assertNotIn('reported_duration', emperor)
        self.assertNotIn('normalized_date', emperor['effective_period']['end'])

    def test_ancestral_origin_and_burial_do_not_invent_birth_or_year(self):
        addresses = self.read('addresses', 'assertions')
        origin = next(a for a in addresses if a['relation'] == 'ancestral_origin')
        self.assertEqual(origin['place']['source_name'], '楚')
        self.assertIsNone(origin['qualifiers']['ancestor_person_id'])
        self.assertFalse(any(a['relation'] == 'birth_place' for a in addresses))
        death = next(e for e in self.read('life-events', 'events')
                     if e['person_id'] == origin['person_id'])
        self.assertIsNone(death['date_expression'])
        self.assertNotIn('normalized_date', death)
        burial = self.read('person-events', 'events')[0]
        self.assertEqual(burial['person_id'], death['person_id'])
        self.assertIsNone(burial['date_expression'])

    def test_chapter_heading_year_does_not_spread_to_later_events(self):
        titles = {h['id']: h for h in self.read('titles', 'holdings')}
        appointment = titles['th-shiji072-009']['effective_period']
        self.assertEqual(appointment['start']['normalized_date']['era_year'], 295)
        self.assertEqual(appointment['end']['normalized_date']['era_year'], 292)
        death = next(e for e in self.read('life-events', 'events')
                     if e['person_id'] == 'r9n_0vc_ywa')
        self.assertEqual(death['normalized_date']['era_year'], 300)
        table = json.loads((ROOT / 'data/historical-tables/shiji-015.json').read_text())
        cells = {c['id']: c for f in table['fragments'] for r in f['rows'] for c in r['cells']}
        dates = [death['normalized_date']]
        dates += [b['normalized_date'] for h in titles.values()
                  for b in h['effective_period'].values() if 'normalized_date' in b]
        self.assertEqual(len(dates), 6)
        for date in dates:
            self.assertEqual(date['status'], 'editorial_provisional')
            for ref in date['references']:
                self.assertEqual(ref['quote'], cells[ref['table_cell_id']]['text'])


if __name__ == '__main__':
    unittest.main()
