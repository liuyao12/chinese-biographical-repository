import copy
import json
import unittest
from pathlib import Path

from scripts.biography_family_clause import valid

ROOT = Path(__file__).resolve().parents[1]


class Nanqishu046ClanRelations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        chapter = json.loads((ROOT / 'corpus/nanqishu/046.json').read_text())
        cls.paragraphs = {p['id']: (chapter['id'], p) for p in chapter['paragraphs']}
        cls.assertions = json.loads((ROOT / 'corpus/nanqishu/046-assertions.json').read_text())['assertions']
        cls.relations = [a for a in cls.assertions if a['id'].startswith('a-nanqi046-')]

    def test_both_source_bound_relations_validate(self):
        self.assertEqual(len(self.relations), 2)
        for assertion in self.relations:
            self.assertTrue(valid(assertion, self.paragraphs, self.assertions), assertion['id'])

    def test_clansman_does_not_invent_paternal_path_or_common_ancestor(self):
        a = next(x for x in self.relations if x['predicate'] == 'kinship_unspecified')
        q = a['qualifiers']
        self.assertEqual(a['subject_person_id'], '7r6_k52_qji_ABDABAABA')
        self.assertEqual(a['object_person_id'], '7r6_k52_qji_ABAAAA*AA')
        self.assertEqual(q['lineage'], 'unspecified')
        self.assertIsNone(q['generation_difference'])
        self.assertIsNone(q['exact_distance'])
        self.assertIsNone(q['common_ancestor_person_id'])
        changed = copy.deepcopy(a)
        changed['qualifiers']['lineage'] = 'paternal'
        self.assertFalse(valid(changed, self.paragraphs, self.assertions))

    def test_congzu_brother_keeps_unknown_distance_and_only_relative_age(self):
        a = next(x for x in self.relations if x['predicate'] == 'agnatic_cousin')
        structure = a['qualifiers']['kinship_structure']
        order = a['qualifiers']['relative_birth_order']
        self.assertEqual(structure['generation_difference'], 0)
        self.assertEqual(structure['distance'], {'kind': 'paternal_second_cousins', 'common_ancestor_depth': {'subject': 3, 'reference': 3}})
        self.assertIsNone(structure['common_ancestor_person_id'])
        self.assertEqual(structure['subject_relative_age'], 'older')
        self.assertIsNone(order['older_ordinal'])
        self.assertIsNone(order['younger_ordinal'])
        changed = copy.deepcopy(a)
        changed['qualifiers']['relative_birth_order']['older_person_id'] = a['object_person_id']
        changed['qualifiers']['relative_birth_order']['younger_person_id'] = a['subject_person_id']
        self.assertFalse(valid(changed, self.paragraphs, self.assertions))
