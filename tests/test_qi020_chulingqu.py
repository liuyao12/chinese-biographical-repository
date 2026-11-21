from copy import deepcopy
import hashlib
import json
from pathlib import Path
import unittest

from scripts.liang021_print_columns import errors as print_errors
from scripts.qi020_chulingqu import named_prince_valid, shaoxing_witness_errors


ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads((ROOT / path).read_bytes())


class ChulingquWitnessTests(unittest.TestCase):
    def test_four_witnesses_keep_the_death_subject_and_demotion(self):
        for base in ['nanqishu/020-chulingqu', 'nanqishu/020-chulingqu-wyd',
                     'nanshi/011-chulingqu', 'nanshi/011-chulingqu-izumo']:
            with self.subTest(base=base):
                stem = 'corpus/' + base
                chapter = read(stem + '.json')
                p, = chapter['paragraphs']
                demotion, = [a for a in chapter['annotation']['narrative_readings']
                             if a['event_type'] == 'demotion']
                self.assertEqual(demotion['person_ids'], ['6fs_tis_zoa_AA', 'w4m_9tw_147_AA'])
                self.assertIn(demotion['source_anchor']['surface'], p['text'])
                mother, = [a for a in read(stem + '-assertions.json')['assertions'] if a['predicate'] == 'mother']
                self.assertEqual((mother['subject_person_id'], mother['object_person_id']),
                                 ('w4m_9tw_147_AA', 'nxr_ok6_sn7'))
                if base.startswith('nanshi'):
                    self.assertIn('而卒', p['text'])
                    death, = read(stem + '-life-events.json')['events']
                    self.assertEqual((death['event_type'], death['person_id']), ('death', 'nxr_ok6_sn7'))
                else:
                    self.assertNotIn('而卒', p['text'])
                    self.assertFalse((ROOT / (stem + '-life-events.json')).exists())
                if base.endswith(('-wyd', '-izumo')):
                    self.assertEqual(print_errors(chapter, ROOT), [])
                    wrong = deepcopy(chapter)
                    wrong['paragraphs'][0]['source_position']['column_projection'][0]['column_from_right'] += 1
                    self.assertTrue(print_errors(wrong, ROOT))

    def test_calendar_disagreements_keep_their_actual_lines(self):
        ledger = read('source-evidence/qi020-chulingqu/chulingqu-nanqishu.json')
        note, = ledger['layers']
        self.assertEqual(note['kind'], 'editorial_note')
        raw = (ROOT / ledger['raw_path']).read_text()
        self.assertEqual(raw[note['raw_start']:note['raw_end']], note['text'])
        self.assertIn('按南史', note['text'])
        locations = set()
        for row in ledger['comparisons']:
            if 'revision_id' in row:
                data = (ROOT / row['path']).read_bytes()
                self.assertEqual(hashlib.sha256(data).hexdigest(), row['raw_sha256'])
                raw = data.decode()
                self.assertEqual(raw[row['raw_start']:row['raw_end']], row['reading'])
                self.assertEqual(1 + raw.count('\n', 0, row['raw_start']), row['raw_line'])
                locations.add((row['revision_id'], row['raw_line'], row['reading']))
        self.assertTrue({
            (2311630, 37, '乙卯，納皇太子妃褚氏，大赦'),
            (1554152, 107, '十一月，丁卯，詔罷世宗東田'),
            (1554152, 109, '己卯，納太子妃褚氏，大赦。妃，澄之女也'),
            (740760, 33, '十月納皇太子妃禇氏'), (740760, 38, '十一月立皇子誦為皇太子'),
            (2027696, 138, '己巳，立皇子誦為皇太子'),
            (803184, 148, '褚后及太子誦並為庶人'),
        } <= locations)

    def test_shaoxing_edition_identifies_both_physical_pages(self):
        c = read('corpus/jiankang-shilu/015-chulingqu-shaoxing.json')
        self.assertEqual(shaoxing_witness_errors(c, ROOT), [])
        self.assertEqual(c['paragraphs'][0]['text'], '八月納皇太子妃褚氏大赦')
        self.assertEqual(c['paragraphs'][2]['text'], '永元元年十一月立皇子誦為太子')
        for change in ('month', 'column', 'missing'):
            wrong = deepcopy(c)
            if change == 'month':
                wrong['paragraphs'][0]['text'] = '十月納皇太子妃禇氏大赦'
            elif change == 'column':
                wrong['paragraphs'][2]['source_position']['column_projection'][0]['pdf_page'] = 12
            else:
                wrong['paragraphs'].pop()
            self.assertTrue(shaoxing_witness_errors(wrong, ROOT))

    def test_named_prince_uses_his_own_emperors_annal(self):
        stem = 'corpus/nanshi/005-song-emperor-and-mother'
        c = read(stem + '.json')
        a, = read(stem + '-assertions.json')['assertions']
        self.assertTrue(named_prince_valid(a, c, ROOT))
        self.assertFalse(named_prince_valid(dict(a, predicate='mother'), c, ROOT))
        self.assertFalse(named_prince_valid(dict(a, evidence=list(reversed(a['evidence']))), c, ROOT))
        other, = [m for m in c['paragraphs'][1]['mentions'] if m['surface'] == '魏孝文皇帝']
        wrong = deepcopy(a)
        wrong['object_person_id'] = other['person_id']
        wrong['evidence'][1]['object_person_mention_id'] = other['id']
        self.assertFalse(named_prince_valid(wrong, c, ROOT))
        wrong_chapter = deepcopy(c)
        wrong_chapter['paragraphs'][1]['source_position']['first_line'] -= 1
        self.assertFalse(named_prince_valid(a, wrong_chapter, ROOT))


if __name__ == '__main__':
    unittest.main()
