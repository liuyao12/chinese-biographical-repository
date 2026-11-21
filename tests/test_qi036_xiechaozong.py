import json
import unittest
from copy import deepcopy
from pathlib import Path

from scripts.qi036_xiechaozong import errors


ROOT = Path(__file__).resolve().parents[1]


def chapter(stem):
    return json.loads((ROOT / 'corpus/nanqishu' / (stem + '.json')).read_text())


class ChaozongReading(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.digital = chapter('036-xiechaozong')
        cls.printed = chapter('036-xiechaozong-wyd')

    def test_fixed_witnesses_and_transposed_name(self):
        for record in (self.digital, self.printed):
            self.assertEqual(errors(record, ROOT), [])
        for record, clause in ((self.digital, '超宗元嘉末得還'), (self.printed, '元嘉末超宗得還')):
            p = record['paragraphs'][0]
            index = p['text'].index(clause) + clause.index('超宗')
            m = next(m for m in p['mentions'] if m['start'] == index)
            self.assertEqual((m['surface'], m['person_id']), ('超宗', 'aa6_83c_juy_CDAABA'))

    def test_two_memorials_and_three_different_outcomes(self):
        record = deepcopy(self.printed)
        row = next(r for r in record['annotation']['narrative_readings'] if r['event_type'] == 'death_in_custody')
        row['person_ids'] = ['aa6_83c_juy_CDAABAA']
        self.assertTrue(errors(record, ROOT))
        self.assertIn('臣司馬侃', self.digital['paragraphs'][12]['text'])
        self.assertIn('請杖督五十，奪勞百日', self.digital['paragraphs'][14]['text'])

    def test_music_treatise_and_printed_variant(self):
        music = chapter('011-xiechaozong')
        self.assertIn('太廟登歌宜用司徒褚淵，餘悉用黃門郎謝超宗辭', music['paragraphs'][0]['text'])
        self.assertIn('以彰深\uf039', self.digital['paragraphs'][12]['text'])
        self.assertIn('以彰深諐', self.printed['paragraphs'][12]['text'])
        self.assertIn('何曇秀等十人', self.printed['paragraphs'][4]['text'])

    def test_same_name_different_office_and_dynasty(self):
        official = next(m for m in self.digital['paragraphs'][3]['mentions'] if m['surface'] == '劉康')
        self.assertNotEqual(official['person_id'], '5yv_wvs_bn0')
        cases = self.digital['annotation']['source_reading_cases']
        self.assertTrue(any(c['person_id'] == official['person_id'] and '山陽公劉康' in c['reading'] for c in cases))
