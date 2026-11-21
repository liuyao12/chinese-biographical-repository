import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def read(path):
    return json.loads((ROOT / path).read_text())

class Jin079LangDaiReading(unittest.TestCase):
    def test_fixed_text_and_each_quoted_source(self):
        review = read('source-evidence/jin079-lang-zhong-xuan-dai/reading.json')
        chapter = read('corpus/jinshu/079.json')
        main = (ROOT / review['raw_path']).read_bytes()
        self.assertEqual(hashlib.sha256(main).hexdigest(), review['sha256'])
        paragraphs = {p['id']: p for p in chapter['paragraphs']}
        for unit in review['unit_boundaries']:
            p = paragraphs[unit['paragraph_id']]
            pos = p['source_position']
            self.assertEqual(main.decode()[pos['raw_start']:pos['raw_end']], p['text'])
            self.assertEqual(unit['first_line'], pos['source_text_line'])
            self.assertTrue(unit['item_reviewed'])
        sources = {}
        for key, witness in review['external_witnesses'].items():
            raw = (ROOT / witness['raw_path']).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), witness['sha256'])
            sources[key] = raw.decode()
        for item in review['parallel_readings']:
            for passage in item['parallel_passages']:
                text = sources[passage['witness']]
                self.assertEqual(text[passage['raw_start']:passage['raw_end']], passage['raw_quote'])
                self.assertEqual(text[:passage['raw_start']].count('\n') + 1, passage['raw_line'])

    def test_philosophical_term_and_two_uncles(self):
        c = read('corpus/jinshu/079.json')
        p = next(p for p in c['paragraphs'] if p['id'].endswith(':p003'))
        names = {m['start']: m for m in p['mentions']}
        self.assertIsNone(names[14]['person_id'])
        self.assertEqual(names[14]['kind'], 'non_person')
        self.assertEqual(names[25]['person_id'], 'aa6_83c_juy_CD')
        review = read('source-evidence/jin079-lang-zhong-xuan-dai/reading.json')
        case = next(r for r in review['parallel_readings'] if r['scope'] == '兩代舅甥')
        rel = {a['id']: a for a in read('corpus/jinshu/079-assertions.json')['assertions']}
        for row in case['relationships']:
            native = rel[row['native_assertion_id']]
            for key in ('subject_person_id', 'predicate', 'object_person_id'):
                self.assertEqual(native[key], row[key])
        self.assertEqual(len({r['object_person_id'] for r in case['relationships']}), 3)

    def test_dai_sibling_order_and_enfeoffment_are_witness_specific(self):
        review = read('source-evidence/jin079-lang-zhong-xuan-dai/reading.json')
        case = next(r for r in review['parallel_readings'] if r['scope'] == '戴氏長幼與封爵')
        jin, shishuo, pedigree = case['claims']
        self.assertEqual((jin['older'], jin['younger']), (shishuo['younger'], shishuo['older']))
        self.assertEqual((jin['title'], pedigree['title']), ('廣信侯', '廣陵侯'))
        rel = next(a for a in read('corpus/jinshu/079-assertions.json')['assertions'] if a['id'] == 'a-jin079-dailu-daikui')
        order = rel['qualifiers']['relative_birth_order']
        self.assertEqual((order['older_person_id'], order['younger_person_id']), (jin['older'], jin['younger']))
