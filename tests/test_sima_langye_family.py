# coding: utf-8
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((ROOT / name).read_text())


class SimaLangyeFamilyTests(unittest.TestCase):
    def setUp(self):
        self.chapter = load('corpus/jinshu/038.json')
        self.assertions = load('corpus/jinshu/038-assertions.json')['assertions']
        self.family = next(x for x in load('registry/family-assemblies.json')['assemblies']
                           if x['id'] == 'family-sima-jun-near-ancestry')
        self.members = {m['person_id']: m for m in self.family['members']}
        self.root = 'dkn_ge4_286'

    def test_yuandi_and_hun_share_attested_father_not_pou(self):
        jin = self.root + '_AAAAAA'
        for child in [self.root + '_AAAAAAA', self.root + '_AAAAAAB']:
            assertion = next(a for a in self.assertions
                             if a['subject_person_id'] == child and a['predicate'] == 'father')
            self.assertEqual(assertion['object_person_id'], jin)
            self.assertEqual(self.members[child]['parent_person_id'], jin)
        pou = self.root + '_AAAAAAAB'
        self.assertEqual(self.members[pou]['parent_person_id'], self.root + '_AAAAAAA')
        # His uncle's ritual succession never replaces the explicit father.
        care = load('corpus/jinshu/064-assertions.json')['assertions']
        self.assertTrue(any(a['subject_person_id'] == pou and a['predicate'] == 'ritual_successor_of'
                            and a['object_person_id'] == self.root + '_AAAAAAB' for a in care))

    def test_all_nine_sons_have_source_bound_biological_mothers(self):
        father = self.root + '_AAAA'
        sons = [a['subject_person_id'] for a in self.assertions
                if a['predicate'] == 'father' and a['object_person_id'] == father]
        self.assertEqual(len(set(sons)), 9)
        mothers = [a for a in self.assertions if a['predicate'] == 'mother'
                   and a['subject_person_id'] in sons]
        self.assertEqual(len(mothers), 9)
        self.assertEqual(sorted(sum(a['object_person_id'] == m['object_person_id']
                                    for a in mothers) for m in mothers),
                         [1, 1, 3, 3, 3, 4, 4, 4, 4])
        self.assertFalse(any(a['predicate'] == 'spouse' for a in self.assertions))

    def test_two_zhang_women_are_not_collapsed_by_surname(self):
        p = next(p for p in self.chapter['paragraphs'] if p['source_position']['first_line'] == 12)
        women = {m['surface']: m['person_id'] for m in p['mentions']
                 if m['surface'] in ['穆張皇后', '張夫人']}
        self.assertEqual(len(set(women.values())), 2)

    def test_dan_second_son_does_not_assign_other_sons_ordinals(self):
        zhou = self.root + '_AAAAA'
        children = [a for a in self.assertions
                    if a['predicate'] == 'father' and a['object_person_id'] == zhou]
        self.assertEqual(len(children), 4)
        numbered = [a for a in children if a['qualifiers'].get('birth_order')]
        self.assertEqual(len(numbered), 1)
        self.assertEqual(numbered[0]['subject_person_id'], self.root + '_AAAAAB')
        self.assertEqual(numbered[0]['qualifiers']['birth_order']['ordinal'], 2)

    def test_actual_family_paths_and_one_assembly_for_each_member(self):
        assemblies = load('registry/family-assemblies.json')['assemblies']
        for pid, member in self.members.items():
            self.assertEqual(sum(m['person_id'] == pid for a in assemblies for m in a['members']), 1)
            parent = member.get('parent_person_id')
            if parent:
                self.assertEqual(pid.rsplit('_', 1)[-1][:-1],
                                 '' if parent == self.root else parent.rsplit('_', 1)[-1])
        self.assertFalse(any(a['id'] == 'family-sima-yuandi-six-sons' for a in assemblies))

    def test_excerpt_boundaries_and_apparatus_remain_explicit(self):
        full = [p for p in self.chapter['paragraphs']
                if p['source_position'].get('editorial_excerpt_boundary') is False]
        self.assertEqual({p['source_position']['first_line'] for p in full}, {12, 28})
        for p in self.chapter['paragraphs']:
            self.assertNotIn('<ref>', p['text'])
            self.assertNotIn('今從吳本', p['text'])
        self.assertTrue(self.chapter['source']['normalization']['removed_apparatus'])


if __name__ == '__main__':
    unittest.main()
