# coding: utf-8
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KEEP = '20b_1c2_a06'
OLD = 'yt9_gts_k6b'
DID = 'd-songshu060-chuwei-cross-chapter'


def load(path):
    return json.loads((ROOT / path).read_text())


class ChuWeiIdentityTests(unittest.TestCase):
    def test_same_event_has_one_person_and_original_source_words(self):
        song = load('corpus/songshu/060.json')
        paragraph = next(p for p in song['paragraphs'] if p['id'] == 'c-songshu-060-xunbozi:p004')
        mention = next(m for m in paragraph['mentions'] if m['id'] == 'c-songshu-060-xunbozi:p004:m0085')
        self.assertEqual(mention['person_id'], KEEP)
        self.assertEqual(mention['identity_decision_id'], DID)
        self.assertEqual(paragraph['text'][mention['start']:mention['end']], '楚王瑋')
        self.assertIn('故楚王瑋矯詔致禍', paragraph['text'])
        jin = load('corpus/jinshu/042-taiyuan-wang.json')
        paragraph = next(p for p in jin['paragraphs'] if p['id'] == 'c-jinshu-042-taiyuan-wang:line023')
        self.assertIn('瑋以矯詔伏誅', paragraph['text'])
        self.assertEqual({m['person_id'] for m in paragraph['mentions'] if m['surface'] in ['楚王瑋', '瑋']}, {KEEP})

    def test_reverse_evidence_complete_without_id_alias(self):
        people = {p['id']: p for p in load('registry/persons.json')['persons']}
        self.assertNotIn(OLD, people)
        self.assertTrue(any(e.get('mention_id') == 'c-songshu-060-xunbozi:p004:m0085' for e in people[KEEP]['evidence']))
        self.assertFalse(any(OLD in p.get('id_aliases', []) for p in people.values()))
        decision = next(d for d in load('corpus/songshu/060-identities.json')['decisions'] if d['id'] == DID)
        self.assertEqual(decision['person_id'], KEEP)
        self.assertEqual({e['work_id'] for e in decision['evidence']}, {'w-songshu', 'w-jinshu'})
        self.assertFalse(decision['human_reviewed'])

    def test_retired_public_endpoints_removed(self):
        for area in ['exports/persons', 'data/corpus/profiles', 'data/corpus/persons']:
            self.assertFalse((ROOT / area / (OLD + '.json')).exists())
        index = load('exports/persons/index.json')
        self.assertNotIn(OLD, {p['person_id'] for p in index['persons']})
        self.assertNotIn(OLD, index.get('id_aliases', {}))
        for path in (ROOT / 'exports/persons').glob('*.md'):
            self.assertNotIn(OLD, path.read_text(), str(path))
        receipt = load('source-evidence/chuwei-cross-chapter/annotation-chain.json')
        self.assertEqual(receipt['retired_person_ids'], [OLD])
        self.assertFalse(receipt['person_aliases_created'])


if __name__ == '__main__':
    unittest.main()
