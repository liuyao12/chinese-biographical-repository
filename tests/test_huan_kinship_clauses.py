"""Source-clause guards must survive family ID changes without broadening claims."""
import copy
import json
from pathlib import Path
import unittest

from scripts.huan_kinship_clauses import mother_valid, cousin_valid

ROOT = Path(__file__).resolve().parents[1]


class HuanKinshipClauses(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.paragraphs = {}
        cls.assertions = []
        for name in ('074-huan-family', '098-huanwen', '099-huanxuan'):
            chapter = json.loads((ROOT / f'corpus/jinshu/{name}.json').read_text())
            cls.paragraphs.update({p['id']: (chapter['id'], p) for p in chapter['paragraphs']})
            facts = json.loads((ROOT / f'corpus/jinshu/{name}-assertions.json').read_text())
            cls.assertions.extend(a for a in facts['assertions']
                                  if a['id'] in {f'a-huan-close-{n:03d}' for n in (41, 42, 43, 58, 59)})

    def valid(self, assertion, paragraphs=None):
        function = mother_valid if assertion['predicate'] == 'maternal_role' else cousin_valid
        return function(assertion, self.paragraphs if paragraphs is None else paragraphs)

    def test_complete_received_contexts(self):
        self.assertEqual(len(self.assertions), 5)
        for assertion in self.assertions:
            self.assertTrue(self.valid(assertion), assertion['id'])

    def test_reversed_people_and_wrong_anchor_identity_rejected(self):
        for assertion in self.assertions:
            bad = copy.deepcopy(assertion)
            bad['subject_person_id'], bad['object_person_id'] = bad['object_person_id'], bad['subject_person_id']
            self.assertFalse(self.valid(bad))
            paragraphs = copy.deepcopy(self.paragraphs)
            evidence = assertion['evidence'][0]
            paragraph = paragraphs[evidence['paragraph_id']][1]
            mention = next(m for m in paragraph['mentions'] if m['id'] == evidence['subject_person_mention_id'])
            mention['person_id'] = 'another-person'
            self.assertFalse(self.valid(assertion, paragraphs))

    def test_truncated_quote_or_shifted_binding_rejected(self):
        for assertion in self.assertions:
            bad = copy.deepcopy(assertion)
            bad['evidence'][0]['quote'] = bad['evidence'][0]['quote'][1:]
            self.assertFalse(self.valid(bad))
            bad = copy.deepcopy(assertion)
            bad['qualifiers']['source_clause_binding']['start'] += 1
            self.assertFalse(self.valid(bad))

    def test_mother_is_not_automatically_birth_mother_or_father(self):
        for assertion in self.assertions:
            if assertion['predicate'] != 'maternal_role':
                continue
            for key, value in (('biological_mother', True), ('father_person_id', assertion['subject_person_id'])):
                bad = copy.deepcopy(assertion)
                bad['qualifiers'][key] = value
                self.assertFalse(mother_valid(bad, self.paragraphs))

    def test_cousin_distance_and_order_cannot_be_invented(self):
        for assertion in self.assertions:
            if assertion['predicate'] != 'agnatic_cousin':
                continue
            bad = copy.deepcopy(assertion)
            bad['qualifiers']['kinship_structure']['distance'] = 2
            self.assertFalse(cousin_valid(bad, self.paragraphs))
            bad = copy.deepcopy(assertion)
            order = bad['qualifiers']['relative_birth_order']
            order['older_person_id'], order['younger_person_id'] = order['younger_person_id'], order['older_person_id']
            self.assertFalse(cousin_valid(bad, self.paragraphs))


if __name__ == '__main__':
    unittest.main()
