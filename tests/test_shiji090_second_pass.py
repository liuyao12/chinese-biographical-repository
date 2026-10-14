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
            self.assertEqual(order['older_person_id'], 'okz_ham_pdc')
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
