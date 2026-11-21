from copy import deepcopy
import hashlib
import json
from pathlib import Path
import unittest

from scripts.liang021_print_columns import errors as print_errors
from scripts.qi020_baoming import parent_grant_valid


ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads((ROOT / path).read_bytes())


class BaomingWitnessTests(unittest.TestCase):
    def test_each_parent_has_the_named_grant(self):
        for edition in ('nanqishu/020-wangbaoming', 'nanqishu/020-wangbaoming-wyd',
                        'nanshi/011-wangbaoming', 'nanshi/011-wangbaoming-izumo'):
            with self.subTest(edition=edition):
                stem = 'corpus/' + edition
                c = read(stem + '.json')
                chapters = {p['id']: (c['id'], p) for p in c['paragraphs']}
                mentions = {m['id']: (c['id'], p['id'], m) for p in c['paragraphs'] for m in p['mentions']}
                gifts = [h for h in read(stem + '-titles.json')['holdings'] if h['mode'] == 'posthumous_grant']
                self.assertEqual({h['title'] for h in gifts}, {'金紫光祿大夫', '豐安縣君'})
                for h in gifts:
                    self.assertTrue(parent_grant_valid(h, chapters, mentions))
                    wrong = deepcopy(h)
                    wrong['person_id'] = 'm9u_v4i_tk5'
                    self.assertFalse(parent_grant_valid(wrong, chapters, mentions))
                    wrong = deepcopy(h)
                    wrong['attestations'][0]['start'] += 1
                    self.assertFalse(parent_grant_valid(wrong, chapters, mentions))
                if edition.endswith(('-wyd', '-izumo')):
                    self.assertEqual(print_errors(c, ROOT), [])
                    wrong = deepcopy(c)
                    wrong['paragraphs'][0]['source_position']['column_projection'][0]['column_from_right'] += 1
                    self.assertTrue(print_errors(wrong, ROOT))
                ages = c['annotation'].get('age_assertions', [])
                self.assertEqual([a['value'] for a in ages], [58] if 'nanqishu' in edition else [])

    def test_print_edition_and_three_excerpt_witnesses(self):
        for path, page, pdf_sha, capture in [
            ('qi020-wangbaoming-wyd/wuying-reading', 5,
             '7849bb904bfa78cf58dd22dcc60fe98cdd06e8b32c4933f684d4e8b150a16bc7',
             'bcbc0bc3b8234c292bb666d73e8b6efbea7faed3bd577aebe9d2ae93facd733a'),
            ('nan011-wangbaoming-izumo/izumo-reading', 21,
             '020c8ce42595fcca7c41ebf3960599287aa83cffeb6dfb846cc0156a2b8793ef',
             'c48b1e2779ec1955c85d052c4659f8258487d8349658ecfd85558d26e87c4840'),
        ]:
            ledger = read('source-evidence/' + path + '.json')
            self.assertEqual(ledger['pdf_sha256'], pdf_sha)
            self.assertEqual(ledger['images'], [dict(pdf_page=page, capture_sha256=capture,
                             source_url=f"{ledger['pdf_url']}#page={page}",
                             catalogue_url=ledger['catalog_permalink'])])
        nan = read('corpus/nanshi/011-wangbaoming-izumo.json')['paragraphs'][0]['text']
        self.assertIn('太子宮人製新麗衣裳', nan)
        self.assertIn('牀帷陳故古舊釵鑷十餘枚', nan)
        for volume, quote in [(143, '爲南陽王妃'), (149, '而後床帳陳古，釵鈐十餘枚'),
                              (718, '而后床惟陳故古舊釵鑷數枚')]:
            c = read(f'corpus/taipingyulan/{volume}-wangbaoming.json')
            self.assertIn(quote, c['paragraphs'][-1]['text'])
            data = (ROOT / c['source']['raw_path']).read_bytes()
            self.assertEqual(hashlib.sha256(data).hexdigest(), c['source']['raw_file_sha256'])
            raw = data.decode()
            for p in c['paragraphs']:
                self.assertEqual(''.join(raw[x] for x in p['source_position']['raw_character_offsets']), p['text'])
            if volume == 149:
                note, = c['annotation']['source_glosses']
                self.assertEqual(raw[note['raw_start']:note['raw_end']], '{{*|小釵也。}}')
                self.assertNotIn('小釵也', c['paragraphs'][-1]['text'])

    def test_two_wangs_and_the_dated_death(self):
        for edition in ['liangshu/002', 'nanshi/006']:
            stem = 'corpus/' + edition + '-wangbaoming-liang-annal'
            c = read(stem + '.json')
            events = [e for e in c['annotation']['narrative_readings'] if e['event_type'] == 'demotion']
            self.assertEqual([e['person_ids'][0] for e in events], ['m9u_v4i_tk5', '7r6_k52_qji_ABAAAAEAA*A'])
            self.assertEqual([p['text'] for p in c['paragraphs'][1:]], [
                '十一年春正月壬辰', '冬十一月乙未', '癸丑，齊宣德太妃王氏薨。'])
            death, = read(stem + '-life-events.json')['events']
            self.assertEqual((death['person_id'], death['date_expression']), ('m9u_v4i_tk5', '癸丑'))
        a, = [a for a in read('corpus/nanshi/044-wangbaoming-maternity-assertions.json')['assertions']
              if a['predicate'] == 'mother']
        self.assertEqual((a['subject_person_id'], a['object_person_id']), ('iop_ybd_afm', 'm9u_v4i_tk5'))


if __name__ == '__main__':
    unittest.main()
