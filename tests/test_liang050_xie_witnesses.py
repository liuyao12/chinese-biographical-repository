import json
import unittest
from pathlib import Path

from scripts.liang050_xie_witnesses import errors
from scripts.unassumed_appointments import unassumed_appointment_valid
from scripts.non_parental_family import non_parental_relation_valid

ROOT = Path(__file__).resolve().parents[1]


def read(stem):
    return json.loads((ROOT / 'corpus/liangshu' / (stem + '.json')).read_text())


class LiangXieWitnessTests(unittest.TestCase):
    def test_ancestor_and_emperor(self):
        for suffix in ('', '-wyd'):
            chapter = read('050-xiezheng' + suffix)
            self.assertEqual(errors(chapter, ROOT), [])
            ancestor = next(r for r in chapter['annotation']['person_reference_occurrences'] if r['quote'] == '高祖景仁')
            ancestor['person_id'] = 'fo7_f8v_rmf'
            self.assertTrue(errors(chapter, ROOT))

    def test_refusal_by_father(self):
        for suffix in ('', '-wyd'):
            chapter = read('050-xiezheng' + suffix)
            proposal = chapter['annotation']['title_proposals'][0]
            self.assertTrue(unassumed_appointment_valid(proposal, chapter))
            other = chapter['paragraphs'][0]['mentions'][0]
            proposal.update(person_id=other['person_id'], person_mention_id=other['id'])
            self.assertFalse(unassumed_appointment_valid(proposal, chapter))

    def test_rearing_roles(self):
        for suffix in ('', '-wyd'):
            stem = '050-xiejiqing-family-intro' + suffix
            chapter = read(stem)
            paragraphs = {p['id']: (chapter['id'], p) for p in chapter['paragraphs']}
            relation = next(row for row in read(stem + '-assertions')['assertions'] if row['predicate'] == 'raised_by')
            self.assertTrue(non_parental_relation_valid(relation, paragraphs))
            relation['object_person_id'] = relation['subject_person_id']
            self.assertFalse(non_parental_relation_valid(relation, paragraphs))

    def test_lacuna_marks(self):
        chapter = read('050-xiejiqing-family-intro-wyd')
        self.assertEqual(errors(chapter, ROOT), [])
        paragraph = chapter['paragraphs'][3]
        paragraph['text'] = paragraph['text'].replace('栖缺匪商官缺', '棲息旣匪高官')
        self.assertTrue(errors(chapter, ROOT))
