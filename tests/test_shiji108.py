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
if __name__ == '__main__':
    unittest.main()
