import unittest

from scripts.temporal_constraints import (
    calculate_temporal_constraint_results, errors, temporal_constraint_closure,
)


ERA = "era-yonghui"
COORD = {"calendar": "chinese_civil", "year_system": "regnal", "precision": "year", "era_id": ERA}


def date(year):
    return dict(COORD, year=year, inclusive=True)


class TemporalConstraintTests(unittest.TestCase):
    def test_cross_person_conditional_sequence_yields_death_years_three_to_six(self):
        constraints = [
            {"id": "death-window", "person_id": "princess", "target_event_id": "death",
             "operator": "within_interval", "interval": {"earliest": date(1), "latest": date(6)}},
            {"id": "death-lower", "person_id": "princess", "target_event_id": "death",
             "operator": "not_before", "bound": date(3)},
            {"id": "appointment-window", "person_id": "wang", "target_event_id": "appointment",
             "operator": "within_interval", "interval": {"earliest": date(1), "latest": date(6)}},
            {"id": "death-before-appointment", "person_id": "wang", "target_event_id": "appointment",
             "operator": "after_event", "related_event_id": "death", "assertion_mode": "derived",
             "derivation": {"rule_id": "narrative_sequence_implies_event_order",
                            "ordering_basis": "narrative_sequence",
                            "condition_status": "conditionally_accepted", "human_reviewed": True}},
        ]
        result = calculate_temporal_constraint_results(constraints)["death"]
        self.assertEqual(result["earliest"]["year"], 3)
        self.assertEqual(result["latest"]["year"], 6)
        self.assertEqual(result["status"], "conditional")
        self.assertIn("narrative_sequence", result["conditional_assumptions"])
        derivation = result["derivations"][0]
        self.assertEqual(set(derivation["input_constraint_ids"]), {"appointment-window", "death-before-appointment"})

    def test_unaccepted_narrative_sequence_is_incomplete(self):
        constraints = [
            {"id": "later-date", "target_event_id": "later", "operator": "within_interval",
             "interval": {"earliest": date(1), "latest": date(6)}},
            {"id": "unaccepted-order", "target_event_id": "later", "related_event_id": "earlier",
             "operator": "after_event", "derivation": {"rule_id": "narrative_sequence_implies_event_order",
             "ordering_basis": "narrative_sequence", "condition_status": "proposed"}},
        ]
        result = calculate_temporal_constraint_results(constraints)["earlier"]
        self.assertEqual(result["status"], "incomplete")
        self.assertIn("unaccepted-order", result["unsupported_constraint_ids"])

    def test_unreviewed_or_unlabeled_sequence_is_incomplete_even_without_validator(self):
        later = {"id": "later-date", "target_event_id": "later", "operator": "within_interval",
                 "interval": {"earliest": date(1), "latest": date(6)}}
        incomplete_relations = [
            {"id": "unreviewed", "target_event_id": "later", "related_event_id": "earlier",
             "operator": "after_event", "assertion_mode": "derived",
             "derivation": {"rule_id": "narrative_sequence_implies_event_order",
                            "ordering_basis": "narrative_sequence", "condition_status": "conditionally_accepted",
                            "human_reviewed": False}},
            {"id": "missing-basis", "target_event_id": "later", "related_event_id": "earlier",
             "operator": "after_event", "assertion_mode": "derived",
             "derivation": {"rule_id": "narrative_sequence_implies_event_order",
                            "condition_status": "conditionally_accepted", "human_reviewed": True}},
        ]
        result = calculate_temporal_constraint_results([later, *incomplete_relations])["earlier"]
        self.assertEqual(result["status"], "incomplete")
        self.assertEqual(set(result["unsupported_constraint_ids"]), {"unreviewed", "missing-basis"})

    def test_incompatible_calendar_relation_stays_incomplete(self):
        later_date = date(6)
        later_date["calendar"] = "other_calendar"
        constraints = [
            {"id": "later-date", "target_event_id": "later", "operator": "not_after", "bound": later_date},
            {"id": "earlier-date", "target_event_id": "earlier", "operator": "not_before", "bound": date(2)},
            {"id": "sequence", "target_event_id": "later", "related_event_id": "earlier",
             "operator": "after_event", "derivation": {"rule_id": "narrative_sequence_implies_event_order",
             "ordering_basis": "narrative_sequence", "condition_status": "conditionally_accepted"}},
        ]
        result = calculate_temporal_constraint_results(constraints)["earlier"]
        self.assertEqual(result["status"], "incomplete")
        self.assertIn("sequence", result["unsupported_constraint_ids"])

    def test_person_bundle_dependency_closure_includes_other_person_and_source_constraints(self):
        constraints = [
            {"id": "death-lower", "person_id": "princess", "target_event_id": "death"},
            {"id": "death-before-appointment", "person_id": "wang", "target_event_id": "appointment",
             "related_event_id": "death", "operator": "after_event"},
            {"id": "appointment-window", "person_id": "wang", "target_event_id": "appointment"},
            {"id": "unrelated", "person_id": "other", "target_event_id": "other-event"},
        ]
        selected = temporal_constraint_closure(constraints, {"princess"})
        self.assertEqual({c["id"] for c in selected},
                         {"death-lower", "death-before-appointment", "appointment-window"})

    def test_validator_accepts_source_anchored_cross_person_order_edge(self):
        # Synthetic test fixture only; it is not an attestation or corpus transcription.
        quote = "王方翼傳：公主卒後，歸長安。永徽中累授安定令。"
        term = "公主卒後"
        claim = {"source_term": term, "start": quote.index(term), "end": quote.index(term) + len(term),
                 "normalized_relation": {"operator": "after_event", "related_event_id": "death"}}
        citation = {"work_id": "work-old-tang", "book_id": "book-185", "source_id": "old-tang",
                    "chapter_id": "chapter-185", "paragraph_id": "p1", "quote": quote,
                    "person_mention_id": "m-wang", "temporal_claim": claim}
        records = [
            {"record_type": "person_life_event_assertion_set", "events": [
                {"id": "death", "person_id": "princess", "event_type": "death"}]},
            {"record_type": "person_event_assertion_set", "events": [
                {"id": "appointment", "person_id": "wang", "event_type": "appointment"}]},
            {"record_type": "temporal_constraint_set", "format_version": "0.1", "work_id": "work-old-tang",
             "book_id": "book-185", "source_id": "old-tang", "chapter_id": "chapter-185", "constraints": [{
                "id": "death-before-appointment", "person_id": "wang", "target_event_id": "appointment",
                "operator": "after_event", "related_event_id": "death", "assertion_mode": "derived",
                "derivation": {"rule_id": "narrative_sequence_implies_event_order",
                               "ordering_basis": "narrative_sequence", "condition_status": "conditionally_accepted",
                               "human_reviewed": True},
                "human_reviewed": True, "evidence": [citation],
            }]},
        ]
        chapter = {"id": "chapter-185", "chapter_id": "chapter-185", "work_id": "work-old-tang", "book_id": "book-185", "source_id": "old-tang",
                   "paragraphs": [{"id": "p1", "text": quote, "mentions": [
                       {"id": "m-wang", "person_id": "wang", "start": 0, "end": 3, "surface": "王方翼"}]}]}
        self.assertEqual(errors(records, {"chapter-185": chapter}, {"princess", "wang"}), [])

    def test_validator_binds_death_lower_bound_to_exact_visited_person_date(self):
        quote = "帝永徽三年幸公主第"
        term = "永徽三年"
        date_claim = {"source_term": term, "start": quote.index(term),
                      "end": quote.index(term) + len(term), "normalized_date": date(3)}
        citation = {"work_id": "work-old-tang", "book_id": "book-annals", "source_id": "old-tang",
                    "chapter_id": "chapter-annals", "paragraph_id": "p1", "quote": quote,
                    "person_mention_id": "m-princess", "temporal_claim": date_claim}
        visit = {"id": "visit", "person_id": "princess", "event_type": "visit",
                 "participant_role": "visited_person", "date_expression": term,
                 "normalized_date": date(3), "evidence": [citation]}
        records = [
            {"record_type": "person_life_event_assertion_set", "events": [
                {"id": "death", "person_id": "princess", "event_type": "death"}, visit]},
            {"record_type": "temporal_constraint_set", "format_version": "0.1", "work_id": "work-old-tang",
             "book_id": "book-annals", "source_id": "old-tang", "chapter_id": "chapter-annals", "constraints": [{
                "id": "death-lower", "person_id": "princess", "target_event_id": "death",
                "operator": "not_before", "bound": date(3), "assertion_mode": "derived",
                "derivation": {"rule_id": "person_alive_at_event_implies_death_not_before", "input_event_id": "visit"},
                "human_reviewed": True, "evidence": [citation],
            }]},
        ]
        chapter = {"id": "chapter-annals", "chapter_id": "chapter-annals", "work_id": "work-old-tang",
                   "book_id": "book-annals", "source_id": "old-tang", "paragraphs": [{
                       "id": "p1", "text": quote, "mentions": [{"id": "m-princess", "person_id": "princess",
                       "start": quote.index("公主"), "end": quote.index("公主") + 2, "surface": "公主"}],
                   }]}
        self.assertEqual(errors(records, {"chapter-annals": chapter}, {"princess"}), [])


if __name__ == "__main__":
    unittest.main()
