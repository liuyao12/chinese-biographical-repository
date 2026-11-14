# coding: utf-8
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def read(path):
    return json.loads((ROOT / path).read_text())

class WangBinSourceFamily(unittest.TestCase):
    def test_complete_units_keep_raw_text_and_exact_person_spans(self):
        for file, lines in [('076-wangbin', [46, 48, 50, 52]), ('076-wangleng', [92, 94])]:
            c = read('corpus/jinshu/' + file + '.json')
            self.assertEqual(c['source']['revision_id'], 2180533)
            self.assertEqual([p['source_position']['first_line'] for p in c['paragraphs']], lines)
            for p, raw in zip(c['paragraphs'], c['source']['normalization']['excerpts']):
                self.assertEqual(hashlib.sha256(raw['raw_quote'].encode()).hexdigest(), raw['raw_quote_sha256'])
                self.assertEqual(hashlib.sha256(p['text'].encode()).hexdigest(), raw['selected_text_sha256'])
                for m in p['mentions']:
                    self.assertEqual(p['text'][m['start']:m['end']], m['surface'])

    def test_eldest_son_is_numeric_but_next_son_keeps_relative_order(self):
        rows = {a['id']: a for a in read('corpus/jinshu/076-wangbin-assertions.json')['assertions']}
        eldest = rows['a-jinshu076-pengzhi-father']['qualifiers']['birth_order']
        self.assertEqual((eldest['scope'], eldest['ordinal']), ('sons_of_parent', 1))
        self.assertNotIn('birth_order', rows['a-jinshu076-biaozhi-father']['qualifiers'])
        relative = rows['a-jinshu076-pengzhi-biaozhi-brother']['qualifiers']['relative_birth_order']
        self.assertEqual((relative['operator'], relative['older_ordinal'], relative['younger_ordinal']), ('lt', 1, None))
        brother = rows['a-jinshu076-yi-bin-brother']
        self.assertEqual(brother['subject_person_id'], '7r6_k52_qji_ABDA')
        self.assertEqual(brother['object_person_id'], '7r6_k52_qji_ABDB')

    def test_shared_fathers_are_inferences_and_named_fathers_keep_sources(self):
        f = next(f for f in read('registry/family-assemblies.json')['assemblies'] if f['id'] == 'family-langye-wang-dao')
        members = {m['person_id']: m for m in f['members']}
        for pid, parent in [('7r6_k52_qji_ABDB', '7r6_k52_qji_ABD'), ('7r6_k52_qji_ABFB', '7r6_k52_qji_ABF')]:
            m = members[pid]
            self.assertEqual(m['parent_person_id'], parent)
            self.assertIsNone(m['source_assertion_id'])
            self.assertEqual(m['parent_connection']['type'], 'shared_father_through_sibling')
        self.assertEqual(members['7r6_k52_qji_ABFA']['source_assertion_id'], 'a-jinshu076-leng-father')
        chen = [p for p in read('registry/persons.json')['persons'] if p['label'] == '王琛']
        self.assertEqual([p['id'] for p in chen], ['7r6_k52_qji_ABF'])

    def test_nephew_does_not_acquire_the_nearest_named_brothers_father(self):
        person = next(p for p in read('registry/persons.json')['persons'] if p['label'] == '王籍之')
        self.assertEqual(len(person['id']), 11)
        for file in ROOT.glob('corpus/**/*-assertions.json'):
            for a in json.loads(file.read_text()).get('assertions', []):
                self.assertFalse(a['subject_person_id'] == person['id'] and a['predicate'] == 'father')

    def test_named_han_and_ying_share_the_source_father_son_branch(self):
        people = {p['label']: p for p in read('registry/persons.json')['persons']}
        father, child = people['王含']['id'], people['王應']['id']
        self.assertEqual(child, father + '_A')
        rows = read('corpus/jinshu/076-wangbin-assertions.json')['assertions']
        a = next(a for a in rows if a['id'] == 'a-jinshu076-wangying-father')
        self.assertEqual((a['subject_person_id'], a['object_person_id']), (child, father))
        self.assertIn('王應勸含投彬', a['evidence'][0]['quote'])
        self.assertIn('沈含父子于江', a['evidence'][0]['quote'])
        family = next(f for f in read('registry/family-assemblies.json')['assemblies'] if f['id'] == 'family-wang-han-ying')
        self.assertEqual(family['members'][1]['source_assertion_id'], a['id'])

    def test_adjacent_brother_context_does_not_fabricate_an_object_mention(self):
        c = read('corpus/jinshu/076-wangleng.json')
        a = next(a for a in read('corpus/jinshu/076-wangleng-assertions.json')['assertions'] if 'context' in a)
        self.assertEqual(a['context']['paragraph_ids'], [p['id'] for p in c['paragraphs']])
        self.assertTrue(c['paragraphs'][1]['text'].startswith('弟侃'))
        self.assertNotIn('棱', c['paragraphs'][1]['text'])
        self.assertEqual(a['object_person_id'], '7r6_k52_qji_ABFA')

    def test_jurisdiction_inside_office_is_not_a_personal_metonym(self):
        c = read('corpus/jinshu/076-wangbin.json')
        office, dialogue = c['paragraphs'][1:3]
        self.assertIn('江州刺史', office['text'])
        self.assertFalse(any(m['surface'] == '江州' for m in office['mentions']))
        names = [m for m in dialogue['mentions'] if m['surface'] == '江州']
        self.assertEqual(len(names), 2)
        self.assertEqual({m['person_id'] for m in names}, {'7r6_k52_qji_ABDB'})
        decisions = read('corpus/jinshu/076-wangbin-identities.json')['decisions']
        d = next(d for d in decisions if d['id'] == 'd-jin076-bin-jiangzhou')
        self.assertEqual(set(d['identification_basis']['target_mention_ids']), {m['id'] for m in names})

if __name__ == '__main__':
    unittest.main()
