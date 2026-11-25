import copy
import json
import unittest
from pathlib import Path

from scripts.uncle_parentage import explicit_maternal_uncle_valid


class CoordinatedMaternalUnclesTest(unittest.TestCase):
    def test_each_uncle_needs_the_same_ordered_source_group(self):
        root = Path(__file__).resolve().parents[1] / 'corpus' / 'jinshu'
        chapter = json.loads((root / '005-jin05.json').read_text())
        record = json.loads((root / '005-jin05-assertions.json').read_text())
        paragraphs = {p['id']: (chapter['id'], p) for p in chapter['paragraphs']}
        self.assertEqual(len(record['assertions']), 2)
        for assertion in record['assertions']:
            self.assertTrue(explicit_maternal_uncle_valid(assertion, paragraphs))

            reversed_group = copy.deepcopy(assertion)
            reversed_group['qualifiers']['coordinated_uncle_mention_ids'].reverse()
            self.assertFalse(explicit_maternal_uncle_valid(reversed_group, paragraphs))

            missing_anchor = copy.deepcopy(assertion)
            missing_anchor['qualifiers']['coordinated_uncle_mention_ids'].pop()
            self.assertFalse(explicit_maternal_uncle_valid(missing_anchor, paragraphs))

    def test_shared_maternal_uncle_needs_both_nephew_anchors(self):
        root = Path(__file__).resolve().parents[1] / 'corpus' / 'jinshu'
        chapter = json.loads((root / '062-liuyu.json').read_text())
        record = json.loads((root / '062-liuyu-assertions.json').read_text())
        paragraphs = {p['id']: (chapter['id'], p) for p in chapter['paragraphs']}
        assertions = [entry for entry in record['assertions']
                      if entry['predicate'] == 'maternal_uncle']
        self.assertEqual(len(assertions), 2)
        for assertion in assertions:
            with self.subTest(person=assertion['subject_person_id']):
                self.assertTrue(explicit_maternal_uncle_valid(assertion, paragraphs))

                reversed_group = copy.deepcopy(assertion)
                reversed_group['qualifiers']['coordinated_nephew_mention_ids'].reverse()
                self.assertFalse(explicit_maternal_uncle_valid(reversed_group, paragraphs))

                short_quote = copy.deepcopy(assertion)
                short_quote['evidence'][0]['quote'] = assertion['qualifiers']['source_term']
                self.assertFalse(explicit_maternal_uncle_valid(short_quote, paragraphs))
