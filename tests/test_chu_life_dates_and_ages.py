# coding: utf-8
import copy
import json
import unittest
from pathlib import Path
from scripts.age_approximations import age_approximation_errors
from scripts.validate_corpus import normalized_date_errors
ROOT = Path(__file__).resolve().parents[1]
def read(path):
    return json.loads((ROOT / path).read_text())

class ChuLifeDatesAndAges(unittest.TestCase):
    def setUp(self):
        self.c = read('corpus/jinshu/093-chupou.json')
        self.a = next(a for a in self.c['annotation']['age_assertions'] if 'approximation' in a)
        self.p = next(p for p in self.c['paragraphs'] if p['source_position']['first_line'] == 49)
        self.death = read('corpus/jinshu/032-chu-lingyuan-life-events.json')['events'][0]
    def test_approaching_fifty_belongs_to_ancestor_and_is_not_exact_or_bound(self):
        self.assertEqual(age_approximation_errors(self.a, self.p), [])
        self.assertEqual(self.a['approximation']['target'], 50)
        self.assertEqual(self.a['person_id'], 'xke_dj3_6ba')
        self.assertIsNone(self.a['value'])
        self.assertIsNone(self.a['birth_year'])
        for key, value in [('value', 49), ('bounds', {'upper': 50}), ('birth_year', 300), ('subject_scope', None)]:
            a = copy.deepcopy(self.a); a[key] = value
            self.assertTrue(age_approximation_errors(a, self.p), key)
    def test_cannot_move_ancestor_age_to_biography_subject_or_false_quote(self):
        a = copy.deepcopy(self.a)
        a['person_id'] = next(m['person_id'] for m in self.p['mentions'] if m['surface'] == '褚裒')
        self.assertTrue(age_approximation_errors(a, self.p))
        a = copy.deepcopy(self.a); a['evidence'][0]['quote'] = '年垂五十'
        self.assertTrue(age_approximation_errors(a, self.p))
    def test_dynastic_prefix_stays_in_original_date_and_has_numeric_year(self):
        d = self.death['normalized_date']
        self.assertEqual(d['source_expression'], '宋元嘉十三年')
        self.assertEqual(d['year'], 436)
        self.assertEqual(normalized_date_errors(d), [])
        self.assertEqual(d['regnal_year_mapping']['source_polity_prefix'], '宋')
    def test_wrong_prefix_dynasty_year_or_missing_prefix_proof_is_rejected(self):
        for change in ['prefix', 'columns', 'year', 'missing', 'empty', 'bad_columns']:
            d = copy.deepcopy(self.death['normalized_date'])
            if change == 'prefix': d['regnal_year_mapping']['source_polity_prefix'] = '明'
            elif change == 'columns': d['references'][0]['columns']['dynasty'] = '東晉'
            elif change == 'year': d['year'] = d['era_year'] = 437
            elif change == 'missing': d['regnal_year_mapping'].pop('source_polity_prefix')
            elif change == 'empty': d['regnal_year_mapping']['source_polity_prefix'] = ''
            else: d['references'][0]['columns'] = None
            self.assertTrue(normalized_date_errors(d), change)
    def test_exact_death_ages_do_not_become_birth_years(self):
        expected = {'093-chupou': (349,47), '032-chu-suanzi': (384,61), '032-chu-lingyuan': (436,53)}
        for stem, (year, value) in expected.items():
            ages = read('corpus/jinshu/' + stem + '.json')['annotation']['age_assertions']
            a = next(a for a in ages if a['age_context']['kind'] == 'at_death')
            self.assertEqual(a['normalized_date']['year'], year)
            self.assertEqual(a['value'], value)
            self.assertIsNone(a['birth_year'])
            self.assertEqual(normalized_date_errors(a['normalized_date']), [])
    def test_stone_death_has_two_passages_without_copying_pou_year(self):
        e = next(e for e in read('corpus/jinshu/093-chupou-life-events.json')['events'] if e['id'].endswith('shijilong-death'))
        self.assertEqual(len(e['evidence']), 2)
        self.assertIsNone(e['date_expression'])
        self.assertNotIn('normalized_date', e)
    def test_places_are_not_inherited_from_relatives_or_offices(self):
        rows = [a for stem in ['093-chupou','032-chu-suanzi','032-chu-lingyuan'] for a in read('corpus/jinshu/' + stem + '-addresses.json')['assertions']]
        self.assertEqual(len(rows), 6)
        self.assertEqual(sum(a['relation'] == 'biographical_origin' for a in rows), 2)
        self.assertTrue(all(a['place']['modern_identification'] is None for a in rows))
        self.assertEqual([a['place']['source_name'] for a in rows if a['relation'] == 'death_place'], ['顯陽殿'])
if __name__ == '__main__':
    unittest.main()
