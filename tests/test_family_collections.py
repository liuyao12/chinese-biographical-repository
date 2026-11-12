"""Rootless family collection groups trees without inventing parent edges."""
import copy
import json
from pathlib import Path
import unittest

from scripts.family_collections import validate, collection_person_ids, write_public_index
from scripts.person_bundle import bundle
from scripts.validate_corpus import family_collection_errors

ROOT = Path(__file__).resolve().parents[1]
COLLECTION_ID = 'family-collection-langye-wang-dao-dun'


class FamilyCollectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / 'registry/family-collections.json').read_text())
        cls.collection = next(c for c in cls.data['collections'] if c['id'] == COLLECTION_ID)

    def test_contains_wang_dao_tree_and_wang_dun_original_id(self):
        validate(self.data, ROOT)
        ids = collection_person_ids(self.data, ROOT, COLLECTION_ID)
        assembly_doc = json.loads((ROOT / 'registry/family-assemblies.json').read_text())
        assembly = next(a for a in assembly_doc['assemblies'] if a['id'] == 'family-langye-wang-dao')
        self.assertEqual(ids, {m['person_id'] for m in assembly['members']} | {'39o_b6y_n74'})
        self.assertIn('7r6_k52_qji_ABAA', ids)
        self.assertIn('39o_b6y_n74', ids)
        self.assertEqual(self.collection['branches'][0]['entry_person_id'], '7r6_k52_qji_ABAA')
        self.assertEqual(self.collection['standalone_members'][0]['person_id'], '39o_b6y_n74')

    def test_assertion_and_exact_quote_are_resolved(self):
        validate(self.data, ROOT)
        relation = self.collection['relationships'][0]
        assertions = json.loads((ROOT / 'corpus/jinshu/065-assertions.json').read_text())['assertions']
        assertion = next(a for a in assertions if a['id'] == relation['assertion_id'])
        self.assertEqual((relation['subject_person_id'], relation['object_person_id']),
                         (assertion['subject_person_id'], assertion['object_person_id']))
        self.assertEqual(assertion['qualifiers']['source_term'], '從兄敦')
        self.assertIn('謂其從兄敦曰', assertion['evidence'][0]['quote'])

    def test_wrong_relation_endpoint_is_rejected(self):
        data = copy.deepcopy(self.data)
        data['collections'][0]['relationships'][0]['object_person_id'] = 'not-the-source-person'
        with self.assertRaises(AssertionError):
            validate(data, ROOT)

    def test_full_corpus_validator_hook_rejects_malformed_collection(self):
        data = copy.deepcopy(self.data)
        data['collections'][0]['relationships'][0]['object_person_id'] = 'not-the-source-person'
        errors = family_collection_errors(ROOT, data)
        self.assertTrue(any('家族集合驗證失敗' in error for error in errors), errors)

    def test_invented_parent_or_common_ancestor_is_rejected(self):
        data = copy.deepcopy(self.data)
        data['collections'][0]['standalone_members'][0]['father_person_id'] = '7r6_k52_qji'
        with self.assertRaises(AssertionError):
            validate(data, ROOT)
        data = copy.deepcopy(self.data)
        data['collections'][0]['relationships'][0]['common_ancestor_person_id'] = '7r6_k52_qji'
        with self.assertRaises(AssertionError):
            validate(data, ROOT)

    def test_json_schema_pattern_and_integer_version_are_enforced(self):
        data = copy.deepcopy(self.data)
        data['collections'][0]['id'] = 'family-collection-王氏'
        with self.assertRaises(AssertionError):
            validate(data, ROOT)
        data = copy.deepcopy(self.data)
        data['schema_version'] = True
        with self.assertRaises(AssertionError):
            validate(data, ROOT)

    def test_public_index_and_each_person_bundle_expose_rootless_collection(self):
        write_public_index(ROOT)
        index = json.loads((ROOT / 'data/corpus/family-collection-index.json').read_text())
        self.assertEqual(index['record_type'], 'family_collection_index')
        for pid in ('7r6_k52_qji_ABAA', '39o_b6y_n74'):
            self.assertIn(COLLECTION_ID, index['by_person_id'][pid])
            person = bundle(pid, root=ROOT, include_provisional=True)
            group = next(c for c in person['family_collections'] if c['id'] == COLLECTION_ID)
            self.assertIn(pid, group['person_ids'])
            self.assertFalse(group['relationships'][0]['parent_edge'])
            self.assertEqual(group['relationships'][0]['assertion_id'], 'a-jinshu065-wang-003')
            source_relation = next(r for r in person['relations'] if r['id'] == 'a-jinshu065-wang-003')
            self.assertEqual(source_relation['evidence'][0]['source_id'], 's-jinshu-065-wangdao-family')
            self.assertIn('謂其從兄敦曰', source_relation['evidence'][0]['quote'])


if __name__ == '__main__':
    unittest.main()
