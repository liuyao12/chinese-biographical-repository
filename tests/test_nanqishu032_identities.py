# coding: utf-8
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class WangYanzhiIdentities(unittest.TestCase):
    def setUp(self):
        self.chapter = json.loads((ROOT / 'corpus/nanqishu/032.json').read_text())
        self.decisions = json.loads(
            (ROOT / 'corpus/nanqishu/032-identities.json').read_text())['decisions']

    def test_all_decisions_bind_actual_mentions_and_primary_references(self):
        mentions = {m['id']: m for p in self.chapter['paragraphs'] for m in p['mentions']}
        self.assertEqual(len(self.decisions), 9)
        for d in self.decisions:
            self.assertIs(d['human_reviewed'], False)
            self.assertIsNone(d['model'])
            for mid in d['identification_basis']['target_mention_ids']:
                self.assertEqual(mentions[mid]['person_id'], d['person_id'])
            self.assertTrue(d['references'])
            for r in d['references']:
                self.assertIs(r['image_verified'], False)
                self.assertIn('oldid=', r['url'])
                self.assertTrue(r['quote'])

    def test_jinxi_is_contextual_successor_not_automatic_name_equivalence(self):
        d = next(d for d in self.decisions if d['id'] == 'd-nanqishu032-jinxi')
        self.assertEqual(d['confidence_level'], 'medium')
        self.assertEqual(d['scope'], 'same_chapter')
        quotes = ''.join(r['quote'] for r in d['references'])
        self.assertIn('北奔', quotes)
        self.assertIn('燮襲爵', quotes)
        self.assertNotIn('normalized_date', d)

    def test_same_generic_royal_words_do_not_merge_song_and_qi(self):
        by_id = {d['id']: d for d in self.decisions}
        emperors = [by_id['d-nanqishu032-' + key] for key in
                    ['song-ming', 'qi-taizu', 'qi-shizu']]
        self.assertEqual(len({d['person_id'] for d in emperors}), 3)
        target_sets = [set(d['identification_basis']['target_mention_ids']) for d in emperors]
        self.assertFalse(target_sets[0] & target_sets[1])
        self.assertFalse(target_sets[1] & target_sets[2])


if __name__ == '__main__':
    unittest.main()
