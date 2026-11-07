import hashlib
import json
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def read(name):
    return json.loads((ROOT / name).read_text())

class CompleteJin039(unittest.TestCase):
    def test_all_three_projections_match_fixed_raw_and_paragraphs(self):
        chapter = read("corpus/jinshu/039.json")
        paragraphs = {p["id"]: p for p in chapter["paragraphs"]}
        raw = (ROOT / "sources/jinshu/039-ws2108782.wikitext").read_bytes()
        lines = raw.decode().splitlines()
        units = []
        for name in ["jin039-xunyi-full-projection", "jin039-xunxu-full-projection", "jin039-complete33-projection"]:
            projection = read("source-evidence/" + name + ".json")
            self.assertEqual(hashlib.sha256(raw).hexdigest(), projection["raw_sha256"])
            for unit in projection["units"]:
                line = lines[unit["source_line"] - 1]
                self.assertEqual(line, unit["raw_line"])
                self.assertEqual(unit["display_text"], "".join(line[i] for i in unit["display_to_raw_columns"]))
                self.assertEqual(unit["display_text"], "".join(paragraphs[x["paragraph_id"]]["text"] for x in unit["parts"]))
                units.append(unit["source_line"])
        self.assertEqual(len(units), 66)
        self.assertEqual(len(set(units)), 66)
        self.assertEqual(len(paragraphs), 69)
        order = [p["source_position"]["first_line"] for p in chapter["paragraphs"]]
        self.assertEqual(order, sorted(order))
        self.assertEqual(order[0], 11)
        self.assertEqual(order[-1], 148)

    def test_qiwang_you_is_not_xun_you(self):
        chapter = read("corpus/jinshu/039.json")
        paragraph = next(p for p in chapter["paragraphs"] if p["id"].endswith(":feng-full:l139"))
        mentions = [m for m in paragraph["mentions"] if m["surface"] in ["齊王攸", "齊王", "攸"]]
        self.assertTrue(mentions)
        self.assertEqual({m["person_id"] for m in mentions}, {"cac_ca2_008"})
