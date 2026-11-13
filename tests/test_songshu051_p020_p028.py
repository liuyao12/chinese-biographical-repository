import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from song051_p020_p028 import (assertions, family_valid, life_event_valid,
                               life_events, load, name_components)
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
