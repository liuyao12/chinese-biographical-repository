"""Exercise the actual reader exporter: source choices must reach cards intact."""
import json
import tempfile
import unittest
from pathlib import Path
from scripts.table_person_profiles import build

ROOT = Path(__file__).resolve().parents[1]


class PairOrderReaderExportTests(unittest.TestCase):
    def test_actual_source_choices_and_raw_relations_survive_reader_export(self):
        selected = {'aa6_83c_juy_A', 'aa6_83c_juy_B', 'aa6_83c_juy_ABA'}
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            # Read the real catalogs and bundles, but write only into the fixture.
            for folder in ('registry', 'data/historical-tables', 'exports/persons'):
                target = root / folder
                target.parent.mkdir(parents=True, exist_ok=True)
                target.symlink_to(ROOT / folder, target_is_directory=True)
            catalog = root / 'data/corpus'
            catalog.mkdir()
            for path in (ROOT / 'data/corpus').iterdir():
                if path.name != 'profiles':
                    (catalog / path.name).symlink_to(path, target_is_directory=path.is_dir())
            build(root, person_ids=selected)
            for pid in selected:
                bundle = json.loads((ROOT / 'exports/persons' / f'{pid}.json').read_text())
                profile = json.loads((catalog / 'profiles' / f'{pid}.json').read_text())
                self.assertEqual(profile['relations'], bundle['relations'])
                self.assertEqual(profile['preferred_relations'], bundle['preferred_relations'])
                if pid == 'aa6_83c_juy_ABA':
                    self.assertNotIn('relative_birth_order_preferences', profile)
                else:
                    choices = profile['relative_birth_order_preferences']
                    self.assertEqual(choices, bundle['relative_birth_order_preferences'])
                    self.assertEqual(choices[0]['display_note'], '謝據較謝安年長（《宋書》作弟）')
                    self.assertFalse(choices[0]['human_reviewed'])


if __name__ == '__main__':
    unittest.main()
