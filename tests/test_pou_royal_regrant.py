# coding: utf-8
import copy
import json
import unittest
from pathlib import Path
from scripts.royal_transfers import royal_transfer_errors
from scripts.noble_transfers import noble_transfer_errors

ROOT = Path(__file__).resolve().parents[1]


def read(f):
    return json.loads((ROOT / f).read_text())


class PouRoyalRegrantTests(unittest.TestCase):
    def setUp(self):
        self.chapter = read('corpus/jinshu/064.json')
        self.paragraphs = {p['id']: (self.chapter['id'], p) for p in self.chapter['paragraphs']}
        self.mentions = {m['id']: (self.chapter['id'], p['id'], m)
                         for p in self.chapter['paragraphs'] for m in p['mentions']}
        self.holdings = {h['id']: h for h in read('corpus/jinshu/064-titles.json')['holdings']}
        self.h = self.holdings['th-jinshu064-pou-langye-regrant']
        self.previous = self.holdings[self.h['transfer_basis']['previous_holding_id']]

    def errors(self, h=None, holdings=None):
        return royal_transfer_errors(self.h if h is None else h,
                                     self.holdings if holdings is None else holdings,
                                     self.paragraphs, self.mentions)

    def test_actual_rank_word_and_elided_realm_are_separate(self):
        self.assertEqual(self.errors(), [])
        self.assertEqual(self.h['title'], '王')
        self.assertEqual(self.h['transfer_basis']['source_term'], '更封裒琅邪')
        self.assertEqual(self.h['jurisdictions'][0]['source_name'], '琅邪')
        a = self.h['attestations'][0]
        p = self.paragraphs[a['paragraph_id']][1]
        self.assertEqual(p['text'][a['start']:a['end']], '王')
        self.assertEqual(a['usage'], 'retrospective')
        self.assertIsNone(self.h['effective_period']['start']['date_expression'])

    def test_previous_unknown_title_is_not_uncles_changle_title(self):
        self.assertEqual(noble_transfer_errors(self.previous, self.holdings,
                                               self.paragraphs, self.mentions), [])
        self.assertIsNone(self.previous['transfer_basis']['previous_holding_id'])
        self.assertEqual(self.previous['transfer_basis']['source_term'], '徙封宣城郡公')

    def test_fabricated_title_realm_and_epithet_are_rejected(self):
        for key, value in [('title', '琅邪王'), ('title', '孝王')]:
            h = copy.deepcopy(self.h)
            h[key] = value
            self.assertTrue(self.errors(h))
        h = copy.deepcopy(self.h)
        h['transfer_basis']['source_term'] = '更封裒琅邪王'
        self.assertTrue(self.errors(h))
        h = copy.deepcopy(self.h)
        h['jurisdictions'][0]['source_name'] = '宣城'
        self.assertTrue(self.errors(h))

    def test_different_person_or_wrong_rank_anchor_is_rejected(self):
        h = copy.deepcopy(self.h)
        h['person_id'] = 'dkn_ge4_286_AAAAAAB'
        self.assertTrue(self.errors(h))
        h = copy.deepcopy(self.h)
        h['transfer_basis']['rank_mention_id'] = h['transfer_basis']['actor_mention_id']
        self.assertTrue(self.errors(h))
        h = copy.deepcopy(self.h)
        h['attestations'][0]['start'] += 1
        self.assertTrue(self.errors(h))

    def test_previous_end_must_be_same_transfer_not_death(self):
        holdings = copy.deepcopy(self.holdings)
        holdings[self.previous['id']]['effective_period']['end']['event_type'] = 'death'
        self.assertTrue(self.errors(holdings=holdings))
        holdings = copy.deepcopy(self.holdings)
        holdings[self.previous['id']]['effective_period']['end']['date_expression'] = '建武元年'
        self.assertTrue(self.errors(holdings=holdings))

    def test_lifetime_rank_cannot_be_attested_as_posthumous_epithet(self):
        h = copy.deepcopy(self.h)
        h['attestations'][0]['usage'] = 'narrative'
        self.assertTrue(self.errors(h))
        h = copy.deepcopy(self.h)
        h['attestations'][0]['date_expression'] = '建武元年'
        self.assertTrue(self.errors(h))


if __name__ == '__main__':
    unittest.main()
