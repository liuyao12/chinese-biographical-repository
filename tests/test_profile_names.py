import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class ProfileNamesTests(unittest.TestCase):
    def test_components_have_exact_received_evidence_and_person_anchor(self):
        data = json.loads((ROOT/'data/corpus/profile-names.json').read_text())
        chapters = {}
        for path in (ROOT/'corpus').glob('*/*.json'):
            chapter = json.loads(path.read_text())
            if chapter.get('record_type') == 'marked_chapter':
                chapters[chapter['id']] = chapter
        from scripts.table_evidence import load_tables, table_cell
        tables = load_tables(ROOT)
        for record in data['records']:
            if record.get('kind') == 'table_cell':
                table = tables[record['table_id']]
                for key, source_key in [('work_id','work_id'), ('book_id','book_id'), ('chapter_id','chapter_id'), ('source_id','id'), ('source_revision','revision')]:
                    self.assertEqual(record[key], table['source'][source_key])
                cell = table_cell(table, record['table_cell_id'])
                self.assertEqual(record['quote'], cell['text'])
                mention = next(m for m in cell['person_mentions'] if m['id'] == record['person_mention_id'])
                self.assertEqual(mention['person_id'], record['person_id'])
                self.assertEqual(mention['surface'], (record['surname'] or '') + record['ming'])
                self.assertEqual(cell['text'][mention['start']:mention['end']], mention['surface'])
                self.assertNotIn('paragraph_id', record)
                self.assertFalse(record['human_reviewed'])
                continue
            chapter = chapters[record['chapter_id']]
            paragraph = next(p for p in chapter['paragraphs'] if p['id'] == record['paragraph_id'])
            self.assertIn(record['quote'], paragraph['text'])
            self.assertTrue(any(m.get('person_id') == record['person_id'] for m in paragraph['mentions']))
            self.assertFalse(record['human_reviewed'])
