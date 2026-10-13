import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class FanCaiIdentityTests(unittest.TestCase):
    def test_qi_two_kings_are_not_collapsed_into_qin_addressee(self):
        chapter = json.loads((ROOT / 'corpus/shiji/079.json').read_text())
        paragraph = next(p for p in chapter['paragraphs'] if p['id'].endswith(':p017'))
        first = next(m for m in paragraph['mentions'] if m['id'].endswith('m017-0295'))
        second = next(m for m in paragraph['mentions'] if m['id'].endswith('m017-0299'))
        self.assertEqual(first['surface'], '王')
        self.assertEqual(second['surface'], '王')
        self.assertEqual(first['person_id'], '9w2_c77_53m_AAAA')
        self.assertEqual(second['person_id'], 'lmu_nbm_rzo_AAAAAAABAAAAAAAA')
        self.assertNotEqual(first['person_id'], second['person_id'])
        self.assertNotIn('ao3_0fy_d45', (first['person_id'], second['person_id']))
        self.assertIn('崔杼、淖齒管齊，射王股，擢王筋', paragraph['text'])
        self.assertTrue(any(m['surface'] == '王' and m['person_id'] is None
                            for m in paragraph['mentions']))
        self.assertEqual(next(m for m in paragraph['mentions'] if m['surface'] == '崔杼')['person_id'], 'xgd_r31_cmr')
        self.assertEqual(next(m for m in paragraph['mentions'] if m['surface'] == '淖齒')['person_id'], 'fvc_9z0_643')

    def test_shaqiu_zhufu_is_resolved_without_harmonizing_duration(self):
        chapter = json.loads((ROOT / 'corpus/shiji/079.json').read_text())
        paragraph = next(p for p in chapter['paragraphs'] if p['id'].endswith(':p017'))
        mention = next(m for m in paragraph['mentions'] if m['surface'] == '主父')
        self.assertEqual(mention['person_id'], 'txj_z8z_5me_A')
        self.assertIn('百日而餓死', paragraph['text'])
        zhao = json.loads((ROOT / 'corpus/shiji/043.json').read_text())
        account = next(p for p in zhao['paragraphs'] if p['id'].endswith(':p081'))
        self.assertIn('三月餘而餓死沙丘宮', account['text'])
        events = json.loads((ROOT / 'corpus/shiji/079-life-events.json').read_text())['events']
        event = next(e for e in events if e['person_id'] == mention['person_id'])
        self.assertEqual(event['normalized_date']['era_year'], 295)
        self.assertEqual(event['normalized_date']['precision'], 'year')

    def test_huaiwang_death_does_not_use_retrospective_qin_year(self):
        events = json.loads((ROOT / 'corpus/shiji/079-life-events.json').read_text())['events']
        event = next(e for e in events if e['person_id'] == 'c2w_s7g_en0')
        self.assertEqual(event['normalized_date']['era_year'], 296)
        self.assertEqual(event['normalized_date']['basis']['kind'], 'parallel_event')
        self.assertEqual(event['normalized_date']['basis']['source_event_quote'], '幽死於秦')
        self.assertTrue(any('頃襄王三年' in r['quote'] for r in event['normalized_date']['references']))

    def test_mengchang_short_forms_do_not_relink_other_wenzi(self):
        chapter = json.loads((ROOT / 'corpus/shiji/079.json').read_text())
        selected = [m for p in chapter['paragraphs'] for m in p['mentions']
                    if m['surface'] in ('文子', '田文')]
        self.assertEqual(len(selected), 3)
        self.assertEqual({m['person_id'] for m in selected}, {'7pl_s0g_rkh'})
        tian = json.loads((ROOT / 'corpus/shiji/046.json').read_text())
        older = [m for p in tian['paragraphs'] for m in p['mentions']
                 if m['surface'] in ('文子須無', '田文子', '文子')]
        self.assertTrue(older)
        self.assertTrue(all(m['person_id'] != '7pl_s0g_rkh' for m in older))

    def test_four_person_summary_resolves_local_baigong_only(self):
        chapter = json.loads((ROOT / 'corpus/shiji/079.json').read_text())
        paragraph = next(p for p in chapter['paragraphs'] if p['id'].endswith(':p032'))
        mention = next(m for m in paragraph['mentions'] if m['surface'] == '白公')
        self.assertEqual(mention['person_id'], '2bk_fz6_icl')
        self.assertIn('則商君、白公、吳起、大夫種是也', paragraph['text'])
        people = json.loads((ROOT / 'registry/persons.json').read_text())['persons']
        chu = [p for p in people if p['label'].startswith('白公勝')]
        self.assertTrue(chu)
        self.assertTrue(all(p['id'] != mention['person_id'] for p in chu))

    def test_commentator_reference_preserves_unverified_image_status(self):
        decisions = json.loads((ROOT / 'corpus/shiji/079-equivalences.json').read_text())['decisions']
        decision = next(d for d in decisions if d['id'] == 'eq-shiji079-baigong')
        self.assertEqual(decision['person_ids'], ['2bk_fz6_icl'])
        self.assertTrue(decision['identity_materialized'])
        self.assertEqual(decision['references'][0]['quote'], '白起。')
        self.assertFalse(decision['references'][0]['image_verified'])
        self.assertFalse(decision['human_reviewed'])
