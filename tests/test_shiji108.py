import json
from pathlib import Path
import unittest
ROOT = Path(__file__).resolve().parents[1]
class HanSourceTests(unittest.TestCase):
    def load(self, suffix):
        return json.loads((ROOT / ('corpus/shiji/108' + suffix + '.json')).read_text())
    def test_li_guang_general_anchor_is_not_wei_qing_title(self):
        h = next(h for h in self.load('-titles')['holdings'] if h['id'] == 'th-shiji108-041')
        a = h['attestations'][0]
        p = next(p for p in self.load('')['paragraphs'] if p['id'] == a['paragraph_id'])
        self.assertEqual(p['text'][a['start']:a['end'] + 2], '將軍李廣')
        self.assertEqual(h['person_id'], 'njk_tl0_6h9')
    def test_acting_chancellor_and_unrealized_hu_sui_offer(self):
        hs = self.load('-titles')['holdings']
        acting = next(h for h in hs if h['id'] == 'th-shiji108-035')
        self.assertEqual(acting['appointment_role'], 'acting')
        self.assertFalse(any(h['person_id'] == 'hmj_pm8_38e' and h['title'] in ('漢相', '丞相') for h in hs))
    def test_wang_dowager_decision_does_not_resolve_jianyuan_occurrence(self):
        d = self.load('')
        p = d['paragraphs'][5]
        mention = next(m for m in p['mentions'] if m['surface'] == '太后')
        self.assertIsNone(mention['person_id'])
        self.assertEqual(mention['kind'], 'unresolved')
        e = next(e for e in self.load('-equivalences')['decisions'] if e['id'] == 'eq-shiji108-wang')
        self.assertNotIn(p['id'], [x['paragraph_id'] for x in e['evidence']])
    def test_hanguo_equivalence_contains_matching_appointment_evidence(self):
        e = next(e for e in self.load('-equivalences')['decisions'] if e['id'] == 'eq-shiji108-hanguo')
        self.assertIn('adb_4so_0qm', e['person_ids'])
        self.assertIn('6hy_i1z_hu2', e['person_ids'])
        appointment = [x for x in e['evidence'] if '建元六年' in x['quote']]
        self.assertEqual(len(appointment), 2)
        self.assertTrue(all('御史大夫' in x['quote'] for x in appointment))
if __name__ == '__main__':
    unittest.main()
