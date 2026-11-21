from copy import deepcopy
import hashlib
import json
from pathlib import Path
import unittest

from scripts.liang021_print_columns import errors as column_errors
from scripts.unspecified_ancestry import unspecified_ancestry_valid


ROOT = Path(__file__).resolve().parents[1]


def read(name):
    return json.loads((ROOT / name).read_bytes())


class ChendaozhiWitnesses(unittest.TestCase):
    def test_family_and_unnumbered_descent_in_each_account(self):
        for stem in ('nanqishu/020-chendaozhi', 'nanqishu/020-chendaozhi-wyd',
                     'nanshi/011-chendaozhi', 'nanshi/011-chendaozhi-izumo'):
            with self.subTest(stem=stem):
                c = read('corpus/' + stem + '.json')
                edges = read('corpus/' + stem + '-assertions.json')['assertions']
                paragraphs = {p['id']: (c['id'], p) for p in c['paragraphs']}
                ancestor, = [x for x in edges if x['predicate'] == 'ancestor']
                self.assertTrue(unspecified_ancestry_valid(ancestor, paragraphs))
                self.assertIsNone(ancestor['qualifiers']['generation_distance'])
                birth_mother, = [x for x in edges if x['predicate'] == 'mother' and x['object_person_id'] == ancestor['subject_person_id']]
                self.assertEqual(birth_mother['subject_person_id'], '47p_kjh_ez7')
                self.assertEqual(ancestor['object_person_id'], 'y5v_7tv_nxw')
                self.assertEqual(len([x for x in edges if x['predicate'] == 'father'
                                      and '庶生' in x['qualifiers']['source_term']]), 2)
                bad = deepcopy(ancestor)
                bad['qualifiers']['generation_distance'] = 4
                self.assertFalse(unspecified_ancestry_valid(bad, paragraphs))
                if 'nanqishu' in stem:
                    bad = deepcopy(ancestor)
                    bad['evidence'][0]['subject_person_mention_id'] = bad['evidence'][0]['object_person_mention_id']
                    self.assertFalse(unspecified_ancestry_valid(bad, paragraphs))
                ages = c['annotation'].get('age_assertions', [])
                self.assertEqual([r['value'] for r in ages], [73] if 'nanqishu' in stem else [])

    def test_two_prints_have_independent_page_and_column_evidence(self):
        for stem, expected_count, pages, variants in [
            ('nanqishu/020-chendaozhi-wyd', 13, [3], ['諱道正','宣帝從仕','昇明三年']),
            ('nanshi/011-chendaozhi-izumo', 18, [17,18], ['諱道止','宣帝從任','昇明二年','祠以太牢','鴨𦞦']),
        ]:
            with self.subTest(stem=stem):
                c = read('corpus/' + stem + '.json')
                ledger = read(c['annotation']['print_projection_ref'])
                inventory = read('data/corpus/six-dynasties-biographies.json')
                survey, = [v for v in inventory['volume_surveys'] if v['book_id'] == c['book_id']]
                witness, = [v for v in survey['text_witness_units'] if v['chapter_id'] == c['id']]
                biography, = [v for v in inventory['biographies'] if v['book_id'] == c['book_id']
                              and v['title'] == witness['title']]
                self.assertEqual(biography['chapter_id'], c['id'].rsplit('-', 1)[0])
                self.assertEqual(column_errors(c, ROOT), [])
                self.assertEqual(len(ledger['columns']), expected_count)
                self.assertEqual([v['pdf_page'] for v in ledger['images']], pages)
                for v in ledger['images']:
                    self.assertEqual(v['source_url'], ledger['pdf_url'] + '#page=' + str(v['pdf_page']))
                    self.assertRegex(v['capture_sha256'], r'^[0-9a-f]{64}$')
                data = (ROOT / ledger['column_file']).read_bytes()
                self.assertEqual(hashlib.sha256(data).hexdigest(), ledger['column_file_sha256'])
                text = ''.join(c['reading'] for c in ledger['columns'])
                for term in variants:self.assertIn(term, text)

    def test_titles_in_annals_and_quoted_name(self):
        q = read('corpus/nanqishu/002-chendaozhi-zhuizun.json')
        self.assertEqual(q['paragraphs'][0]['text'], '五月丙午')
        self.assertIn('丙寅，追尊皇考曰宣皇帝，皇妣為孝皇后，妃為昭皇后', q['paragraphs'][1]['text'])
        n = read('corpus/nanshi/004-chendaozhi-zhuizun.json')
        self.assertIn('夏四月甲午', n['paragraphs'][0]['text'])
        self.assertIn('陵曰永安。妃曰昭皇后，陵曰泰安', n['paragraphs'][1]['text'])
        y = read('corpus/taipingyulan/143-chendaozhi.json')
        self.assertEqual(y['paragraphs'][0]['text'], '齊蕭道成母陳后')
        self.assertIn('諱道正', y['paragraphs'][1]['text'])
