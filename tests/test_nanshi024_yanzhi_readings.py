import copy
import hashlib
import json
from pathlib import Path
import unittest

from scripts.person_bundle import validate_former_given_name
from scripts.uncle_parentage import paired_nephews_valid


ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads((ROOT / path).read_bytes())


class NanshiYanzhiReadings(unittest.TestCase):
    def test_all_biography_boundaries_against_fixed_raw_lines(self):
        inventory = load('data/corpus/six-dynasties-biographies.json')
        book = 'b-nanshi-024'
        survey, = [s for s in inventory['volume_surveys'] if s['book_id'] == book]
        boundary = load(survey['source_review_path'])
        raw = (ROOT / survey['raw_path']).read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), boundary['sha256'])
        lines = raw.decode().splitlines()
        first = lines.index('=王裕之=') + 1
        end = lines.index('=論=')
        body = {i + 1: lines[i] for i in range(first, end)
                if lines[i] and not lines[i].startswith('=')}
        pieces = {int(k): v for k, v in boundary['coverage'].items()}
        self.assertEqual(body.keys(), pieces.keys())
        spans = {}
        for i, text in body.items():
            cursor = 0
            for piece in pieces[i]:
                start, stop = piece['start'], piece['end']
                self.assertEqual(start, cursor, (i, piece['title']))
                self.assertGreater(stop, start)
                self.assertEqual(text[start:stop], piece['quote'])
                spans.setdefault(piece['title'], []).append((i, start, stop))
                cursor = stop
            self.assertEqual(cursor, len(text), i)
        rows = [r for r in inventory['biographies'] if r['book_id'] == book]
        self.assertEqual((len(rows), len(body), sum(map(len, body.values()))), (40, 68, 8606))
        self.assertEqual(set(spans), {r['title'] for r in rows})
        for r in rows:
            self.assertTrue(r['item_reviewed'], r['title'])
            located = []
            for s in [r, *r.get('continuation_spans', [])]:
                for i in range(s['first_line'], s['last_line'] + 1):
                    if i in body:
                        start = s['start_codepoint'] if i == s['first_line'] else 0
                        end = s['end_codepoint'] if i == s['last_line'] else len(body[i])
                        located.append((i, start, end))
            self.assertEqual(sorted(located), sorted(spans[r['title']]), r['title'])
        comment = boundary['excluded_commentary']
        self.assertEqual(comment['quote'], lines[comment['line'] - 1])

    def test_former_name_belongs_to_deyuan(self):
        stem = 'corpus/nanshi/024-wangdeyuan'
        name, = load(stem + '-name-components.json')['records']
        paragraph, = load(stem + '.json')['paragraphs']
        validate_former_given_name(name, paragraph)
        for change in ({'former_ming': '劉湛'}, {'former_ming': '江湛'}, {'person_id': 'h3c_ulm_pto'},
                       {'quote': '劉湛、江湛，並不善終，此非佳名也。'}):
            with self.assertRaises(ValueError):
                validate_former_given_name(dict(name, **change), paragraph)

    def test_uncle_in_both_histories_and_print(self):
        for stem in ('nanqishu/032', 'nanshi/024', 'nanshi/024-yanzhi-ruantao-wyd'):
            path = 'corpus/' + stem
            chapter = load(path + '.json')
            paragraphs = {p['id']: (chapter['id'], p) for p in chapter['paragraphs']}
            assertions = load(path + '-assertions.json')['assertions']
            nephews = [a for a in assertions if a['qualifiers'].get('source_clause_binding', {}).get('kind')
                       == 'paired_named_nephews_of_named_uncle']
            self.assertEqual({a['subject_person_id'] for a in nephews},
                             {'7r6_k52_qji_ABDABAACA', '03n_n2r_8rt_***A'})
            for a in nephews:
                self.assertTrue(paired_nephews_valid(a, paragraphs))
                wrong = copy.deepcopy(a)
                wrong['evidence'][0]['object_person_mention_id'] = a['evidence'][0]['subject_person_mention_id']
                self.assertFalse(paired_nephews_valid(wrong, paragraphs))

    def test_three_witnesses_to_name_in_wang_xin(self):
        proof = load('source-evidence/nanshi024-wangyanzhi/xin-reading.json')
        self.assertEqual(proof['character_identification']['source_quote'], "['1357']={\"𤅢\"},")
        identities = load('corpus/nanshi/024-identities.json')['decisions']
        decision, = [d for d in identities if d['id'] == 'd-nan024-xin-xieyue']
        self.assertEqual(decision['person_id'], 'aa6_83c_juy_DBABAC')
        for stem, expected in [('nanshi/024', '謝伷'), ('nanshi/024-yanzhi-ruantao-wyd', '謝𤅢'),
                               ('nanqishu/043-xieyue', '謝𤅢')]:
            chapter = load('corpus/' + stem + '.json')
            e, = [e for e in decision['evidence'] if e['chapter_id'] == chapter['id']]
            p, = [p for p in chapter['paragraphs'] if p['id'] == e['paragraph_id']]
            m, = [m for m in p['mentions'] if m['id'] == e['person_mention_id']]
            self.assertEqual((p['text'][m['start']:m['end']], m['person_id']), (expected, decision['person_id']))

    def test_division_of_printed_biographies_and_grant_dates(self):
        inv = load('data/corpus/six-dynasties-biographies.json')
        survey, = [s for s in inv['volume_surveys'] if s['book_id'] == 'b-nanshi-024']
        cid = 'c-nanshi-024-yanzhi-ruantao-wyd'
        units = {r['title']: r for r in survey['text_witness_units'] if r['chapter_id'] == cid}
        self.assertEqual(set(units), {'王延之', '阮韜', '王綸之', '王昕'})
        p = load('corpus/nanshi/024-yanzhi-ruantao-wyd.json')['paragraphs'][2]
        boundary = p['text'].index('韜字長明')
        self.assertEqual(units['王延之']['paragraph_slices'][p['id']], [{'start': 0, 'end': boundary}])
        self.assertEqual(units['阮韜']['paragraph_slices'][p['id']], [{'start': boundary, 'end': len(p['text'])}])
        proof = load('source-evidence/nanshi024-wangyanzhi/yan-reading.json')
        grant, = [r for r in proof['chronology'] if r.get('action') == '進號鎮南將軍']
        self.assertEqual((grant['term'], grant['year'], grant['parallel_term'], grant['parallel_year']),
                         ('建元元年', 479, '建元二年', 480))

    def test_speaker_in_wang_cong_biography(self):
        book = load('corpus/nanshi/024-wangjun-wangcong-wyd.json')
        readings = {r['source_quote']: r for r in book['annotation']['source_reading_cases']
                    if r['kind'] == 'witness_collation'}
        self.assertEqual(readings['下官曾祖是謝仁祖外孫']['person_id'], '7r6_k52_qji_ABDABAABAA')
        self.assertEqual(readings['覽自吏部尚書出為吳興郡']['person_id'], 'g2h_mgn_tvz')
