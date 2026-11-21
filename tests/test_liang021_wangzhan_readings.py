import copy
import json
import unittest
from pathlib import Path

from scripts.liang021_print_columns import errors
from scripts.liang021_wangzhan_kin import senior_valid, wife_valid


ROOT = Path(__file__).resolve().parents[1]


def corpus(stem):
    return json.loads((ROOT / 'corpus/liangshu' / (stem + '.json')).read_text())


class WangZhanReadings(unittest.TestCase):
    def test_baoyin_family_profile_uses_the_source_person_name(self):
        directory = ROOT / 'data/corpus/profiles'
        family = json.loads((directory / 'w4m_9tw_147_D.json').read_text())
        source = json.loads((directory / 'bni_9ky_npc.json').read_text())
        self.assertEqual(family['label'], source['label'])
        self.assertIn('蕭寶夤', family['label'])
        self.assertEqual({row['source_term'] for row in family['life_events']}, {'賜死', '誅'})

    def test_variants_belong_to_the_biography_subject(self):
        for stem in ('021-wangzhan', '021-wangzhi'):
            chapter = corpus(stem)
            subject = chapter['paragraphs'][0]['mentions'][0]['person_id']
            cases = chapter['annotation']['source_reading_cases']
            self.assertTrue(cases)
            self.assertTrue(all(row['person_id'] == subject for row in cases))

    def test_complete_print_cannot_relabel_column_or_skip_a_glyph(self):
        for stem in ('021-wangzhan-wyd', '021-wangzhi-wyd'):
            chapter = corpus(stem)
            self.assertEqual(errors(chapter, ROOT), [])
            for key, value in [('column_from_right', 1), ('start', 1), ('text', '')]:
                changed = copy.deepcopy(chapter)
                changed['paragraphs'][0]['source_position']['column_projection'][0][key] = value
                self.assertTrue(errors(changed, ROOT))

    def test_congfu_and_unnamed_wife_bind_the_correct_people(self):
        chapter = corpus('021-wangzhan')
        paragraphs = {p['id']: (chapter['id'], p) for p in chapter['paragraphs']}
        assertions = corpus('021-wangzhan-assertions')['assertions']
        senior = next(a for a in assertions if a['predicate'] == 'agnatic_senior_kin')
        wife = next(a for a in assertions if a['predicate'] == 'spouse')
        self.assertTrue(senior_valid(senior, paragraphs))
        self.assertTrue(wife_valid(wife, wife['evidence'][0], chapter))
        self.assertFalse(senior_valid(dict(senior, predicate='father'), paragraphs))
        self.assertFalse(wife_valid(dict(wife, object_person_id=senior['object_person_id']),
                                    wife['evidence'][0], chapter))
