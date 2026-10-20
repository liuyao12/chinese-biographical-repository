import copy
import json
import unittest
from pathlib import Path
from scripts.collateral_kinship import agnatic_senior_kin_valid, source_sibling_group_valid
from scripts.uncle_parentage import explicit_maternal_uncle_valid
from scripts.validate_corpus import source_age_number

ROOT = Path(__file__).resolve().parents[1]


class CollateralKinshipTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        c = json.loads((ROOT / 'corpus/jinshu/032.json').read_text())
        cls.paragraphs = {p['id']: (c['id'], p) for p in c['paragraphs']}
        cls.assertions = json.loads((ROOT / 'corpus/jinshu/032-assertions.json').read_text())['assertions']
        cls.person_ids = {p['id'] for p in json.loads((ROOT / 'registry/persons.json').read_text())['persons']}
        cls.junior = next(a for a in cls.assertions if a['predicate'] == 'agnatic_senior_kin')
        cls.group = next(a for a in cls.assertions if 'source_sibling_group' in a.get('qualifiers', {}))
        cls.uncle = next(a for a in cls.assertions if a['predicate'] == 'maternal_uncle')

    def test_congzi_preserves_generation_without_father_distance_or_age(self):
        self.assertTrue(agnatic_senior_kin_valid(self.junior, self.paragraphs))
        self.assertEqual(self.junior['qualifiers']['kinship_structure']['generation_difference'], -1)
        for key, value in [('generation_difference', 0), ('distance', 2),
                           ('common_ancestor_person_id', self.junior['object_person_id']),
                           ('subject_relative_age', 'younger'), ('direct_parent_person_id', self.junior['object_person_id'])]:
            a = copy.deepcopy(self.junior)
            a['qualifiers']['kinship_structure'][key] = value
            self.assertFalse(agnatic_senior_kin_valid(a, self.paragraphs), key)

    def test_congzi_cannot_borrow_another_senior_or_clause(self):
        a = copy.deepcopy(self.junior)
        a['object_person_id'] = a['subject_person_id']
        self.assertFalse(agnatic_senior_kin_valid(a, self.paragraphs))
        a = copy.deepcopy(self.junior)
        a['qualifiers']['source_term'] = '子傭'
        self.assertFalse(agnatic_senior_kin_valid(a, self.paragraphs))
        a = copy.deepcopy(self.junior)
        a['evidence'][0]['chapter_id'] = 'another-book'
        self.assertFalse(agnatic_senior_kin_valid(a, self.paragraphs))

    def test_reported_four_sisters_keep_only_explicit_one_and_three(self):
        self.assertTrue(source_sibling_group_valid(self.group, self.paragraphs, self.person_ids, source_age_number))
        g = self.group['qualifiers']['source_sibling_group']
        self.assertEqual(g['reported_count'], 4)
        roles = {r['source_term']: r for r in g['member_roles']}
        self.assertEqual(roles['后最長']['ordinal'], 1)
        self.assertEqual(roles['第三者']['ordinal'], 3)
        self.assertIsNone(roles['中者']['ordinal'])
        self.assertIsNone(roles['小者']['ordinal'])
        for term, ordinal in [('中者', 2), ('小者', 4)]:
            a = copy.deepcopy(self.group)
            next(r for r in a['qualifiers']['source_sibling_group']['member_roles']
                 if r['source_term'] == term)['ordinal'] = ordinal
            self.assertFalse(source_sibling_group_valid(a, self.paragraphs, self.person_ids, source_age_number))

    def test_group_cannot_change_count_members_or_person_roles(self):
        for mutation in [
            lambda g: g.update(reported_count=3),
            lambda g: g['member_person_ids'].pop(),
            lambda g: g['member_roles'][0].update(person_id=g['member_roles'][1]['person_id']),
            lambda g: g['member_roles'][0].update(ordinal=True),
            lambda g: g['source_anchor'].update(start=0),
        ]:
            a = copy.deepcopy(self.group)
            mutation(a['qualifiers']['source_sibling_group'])
            self.assertFalse(source_sibling_group_valid(a, self.paragraphs, self.person_ids, source_age_number))

    def test_maternal_uncle_can_have_an_explicit_place_in_the_phrase(self):
        self.assertTrue(explicit_maternal_uncle_valid(self.uncle, self.paragraphs))
        a = copy.deepcopy(self.uncle)
        a['qualifiers']['intervening_place_name'] = 'another-place'
        self.assertFalse(explicit_maternal_uncle_valid(a, self.paragraphs))
        a = copy.deepcopy(self.uncle)
        a['qualifiers']['mother_person_id'] = a['subject_person_id']
        self.assertFalse(explicit_maternal_uncle_valid(a, self.paragraphs))


if __name__ == '__main__':
    unittest.main()
