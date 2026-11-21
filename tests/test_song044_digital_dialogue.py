from copy import deepcopy
import json
from pathlib import Path
import unittest

from scripts.nanshi019_dialogue import age_anchor

ROOT = Path(__file__).resolve().parents[1]


class SongDialogue(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = json.loads((ROOT / 'corpus/songshu/044-xiehui-digital.json').read_text())
        cls.answer, cls.recollection = cls.chapter['annotation']['age_assertions'][:2]

    def test_receives_both_reports_with_different_subjects(self):
        for record in [self.answer, self.recollection]:
            self.assertEqual(age_anchor(record, self.chapter)['person_id'], record['person_id'])
        self.assertNotEqual(self.answer['person_id'], self.recollection['person_id'])

    def test_asker_cannot_supply_answer(self):
        a = deepcopy(self.answer)
        a['reported_dialogue']['speaker_mention_id'] = a['reported_dialogue']['asker_mention_id']
        self.assertIsNone(age_anchor(a, self.chapter))

    def test_recollection_qualifies_an_exact_reference(self):
        a = deepcopy(self.recollection)
        a['evidence'][0]['person_reference_id'] = self.answer['reported_dialogue']['speaker_mention_id']
        self.assertIsNone(age_anchor(a, self.chapter))
        a = deepcopy(self.recollection)
        a['value'] = 29
        self.assertIsNone(age_anchor(a, self.chapter))

    def test_cannot_exchange_witness_or_clause(self):
        a = deepcopy(self.answer)
        a['reported_dialogue']['clause'] = '澹問晦年'
        self.assertIsNone(age_anchor(a, self.chapter))
        ch = deepcopy(self.chapter)
        ch['source']['revision_id'] = 1531762
        self.assertIsNone(age_anchor(self.answer, ch))
        ch = deepcopy(self.chapter)
        ch['source']['raw_file_sha256'] = '0' * 64
        self.assertIsNone(age_anchor(self.answer, ch))
