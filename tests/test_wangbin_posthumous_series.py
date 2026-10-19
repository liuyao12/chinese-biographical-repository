# coding: utf-8
import copy
import json
import unittest
from pathlib import Path
from scripts.posthumous_gifts import posthumous_gift_valid

ROOT = Path(__file__).resolve().parents[1]

class WangBinPosthumousSeries(unittest.TestCase):
    def setUp(self):
        c = json.loads((ROOT / 'corpus/jinshu/076-wangbin.json').read_text())
        self.paragraphs = {p['id']: (c['id'], p) for p in c['paragraphs']}
        self.mentions = {m['id']: (c['id'], p['id'], m) for p in c['paragraphs'] for m in p['mentions']}
        self.holdings = [h for h in json.loads((ROOT / 'corpus/jinshu/076-wangbin-titles.json').read_text())['holdings'] if h['mode'] == 'posthumous_grant']

    def test_three_coordinated_gifts_keep_source_and_unknown_year(self):
        self.assertEqual({h['title'] for h in self.holdings}, {'特進', '衛將軍', '散騎常侍'})
        for h in self.holdings:
            self.assertTrue(posthumous_gift_valid(h, self.paragraphs, self.mentions), h['id'])
            self.assertIsNone(h['effective_period']['start']['date_expression'])
            self.assertNotIn('normalized_date', h['effective_period']['start'])

    def test_cannot_promote_prior_office_or_change_recipient(self):
        h = copy.deepcopy(self.holdings[0])
        h['title'] = '尚書右僕射'
        self.assertFalse(posthumous_gift_valid(h, self.paragraphs, self.mentions))
        h = copy.deepcopy(self.holdings[0])
        h['person_id'] = 'another-person'
        self.assertFalse(posthumous_gift_valid(h, self.paragraphs, self.mentions))

    def test_cannot_silently_rewrite_gift_or_death_phrase(self):
        for key, value in [('grant_term', '追贈特進、衛將軍，加散騎常侍'), ('death_term', '薨')]:
            h = copy.deepcopy(self.holdings[0])
            h['posthumous_basis'][key] = value
            self.assertFalse(posthumous_gift_valid(h, self.paragraphs, self.mentions))

if __name__ == '__main__':
    unittest.main()
