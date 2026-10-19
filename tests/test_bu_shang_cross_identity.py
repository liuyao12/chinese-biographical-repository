import json
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
class BuShangCrossIdentityTests(unittest.TestCase):
    def test_contextual_mentions_share_bu_shang_identity(self):
        expected={'044.json':{'c-shiji-044-wei:p017','c-shiji-044-wei:p019'},'047.json':{'c-shiji-047-kong:p074'},'130.json':{'c-shiji-130-taishigong:p056'}}
        seen=0
        for filename,paragraphs in expected.items():
            for p in json.loads((ROOT/'corpus/shiji'/filename).read_text())['paragraphs']:
                if p['id'] not in paragraphs:continue
                names=[m for m in p['mentions'] if m['surface'] in ('子夏','卜子夏')]
                self.assertTrue(names)
                for m in names:self.assertEqual(m['person_id'],'z8l_wje_08d');seen+=1
        self.assertEqual(seen,4)
    def test_retired_candidates_are_removed_without_aliases(self):
        retired={'26r_t32_9rn','cuz_4hf_i52','qs4_045_sjd'}
        registry=json.loads((ROOT/'registry/persons.json').read_text())
        self.assertFalse(retired & {p['id'] for p in registry['persons']})
        for pid in retired:
            self.assertFalse((ROOT/'exports/persons'/f'{pid}.json').exists())
            self.assertFalse((ROOT/'data/corpus/profiles'/f'{pid}.json').exists())
        bundle=json.loads((ROOT/'exports/persons/z8l_wje_08d.json').read_text())
        self.assertEqual(bundle['id_aliases'],[])
        self.assertEqual(len(bundle['table_occurrences']),1)
        self.assertEqual(bundle['table_occurrences'][0]['table_cell_id'],'shiji-015-r070-c03')
        chapters={m['chapter_id'] for m in bundle['mentions']}
        self.assertTrue({'c-shiji-044-wei','c-shiji-047-kong','c-shiji-067-disciples','c-shiji-130-taishigong'}<=chapters)
    def test_unrelated_wang_shang_and_bu_shang_son_remain_distinct(self):
        people={p['id']:p for p in json.loads((ROOT/'registry/persons.json').read_text())['persons']}
        self.assertIn('4w5_b4e_vf5_AI',people)
        self.assertIn('z8l_wje_08d_A',people)
        self.assertNotEqual(people['4w5_b4e_vf5_AI']['label'],people['z8l_wje_08d']['label'])
