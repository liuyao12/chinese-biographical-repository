"""Synthetic counterexamples: no historical text is changed by these tests."""
import json
from pathlib import Path
import unittest
from scripts.quotation_boundaries import unquoted_span
from scripts.validate_corpus import normalized_date_errors, title_proposal_errors
from scripts.unassumed_appointments import unassumed_appointment_valid
DATA = json.loads((Path(__file__).parent/'fixtures/quotation-boundary-counterexamples.json').read_text())
class NarrativeQuotationBoundaryTests(unittest.TestCase):
    def test_plain_narration(self):
        self.assertTrue(unquoted_span('甲。乙丙。',2,4))
    def test_earlier_completed_quote(self):
        self.assertTrue(unquoted_span('曰：「舊事。」今事。',8,10))
    def test_already_open_quote(self):
        self.assertFalse(unquoted_span('曰：「甲乙丙。」',4,6))
    def test_nested_quote(self):
        self.assertFalse(unquoted_span('曰：「甲『乙丙』丁。」',6,8))
    def test_new_quote_inside_span(self):
        self.assertFalse(unquoted_span('甲曰：「乙丙。」',0,7))
    def test_mismatched_close(self):
        self.assertFalse(unquoted_span('「甲』乙。',4,5))
    def test_book_title_is_not_speech(self):
        self.assertTrue(unquoted_span('著《甲書》。五年任官。',6,10))
    def test_wrong_bounds(self):
        self.assertFalse(unquoted_span('甲乙',True,2))
        self.assertFalse(unquoted_span('甲乙',1,3))
    def test_local_year_scope_already_inside_quote_rejected(self):
        x=DATA['local_source'];c=x['chapter']
        self.assertTrue(normalized_date_errors(x['dates'][0],{c['id']:c}))
    def test_other_speaker_decline_rejected(self):
        x=DATA['declined_source'];c=x['chapter'];q=x['proposals'][0]
        self.assertFalse(unassumed_appointment_valid(q,c))
        self.assertTrue(title_proposal_errors(q,c,{q['person_id']}))
if __name__ == '__main__': unittest.main()
