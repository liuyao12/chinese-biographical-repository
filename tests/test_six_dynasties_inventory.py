import unittest
import json
from pathlib import Path

from scripts.six_dynasties_inventory import verify
from scripts.person_references import reference_errors
from scripts.family_assemblies import registry_sibling_path_valid


class SixDynastiesInventoryTest(unittest.TestCase):
    def test_full_entries_match_fixed_witness_and_progress(self):
        books, counts = verify()
        self.assertIn('b-nanshi-080', books)
        self.assertIn('b-sanguozhi-046', books)
        self.assertGreaterEqual(counts['item_reviewed'], 2)

    def test_quote_must_cover_this_occurrence_of_the_pronoun(self):
        pid = 'c-example:p001'
        ref = dict(id=pid + ':r0004', paragraph_id=pid, start=4, end=5, surface='我',
                   quote='我問君', referent_role='speaker_self', person_id='甲', note='發言者自稱。')
        chapter = dict(id='c-example', paragraphs=[dict(id=pid, text='我問君，我答之。', mentions=[])],
                       annotation=dict(person_reference_occurrences=[ref]))
        self.assertTrue(reference_errors(chapter, {'甲'}))
        ref['quote'] = '我答之'
        self.assertFalse(reference_errors(chapter, {'甲'}))

    def test_inferred_parent_requires_every_sibling_link(self):
        root = Path(__file__).resolve().parents[1]
        people = json.loads((root / 'registry/persons.json').read_text())['persons']
        chapter = json.loads((root / 'corpus/weishu-weishou/024-cuidaogu.json').read_text())
        last = next(p for p in chapter['paragraphs'] if p['text'].startswith('景業弟景淵'))
        person = next(m['person_id'] for m in last['mentions'] if m['surface'] == '景淵')
        path = next(p['family_path'] for p in people if p['id'] == person)
        assertions = {}
        for source in ('corpus/weishu-weishou/024-cuidaogu-assertions.json', 'corpus/beishi/044-cuidaogu-assertions.json'):
            assertions.update({a['id']: a for a in json.loads((root / source).read_text())['assertions']})
        self.assertTrue(registry_sibling_path_valid(person, path, assertions))
        broken = dict(path, evidence=path['evidence'][1:])
        self.assertFalse(registry_sibling_path_valid(person, broken, assertions))
        broken = dict(path, parent_person_id=person)
        self.assertFalse(registry_sibling_path_valid(person, broken, assertions))
