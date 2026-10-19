# coding: utf-8
import copy
import json
import unittest
from pathlib import Path
from scripts.posthumous_gifts import posthumous_gift_valid
ROOT = Path(__file__).resolve().parents[1]

class ContinuedGift(unittest.TestCase):
    def setUp(self):
        def read(suffix):
            return json.loads((ROOT / ('corpus/jinshu/076-wangbiaozhi' + suffix + '.json')).read_text())
        c = read('')
        self.paragraphs = {p['id']: (c['id'], p) for p in c['paragraphs']}
        self.mentions = {m['id']: (c['id'], p['id'], m) for p in c['paragraphs'] for m in p['mentions']}
        self.events = {e['id']: e for e in read('-life-events')['events']}
        self.h = next(h for h in read('-titles')['holdings'] if h['mode'] == 'posthumous_grant')
    def valid(self, h=None, events=None):
        return posthumous_gift_valid(h or self.h, self.paragraphs, self.mentions, self.events if events is None else events)
    def test_omitted_recipient_has_death_and_adjacent_subject_evidence(self):
        self.assertTrue(self.valid())
        self.assertEqual(self.h['title'], '光祿')
        self.assertIsNone(self.h['effective_period']['start']['date_expression'])
    def test_no_other_person_death_or_missing_event(self):
        self.assertFalse(self.valid(events={}))
        events = copy.deepcopy(self.events)
        events[self.h['posthumous_basis']['death_event_id']]['person_id'] = 'another'
        self.assertFalse(self.valid(events=events))
    def test_cannot_add_ungranted_companion_office(self):
        h = copy.deepcopy(self.h); h['title'] = '儀同三司'
        self.assertFalse(self.valid(h))
    def test_cannot_change_previous_subject_or_death_quote(self):
        for field in ['person_mention_id', 'quote']:
            h = copy.deepcopy(self.h)
            h['posthumous_basis']['evidence'][0]['context'][field] = 'wrong'
            self.assertFalse(self.valid(h))
        events = copy.deepcopy(self.events)
        events[self.h['posthumous_basis']['death_event_id']]['evidence'][0]['quote'] = '別段'
        self.assertFalse(self.valid(events=events))
if __name__ == '__main__':
    unittest.main()
