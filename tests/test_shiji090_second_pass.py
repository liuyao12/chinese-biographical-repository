# coding: utf-8
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class WeiPengIdentityTests(unittest.TestCase):
    def load(self, name):
        return json.loads((ROOT / 'corpus/shiji' / name).read_text())

    def paragraph(self, number, suffix):
        return next(p for p in self.load(number + '.json')['paragraphs']
                    if p['id'].endswith(':' + suffix))

    def test_conflicting_kinship_preserves_shared_relative_order(self):
        rows = self.load('090-assertions.json')['assertions']
        claims = [r for r in rows if r['id'] in {'a-shiji090-001', 'a-shiji090-002'}]
        self.assertEqual({r['predicate'] for r in claims}, {'brother', 'agnatic_cousin'})
        for row in claims:
            q = row['qualifiers']
            self.assertEqual(q['discrepancy_group_id'], 'kin-shiji090-wei')
            order = q['relative_birth_order']
            self.assertEqual(order['older_person_id'], 'kez_re1_kcr')
            self.assertEqual(order['younger_person_id'], '6ve_ik8_jv8')
            self.assertIsNone(order['older_ordinal'])
            self.assertIsNone(order['younger_ordinal'])
        cousin = next(r for r in claims if r['predicate'] == 'agnatic_cousin')
        self.assertIsNone(cousin['qualifiers']['kinship_structure']['distance'])
        self.assertIsNone(cousin['qualifiers']['kinship_structure']['common_ancestor_person_id'])

    def test_chenxi_identity_preserves_year_difference_and_fabricated_report(self):
        for number, suffix, wording in [('090', 'p011', '十年秋'),
                                       ('093', 'p010', '漢十一年秋'),
                                       ('092', 'p025', '詐令人從上所來，言豨已得死')]:
            p = self.paragraph(number, suffix)
            self.assertIn(wording, p['text'])
            self.assertTrue(any(m['surface'] == '陳豨' and m['person_id'] == '1xx_s1v_svn'
                                for m in p['mentions']))

    def test_title_reference_resolves_person_without_rewriting_received_text(self):
        p = self.paragraph('090', 'p009')
        self.assertTrue(any(m['surface'] == '留侯' and m['person_id'] == 'ea5_zvr_hlp'
                            for m in p['mentions']))
        self.assertIn('碧陵', p['text'])
        self.assertIn('留侯張良者', self.paragraph('055', 'p001')['text'])
        for number, suffix, surface in [('090', 'p011', '王恬開'),
                                        ('102', 'p007', '山都侯王恬開')]:
            p = self.paragraph(number, suffix)
            self.assertTrue(any(m['surface'] == surface and m['person_id'] == 'ylb_xg7_6t9'
                                for m in p['mentions']))
        decision = next(d for d in self.load('090-equivalences.json')['decisions']
                        if d['id'] == 'eq-shiji090-review-wangtiankai')
        self.assertEqual(decision['status'], 'contextual_provisional')
        self.assertFalse(decision['human_reviewed'])

    def test_death_date_does_not_use_start_of_peng_case(self):
        events = self.load('090-life-events.json')['events']
        self.assertEqual(len(events), 4)
        self.assertFalse(any(e['person_id'] in {'9ta_gen_pky', 'ujq_cg1_bc8'} for e in events))
        bao = next(e for e in events if e['person_id'] == '6ve_ik8_jv8')
        self.assertEqual(bao['source_term'], '周苛遂殺魏豹')
        peng = next(e for e in events if e['person_id'] == '9qt_orl_5f2')
        self.assertIsNone(peng['date_expression'])
        self.assertEqual(peng['normalized_date']['era_year'], 196)
        basis = peng['normalized_date']['basis']
        self.assertEqual(basis['kind'], 'parallel_event')
        self.assertIn('夏，梁王彭越', basis['reference_event_quote'])
        self.assertTrue(any('十一年' in r['quote'] for r in peng['normalized_date']['references']))
        self.assertIn('十年秋', peng['evidence'][0]['quote'])

    def test_requested_origin_is_not_an_extra_residence(self):
        rows = self.load('090-addresses.json')['assertions']
        self.assertEqual({(a['relation'], a['place']['source_name']) for a in rows},
                         {('biographical_origin', '昌邑'), ('residence', '鉅野中'), ('residence', '河上')})
        self.assertTrue(all(a['place']['modern_identification'] is None for a in rows))

    def test_grant_years_preserve_original_season_and_unknown_end(self):
        rows = self.load('090-titles.json')['holdings']
        for hid, year, expression in [('th-shiji090-004', 206, '漢元年'),
                                      ('th-shiji090-008', 206, '漢元年秋'),
                                      ('th-shiji090-009', 205, '漢王二年春'),
                                      ('th-shiji090-012', 202, '（五年）')]:
            h = next(h for h in rows if h['id'] == hid)
            start = h['effective_period']['start']
            self.assertEqual(start['date_expression'], expression)
            self.assertEqual(start['normalized_date']['era_year'], year)
            self.assertNotIn('month', start['normalized_date'])
            end = h['effective_period']['end']
            self.assertIsNone(end['date_expression'])
            self.assertNotIn('normalized_date', end)
            if hid == 'th-shiji090-012':
                self.assertEqual(end['event_type'], 'deposition')
                self.assertIn('上赦以為庶人', end['evidence'][0]['quote'])
            else:
                self.assertEqual(end['status'], 'unknown')
