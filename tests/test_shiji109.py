import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class LiGuangSourceTests(unittest.TestCase):
    def test_wang_shuo_anchor_does_not_consume_era_name(self):
        chapter = json.loads((ROOT / 'corpus/shiji/109.json').read_text())
        paragraph = chapter['paragraphs'][10]
        anchors = [m for m in paragraph['mentions'] if m['person_id'] == '224_en7_aho']
        self.assertEqual([m['surface'] for m in anchors], ['王朔', '朔', '朔'])
        self.assertTrue(all(paragraph['text'][m['start'] - 1:m['start']] != '元' for m in anchors))

    def test_received_chariot_title_variant_is_preserved(self):
        titles = json.loads((ROOT / 'corpus/shiji/109-titles.json').read_text())
        holding = next(h for h in titles['holdings'] if h['id'] == 'th-shiji109-056')
        self.assertEqual(holding['title'], '輕車將車')
        self.assertEqual(holding['effective_period']['start']['normalized_date']['era_year'], 124)
        self.assertEqual(holding['effective_period']['end']['status'], 'unknown')

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
