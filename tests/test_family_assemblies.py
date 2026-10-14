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
    def test_single_sibling_connection_rejects_explicit_different_father(self):
        data = json.loads((ROOT / 'registry/family-assemblies.json').read_text())
        member = next(m for f in data['assemblies'] for m in f['members']
                      if m.get('parent_connection', {}).get('type') == 'shared_father_through_sibling')
        assertion_id = member['parent_connection']['sibling_assertion_id']
        catalog = copy.deepcopy(load_catalog(ROOT))
        assertion = next(a for r in catalog[1] if r.get('record_type') == 'person_assertion_set'
                         for a in r['assertions'] if a['id'] == assertion_id)
        assertion['qualifiers']['shared_father'] = False
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'registry').mkdir()
            (root / 'registry/family-assemblies.json').write_text(json.dumps(data))
            with self.assertRaisesRegex(ValueError, '同父兄弟組裝缺少有效兄弟及父親證據'):
                load_assemblies(root, catalog)

    def test_sibling_chain_keeps_inference_separate_from_direct_father(self):
        source, rows = load_assemblies(ROOT, load_catalog(ROOT))
        king = source['wjt_htu_081_AABC']
        daughter = source['wjt_htu_081_AABCA']
        self.assertEqual(king['parent_person_id'], 'wjt_htu_081_AAB')
        self.assertIsNone(king['source_assertion_id'])
        self.assertEqual(king['parent_connection']['sibling_assertion_ids'],
                         ['a-shiji110-024', 'a-shiji110-022'])
        self.assertEqual(daughter['parent_person_id'], king['person_id'])
        self.assertEqual(daughter['source_assertion_id'], 'a-shiji110-025')

    def test_sibling_chain_rejects_broken_steps_and_explicit_different_father(self):
        original = json.loads((ROOT / 'registry/family-assemblies.json').read_text())
        for alteration in ('missing_step', 'reverse', 'cycle', 'wrong_father', 'different_father'):
            with self.subTest(alteration=alteration):
                data = copy.deepcopy(original)
                catalog = copy.deepcopy(load_catalog(ROOT))
                family = next(f for f in data['assemblies'] if f['id'] == 'family-touman-shiji110')
                member = next(m for m in family['members'] if m['representative_source_person_id'] == 'wjt_htu_081_AABC')
                connection = member['parent_connection']
                if alteration == 'missing_step':
                    connection['sibling_assertion_ids'].pop()
                elif alteration == 'reverse':
                    connection['sibling_assertion_ids'].reverse()
                elif alteration == 'cycle':
                    connection['sibling_person_ids'][0] = member['person_id']
                elif alteration == 'wrong_father':
                    connection['sibling_father_assertion_id'] = 'a-shiji110-020'
                else:
                    record = next(r for r in catalog[1] if r.get('record_type') == 'person_assertion_set'
                                  and any(a['id'] == 'a-shiji110-024' for a in r['assertions']))
                    next(a for a in record['assertions'] if a['id'] == 'a-shiji110-024')['qualifiers']['shared_father'] = False
                with tempfile.TemporaryDirectory() as folder:
                    root = Path(folder)
                    (root / 'registry').mkdir()
                    (root / 'registry/family-assemblies.json').write_text(json.dumps(data))
                    with self.assertRaisesRegex(ValueError, '同父兄弟鏈組裝缺少有效逐步證據'):
                        load_assemblies(root, catalog)

    def test_han_changru_royal_candidates_join_existing_paternal_nodes(self):
        source, rows = load_assemblies(ROOT, load_catalog(ROOT))
        pairs = [('yqp_nlb_p1p', 'yqp_nlb_p1p'), ('yqp_nlb_p1p_A', 'yqp_nlb_p1p_A'),
                 ('yqp_nlb_p1p_ACA', 'yqp_nlb_p1p_ACA'), ('yqp_nlb_p1p_ACAA', 'yqp_nlb_p1p_ACAA'),
                 ('yqp_nlb_p1p_ACG', 'yqp_nlb_p1p_ACG'), ('yqp_nlb_p1p_ACAH', 'yqp_nlb_p1p_ACAH'),
                 ('yqp_nlb_p1p_AC', 'yqp_nlb_p1p_AC'), ('yqp_nlb_p1p_ACGA', 'yqp_nlb_p1p_ACGA')]
        for received, earlier in pairs:
            with self.subTest(received=received):
                self.assertEqual(source[received]['person_id'], source[earlier]['person_id'])
                self.assertEqual(source[received]['root_person_id'], 'yqp_nlb_p1p')
        chapter = json.loads((ROOT / 'corpus/shiji/108.json').read_text())
        father = next(m for p in chapter['paragraphs'] for m in p['mentions'] if m['person_id'] == 'yqp_nlb_p1p_AC')
        self.assertEqual(father['surface'], '父')
    def test_liu_lineage_keeps_source_candidates_and_shared_root(self):
        source, rows = load_assemblies(ROOT, load_catalog(ROOT))
        bang = source['yqp_nlb_p1p_A']
        che = source['yqp_nlb_p1p_ACAA']
        self.assertEqual(bang['root_person_id'], che['root_person_id'])
        self.assertEqual(bang['parent_person_id'], 'yqp_nlb_p1p')
        self.assertEqual(che['parent_person_id'], 'yqp_nlb_p1p_ACA')
        self.assertEqual(source['yqp_nlb_p1p_AB']['person_id'], 'yqp_nlb_p1p_AB')
        self.assertEqual(len(source), len(rows))
        self.assertTrue(all(row['person_id'].startswith(row['root_person_id']) for row in rows.values()))
        jiao = source['yqp_nlb_p1p_D']
        self.assertEqual(jiao['parent_person_id'], 'yqp_nlb_p1p')
        self.assertIsNone(jiao['source_assertion_id'])
        self.assertEqual(jiao['parent_connection']['type'], 'shared_father_through_sibling')
        self.assertIn('同父少弟', jiao['parent_connection']['references'][0]['quote'])
        wu = source['yqp_nlb_p1p_CA']
        zhong = source['yqp_nlb_p1p_C']
        self.assertEqual(wu['parent_person_id'], zhong['person_id'])
        self.assertEqual(zhong['parent_person_id'], 'yqp_nlb_p1p')
        self.assertIn('yqp_nlb_p1p_C', zhong['source_person_ids'])
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

    def test_grandson_joins_root_without_fabricating_a_father(self):
        source, rows = load_assemblies(ROOT, load_catalog(ROOT))
        an = source['yqp_nlb_p1p_A*A']
        self.assertEqual(an['person_id'], 'yqp_nlb_p1p_A*A')
        self.assertEqual(an['root_person_id'], source['yqp_nlb_p1p_ACAA']['root_person_id'])
        self.assertEqual(an['ancestor_person_id'], source['yqp_nlb_p1p_A']['person_id'])
        self.assertIsNone(an['parent_person_id'])
        self.assertEqual(an['intermediate_person_ids'], [None])
        self.assertEqual(an['generation_distance'], 2)
        self.assertNotIn('yqp_nlb_p1p_A*', rows)
        self.assertEqual(source['yqp_nlb_p1p_ACG']['person_id'], 'yqp_nlb_p1p_ACG')

    def test_missing_generation_rejects_wrong_distance_or_ancestor(self):
        original = json.loads((ROOT / 'registry/family-assemblies.json').read_text())
        catalog = load_catalog(ROOT)
        for alteration in ('distance', 'ancestor', 'invented_parent', 'detached'):
            data = copy.deepcopy(original)
            child = next(m for m in data['assemblies'][0]['members'] if 'ancestor_person_id' in m)
            if alteration == 'distance':
                child['generation_distance'] = 3
            elif alteration == 'ancestor':
                child['ancestor_person_id'] = 'yqp_nlb_p1p_AC'
            elif alteration == 'invented_parent':
                child['parent_person_id'] = 'yqp_nlb_p1p_AC'
            else:
                del child['ancestor_person_id']
            with tempfile.TemporaryDirectory() as folder:
                root = Path(folder)
                (root / 'registry').mkdir()
                (root / 'registry/family-assemblies.json').write_text(json.dumps(data))
                with self.assertRaises(ValueError):
                    load_assemblies(root, catalog)

    def test_maternal_siblings_keep_separate_paternal_roots(self):
        source, rows = load_assemblies(ROOT, load_catalog(ROOT))
        fen, sheng, gai, queen = (source[p] for p in ('7mz_d13_9ka_A', '7mz_d13_9ka_B', '6d6_eg1_o3a_B', '6d6_eg1_o3a_A'))
        self.assertEqual(fen['parent_person_id'], '7mz_d13_9ka')
        self.assertEqual(sheng['parent_person_id'], '7mz_d13_9ka')
        self.assertEqual(gai['parent_person_id'], '6d6_eg1_o3a')
        self.assertEqual(queen['parent_person_id'], '6d6_eg1_o3a')
        self.assertNotEqual(fen['root_person_id'], gai['root_person_id'])
        self.assertEqual(source['7mz_d13_9ka_AA']['parent_person_id'], fen['person_id'])
        self.assertEqual(source['7mz_d13_9ka_AA']['person_id'], '7mz_d13_9ka_AA')

    def test_li_crown_prince_joins_existing_liu_rong_line(self):
        source, _ = load_assemblies(ROOT, load_catalog(ROOT))
        rong = source['yqp_nlb_p1p_ACAH']
        self.assertEqual(rong['person_id'], source['yqp_nlb_p1p_ACAH']['person_id'])
        self.assertEqual(rong['parent_person_id'], source['yqp_nlb_p1p_ACA']['person_id'])
        self.assertEqual(rong['root_person_id'], source['yqp_nlb_p1p_ACAA']['root_person_id'])
