# coding: utf-8
import json
import tempfile
import unittest
from pathlib import Path

from scripts.family_assemblies import load_assemblies


class MaternalAncestorPaths(unittest.TestCase):
    def fixture(self, lineage):
        root, child = 'abc_def_123', 'abc_def_123_*A'
        def member(pid):
            return dict(person_id=pid, source_person_ids=[pid],
                        representative_source_person_id=pid,
                        identity_equivalence_decision_ids=[], parent_person_id=None,
                        source_assertion_id=None)
        ancestor = member(root)
        descendant = dict(member(child), ancestor_person_id=root,
                          source_assertion_id='synthetic-grandfather', connection='grandfather',
                          generation_distance=2, intermediate_person_ids=[None],
                          interpretation_note='Synthetic missing father remains unknown.')
        assembly = dict(id='synthetic-family', root_person_id=root,
                        status='contextual_provisional', human_reviewed=False,
                        members=[ancestor, descendant])
        assertion = dict(id='synthetic-grandfather', predicate='grandfather',
                         subject_person_id=child, object_person_id=root,
                         qualifiers={'lineage': lineage}, evidence=[])
        catalog = ({root: {}, child: {}}, [dict(record_type='person_assertion_set', assertions=[assertion])])
        return assembly, catalog

    def load(self, lineage):
        assembly, catalog = self.fixture(lineage)
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'registry').mkdir()
            (root / 'registry/family-assemblies.json').write_text(json.dumps({'assemblies': [assembly]}))
            return load_assemblies(root, catalog)

    def test_explicit_paternal_grandfather_keeps_the_missing_generation(self):
        _, people = self.load('paternal')
        self.assertEqual(people['abc_def_123_*A']['ancestor_person_id'], 'abc_def_123')

    def test_maternal_grandfather_cannot_supply_a_paternal_family_id_path(self):
        with self.assertRaisesRegex(ValueError, '缺代組裝祖孫端點與來源不符'):
            self.load('maternal')
