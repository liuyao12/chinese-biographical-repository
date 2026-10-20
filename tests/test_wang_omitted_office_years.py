# coding: utf-8
import json
import unittest
from pathlib import Path
from scripts.person_bundle import bundle, load_catalog
from scripts.validate_corpus import normalized_date_errors

ROOT = Path(__file__).resolve().parents[1]


class WangOmittedOfficeYears(unittest.TestCase):
    def setUp(self):
        self.song = json.loads((ROOT / 'corpus/songshu/066-titles.json').read_text())['holdings']
        self.qi = json.loads((ROOT / 'corpus/nanqishu/032-titles.json').read_text())['holdings']

    def test_song_sixth_year_and_qi_fourth_year_keep_era_evidence(self):
        for holdings, prefix, titles, year in [
                (self.song, 'th-wang-full-s-18-', ['侍中', '特進', '左光祿大夫'], 429),
                (self.qi, 'th-wang-full-q-87-', ['中書令', '右光祿大夫', '本州大中正'], 482)]:
            rows = [h for h in holdings if h['id'].startswith(prefix) and h['title'] in titles]
            self.assertEqual(len(rows), 3)
            for h in rows:
                date = h['effective_period']['start']['normalized_date']
                self.assertEqual(date['year'], year)
                self.assertEqual(normalized_date_errors(date), [])
        later = next(h for h in self.qi if h['id'].startswith('th-wang-full-q-87-') and h['title'] == '左僕射')
        self.assertNotIn('normalized_date', later['effective_period']['start'])

    def test_third_year_precedes_jianyuan_and_is_shengming479(self):
        rows = [h for h in self.qi if h['id'].startswith('th-wang-full-q-83-') and h['mode'] == 'grant']
        self.assertEqual(len(rows), 4)
        for h in rows:
            date = h['effective_period']['start']['normalized_date']
            self.assertEqual(date['year'], 479)
            self.assertEqual(date['regnal_year_mapping']['era_name'], '昇明')
            self.assertEqual(date['source_expression'], '三年')

    def test_can_zan_case_is_available_from_both_unmerged_people(self):
        catalog = load_catalog(ROOT)
        people = catalog[0]
        can = next(p['id'] for p in people.values() if p['label'] == '王粲之（延之出繼伯父）')
        zan = next(p['id'] for p in people.values() if p['label'] == '王瓚之')
        self.assertNotEqual(can, zan)
        for pid in [can, zan]:
            b = bundle(pid, ROOT, catalog=catalog)
            case = next(c for c in b['unresolved_identity_cases'] if c['id'] == 'u-nanqishu032-can-zan')
            self.assertEqual(set(case['candidate_person_ids']), {can, zan})
            self.assertEqual(case['status'], 'unresolved')


if __name__ == '__main__':
    unittest.main()
