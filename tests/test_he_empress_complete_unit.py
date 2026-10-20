# coding: utf-8
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class HeEmpressCompleteUnitTests(unittest.TestCase):
    def test_complete_paragraphs_preserve_fixed_witness(self):
        chapter = json.loads((ROOT / 'corpus/jinshu/032-he-empress.json').read_text())
        excerpts = chapter['source']['normalization']['excerpts']
        self.assertEqual([p['source_position']['first_line'] for p in chapter['paragraphs']], [53, 55])
        self.assertEqual(chapter['source']['revision_id'], 1543614)
        for p, e in zip(chapter['paragraphs'], excerpts):
            self.assertEqual(hashlib.sha256(p['text'].encode()).hexdigest(), e['selected_text_sha256'])
            self.assertEqual(hashlib.sha256(e['raw_quote'].encode()).hexdigest(), e['raw_quote_sha256'])
            for m in p['mentions']:
                self.assertEqual(p['text'][m['start']:m['end']], m['surface'])
        self.assertTrue(chapter['paragraphs'][1]['text'].startswith('后無子。'))
        note = excerpts[1]['removed_digital_editorial_notes'][0]
        self.assertIn('原作「永興」', note['text'])
        self.assertFalse(note['independently_verified'])
        self.assertFalse(chapter['source']['image_verified'])

    def test_source_father_and_profile_name_share_current_identity(self):
        assertions = json.loads((ROOT / 'corpus/jinshu/032-he-empress-assertions.json').read_text())['assertions']
        self.assertEqual(len(assertions), 1)
        a = assertions[0]
        self.assertEqual((a['subject_person_id'], a['predicate'], a['object_person_id']),
                         ('3ea_uzt_2n2_A', 'father', '3ea_uzt_2n2'))
        self.assertEqual(a['qualifiers']['source_term'], '父準')
        names = json.loads((ROOT / 'data/corpus/profile-names.json').read_text())['records']
        n = next(n for n in names if n['person_id'] == '3ea_uzt_2n2_A')
        self.assertEqual((n['title'], n['surname'], n['ming']), ('穆章皇后', '何', '法倪'))
        assemblies = json.loads((ROOT / 'registry/family-assemblies.json').read_text())['assemblies']
        family = next(f for f in assemblies if f['id'] == 'family-he-zhun-fani')
        self.assertEqual(len(family['members']), 2)
        self.assertEqual(family['members'][1]['source_assertion_id'], a['id'])
        registry = json.loads((ROOT / 'registry/persons.json').read_text())['persons']
        self.assertFalse(any(p['id'] == 'l65_l8v_5ku' for p in registry))

    def test_two_officials_use_native_identity_evidence_and_keep_original_anchors(self):
        chapter = json.loads((ROOT / 'corpus/jinshu/032-he-empress.json').read_text())
        mentions = {m['surface']: m for m in chapter['paragraphs'][0]['mentions']}
        for surface, pid, mid in [('彪之', '7r6_k52_qji_ABDBB', 'c-jinshu-032-he-empress:line053:m0099'),
                                  ('洽', '7r6_k52_qji_ABAAA', 'c-jinshu-032-he-empress:line053:m0207')]:
            self.assertEqual(mentions[surface]['kind'], 'person')
            self.assertEqual((mentions[surface]['person_id'], mentions[surface]['id']), (pid, mid))
        decisions = json.loads((ROOT / 'corpus/jinshu/032-he-empress-identities.json').read_text())['decisions']
        officials = [d for d in decisions if d['id'] != 'd-jin032-he-aidi']
        self.assertEqual(len(officials), 2)
        self.assertEqual({d['references'][0]['book_id'] for d in officials}, {'b-jinshu-065', 'b-jinshu-076'})
        emperor = next(d for d in decisions if d['id'] == 'd-jin032-he-aidi')
        second = {m['surface']: m for m in chapter['paragraphs'][1]['mentions']}
        self.assertEqual(second['哀帝']['person_id'], 'emb_vx4_gm9')
        self.assertIn(second['哀帝']['id'], emperor['identification_basis']['target_mention_ids'])
        self.assertEqual(mentions['綜']['kind'], 'unresolved')

    def test_existing_jin32_selection_is_preserved(self):
        earlier = json.loads((ROOT / 'corpus/jinshu/032.json').read_text())
        self.assertEqual(earlier['id'], 'c-jinshu-032-zheng-achun-family')
        self.assertEqual(len(earlier['paragraphs']), 7)
        works = json.loads((ROOT / 'registry/works.json').read_text())
        book = next(b for w in works['works'] for b in w['books'] if b['id'] == 'b-jinshu-032')
        self.assertIn(earlier['id'], book['chapter_ids'])
        self.assertIn('c-jinshu-032-he-empress', book['chapter_ids'])

if __name__ == '__main__':
    unittest.main()
