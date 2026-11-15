import copy
import json
import unittest
from pathlib import Path

from scripts.jinshu075_clan_ancestor import valid


ROOT = Path(__file__).resolve().parents[1]


class Jinshu075ClanAncestorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        source = json.loads((ROOT / "corpus/jinshu/075.json").read_text())
        cls.paragraphs = {
            p["id"]: (p["id"].split(":", 1)[0], p)
            for p in source["paragraphs"]
        }
        assertions = json.loads((ROOT / "corpus/jinshu/075-assertions.json").read_text())
        cls.assertion = next(
            a for a in assertions["assertions"]
            if a["id"] == "a-jinshu075-xunsong-clan-ancestor"
        )

    def test_preserves_clan_ancestor_appellation_without_tree_edge(self):
        self.assertTrue(valid(self.assertion, self.paragraphs))
        q = self.assertion["qualifiers"]
        self.assertEqual(q["source_term"], "族曾祖顗")
        self.assertIsNone(q["generation_difference"])
        self.assertIsNone(q["common_ancestor_person_id"])

    def test_rejects_a_direct_ancestor_claim_or_wrong_source_term(self):
        for change in (
            lambda a: a.update(predicate="ancestor"),
            lambda a: a["qualifiers"].update(source_term="曾祖顗"),
            lambda a: a["qualifiers"].update(generation_difference=3),
        ):
            candidate = copy.deepcopy(self.assertion)
            change(candidate)
            self.assertFalse(valid(candidate, self.paragraphs))


if __name__ == "__main__":
    unittest.main()
