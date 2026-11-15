import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PERSON_ID = 'aa6_83c_juy_AAAA'
JINSHU_CHAPTER = 'c-jinshu-079-xielang-family'
SONGSHU_CHAPTER = 'c-songshu-044-xiehui'
SONGSHU_WYG_CHAPTER = 'c-songshu-044-wyd1739-xiehui'
SONGSHU_042_CHAPTER = 'c-songshu-042-wanghong'
JINSHU_MENTION = 'c-jinshu-079-xielang-family:phase6-line071:m0272'
SONGSHU_MENTION = 'c-songshu-044-xiehui:p001:m0000'
SONGSHU_WYG_MENTION = 'c-songshu-044-wyd1739-xiehui:p001:m0000'
SONGSHU_042_MENTION = 'c-songshu-042-wanghong:line061:m0071'


def read_json(path):
    return json.loads((ROOT / path).read_text())


def paragraph(path, paragraph_id):
    corpus = read_json(path)
    return next(p for p in corpus['paragraphs'] if p['id'] == paragraph_id)


class Jinshu079XiehuiCrossIdentityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.jinshu = read_json('corpus/jinshu/079-identities.json')
        cls.songshu_received = read_json('corpus/songshu/044-identities.json')
        cls.songshu = read_json('corpus/songshu/044-wyd1739-identities.json')
        cls.jin_decision = next(
            d for d in cls.jinshu['decisions']
            if d['id'] == 'd-phase6-079-aa6_83c_juy_AAAA'
        )
        cls.song_decision = next(
            d for d in cls.songshu['decisions']
            if d['id'] == 'd-song044-wyd-role-hui'
        )
        cls.song_received_decision = next(
            d for d in cls.songshu_received['decisions']
            if d['id'] == 'd-songshu044-xiehui-jinshu079'
        )

    def test_both_source_decisions_point_to_the_same_person_and_each_other(self):
        for decision in (self.jin_decision, self.song_decision, self.song_received_decision):
            self.assertEqual(decision['person_id'], PERSON_ID)
            self.assertEqual(decision['scope'], 'cross_chapter')
            self.assertEqual(decision['status'], 'contextual_provisional')
            self.assertFalse(decision['human_reviewed'])
            evidence_chapters = {e['chapter_id'] for e in decision['evidence']}
            self.assertEqual(set(decision['chapter_ids']), evidence_chapters)
            evidence_anchors = {e.get('person_mention_id') for e in decision['evidence']}
            self.assertTrue(all(anchor in evidence_anchors for anchor in
                                (JINSHU_MENTION, SONGSHU_MENTION,
                                 SONGSHU_WYG_MENTION, SONGSHU_042_MENTION)))
        self.assertIn(JINSHU_CHAPTER, self.song_decision['chapter_ids'])
        self.assertIn(SONGSHU_WYG_CHAPTER, self.jin_decision['chapter_ids'])
        self.assertIn(JINSHU_MENTION, self.song_decision['identification_basis']['target_mention_ids'])
        self.assertIn(SONGSHU_WYG_MENTION, self.jin_decision['identification_basis']['target_mention_ids'])
        self.assertIn(SONGSHU_MENTION, self.jin_decision['identification_basis']['target_mention_ids'])
        self.assertIn(JINSHU_MENTION, self.song_received_decision['identification_basis']['target_mention_ids'])

    def test_cross_source_evidence_quotes_and_mention_anchors_resolve(self):
        expected = {
            JINSHU_MENTION: ('corpus/jinshu/079.json',
                             'c-jinshu-079-xielang-family:phase6-line071', '謝晦'),
            SONGSHU_MENTION: ('corpus/songshu/044.json',
                              'c-songshu-044-xiehui:p001', '謝晦'),
            SONGSHU_WYG_MENTION: ('corpus/songshu/044-wyd1739.json',
                                  'c-songshu-044-wyd1739-xiehui:p001', '謝晦'),
            SONGSHU_042_MENTION: ('corpus/songshu/042.json',
                                  'c-songshu-042-wanghong:line061', '謝晦'),
        }
        for decision in (self.jin_decision, self.song_decision, self.song_received_decision):
            for evidence in decision['evidence']:
                path, expected_id, _ = expected.get(evidence.get('person_mention_id'), (None, None, None))
                if path is None:
                    continue
                source_paragraph = paragraph(path, expected_id)
                self.assertEqual(evidence['paragraph_id'], expected_id)
                self.assertIn(evidence['quote'], source_paragraph['text'])
                mention = next(m for m in source_paragraph['mentions']
                               if m['id'] == evidence['person_mention_id'])
                self.assertEqual(mention['surface'], '謝晦')
                self.assertEqual(mention['person_id'], PERSON_ID)
        for mention_id, (path, paragraph_id, surface) in expected.items():
            source_paragraph = paragraph(path, paragraph_id)
            mention = next(m for m in source_paragraph['mentions'] if m['id'] == mention_id)
            self.assertEqual(mention['surface'], surface)
            self.assertEqual(mention['person_id'], PERSON_ID)

    def test_rationale_uses_accession_and_family_evidence_without_turning_it_into_kinship(self):
        rationale = self.jin_decision['rationale']
        self.assertIn('宋受禪', rationale)
        self.assertIn('劉裕', rationale)
        self.assertIn('祖朗、父重、兄絢', rationale)
        self.assertIn('仍為 contextual_provisional', rationale)
        self.assertEqual(self.jin_decision['surfaces'], ['謝晦'])


if __name__ == '__main__':
    unittest.main()
