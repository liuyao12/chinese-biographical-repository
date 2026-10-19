# coding: utf-8
import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads((ROOT / path).read_text())


class NanshiWangFamily(unittest.TestCase):
    def setUp(self):
        self.c = read('corpus/nanshi/024.json')
        self.p = {p['source_position']['first_line']: p for p in self.c['paragraphs']}
        self.a = {a['id']: a for a in read('corpus/nanshi/024-assertions.json')['assertions']}

    def test_complete_selected_paragraphs_preserve_raw_spelling(self):
        self.assertEqual(sorted(self.p), [15, 17, 19, 21, 23, 25, 29, 33, 35, 37,
                                         39, 43, 45, 47, 49, 53, 57, 61, 63, 67,
                                         71, 73, 77, 79, 81])
        excerpts = {e['proposed_paragraph_id']: e for e in self.c['source']['normalization']['excerpts']}
        for p in self.c['paragraphs']:
            e = excerpts[p['id']]
            self.assertEqual(p['text'], re.sub(r'-\{([^{}]*)\}-', r'\1', e['raw_quote']))
            self.assertEqual(hashlib.sha256(e['raw_quote'].encode()).hexdigest(), e['raw_quote_sha256'])
            self.assertFalse(p['source_position']['editorial_excerpt_boundary'])
        self.assertIn('升之', self.p[29]['text'])
        self.assertIn('鎭南', self.p[45]['text'])

    def test_new_generations_share_existing_paternal_family(self):
        family = next(f for f in read('registry/family-assemblies.json')['assemblies']
                      if f['id'] == 'family-langye-wang-dao')
        members = {m['person_id']: m for m in family['members']}
        for key in ['xiuzhi', 'jun', 'cong', 'xin']:
            a = self.a['a-nanshi024-' + key + '-father']
            m = members[a['subject_person_id']]
            self.assertEqual(m['parent_person_id'], a['object_person_id'])
            self.assertEqual(m['source_assertion_id'], a['id'])
            self.assertTrue(m['person_id'].startswith(m['parent_person_id']))

    def test_lun_variants_bind_same_identity_using_shared_event(self):
        d = next(d for d in read('corpus/nanshi/024-identities.json')['decisions']
                 if d['id'] == 'd-nanshi024-lunzhi-variant')
        self.assertIn('綸之', self.p[53]['text'])
        qi = read('corpus/nanqishu/032.json')
        p = next(p for p in qi['paragraphs'] if p['source_position']['first_line'] == 89)
        self.assertIn('倫之', p['text'])
        self.assertEqual({m['person_id'] for m in self.p[53]['mentions'] if m['surface'] == '綸之'}, {d['person_id']})
        self.assertEqual({m['person_id'] for m in p['mentions'] if m['surface'] == '倫之'}, {d['person_id']})
        self.assertEqual({e['work_id'] for e in d['evidence']}, {'w-nanshi', 'w-nanqishu'})
        self.assertEqual(d['scope'], 'cross_chapter')
        self.assertEqual(set(d['chapter_ids']), {e['chapter_id'] for e in d['evidence']})

    def test_conflicting_received_years_are_not_silently_rewritten(self):
        self.assertIn('升明三年', self.p[21]['text'])
        song = read('corpus/songshu/066.json')
        self.assertTrue(any('昇明二年' in p['text'] for p in song['paragraphs']))
        self.assertIn('建元元年', self.p[45]['text'])
        qi = read('corpus/nanqishu/032.json')
        self.assertTrue(any('建元二年' in p['text'] for p in qi['paragraphs']))

    def test_dialogue_distinguishes_jun_cong_and_royal_speaker(self):
        p = self.p[67]
        ids = lambda surface: {m['person_id'] for m in p['mentions'] if m['surface'] == surface}
        self.assertEqual(ids('下官'), ids('峻'))
        self.assertNotEqual(ids('下官'), ids('琮'))
        self.assertEqual(ids('僕'), ids('始興王'))
        self.assertEqual(ids('殿下'), ids('始興王'))
        self.assertNotEqual(ids('謝仁祖'), ids('峻'))
        self.assertFalse(any(a['object_person_id'] in ids('謝仁祖') for a in self.a.values()
                             if a['predicate'] in ['father', 'grandfather', 'great_grandfather']
                             and a.get('qualifiers', {}).get('lineage') != 'maternal'))

    def test_qi_and_liang_wudi_and_an_cheng_remain_distinct(self):
        qi = next(m['person_id'] for m in self.p[53]['mentions'] if m['surface'] == '武帝')
        liang = next(m['person_id'] for m in self.p[61]['mentions'] if m['surface'] == '武帝')
        an = next(m['person_id'] for m in self.p[53]['mentions'] if m['surface'] == '安成王')
        self.assertEqual(len({qi, liang, an}), 3)


if __name__ == '__main__':
    unittest.main()
