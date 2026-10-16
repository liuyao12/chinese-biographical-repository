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
        for record in data['records']:
            chapter = chapters[record['chapter_id']]
            paragraph = next(p for p in chapter['paragraphs'] if p['id'] == record['paragraph_id'])
            self.assertIn(record['quote'], paragraph['text'])
            self.assertTrue(any(m.get('person_id') == record['person_id'] for m in paragraph['mentions']))
            self.assertFalse(record['human_reviewed'])
