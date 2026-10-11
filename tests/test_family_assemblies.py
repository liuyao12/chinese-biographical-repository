import copy
import json
import tempfile
import unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from family_assemblies import load_assemblies
from person_bundle import load_catalog, ROOT


class FamilyAssembliesTests(unittest.TestCase):
    def test_liu_lineage_keeps_source_candidates_and_shared_root(self):
        source, rows = load_assemblies(ROOT, load_catalog(ROOT))
        bang = source['yqp_nlb_p1p_A']
        che = source['yqp_nlb_p1p_ACAA']
        self.assertEqual(bang['root_person_id'], che['root_person_id'])
        self.assertEqual(bang['parent_person_id'], 'yqp_nlb_p1p')
        self.assertEqual(che['parent_person_id'], 'yqp_nlb_p1p_ACA')
        self.assertEqual(source['byp_ks5_71a_A']['person_id'], 'yqp_nlb_p1p_AB')
        self.assertGreater(len(source), len(rows))
        self.assertTrue(all(row['person_id'].startswith('yqp_nlb_p1p') for row in rows.values()))
        jiao = source['n7i_i5n_lay']
        self.assertEqual(jiao['parent_person_id'], 'yqp_nlb_p1p')
        self.assertIsNone(jiao['source_assertion_id'])
        self.assertEqual(jiao['parent_connection']['type'], 'shared_father_through_sibling')
        self.assertIn('同父少弟', jiao['parent_connection']['references'][0]['quote'])
        wu = source['dlg_vnw_1bi_A']
        zhong = source['p7f_7ie_ydf']
        self.assertEqual(wu['parent_person_id'], zhong['person_id'])
        self.assertEqual(zhong['parent_person_id'], 'yqp_nlb_p1p')
        self.assertIn('dlg_vnw_1bi', zhong['source_person_ids'])
        self.assertNotIn('1g3_02y_oor', source)  # 太公望不能因稱呼加入。

    def test_rejects_unsupported_candidate_and_wrong_father(self):
        original = json.loads((ROOT / 'registry/family-assemblies.json').read_text())
        catalog = load_catalog(ROOT)
        for alteration in ('candidate', 'father'):
            data = copy.deepcopy(original)
            child = data['assemblies'][0]['members'][1]
            if alteration == 'candidate':
                child['source_person_ids'].append('1g3_02y_oor')
            else:
                child['parent_person_id'] = child['person_id']
            with tempfile.TemporaryDirectory() as folder:
                root = Path(folder)
                (root / 'registry').mkdir()
                (root / 'registry/family-assemblies.json').write_text(json.dumps(data))
                with self.assertRaises(ValueError):
                    load_assemblies(root, catalog)
