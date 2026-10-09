import copy
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('validator', ROOT / 'scripts/validate.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)


class IntegrityTests(unittest.TestCase):
    def setUp(self):
        records, errors = v.load_records(ROOT)
        self.assertEqual(errors, [])
        self.records = copy.deepcopy(records)

    def first(self, kind):
        return next(r for r in self.records if r['record_type'] == kind)

    def test_seed_has_valid_evidence(self):
        self.assertEqual(v.validate_records(self.records), [])

    def test_changed_source_requires_new_fingerprint(self):
        self.first('source')['text']['segments'][0]['text'] += '竄入文字'
        self.assertTrue(any('SHA-256' in e for e in v.validate_records(self.records)))

    def test_fabricated_quote_is_rejected(self):
        self.first('assertion_set')['assertions'][0]['evidence'][0]['quote'] = '原文並不存在的引句'
        self.assertTrue(any('引句不在' in e for e in v.validate_records(self.records)))

    def test_unresolved_decision_cannot_choose(self):
        d = next(r for r in self.records if r['record_type'] == 'precedence_decision' and r['status'] == 'unresolved')
        d['preferred_assertion_id'] = d['candidates'][0]
        self.assertTrue(any('未解決定' in e for e in v.validate_records(self.records)))

    def test_precedence_cannot_select_another_predicate(self):
        d = self.first('precedence_decision')
        a = next(a for r in self.records if r['record_type'] == 'assertion_set' for a in r['assertions'] if a['predicate'] == 'name')
        d['candidates'][0] = a['id']
        self.assertTrue(any('超出決定範圍' in e for e in v.validate_records(self.records)))

    def test_identity_cannot_claim_the_same_mention_twice(self):
        d = self.first('identity_decision')
        duplicate = copy.deepcopy(d['groups'][0])
        duplicate['id'] += '-duplicate'
        d['groups'].append(duplicate)
        self.assertTrue(any('另一身份組' in e for e in v.validate_records(self.records)))

    def test_two_lu_women_are_not_merged_by_surname(self):
        d = self.first('identity_decision')
        liu_mother = 's-liuzongyuan-liuzhen-shendaobiao#lady-lu'
        han_wife = 's-huangfushi-hanyu-muzhiming#lady-lu'
        self.assertFalse(any(liu_mother in g['members'] and han_wife in g['members'] for g in d['groups']))

    def test_zhen_is_the_kinship_center_of_his_memorial(self):
        a = next(a for r in self.records if r['record_type'] == 'assertion_set' for a in r['assertions'] if a['id'] == 'a-liuzongyuan-liuzhen-shendaobiao-father-chagong')
        self.assertEqual(a['subject'], 's-liuzongyuan-liuzhen-shendaobiao#liu-zhen')
        self.assertEqual(a['object']['id'], 's-liuzongyuan-liuzhen-shendaobiao#liu-chagong')

    def test_schema_rejects_unknown_record_field(self):
        schema = __import__('json').loads((ROOT / 'schema/records.schema.json').read_text())
        source = self.first('source')
        source['living_person_contact'] = '不應出現'
        self.assertTrue(v.schema_errors(source, schema, schema))


if __name__ == '__main__':
    unittest.main()
