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
        from scripts.table_evidence import load_tables
        native_tables={t['source']['chapter_id']:t for t in load_tables(root).values()
                       if t['source']['work_id']=='w-hanshu'}
        self.assertEqual({c['chapter_id'] for c in catalog['chapters']},set(sources)|set(native_tables))
        for chapter in catalog['chapters']:
            if chapter['available']=='table':
                table=native_tables[chapter['chapter_id']]
                self.assertEqual(chapter['table_id'],table['id'])
                self.assertEqual(chapter['work_id'],table['source']['work_id'])
                self.assertEqual(chapter['book_id'],table['source']['book_id'])
                self.assertEqual(chapter['text_scope'],table['source'].get('text_scope','table'))
                self.assertEqual(chapter['scope_note'],table['source'].get('extent',table['source']['note']))
                self.assertNotIn('path',chapter)
                self.assertFalse((root/'corpus/hanshu'/f"{chapter['number']:03d}.json").exists())
                continue
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

    def test_progress_follows_chapter_not_shared_book(self):
        import json
        from pathlib import Path
        from collections import defaultdict
        from unittest.mock import patch
        root=reading_catalog.ROOT
        progress_path=root/'corpus/progress.json'
        rows=json.loads(progress_path.read_text())
        native={}
        for path in (root/'corpus').glob('*/*.json'):
            chapter=json.loads(path.read_text())
            if chapter.get('record_type')=='marked_chapter' and chapter['work_id']!='w-shiji':
                native[chapter['id']]=chapter
        groups=defaultdict(list)
        for row in rows['books']:
            if row.get('chapter_id') in native:groups[row['book_id']].append(row)
        first,second=next(group[:2] for group in groups.values() if len(group)>1)
        expected={first['chapter_id']:'synthetic-status-one',second['chapter_id']:'synthetic-status-two'}
        first['person_status'],second['person_status']=expected.values()
        original=Path.read_text
        def read(path,*args,**kwargs):
            return json.dumps(rows) if path==progress_path else original(path,*args,**kwargs)
        with patch.object(Path,'read_text',read):outputs=reading_catalog.outputs(root=root)
        work_id=native[first['chapter_id']]['work_id']
        catalog=json.loads(outputs[root/('data/corpus/'+work_id.removeprefix('w-')+'/index.json')])
        actual={chapter['chapter_id']:chapter['annotation_status'] for chapter in catalog['chapters'] if chapter['chapter_id'] in expected}
        self.assertEqual(actual,expected)

    def test_all_native_chapters_have_explicit_progress(self):
        import json
        root=reading_catalog.ROOT
        rows=json.loads((root/'corpus/progress.json').read_text())['books']
        by_id={row['chapter_id']:row for row in rows}
        self.assertEqual(len(by_id),len(rows))
        for path in (root/'corpus').glob('*/*.json'):
            chapter=json.loads(path.read_text())
            if chapter.get('record_type')=='marked_chapter':
                self.assertIn(chapter['id'],by_id,str(path))
                self.assertEqual(by_id[chapter['id']]['book_id'],chapter['book_id'])
