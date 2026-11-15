import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class Shiji117WorkTitleSpans(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = json.loads((ROOT / 'corpus/shiji/117.json').read_text())
        cls.paragraph = next(p for p in cls.chapter['paragraphs'] if p['id'] == 'c-shiji-117-xiangru:p069')
        cls.review = next(r for r in cls.chapter['annotation']['work_reference_reviews']
                          if r['id'] == 'work-review-shiji117-xiangru-p069')
        cls.mentions = {m['id']: m for m in cls.paragraph['mentions']}

    def test_pending_titles_have_exact_independent_spans_and_preserve_overlapping_entities(self):
        expected = {
            '遺平陵侯書': ('c-shiji-117-xiangru:m069-0008',),
            '與五公子相難': ('c-shiji-117-xiangru:m069-0014',),
            '草木書': (),
        }
        self.assertEqual({x['surface'] for x in self.review['work_identity_pending']}, set(expected))
        for row in self.review['work_identity_pending']:
            surface = row['surface']
            start = self.paragraph['text'].index(surface)
            self.assertEqual(row['source_span'], {'start': start, 'end': start + len(surface), 'surface': surface})
            self.assertEqual(tuple(row['overlapping_mention_ids']), expected[surface])
            for mention_id in row['overlapping_mention_ids']:
                mention = self.mentions[mention_id]
                self.assertLess(start, mention['end'])
                self.assertLess(mention['start'], start + len(surface))
                self.assertEqual(self.paragraph['text'][mention['start']:mention['end']], mention['surface'])
        self.assertEqual(self.paragraph['text'], '相如他所著，若遺平陵侯書、與五公子相難、草木書篇不采，采其尤著公卿者云。')

if __name__ == '__main__':
    unittest.main()
