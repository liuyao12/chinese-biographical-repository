# coding: utf-8
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CID = 'c-hanshu-050-zhangfengjizheng'
BID = 'b-hanshu-050'

def read(path):
    return json.loads((ROOT / path).read_text())

class Hanshu050SourceTests(unittest.TestCase):
    def test_partial_scope_and_exact_fixed_source_extraction(self):
        chapter = read('corpus/hanshu/050.json')
        self.assertEqual(chapter['source']['text_scope'], 'partial_chapter')
        self.assertEqual(len(chapter['paragraphs']), 9)
        self.assertFalse(chapter['source']['image_verified'])
        self.assertEqual(chapter['source']['source_commit'], '683113d4baf6febecaf2ccb7913df87c4d68d454')
        self.assertEqual(chapter['source']['source_blob_sha'], '883ed25b93ffce6f13fe4f1ce42f0519ded60cf3')
        by_id = {p['id']: p for p in chapter['paragraphs']}
        for excerpt in chapter['source']['normalization']['excerpts']:
            self.assertEqual(hashlib.sha256(excerpt['raw_quote'].encode()).hexdigest(), excerpt['raw_quote_sha256'])
            scope = excerpt['body_selection']
            text = excerpt['body_before_excerpt_selection'][scope['start']:scope['end']]
            self.assertEqual(text, by_id[excerpt['proposed_paragraph_id']]['text'])
            self.assertTrue(text.startswith(scope['begin_anchor']))
            self.assertTrue(text.endswith(scope['end_anchor']))
            for note in excerpt['commentary']:
                self.assertEqual(excerpt['raw_quote'][note['raw_start']:note['raw_end']], note['raw_quote'])

    def test_registered_native_work_book_and_incomplete_progress(self):
        work = next(w for w in read('registry/works.json')['works'] if w['id'] == 'w-hanshu')
        book = next(b for b in work['books'] if b['id'] == BID)
        self.assertEqual((book['work_id'], book['number'], book['chapter_ids']), ('w-hanshu', 50, [CID]))
        progress = next(b for b in read('corpus/progress.json')['books'] if b['book_id'] == BID)
        self.assertFalse(progress['complete'])
        self.assertEqual(progress['text_status'], 'partial_transcription')

    def test_seventy_two_person_markers_and_twenty_four_crosswork_decisions(self):
        chapter = read('corpus/hanshu/050.json')
        people = {p['id']: p for p in read('registry/persons.json')['persons']}
        person_count = unresolved_count = 0
        ids = set()
        for p in chapter['paragraphs']:
            for m in p['mentions']:
                self.assertEqual(p['text'][m['start']:m['end']], m['surface'])
                if m['person_id']:
                    person_count += 1
                    ids.add(m['person_id'])
                    evidence = next(e for e in people[m['person_id']]['evidence'] if e['mention_id'] == m['id'])
                    self.assertEqual((evidence['work_id'], evidence['book_id'], evidence['chapter_id']), ('w-hanshu', BID, CID))
                else:
                    unresolved_count += 1
        self.assertEqual((person_count, unresolved_count, len(ids)), (72, 7, 24))
        decisions = read('corpus/hanshu/050-identities.json')['decisions']
        self.assertEqual({d['person_id'] for d in decisions}, ids)
        for d in decisions:
            self.assertIn('c-shiji-120-jizheng', d['chapter_ids'])
            self.assertFalse(d['human_reviewed'])
            self.assertIsNone(d['model'])

    def test_source_variants_and_commentary_are_not_silently_corrected(self):
        chapter = read('corpus/hanshu/050.json')
        text = '\n'.join(p['text'] for p in chapter['paragraphs'])
        for phrase in ['至黯十世', '居淮陽十歳而卒', '黯姊子司馬安', '遷為大司農', '當時為大吏']:
            self.assertIn(phrase, text)
        shiji = '\n'.join(p['text'] for p in read('corpus/shiji/120.json')['paragraphs'])
        for phrase in ['至黯七世', '七歲而卒', '黯姑姊子司馬安', '遷為大農令', '莊為太史']:
            self.assertIn(phrase, shiji)
        self.assertNotIn('師古曰', text)
        self.assertNotIn('皇后凡也', text)
        raw = ''.join(e['raw_quote'] for e in chapter['source']['normalization']['excerpts'])
        self.assertIn('皇后/凡也', raw)
        self.assertIn('孟賁夏育皆/古之勇士也', raw)

    def test_sima_an_maternal_uncle_retains_unknown_mother(self):
        rows = read('corpus/hanshu/050-assertions.json')['assertions']
        relation = next(a for a in rows if a['id'] == 'a-hanshu050-kin-003')
        self.assertEqual((relation['subject_person_id'], relation['predicate'], relation['object_person_id']),
                         ('84g_35d_vcn', 'maternal_uncle', 'fmh_dmt_cql'))
        self.assertEqual(relation['qualifiers'], {'source_term': '姊子', 'lineage': 'maternal',
                         'generation_difference': -1, 'mother_person_id': None})
        self.assertIn('黯姊子司馬安', relation['evidence'][0]['quote'])
        self.assertFalse(any(a['subject_person_id'] == '84g_35d_vcn' and a['predicate'] in ['father', 'mother'] for a in rows))

    def test_title_and_character_boundaries_preserve_hypothetical_ruler(self):
        chapter = read('corpus/hanshu/050.json')
        intro = next(p for p in chapter['paragraphs'] if p['id'].endswith(':jian:p-intro-001'))
        for token in ['以嚴見憚', '太子洗馬']:
            start = intro['text'].index(token)
            self.assertFalse(any(start <= m['start'] < start + len(token) for m in intro['mentions']))
        illness = next(p for p in chapter['paragraphs'] if p['id'].endswith(':jian:p002'))
        hypothetical = next(m for m in illness['mentions'] if m['surface'] == '少主')
        self.assertIsNone(hypothetical['person_id'])
        self.assertEqual({m['person_id'] for m in illness['mentions'] if m['surface'] in ['賁', '育']}, {'dwv_5hn_680', '66l_m67_5ie'})

class Hanshu050PublicProfileTests(unittest.TestCase):
    def test_head_origins_are_exported_without_birth_or_modern_place_claims(self):
        for pid, name in [('fmh_dmt_cql', '濮陽'), ('jws_b08_hob', '陳')]:
            profile = read('data/corpus/profiles/' + pid + '.json')
            entry = next(a for a in profile['addresses'] if a['id'].startswith('pa-hanshu050-origin-'))
            self.assertEqual(entry['relation'], 'biographical_origin')
            self.assertEqual(entry['place'], {'source_name': name, 'place_id': None, 'modern_identification': None})
            self.assertEqual(entry['source_term'], name + '人也')
            self.assertEqual((entry['evidence'][0]['work_id'], entry['evidence'][0]['book_id']), ('w-hanshu', BID))

    def test_all_new_mentions_have_work_scoped_api_occurrences(self):
        chapter = read('corpus/hanshu/050.json')
        for p in chapter['paragraphs']:
            for m in p['mentions']:
                if not m['person_id']:
                    continue
                profile = read('data/corpus/profiles/' + m['person_id'] + '.json')
                self.assertTrue(any(o['work_id'] == 'w-hanshu' and o['book_id'] == BID and o['chapter_id'] == CID
                                    and p['id'] in o['paragraph_ids'] and m['id'] in o['mention_ids'] for o in profile['occurrences']))

    def test_full_name_and_maternal_relation_are_exported(self):
        name = next(n for n in read('data/corpus/profile-names.json')['records'] if n['person_id'] == 'e08_fra_mj5')
        self.assertEqual((name['title'], name['surname'], name['ming']), ('宗正', '劉', '棄疾'))
        person = read('data/corpus/profiles/84g_35d_vcn.json')
        relation = next(r for r in person['relations'] if r['id'] == 'a-hanshu050-kin-003')
        self.assertEqual(relation['predicate'], 'maternal_uncle')
        self.assertIsNone(relation['qualifiers']['mother_person_id'])

if __name__ == '__main__':
    unittest.main()
