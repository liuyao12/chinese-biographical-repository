import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from song051_p020_p028 import (addresses, age_assertions, assertions, family_valid, life_event_valid,
                               life_events, load, name_components, titles)
from maternal_cousins import maternal_cousin_valid
from surname_from_father import validate as validate_surname


class Songshu051P020P028Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = load(ROOT, 'corpus/songshu/051-wyd1739.json')
        cls.ps = {p['id']: (cls.chapter['id'], p) for p in cls.chapter['paragraphs']}
        cls.assertions = assertions(cls.chapter)['assertions']

    def test_explicit_huan_father_and_son_binding(self):
        assertion = self.assertions[0]
        self.assertTrue(family_valid(assertion, self.ps, {self.chapter['id']: self.chapter}, ROOT))
        mutated = copy.deepcopy(assertion)
        mutated['qualifiers']['source_clause_binding']['end'] += 1
        self.assertFalse(family_valid(mutated, self.ps, {self.chapter['id']: self.chapter}, ROOT))

    def test_congmu_xiong_is_maternal_and_older(self):
        assertion = self.assertions[1]
        self.assertTrue(maternal_cousin_valid(assertion, self.ps))
        mutated = copy.deepcopy(assertion)
        mutated['qualifiers']['kinship_structure']['lineage'] = 'paternal'
        self.assertFalse(maternal_cousin_valid(mutated, self.ps))
        mutated = copy.deepcopy(assertion)
        mutated['qualifiers']['relative_birth_order']['operator'] = 'gt'
        self.assertFalse(maternal_cousin_valid(mutated, self.ps))

    def test_daoer_surname_is_only_contextual_same_clause(self):
        record = name_components(self.chapter)['records'][2]
        names = json.loads((ROOT / 'corpus/songshu/051-wyd1739-p020-p028-name-components.json').read_text())['records']
        validate_surname(record, names, {self.chapter['id']: self.chapter}, self.assertions, ROOT)
        mutated = copy.deepcopy(record)
        mutated['surname_basis']['start'] += 1
        with self.assertRaises(ValueError):
            validate_surname(mutated, names, {self.chapter['id']: self.chapter}, self.assertions, ROOT)

    def test_second_son_rank_is_source_attested(self):
        rank = next(a for a in self.assertions if a['id'] == 'a-song051-p020-p028-liu-yiqing-second-son-of-daolian')
        self.assertEqual(('3qs_nqa_ioa_AABB', '3qs_nqa_ioa_AAB'), (rank['subject_person_id'], rank['object_person_id']))
        self.assertEqual({'ordinal': 2, 'source_term': '第二子', 'scope': 'sons_of_parent',
                          'parent_person_id': '3qs_nqa_ioa_AAB', 'position': 'unspecified',
                          'interpretation_status': 'source_attested'}, rank['qualifiers']['birth_order'])

    def test_daogui_reported_age_preserves_split_source_phrase(self):
        age = age_assertions(self.chapter, ROOT)['assertions'][0]
        self.assertEqual((43, '四十三', '時年四十三'), (age['value'], age['source_number'], age['source_term']))
        self.assertEqual(['時年', '四十三'], [p['surface'] for p in age['source_term_split_binding']['parts']])
        self.assertIsNone(age['birth_year'])
        self.assertEqual(412, age['normalized_date']['year'])

    def test_daogui_death_context_uses_main_subject_mention(self):
        expected = 'c-songshu-051-wyd1739-zongshi:p027:m0129'
        death = next(e for e in life_events(self.chapter, ROOT)['events'] if e['id'] == 'le-song051-p020-p028-daogui-death')
        self.assertEqual(expected, death['evidence'][0]['person_mention_id'])
        self.assertEqual(expected, death['normalized_date']['evidence'][0]['person_mention_id'])
        address = next(a for a in addresses(self.chapter)['assertions'] if a['id'] == 'ad-song051-p020-p028-daogui-death-place')
        self.assertEqual(expected, address['evidence'][0]['person_mention_id'])
        age = age_assertions(self.chapter, ROOT)['assertions'][0]
        self.assertEqual(expected, age['evidence'][0]['person_mention_id'])
        holdings = titles(self.chapter)['holdings']
        self.assertTrue(all(h['attestations'][0]['person_mention_id'] == expected
                            for h in holdings if h['id'].endswith(('daogui-zhengxi','daogui-kaifu','daogui-sanjichangshi'))))
        enfeoffment = next(h for h in holdings if h['id'] == 'th-song051-p020-p028-daogui-linchuanwang')
        self.assertEqual(expected, enfeoffment['enfeoffment_basis']['death_context']['person_mention_id'])

    def test_death_dates_are_source_bound_and_reversible(self):
        events = life_events(self.chapter, ROOT)['events']
        self.assertEqual([414, 412], [e['normalized_date']['year'] for e in events])
        self.assertTrue(all(life_event_valid(e, ROOT) for e in events))
        self.assertEqual('義熙十年', events[0]['normalized_date']['source_expression'])
        self.assertEqual('八年閏月', events[1]['normalized_date']['source_expression'])
        mutated = copy.deepcopy(events[1])
        mutated['normalized_date']['year'] = 413
        self.assertFalse(life_event_valid(mutated, ROOT))


if __name__ == '__main__':
    unittest.main()
