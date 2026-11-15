import copy
import json
import unittest
from pathlib import Path

from scripts.collateral_kinship import agnatic_senior_kin_valid

ROOT = Path(__file__).resolve().parents[1]


class SongshuXieKinshipTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.paragraphs = {}
        cls.assertions = []
        for stem in ('058-xiehongwei', '067-xielingyun'):
            chapter = json.loads((ROOT / f'corpus/songshu/{stem}.json').read_text())
            aset = json.loads((ROOT / f'corpus/songshu/{stem}-assertions.json').read_text())
            cls.paragraphs.update({p['id']: (chapter['id'], p) for p in chapter['paragraphs']})
            cls.assertions.extend(a for a in aset['assertions']
                                  if a.get('id', '').startswith(('a-song058-xiehun-', 'a-song067-lingyun-congshu-')))

    def test_four_people_share_the_exact_collective_zuzi_clause(self):
        self.assertEqual(len([a for a in self.assertions if a['id'].startswith('a-song058')]), 4)
        for a in self.assertions:
            if a['id'].startswith('a-song058'):
                self.assertTrue(agnatic_senior_kin_valid(a, self.paragraphs), a['id'])
                self.assertEqual(a['qualifiers']['source_term'], '族子')
                self.assertEqual(a['qualifiers']['kinship_structure']['distance'], None)
                self.assertIsNone(a['qualifiers']['kinship_structure']['common_ancestor_person_id'])

    def test_congshu_is_bound_only_to_lingyun_and_hun_in_songshu_67(self):
        a = next(a for a in self.assertions if a['id'] == 'a-song067-lingyun-congshu-hun')
        self.assertTrue(agnatic_senior_kin_valid(a, self.paragraphs))
        self.assertEqual((a['subject_person_id'], a['object_person_id']),
                         ('aa6_83c_juy_CDAA', 'aa6_83c_juy_BAC'))

    def test_collective_clause_rejects_mutated_scope_or_member(self):
        original = next(a for a in self.assertions if a['id'] == 'a-song058-xiehun-zhan-zuzi')
        mutations = [
            lambda a: a['qualifiers']['source_clause_binding'].update(start=12),
            lambda a: a['qualifiers'].update(source_term='族子瞻'),
            lambda a: a['evidence'][0].update(subject_person_mention_id='c-songshu-058-xiehongwei:p003:m0013'),
            lambda a: a['evidence'][0].update(object_person_mention_id='c-songshu-058-xiehongwei:p003:m0041'),
            lambda a: a.update(subject_person_id='aa6_83c_juy_CDAA'),
        ]
        for mutate in mutations:
            bad = copy.deepcopy(original)
            mutate(bad)
            self.assertFalse(agnatic_senior_kin_valid(bad, self.paragraphs))

    def test_congshu_rejects_wrong_direction_clause_or_invented_degree(self):
        original = next(a for a in self.assertions if a['id'] == 'a-song067-lingyun-congshu-hun')
        mutations = [
            lambda a: a.update(subject_person_id=a['object_person_id'], object_person_id=a['subject_person_id']),
            lambda a: a['evidence'][0]['relationship_anchor'].update(start=70),
            lambda a: a['qualifiers'].update(source_term='叔混'),
            lambda a: a['qualifiers']['kinship_structure'].update(distance=2),
            lambda a: a['qualifiers']['kinship_structure'].update(subject_relative_age='younger'),
            lambda a: a['evidence'][0].update(subject_person_mention_id='c-songshu-067-xielingyun:p001:m00001'),
            lambda a: a['evidence'][0].update(object_person_mention_id='c-songshu-067-xielingyun:p001:m00070'),
        ]
        for mutate in mutations:
            bad = copy.deepcopy(original)
            mutate(bad)
            self.assertFalse(agnatic_senior_kin_valid(bad, self.paragraphs))


if __name__ == '__main__':
    unittest.main()
