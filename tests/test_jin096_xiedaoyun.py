import copy
import json
from pathlib import Path
import unittest

from scripts import jin096_xiedaoyun as daoyun
from scripts import jin096_zhong_and_guan as zhong


ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


class Jin96Witnesses(unittest.TestCase):
    def test_feng_has_distinct_glosses_and_sources(self):
        for suffix, name in [('', '謝韶'), ('-wyd', '謝歆')]:
            c = read('corpus/jinshu/096-xiedaoyun' + suffix + '.json')
            self.assertEqual(daoyun.errors(c, ROOT), [])
            p = c['paragraphs'][1]
            gloss = next(m for m in p['mentions'] if m['surface'] == name)
            next(m for m in p['mentions'] if m['surface'] == '封')['person_id'] = 'wrong'
            self.assertTrue(daoyun.errors(c, ROOT))
            self.assertIn('封謂' + gloss['surface'], p['text'].replace('，', ''))

    def test_opening_uncle_and_niece(self):
        for suffix in ('', '-wyd'):
            base = 'corpus/jinshu/096-xiedaoyun' + suffix
            c = read(base + '.json')
            paragraphs = {p['id']: (c['id'], p) for p in c['paragraphs']}
            rows = read(base + '-assertions.json')['assertions']
            a = next(r for r in rows if r['subject_person_id'] == daoyun.DAO
                     and r['predicate'] == 'paternal_uncle' and r['object_person_id'] == daoyun.AN)
            self.assertTrue(daoyun.uncle_valid(a, paragraphs))
            altered = copy.deepcopy(a)
            evidence = altered['evidence'][0]
            evidence['subject_person_mention_id'] = evidence['object_person_mention_id']
            self.assertFalse(daoyun.uncle_valid(altered, paragraphs))

    def test_sources_for_zhang_zuxi(self):
        d = read('corpus/jinshu/096-xiedaoyun-equivalences.json')['decisions'][0]
        self.assertEqual(set(d['person_ids']), {'ce4_5fc_839', '52e_1dd_651'})
        c = read('corpus/shishuoxinyu/002-zhangzuxi.json')
        p = c['paragraphs'][0]
        self.assertEqual(p['attribution']['quoted_work'], '續晉陽秋')
        self.assertIn('張玄之字祖希', p['text'])
        self.assertNotEqual(next(m for m in p['mentions'] if m['surface'] == '澄')['person_id'],
                            'zew_5dv_v7n')
        self.assertIn(c['id'], d['chapter_ids'])

    def test_zhong_genealogical_readings_keep_their_attribution(self):
        c = read('corpus/jinshu/096.json')
        self.assertEqual(zhong.errors(c, ROOT), [])
        row = next(r for r in c['annotation']['source_reading_cases']
                   if '名琰之' in r['reading'])
        row['reading'] = row['reading'].replace('之孫', '曾孫')
        self.assertTrue(zhong.errors(c, ROOT))

    def test_xunguan_and_zhoufu_have_separate_counts(self):
        c = read('corpus/jinshu/096-xunguan-wyd.json')
        self.assertEqual(zhong.errors(c, ROOT), [])
        p = c['paragraphs'][0]
        self.assertIn('勇士數十人', p['text'])
        p['text'] = p['text'].replace('勇士數十人', '勇士數千人')
        self.assertTrue(zhong.errors(c, ROOT))
