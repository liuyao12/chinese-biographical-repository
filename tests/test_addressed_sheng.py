import copy
import json
import unittest
from pathlib import Path

from scripts.contextual_relations import addressed_sheng_valid


ROOT = Path(__file__).resolve().parents[1]


class AddressedShengTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        chapter = json.loads((ROOT/'corpus/jinshu/079.json').read_text())
        cls.paragraphs = {p['id']: (chapter['id'], p) for p in chapter['paragraphs']}
        cls.row, = json.loads((ROOT/'corpus/jinshu/079-yangtan-assertions.json').read_text())['assertions']

    def test_source_direction_and_term(self):
        self.assertTrue(addressed_sheng_valid(self.row, self.paragraphs))
        row = copy.deepcopy(self.row)
        evidence, = row['evidence']
        for mapping, left, right in [
            (row, 'subject_person_id', 'object_person_id'),
            (evidence, 'subject_person_mention_id', 'object_person_mention_id')
        ]:
            mapping[left], mapping[right] = mapping[right], mapping[left]
        self.assertFalse(addressed_sheng_valid(row, self.paragraphs))

    def test_reject_unattested_maternal_order(self):
        for key, value in [('source_term', '姊子'), ('lineage', 'maternal'), ('generation_difference', -1)]:
            with self.subTest(key=key):
                row = copy.deepcopy(self.row)
                row['qualifiers'][key] = value
                self.assertFalse(addressed_sheng_valid(row, self.paragraphs))

    def test_reject_later_unrelated_speech(self):
        row = copy.deepcopy(self.row)
        b = row['qualifiers']['kinship_clause_binding']
        p = self.paragraphs[row['evidence'][0]['paragraph_id']][1]
        b['end'] = p['text'].rindex('」') + 1
        b['surface'] = p['text'][b['start']:b['end']]
        self.assertFalse(addressed_sheng_valid(row, self.paragraphs))
