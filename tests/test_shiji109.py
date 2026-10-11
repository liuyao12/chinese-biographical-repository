import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class LiGuangSourceTests(unittest.TestCase):
    def test_later_general_grant_has_its_own_anchor(self):
        chapter = json.loads((ROOT / 'corpus/shiji/109.json').read_text())
        titles = json.loads((ROOT / 'corpus/shiji/109-titles.json').read_text())
        holding = next(h for h in titles['holdings'] if h['id'] == 'th-shiji109-036')
        anchor = holding['attestations'][0]
        text = chapter['paragraphs'][4]['text']
        self.assertEqual(text[anchor['start'] - 3:anchor['end']], '衞尉爲將軍')
        self.assertEqual(holding['mode'], 'grant')

    def test_subordinate_general_does_not_become_li_guang_office(self):
        titles = json.loads((ROOT / 'corpus/shiji/109-titles.json').read_text())
        guard = next(h for h in titles['holdings'] if h['id'] == 'th-shiji109-034')
        self.assertEqual(guard['title'], '護軍將軍')
        self.assertNotEqual(guard['person_id'], '27j_f4p_jwp')
        commoner = next(h for h in titles['holdings'] if h['id'] == 'th-shiji109-039')
        self.assertEqual(commoner['mode'], 'demotion')
        self.assertEqual(commoner['effective_period']['end']['status'], 'unknown')
