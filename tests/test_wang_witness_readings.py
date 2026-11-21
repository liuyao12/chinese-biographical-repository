"""王氏數位、殿本及異書的紀年與親屬必須各回到原證。"""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import unittest

from scripts import wang_family_women_sources, ws_song071_wang, wyd_song071_wang

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads((ROOT / path).read_text())


class WangWitnessReadings(unittest.TestCase):
    def test_wangzhi_appointment_and_separate_death_year(self):
        for chapter in ('022-wangzhi', '022-wangzhi-digital'):
            book = read(f'corpus/nanshi/{chapter}.json')
            case, = [c for c in book['annotation']['source_reading_cases']
                     if c.get('reported_death_year') == 513]
            self.assertEqual(case['appointment_year'], 510)
            self.assertEqual(case['reported_death_age'], 54)
            self.assertIsNone(case['explicit_death_year_in_local_witness'])
            paragraph = next(p for p in book['paragraphs'] if p['id'] == case['paragraph_id'])
            self.assertIn(case['source_quote'], paragraph['text'])
            witness = case['parallel_anchor']
            raw = (ROOT / witness['parallel_source']).read_bytes()
            line = raw.decode().splitlines()[witness['first_line'] - 1]
            self.assertEqual(hashlib.sha256(raw).hexdigest(), witness['sha256'])
            self.assertEqual(line[witness['start_codepoint']:witness['end_codepoint']], case['reading'])
            self.assertIn('十二年，卒，時年五十四', case['reading'])

    def test_sengchuo_and_qigui_relationships_keep_both_endpoints(self):
        cases = (
            ('songshu/071-wangsengchuo-ws', ws_song071_wang),
            ('songshu/071-wangsengchuo-wyd', wyd_song071_wang),
            ('songshu/041-yuanqigui', wang_family_women_sources),
            ('nanshi/011-yuanqigui', wang_family_women_sources),
        )
        for stem, validator in cases:
            chapter = read(f'corpus/{stem}.json')
            self.assertEqual(validator.errors(chapter, ROOT), [])
            assertions = read(f'corpus/{stem}-assertions.json')['assertions']
            self.assertTrue(assertions)
            for assertion in assertions:
                with self.subTest(assertion=assertion['id']):
                    self.assertTrue(validator.kin_valid(assertion, chapter, ROOT))
                    wrong = deepcopy(assertion)
                    wrong['object_person_id'], wrong['subject_person_id'] = (
                        assertion['subject_person_id'], assertion['object_person_id'])
                    self.assertFalse(validator.kin_valid(wrong, chapter, ROOT))

    def test_donghun_receipt_binds_the_biography_and_annals(self):
        review = read('source-evidence/nanshi022-donghun/review.json')
        ids = {r['chapter_id'] for r in review['native_marked_witnesses']}
        self.assertEqual(len(ids), 4)
        for row in review['primary_witness']:
            raw = (ROOT / row['raw_path']).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), row['sha256'])
            line = raw.decode().splitlines()[row['line'] - 1]
            self.assertEqual(line[row['start_codepoint']:row['end_codepoint']], row['quote'])
        receipt = read(review['retirement_receipt'])
        retired, = receipt['retired_person_ids']
        registry = {p['id']: p for p in read('registry/persons.json')['persons']}
        self.assertNotIn(retired, registry)
        person = registry[review['person_id']]
        self.assertEqual(person['label'], '蕭寶卷')
        self.assertTrue({r['mention_id'] for r in review['native_marked_witnesses']}
                        <= {r['mention_id'] for r in person['evidence']})
