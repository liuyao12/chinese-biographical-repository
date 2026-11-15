import copy
import json
import unittest
from pathlib import Path

from scripts.song051_p014_p017_life_dates import valid
from scripts.validate_corpus import normalized_date_errors


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = json.loads((ROOT / 'corpus/songshu/051-wyd1739.json').read_text(encoding='utf-8'))
LIFE = json.loads((ROOT / 'corpus/songshu/051-wyd1739-life-events.json').read_text(encoding='utf-8'))
CHAPTERS = {CHAPTER['id']: CHAPTER}
EVENTS = {event['id']: event for event in LIFE['events']}


class Song051ContextualLifeDatesTest(unittest.TestCase):
    def event(self, event_id):
        return copy.deepcopy(EVENTS[event_id])

    def test_all_four_fixed_dates_pass_specific_and_common_validation(self):
        ids = (
            'le-song051-p014-yizong-death',
            'le-song051-p017-m0062-death',
            'le-song051-p017-m0076-death',
            'le-song051-p017-m0077-death',
        )
        for event_id in ids:
            with self.subTest(event=event_id):
                event = self.event(event_id)
                date = event['normalized_date']
                self.assertTrue(valid(date, event, CHAPTERS, ROOT, 'life_event'))
                self.assertEqual([], normalized_date_errors(date, CHAPTERS, ROOT, event, 'life_event'))

    def test_rejects_missing_or_tampered_yuanhui_row_receipt(self):
        event = self.event('le-song051-p017-m0062-death')
        date = event['normalized_date']
        next(ref for ref in date['references'] if ref.get('quote') == '元徽')['fixed_row_reference']['sha256'] = '0' * 64
        self.assertFalse(valid(date, event, CHAPTERS, ROOT, 'life_event'))

    def test_rejects_wrong_yuanhui_era_span_or_conversion(self):
        event = self.event('le-song051-p017-m0062-death')
        date = event['normalized_date']
        ref = next(ref for ref in date['references'] if ref.get('quote') == '元徽')
        ref['columns']['last_year'] = '476'
        self.assertFalse(valid(date, event, CHAPTERS, ROOT, 'life_event'))
        event = self.event('le-song051-p017-m0062-death')
        event['normalized_date']['year'] = 476
        self.assertFalse(valid(event['normalized_date'], event, CHAPTERS, ROOT, 'life_event'))

    def test_rejects_broken_biographical_context(self):
        event = self.event('le-song051-p017-m0062-death')
        event['contextual_date_basis']['accession_anchor'] = '孝武帝即位'
        self.assertFalse(valid(event['normalized_date'], event, CHAPTERS, ROOT, 'life_event'))

    def test_yuanjia_omitted_era_year_requires_preceding_same_biography_era(self):
        event = self.event('le-song051-p014-yizong-death')
        chapter = copy.deepcopy(CHAPTER)
        para = next(p for p in chapter['paragraphs'] if p['id'].endswith(':p014'))
        para['text'] = para['text'].replace('元嘉八年', '泰始八年')
        self.assertFalse(valid(event['normalized_date'], event, {chapter['id']: chapter}, ROOT, 'life_event'))

    def test_yuanhui_row_does_not_claim_raw_response_hash(self):
        row = json.loads((ROOT / 'source-evidence/song051-wyd1739-zongshi/p014-p017-yuanhui-calendar-row.json').read_text())
        self.assertEqual('2026-11-13', row['accessed_on'])
        self.assertIn('元徽 | 473 | 477', row['row_text'])
        self.assertNotIn('raw_response_sha256', row)
        self.assertNotIn('raw_html_sha256', row)


if __name__ == '__main__':
    unittest.main()
