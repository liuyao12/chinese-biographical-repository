# coding: utf-8
import copy
import json
import unittest
from pathlib import Path
from scripts.posthumous_gifts import posthumous_gift_valid

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads((ROOT / path).read_text())


class BiographyPosthumousGiftTests(unittest.TestCase):
    def setUp(self):
        chapters = [load('corpus/jinshu/' + b + '.json') for b in ['032', '064']]
        self.paragraphs = {p['id']: (c['id'], p) for c in chapters for p in c['paragraphs']}
        self.mentions = {m['id']: (c['id'], p['id'], m) for c in chapters
                         for p in c['paragraphs'] for m in p['mentions']}
        self.events = {e['id']: e for b in ['032', '064']
                       for e in load('corpus/jinshu/' + b + '-life-events.json')['events']}
        self.holdings = [h for b in ['032', '064']
                         for h in load('corpus/jinshu/' + b + '-titles.json')['holdings']
                         if '-care-posthumous-' in h['id']]

    def valid(self, h, events=None):
        return posthumous_gift_valid(h, self.paragraphs, self.mentions,
                                    self.events if events is None else events)

    def test_deictic_named_and_topic_gifts_retain_real_recipients(self):
        self.assertEqual(len(self.holdings), 4)
        for h in self.holdings:
            self.assertTrue(self.valid(h), h['id'])
            self.assertIsNone(h['effective_period']['start']['date_expression'])
            self.assertEqual(h['mode'], 'posthumous_grant')

    def test_different_womans_death_cannot_support_pou_gift(self):
        for h in self.holdings:
            bad = copy.deepcopy(h)
            if h['person_id'] == 'dkn_ge4_286_AAAAAAAB':
                self.assertIn('le-jinshu064-shan-consort-death', self.events)
                bad['posthumous_basis']['death_event_id'] = 'le-jinshu064-shan-consort-death'
                self.assertFalse(self.valid(bad))
            self.assertFalse(self.valid(h, {}))

    def test_topic_and_recipient_must_belong_to_same_person(self):
        for h in self.holdings:
            b = h['posthumous_basis']
            p = self.paragraphs[h['evidence'][0]['paragraph_id']][1]
            other = next(m for m in p['mentions'] if m.get('person_id')
                         and m['person_id'] != h['person_id'])
            for key in ['topic_person_mention_id', 'recipient_person_mention_id']:
                bad = copy.deepcopy(h)
                bad['posthumous_basis'][key] = other['id']
                self.assertFalse(self.valid(bad), key)

    def test_moved_grant_title_and_death_anchor_are_rejected(self):
        for h in self.holdings:
            for key, value in [('grant_term', '贈不存在官'), ('death_term', '山氏薨'),
                               ('grant_recipient_kind', 'nearest_emperor')]:
                bad = copy.deepcopy(h)
                bad['posthumous_basis'][key] = value
                self.assertFalse(self.valid(bad))
            bad = copy.deepcopy(h)
            bad['attestations'][0]['start'] = 0
            self.assertFalse(self.valid(bad))

    def test_living_grants_cannot_use_posthumous_evidence(self):
        for h in self.holdings:
            bad = copy.deepcopy(h)
            bad['mode'] = 'grant'
            self.assertFalse(self.valid(bad))
        self.assertFalse(posthumous_gift_valid({'posthumous_basis': None}, {}, {}))


if __name__ == '__main__':
    unittest.main()
