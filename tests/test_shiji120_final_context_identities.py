# coding: utf-8
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = json.loads((ROOT / 'tests/fixtures/shiji120-final-context-identities.json').read_text())

def read(path):
    return json.loads((ROOT / path).read_text())

class JizhengFinalContextTests(unittest.TestCase):
    def test_eight_original_mentions_keep_their_exact_spans(self):
        chapter = read('corpus/shiji/120.json')
        self.assertEqual(len(FIXTURE['mentions']), 8)
        for ref in FIXTURE['mentions']:
            p = next(p for p in chapter['paragraphs'] if p['id'] == ref['paragraph_id'])
            self.assertEqual(p['text'], FIXTURE['paragraphs'][p['id']])
            self.assertEqual(next(m for m in p['mentions'] if m['id'] == ref['marker']['id']), ref['marker'])

    def test_five_retired_ids_have_no_active_registry_or_person_json(self):
        people = {p['id']: p for p in read('registry/persons.json')['persons']}
        for old, target in FIXTURE['mapping'].items():
            self.assertNotIn(old, people)
            self.assertIn(target, people)
            self.assertFalse((ROOT / 'exports/persons' / (old + '.json')).exists())
            self.assertFalse((ROOT / 'data/corpus/profiles' / (old + '.json')).exists())

    def test_han_founder_wendi_and_xiangji_have_separate_contexts(self):
        decisions = {d['id']: d for d in read('corpus/shiji/120-identities.json')['decisions']}
        expected = [('01', 'ob7_g6i_7pp', 'c-shiji-007-xiangyu'),
                    ('02', 'yqp_nlb_p1p_A', 'c-shiji-008-gaozu'),
                    ('03', 'yqp_nlb_p1p_AC', 'c-shiji-010-wendi')]
        for suffix, person, chapter in expected:
            decision = decisions['d-shiji120-final-context-' + suffix]
            self.assertEqual(decision['person_id'], person)
            self.assertIn(chapter, {e['chapter_id'] for e in decision['evidence']})

    def test_weiqi_same_case_cites_zheng_dangshi_testimony(self):
        decision = next(d for d in read('corpus/shiji/120-identities.json')['decisions'] if d['id'] == 'd-shiji120-final-context-04')
        self.assertEqual(decision['person_id'], 'nuf_tb9_fjs_A')
        self.assertTrue(any(e['paragraph_id'] == 'c-shiji-107-weiqi:p022' and e['quote'] == '內史鄭當時是魏其，後不敢堅對。' for e in decision['evidence']))

    def test_authorial_taishigong_does_not_reassign_father_tan(self):
        father = 'pme_eis_xqi_*A*AAAA'
        son = 'pme_eis_xqi_*A*AAAAA'
        ch = read('corpus/shiji/130.json')
        p = next(p for p in ch['paragraphs'] if p['id'] == 'c-shiji-130-taishigong:p003')
        self.assertEqual({m['person_id'] for m in p['mentions'] if m['surface'] == '太史公'}, {father})
        decision = next(d for d in read('corpus/shiji/120-identities.json')['decisions'] if d['id'] == 'd-shiji120-final-context-05')
        self.assertEqual(decision['person_id'], son)
        self.assertIn('不證本段親撰', decision['rationale'])

    def test_received_death_mentions_keep_unspecified_years(self):
        event = next(e for e in read('corpus/shiji/120-life-events.json')['events'] if e['id'] == 'le-shiji120-005')
        self.assertEqual(event['person_id'], '4kq_1x4_48g')
        self.assertIsNone(event['date_expression'])
        self.assertIn('鄭君死孝文時', event['evidence'][0]['quote'])
        xiang = next(e for e in read('corpus/shiji/120-life-events.json')['events'] if e['id'] == 'le-shiji120-004')
        self.assertEqual(xiang['person_id'], 'ob7_g6i_7pp')
        self.assertIsNone(xiang['date_expression'])

    def test_five_decisions_remain_provisional_with_exact_target_markers(self):
        rows = [d for d in read('corpus/shiji/120-identities.json')['decisions'] if d['id'].startswith('d-shiji120-final-context-')]
        self.assertEqual(len(rows), 5)
        self.assertEqual(sum(len(d['identification_basis']['target_mention_ids']) for d in rows), 8)
        for d in rows:
            self.assertFalse(d['human_reviewed'])
            self.assertIsNone(d['model'])
            self.assertEqual(d['status'], 'contextual_provisional')

if __name__ == '__main__':
    unittest.main()
