import json
import unittest
from copy import deepcopy
from hashlib import sha256
from pathlib import Path

from scripts.chen017_appointments import MAI, TONG, valid

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads((ROOT / path).read_text())


class ChenWangBrothers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapters = {cid: read('corpus/chenshu/' + cid.removeprefix('c-chenshu-') + '.json')
                        for cid in (TONG, MAI)}

    def test_sentences_cover_fixed_text_and_native_character_positions(self):
        for chapter in self.chapters.values():
            raw = (ROOT / chapter['source']['raw_path']).read_text()
            self.assertEqual(sha256(raw.encode()).hexdigest(), chapter['source']['raw_file_sha256'])
            for p in chapter['paragraphs']:
                cases = [row for row in chapter['annotation']['source_reading_cases']
                         if row['kind'] == 'received_sentence' and row['paragraph_id'] == p['id']]
                offset = 0
                for case in cases:
                    self.assertEqual(case['start_codepoint'], offset)
                    self.assertEqual(p['text'][offset:case['end_codepoint']], case['source_quote'])
                    self.assertTrue(case['reading'])
                    offset = case['end_codepoint']
                self.assertEqual(offset, len(p['text']))
                positions = p['source_position']['raw_character_offsets']
                self.assertEqual(''.join(raw[i] for i in positions), p['text'])

    def test_offered_dignity_and_provincial_appointments_bind_exact_passages(self):
        for cid, chapter in self.chapters.items():
            offers = chapter['annotation']['title_proposals']
            expected = {'特進'} if cid == TONG else {'廣州刺史', '衡州刺史', '侍中', '都官尚書'}
            self.assertEqual({o['title'] for o in offers}, expected)
            for offer in offers:
                self.assertTrue(valid(offer, chapter))
                displaced = deepcopy(offer)
                displaced['non_assumption_anchor']['start'] += 1
                self.assertFalse(valid(displaced, chapter))
                wrong = deepcopy(offer)
                wrong['person_id'] = self.chapters[MAI if cid == TONG else TONG]['annotation']['age_assertions'][0]['person_id']
                self.assertFalse(valid(wrong, chapter))
        titles = read('corpus/chenshu/017-wangtong-complete-titles.json')['holdings']
        self.assertNotIn('特進', [row['title'] for row in titles])

    def test_print_and_annals_retain_separate_readings(self):
        basedir = 'source-evidence/chenshu017-wangyuan/'
        tong = read(basedir + 'wangtong-wuyingdian.json')
        mai = read(basedir + 'wangmai-wuyingdian.json')
        self.assertEqual(tong['pdf_sha256'], mai['pdf_sha256'])
        lines = {(r['pdf_page'], r['half'], r['column_from_right']): r['text'] for r in tong['columns']}
        self.assertIn('司空左長史', lines[55, '右', 9])
        self.assertIn('南史作司徒', lines[60, '左', 2])
        self.assertIn('父琳，司徒左長史', self.chapters[TONG]['paragraphs'][0]['text'])
        self.assertEqual(len(mai['columns']), 30)
        self.assertTrue(all(len(row['text']) == 21 for row in mai['columns']))
        self.assertIn('勅勱令從輦側', ''.join(r['text'] for r in mai['columns']))
        self.assertIn('队勱令從輦側', self.chapters[MAI]['paragraphs'][1]['text'])
        for slug in ('wangtong', 'wangmai'):
            ledger = read(basedir + slug + '-reading.json')
            for witness in ledger['external_witnesses']:
                raw = (ROOT / witness['raw_path']).read_bytes()
                self.assertEqual(sha256(raw).hexdigest(), witness['raw_sha256'])
                lines = raw.decode().splitlines()
                for part in witness['clauses']:
                    self.assertEqual(lines[part['line'] - 1][part['start']:part['end']], part['quote'])
