# coding: utf-8
import json
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def read(path):
    return json.loads((ROOT / path).read_text())

class ChuSuanziReceivedUnit(unittest.TestCase):
    def setUp(self):
        self.c = read('corpus/jinshu/032-chu-suanzi.json')
        self.people = {p['label']: p['id'] for p in read('registry/persons.json')['persons']}
    def paragraph(self, line):
        return next(p for p in self.c['paragraphs'] if p['source_position']['first_line'] == line)
    def test_all_six_complete_paragraphs_and_spans(self):
        self.assertEqual([p['source_position']['first_line'] for p in self.c['paragraphs']], [40, 42, 44, 46, 48, 50])
        self.assertEqual(sum(len(p['mentions']) for p in self.c['paragraphs']), 83)
        for p in self.c['paragraphs']:
            for m in p['mentions']:
                self.assertEqual(p['text'][m['start']:m['end']], m['surface'])
    def test_petition_address_distinguishes_explicit_queen_and_qualified_chupou_reading(self):
        queen = self.people['褚蒜子']
        addressed = [m for p in self.c['paragraphs'] for m in p['mentions'] if m['surface'] == '陛下']
        self.assertTrue(addressed)
        self.assertTrue(all(m['person_id'] == queen for m in addressed))
        other = read('corpus/jinshu/093-chupou.json')
        emperor = [m for p in other['paragraphs'] for m in p['mentions'] if m['surface'] == '陛下']
        self.assertTrue(emperor)
        self.assertTrue(all(m['person_id'] == queen for m in emperor))
        decision = next(d for d in read('corpus/jinshu/093-chupou-identities.json')['decisions'] if d['id'].endswith('regency-addressee'))
        self.assertEqual(decision['confidence_level'], 'medium')
        self.assertEqual(decision['alternatives'][0]['person_id'], self.people['晉穆帝'])
        self.assertEqual(decision['alternatives'][0]['status'], 'not_preferred_but_not_excluded')
    def test_same_paragraph_switches_from_jianwen_death_to_xiaowu_coronation(self):
        p = self.paragraph(48)
        deaths = [m for m in p['mentions'] if m['surface'] == '帝' and p['text'][m['start']:m['end'] + 1] == '帝崩']
        self.assertEqual(len(deaths), 1)
        self.assertEqual(deaths[0]['person_id'], self.people['晉簡文帝'])
        crowned = next(m for m in p['mentions'] if m['surface'] == '帝' and p['text'][m['start']:m['end'] + 2] == '帝既冠')
        self.assertEqual(crowned['person_id'], self.people['晉孝武帝'])
    def test_prior_mothers_are_distinct_people_without_reusing_other_xun(self):
        p = self.paragraph(42)
        xun = next(m for m in p['mentions'] if m['surface'] == '荀')
        bian = next(m for m in p['mentions'] if m['surface'] == '卞')
        self.assertNotEqual(xun['person_id'], bian['person_id'])
        self.assertNotEqual(xun['person_id'], self.people['荀氏（明帝及裒生母）'])
        proposals = read('corpus/jinshu/032-chu-suanzi-assertions.json')['assertions']
        self.assertFalse(any(a['predicate'] == 'mother' for a in proposals))
    def test_collective_examples_not_forced_to_single_person_and_later_situ_not_caimo(self):
        for line, term in [(42, '二媯'), (48, '有莘')]:
            m = next(m for m in self.paragraph(line)['mentions'] if m['surface'] == term)
            self.assertIsNone(m['person_id'])
        later = next(m for m in self.paragraph(44)['mentions'] if m['surface'] == '司徒')
        self.assertNotEqual(later['person_id'], self.people['蔡謨'])
        self.assertEqual(later['person_id'], self.people['晉簡文帝'])
        decisions = read('corpus/jinshu/032-chu-suanzi-identities.json')['decisions']
        d = next(x for x in decisions if x['id'] == 'd-jinshu032-chu-suanzi-situ-at-mu-coming-of-age')
        self.assertEqual(d['identification_basis']['target_mention_ids'], [later['id']])
        self.assertTrue(all(r['source_revision'] == 2644502 for r in d['references']))
if __name__ == '__main__':
    unittest.main()
