"""Declining an offered office and immediate reassignment is not service."""
import copy
import json
from pathlib import Path
import unittest
from scripts.unassumed_appointments import unassumed_appointment_valid
from scripts.validate_corpus import title_proposal_errors, normalized_date_errors
DATA = json.loads((Path(__file__).parent/'fixtures/declined-reassignment.json').read_text())
class DeclinedReassignmentTests(unittest.TestCase):
    def setUp(self):
        self.c = copy.deepcopy(DATA['chapter'])
        self.q = copy.deepcopy(DATA['proposals'][0])
    def valid(self):
        return unassumed_appointment_valid(self.q, self.c)
    def test_both_offices_remain_unassumed(self):
        for q in DATA['proposals']:
            self.assertTrue(unassumed_appointment_valid(q, self.c))
            self.assertEqual(title_proposal_errors(q, self.c, {q['person_id']}), [])
            self.assertEqual(q['outcome'], 'not_assumed')
    def test_absent_reassignment_context_rejected(self):
        del self.q['declined_reassignment_context']
        self.assertFalse(self.valid())
    def test_other_recipient_rejected(self):
        self.q['person_id'] = 'other'
        self.assertFalse(self.valid())
    def test_other_office_rejected(self):
        self.q['title'] = '太府卿'
        self.assertFalse(self.valid())
    def test_refusal_span_change_rejected(self):
        self.q['non_assumption_anchor']['end'] -= 1
        self.assertFalse(self.valid())
    def test_missing_coordinated_office_rejected(self):
        self.q['declined_reassignment_context']['title_anchors'].pop()
        self.assertFalse(self.valid())
    def test_replacement_not_a_reassignment_rejected(self):
        self.q['declined_reassignment_context']['replacement_appointment_anchor']['surface'] = '復任光祿大夫'
        self.assertFalse(self.valid())
    def test_changed_subject_inside_office_clause_rejected(self):
        p = self.c['paragraphs'][4]
        p['mentions'].append({'id':'synthetic-other', 'start':168, 'end':169,
                              'surface':p['text'][168:169], 'kind':'person', 'person_id':'other'})
        self.assertFalse(self.valid())
    def test_years_and_no_derived_birth(self):
        for q in DATA['proposals']:
            self.assertEqual(normalized_date_errors(q['normalized_date'], {self.c['id']:self.c}), [])
            self.assertEqual(q['normalized_date']['year'], 546)
        e = DATA['death_event']
        self.assertEqual(e['normalized_date']['year'], 549)
        self.assertEqual(normalized_date_errors(e['normalized_date'], {self.c['id']:self.c}), [])
        self.assertEqual(e['event_type'], 'death')
if __name__ == '__main__': unittest.main()
