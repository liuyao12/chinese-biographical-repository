import copy
import json
import unittest
from pathlib import Path
from scripts.family_assemblies import load_assemblies
from scripts.person_bundle import load_catalog
from scripts.unspecified_ancestry import unspecified_ancestry_valid

ROOT = Path(__file__).resolve().parents[1]


def read(p):
    return json.loads((ROOT / p).read_text())


class WangRoots033(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.people = {p['label']: p['id'] for p in read('registry/persons.json')['persons']}
        cls.chapter = read('corpus/jinshu/033.json')
        cls.assertions = read('corpus/jinshu/033-assertions.json')['assertions']
        cls.paragraphs = {p['id']: (cls.chapter['id'], p) for p in cls.chapter['paragraphs']}

    def test_extended_paternal_tree_keeps_same_four_descendants(self):
        _, members = load_assemblies(ROOT, load_catalog(ROOT))
        for child, parent in [('王弘', '王珣'), ('王珣', '王洽'), ('王洽', '王導'),
                              ('王導', '王裁'), ('王裁', '王覽'), ('王覽', '王融'), ('王融', '王仁')]:
            self.assertEqual(members[self.people[child]]['parent_person_id'], self.people[parent])
        self.assertIsNone(members[self.people['王覽']]['source_assertion_id'])
        self.assertIsNone(members[self.people['王融']]['source_assertion_id'])

    def test_stepparent_does_not_become_birth_mother(self):
        zhu = self.people['朱氏（王覽母）']
        rels = {(a['subject_person_id'], a['predicate'], a['object_person_id']) for a in self.assertions}
        self.assertIn((self.people['王祥'], 'stepmother', zhu), rels)
        self.assertIn((self.people['王覽'], 'mother', zhu), rels)
        self.assertNotIn((self.people['王祥'], 'mother', zhu), rels)
        self.assertTrue(any(a['predicate'] == 'stepmother' and a['qualifiers']['source_term'] == '繼母' for a in self.assertions))

    def test_six_sons_are_not_six_absolute_ordinals(self):
        a = [a for a in self.assertions if a['predicate'] == 'father' and a['object_person_id'] == self.people['王覽']]
        self.assertEqual({x['subject_person_id'] for x in a}, {self.people[n] for n in ['王裁','王基','王會','王正','王彥','王琛']})
        self.assertTrue(all('birth_order' not in x['qualifiers'] for x in a))
        self.assertTrue(all(x['context']['kind'] == 'adjacent_paragraphs' for x in a))

    def test_remote_descent_remains_unknown_and_outside_tree(self):
        a = next(a for a in self.assertions if a['predicate'] == 'ancestor')
        self.assertTrue(unspecified_ancestry_valid(a, self.paragraphs))
        self.assertIsNone(a['qualifiers']['generation_distance'])
        _, members = load_assemblies(ROOT, load_catalog(ROOT))
        self.assertNotIn(a['object_person_id'], members)
        for key, value in [('generation_distance', 10), ('source_number', '十'), ('reported_generation_number', 10), ('adopted_for_family_tree', True)]:
            bad = copy.deepcopy(a); bad['qualifiers'][key] = value
            self.assertFalse(unspecified_ancestry_valid(bad, self.paragraphs))

    def test_remote_claim_cannot_use_another_person_or_unanchored_term(self):
        a = next(a for a in self.assertions if a['predicate'] == 'ancestor')
        bad = copy.deepcopy(a); bad['object_person_id'] = self.people['王仁']
        self.assertFalse(unspecified_ancestry_valid(bad, self.paragraphs))
        bad = copy.deepcopy(a); bad['qualifiers']['source_term'] = '另人之後'
        self.assertFalse(unspecified_ancestry_valid(bad, self.paragraphs))

    def test_witness_character_and_date_template_are_preserved(self):
        self.assertTrue(any('漢未遭亂' in p['text'] for p in self.chapter['paragraphs']))
        self.assertTrue(any('乙太中大夫歸老' in p['text'] for p in self.chapter['paragraphs']))
        self.assertTrue(any('咸寧四年' in p['text'] for p in self.chapter['paragraphs']))
        self.assertFalse(any('{{YL' in p['text'] for p in self.chapter['paragraphs']))
        self.assertFalse(self.chapter['source']['image_verified'])

    def test_death_year_age_and_unknown_parent_deaths_remain_separate(self):
        deaths = read('corpus/jinshu/033-life-events.json')['events']
        lan = next(e for e in deaths if e['person_id'] == self.people['王覽'])
        self.assertEqual(lan['normalized_date']['year'], 278)
        self.assertEqual(lan['normalized_date']['calendar'], 'chinese_civil')
        self.assertEqual(lan['date_expression'], '咸寧四年')
        age = self.chapter['annotation']['age_assertions'][0]
        self.assertEqual(age['value'], 73)
        self.assertIsNone(age['birth_year'])
        for e in deaths:
            self.assertEqual(e['event_type'], 'death')
            if e['person_id'] != self.people['王覽']:
                self.assertIsNone(e['date_expression'])
                self.assertNotIn('normalized_date', e)

    def test_flight_is_not_inherited_native_place(self):
        addresses = read('corpus/jinshu/033-addresses.json')['assertions']
        origins = [a for a in addresses if a['relation'] == 'biographical_origin']
        self.assertEqual([a['person_id'] for a in origins], [self.people['王祥']])
        self.assertEqual(origins[0]['place']['source_name'], '琅邪臨沂')
        moves = [a for a in addresses if a['relation'] == 'migration_destination']
        self.assertEqual({a['person_id'] for a in moves}, {self.people[n] for n in ['王祥','王覽','朱氏（王覽母）']})
        self.assertTrue(all(a['place']['source_name'] == '廬江' and a['place']['modern_identification'] is None for a in moves))

    def test_office_abolition_and_retirement_do_not_close_all_titles_at_death(self):
        titles = read('corpus/jinshu/033-titles.json')['holdings']
        shaofu = next(h for h in titles if h['title'] == '弘訓少府')
        zongzheng = next(h for h in titles if h['title'] == '宗正卿')
        self.assertEqual(shaofu['effective_period']['end']['event_type'], 'abolition')
        self.assertEqual(zongzheng['effective_period']['end']['event_type'], 'renunciation')
        self.assertTrue(all('normalized_date' not in h['effective_period']['end'] for h in titles))
        self.assertFalse(any(h['title'] in ['三公','公府'] for h in titles))
