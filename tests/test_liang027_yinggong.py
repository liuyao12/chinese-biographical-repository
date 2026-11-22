from copy import deepcopy
import json
from pathlib import Path
import unittest

from scripts.directed_uncle_roles import paternal_uncle_direction_valid


class LuYinggongKinship(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        directory = Path(__file__).resolve().parents[1] / 'corpus' / 'liangshu'
        chapter = json.loads((directory/'027-luxiang-complete.json').read_text())
        assertions = json.loads((directory/'027-luxiang-complete-assertions.json').read_text())
        cls.relation, = (r for r in assertions['assertions'] if r['predicate'] == 'paternal_uncle')
        cls.paragraphs = {p['id']:(chapter['id'],p) for p in chapter['paragraphs']}

    def test_dispatch_identifies_the_uncle(self):
        self.assertTrue(paternal_uncle_direction_valid(self.relation,self.paragraphs))

    def test_both_named_ends_reversed(self):
        row = deepcopy(self.relation)
        e, = row['evidence']
        row['subject_person_id'], row['object_person_id'] = row['object_person_id'], row['subject_person_id']
        e['subject_person_mention_id'], e['object_person_mention_id'] = e['object_person_mention_id'], e['subject_person_mention_id']
        self.assertFalse(paternal_uncle_direction_valid(row,self.paragraphs))

    def test_another_instance_of_xiangs_name_cannot_prove_the_dispatch(self):
        row = deepcopy(self.relation)
        e, = row['evidence']
        p = self.paragraphs[e['paragraph_id']][1]
        unrelated = next(m for m in p['mentions'] if m['surface']=='襄' and m['id']!=e['object_person_mention_id'])
        e['object_person_mention_id']=unrelated['id']
        self.assertFalse(paternal_uncle_direction_valid(row,self.paragraphs))
