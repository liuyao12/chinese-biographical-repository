# coding: utf-8
import json
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def cells(number):
    table = json.loads((ROOT / ('data/historical-tables/shiji-%03d.json' % number)).read_text())
    return [cell for fragment in table['fragments'] for row in fragment['rows'] for cell in row['cells']]
class TablePersonIdentityTests(unittest.TestCase):
    def test_all_ten_tables_have_inline_person_markup(self):
        for number in range(13, 23):
            with self.subTest(number=number):
                self.assertTrue(any(cell['person_mentions'] for cell in cells(number)))
    def test_two_shang_taidings_remain_distinct(self):
        people = {mention['person_id'] for cell in cells(13) for mention in cell['person_mentions'] if mention['surface'] == '太丁'}
        self.assertEqual(people, {'tlt_5h1_n6y', 'bnu_h9l_z1o'})
    def test_han_king_xin_is_not_huaiyin_general(self):
        cell = next(cell for cell in cells(17) if '初王韓信元年' in cell['text'])
        self.assertEqual(cell['person_mentions'][0]['person_id'], 'hm1_rqr_l9u')
        other = {mention['person_id'] for cell in cells(16) for mention in cell['person_mentions'] if mention['surface'] == '韓信'}
        self.assertEqual(other, {'ofc_8ei_jb7'})
    def test_titled_same_name_in_different_fiefs_is_not_merged(self):
        people = {mention['person_id'] for cell in cells(21) for mention in cell['person_mentions'] if mention['surface'] == '劉成'}
        self.assertGreaterEqual(len(people), 2)
