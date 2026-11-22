import json
import unittest
from collections import Counter
from copy import deepcopy
from hashlib import sha256
from pathlib import Path

from scripts.chen017_appointments import SHU, valid
from scripts.six_dynasties_inventory import chapter_passage, source_paragraphs, source_passage

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / 'source-evidence/chenshu017-wangyuan'


def read(path):
    return json.loads((ROOT / path).read_bytes())


class ChenYuan(unittest.TestCase):
    def test_mixed_accounts_partition_the_fixed_volume_once(self):
        survey = read(EVIDENCE / 'volume-boundaries.json')
        raw = (ROOT / survey['raw_path']).read_bytes()
        self.assertEqual(sha256(raw).hexdigest(), survey['raw_sha256'])
        lines = raw.decode().splitlines()
        inventory = read('data/corpus/six-dynasties-biographies.json')
        entries = [v for v in inventory['biographies'] if v['book_id'] == survey['book_id']]
        self.assertEqual(len(entries), 10)
        assigned = Counter()
        for entry in entries:
            native = read(entry['chapter_path'])
            selected = source_passage(entry, lines, set(), set())
            self.assertEqual(source_paragraphs(selected, entry['source_layout']), chapter_passage(entry, native)[1])
            for span in [entry, *entry.get('continuation_spans', [])]:
                for n in range(span['first_line'], span['last_line'] + 1):
                    a = span['start_codepoint'] if n == span['first_line'] else 0
                    b = span['end_codepoint'] if n == span['last_line'] else len(lines[n-1])
                    assigned.update((n, j) for j in range(a, b))
        expected = {(n, j) for n in survey['body_lines'] for j in range(len(lines[n-1]))}
        self.assertEqual(len(expected), survey['body_codepoints'])
        self.assertEqual(assigned, Counter(expected))

    def test_annals_collations_and_distinct_appointments(self):
        for slug, count in [('yuanjing', 11), ('yuanshu', 34), ('chen-appraisal', 3)]:
            ledger = read(EVIDENCE / (slug + '-reading.json'))
            printed = read(EVIDENCE / (slug + '-wuyingdian.json'))
            self.assertEqual(len(printed['columns']), count)
            for witness in ledger['external_witnesses']:
                raw = (ROOT / witness['raw_path']).read_bytes()
                self.assertEqual(sha256(raw).hexdigest(), witness['raw_sha256'])
                lines = raw.decode().splitlines()
                for quote in witness['clauses']:
                    self.assertEqual(lines[quote['line']-1][quote['start']:quote['end']], quote['quote'])
        shu = read('corpus/chenshu/017-yuanshu-complete.json')
        self.assertEqual(shu['id'], SHU)
        offers = shu['annotation']['title_proposals']
        self.assertEqual({a['title'] for a in offers}, {'左民尚書', '給事黃門侍郎'})
        for offer in offers:
            self.assertTrue(valid(offer, shu))
            wrong = deepcopy(offer)
            wrong['non_assumption_anchor'] = next(p['non_assumption_anchor'] for p in offers if p is not offer)
            self.assertFalse(valid(wrong, shu))
        holdings = read('corpus/chenshu/017-yuanshu-complete-titles.json')['holdings']
        self.assertFalse({'左民尚書', '給事黃門侍郎', '駙馬都尉', '亭侯'} & {x['title'] for x in holdings})

    def test_three_princesses_and_proposed_grants(self):
        shu = read('corpus/chenshu/017-yuanshu-complete.json')
        p = shu['paragraphs'][2]
        ids = {m['surface']: m['person_id'] for m in p['mentions']}
        self.assertEqual(len({ids['永世公主'], ids['高陵宣公主'], ids['新安穆公主']}), 3)
        roles = {r['start']: r['person_id'] for r in shu['annotation']['person_reference_occurrences']}
        self.assertEqual(roles[p['text'].index('而主已亡') + 1], ids['高陵宣公主'])
        self.assertEqual(roles[p['text'].index('公主所生')], ids['永世公主'])
        relationships = read('corpus/chenshu/017-yuanshu-complete-assertions.json')['assertions']
        parents = {(r['subject_person_id'], r['predicate']): r['object_person_id'] for r in relationships}
        self.assertEqual(parents[ids['岊'], 'mother'], ids['永世公主'])
        self.assertEqual(parents[ids['岊'], 'father'], ids['錢蕆'])
        self.assertEqual(parents[ids['高陵宣公主'], 'father'], ids['晉宣帝'])
        self.assertEqual(parents[ids['新安穆公主'], 'father'], ids['梁(之)[文]帝'])
