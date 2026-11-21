import copy
import hashlib
import json
from pathlib import Path
import unittest

from scripts.liang021_print_columns import errors as print_errors
from scripts.person_ids import family_path_errors


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = 'source-evidence/qi020-wang-consorts/'
WITNESSES = [('nanqishu', '020', 'wyd'), ('nanshi', '011', 'izumo')]


def read(path):
    return json.loads((ROOT / path).read_bytes())


class QiConsorts(unittest.TestCase):
    def test_each_primary_comparison_reproduces_both_passages(self):
        for slug in ('wangshaoming', 'wangshunhua'):
            for work, volume, unused in WITNESSES:
                with self.subTest(slug=slug, work=work):
                    chapter = read(f'corpus/{work}/{volume}-{slug}.json')
                    paragraph, = chapter['paragraphs']
                    proof = read(EVIDENCE + work + '-' + slug + '.json')
                    self.assertEqual(len(proof['comparisons']), 12)
                    for row in proof['comparisons']:
                        self.assertEqual(paragraph['text'][row['start_codepoint']:row['end_codepoint']], row['source_quote'])
                        raw = (ROOT / row['path']).read_bytes()
                        self.assertEqual(hashlib.sha256(raw).hexdigest(), row['sha256'])
                        self.assertEqual(raw.decode()[row['raw_start']:row['raw_end']], row['reading'])

    def test_title_name_and_separate_daughters(self):
        received = read(EVIDENCE + 'nanshi-wangshaoming.json')
        self.assertIn('紹明', received['heading'])
        people = {p['id']: p for p in read('registry/persons.json')['persons']}
        consort = people[received['source_person_id']]
        other = people['7r6_k52_qji_ABAAAAEBAC']
        self.assertIn('韶明', consort['label'])
        self.assertIn('江夏王鋒', other['label'])
        self.assertNotEqual(consort['id'], other['id'])
        self.assertEqual(consort['family_path']['parent_person_id'], '7r6_k52_qji_ABAAAAEBA')
        shunhua = people[read(EVIDENCE + 'nanshi-wangshunhua.json')['source_person_id']]
        path = shunhua['family_path']
        self.assertEqual(path['ancestor_person_id'], '7r6_k52_qji_ABAAAAEAA')
        self.assertEqual(path['intermediate_person_ids'], [None])
        self.assertEqual(family_path_errors(shunhua['id'], path), [])

    def test_print_indices_and_original_images(self):
        for work, volume, edition in WITNESSES:
            for slug in ('wangshaoming', 'wangshunhua'):
                with self.subTest(work=work, slug=slug):
                    chapter = read(f'corpus/{work}/{volume}-{slug}-{edition}.json')
                    self.assertEqual(print_errors(chapter, ROOT), [])
                    proof = read(chapter['annotation']['print_projection_ref'])
                    for image in proof['images']:
                        self.assertRegex(image['capture_sha256'], r'^[0-9a-f]{64}$')
                        self.assertEqual(image['source_url'], f"{proof['pdf_url']}#page={image['pdf_page']}")
                    bad = copy.deepcopy(chapter)
                    bad['paragraphs'][0]['source_position']['column_projection'][0]['column_from_right'] += 1
                    self.assertTrue(print_errors(bad, ROOT))
        proof = read('source-evidence/nan011-wangshaoming-izumo/izumo-reading.json')
        self.assertEqual([(x['digital'], x['printed']) for x in proof['differences']], [('郁', '鬱')])

    def test_baling_is_the_later_witness_reading(self):
        proof = read(EVIDENCE + 'huiyao-comparison.json')
        manuscript = proof['image']
        self.assertRegex(manuscript['capture_sha256'], r'^[0-9a-f]{64}$')
        self.assertEqual(manuscript['source_url'], f"{proof['pdf_url']}#page=6")
        row, = [r for r in proof['readings'] if '巴陵' in r['reading']]
        self.assertEqual((row['half'], row['column_from_right'], row['reading']), ('左', 4, '帝禪位降為巴陵王妃'))
        for work, volume, edition in WITNESSES:
            for suffix in ('', '-' + edition):
                chapter = read(f'corpus/{work}/{volume}-wangshunhua{suffix}.json')
                self.assertNotIn('巴陵', chapter['paragraphs'][0]['text'])
                self.assertIn('后降為妃', chapter['paragraphs'][0]['text'])


if __name__ == '__main__':
    unittest.main()
