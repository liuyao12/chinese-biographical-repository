import unittest
from scripts.person_bundle import bundle


class PersonBundleTests(unittest.TestCase):
    def test_real_person_has_reverse_relations_and_source_text(self):
        result = bundle('cbr-p004938')
        self.assertTrue(any(a['object_person_id'] == 'cbr-p004938' for a in result['relations']))
        self.assertTrue(result['title_holdings'])
        passages = {p['id']: p for p in result['passages']}
        for title in result['title_holdings']:
            for evidence in title['evidence']:
                self.assertEqual(evidence['quote'], passages[evidence['paragraph_id']]['text'])
        self.assertTrue(result['time_policy']['unknown_is_not_unbounded'])

    def test_provisional_equivalence_is_explicit(self):
        exact = bundle('cbr-p000537')
        combined = bundle('cbr-p000537', include_provisional=True)
        self.assertEqual(exact['person_ids'], ['cbr-p000537'])
        self.assertIn('cbr-p004868', combined['person_ids'])
        self.assertTrue(combined['equivalence_decisions'])
        self.assertGreater(len(combined['mentions']), len(exact['mentions']))

    def test_unknown_person_rejected(self):
        with self.assertRaises(ValueError):
            bundle('missing')

    def test_birth_order_is_structured_and_keeps_uncertainty(self):
        result = bundle('cbr-p000533')
        constraints = {c['assertion_id']: c for c in result['birth_order_constraints']}
        eldest = constraints['a-shiji006-005']
        self.assertEqual(eldest['ordinal'], 1)
        self.assertEqual(eldest['scope'], 'sons_of_parent')
        self.assertEqual(eldest['parent_person_id'], 'cbr-p000533')
        younger = constraints['a-shiji006-006']
        self.assertIsNone(younger['ordinal'])
        self.assertEqual(younger['interpretation_status'], 'ambiguous')
        relative = constraints['a-shiji006-004']
        self.assertEqual(relative['older_person_id'], 'cbr-p000533')
        self.assertEqual(relative['younger_person_id'], 'cbr-p000543')
        self.assertIsNone(relative['older_ordinal'])
        self.assertIsNone(relative['younger_ordinal'])
        self.assertTrue(relative['evidence'])

    def test_native_place_keeps_source_and_unknown_geography(self):
        result = bundle('cbr-p005166')
        address = result['address_assertions'][0]
        self.assertEqual(address['relation'], 'biographical_origin')
        self.assertEqual(address['place']['source_name'], '豐')
        self.assertIsNone(address['place']['place_id'])
        self.assertIsNone(address['place']['modern_identification'])
        passages = {p['id']: p for p in result['passages']}
        evidence = address['evidence'][0]
        self.assertEqual(evidence['quote'], passages[evidence['paragraph_id']]['text'])

    def test_birth_death_and_burial_places_are_separate(self):
        result = bundle('cbr-p000533')
        addresses = {a['relation']: a for a in result['address_assertions']}
        self.assertEqual(addresses['birth_place']['place']['source_name'], '邯鄲')
        self.assertEqual(addresses['death_place']['place']['source_name'], '沙丘平臺')
        self.assertEqual(addresses['burial_place']['place']['source_name'], '酈邑')
        self.assertNotIn('biographical_origin', addresses)
        for a in addresses.values():
            self.assertIsNone(a['place']['modern_identification'])
            self.assertTrue(a['evidence'])
