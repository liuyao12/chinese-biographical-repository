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
