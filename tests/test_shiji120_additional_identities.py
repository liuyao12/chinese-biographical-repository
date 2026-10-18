# coding: utf-8
"""Contextual identities in 汲鄭 and the related 王信 account."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = json.loads((ROOT / 'tests/fixtures/shiji120-additional-identities.json').read_text())

def read(rel):
    return json.loads((ROOT / rel).read_text())

class JizhengAdditionalIdentityTests(unittest.TestCase):
    def test_thirteen_original_markers_resolve_without_changed_spans(self):
        self.assertEqual(len(FIXTURE['mentions']), 13)
        for ref in FIXTURE['mentions']:
            paragraph = next(p for p in read(ref['chapter_path'])['paragraphs'] if p['id'] == ref['paragraph_id'])
            marker = next(m for m in paragraph['mentions'] if m['id'] == ref['marker']['id'])
            self.assertEqual(marker, ref['marker'])
            self.assertEqual(paragraph['text'], FIXTURE['raw_paragraphs'][paragraph['id']])

    def test_retired_ids_have_no_registry_or_public_profile(self):
        people = {p['id']: p for p in read('registry/persons.json')['persons']}
        for old in FIXTURE['mapping']:
            self.assertNotIn(old, people)
            self.assertFalse((ROOT / 'data/corpus/profiles' / (old + '.json')).exists())
            self.assertFalse((ROOT / 'exports/persons' / (old + '.json')).exists())

    def test_wang_xin_remains_son_of_wang_zhong(self):
        person = next(p for p in read('registry/persons.json')['persons'] if p['id'] == '6d6_eg1_o3a_B')
        self.assertEqual(person['family_path']['parent_person_id'], '6d6_eg1_o3a')
        self.assertEqual(person['family_path']['source_assertion_id'], 'a-shiji049-019')
        self.assertEqual(person['label'], '王信')
        self.assertEqual(person['family_path']['generation_distance'], 1)

    def test_taihou_is_wang_not_nearest_empress_dowager(self):
        chapter = read('corpus/shiji/120.json')
        marker = next(m for p in chapter['paragraphs'] for m in p['mentions'] if m['id'] == 'c-shiji-120-jizheng:m003-0004')
        self.assertEqual((marker['surface'], marker['kind'], marker['person_id'], marker['status']),
                         ('太后', 'person', '6d6_eg1_o3a_A', 'contextual_provisional'))
        decision = next(d for d in read('corpus/shiji/120-identities.json')['decisions'] if d['id'] == 'd-shiji120-wang-taihou')
        self.assertEqual({e['chapter_id'] for e in decision['evidence']},
                         {'c-shiji-120-jizheng', 'c-shiji-107-weiqi', 'c-shiji-012-wudi'})

    def test_wang_xin_profile_name_is_attested_without_invented_date(self):
        record = next(n for n in read('data/corpus/profile-names.json')['records'] if n['person_id'] == '6d6_eg1_o3a_B')
        self.assertEqual((record['title'], record['surname'], record['ming']), ('蓋侯', '王', '信'))
        self.assertEqual(record['paragraph_id'], 'c-shiji-057-zhou:p023')
        self.assertEqual(record['quote'], '死後，景帝乃封王信為蓋侯。')
        self.assertNotIn('effective_period', record)

    def test_eight_decisions_are_provisional_and_have_actual_chapter_scope(self):
        count = 0
        for number in ['057', '120']:
            data = read(f'corpus/shiji/{number}-identities.json')
            for d in data['decisions']:
                if d['id'] == 'd-shiji057-wangxin-cross-chapter' or d['id'].startswith('d-shiji120-additional-') or d['id'] == 'd-shiji120-wang-taihou':
                    self.assertIn(data['chapter_id'], d['chapter_ids'])
                    self.assertFalse(d['human_reviewed'])
                    self.assertIsNone(d['model'])
                    self.assertEqual(d['status'], 'contextual_provisional')
                    for ref in d.get('references', []):
                        self.assertFalse(ref['image_verified'])
                        self.assertTrue(ref['display_claim_is_paraphrase'])
                        self.assertIn(ref['source_commit'], ref['url'])
                    count += 1
        self.assertEqual(count, 8)

    def test_hypothetical_young_ruler_remains_unresolved(self):
        p = next(p for p in read('corpus/shiji/120.json')['paragraphs'] if p['id'] == 'c-shiji-120-jizheng:p004')
        marker = next(m for m in p['mentions'] if m['surface'] == '少主')
        self.assertIsNone(marker['person_id'])
        self.assertIn('雖自謂賁育亦不能奪之矣', p['text'])

if __name__ == '__main__':
    unittest.main()
