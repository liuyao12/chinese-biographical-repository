"""Public profiles retain exact source scopes and every marked occurrence."""
import json
import unittest
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ProfileSourceScopesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapters = {}
        cls.mentions = {}
        cls.by_person = defaultdict(lambda: defaultdict(set))
        for path in (ROOT / 'corpus').glob('*/*.json'):
            ch = json.loads(path.read_text())
            if ch.get('record_type') != 'marked_chapter':
                continue
            cls.chapters[ch['id']] = ch
            for p in ch['paragraphs']:
                for m in p['mentions']:
                    if m['kind'] == 'person':
                        cls.mentions[m['id']] = (ch, p, m)
                        cls.by_person[m['person_id']][ch['id']].add(m['id'])
        cls.canonical_mentions = {}
        for path in (ROOT / 'corpus').glob('*/*-occurrence-concordance.json'):
            for row in json.loads(path.read_text())['records']:
                if row['kind'] == 'resolved_person_occurrence_alias':
                    cls.canonical_mentions[row['duplicate_mention_id']] = row['canonical_mention_id']
        cls.profiles = [json.loads(p.read_text()) for p in
                        (ROOT / 'data/corpus/profiles').glob('*.json')
                        if p.stem != 'index']

    def test_all_body_occurrences_have_exact_ids_and_complete_mention_coverage(self):
        for profile in self.profiles:
            own = set(profile.get('person_ids', [profile['id']]))
            expected = defaultdict(set)
            for pid in own:
                for cid, mids in self.by_person[pid].items():
                    expected[cid].update(mids)
            observed = {}
            for o in profile['occurrences']:
                ch = self.chapters[o['chapter_id']]
                for key in ('work_id', 'book_id', 'chapter_id', 'source_id'):
                    self.assertEqual(o[key], ch['id'] if key == 'chapter_id' else ch[key], profile['id'])
                self.assertNotIn(ch['id'], observed)
                observed[ch['id']] = set(o['mention_ids'])
                self.assertEqual(len(o['mention_ids']), o['raw_count'])
                self.assertEqual(len(observed[ch['id']]), o['raw_count'])
                expected_groups = defaultdict(set)
                for mid in o['mention_ids']:
                    expected_groups[self.canonical_mentions.get(mid, mid)].add(mid)
                actual_groups = {}
                for group in o['occurrence_groups']:
                    canonical = group['canonical_mention_id']
                    self.assertNotIn(canonical, actual_groups)
                    self.assertIn(canonical, group['mention_ids'])
                    self.assertEqual(len(group['mention_ids']), len(set(group['mention_ids'])))
                    actual_groups[canonical] = set(group['mention_ids'])
                self.assertEqual(actual_groups, dict(expected_groups), profile['id'])
                self.assertEqual(len(actual_groups), o['count'])
                self.assertEqual(o['raw_count'] - o['count'], o['duplicate_count'])
                paragraphs = set()
                for mid in o['mention_ids']:
                    actual_ch, paragraph, mention = self.mentions[mid]
                    self.assertEqual(actual_ch['id'], ch['id'])
                    self.assertIn(mention['person_id'], own)
                    paragraphs.add(paragraph['id'])
                self.assertEqual(set(o['paragraph_ids']), paragraphs)
                self.assertIn(o['paragraph_id'], paragraphs)
                first = next(p for p in ch['paragraphs'] if p['id'] == o['paragraph_id'])
                self.assertIn(o['quote'], first['text'])
            self.assertEqual(observed, dict(expected), profile['id'])

    def test_all_native_occurrences_cite_the_original_work_book_cell_and_revision(self):
        tables = {}
        for path in (ROOT / 'data/historical-tables').glob('*.json'):
            t = json.loads(path.read_text())
            if 'fragments' in t:
                tables[t['id']] = t
        cells = {c['id']: (t, row, c) for t in tables.values()
                 for f in t['fragments'] for row in f['rows'] for c in row['cells']}
        for profile in self.profiles:
            for o in profile['table_occurrences']:
                t, row, cell = cells[o['cell_id']]
                self.assertEqual(o['table_id'], t['id'])
                for key in ('work_id', 'book_id', 'chapter_id'):
                    self.assertEqual(o[key], t['source'][key])
                self.assertEqual(o['source_id'], t['source']['id'])
                self.assertEqual(o['source_revision'], t['source']['revision'])
                self.assertEqual(o['quote'], cell['text'])
                self.assertEqual(o['year'], row['year'])
                self.assertIn(o['mention'], cell['person_mentions'])


if __name__ == '__main__':
    unittest.main()
