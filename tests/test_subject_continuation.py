import copy
import unittest
from scripts.subject_continuation import prior_subject_valid, title_attestation_subject_valid


def fixture():
    # Synthetic omitted-subject passage, never exported as historical data.
    chapter = {'id': 'c', 'source_id': 's', 'paragraphs': [
        {'id': 'p0', 'text': '甲任職。', 'mentions': [{'id': 'm', 'person_id': 'a', 'kind': 'person', 'start': 0, 'end': 1}],
         'source_position': {'first_line': 10, 'last_line': 11, 'editorial_excerpt_boundary': True}},
        {'id': 'p1', 'text': '遷太守，年六十。', 'mentions': [],
         'source_position': {'first_line': 12, 'last_line': 13, 'editorial_excerpt_boundary': True}}]}
    context = {'kind': 'prior_paragraph_subject', 'paragraph_id': 'p0', 'person_mention_id': 'm', 'quote': '甲任職。', 'intervening_paragraph_ids': []}
    evidence = {'chapter_id': 'c', 'source_id': 's', 'paragraph_id': 'p1', 'quote': '遷太守，年六十。'}
    return context, evidence, chapter


class SubjectContinuationTests(unittest.TestCase):
    def test_actual_previous_subject(self):
        x, e, c = fixture()
        self.assertTrue(prior_subject_valid(x, e, 'a', c))

    def test_wrong_person_or_excerpt_gap(self):
        x, e, c = fixture()
        self.assertFalse(prior_subject_valid(x, e, 'b', c))
        c['paragraphs'][1]['source_position']['first_line'] = 14
        self.assertFalse(prior_subject_valid(x, e, 'a', c))

    def test_anchor_must_be_inside_quote_and_same_source(self):
        x, e, c = fixture()
        x['quote'] = '任職'
        self.assertFalse(prior_subject_valid(x, e, 'a', c))
        x, e, c = fixture(); e['source_id'] = 'other'
        self.assertFalse(prior_subject_valid(x, e, 'a', c))

    def test_title_requires_same_context_in_source_evidence(self):
        x, e, c = fixture()
        x.pop('intervening_paragraph_ids'); x['kind'] = 'previous_paragraph_subject'
        a = {'person_mention_id': 'm', 'paragraph_id': 'p1', 'context': x}
        h = {'person_id': 'a', 'evidence': [dict(e, context=copy.deepcopy(x))]}
        self.assertTrue(title_attestation_subject_valid(a, h, c))
        h['evidence'][0]['context']['person_mention_id'] = 'someone-else'
        self.assertFalse(title_attestation_subject_valid(a, h, c))
        h['evidence'][0]['context'] = x; a['person_mention_id'] = None
        self.assertFalse(title_attestation_subject_valid(a, h, c))
