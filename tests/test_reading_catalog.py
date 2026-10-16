import unittest
from scripts import reading_catalog


class ReadingCatalogTests(unittest.TestCase):
    def test_other_work_catalog_uses_native_ids_and_partial_scope(self):
        outputs=reading_catalog.outputs()
        import json
        root=reading_catalog.ROOT
        manifest=json.loads(outputs[root/'data/corpus/works.json'])
        hanshu=next(w for w in manifest['works'] if w['id']=='w-hanshu')
        self.assertEqual(next(w for w in manifest['works'] if w['id']=='w-shiji')['reader_kind'],'shiji')
        catalog=json.loads(outputs[root/hanshu['catalog_path']])
        self.assertEqual(len(catalog['chapters']),1)
        chapter=catalog['chapters'][0]
        self.assertEqual(chapter['text_scope'],'partial_chapter')
        self.assertEqual(outputs[root/chapter['path']],(root/'corpus/hanshu/041.json').read_bytes())

    def test_derived_reader_copies_match_authoritative_chapter_bytes(self):
        reading_catalog.run(check=True)

    def test_category_boundaries_cover_every_shiji_chapter_once(self):
        numbers = [n for start, end, _, _ in reading_catalog.CATEGORIES for n in range(start, end + 1)]
        self.assertEqual(numbers, list(range(1, 131)))
