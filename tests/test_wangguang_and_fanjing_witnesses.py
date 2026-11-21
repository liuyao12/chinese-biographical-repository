import hashlib
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


def read(relative):
    return json.loads((ROOT / relative).read_bytes())


class WangGuangWitnesses(unittest.TestCase):
    def test_comparisons_recover_fixed_characters(self):
        proof = read('source-evidence/jin096-wangguang/wangguangnu-reading.json')
        chapter = read('corpus/jinshu/096-wangguangnu.json')
        paragraph, = chapter['paragraphs']
        self.assertEqual(len(proof['external_comparisons']), 17)
        for row in proof['external_comparisons']:
            with self.subTest(row=row['id']):
                raw = (ROOT / row['path']).read_bytes()
                self.assertEqual(hashlib.sha256(raw).hexdigest(), row['sha256'])
                text = raw.decode('utf-8')
                self.assertEqual(''.join(text[i] for i in row['raw_character_offsets']), row['raw_quote'])
                self.assertEqual(paragraph['text'][row['start_codepoint']:row['end_codepoint']], row['source_quote'])

    def test_variants_and_named_victims(self):
        for suffix, words in [('', ('暗室', '何謂反乎', '通逵')),
                              ('-wyd', ('闇室', '可謂反乎', '通達'))]:
            base = 'corpus/jinshu/096-wangguangnu' + suffix
            paragraph, = read(base + '.json')['paragraphs']
            for word in words:
                self.assertIn(word, paragraph['text'])
            relation, = read(base + '-assertions.json')['assertions']
            self.assertEqual((relation['subject_person_id'], relation['predicate'], relation['object_person_id']),
                             ('pne_ii9_42q_A', 'father', 'pne_ii9_42q'))
            events = read(base + '-life-events.json')['events']
            self.assertEqual({(event['person_id'], event['source_anchor']['surface']) for event in events},
                             {('pne_ii9_42q', '被殺'), ('pne_ii9_42q_A', '自殺')})

    def test_leishu_witnesses_preserve_different_narratives(self):
        earlier, = read('corpus/taipingyulan/440-wangguangnu.json')['paragraphs']
        later, = read('corpus/taipingyulan/519-wangguangnu.json')['paragraphs']
        self.assertIn('蠻囚廣將詣芳', earlier['text'])
        self.assertIn('魯陽侯王廣，字廣之', earlier['text'])
        self.assertIn('廣被殺', later['text'])
        self.assertIn('梟汝首于通達', later['text'])


class XieFanjingWitnesses(unittest.TestCase):
    def test_two_histories_and_annal_anchors(self):
        for work, book in [('songshu', '041'), ('nanshi', '011')]:
            chapter = read('corpus/' + work + '/' + book + '-xiefanjing.json')
            paragraph, = chapter['paragraphs']
            proof = read('source-evidence/song041-xiefanjing/' + work + '-reading.json')
            self.assertEqual(len(proof['comparisons']), 12)
            for row in proof['comparisons']:
                with self.subTest(row=row['id']):
                    raw = (ROOT / row['path']).read_bytes()
                    self.assertEqual(hashlib.sha256(raw).hexdigest(), row['sha256'])
                    self.assertEqual(raw.decode()[row['raw_start']:row['raw_end']], row['reading'])
                    self.assertEqual(paragraph['text'][row['start_codepoint']:row['end_codepoint']], row['source_quote'])
            self.assertEqual([(x['year'], x.get('sexagenary_day')) for x in proof['dates']], [(478, '壬寅'), (479, None)])
            self.assertEqual('父揚，車騎功曹' in paragraph['text'], work == 'nanshi')

    def test_siku_and_palace_editions(self):
        proof = read('source-evidence/song041-xiefanjing/songshu-reading.json')['siku_parallel']
        raw = (ROOT / proof['raw_path']).read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), proof['raw_file_sha256'])
        lines = raw.decode().splitlines()
        self.assertEqual(lines[564], proof['page_marker'])
        for col in proof['columns']:
            self.assertEqual(lines[col['line'] - 1][col['start']:col['end']], col['reading'])
        print_proof = read('source-evidence/song041-xiefanjing-wyd/wuying-reading.json')
        self.assertEqual([(c['pdf_page'], c['leaf'], c['column_from_right']) for c in print_proof['columns']],
                         [(27, '二十五下', 8), (27, '二十五下', 9), (27, '二十五下', 10)])
        siku = ''.join(c['reading'] for c in proof['columns'])
        text = ''.join(c['reading'] for c in print_proof['columns'])
        self.assertIn('汝隂王妃', siku)
        self.assertEqual(siku.replace('汝隂王妃', '汝陰王妃'), text)

    def test_corrected_fold_numbers(self):
        receipt = read('source-evidence/song041-xiefanjing-wyd/folio-collation.json')
        image = receipt['image']
        self.assertEqual(hashlib.sha256((ROOT / image['path']).read_bytes()).hexdigest(), image['sha256'])
        self.assertEqual(len(receipt['corrected_readings']), 14)
        numbers = {(r['pdf_page'], r['half']): r['printed_leaf'] for r in receipt['folio_strips']}
        for fix in receipt['corrected_readings']:
            row = read(fix['path'])['printed_readings'][fix['index']]
            self.assertEqual(row['printed_leaf'], numbers[row['pdf_page'], row['half']])
            self.assertEqual((row['surface'], row['columns_from_right']), (fix['surface'], fix['columns_from_right']))
            self.assertNotEqual(row['printed_leaf'], fix['previous_leaf'])


if __name__ == '__main__':
    unittest.main()
