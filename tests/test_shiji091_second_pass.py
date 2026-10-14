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
