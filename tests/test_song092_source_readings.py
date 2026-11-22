import copy
import hashlib
import json
from pathlib import Path
import unittest

from scripts.uncle_parentage import explicit_maternal_uncle_valid


ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads((ROOT / path).read_bytes())


class SongshuOfficialReadings(unittest.TestCase):
    def test_wang_jie_and_his_eldest_son(self):
        from scripts.song092_officials_kin import valid

        stem = 'corpus/jinshu/051-wangjie-qianqi'
        chapter = load(stem + '.json')
        father, son = chapter['paragraphs']
        fact, = load(stem + '-assertions.json')['assertions']
        anchor, = fact['evidence']
        receipt = load('source-evidence/song092-wangxinzhi/reading.json')['kinship_corroboration']
        name, = [m for m in father['mentions'] if m['id'] == receipt['antecedent_mention_id']]
        self.assertEqual((father['id'], father['text'], name['surface'], name['person_id']),
                         (receipt['antecedent_paragraph_id'], receipt['antecedent_quote'], '王接', fact['object_person_id']))
        self.assertEqual((fact['id'], anchor['paragraph_id'], fact['qualifiers']['source_term']),
                         (receipt['assertion_id'], son['id'], '長子愆期'))
        self.assertTrue(valid(fact, anchor, chapter, ROOT))
        self.assertFalse(valid(dict(fact, object_person_id=fact['subject_person_id']), anchor, chapter, ROOT))
        self.assertFalse(valid(fact, dict(anchor, object_person_reference_id=name['id']), chapter, ROOT))

    def test_edition_keeps_the_gap_in_the_burial_phrase(self):
        digital = load('corpus/songshu/092.json')
        printed = load('corpus/songshu/092-wangzhenzhi-wyd.json')
        proof = load(printed['annotation']['print_projection_ref'])
        self.assertIn('上虞舊墓。葬畢', digital['paragraphs'][1]['text'])
        self.assertIn('還上虞舊基畢', printed['paragraphs'][1]['text'])
        self.assertEqual([(r['digital'], r['printed']) for r in proof['differences']
                          if len(r['digital']) != len(r['printed'])], [('墓葬', '基')])
        self.assertEqual([r['pdf_page'] for r in proof['images']], [91, 92, 93])
        self.assertEqual(len(proof['columns']), 23)
        self.assertEqual(sum(len(r['reading']) for r in proof['columns']), 475)
        old_id = 'c-songshu-092-wangzhenzhi:line014:m0129'
        mother, = [r for r in digital['annotation']['person_reference_occurrences'] if r['id'] == old_id]
        self.assertEqual((mother['person_id'], mother['quote']), ('p48_ngr_u0u', '以母老求補安成太守'))

    def test_wang_sui_and_huan_xuan_in_unpunctuated_print(self):
        path = 'corpus/songshu/092-wangzhenzhi-wyd'
        chapter = load(path + '.json')
        paragraphs = {p['id']: (chapter['id'], p) for p in chapter['paragraphs']}
        uncle, = [r for r in load(path + '-assertions.json')['assertions'] if r['predicate'] == 'maternal_uncle']
        self.assertTrue(explicit_maternal_uncle_valid(uncle, paragraphs))
        wrong = copy.deepcopy(uncle)
        wrong['evidence'][0]['object_person_mention_id'] = wrong['evidence'][0]['subject_person_mention_id']
        self.assertFalse(explicit_maternal_uncle_valid(wrong, paragraphs))
        wrong = copy.deepcopy(uncle)
        wrong['qualifiers']['source_term'] = '玄之外甥'
        self.assertFalse(explicit_maternal_uncle_valid(wrong, paragraphs))

    def test_memorial_and_attestations(self):
        path = 'corpus/songshu/092-xunli-xunxing'
        chapter = load(path + '.json')
        paragraphs = {p['id']: p for p in chapter['paragraphs']}
        shared = [r for r in load(path + '-titles.json')['holdings'] if r['title'] == '散騎常侍']
        self.assertEqual({r['person_id'] for r in shared}, {'bd2_8y8_397', 'vhw_07a_wzm_AB'})
        anchors = {r['attestations'][0]['person_mention_id'] for r in shared}
        first = chapter['paragraphs'][0]
        self.assertEqual({m['surface'] for m in first['mentions'] if m['id'] in anchors}, {'王歆之', '孔默之'})
        proof = load('source-evidence/song092-xunli/reading.json')
        self.assertEqual(len(proof['boundaries']), 13)
        witness = proof['print_readings']
        self.assertEqual(hashlib.sha256((ROOT / witness['column_file']).read_bytes()).hexdigest(),
                         witness['column_file_sha256'])
        self.assertEqual((len(witness['columns']), sum(len(c['text']) for c in witness['columns'])), (33, 642))
        self.assertIn(('泰', '太'), {(v['received'], v['printed']) for v in witness['differences']})
        self.assertIn(('啟玄', '啓𤣥'), {(v['received'], v['printed']) for v in witness['differences']})
        for row in proof['boundaries']:
            para = paragraphs[row['paragraph_id']]
            for raw, printed in zip(row['raw_segments'], row['print_columns'], strict=True):
                quote = raw['source_quote']
                self.assertEqual(para['text'][raw['start_codepoint']:raw['end_codepoint']], quote)
                self.assertEqual(len(''.join(p['text'] for p in printed)), sum(c.isalnum() for c in quote))
        for w in proof['external_witnesses']:
            data = (ROOT / w['raw_path']).read_bytes()
            self.assertEqual(hashlib.sha256(data).hexdigest(), w['raw_sha256'])
            self.assertEqual(data.decode().splitlines()[w['line'] - 1][w['start']:w['end']], w['source_quote'])

    def test_complete_inventory_and_scope_of_each_biography(self):
        inventory = load('data/corpus/six-dynasties-biographies.json')
        survey, = [s for s in inventory['volume_surveys'] if s['book_id'] == 'b-songshu-092']
        notes = load(survey['source_review_path'])
        raw = (ROOT / survey['raw_path']).read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), notes['sha256'])
        lines = raw.decode().splitlines()
        self.assertEqual(notes['raw_body_lines'], [n for n in range(12, 80)
                         if lines[n - 1] and not lines[n - 1].startswith('=')])
        intervals = {n: [] for n in notes['raw_body_lines']}
        rows = [r for r in inventory['biographies'] if r['book_id'] == survey['book_id']]
        self.assertEqual(len(rows), 30)
        for row in rows:
            self.assertTrue(row['item_reviewed'], row['title'])
            for s in [row, *row.get('continuation_spans', [])]:
                for n in range(s['first_line'], s['last_line'] + 1):
                    if n in intervals:
                        start = s['start_codepoint'] if n == s['first_line'] else 0
                        end = s['end_codepoint'] if n == s['last_line'] else len(lines[n-1])
                        intervals[n].append((start, end, row['title']))
        for n, parts in intervals.items():
            cursor = 0
            for start, end, title in sorted(parts):
                self.assertEqual(cursor, start, (n, title))
                self.assertGreater(end, start)
                cursor = end
            self.assertEqual(cursor, len(lines[n - 1]), n)
