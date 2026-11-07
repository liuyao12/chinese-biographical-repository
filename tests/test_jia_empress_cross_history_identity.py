import json
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def read(path):
    return json.loads((ROOT / path).read_text())

class JiaEmpressIdentity(unittest.TestCase):
    def test_cross_history_forms_share_attested_paternal_identity(self):
        cases = [("corpus/jinshu/039.json", "女", "c-jinshu-039-wangxun-feng:yi-full:p006"), ("corpus/jinshu/059.json", "賈后", "c-jinshu-059-liang-yang:line026"), ("corpus/songshu/060.json", "賈庶人", "c-songshu-060-xunbozi:p004")]
        for path, surface, paragraph_id in cases:
            p = next(p for p in read(path)["paragraphs"] if p["id"] == paragraph_id)
            marks = [m for m in p["mentions"] if m["surface"] == surface]
            self.assertTrue(marks)
            self.assertEqual({m["person_id"] for m in marks}, {"c27_590_7e3_A"})
        assertions = read("corpus/jinshu/039-assertions.json")["assertions"]
        father = next(a for a in assertions if a["id"] == "a-jinshu039-yi-full-003")
        self.assertEqual((father["predicate"], father["subject_person_id"], father["object_person_id"]), ("father", "c27_590_7e3_A", "c27_590_7e3"))

    def test_fixed_bridge_distinguishes_sister_from_empress(self):
        raw = (ROOT / "sources/jinshu/031-jia-ws2479706.wikitext").read_text()
        self.assertIn("始欲聘后妹午", raw)
        self.assertIn("更娶南風", raw)
        self.assertIn("荀顗、荀勖並稱充女之賢，乃定婚", raw)
        self.assertIn("惠帝即位，立為皇后", raw)
