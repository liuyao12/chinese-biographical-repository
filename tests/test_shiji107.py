"""Regression checks for source distinctions that affect generated lineage data."""
import json
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

class WeiqiSourceTests(unittest.TestCase):
    def load(self, suffix):
        return json.loads((ROOT / ('corpus/shiji/107' + suffix + '.json')).read_text())

    def test_successor_usage_year_does_not_become_accession_year(self):
        holdings = self.load('-titles')['holdings']
        h = next(h for h in holdings if h['interpretation_note'].startswith('子恬嗣'))
        self.assertEqual(h['effective_period']['start']['date_expression'], '其春')
        self.assertNotIn('normalized_date', h['effective_period']['start'])
        self.assertEqual(h['effective_period']['end']['status'], 'unknown')
        self.assertEqual(h['attestations'][0]['normalized_date']['era_year'], 126)
        self.assertEqual(h['attestations'][0]['date_expression'], '元朔三年')

    def test_palace_assignment_is_not_invented(self):
        hs = [h for h in self.load('-titles')['holdings'] if h['title'] == '衛尉']
        self.assertEqual(len(hs), 2)
        self.assertEqual(len({h['person_id'] for h in hs}), 2)
        for h in hs:
            self.assertEqual(h['effective_period']['start']['status'], 'unknown')
            self.assertIn('不足以分配', h['interpretation_note'])

    def test_metaphorical_father_is_not_a_father_assertion(self):
        c = self.load('')
        self.assertIn('如父子然', c['paragraphs'][15]['text'])
        for a in self.load('-assertions')['assertions']:
            if a['predicate'] == 'father':
                self.assertFalse(any(e['paragraph_id'] == c['paragraphs'][15]['id'] for e in a['evidence']))

if __name__ == '__main__':
    unittest.main()
