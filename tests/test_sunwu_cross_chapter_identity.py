import json
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def read(path):
    return json.loads((ROOT / path).read_text())

class SunwuCrossChapterIdentity(unittest.TestCase):
    def test_wu_campaigns_use_one_identity(self):
        cases = [("031", "p027", "孫武"), ("031", "p028", "孫武"), ("065", "p001", "孫子武"), ("066", "p014", "孫武")]
        for number, suffix, surface in cases:
            chapter = read("corpus/shiji/" + number + ".json")
            paragraph = next(p for p in chapter["paragraphs"] if p["id"].endswith(":" + suffix))
            marks = [m for m in paragraph["mentions"] if m["surface"] == surface]
            self.assertTrue(marks)
            self.assertEqual({m["person_id"] for m in marks}, {"vax_w2r_0za"})

    def test_sunbin_is_separate_in_same_paragraph(self):
        chapter = read("corpus/shiji/065.json")
        paragraph = next(p for p in chapter["paragraphs"] if p["id"].endswith(":p002"))
        self.assertIn("孫武既死，後百餘歲有孫臏", paragraph["text"])
        self.assertEqual({m["person_id"] for m in paragraph["mentions"] if m["surface"] == "孫臏"}, {"u7n_hyp_nqf"})
        self.assertEqual({m["person_id"] for m in paragraph["mentions"] if m["surface"] == "孫武"}, {"vax_w2r_0za"})
        people = {p["id"] for p in read("registry/persons.json")["persons"]}
        self.assertIn("vax_w2r_0za", people)
        self.assertIn("u7n_hyp_nqf", people)
