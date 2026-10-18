import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads((ROOT / path).read_text())


class ZichanCrossReferencesTests(unittest.TestCase):
    def test_same_visit_and_explicit_alias_connect_jizha(self):
        ch = load('corpus/shiji/042.json')
        para = next(p for p in ch['paragraphs'] if p['id'].endswith(':p039'))
        mentions = {m['surface']: m['person_id'] for m in para['mentions']}
        self.assertEqual(mentions['延陵季子'], '5dm_e40_rqh_AAAAAAAAAAAAAAAAAAD')
        self.assertEqual(mentions['季子'], mentions['延陵季子'])
        self.assertEqual(mentions['子産'], 'qjs_3hl_6ck_A')

    def test_ranji_courtesy_name_is_not_zheng_zichan(self):
        ch = load('corpus/shiji/067.json')
        para = next(p for p in ch['paragraphs'] if p['text'] == '冉季字子產。')
        mention = next(m for m in para['mentions'] if m['surface'] == '子產')
        self.assertEqual(mention['person_id'], 'v7p_b12_9nv')
        self.assertEqual(para['text'][mention['start']:mention['end']], '子產')
        first = next(p for p in ch['paragraphs'] if p['id'].endswith(':p002'))
        self.assertEqual(next(m for m in first['mentions'] if m['surface'] == '子產')['person_id'], 'qjs_3hl_6ck_A')

    def test_kinship_prefix_is_outside_two_person_spans(self):
        for chapter, mid, pid, expected in [
            ('009', 'c-shiji-009-lvhou:m002-0050', 'acg_se3_w5x_B', '產'),
            ('032', 'c-shiji-032-qi:m065-0010', 'xgd_r31_cmr_A', '成'),
        ]:
            with self.subTest(chapter=chapter):
                ch = load(f'corpus/shiji/{chapter}.json')
                para, mention = next((p,m) for p in ch['paragraphs'] for m in p['mentions'] if m['id'] == mid)
                self.assertEqual(mention['person_id'], pid)
                self.assertEqual(mention['surface'], expected)
                self.assertEqual(para['text'][mention['start']-1], '子')
                self.assertEqual(para['text'][mention['start']:mention['end']], expected)
                person = next(p for p in load('registry/persons.json')['persons'] if p['id'] == pid)
                self.assertNotIn('子'+expected, [a['surface'] for a in person['aliases']])
                self.assertEqual(next(e['quote'] for e in person['evidence'] if e['mention_id'] == mid), expected)

    def test_received_name_does_not_assert_historical_participation(self):
        decisions = load('corpus/shiji/066-identities.json')['decisions']
        decision = next(d for d in decisions if d['id'] == 'd-shiji-zichan-crossrefs-03')
        self.assertEqual(decision['person_id'], 'qjs_3hl_6ck_A')
        self.assertIn('不採信其真實參與誅建', decision['rationale'])
        self.assertIn('不延長生卒', decision['rationale'])
        self.assertFalse(decision['human_reviewed'])

    def test_retired_source_candidates_have_no_active_registry_entry(self):
        people = {p['id'] for p in load('registry/persons.json')['persons']}
        for pid in ['34u_t1e_mvb','53z_6rk_goh','wie_ryy_5wa','bvk_gpk_f1b','6tl_wrj_8ll','xn7_c7s_lzh','9g0_ueo_x4u']:
            self.assertNotIn(pid, people)


if __name__ == '__main__':
    unittest.main()
