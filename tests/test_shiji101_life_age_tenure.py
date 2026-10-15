"""Source limits in the Yuan Ang / Chao Cuo biography."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def read(name):
    return json.loads((ROOT / "corpus/shiji" / name).read_text())

class LifeAgeTenure(unittest.TestCase):
    def test_deaths_have_correct_subjects_and_no_invented_dates(self):
        events = {x["id"]: x for x in read("101-life-events.json")["events"]}
        subjects = {4: "i30_mjq_6q8_A", 5: "yqp_nlb_p1p_AF", 6: "yqp_nlb_p1p_AC", 7: "qel_t1a_itz", 8: "j32_wtj_khz_A"}
        for n, person in subjects.items():
            e = events[f"le-shiji101-{n:03}"]
            self.assertEqual(e["person_id"], person)
            self.assertEqual(e["event_type"], "death")
            self.assertIsNone(e["date_expression"])
            self.assertNotIn("normalized_date_range", e)
            self.assertIn(e["source_term"], e["evidence"][0]["quote"])
        self.assertEqual(events["le-shiji101-007"]["source_term"], "母死")
        self.assertEqual(events["le-shiji101-008"]["source_term"], "刺殺盎")

    def test_chao_event_chronology_does_not_date_father(self):
        events = {x["id"]: x for x in read("101-life-events.json")["events"]}
        father, son = events["le-shiji101-002"], events["le-shiji101-003"]
        self.assertNotIn("normalized_date_range", father)
        dates = son["normalized_date_range"]
        self.assertEqual((dates["earliest"]["year"], dates["latest"]["year"]), (-154, -153))
        self.assertEqual(son["date_expression"], "吳楚七國果反")
        self.assertEqual(dates["evidence"], son["evidence"])
        self.assertTrue(any(r.get("book_id") == "b-shiji-011" for r in dates["references"]))

    def test_fu_age_is_open_report_not_birth_or_death_age(self):
        age = read("101.json")["annotation"]["age_assertions"][0]
        self.assertEqual(age["person_id"], "t6q_oe6_hom")
        self.assertEqual(age["source_term"], "年九十餘")
        self.assertEqual(age["bounds"], {"lower": 90, "lower_inclusive": False, "upper": None, "upper_inclusive": None})
        self.assertIsNone(age["value"])
        self.assertIsNone(age["birth_year"])
        self.assertEqual(age["date_expression"], "孝文帝時")

    def test_deng_duration_preserves_unknown_office_and_dates(self):
        h = next(x for x in read("101-titles.json")["holdings"] if x["id"] == "th-shiji101-048")
        self.assertEqual(h["person_id"], "ktk_wbg_wnm")
        self.assertEqual(h["reported_duration"]["value"], 1)
        self.assertEqual(h["reported_duration"]["source_term"], "一年")
        self.assertEqual(h["reported_duration"]["unit"], "title_year")
        self.assertEqual(h["reported_duration"]["evidence"], h["evidence"])

if __name__ == "__main__":
    unittest.main()
