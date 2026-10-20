import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads((ROOT / path).read_text())


class WangYiSourceBoundaries(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        chapter = read('corpus/songshu/046-wangyi.json')
        cls.paragraphs = {p['id'].rsplit(':', 1)[1]: p for p in chapter['paragraphs']}
        cls.relations = read('corpus/songshu/046-wangyi-assertions.json')['assertions']

    def test_wangji_in_capital_argument_is_not_a_person(self):
        p = self.paragraphs['p007']
        start = p['text'].index('王基')
        self.assertFalse(any(m['start'] < start + 2 and m['end'] > start
                             for m in p['mentions']))

    def test_self_reported_distant_ancestor_does_not_become_parent(self):
        p = self.paragraphs['p001']
        distant = next(m['person_id'] for m in p['mentions'] if m['surface'] == '懋')
        self.assertFalse(any(a['object_person_id'] == distant for a in self.relations))
        father = next(a for a in self.relations
                      if a['subject_person_id'] == '864_b79_ed2' and a['predicate'] == 'father')
        self.assertEqual(father['qualifiers']['source_term'], '父苖')
        self.assertEqual(father['object_person_id'], 'ymz_r2c_cek')

    def test_unresolved_zhangchang_is_not_a_claim_of_distinct_people(self):
        review = read('source-evidence/song046-wangyi-recovery-v2/zhangchang-candidates.json')
        self.assertIsNone(review['same_person'])
        self.assertIsNone(review['distinct_people'])
        self.assertFalse(review['reference_only']['original_scholar_work_examined'])
        p = self.paragraphs['p003']
        self.assertEqual(next(m['person_id'] for m in p['mentions']
                              if m['surface'] == '張暢'), 'q7q_j3y_nhj')

    def test_variant_year_and_later_supplement_remain_visible(self):
        self.assertTrue(self.paragraphs['p008']['text'].startswith('元嘉三年'))
        layers = read('source-evidence/song046-wangyi-recovery/source-layers.json')
        self.assertEqual(layers['selected_biography'], 'received_later_supplemented_biography')
        self.assertTrue(all(n['image_verified'] is False
                            for n in layers['qualifying_witness_notes']))


if __name__ == '__main__':
    unittest.main()
