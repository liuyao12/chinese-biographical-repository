# coding: utf-8
"""Complete received-witness career roles, qualified continuation and typed links."""
from pathlib import Path
import copy
import json
import sys
import unittest
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts import fixed_witness_fact_slots as facts
from scripts.subject_continuation import title_attestation_subject_valid


class DuyuCareer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = json.loads((ROOT/'corpus/jinshu/034-duyu.json').read_bytes())
        cls.records = facts.records(cls.chapter, ROOT)
        cls.slots = {x['fixed_source_fact_binding']['slot']: x for x in cls.records}
        cls.holding = cls.slots['career_049']

    def checked_subject(self, holding=None, chapter=None, root=ROOT):
        h = holding if holding is not None else copy.deepcopy(self.holding)
        c = chapter if chapter is not None else copy.deepcopy(self.chapter)
        return title_attestation_subject_valid(h['attestations'][0], h, c, root=root)

    def test_complete_source_and_career_scope(self):
        self.assertEqual(len(self.chapter['paragraphs']), 27)
        self.assertEqual(len([s for s in self.slots if s.startswith('career_')]), 75)

    def test_continuation_with_actual_root_and_raw(self):
        self.assertTrue(self.checked_subject())

    def test_missing_root_is_rejected(self):
        self.assertFalse(self.checked_subject(root=None))

    def test_temporal_patient_is_not_rewarded(self):
        h = copy.deepcopy(self.holding)
        ctx = h['attestations'][0]['context']
        patient = next(m for p in self.chapter['paragraphs'] for m in p['mentions']
                       if m['id'] == ctx['temporal_patient_mention_id'])
        h['person_id'] = patient['person_id']
        self.assertFalse(self.checked_subject(h))

    def test_wrong_previous_subject_is_rejected(self):
        h = copy.deepcopy(self.holding)
        h['attestations'][0]['context']['person_mention_id'] = 'c-jinshu-034-duyu:p016:m0000'
        self.assertFalse(self.checked_subject(h))

    def test_coherently_wrong_named_previous_person_is_rejected(self):
        h = copy.deepcopy(self.holding)
        wrong = next(m for p in self.chapter['paragraphs'] for m in p['mentions']
                     if m['id'] == 'c-jinshu-034-duyu:p016:m0000')
        self.assertNotEqual(wrong['person_id'], h['person_id'])
        h['person_id'] = wrong['person_id']
        att = h['attestations'][0]
        att['person_mention_id'] = wrong['id']
        att['context']['person_mention_id'] = wrong['id']
        for evidence in h['evidence']:
            if evidence['paragraph_id'] == 'c-jinshu-034-duyu:p016':
                evidence['person_mention_id'] = wrong['id']
            if 'context' in evidence:
                evidence['context']['person_mention_id'] = wrong['id']
        self.assertFalse(self.checked_subject(h))

    def test_missing_paired_evidence_is_rejected(self):
        h = copy.deepcopy(self.holding)
        h['evidence'] = h['evidence'][:1]
        self.assertFalse(self.checked_subject(h))

    def test_changed_context_quote_is_rejected(self):
        h = copy.deepcopy(self.holding)
        h['attestations'][0]['context']['quote'] += '。'
        self.assertFalse(self.checked_subject(h))

    def test_commentary_layer_cannot_be_biography(self):
        c = copy.deepcopy(self.chapter)
        c['paragraphs'][16]['source_position']['source_layer'] = 'commentary'
        self.assertFalse(self.checked_subject(chapter=c))

    def test_changed_received_text_is_rejected(self):
        c = copy.deepcopy(self.chapter)
        c['paragraphs'][16]['text'] += '。'
        self.assertFalse(self.checked_subject(chapter=c))

    def test_raw_coshift_is_rejected(self):
        c = copy.deepcopy(self.chapter)
        pos = c['paragraphs'][16]['source_position']
        pos['raw_start'] += 1
        pos['raw_end'] += 1
        pos['raw_character_offsets'] = [x+1 for x in pos['raw_character_offsets']]
        self.assertFalse(self.checked_subject(chapter=c))

    def test_annotator_is_not_received_role(self):
        c = copy.deepcopy(self.chapter)
        c['paragraphs'][15]['annotator'] = '古注'
        self.assertFalse(self.checked_subject(chapter=c))

    def test_nonadjacent_subject_is_rejected(self):
        h = copy.deepcopy(self.holding)
        h['attestations'][0]['context']['paragraph_id'] = self.chapter['paragraphs'][14]['id']
        self.assertFalse(self.checked_subject(h))

    def test_office_ends_remain_undated(self):
        for record in self.records:
            if record['fixed_source_fact_binding']['slot'].startswith('career_') and 'effective_period' in record:
                self.assertNotIn('year', record['effective_period']['end'])
                self.assertIsNone(record['effective_period']['end']['date_expression'])

    def test_sili_is_reported_appointment_not_service_holding(self):
        notice = self.slots['career_056']
        self.assertEqual(notice['kind'], 'appointment_service_unreported')
        self.assertEqual(notice['values']['arrival_status'], 'not_reported')
        self.assertFalse(any(x.get('title') == '司隸校尉' and x['person_id'] == notice['person_id']
                             for x in self.records))

    def test_xi_two_nonassumptions_keep_alternative_scope(self):
        xs = [x for x in self.records if x.get('proposal_kind') == 'unassumed_appointment']
        self.assertEqual({x['title'] for x in xs}, {'吏部郎', '城陽太守'})
        self.assertTrue(all(x['source_qualification']['alternative_scope'] == 'last_office_only' for x in xs))

    def test_death_year_cannot_be_added_as_office_end(self):
        h = copy.deepcopy(self.holding)
        h['effective_period']['end']['year'] = 284
        self.assertFalse(facts.valid(h, self.chapter, ROOT))

    def test_six_links_bind_exact_same_person_holdings(self):
        pairs = {'005': ('003', 'linked_holding_id'), '013': ('010', 'prior_holding_id'),
                 '024': ('023', 'prior_holding_id'), '026': ('023', 'linked_holding_id'),
                 '050': ('049', 'linked_holding_id'), '052': ('051', 'linked_holding_id')}
        holdings = [x for x in self.records if 'attestations' in x]
        for source, (target, field) in pairs.items():
            with self.subTest(slot=source):
                record = self.slots['career_'+source]
                correct = self.slots['career_'+target]
                self.assertEqual(record['values'][field], correct['id'])
                self.assertEqual(record['person_id'], correct['person_id'])
                self.assertTrue(facts.valid(record, self.chapter, ROOT))
                alternatives = [h for h in holdings
                                if h['person_id'] == record['person_id'] and h['id'] != correct['id']]
                # The child has only one attested holding: do not invent another career.
                others = alternatives[:1] + [next(h for h in holdings if h['person_id'] != record['person_id'])]
                for other in others:
                    wrong = copy.deepcopy(record)
                    wrong['values'][field] = other['id']
                    self.assertFalse(facts.valid(wrong, self.chapter, ROOT))

    def test_removal_and_continued_duties_are_separate(self):
        removal = self.slots['career_024']
        continuation = self.slots['career_026']
        self.assertFalse(removal['values']['duties_ended_inferred'])
        self.assertEqual(removal['values']['duties_continuation_report_id'], continuation['id'])
        self.assertEqual(continuation['values']['prior_removal_report_id'], removal['id'])
        self.assertFalse(continuation['values']['new_independent_office_inferred'])


if __name__ == '__main__':
    unittest.main()
