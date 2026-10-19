# coding: utf-8
import copy
import json
import unittest
from pathlib import Path
from scripts.ancestry_chain import consecutive_ancestor_parent_valid
ROOT = Path(__file__).resolve().parents[1]
def read(p):
    return json.loads((ROOT / p).read_text())

class ChuReceivedUnits(unittest.TestCase):
    def setUp(self):
        self.chapters = {c['id']: c for c in [read('corpus/jinshu/' + stem + '.json') for stem in ['093-chushuang', '032-chu-lingyuan']]}
        self.relations = {a['id']: a for stem in ['093-chushuang', '032-chu-lingyuan'] for a in read('corpus/jinshu/' + stem + '-assertions.json')['assertions']}
        self.family = next(f for f in read('registry/family-assemblies.json')['assemblies'] if f['id'] == 'family-henan-yangdi-chu')
        extra = read('corpus/jinshu/093-chupou.json')
        self.ancestry_chapters = dict(self.chapters, **{extra['id']: extra})
        self.ancestry_relations = dict(self.relations, **{a['id']: a for a in read('corpus/jinshu/093-chupou-assertions.json')['assertions']})
    def test_two_complete_paragraphs_preserve_unusual_nickname_and_real_spans(self):
        self.assertEqual(sum(len(c['paragraphs']) for c in self.chapters.values()), 2)
        self.assertEqual(sum(len(p['mentions']) for c in self.chapters.values() for p in c['paragraphs']), 21)
        for c in self.chapters.values():
            for p in c['paragraphs']:
                for m in p['mentions']:
                    self.assertEqual(p['text'][m['start']:m['end']], m['surface'])
        p = self.chapters['c-jinshu-093-chushuang']['paragraphs'][0]
        nicknames = [m for m in p['mentions'] if m['surface'] in ['斯生', '期生']]
        self.assertEqual(len(nicknames), 2)
        self.assertEqual(len({m['person_id'] for m in nicknames}), 1)
    def test_father_between_named_ancestors_is_inferred_and_rejects_other_subject(self):
        rows = {m['person_id']: m for m in self.family['members']}
        jia = rows['xke_dj3_6ba_A']
        self.assertIsNone(jia['source_assertion_id'])
        self.assertTrue(consecutive_ancestor_parent_valid(jia, rows, self.ancestry_relations, self.ancestry_chapters))
        bad = copy.deepcopy(jia)
        bad['parent_connection']['chain_subject_person_id'] = 'xke_dj3_6ba_AAAAA'
        self.assertFalse(consecutive_ancestor_parent_valid(bad, rows, self.ancestry_relations, self.ancestry_chapters))
    def test_xin_now_has_direct_father_source_without_deleting_grandfather_evidence(self):
        xin = next(m for m in self.family['members'] if m['person_id'] == 'xke_dj3_6ba_AAA')
        self.assertEqual(xin['source_assertion_id'], 'a-jinshu-chu-xin-father-explicit')
        self.assertNotIn('parent_connection', xin)
        self.assertEqual(self.ancestry_relations[xin['source_assertion_id']]['qualifiers']['source_term'], '子歆')
        self.assertIn('a-jinshu-chu-shuang-grandfather', self.ancestry_relations)

    def test_princesses_have_explicit_mother_without_father_or_order(self):
        mothers = [a for a in self.relations.values() if a['predicate'] == 'mother']
        self.assertEqual(len(mothers), 2)
        for a in mothers:
            self.assertEqual(a['object_person_id'], 'xke_dj3_6ba_AAAAD')
            self.assertFalse(any(b['subject_person_id'] == a['subject_person_id'] and b['predicate'] == 'father' for b in self.relations.values()))
            self.assertNotIn('birth_order', a['qualifiers'])
    def test_parallel_daughter_assertions_retain_two_source_chapters(self):
        rows = [a for a in self.relations.values() if a['subject_person_id'] == 'xke_dj3_6ba_AAAAD' and a['predicate'] == 'father']
        self.assertEqual(len(rows), 2)
        self.assertEqual({a['object_person_id'] for a in rows}, {'xke_dj3_6ba_AAAA'})
        self.assertEqual(len({a['evidence'][0]['chapter_id'] for a in rows}), 2)
    def test_listed_sons_do_not_gain_absolute_birth_order(self):
        for a in self.relations.values():
            self.assertNotIn('birth_order', a['qualifiers'])
if __name__ == '__main__':
    unittest.main()
