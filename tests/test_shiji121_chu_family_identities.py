# coding: utf-8
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read(rel):
    return json.loads((ROOT / rel).read_text())

def fixture():
    return read('tests/fixtures/shiji121-chu-family-identities.json')

def assembly_nodes():
    found = {}
    def walk(value):
        if isinstance(value, dict):
            if value.get('person_id') in ['yqp_nlb_p1p_DC', 'yqp_nlb_p1p_DCA']:
                found[value['person_id']] = value
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)
    walk(read('registry/family-assemblies.json'))
    return found

class ChuFamilySourceTests(unittest.TestCase):
    def test_seven_original_markers_keep_exact_text_positions(self):
        self.assertEqual(len(fixture()['mentions']), 7)
        for item in fixture()['mentions']:
            p = next(p for p in read(item['path'])['paragraphs'] if p['id'] == item['paragraph_id'])
            self.assertEqual(p['text'], item['text'])
            self.assertEqual(next(m for m in p['mentions'] if m['id'] == item['marker']['id']), item['marker'])

    def test_two_father_sources_and_existing_assembly_are_retained(self):
        first = next(a for a in read('corpus/shiji/050-assertions.json')['assertions'] if a['id'] == 'a-shiji050-006')
        second = next(a for a in read('corpus/shiji/121-assertions.json')['assertions'] if a['id'] == 'a-shiji121-001')
        for assertion in [first, second]:
            self.assertEqual((assertion['subject_person_id'], assertion['predicate'], assertion['object_person_id']),
                             ('yqp_nlb_p1p_DCA', 'father', 'yqp_nlb_p1p_DC'))
        nodes = assembly_nodes()
        self.assertEqual(nodes['yqp_nlb_p1p_DCA']['source_assertion_id'], 'a-shiji050-006')
        self.assertEqual(nodes['yqp_nlb_p1p_DCA']['parent_person_id'], 'yqp_nlb_p1p_DC')
        self.assertEqual(nodes['yqp_nlb_p1p_DC']['parent_person_id'], 'yqp_nlb_p1p_D')

    def test_shengong_homonyms_remain_distinct_and_teacher_is_not_parent(self):
        people = {p['id']: p for p in read('registry/persons.json')['persons']}
        self.assertIn('wxo_k8i_1it', people)
        self.assertIn('4d0_phq_cjk', people)  # 申公巫臣
        self.assertIn('6wx_fr3_b2e_A', people)  # 陳申公
        self.assertFalse(set(fixture()['mapping']) & set(people))
        assertions = read('corpus/shiji/121-assertions.json')['assertions']
        self.assertFalse(any(a['predicate'] in ['father', 'mother'] and 'wxo_k8i_1it' in
                             [a['subject_person_id'], a['object_person_id']] for a in assertions))

    def test_three_identity_decisions_have_subject_mentions_and_no_false_review(self):
        chapter = read('corpus/shiji/121-identities.json')
        rows = [d for d in chapter['decisions'] if d['id'].startswith('d-shiji121-chu-family-')]
        self.assertEqual(len(rows), 3)
        for d in rows:
            self.assertFalse(d['human_reviewed'])
            self.assertIsNone(d['model'])
            self.assertEqual(set(d['chapter_ids']), {'c-shiji-121-rulin', 'c-shiji-050-chuyuan'})
        names = {n['person_id']: n for n in read('data/corpus/profile-names.json')['records']}
        self.assertEqual((names['yqp_nlb_p1p_DC']['title'], names['yqp_nlb_p1p_DC']['surname'], names['yqp_nlb_p1p_DC']['ming']), ('楚夷王', '劉', '郢'))
        child = names['yqp_nlb_p1p_DCA']
        self.assertEqual((child['title'], child['surname'], child['ming']), ('楚王', '劉', '戊'))
        surname = next(e for e in child['component_evidence'] if 'surname' in e['field_names'])
        self.assertEqual(surname['basis'], 'documented_paternal_lineage_context')
        self.assertEqual(surname['source_assertion_id'], 'a-shiji050-006')

class ChuFamilyPublicProfileTests(unittest.TestCase):
    def test_retired_profiles_are_removed_and_each_person_has_both_chapters(self):
        for old, current in fixture()['mapping'].items():
            self.assertFalse((ROOT / 'data/corpus/profiles' / (old + '.json')).exists())
            self.assertFalse((ROOT / 'exports/persons' / (old + '.json')).exists())
            profile = read('data/corpus/profiles/' + current + '.json')
            chapters = {o['chapter_id'] for o in profile['occurrences']}
            self.assertTrue({'c-shiji-121-rulin', 'c-shiji-050-chuyuan'}.issubset(chapters))

    def test_selected_json_parent_and_two_source_relations_are_parseable(self):
        profile = read('data/corpus/profiles/yqp_nlb_p1p_DCA.json')
        fathers = [r for r in profile['preferred_relations'] if r['predicate'] == 'father' and r['subject_person_id'] == profile['id']]
        self.assertEqual({r['object_person_id'] for r in fathers}, {'yqp_nlb_p1p_DC'})
        self.assertTrue({'a-shiji050-006', 'a-shiji121-001'}.issubset({r['id'] for r in profile['relations']}))
        parent = read('data/corpus/profiles/yqp_nlb_p1p_DC.json')
        self.assertEqual({r['object_person_id'] for r in parent['preferred_relations'] if r['predicate'] == 'father' and r['subject_person_id'] == parent['id']}, {'yqp_nlb_p1p_D'})

if __name__ == '__main__':
    unittest.main()
