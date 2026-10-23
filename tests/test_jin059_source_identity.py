# coding: utf-8
"""Fixed received text and event-level identity links for the two 059 units."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / 'source-evidence/jin059-jiong-yi-source'


def read(path):
    return json.loads(path.read_text())


class Jin059SourceIdentityTests(unittest.TestCase):
    def test_exact_received_text_and_person_spans(self):
        raw_bytes = (ROOT / 'sources/calendar-context/jinshu059-fixed2650517.wikitext').read_bytes()
        raw = raw_bytes.decode('utf-8')
        for key, count in [('jiong', 18), ('yi', 9)]:
            chapter = read(ROOT / ('corpus/jinshu/059-' + key + '.json'))
            projection = read(EVIDENCE / (key + '-projection.json'))
            self.assertEqual(hashlib.sha256(raw_bytes).hexdigest(), projection['raw_file_sha256'])
            self.assertEqual(len(chapter['paragraphs']), count)
            for paragraph in chapter['paragraphs']:
                positions = projection['paragraph_raw_positions'][paragraph['id']]
                self.assertEqual(''.join(raw[i] for i in positions), paragraph['text'])
                for mention in paragraph['mentions']:
                    self.assertEqual(paragraph['text'][mention['start']:mention['end']], mention['surface'])

    def test_qi_and_changsha_are_distinct_and_parallel_qi_refers_to_jiong(self):
        jiong = read(ROOT / 'corpus/jinshu/059-jiong.json')['paragraphs'][0]['mentions'][0]['person_id']
        yi = read(ROOT / 'corpus/jinshu/059-yi.json')['paragraphs'][0]['mentions'][0]['person_id']
        self.assertNotEqual(jiong, yi)
        chapter = read(ROOT / 'corpus/jinshu/043-wangyan.json')
        mentions = {m['id']: m for p in chapter['paragraphs'] for m in p['mentions']}
        for mid in ['c-jinshu-043-wangyan:p006:m0044', 'c-jinshu-043-wangyan:p006:m0063']:
            self.assertEqual(mentions[mid]['person_id'], jiong)

    def test_sunhui_direct_events_and_complete_intervening_letter(self):
        bridge = read(EVIDENCE / 'sunhui071-bridge.json')
        raw = (ROOT / bridge['source']['raw_file']).read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), bridge['source']['raw_file_sha256'])
        decoded = raw.decode('utf-8')
        unit = bridge['complete_unit']
        self.assertEqual(decoded[unit['raw_start']:unit['raw_end']], unit['complete_raw'])
        self.assertEqual(len(unit['paragraphs']), 8)
        self.assertIn('秦秘之', unit['complete_raw'])
        for endpoint in ['existing059', 'existing061']:
            item = bridge[endpoint]
            current = read(ROOT / item['chapter_path'])
            current_paragraphs = {p['id']: p for p in current['paragraphs']}
            for paragraph in item.get('paragraphs', [item.get('paragraph')]):
                self.assertEqual(current_paragraphs[paragraph['id']]['text'], paragraph['text'])
        for link in bridge['links']:
            paragraph = next(p for p in unit['paragraphs'] if p['id'] == link['new_paragraph_id'])
            self.assertIn(link['new_quote'], paragraph['text'])
        chapters = [read(ROOT / 'corpus/jinshu/059-jiong.json'), read(ROOT / 'corpus/jinshu/061-zhou-family.json')]
        for chapter in chapters:
            names = [m for p in chapter['paragraphs'] for m in p['mentions'] if m['surface'] == '孫惠']
            self.assertTrue(names)
            self.assertEqual({m['person_id'] for m in names}, {bridge['person_id']})
        self.assertFalse(bridge['human_reviewed'])


if __name__ == '__main__':
    unittest.main()
