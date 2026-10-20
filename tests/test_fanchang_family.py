# coding: utf-8
import json
import unittest
from pathlib import Path
from scripts.family_assemblies import load_assemblies
from scripts.person_bundle import load_catalog, bundle

ROOT = Path(__file__).resolve().parents[1]


class FanchangFamily(unittest.TestCase):
    def test_father_family_and_former_spouse_share_one_identity(self):
        catalog = load_catalog(ROOT)
        people, _ = catalog
        father = next(p['id'] for p in people.values() if p['label'] == '始興王憺')
        daughter = next(p['id'] for p in people.values() if p['label'] == '繁昌主')
        self.assertTrue(daughter.startswith(father + '_'))
        _, assembled = load_assemblies(ROOT, catalog)
        self.assertEqual(assembled[daughter]['parent_person_id'], father)
        b = bundle(daughter, ROOT, catalog=catalog)
        self.assertTrue(any(r['predicate'] == 'father' and r['object_person_id'] == father for r in b['relations']))
        self.assertTrue(any(r['predicate'] == 'spouse' and r['qualifiers'].get('marriage_termination', {}).get('kind') == 'divorce'
                            for r in b['relations']))
        self.assertFalse(any(r['predicate'] == 'mother' for r in b['relations']))
        father_bundle = bundle(father, ROOT, catalog=catalog)
        father_relation = next(r for r in b['relations'] if r['predicate'] == 'father' and r['object_person_id'] == father)
        self.assertIn(father_relation, father_bundle['relations'])
        marriage = next(r for r in b['relations'] if r['predicate'] == 'spouse')
        husband_id = marriage['object_person_id'] if marriage['subject_person_id'] == daughter else marriage['subject_person_id']
        self.assertIn(marriage, bundle(husband_id, ROOT, catalog=catalog)['relations'])

    def test_old_unpublished_id_has_no_registry_redirect_or_source_reference(self):
        retired = 'nv0_nji_w3b'
        reg = json.loads((ROOT / 'registry/persons.json').read_text())
        self.assertFalse(any(p['id'] == retired or retired in p.get('id_aliases', []) for p in reg['persons']))
        for path in (ROOT / 'corpus').glob('*/*.json'):
            self.assertNotIn(retired, path.read_text(), str(path))
        for folder in ['exports/persons', 'data/corpus/profiles']:
            self.assertFalse((ROOT / folder / (retired + '.json')).exists())


if __name__ == '__main__':
    unittest.main()
