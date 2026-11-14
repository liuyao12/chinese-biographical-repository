import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PID = '74s_z7l_t28'
OLD = 'xp2_dxz_zcn'

def read(path):
    return json.loads((ROOT / path).read_text())

class FengJingCrossReading(unittest.TestCase):
    def test_three_received_mentions_share_identity_and_exact_source_positions(self):
        expected = {
            '084': {'c-shiji-084-qujia:m022-0128': '馮敬'},
            '118': {'c-shiji-118-huainan:m004-0010': '馮敬',
                    'c-shiji-118-huainan:m006-0004': '臣敬'},
        }
        for book, markers in expected.items():
            found = {}
            for p in read(f'corpus/shiji/{book}.json')['paragraphs']:
                for m in p['mentions']:
                    if m['id'] in markers:
                        self.assertEqual(m['person_id'], PID)
                        self.assertEqual(p['text'][m['start']:m['end']], markers[m['id']])
                        found[m['id']] = m['surface']
            self.assertEqual(found, markers)

    def test_parentage_disagreement_is_attributed_and_not_a_family_edge(self):
        person = next(p for p in read('registry/persons.json')['persons'] if p['id'] == PID)
        self.assertFalse(person.get('family_path'))
        decision = next(d for d in read('corpus/shiji/118-identities.json')['decisions']
                        if d['id'] == 'd-shiji118-fengjing-jia-context')
        dispute = decision['parentage_reference_disagreement']
        self.assertFalse(dispute['primary_table_checked'])
        self.assertEqual(dispute['default_graph_action'], 'omit_unproved_parent_edge')
        self.assertEqual([(c['attribution'], c['polarity']) for c in dispute['source_claims']],
                         [('如淳', 'affirms_parentage'), ('宋祁', 'denies_parentage')])
        for claim in dispute['source_claims']:
            ref = next(r for r in decision['references'] if r['url'] == claim['reference_url'])
            span = claim['raw_quote_span']
            self.assertEqual(ref['quote'][span['start']:span['end']], claim['source_term'])
            self.assertEqual(claim['status'], 'not_adopted_as_genealogical_edge')
        self.assertTrue(any('奏淮南' in r['quote'] for r in decision['references']))

    def test_received_punctuation_and_source_wording_remain_separate_from_reading(self):
        p = next(p for p in read('corpus/shiji/118.json')['paragraphs']
                 if p['id'] == 'c-shiji-118-huainan:p004')
        self.assertIn('典客臣馮敬、行御史大夫事宗正臣逸', p['text'])
        records = read('corpus/shiji/118-titles.json')['holdings']
        acting = [r for r in records if r.get('person_id') == PID and r.get('source_term') == '行御史大夫事']
        self.assertEqual(len(acting), 1)
        self.assertEqual(acting[0]['punctuation_attribution']['preferred_segmentation'],
                         '典客臣馮敬行御史大夫事、宗正臣逸')

    def test_retired_identity_has_no_registry_or_export_entry(self):
        self.assertNotIn(OLD, {p['id'] for p in read('registry/persons.json')['persons']})
        for folder in ['exports/persons', 'data/corpus/profiles']:
            self.assertFalse((ROOT / folder / (OLD + '.json')).exists())

if __name__ == '__main__':
    unittest.main()
