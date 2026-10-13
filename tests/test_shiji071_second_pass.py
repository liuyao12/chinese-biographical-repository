import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class Shiji071EvidenceTests(unittest.TestCase):
    def read(self, name):
        return json.loads((ROOT / name).read_text(encoding='utf-8'))

    def test_dates_preserve_exact_parallel_cells_and_year_layer(self):
        table = self.read('data/historical-tables/shiji-015.json')
        cells = {c['id']: c for f in table['fragments']
                 for r in f['rows'] for c in r['cells']}
        events = self.read('corpus/shiji/071-life-events.json')['events']
        holdings = self.read('corpus/shiji/071-titles.json')['holdings']
        dates = [e['normalized_date'] for e in events if 'normalized_date' in e]
        dates += [h['effective_period']['start']['normalized_date']
                  for h in holdings
                  if 'normalized_date' in h['effective_period']['start']]
        self.assertEqual(sorted(d['era_year'] for d in dates), [300, 309, 309, 313])
        for date in dates:
            self.assertEqual(date['status'], 'editorial_provisional')
            self.assertEqual(date['year'], 1 - date['era_year'])
            for reference in date['references']:
                cell = cells[reference['table_cell_id']]
                self.assertEqual(reference['quote'], cell['text'])
                self.assertEqual(cell['column'] == 0,
                                 reference['scope'] == 'digital_editorial_regnal_year_equivalence_only')
                self.assertFalse(reference['image_verified'])

    def test_death_does_not_date_burial_or_all_title_ends(self):
        events = self.read('corpus/shiji/071-person-events.json')['events']
        burial = next(e for e in events if e['event_type'] == 'burial')
        self.assertIsNone(burial['date_expression'])
        self.assertNotIn('normalized_date', burial)
        holdings = self.read('corpus/shiji/071-titles.json')['holdings']
        for holding in holdings:
            if holding['person_id'] == burial['person_id']:
                self.assertNotIn('normalized_date', holding['effective_period']['end'])

    def test_granted_title_and_diplomatic_duration_remain_separate(self):
        holdings = self.read('corpus/shiji/071-titles.json')['holdings']
        grants = [h for h in holdings if h['person_id'] == '8im_m5e_cpy'
                  and h['title'] == '上卿']
        self.assertEqual(len(grants), 2)
        by_polity = {h['granting_polity']['source_name']: h for h in grants}
        self.assertEqual(set(by_polity), {'秦', '齊'})
        self.assertEqual(by_polity['秦']['service_realization']['status'], 'not_taken_up')
        self.assertNotIn('service_realization', by_polity['齊'])
        event = next(e for e in self.read('corpus/shiji/071-person-events.json')['events']
                     if e['event_type'] == 'diplomatic_service')
        self.assertEqual(event['reported_duration']['unit'], 'service_year')
        self.assertEqual(event['reported_duration']['value'], 3)
        self.assertIsNone(event['date_expression'])
        for holding in holdings:
            if holding['person_id'] == event['person_id']:
                self.assertNotIn('reported_duration', holding)

    def test_geographical_designation_does_not_become_native_place(self):
        addresses = self.read('corpus/shiji/071-addresses.json')['assertions']
        designation = next(a for a in addresses if a['relation'] == 'source_locality_designation')
        self.assertIsNone(designation['qualifiers']['origin_or_residence'])
        service = next(a for a in addresses if a['relation'] == 'service_location')
        self.assertEqual(service['person_id'], designation['person_id'])
        self.assertEqual(service['qualifiers']['source_position'], '監門')
        self.assertFalse(any(a['relation'] in ('birth_place', 'native_place', 'biographical_origin')
                             for a in addresses if a['person_id'] == service['person_id']))


if __name__ == '__main__':
    unittest.main()
