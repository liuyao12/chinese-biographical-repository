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
        sources={json.loads(p.read_text())['id']:p for p in (root/'corpus/hanshu').glob('*.json') if json.loads(p.read_text()).get('record_type')=='marked_chapter'}
        self.assertEqual({c['chapter_id'] for c in catalog['chapters']},set(sources))
        for chapter in catalog['chapters']:
            source=sources[chapter['chapter_id']]
            native=json.loads(source.read_text())
            self.assertEqual(chapter['work_id'],native['work_id'])
            self.assertEqual(chapter['book_id'],native['book_id'])
            self.assertEqual(chapter['text_scope'],native['source'].get('text_scope','chapter'))
            self.assertEqual(outputs[root/chapter['path']],source.read_bytes())

    def test_derived_reader_copies_match_authoritative_chapter_bytes(self):
        reading_catalog.run(check=True)

    def test_category_boundaries_cover_every_shiji_chapter_once(self):
        numbers = [n for start, end, _, _ in reading_catalog.CATEGORIES for n in range(start, end + 1)]
        self.assertEqual(numbers, list(range(1, 131)))
