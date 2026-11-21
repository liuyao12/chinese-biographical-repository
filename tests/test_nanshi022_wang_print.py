import json
from copy import deepcopy
from pathlib import Path
import unittest

from scripts.nanshi022_print import errors
from scripts.nanshi022_royal_kin import valid

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "corpus/nanshi"


def read(path):
    return json.loads(path.read_text())


class PrintedWangAccounts(unittest.TestCase):
    def test_placement_of_each_glyph_matters(self):
        chapter = read(BASE / "022-wangsengchuo-wyd.json")
        self.assertEqual(errors(chapter, ROOT), [])
        changed = deepcopy(chapter)
        first = changed["paragraphs"][0]["source_position"]["column_projection"]
        span = first[0]
        column = dict(line.split(maxsplit=1) for line in
                      (ROOT / chapter["source"]["raw_path"]).read_text().splitlines())
        glyph = span["text"][0]
        other, offset = next((col, text.index(glyph)) for col, text in column.items()
                             if col != span["column"] and glyph in text)
        first[:1] = [dict(column=other, start=offset, end=offset + 1, text=glyph),
                     dict(span, start=span["start"] + 1, text=span["text"][1:])]
        self.assertTrue(errors(changed, ROOT))

    def test_female_relations_and_open_cases_in_both_witnesses(self):
        for suffix in ("", "-wyd"):
            slug = "022-wangsengchuo" + suffix
            chapter = read(BASE / (slug + ".json"))
            assertions = read(BASE / (slug + "-assertions.json"))["assertions"]
            frames = [a for a in assertions if "royal_kin_frame" in a["qualifiers"]]
            self.assertEqual(len(frames), 6)
            for assertion in frames:
                self.assertTrue(valid(assertion, chapter, ROOT))
                swapped = dict(assertion, subject_person_id=assertion["object_person_id"])
                self.assertFalse(valid(swapped, chapter, ROOT))
            candidates = {m["surface"]: m["candidate_person_ids"] for p in chapter["paragraphs"]
                          for m in p["mentions"] if m.get("candidate_person_ids")}
            self.assertEqual(candidates["兒"], ["fof_k8v_7md", "3b1_39e_aa6"])
            self.assertEqual(candidates["袁悅"], ["c72_605_73c"])
