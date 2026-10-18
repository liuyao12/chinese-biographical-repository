import copy
import hashlib
import json
import unittest
from pathlib import Path
from scripts.biographical_kinship import child_continuation_errors, digital_paratext_errors
from scripts.uncle_parentage import parent_through_paternal_uncle_valid, explicit_maternal_uncle_valid
from scripts.person_bundle import load_catalog
from scripts.family_assemblies import load_assemblies

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads((ROOT / path).read_text())


class XieRoots079(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c = read('corpus/jinshu/079.json')
        cls.people = {p['label']: p['id'] for p in read('registry/persons.json')['persons']}
        cls.rels = read('corpus/jinshu/079-assertions.json')['assertions']
        cls.assertions = {a['id']: a for a in cls.rels}
        cls.family = next(a for a in read('registry/family-assemblies.json')['assemblies']
                          if a['id'] == 'family-chenjun-xie-lang')
        cls.rows = {m['person_id']: m for m in cls.family['members']}
        cls.paragraphs = {p['id']: (cls.c['id'], p) for p in cls.c['paragraphs']}

    def test_uncle_derived_parent_remains_inference_with_three_primary_proofs(self):
        member = self.rows[self.people['謝據']]
        self.assertTrue(parent_through_paternal_uncle_valid(member, self.rows, self.assertions, {self.c['id']: self.c}))
        self.assertIsNone(member['source_assertion_id'])
        self.assertEqual(member['parent_person_id'], self.people['謝裒'])
        self.assertFalse(any(a['predicate'] == 'father' and a['subject_person_id'] == self.people['謝據'] for a in self.rels))
        bad = copy.deepcopy(self.assertions)
        uncle_id = member['parent_connection']['nephew_uncle_assertion_id']
        bad[uncle_id]['predicate'] = 'maternal_uncle'
        self.assertFalse(parent_through_paternal_uncle_valid(member, self.rows, bad, {self.c['id']: self.c}))
        bad = copy.deepcopy(member); bad['parent_connection']['human_reviewed'] = True
        self.assertFalse(parent_through_paternal_uncle_valid(bad, self.rows, self.assertions, {self.c['id']: self.c}))

    def test_uncle_inference_rejects_conflicting_father_or_wrong_nephew(self):
        member = self.rows[self.people['謝據']]
        bad = copy.deepcopy(self.assertions)
        bad['conflict'] = dict(predicate='father', subject_person_id=self.people['謝據'], object_person_id=self.people['王濛'])
        self.assertFalse(parent_through_paternal_uncle_valid(member, self.rows, bad, {self.c['id']: self.c}))
        bad = copy.deepcopy(member); bad['parent_connection']['nephew_person_id'] = self.people['謝絢']
        self.assertFalse(parent_through_paternal_uncle_valid(bad, self.rows, self.assertions, {self.c['id']: self.c}))

    def test_son_continuation_crosses_only_recorded_digital_headings(self):
        a = next(a for a in self.rels if 'context' in a)
        self.assertEqual(child_continuation_errors(a, self.c), [])
        bad = copy.deepcopy(self.c)
        bad['source']['normalization']['omitted_digital_paratext'] = []
        self.assertTrue(child_continuation_errors(a, bad))
        bad = copy.deepcopy(self.c)
        bad['source']['normalization']['omitted_digital_paratext'][1]['source_revision'] += 1
        self.assertTrue(child_continuation_errors(a, bad))
        self.assertTrue(all('=' not in p['text'] for p in self.c['paragraphs']))

    def test_heading_metadata_cannot_hide_prose_even_with_recomputed_hash(self):
        self.assertEqual(digital_paratext_errors(self.c), [])
        for raw in ['父裒\n', '====朗子 重====\n另有未錄傳文']:
            bad = copy.deepcopy(self.c)
            e = bad['source']['normalization']['omitted_digital_paratext'][1]
            e['raw_quote'] = raw; e['raw_quote_sha256'] = hashlib.sha256(raw.encode()).hexdigest()
            self.assertTrue(digital_paratext_errors(bad))
        bad = copy.deepcopy(self.c)
        e = bad['source']['normalization']['omitted_digital_paratext'][1]
        e['source_lines'] = [125, 126]
        self.assertTrue(digital_paratext_errors(bad))

    def test_mother_and_maternal_grandfather_belong_to_different_generations(self):
        mothers = [a for a in self.rels if a['predicate'] == 'mother']
        self.assertEqual([(a['subject_person_id'], a['object_person_id']) for a in mothers],
                         [(self.people['謝朗'], self.people['王氏（謝朗母）'])])
        grand = next(a for a in self.rels if a['predicate'] == 'grandfather')
        self.assertEqual((grand['subject_person_id'], grand['object_person_id']),
                         (self.people['謝重'], self.people['王胡之']))
        self.assertEqual(grand['qualifiers']['lineage'], 'maternal')
        self.assertIsNone(grand['qualifiers']['mother_person_id'])
        self.assertNotIn(self.people['王胡之'], self.rows)
        self.assertNotIn(self.people['王氏（謝朗母）'], self.rows)

    def test_two_generations_of_uncles_keep_distinct_persons_and_source_anchors(self):
        uncles = [a for a in self.rels if a['predicate'] == 'maternal_uncle']
        self.assertEqual({(a['subject_person_id'], a['object_person_id']) for a in uncles},
                         {(self.people['謝絢'], self.people['袁湛']),
                          (self.people['謝重'], self.people['謝重之舅（未名）'])})
        for a in uncles:
            self.assertTrue(explicit_maternal_uncle_valid(a, self.paragraphs))
            bad = copy.deepcopy(a)
            bad['object_person_id'] = self.people['王胡之']
            self.assertFalse(explicit_maternal_uncle_valid(bad, self.paragraphs))
        p = self.c['paragraphs'][-1]
        mentions = [m for m in p['mentions'] if m['surface'] == '舅']
        self.assertEqual(len(mentions), 2)
        self.assertEqual({m['person_id'] for m in mentions}, {self.people['謝重之舅（未名）']})

    def test_complete_name_huzhi_is_not_misparsed_as_possessive(self):
        p = self.c['paragraphs'][-1]
        m = next(m for m in p['mentions'] if m['person_id'] == self.people['王胡之'])
        self.assertEqual(m['surface'], '王胡之')
        name = next(n for n in read('data/corpus/profile-names.json')['records']
                    if n['person_id'] == self.people['王胡之'])
        self.assertEqual((name['surname'], name['ming']), ('王', '胡之'))
        self.assertFalse(any(a['predicate'] == 'mother' and a['subject_person_id'] == self.people['謝重'] for a in self.rels))

    def test_langlun_is_not_a_person_mention(self):
        p = next(p for p in self.c['paragraphs'] if '支遁朗論' in p['text'])
        at = p['text'].index('朗論')
        self.assertFalse(any(m['start'] <= at < m['end'] for m in p['mentions']))
        self.assertTrue(any(m['surface'] == '支遁' for m in p['mentions']))

    def test_death_is_father_ju_and_terminal_office_is_not_a_death_date(self):
        events = read('corpus/jinshu/079-life-events.json')['events']
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]['person_id'], self.people['謝據'])
        self.assertIsNone(events[0]['date_expression'])
        self.assertNotIn('normalized_date', events[0])
        self.assertFalse(any(a['person_id'] == self.people['謝朗'] for a in events))
        title = next(h for h in read('corpus/jinshu/079-titles.json')['holdings'] if h['person_id'] == self.people['謝朗'])
        self.assertEqual(title['title'], '東陽太守')
        self.assertEqual(title['effective_period']['end']['status'], 'unknown')

    def test_wang_meng_canonical_label_preserves_received_meng_spelling(self):
        person = self.people['王濛']
        mentions = [m for p in self.c['paragraphs'] for m in p['mentions']
                    if m.get('person_id') == person]
        self.assertTrue(any(m['surface'] == '王蒙' for m in mentions))
        self.assertTrue(any(m['surface'] == '蒙' for m in mentions))
        self.assertFalse(any(m['surface'] == '王濛' for m in mentions))
        names = next(n for n in read('data/corpus/profile-names.json')['records']
                     if n['person_id'] == person)
        self.assertEqual(names['ming'], '濛')

    def test_selected_tree_traces_new_ancestors_and_keeps_siblings(self):
        _, assembled = load_assemblies(ROOT, load_catalog(ROOT))
        for child, parent in [('謝安', '謝裒'), ('謝據', '謝裒'), ('謝朗', '謝據'),
                              ('謝重', '謝朗'), ('謝晦', '謝重'), ('謝絢', '謝重')]:
            self.assertEqual(assembled[self.people[child]]['parent_person_id'], self.people[parent])
        self.assertEqual(len(self.rows), 8)
        self.assertNotIn(self.people['謝玄'], self.rows)
        self.assertNotIn(self.people['謝尚'], self.rows)
        self.assertEqual(assembled[self.people['王修']]['parent_person_id'], self.people['王濛'])
        self.assertNotEqual(assembled[self.people['王濛']]['root_person_id'], self.people['王仁'])


if __name__ == '__main__':
    unittest.main()
