import copy
import json
import unittest
from pathlib import Path
from scripts.fixed_zhou041_wangbao import proof, guard_bundle
from scripts.zhou041_wangbao_noble_ranks import source_record
from scripts.received_career_roles import holding_valid
from scripts.person_bundle import load_catalog, bundle

ROOT = Path(__file__).resolve().parents[1]

class WangBaoNobleRanks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter, _, cls.roles = proof(ROOT)
        cls.people, cls.records = load_catalog(ROOT)
        cls.title_set = source_record(ROOT, cls.chapter, cls.roles)

    def test_two_received_modes_and_source_scoped_numeric_date(self):
        holds = self.title_set['holdings']
        self.assertEqual([(h['title'], h['mode']) for h in holds], [('南昌縣侯', 'accession'), ('石泉縣子', 'grant')])
        self.assertEqual(holds[1]['effective_period']['start']['date_expression'], '孝閔帝踐阼')
        for h in holds:
            self.assertTrue(holding_valid(h, self.chapter, ROOT))
            if h['mode'] == 'accession':
                self.assertNotIn('normalized_date', h['effective_period']['start'])
            else:
                date = h['effective_period']['start']['normalized_date']
                self.assertEqual((date['year'], date['precision'], date['calendar']), (557, 'year', 'chinese_civil'))
            self.assertEqual(h['effective_period']['end']['status'], 'unknown')
        self.assertIn('邑三百戶', holds[1]['evidence'][0]['quote'])
        self.assertNotIn('fief_household_count', holds[1])

    def test_nearby_ruler_is_not_recipient(self):
        h = copy.deepcopy(self.title_set['holdings'][1])
        h['person_id'] = self.roles['$xiaomin']
        self.assertFalse(holding_valid(h, self.chapter, ROOT))
        h['source_career_role']['recipient_mention_id'] = h['source_career_role']['ruler_mention_id']
        self.assertFalse(holding_valid(h, self.chapter, ROOT))

    def test_modes_cannot_be_coherently_swapped(self):
        for h in self.title_set['holdings']:
            wrong = copy.deepcopy(h)
            wrong['mode'] = 'grant' if h['mode'] == 'accession' else 'accession'
            wrong['effective_period']['start']['event_type'] = wrong['mode']
            self.assertFalse(holding_valid(wrong, self.chapter, ROOT))

    def test_numeric_year_death_end_and_child_grant_are_not_created(self):
        h = self.title_set['holdings'][1]
        for mutate in [lambda x: x['effective_period']['start'].update(normalized_date={'year':557}),
                       lambda x: x['effective_period'].update(end={'status':'source_event','event_type':'death','date_expression':None,'normalized_date':{'year':576}}),
                       lambda x: x.update(person_id=self.roles['$zi'])]:
            wrong = copy.deepcopy(h)
            mutate(wrong)
            self.assertFalse(holding_valid(wrong, self.chapter, ROOT))

    def test_received_title_not_replaced_by_other_source_variant(self):
        wrong = copy.deepcopy(self.title_set['holdings'][0])
        wrong['title'] = '南昌侯'
        self.assertFalse(holding_valid(wrong, self.chapter, ROOT))
        old = [h for r in self.records if r.get('record_type') == 'title_holding_assertion_set' for h in r['holdings'] if h['id'] == 'th-liang041-bao-nanchang']
        self.assertEqual(len(old), 1)
        self.assertEqual(old[0]['title'], '南昌侯')

    def test_caller_cannot_hide_noble_set(self):
        records = [r for r in self.records if r != self.title_set]
        with self.assertRaises(AssertionError):
            guard_bundle(ROOT, self.roles['$bao'], self.people, records)

    def test_actual_api_preserves_heading_and_basic_layer(self):
        b = bundle(self.roles['$bao'], ROOT, catalog=(self.people, self.records))
        ids = {h['id'] for h in b['title_holdings']}
        self.assertTrue({'th-liang041-bao-nanchang','th-zhou041-wangbao-nanchang','th-zhou041-wangbao-shiquan'} <= ids)
        self.assertEqual(b['default_profile_title']['title'], '南昌侯')
        self.assertEqual(b['age_assertions'][0]['value'], 64)
        self.assertEqual(b['preferred_name_component_readings'][0]['preferred_value'], '褒')

    def test_557_normalizer_uses_actual_official_row_and_recipient(self):
        from scripts.validate_corpus import normalized_date_errors
        h = self.title_set['holdings'][1]
        date = h['effective_period']['start']['normalized_date']
        self.assertEqual(normalized_date_errors(date, {self.chapter['id']: self.chapter}, ROOT, h, 'start'), [])
        self.assertIn('557 557', date['references'][0]['quote'])
        self.assertNotEqual(h['person_id'], self.roles['$xiaomin'])
        for key, value in [('year', 558), ('calendar', 'gregorian'), ('precision', 'month'), ('human_reviewed', True)]:
            wrong = copy.deepcopy(date)
            wrong[key] = value
            self.assertTrue(normalized_date_errors(wrong, {self.chapter['id']: self.chapter}, ROOT, h, 'start'))

    def test_557_does_not_date_inheritance_or_death(self):
        from scripts.zhou041_wangbao_noble_ranks import date_valid
        h = self.title_set['holdings'][1]
        date = h['effective_period']['start']['normalized_date']
        self.assertFalse(date_valid(date, self.title_set['holdings'][0], 'start', {self.chapter['id']: self.chapter}, ROOT))
        self.assertFalse(date_valid(date, h, 'life_event', {self.chapter['id']: self.chapter}, ROOT))
        self.assertFalse(date_valid(date, h, 'end', {self.chapter['id']: self.chapter}, ROOT))

    def test_changed_official_row_and_missing_source_reading_cannot_pass(self):
        from scripts.zhou041_wangbao_noble_ranks import source_record
        import tests.test_zhou041_wangbao_profile_facts as helpers
        rel = 'source-evidence/zhou041-wangbao-ws2432538/xiaomin557-observed-official-row.json'
        row = json.loads((ROOT / rel).read_text())
        row['reference']['accession_year'] = 558
        with helpers.WangBaoProfileFacts.overlay(self, {rel: row}), self.assertRaises(AssertionError):
            source_record(ROOT, self.chapter, self.roles)

if __name__ == '__main__':
    unittest.main()
