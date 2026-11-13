import json
import unittest
from pathlib import Path

from scripts.person_bundle import ROOT, load_catalog
from scripts.family_assemblies import load_assemblies


class Jinshu054LuFamilyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = json.loads((ROOT / 'corpus/jinshu/054-lu-family.json').read_text())
        cls.facts = json.loads((ROOT / 'corpus/jinshu/054-lu-family-assertions.json').read_text())['assertions']
        cls.source_map, cls.assembled = load_assemblies(ROOT, load_catalog(ROOT))
        cls.assembly = next(a for a in json.loads((ROOT / 'registry/family-assemblies.json').read_text())['assemblies'] if a['id'] == 'family-jinshu054-lu-xun')

    def test_fixed_witness_is_qualified_and_partial(self):
        source = self.chapter['source']
        self.assertEqual(source['revision_id'], 2605147)
        self.assertFalse(source['image_verified'])
        self.assertEqual(source['text_scope'], 'partial_chapter')
        self.assertIn('底本未明', source['edition'])
        self.assertIn('CC BY-SA 4.0', source['rights'])
        self.assertFalse(self.chapter['annotation']['human_reviewed'])

    def test_explicit_kinship_edges_remain_distinct(self):
        by_id = {a['id']: a for a in self.facts}
        self.assertEqual((by_id['a-jin054-lu-ji-father-kang']['subject_person_id'],
                         by_id['a-jin054-lu-ji-father-kang']['object_person_id']),
                         ('69h_uhy_hta', '8kb_zhi_yt3_A'))
        self.assertEqual((by_id['a-jin054-lu-ji-grandfather-xun']['subject_person_id'],
                         by_id['a-jin054-lu-ji-grandfather-xun']['object_person_id']),
                         ('69h_uhy_hta', '8kb_zhi_yt3'))
        self.assertFalse(any(a['predicate'] == 'father' and a['subject_person_id'] == '8kb_zhi_yt3_A'
                             and a['object_person_id'] == '8kb_zhi_yt3' for a in self.facts))
        kang = next(m for m in self.assembly['members'] if m['person_id'] == '8kb_zhi_yt3_A')
        self.assertEqual(kang['parent_connection']['type'], 'parent_between_consecutive_ancestors')
        self.assertEqual(self.source_map['69h_uhy_hta']['person_id'], '8kb_zhi_yt3_AA')
        self.assertIsNone(kang['source_assertion_id'])

    def test_generated_family_and_source_profiles_keep_human_names_and_canonical_ids(self):
        family_profile = json.loads((ROOT / 'data/corpus/profiles/8kb_zhi_yt3_AA.json').read_text())
        source_profile = json.loads((ROOT / 'data/corpus/profiles/69h_uhy_hta.json').read_text())
        self.assertEqual((family_profile['label'], family_profile['canonical_person_id']), ('陸機', '8kb_zhi_yt3_AA'))
        self.assertEqual(source_profile['canonical_person_id'], '69h_uhy_hta')

    def test_sibling_direction_children_and_all_excerpt_mentions(self):
        by_id = {a['id']: a for a in self.facts}
        yun = by_id['a-jin054-lu-yun-younger-brother-ji']
        self.assertEqual((yun['subject_person_id'], yun['object_person_id']), ('8kb_zhi_yt3_AB', '69h_uhy_hta'))
        self.assertEqual(yun['qualifiers']['older_person_id'], '69h_uhy_hta')
        children = [a for a in self.facts if a['predicate'] == 'father' and a['object_person_id'] == '69h_uhy_hta']
        self.assertEqual({a['subject_person_id'] for a in children}, {'8kb_zhi_yt3_AAA', '8kb_zhi_yt3_AAB'})
        mentions = [m for p in self.chapter['paragraphs'] for m in p['mentions']]
        self.assertEqual(sum(m['surface'] == '雲' and m['person_id'] == '8kb_zhi_yt3_AB' for m in mentions), 3)
        self.assertEqual(self.chapter['annotation']['age_assertions'][0]['value'], 43)
        self.assertIsNone(self.chapter['annotation']['age_assertions'][0]['birth_year'])


if __name__ == '__main__':
    unittest.main()
