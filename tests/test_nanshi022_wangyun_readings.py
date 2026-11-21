"""Keep the two sets of glosses, printed variants, and three Wang generations distinct."""
import json
import unittest
from copy import deepcopy
from pathlib import Path

from scripts.fixed_wikisource_units import source_errors
from scripts.liang021_print_columns import errors as print_errors

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads((ROOT / path).read_text())


class WangYunReadings(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.digital = load('corpus/nanshi/022-wangyun-family.json')
        cls.printed = load('corpus/nanshi/022-wangyun-family-wyd.json')

    def test_inline_notes_belong_to_their_own_characters(self):
        self.assertEqual(source_errors(self.digital, ROOT), [])
        altered = deepcopy(self.digital)
        glosses = altered['annotation']['source_phonetic_glosses']
        self.assertEqual([n['gloss'] for n in glosses], ['五的反', '五兮反'])
        glosses[1]['headword_raw_offset'] = glosses[0]['headword_raw_offset']
        self.assertTrue(source_errors(altered, ROOT))

    def test_print_columns_preserve_words_and_small_type(self):
        self.assertEqual(print_errors(self.printed, ROOT), [])
        altered = deepcopy(self.printed)
        changed = altered['paragraphs'][5]
        self.assertIn('家人十二口', changed['text'])
        changed['text'] = changed['text'].replace('家人十二口', '家人十三口')
        self.assertTrue(print_errors(altered, ROOT))
        altered = deepcopy(self.printed)
        notes = altered['annotation']['printed_phonetic_glosses']
        notes[1]['headword_start'] = notes[0]['headword_start']
        self.assertTrue(print_errors(altered, ROOT))

    def test_era_totals_and_household_counts_stay_with_each_edition(self):
        texts = [''.join(p['text'] for p in ch['paragraphs']) for ch in (self.digital, self.printed)]
        for text, expressions in zip(texts, [('中大通二年', '家人十三口', '四十六載', '賢弟手'),
                                             ('大通二年', '家人十二口', '四十載', '賢弟子')]):
            for expression in expressions:
                self.assertIn(expression, text)
        self.assertNotIn('中大通二年', texts[1])
        for ch in (self.digital, self.printed):
            self.assertIsNone(next(a for a in ch['annotation']['age_assertions'] if a['value'] == 69)['birth_year'])

    def test_son_and_grandson_keep_separate_source_clauses(self):
        for suffix in ('', '-wyd'):
            rows = load(f'corpus/nanshi/022-wangyun-family{suffix}-assertions.json')['assertions']
            father, = [r for r in rows if r['predicate'] == 'father']
            self.assertEqual((father['subject_person_id'], father['object_person_id']), ('mxz_qw8_acd_AA', 'mxz_qw8_acd_A'))
            self.assertEqual(len(father['context']['paragraph_ids']), 2)
        sui = load('corpus/suishu/076-wangzhou-wangyun-assertions.json')['assertions']
        self.assertEqual({(r['predicate'], r['subject_person_id'], r['object_person_id']) for r in sui},
                         {('father', 'mxz_qw8_acd_AAA', 'mxz_qw8_acd_AA'),
                          ('grandfather', 'mxz_qw8_acd_AAA', 'mxz_qw8_acd_A')})
