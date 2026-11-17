# coding: utf-8
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


class NingxingIdentityReconciliationTests(unittest.TestCase):
    def test_anonymous_physician_reference_is_not_a_name_mention(self):
        chapter = read('corpus/shiji/125.json')
        reference, = [item for item in chapter['annotation']['person_reference_occurrences']
                      if item['id'] == 'c-shiji-125-ningxing:m002-0182']
        paragraph = next(p for p in chapter['paragraphs']
                         if p['id'] == 'c-shiji-125-ningxing:p002')
        self.assertEqual(reference['person_id'], 'w0i_qc3_tpy')
        self.assertEqual(reference['surface'], '善相者')
        self.assertFalse(any(m['id'] == reference['id'] for m in paragraph['mentions']))
        self.assertIn('《史記》與《漢書》', reference['rationale'])
        self.assertFalse(reference['human_reviewed'])

    def test_cross_chapter_person_ids_are_materialized_and_referenced(self):
        chapter = read('corpus/shiji/125.json')
        identities = {
            ('長公主', 'yqp_nlb_p1p_ACF'),
            ('周文仁', '2jn_tjp_75n'),
            ('仁', '2jn_tjp_75n'),
            ('彌子瑕', 'eb9_g6y_4q6'),
        }
        observed = {(m['surface'], m['person_id'])
                    for p in chapter['paragraphs'] for m in p['mentions']}
        self.assertTrue(identities <= observed)

        decisions = read('corpus/shiji/125-equivalences.json')['decisions']
        for decision_id in ('eq-shiji125-cross-004', 'eq-shiji125-cross-005',
                            'eq-shiji125-cross-006'):
            decision = next(d for d in decisions if d['id'] == decision_id)
            self.assertTrue(decision['identity_materialized'])
            self.assertEqual(len(decision['person_ids']), 1)
            self.assertEqual(decision['canonical_person_id'], decision['person_ids'][0])

    def test_retired_duplicate_ids_have_no_registry_or_public_profile(self):
        retired = ('qlu_yvc_mtu', 'qjf_e2p_lm1', 'leq_v5u_u2n',
                   'c0b_mpt_epd', 'ux5_ksp_tlb')
        people = {person['id'] for person in read('registry/persons.json')['persons']}
        for person_id in retired:
            with self.subTest(person_id=person_id):
                self.assertNotIn(person_id, people)
                self.assertFalse((ROOT / 'exports/persons' / f'{person_id}.json').exists())
                self.assertFalse((ROOT / 'data/corpus/profiles' / f'{person_id}.json').exists())
                self.assertFalse((ROOT / 'data/corpus/summaries' / f'{person_id}.json').exists())


if __name__ == '__main__':
    unittest.main()
