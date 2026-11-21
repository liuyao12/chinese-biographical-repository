import hashlib
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SUBJECTS = {'wangxianyuan': '7r6_k52_qji_ABAACAABA', 'wangzhenfeng': 'q7m_r8k_2vn_B'}


def load(relative):
    return json.loads((ROOT / relative).read_bytes())


class NanshiWangEmpresses(unittest.TestCase):
    def test_mothers_and_empresses_dowager(self):
        six = {'iwn_c2g_zvh', 'y7i_swu_xgh', 'hx8_st4_jdd_C', 'hx8_st4_jdd_D',
               'hx8_st4_jdd_E', 'hx8_st4_jdd_F'}
        two = {'cti_o52_4nz_B', 'cti_o52_4nz_C'}
        for witness in ('', '-izumo'):
            for slug, children in [('wangxianyuan', six), ('wangzhenfeng', two)]:
                path = f'corpus/nanshi/011-{slug}{witness}'
                kin = load(path + '-assertions.json')['assertions']
                self.assertEqual({(r['subject_person_id'], r['object_person_id'])
                                  for r in kin if r['predicate'] == 'mother'},
                                 {(child, SUBJECTS[slug]) for child in children})
            chapter = load('corpus/nanshi/011-wangxianyuan' + witness + '.json')
            para = chapter['paragraphs'][1]
            marks = para['mentions'] + [r for r in chapter['annotation']['person_reference_occurrences']
                                        if r['paragraph_id'] == para['id']]
            dowagers = sorted((r['start'], r['person_id']) for r in marks if r['surface'] == '皇太后')
            self.assertEqual([pid for _, pid in dowagers], ['bfe_7hz_jcb', SUBJECTS['wangxianyuan']])

    def test_distinguish_deaths_and_time_expressions(self):
        for witness in ('', '-izumo'):
            path = 'corpus/nanshi/011-wangzhenfeng' + witness
            events = load(path + '-life-events.json')['events']
            self.assertEqual({(e['person_id'], e['source_term'], e['date_expression']) for e in events},
                             {('6y2_apj_l05', '殂', None), (SUBJECTS['wangzhenfeng'], '薨', '建元元年')})
            for record in events:
                anchor = record['source_anchor']
                paragraph = next(p for p in load(path + '.json')['paragraphs']
                                 if p['id'] == anchor['paragraph_id'])
                self.assertEqual(paragraph['text'][anchor['start']:anchor['end']], record['source_term'])
        for slug, age in [('wangxianyuan', '三十八'), ('wangzhenfeng', '四十四')]:
            proof = load(f'source-evidence/nan011-wang-queens/{slug}-nanshi.json')
            self.assertTrue(any('時年' + age in case['reading'] and case['revision_id'] == 2634831
                                for case in proof['comparisons']))
            self.assertNotIn('時年' + age, ''.join(p['text'] for p in
                                                  load(f'corpus/nanshi/011-{slug}.json')['paragraphs']))

    def test_verified_columns_and_external_readings(self):
        for slug, expected in [('wangxianyuan', (8, 129)), ('wangzhenfeng', (20, 345))]:
            ledger = load(f'source-evidence/nan011-{slug}-izumo/izumo-reading.json')
            printed = ''.join(col['reading'] for col in ledger['columns'])
            self.assertEqual((len(ledger['columns']), len(printed)), expected)
            if slug == 'wangzhenfeng':
                self.assertIn('從舅陳郡謝綽', printed)
                self.assertIn('順帝殂于丹楊', printed)
            else:
                self.assertIn('康樂公主脩明', printed)
            proof = load(f'source-evidence/nan011-wang-queens/{slug}-nanshi.json')
            for case in proof['comparisons']:
                source = (ROOT / case['path']).read_bytes()
                self.assertEqual(hashlib.sha256(source).hexdigest(), case['raw_sha256'])
                self.assertEqual(source.decode()[case['raw_start']:case['raw_end']], case['reading'])
