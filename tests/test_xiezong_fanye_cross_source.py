"""Cross-source identity choices preserve literal evidence and uncertainty."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class XieZongFanYeCrossSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        def load(path):
            return json.loads((ROOT / path).read_text())
        cls.qi = load('corpus/nanqishu/033-wangsengqian.json')
        cls.song = load('corpus/songshu/052-xiejingren.json')
        cls.qp = next(p for p in cls.qi['paragraphs'] if p['id'].endswith(':p014'))
        cls.sp = next(p for p in cls.song['paragraphs'] if p['id'].endswith(':p019'))
        cls.marks = {m['id']: m for c in (cls.qi, cls.song)
                     for p in c['paragraphs'] for m in p['mentions']}
        cls.people = {p['id']: p for p in load('registry/persons.json')['persons']}
        cls.decisions = {d['id']: d for d in load('corpus/nanqishu/033-wangsengqian-identities.json')['decisions']}
        cls.zong = cls.marks[cls.sp['id'] + ':m0005']['person_id']
        cls.fan = cls.marks[cls.sp['id'] + ':m0020']['person_id']

    def test_names_and_calligraphy_bridge_preserve_both_sources(self):
        self.assertIn('謝綜書其舅云', self.qp['text'])
        self.assertIn('綜有才藝善𨽻書', self.sp['text'])
        self.assertIn('與舅范曄謀反', self.sp['text'])
        self.assertIn('范曅與蕭思話', self.qp['text'])
        for suffix, pid in [('m0365', self.zong), ('m0368', self.zong), ('m0369', self.fan)]:
            mark = self.marks[self.qp['id'] + ':' + suffix]
            self.assertEqual(mark['person_id'], pid)
            self.assertEqual(self.qp['text'][mark['start']:mark['end']], mark['surface'])

    def test_reverse_mentions_preserve_literal_uncle_not_an_inserted_name(self):
        mark = self.marks[self.qp['id'] + ':m0369']
        self.assertEqual(mark['surface'], '舅')
        for mid in [self.qp['id'] + ':m0365', self.qp['id'] + ':m0368', mark['id']]:
            mention = self.marks[mid]
            person = self.people[mention['person_id']]
            self.assertTrue(any(e.get('mention_id') == mid and e.get('quote') == mention['surface']
                                for e in person['evidence']))
            self.assertTrue(any(a['surface'] == mention['surface'] and mid in a['mention_ids']
                                for a in person['aliases']))

    def test_uncle_choice_is_separate_and_less_certain_than_zong(self):
        z = self.decisions['d-nanqi033-song052-xiezong']
        u = self.decisions['d-nanqi033-song052-xiezong-uncle']
        self.assertEqual((z['person_id'], u['person_id']), (self.zong, self.fan))
        self.assertEqual((z['confidence_level'], u['confidence_level']), ('high', 'medium'))
        self.assertIn('一人可能多舅', u['rationale'])
        self.assertIn('不推母名', u['rationale'])
        for decision in (z, u):
            self.assertEqual(decision['status'], 'contextual_provisional')
            self.assertIs(decision['human_reviewed'], False)
            self.assertEqual({e['paragraph_id']: e['quote'] for e in decision['evidence']},
                             {self.qp['id']: self.qp['text'], self.sp['id']: self.sp['text']})

    def test_retired_ids_are_neither_people_nor_alias_endpoints(self):
        from scripts.retired_person_ids import retired_person_ids
        retired = {'tbn_5t5_xwp', 'afp_p47_7v4'}
        self.assertTrue(retired <= retired_person_ids(ROOT))
        self.assertFalse(retired & set(self.people))
        self.assertFalse(retired & {a for p in self.people.values() for a in p.get('id_aliases', [])})
        for pid in retired:
            for folder in ('exports/persons', 'data/corpus/profiles'):
                self.assertFalse((ROOT / folder / f'{pid}.json').exists())


if __name__ == '__main__':
    unittest.main()
