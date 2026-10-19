# coding: utf-8
import json
import unittest
from pathlib import Path
from scripts.family_assemblies import load_assemblies
from scripts.person_bundle import load_catalog, bundle

ROOT = Path(__file__).resolve().parents[1]


class RuanTaoGapFamily(unittest.TestCase):
    def test_four_generations_preserve_three_unknown_people(self):
        catalog = load_catalog(ROOT)
        _, assembled = load_assemblies(ROOT, catalog)
        member = assembled['03n_n2r_8rt_***A']
        self.assertEqual(member['ancestor_person_id'], '03n_n2r_8rt')
        self.assertEqual(member['root_person_id'], '03n_n2r_8rt')
        self.assertEqual(member['generation_distance'], 4)
        self.assertEqual(member['intermediate_person_ids'], [None, None, None])
        self.assertIsNone(member['parent_person_id'])
        self.assertFalse(any(pid in catalog[0] for pid in ['03n_n2r_8rt_*', '03n_n2r_8rt_**', '03n_n2r_8rt_***']))
        assertion = next(a for record in catalog[1] for a in record.get('assertions', [])
                         if a['id'] == member['source_assertion_id'])
        self.assertEqual(assertion['qualifiers']['generation_distance'], member['generation_distance'])
        self.assertEqual(assertion['subject_person_id'], member['person_id'])
        for pid in [member['person_id'], member['ancestor_person_id']]:
            self.assertIn(assertion, bundle(pid, ROOT, catalog=catalog)['relations'])

    def test_source_generation_cannot_be_changed_without_matching_assembly(self):
        people, records = load_catalog(ROOT)
        assertion = next(a for record in records for a in record.get('assertions', [])
                         if a['id'] == 'a-received-032-ruantao-ancestor')
        assertion['qualifiers']['generation_distance'] = 5
        with self.assertRaisesRegex(ValueError, '缺代組裝祖孫端點與來源不符'):
            load_assemblies(ROOT, (people, records))


if __name__ == '__main__':
    unittest.main()
