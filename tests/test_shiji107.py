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

    def test_emperor_reference_changes_with_narrative_time(self):
        p = self.load('')['paragraphs'][12]
        boundary = p['text'].index('今上初即位')
        early = [m for m in p['mentions'] if m['surface'] == '上' and m['start'] < boundary]
        late = [m for m in p['mentions'] if m['surface'] == '上' and m['start'] > boundary]
        self.assertEqual(len(early), 2)
        self.assertEqual({m['person_id'] for m in early}, {'4gj_xfa_r7s'})
        self.assertEqual({m['person_id'] for m in late}, {'gni_rru_0gw'})

    def test_quoted_deceased_emperor_is_not_current_emperor(self):
        p = self.load('')['paragraphs'][23]
        quoted = p['text'].index('便宜論上') + len('便宜論')
        m = next(m for m in p['mentions'] if m['start'] == quoted)
        self.assertEqual(m['person_id'], '4gj_xfa_r7s')
        for m in p['mentions']:
            if m['surface'] == '上':
                self.assertFalse(p['text'].startswith('上書', m['start']))

    def test_unqualified_dowager_keeps_two_candidates(self):
        c = self.load('')
        p = c['paragraphs'][6]
        m = next(m for m in p['mentions'] if m['surface'] == '太后')
        self.assertEqual(m['kind'], 'unresolved')
        self.assertIsNone(m['person_id'])
        case = next(case for case in c['annotation']['unresolved_identity_cases'] if p['id'] in case['paragraph_ids'])
        self.assertEqual(set(case['candidate_person_ids']), {'5u3_i3p_ngq', 'l26_mjw_rwe'})

if __name__ == '__main__':
    unittest.main()
