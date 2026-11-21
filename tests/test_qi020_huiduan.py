from copy import deepcopy
import json
from pathlib import Path
import unittest

from scripts.liang021_print_columns import errors as print_errors
from scripts.qi020_huiduan import grant_valid, marriage_valid, wenxuan_errors


ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads((ROOT / path).read_bytes())


class HuiduanWitnessTests(unittest.TestCase):
    def test_four_accounts_bind_names_marriage_and_recipients(self):
        for base in ('nanqishu/020-xietiao-jing', 'nanqishu/020-xietiao-jing-wyd',
                     'nanshi/011-liuhuiduan', 'nanshi/011-liuhuiduan-izumo'):
            with self.subTest(base=base):
                stem = 'corpus/' + base
                chapter = read(stem + '.json')
                paragraph, = chapter['paragraphs']
                self.assertEqual(print_errors(chapter, ROOT), [])
                if base.endswith(('-wyd', '-izumo')):
                    bad = deepcopy(chapter)
                    bad['paragraphs'][0]['source_position']['column_projection'][0]['column_from_right'] += 1
                    self.assertTrue(print_errors(bad, ROOT))
                index = {paragraph['id']: (chapter['id'], paragraph)}
                marks = {m['id']: (chapter['id'], paragraph['id'], m) for m in paragraph['mentions']}
                kin = read(stem + '-assertions.json')['assertions']
                spouse, = [a for a in kin if a['predicate'] == 'spouse']
                evidence, = spouse['evidence']
                self.assertTrue(marriage_valid(spouse, evidence, chapter))
                self.assertFalse(marriage_valid(dict(spouse, object_person_id='47p_kjh_ez7'), evidence, chapter))
                self.assertEqual({(a['predicate'], a['object_person_id']) for a in kin}, {
                    ('father', 'gjl_f5h_2a6'), ('grandfather', 'vus_7f1_rrz'),
                    ('mother', 'q20_pas_ain'), ('spouse', 'w4m_9tw_147')})
                gifts = [h for h in read(stem + '-titles.json')['holdings']
                         if h.get('posthumous_basis', {}).get('kind') == 'qi020_huiduan_named_gifts']
                self.assertEqual({v['title'] for v in gifts}, {'宣城王妃', '金紫光祿大夫', '平陽鄉君'})
                for holding in gifts:
                    self.assertTrue(grant_valid(holding, index, marks))
                    self.assertFalse(grant_valid(dict(holding, person_id='w4m_9tw_147'), index, marks))

    def test_wenxuan_layers_and_different_kinship_readings(self):
        for layer in ('shan', 'liang', 'received', 'aice'):
            with self.subTest(layer=layer):
                c = read('corpus/wenxuan/058-huiduan-' + layer + '.json')
                self.assertEqual(wenxuan_errors(c, ROOT), [])
                bad = deepcopy(c)
                pos = bad['paragraphs'][0]['source_position']
                if layer in ('shan', 'liang'):
                    pos['column_projection'][0]['small_column'] = '左'
                else:
                    pos['raw_character_offsets'][0] += 1
                self.assertTrue(wenxuan_errors(bad, ROOT))
        decision, = read('corpus/wenxuan/family-tree-decisions.json')['decisions']
        self.assertEqual(decision['preferred_parent_person_id'], 'gjl_f5h_2a6')
        self.assertEqual(set(decision['excluded_assertion_ids']),
                         {'a-wenxuan-058-huiduan-shan-kin', 'a-wenxuan-058-huiduan-received-kin'})
        for layer in ('shan', 'liang', 'received'):
            a, = read(f'corpus/wenxuan/058-huiduan-{layer}-assertions.json')['assertions']
            pred, term = ('grandfather', '弘道孫') if layer == 'liang' else ('father', '道弘女')
            self.assertEqual((a['predicate'], a['qualifiers']['source_term']), (pred, term))

    def test_earlier_identifiers_survive_the_full_reading(self):
        c = read('corpus/nanqishu/020-xietiao-jing.json')
        p, = c['paragraphs']
        old = {m['surface']: m['id'] for m in p['mentions']}
        self.assertEqual(old['惠端'], p['id'] + ':m0006')
        self.assertEqual(old['景猷'], p['id'] + ':m0084')
        father, = [a for a in read('corpus/nanqishu/020-xietiao-jing-assertions.json')['assertions']
                   if a['predicate'] == 'father']
        self.assertEqual(father['id'], 'a-nanqishu-020-xietiao-jing-hui')


if __name__ == '__main__':
    unittest.main()
