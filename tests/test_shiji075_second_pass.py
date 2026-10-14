import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class MengchangEvidenceTests(unittest.TestCase):
    def read(self, suffix, key):
        return json.loads((ROOT / ('corpus/shiji/075-' + suffix + '.json')).read_text())[key]

    def test_capture_and_unknown_birth_year_are_not_filled(self):
        events = self.read('life-events', 'events')
        self.assertFalse(any(e['person_id'] == 'egy_txn_xs1' for e in events))
        birth = next(e for e in events if e['event_type'] == 'birth')
        self.assertNotIn('normalized_date', birth)
        anonymous = [e for e in events if e['person_id'] in ('trw_uc5_2fn', 'ika_oa1_ubm')]
        self.assertEqual(len(anonymous), 2)
        self.assertNotEqual(anonymous[0]['evidence'][0]['paragraph_id'], anonymous[1]['evidence'][0]['paragraph_id'])

    def test_age_order_does_not_invent_ordinals_or_maternal_identity(self):
        assertions = {a['id']: a for a in self.read('assertions', 'assertions')}
        order = assertions['a-shiji075-002']['qualifiers']['birth_order']
        self.assertIsNone(order['ordinal'])
        self.assertEqual(order['position'], 'younger_or_youngest')
        qualifiers = assertions['a-shiji075-003']['qualifiers']
        self.assertNotIn('shared_mother', qualifiers)
        self.assertEqual(qualifiers['relative_birth_order']['operator'], 'lt')

    def test_residence_does_not_become_origin_or_burial(self):
        addresses = self.read('addresses', 'assertions')
        own = [a for a in addresses if a['person_id'] == '7pl_s0g_rkh']
        self.assertFalse(any(a['relation'] in ('biographical_origin', 'birth_place', 'death_place', 'burial_place') for a in own))
        self.assertFalse(any(a['evidence'][0]['paragraph_id'].endswith(':p005') for a in own))

    def test_retrospective_qi_king_resolves_without_rewriting_source(self):
        chapter = json.loads((ROOT / 'corpus/shiji/075.json').read_text())
        paragraphs = {p['id'].rsplit(':', 1)[1]: p for p in chapter['paragraphs']}
        self.assertTrue(paragraphs['p014']['text'].startswith('初，馮驩'))
        for key, count in [('p017', 6), ('p018', 1)]:
            paragraph = paragraphs[key]
            mentions = [m for m in paragraph['mentions'] if m.get('person_id') == 'lmu_nbm_rzo_AAAAAAABAAAAAAAA']
            self.assertEqual(len(mentions), count)
            for mention in mentions:
                self.assertIn(mention['surface'], ['齊王', '王'])
                self.assertEqual(paragraph['text'][mention['start']:mention['end']], mention['surface'])
        # 襄王連和段與馮驩向秦王的發言，不能因同稱王而一起改指。
        self.assertTrue(any(m.get('person_id') == 'sba_huu_hk2' for m in paragraphs['p013']['mentions']))
        self.assertTrue(any(m.get('person_id') == 'zp9_5vn_rqb' for m in paragraphs['p017']['mentions']))
        decision = next(d for d in self.read('equivalences', 'decisions') if d['id'] == 'eq-shiji075-feng-qi-min')
        self.assertEqual(decision['status'], 'contextual_provisional')
        self.assertFalse(decision['human_reviewed'])
