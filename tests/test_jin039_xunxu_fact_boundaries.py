import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def read(path):
    return json.loads((ROOT / path).read_text())

class XunxuFactBoundaries(unittest.TestCase):
    def test_explicit_death_years_and_original_expressions(self):
        events = [e for e in read("corpus/jinshu/039-life-events.json")["events"] if e["id"].startswith("le-jin039-xu30-")]
        self.assertEqual(len(events), 10)
        dated = {e["person_id"]: (e["normalized_date"]["year"], e["date_expression"]) for e in events if "normalized_date" in e}
        self.assertEqual(dated, {"yoo_ox0_545_FAAA": (289, "太康十年"), "yoo_ox0_545_FAAAA": (313, "建興元年"), "yoo_ox0_545_FAAAAB": (324, "太寧二年"), "yoo_ox0_545_FAAACA": (332, "咸和七年")})
        for event in events:
            self.assertEqual(event["event_type"], "death")
            self.assertTrue(event["evidence"])

    def test_declined_appointments_are_not_active_holdings(self):
        holdings = read("corpus/jinshu/039-titles.json")["holdings"]
        rejected = {("yoo_ox0_545_FAAAA", "司空"), ("yoo_ox0_545_FAAAC", "太子太保"), ("yoo_ox0_545_FAAACA", "中舍人"), ("yoo_ox0_545_FAAACA", "散騎侍郎")}
        for holding in holdings:
            self.assertNotIn((holding["person_id"], holding["title"]), rejected)
        added = [h for h in holdings if h["id"].startswith("th-jin039-xu30-")]
        self.assertEqual(len(added), 100)
        self.assertFalse(any(h["title"] == "濟北郡公" for h in added))

    def test_consumption_anchors_match_received_text(self):
        audit = read("source-evidence/jin039-xunxu-facts30-consumption.json")
        paragraphs = {p["id"]: p["text"] for p in read("corpus/jinshu/039.json")["paragraphs"]}
        rows = audit["ledger"]["records"]
        self.assertEqual(len(rows), 87)
        self.assertFalse(audit["human_reviewed"])
        self.assertFalse(audit["image_verified"])
        for row in rows:
            self.assertTrue(row["native_targets"] or row["reused_targets"] or row["typed_targets"])
            for anchor in row["anchors"]:
                self.assertEqual(paragraphs[anchor["paragraph_id"]][anchor["start"]:anchor["end"]], anchor["surface"])
