from copy import deepcopy
import json
from pathlib import Path
import unittest

from scripts.song063_wanghua_reading import DIGITAL, PRINT, HUA, errors, issued_references
from scripts.six_dynasties_inventory import chapter_passage

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads((ROOT / path).read_text())


class WangHuaWitness(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.digital = read('corpus/songshu/063-wanghua-tanshou.json')
        cls.printed = read('corpus/songshu/063-wanghua-wyd.json')

    def test_juvenile_age_and_fathers_posthumous_name_are_witness_specific(self):
        for chapter, age, title in [(self.digital, '十三', '定侯'), (self.printed, '十二', '宣侯')]:
            with self.subTest(chapter=chapter['id']):
                self.assertEqual(errors(chapter, ROOT), [])
                texts = [p['text'] for p in chapter['paragraphs']]
                self.assertIn('華時年' + age, texts[0])
                self.assertIn('宣侯', texts[6])
                self.assertTrue(texts[7].startswith('子' + title + '嗣'))
                wrong = deepcopy(chapter)
                wrong['annotation']['age_assertions'][0]['birth_year'] = 385
                self.assertTrue(errors(wrong, ROOT))
        kin = read('corpus/songshu/063-wanghua-wyd-assertions.json')['assertions']
        son = next(a for a in kin if a['predicate'] == 'father' and a['object_person_id'] == HUA)
        self.assertEqual(son['source_term_anchor']['surface'], '子宣侯嗣')
        self.assertEqual(son['qualifiers']['source_term'], '子宣侯嗣')

    def test_released_pronoun_ids_resolve_in_their_original_speech(self):
        roles = [r for p in self.digital['paragraphs'] for r in issued_references(self.digital, p)]
        self.assertEqual(len(roles), 7)
        self.assertEqual({(r['surface'], r['person_id']) for r in roles if r['referent_role'] == 'speaker_self'},
                         {('我', '58f_d92_1b5')})
        wrong = deepcopy(self.digital)
        ref = next(r for r in wrong['annotation']['person_reference_occurrences'] if r['surface'] == '奴子')
        ref['person_id'] = '58f_d92_1b5'
        self.assertTrue(errors(wrong, ROOT))

    def test_kong_ningzi_resumes_after_wang_huas_recitation(self):
        inv = read('data/corpus/six-dynasties-biographies.json')
        unit = next(x for x in inv['biographies'] if x['title'] == '孔甯子' and x['chapter_id'] == DIGITAL)
        _, pieces = chapter_passage(unit, self.digital)
        self.assertIn('冒昧陳愚', pieces[0])
        self.assertIn('弒君亭', pieces[1])
        self.assertEqual(pieces[2], '元嘉二年，甯子病卒。')
        self.assertNotIn('登樓賦', ''.join(pieces))
        proof = read('source-evidence/song063-wanghua/reading.json')
        self.assertEqual({r['reading_status'] for r in proof['parallel_readings'] if r['surface'] == '免徒之守'},
                         {'unresolved_analogy'})
        print_survey = next(s for s in inv['volume_surveys'] if s['book_id'] == 'b-songshu-063')
        self.assertEqual(sum(w['chapter_id'] == PRINT for w in print_survey['text_witness_units']), 1)

    def test_two_officers_have_distinct_occurrences_of_sima(self):
        for path, chap in [('063-wanghua-tanshou', self.digital), ('063-wanghua-wyd', self.printed)]:
            p = chap['paragraphs'][2]
            holds = read('corpus/songshu/' + path + '-titles.json')['holdings']
            found = {h['person_id']: h['attestations'][0]['start'] for h in holds if h['title'] == '司馬'
                     and h['attestations'][0]['paragraph_id'] == p['id']}
            self.assertEqual(found[HUA], p['text'].index('華代為司馬') + 3)
            self.assertEqual(found['d50_8f5_wul_AAAC'], p['text'].index('司馬張邵'))
