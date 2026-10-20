"""Narrative identity must not absorb general or fictional imperial roles."""
import json
from pathlib import Path
import unittest
from scripts.consolidate_person_ids import reference_files

ROOT = Path(__file__).resolve().parents[1]
WU = 'yqp_nlb_p1p_ACAA'
OLD = '7jv_d9q_x7x'
GENERIC = {'c-shiji-117-xiangru:m003-0160',
           'c-shiji-117-xiangru:m003-0176',
           'c-shiji-117-xiangru:m038-0031'}

def read(path):
    return json.loads((ROOT / path).read_text())

class XiangruEmperorScope(unittest.TestCase):
    def test_forty_four_contextual_occurrences_reach_wudi(self):
        chapter = read('corpus/shiji/117.json')
        mentions = [m for p in chapter['paragraphs'] for m in p['mentions']]
        actual = [m for m in mentions if m['person_id'] == WU]
        self.assertEqual(len(actual), 44)
        self.assertEqual({m['surface'] for m in actual}, {'上', '天子', '陛下', '君'})
        self.assertFalse(GENERIC & {m['id'] for m in actual})

    def test_three_general_roles_remain_unlinked_with_nonexhaustive_case(self):
        chapter = read('corpus/shiji/117.json')
        mentions = {m['id']: m for p in chapter['paragraphs'] for m in p['mentions']}
        for mid in GENERIC:
            self.assertIsNone(mentions[mid]['person_id'])
            self.assertEqual(mentions[mid]['kind'], 'unresolved')
        case = next(c for c in chapter['annotation']['unresolved_identity_cases']
                    if c['id'] == 'u-shiji117-imperial-role-and-allusion')
        self.assertEqual(set(case['unresolved_mention_ids']), GENERIC)
        self.assertEqual(case['candidate_person_ids'], [WU])
        self.assertFalse(case['candidate_list_exhaustive'])
        self.assertTrue(case['unknown_identity_possible'])
        self.assertIn('generic_imperial_role', case['referent_kind_alternatives'])

    def test_identity_is_supported_by_parallel_missions_and_rituals(self):
        decision = next(d for d in read('corpus/shiji/117-equivalences.json')['decisions']
                        if d['id'] == 'eq-shiji117-reigning-emperor')
        self.assertEqual(decision['person_ids'], [WU])
        self.assertTrue(decision['identity_materialized'])
        self.assertFalse(decision['human_reviewed'])
        self.assertEqual(set(decision['chapter_ids']),
                         {'c-shiji-117-xiangru', 'c-shiji-116-xinanyi', 'c-shiji-012-wudi'})
        self.assertTrue(all(e['quote'] and e['mention_ids'] for e in decision['evidence']))

    def test_old_identity_is_retired_after_reference_migration(self):
        self.assertNotIn(OLD, {p['id'] for p in read('registry/persons.json')['persons']})
        for path in reference_files(ROOT):
            self.assertNotIn(OLD, path.read_text(), str(path))
        for directory in ('exports/persons', 'data/corpus/profiles'):
            self.assertFalse((ROOT / directory / f'{OLD}.json').exists())

    def test_attested_given_name_and_retrospective_heading_are_separate(self):
        name = next(n for n in read('data/corpus/profile-names.json')['records']
                    if n['person_id'] == WU)
        self.assertEqual(name['ming'], '徹')
        self.assertIsNone(name['surname'])
        self.assertEqual(name['title'], '孝武皇帝')
        self.assertIn('名徹', name['quote'])
        self.assertEqual(name['chapter_id'], 'c-shiji-011-jingdi')
        self.assertEqual(name['references'][0]['scope'], 'received_heading_title')

if __name__ == '__main__':
    unittest.main()
