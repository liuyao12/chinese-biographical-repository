import hashlib
import json
import unittest
from pathlib import Path

from scripts.sgz058_lu_family import comparison_only_valid, no_materialized_relations, unadopted_record_valid

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "source-evidence/sanguozhi058-lu-family"


class Sanguozhi058ComparisonOnlyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reading = json.loads((EVIDENCE / "reading.json").read_text())
        cls.identities = json.loads((EVIDENCE / "identities.json").read_text())
        cls.boundary = (EVIDENCE / "comparison-boundary.md").read_text()
        cls.excerpts = (EVIDENCE / "excerpts.txt").read_text()

    def test_unknown_print_base_remains_comparison_only(self):
        self.assertTrue(comparison_only_valid(self.reading, self.identities, self.boundary, self.excerpts))

    def test_optional_untracked_dispositions_have_no_active_assertions(self):
        path = ROOT / "corpus/sanguozhi/058-lu-xun-family-assertions.json"
        if not path.exists():
            self.skipTest("本次 PR 不納入非語料工作樹暫存檔")
        self.assertTrue(no_materialized_relations(json.loads(path.read_text())))

    def test_optional_local_chapter_stub_is_not_an_api_chapter(self):
        path = ROOT / "corpus/sanguozhi/058-lu-xun-family.json"
        if not path.exists():
            self.skipTest("本次 PR 不納入非語料工作樹暫存檔")
        chapter = json.loads(path.read_text())
        self.assertEqual(chapter.get("record_type"), "comparison_only_not_materialized")
        self.assertEqual(chapter.get("status"), "not_adopted")

    def test_unadopted_comparison_record_has_no_graph_assertions(self):
        record = json.loads((EVIDENCE / "unadopted-comparison.json").read_text())
        digest = hashlib.sha256((EVIDENCE / "excerpts.txt").read_bytes()).hexdigest()
        self.assertTrue(unadopted_record_valid(record, digest))

    def test_comparison_excerpt_hash_is_fixed(self):
        digest = hashlib.sha256((EVIDENCE / "excerpts.txt").read_bytes()).hexdigest()
        self.assertEqual(digest, self.reading["excerpt_sha256"])

    def test_witness_is_not_registered_as_active_chapter_or_text_base(self):
        works = json.loads((ROOT / "registry/works.json").read_text())
        sanguozhi = next(work for work in works["works"] if work["id"] == "w-sanguozhi")
        self.assertFalse(any(book["id"] == "b-sanguozhi-058" for book in sanguozhi["books"]))
        provenance = json.loads((ROOT / "registry/work-provenance.json").read_text())
        self.assertNotIn("s-sanguozhi-058-wikisource-lu-family", provenance["text_bases"])

    def test_no_private_revision_author_is_persisted(self):
        self.assertNotIn("revision_author", self.reading["witness"])


if __name__ == "__main__":
    unittest.main()
