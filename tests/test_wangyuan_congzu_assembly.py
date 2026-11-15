# -*- coding: utf-8 -*-
import copy
import json
import unittest
from pathlib import Path
from scripts.family_assemblies import load_assemblies
from scripts.person_bundle import load_catalog, ROOT
from scripts.wangyuan_congzu_assembly import valid

class WangyuanCongzuAssemblyTests(unittest.TestCase):
    def setUp(self):
        self.catalog = load_catalog(ROOT)
        self.source, self.rows = load_assemblies(ROOT, self.catalog)
        self.yuan = self.source['7r6_k52_qji_ABAAAA*A']
        self.member = next(m for a in json.loads((ROOT/'registry/family-assemblies.json').read_text())['assemblies']
                           for m in a['members'] if m['person_id'] == self.yuan['person_id'])
        self.assertions = {a['id']: a for r in self.catalog[1] if r.get('record_type') == 'person_assertion_set' for a in r['assertions']}

    def test_shared_ancestor_connection_uses_three_attested_steps_and_one_wildcard(self):
        self.assertTrue(valid(self.member, {m['person_id']: m for a in json.loads((ROOT/'registry/family-assemblies.json').read_text())['assemblies'] for m in a['members']}, self.assertions))
        self.assertEqual(self.member['ancestor_person_id'], '7r6_k52_qji_ABAAAA')
        self.assertEqual(self.member['generation_distance'], 2)
        self.assertEqual(self.member['intermediate_person_ids'], [None])
        self.assertEqual(self.member['person_id'].count('*'), 1)
        self.assertEqual(self.rows['7r6_k52_qji_ABAAAA*AA']['parent_person_id'], self.member['person_id'])
        self.assertNotIn('a-wangyuan-to-wangxun', self.assertions)

    def test_route_and_wildcard_mutations_are_rejected(self):
        fullrows = {m['person_id']: m for a in json.loads((ROOT/'registry/family-assemblies.json').read_text())['assemblies'] for m in a['members']}
        for mutation in ('wrong_route', 'wrong_depth', 'extra_wildcard', 'invent_direct_assertion',
                         'wrong_songshu_clause', 'false_anchor'):
            with self.subTest(mutation=mutation):
                m = copy.deepcopy(self.member); rows = copy.deepcopy(fullrows); assertions = copy.deepcopy(self.assertions)
                if mutation == 'wrong_route': m['ancestor_connection']['references'][2]['assertion_id'] = 'a-jinshu065-wang-013'
                elif mutation == 'wrong_depth': m['ancestor_connection']['common_ancestor_depth'] = 2
                elif mutation == 'extra_wildcard': m['person_id'] = '7r6_k52_qji_ABAAAA**A'
                elif mutation == 'invent_direct_assertion': assertions['a-nanqishu046-sengyou-father']['object_person_id'] = '7r6_k52_qji_ABAAAA'
                elif mutation == 'wrong_songshu_clause':
                    ref = next(r for r in m['ancestor_connection']['references'] if r['assertion_id'] == 'a-songshu063-phase5-027')
                    ref['paragraph_id'] = 'c-songshu-063-wanghua-tanshou:line037'
                else:
                    ref = next(r for r in m['ancestor_connection']['references'] if r['assertion_id'] == 'a-songshu063-phase5-027')
                    ref['source_term_anchor']['start'] = 12
                self.assertFalse(valid(m, rows, assertions))

    def test_retired_ids_are_absent_from_open_data(self):
        for old in ('p93_tgr_t8r', 'p93_tgr_t8r_A'):
            for path in (ROOT/'registry/persons.json', ROOT/'registry/family-assemblies.json',
                         ROOT/'corpus/nanqishu/046.json', ROOT/'corpus/nanqishu/046.xml',
                         ROOT/'corpus/nanqishu/046-assertions.json', ROOT/'data/corpus/persons.json',
                         ROOT/'data/corpus/person-directory.json', ROOT/'exports/persons/index.json'):
                self.assertNotIn(old, path.read_text())

if __name__ == '__main__':
    unittest.main()
