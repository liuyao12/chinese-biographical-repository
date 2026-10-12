import unittest
from scripts import reading_catalog


class ReadingCatalogTests(unittest.TestCase):
    def test_derived_reader_copies_match_authoritative_chapter_bytes(self):
        reading_catalog.run(check=True)

    def test_category_boundaries_cover_every_shiji_chapter_once(self):
        numbers = [n for start, end, _, _ in reading_catalog.CATEGORIES for n in range(start, end + 1)]
        self.assertEqual(numbers, list(range(1, 131)))
