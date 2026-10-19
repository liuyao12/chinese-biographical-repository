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
