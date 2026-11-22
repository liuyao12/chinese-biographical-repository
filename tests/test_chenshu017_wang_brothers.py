import json
import unittest
from copy import deepcopy
from hashlib import sha256
from pathlib import Path

from scripts.chen017_appointments import CHONG, MAI, TONG, valid

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads((ROOT / path).read_text())


class ChenWangBrothers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapters = {cid: read('corpus/chenshu/' + cid.removeprefix('c-chenshu-') + '.json')
                        for cid in (TONG, MAI, CHONG)}

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
            expected = {TONG: {'特進'}, MAI: {'廣州刺史', '衡州刺史', '侍中', '都官尚書'},
                        CHONG: {'左光祿大夫'}}[cid]
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
        for slug in ('wangtong', 'wangmai', 'wangchong'):
            ledger = read(basedir + slug + '-reading.json')
            for witness in ledger['external_witnesses']:
                raw = (ROOT / witness['raw_path']).read_bytes()
                self.assertEqual(sha256(raw).hexdigest(), witness['raw_sha256'])
                lines = raw.decode().splitlines()
                for part in witness['clauses']:
                    self.assertEqual(lines[part['line'] - 1][part['start']:part['end']], part['quote'])

    def test_chong_two_grants_and_the_two_princely_deaths(self):
        chapter = self.chapters[CHONG]
        para = chapter['paragraphs'][4]
        offer, = chapter['annotation']['title_proposals']
        holdings = read('corpus/chenshu/017-wangchong-complete-titles.json')['holdings']
        held, = [h for h in holdings if h['title'] == offer['title']]
        anchor = held['attestations'][0]
        self.assertEqual(anchor['start'], para['text'].index('左光祿大夫', para['text'].index('文帝嗣位')))
        wrong = deepcopy(offer)
        wrong['role_anchor'].update(start=anchor['start'], end=anchor['end'])
        self.assertFalse(valid(wrong, chapter))
        wrong = deepcopy(offer)
        wrong['evidence'][0]['context']['paragraph_id'] = para['id']
        self.assertFalse(valid(wrong, chapter))
        opening = chapter['paragraphs'][0]
        deaths = {m['start']: m['person_id'] for m in opening['mentions'] if m['surface'] == '王'}
        self.assertEqual(deaths[opening['text'].index('王薨於湘州')], 'z8c_kq5_fri_A')
        self.assertEqual(deaths[opening['text'].index('王薨，行州府事')], 'fo7_f8v_rmf_G')
        pr = read('source-evidence/chenshu017-wangyuan/wangchong-wuyingdian.json')
        self.assertEqual(len(pr['columns']), 33)
        self.assertIn('佐藩莅人', ''.join(v['text'] for v in pr['columns']))
        self.assertIn('佐藩两人', opening['text'])
