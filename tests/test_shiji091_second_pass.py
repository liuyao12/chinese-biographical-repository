# coding: utf-8
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class QingbuIdentityTests(unittest.TestCase):
    def chapter(self, number):
        return json.loads((ROOT / f'corpus/shiji/{number}.json').read_text())

    def paragraph(self, number, suffix):
        return next(p for p in self.chapter(number)['paragraphs']
                    if p['id'].endswith(':' + suffix))

    def test_fan_variant_matches_office_configuration_without_rewriting(self):
        a = self.paragraph('091', 'p003')
        b = self.paragraph('007', 'p011')
        for p, surface in [(a, '范曾'), (b, '范增')]:
            self.assertTrue(any(m['surface'] == surface and m['person_id'] == 'uw6_a0a_tjp'
                                for m in p['mentions']))
        self.assertIn('范曾為末將', a['text'])
        self.assertIn('范增為末將', b['text'])

    def test_opening_army_configurations_resolve_separate_people(self):
        for suffix, surface, pid in [('p002', '陳嬰', '6us_ibm_u05'),
                                     ('p003', '項梁', '5xt_rg8_7zs_A'),
                                     ('p003', '景駒', 'nw9_lle_9jg'),
                                     ('p003', '秦嘉', '0j3_2uz_7wo'),
                                     ('p003', '宋義', 'uj9_x5q_yir'),
                                     ('p003', '章邯', '4jv_qte_5p4')]:
            p = self.paragraph('091', suffix)
            self.assertTrue(any(m['surface'] == surface and m['person_id'] == pid
                                for m in p['mentions']))

    def test_anonymous_wives_and_changsha_rulers_remain_distinct(self):
        d = self.chapter('091')
        ids = lambda surface: {m['person_id'] for p in d['paragraphs'] for m in p['mentions']
                               if m['surface'] == surface and m['person_id']}
        self.assertEqual(ids('番君'), {'o0l_em5_5v9'})
        self.assertEqual(ids('長沙哀王'), {'3lw_vex_s0b'})
        self.assertNotEqual(ids('其女'), ids('愛姬'))
        self.assertIn('六年，布與劉賈入九江', self.paragraph('091', 'p010')['text'])

    def test_han_court_names_resolve_in_their_own_events(self):
        for suffix, surface, pid in [('p002', '陳勝', 'pom_ycp_ha5'),
                                     ('p013', '高后', 'i30_mjq_6q8_A'),
                                     ('p013', '淮陰侯', 'ofc_8ei_jb7'),
                                     ('p013', '梁王彭越', '9qt_orl_5f2'),
                                     ('p014', '蕭相國', 'xd8_uww_5ok')]:
            p = self.paragraph('091', suffix)
            self.assertTrue(any(m['surface'] == surface and m['person_id'] == pid
                                for m in p['mentions']))
        self.assertTrue(any(m['surface'] == '蕭相國何' and m['person_id'] == 'xd8_uww_5ok'
                            for m in self.paragraph('053', 'p001')['mentions']))

    def test_common_identity_does_not_unify_narrative_years(self):
        self.assertIn('十一年，高后誅淮陰侯', self.paragraph('091', 'p013')['text'])
        self.assertIn('夏，漢誅梁王彭越', self.paragraph('091', 'p013')['text'])
        self.assertIn('十年秋，陳豨反代地', self.paragraph('090', 'p011')['text'])
        self.assertIn('漢十二年秋，黥布反', self.paragraph('053', 'p011')['text'])

    def test_death_events_do_not_turn_suicide_intent_into_death(self):
        data = json.loads((ROOT / 'corpus/shiji/091-life-events.json').read_text())['events']
        bu = next(e for e in data if e['person_id'] == 'zxd_afr_2xg')
        self.assertIn('欲自殺', self.paragraph('091', 'p009')['text'])
        self.assertEqual(bu['source_term'], '番陽人殺布茲鄉民田舍')
        self.assertIsNone(bu['date_expression'])
        self.assertNotIn('normalized_date', bu)
        yi = next(e for e in data if e['person_id'] == 'c2w_s7g_en0_*A')
        self.assertEqual(yi['date_expression'], '其八月')
        self.assertEqual(yi['normalized_date']['era_year'], 206)
        xin = next(e for e in data if e['person_id'] == 'ofc_8ei_jb7')
        self.assertEqual(xin['normalized_date']['era_year'], 196)
        self.assertIn('春，淮陰侯韓信', xin['normalized_date']['basis']['reference_event_quote'])

    def test_native_place_migration_and_death_places_are_separate(self):
        data = json.loads((ROOT / 'corpus/shiji/091-addresses.json').read_text())['assertions']
        bu = {(a['relation'], a['place']['source_name']) for a in data if a['person_id'] == 'zxd_afr_2xg'}
        self.assertEqual(bu, {('biographical_origin', '六'), ('migration_destination', '麗山'),
                              ('migration_destination', '江中'), ('death_place', '茲鄉民田舍')})
        self.assertFalse(any(a['relation'] in {'birth_place', 'burial_place'} for a in data))
        self.assertTrue(all(a['place']['modern_identification'] is None for a in data))
        titles = json.loads((ROOT / 'corpus/shiji/091-titles.json').read_text())['holdings']
        start = next(h for h in titles if h['id'] == 'th-shiji091-012')['effective_period']['start']
        self.assertEqual(start['date_expression'], '四年七月')
        self.assertEqual(start['normalized_date']['era_year'], 203)
        self.assertNotIn('month', start['normalized_date'])

    def test_qing_is_not_used_as_surname(self):
        rows = json.loads((ROOT / 'data/corpus/profile-names.json').read_text())['records']
        bu = next(r for r in rows if r['person_id'] == 'zxd_afr_2xg')
        self.assertEqual((bu['surname'], bu['ming']), ('英', '布'))
        self.assertIn('姓英氏', bu['quote'])
        self.assertIn('黥布', bu['additional_names'])
        self.assertIn('英布', self.paragraph('091', 'p002')['text'])
