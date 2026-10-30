import copy
import json
import unittest
from pathlib import Path
from unittest.mock import patch
from scripts.fixed_zhou041_wangbao import proof, guard_bundle, CH
from scripts.zhou041_wangbao_profile_facts import source_records, REF
from scripts.person_bundle import load_catalog
from scripts.preferred_name_components import validated_readings

ROOT = Path(__file__).resolve().parents[1]

class WangBaoProfileFacts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter, cls.source, cls.roles = proof(ROOT)
        cls.people, cls.records = load_catalog(ROOT)
        cls.expected = source_records(ROOT, cls.chapter, cls.roles)

    def overlay(self, changes):
        original_text, original_bytes = Path.read_text, Path.read_bytes
        def raw(p):
            rel = str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else None
            return json.dumps(changes[rel], ensure_ascii=False).encode() if rel in changes else None
        from contextlib import ExitStack
        stack = ExitStack()
        stack.enter_context(patch.object(Path, 'read_text', lambda p, *a, **kw: raw(p).decode() if raw(p) is not None else original_text(p, *a, **kw)))
        stack.enter_context(patch.object(Path, 'read_bytes', lambda p: raw(p) if raw(p) is not None else original_bytes(p)))
        return stack

    def test_literal_variants_and_source_scoped_reading(self):
        names = [n for r in self.records if r.get('record_type') == 'person_name_component_set' for n in r['records']]
        rows = [n for n in names if n['person_id'] == self.roles['$bao']]
        self.assertEqual({(n['ming'], n.get('zi')) for n in rows}, {('褒', '子漢'), ('褒', '子淵'), ('襃', '子淵')})
        chapters = {r['id']: r for r in self.records if r.get('record_type') == 'marked_chapter'}
        selected = validated_readings(self.records, names, chapters, [self.roles['$bao']], root=ROOT)
        self.assertEqual(selected[0]['preferred_value'], '褒')
        self.assertEqual(len(selected[0]['records']), 3)
        self.assertEqual(selected[0]['field'], 'ming')

    def test_unknown_dates_and_age_do_not_create_birth_or_death_place(self):
        age = self.chapter['annotation']['age_assertions'][0]
        self.assertEqual(age['value'], 64)
        self.assertEqual(age['counting'], 'unspecified_source_age')
        self.assertIsNone(age['birth_year'])
        event = next(r['events'][0] for r in self.expected.values() if r['record_type'] == 'person_life_event_assertion_set')
        self.assertIsNone(event['date_expression'])
        self.assertNotIn('normalized_date', event)
        addresses = next(r['assertions'] for r in self.expected.values() if r['record_type'] == 'person_address_assertion_set')
        self.assertEqual([(a['relation'], a['place']['source_name']) for a in addresses], [('biographical_origin', '琅邪臨沂')])
        self.assertEqual(age['age_context']['life_event_id'], event['id'])

    def test_changed_age_birth_and_calendar_inference_rejected(self):
        for field, value in [('value', 65), ('birth_year', 513), ('counting', 'traditional_nominal_age')]:
            ch = copy.deepcopy(self.chapter)
            ch['annotation']['age_assertions'][0][field] = value
            with self.overlay({CH: ch}), self.assertRaises(AssertionError):
                proof(ROOT)
        ch = copy.deepcopy(self.chapter)
        ch['annotation']['age_assertions'][0]['normalized_date'] = {'year': 576}
        with self.overlay({CH: ch}), self.assertRaises(AssertionError):
            proof(ROOT)

    def test_wrong_deceased_parent_name_or_origin_rejected(self):
        mutations = [
            ('person_life_event_assertion_set', lambda r: r['events'][0].update(person_id=self.roles['$zi'])),
            ('person_assertion_set', lambda r: r['assertions'][0].update(object_person_id=self.roles['$gui'])),
            ('person_name_component_set', lambda r: r['records'][0].update(zi='子漢')),
            ('person_name_component_set', lambda r: r['records'][0].update(surname='周')),
            ('person_address_assertion_set', lambda r: r['assertions'][0].update(relation='death_place')),
        ]
        for kind, mutate in mutations:
            rel, record = next((rel, copy.deepcopy(r)) for rel, r in self.expected.items() if r['record_type'] == kind)
            mutate(record)
            with self.overlay({rel: record}), self.assertRaises(AssertionError):
                proof(ROOT)

    def test_explicit_child_corroborates_existing_source_not_succession_alone(self):
        a = next(r['assertions'][0] for r in self.expected.values() if r['record_type'] == 'person_assertion_set')
        self.assertEqual(a['qualifiers']['source_term'], '子鼒')
        self.assertEqual(a['subject_person_id'], self.roles['$zi'])
        self.assertEqual(a['object_person_id'], self.roles['$bao'])
        old = [a for r in self.records if r.get('record_type') == 'person_assertion_set' for a in r['assertions'] if a['id'] == 'a-xintang072-wyd-zi_sui-father']
        self.assertEqual(len(old), 1)
        self.assertEqual((old[0]['subject_person_id'], old[0]['object_person_id']), (a['subject_person_id'], a['object_person_id']))
        self.assertNotIn('birth_order', a['qualifiers'])
        self.assertNotIn('title_holding_id', a['qualifiers'])

    def test_caller_omission_and_reverse_loss_do_not_hide_installed_owner(self):
        for expected in self.expected.values():
            records = [r for r in self.records if r != expected]
            with self.assertRaises(AssertionError):
                guard_bundle(ROOT, self.roles['$bao'], self.people, records)
        people = copy.deepcopy(self.people)
        target = people[self.roles['$bao']]
        target['evidence'] = [e for e in target['evidence'] if e.get('chapter_id') != self.chapter['id']]
        records = [r for r in self.records if r not in self.expected.values()]
        with self.assertRaises(AssertionError):
            guard_bundle(ROOT, self.roles['$bao'], people, records)

    def test_changed_reading_cannot_omit_known_name_record(self):
        rel, r = next((p, copy.deepcopy(v)) for p, v in self.expected.items() if v['record_type'] == 'preferred_name_component_reading_set')
        r['readings'][0]['records'].pop()
        with self.overlay({rel: r}), self.assertRaises(AssertionError):
            proof(ROOT)

    def test_source_contract_and_raw_capture_remain_original(self):
        import hashlib
        base = self.source
        self.assertEqual(hashlib.sha256((ROOT / base['raw_file']).read_bytes()).hexdigest(), base['raw_sha256'])
        self.assertEqual(hashlib.sha256((ROOT / 'source-evidence/zhou041-wangbao-ws2432538/source-ner-contract.json').read_bytes()).hexdigest(), '3e6008028d663e86ca0a1a2b114f584268d88a1d858dbfc03fa5a211e585149e')
        ch = copy.deepcopy(self.chapter)
        del ch['annotation']['profile_facts_ref']
        del ch['annotation']['age_assertions']
        with self.overlay({CH: ch}), self.assertRaises(AssertionError):
            proof(ROOT)

if __name__ == '__main__':
    unittest.main()
