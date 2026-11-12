import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from family_assemblies import load_assemblies
from person_bundle import load_catalog
from quoted_genealogy_ancestry import valid as quoted_genealogy_parent_valid


class GuoFamilyAssemblyTests(unittest.TestCase):
    def setUp(self):
        self.catalog = load_catalog(ROOT)
        self.source, self.rows = load_assemblies(ROOT, self.catalog)
        self.assembly = next(a for a in json.loads((ROOT / 'registry/family-assemblies.json').read_text())['assemblies']
                             if a['id'] == 'family-taiyuan-guo-huai-near')
        self.members = {m['person_id']: m for m in self.assembly['members']}

    def test_guo_quan_to_guo_yun_is_contextual_quote_role_assembly(self):
        yun = self.members['r02_hoi_pu7_A']
        self.assertIsNone(yun['source_assertion_id'])
        self.assertEqual(yun['parent_person_id'], 'r02_hoi_pu7')
        self.assertEqual(yun['parent_connection']['interpretation_basis'],
                         'quoted_genealogy_named_father_grandfather_roles')
        self.assertTrue(quoted_genealogy_parent_valid(
            yun,
            self.members,
            {a['id']: a for r in self.catalog[1] if r.get('record_type') == 'person_assertion_set'
             for a in r['assertions']},
            {r['id']: r for r in self.catalog[1] if r.get('record_type') == 'marked_chapter'},
        ))
        assertions = [a for r in self.catalog[1] if r.get('record_type') == 'person_assertion_set'
                      for a in r['assertions']]
        self.assertFalse(any(a['predicate'] == 'father' and a['subject_person_id'] == 'ozn_wl2_nrm'
                             and a['object_person_id'] == 'r02_hoi_pu7' for a in assertions))

    def test_families_connect_only_through_attested_kinship_and_recorded_shared_father_rules(self):
        expected = {
            'd7u_f1n_let': ('r02_hoi_pu7_AA', 'r02_hoi_pu7_A', 'a-sgz026-guohuai-family-001'),
            'vji_mqe_2dj': ('r02_hoi_pu7_AB', 'r02_hoi_pu7_A', None),
            'd2s_53o_65p': ('r02_hoi_pu7_AC', 'r02_hoi_pu7_A', None),
            '64e_ce8_aba': ('r02_hoi_pu7_ACA', 'r02_hoi_pu7_AC', 'a-sgz026-guohuai-family-005'),
            '1cz_c76_jxs': ('r02_hoi_pu7_AAA', 'r02_hoi_pu7_AA', 'a-sgz026-guohuai-family-013'),
            'tiq_tug_olu': ('r02_hoi_pu7_AAAA', 'r02_hoi_pu7_AAA', 'a-sgz026-guohuai-family-014'),
        }
        for source_id, (person_id, parent_id, assertion_id) in expected.items():
            with self.subTest(source_id=source_id):
                row = self.source[source_id]
                self.assertEqual((row['person_id'], row['parent_person_id'], row['source_assertion_id']),
                                 (person_id, parent_id, assertion_id))
                self.assertEqual(row['root_person_id'], 'r02_hoi_pu7')
        self.assertEqual(self.source['64e_ce8_aba']['person_id'], 'r02_hoi_pu7_ACA')
        jinshu = next(r for r in self.catalog[1] if r.get('record_type') == 'marked_chapter'
                      and r['id'] == 'c-jinshu-045-guoyi')
        self.assertTrue(any(m.get('person_id') == '64e_ce8_aba' and m.get('surface') == '郭奕'
                            for p in jinshu['paragraphs'] for m in p.get('mentions', [])))
        separate = next(a for a in json.loads((ROOT / 'registry/family-assemblies.json').read_text())['assemblies']
                        if a['id'] == 'family-yingchuan-guo-jia-core')
        self.assertEqual(separate['root_person_id'], '344_68f_98e')
        self.assertFalse(any('64e_ce8_aba' in m['source_person_ids'] for m in separate['members']))

    def test_derived_profiles_and_summaries_expose_the_connected_cross_history_family(self):
        root = json.loads((ROOT / 'data/corpus/profiles/r02_hoi_pu7.json').read_text())
        self.assertEqual(root['assembled_children'][0]['person_id'], 'r02_hoi_pu7_A')
        self.assertEqual(root['assembled_children'][0]['parent_connection']['interpretation_basis'],
                         'quoted_genealogy_named_father_grandfather_roles')
        summary = json.loads((ROOT / 'data/corpus/summaries/r02_hoi_pu7.json').read_text())
        self.assertEqual(summary['family']['children'][0]['id'], 'ozn_wl2_nrm')
        self.assertEqual(summary['family']['children'][0]['label'], '郭緼')
        guoyi = json.loads((ROOT / 'data/corpus/summaries/r02_hoi_pu7_ACA.json').read_text())
        self.assertEqual(guoyi['heading'], '郭奕')
        self.assertEqual(guoyi['family']['ancestors'][0][0]['id'], 'd2s_53o_65p')
        self.assertEqual(guoyi['family']['ancestors'][0][0]['label'], '鎮〔郭配弟，字季南〕')

    def test_role_chain_rejects_wrong_layer_changed_role_and_different_source_context(self):
        assertions = {a['id']: a for r in self.catalog[1] if r.get('record_type') == 'person_assertion_set'
                      for a in r['assertions']}
        chapters = {r['id']: r for r in self.catalog[1] if r.get('record_type') == 'marked_chapter'}
        original = self.members['r02_hoi_pu7_A']
        for alteration in ('layer', 'far_role', 'different_paragraph', 'maternal',
                           'wrong_witness', 'wrong_quote'):
            with self.subTest(alteration=alteration):
                member = copy.deepcopy(original)
                aa = copy.deepcopy(assertions)
                cc = copy.deepcopy(chapters)
                if alteration == 'layer':
                    paragraph = next(p for p in cc['c-sanguozhi-026-guohuai']['paragraphs']
                                     if p['id'] == 'c-sanguozhi-026-guohuai:unit002')
                    paragraph['text_layer'] = 'received_chapter'
                elif alteration == 'far_role':
                    aa['a-sgz026-guohuai-family-002']['qualifiers']['source_kinship_frame']['roles']['grandfather'] = 'missing-mention'
                elif alteration == 'different_paragraph':
                    aa['a-sgz026-guohuai-family-002']['evidence'][0]['paragraph_id'] = 'other-paragraph'
                elif alteration == 'wrong_witness':
                    aa['a-sgz026-guohuai-family-001']['qualifiers']['source_kinship_frame']['fixed_witness_reference']['sha256'] = '0' * 64
                elif alteration == 'wrong_quote':
                    aa['a-sgz026-guohuai-family-002']['evidence'][0]['quote'] += '異'
                else:
                    aa['a-sgz026-guohuai-family-002']['qualifiers']['lineage'] = 'maternal'
                self.assertFalse(quoted_genealogy_parent_valid(member, self.members, aa, cc))

    def test_role_chain_rejects_a_conflicting_explicit_father_for_the_inferred_parent(self):
        assertions = {a['id']: a for r in self.catalog[1] if r.get('record_type') == 'person_assertion_set'
                      for a in r['assertions']}
        chapters = {r['id']: r for r in self.catalog[1] if r.get('record_type') == 'marked_chapter'}
        altered = copy.deepcopy(assertions)
        conflict = copy.deepcopy(altered['a-sgz026-guohuai-family-001'])
        conflict['id'] = 'test-yun-conflicting-father'
        conflict['subject_person_id'] = 'ozn_wl2_nrm'
        conflict['object_person_id'] = 'd7u_f1n_let'
        altered[conflict['id']] = conflict
        self.assertFalse(quoted_genealogy_parent_valid(
            self.members['r02_hoi_pu7_A'], self.members, altered, chapters))


if __name__ == '__main__':
    unittest.main()
