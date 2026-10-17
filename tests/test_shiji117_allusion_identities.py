"""Allusive identities retain scope, evidence, and legendary provenance."""
import json
from pathlib import Path
import unittest
from scripts.consolidate_person_ids import reference_files

ROOT = Path(__file__).resolve().parents[1]
MAPPING = {'qq3_6ej_sfv':'78u_8ii_bnr', 'gh2_5l2_341':'6ip_dr3_fbl',
           'jwt_uii_drr':'ea8_yum_lvj', '92c_g3l_una':'oho_r3f_c6y',
           'tmz_ye1_qq7':'ddb_l4j_4j2', 'zg6_7x0_rlx':'8jz_o3s_obt',
           'rbd_piw_ehz':'jqy_1fv_u7v', '6wz_jmz_gmc':'ubt_idy_jr8',
           'dk9_ope_ko7':'y4i_pjk_4gn_A', 'u3d_aj2_qbe':'tpz_x3m_e0h',
           'sxc_v8z_vpu':'y4i_pjk_4gn_AA', '5sw_h4w_dcv':'rzv_0ll_3ty',
           'flz_o6t_45l':'ao3_0fy_d45_AAAA'}

def read(path):
    return json.loads((ROOT / path).read_text())

class XiangruAllusionIdentities(unittest.TestCase):
    def test_thirteen_materialized_decisions_keep_both_chapter_witnesses(self):
        ds = [d for d in read('corpus/shiji/117-equivalences.json')['decisions']
              if d['id'].startswith('eq-shiji117-allusion-')]
        self.assertEqual(len(ds), 13)
        self.assertEqual({d['canonical_person_id'] for d in ds}, set(MAPPING.values()))
        for d in ds:
            self.assertTrue(d['identity_materialized'])
            self.assertEqual(d['person_ids'], [d['canonical_person_id']])
            self.assertEqual(len(d['chapter_ids']), 2)
            self.assertEqual({e['chapter_id'] for e in d['evidence']}, set(d['chapter_ids']))
            self.assertTrue(all(e['quote'] and e['mention_ids'] for e in d['evidence']))
            self.assertFalse(d['human_reviewed'])

    def test_ancient_commentary_is_attributed_and_not_image_collation(self):
        ds = read('corpus/shiji/117-equivalences.json')['decisions']
        for suffix in ['zhu', 'yu', 'qi']:
            d = next(d for d in ds if d['id'] == 'eq-shiji117-allusion-' + suffix)
            ref, = d['references']
            self.assertIn('683113d4baf6febecaf2ccb7913df87c4d68d454', ref['url'])
            self.assertEqual(ref['scope'], 'ancient_commentary_identification')
            self.assertFalse(ref['image_verified'])
            self.assertEqual(len(ref['source_blob']), 40)
            self.assertEqual(len(ref['response_sha256']), 64)

    def test_weaker_short_form_and_strength_comparisons_are_provisional(self):
        ds = read('corpus/shiji/117-equivalences.json')['decisions']
        for suffix in ['tang', 'wu', 'wuhuo']:
            d = next(d for d in ds if d['id'] == 'eq-shiji117-allusion-' + suffix)
            self.assertEqual(d['confidence_level'], 'moderate')
            self.assertEqual(d['status'], 'contextual_provisional')

    def test_flood_xiahou_is_yu_without_new_genealogy(self):
        c = read('corpus/shiji/117.json')
        p = next(p for p in c['paragraphs'] if p['id'].endswith('p041'))
        m = next(m for m in p['mentions'] if m['surface'] == '夏後氏')
        self.assertEqual(m['person_id'], '6ip_dr3_fbl')
        d = next(d for d in read('corpus/shiji/117-identities.json')['decisions']
                 if d['id'] == 'd-shiji117-xiahou-flood')
        self.assertEqual(d['identification_basis']['target_mention_ids'], [m['id']])
        self.assertEqual(d['identification_basis']['historicity'], 'legendary_tradition')
        self.assertEqual(set(d['chapter_ids']), {'c-shiji-117-xiangru','c-shiji-002-xia'})
        self.assertNotIn('qualifiers', d)

    def test_legendary_sources_and_same_name_han_prince_stay_distinct(self):
        people = {p['id']: p for p in read('registry/persons.json')['persons']}
        for pid in ['6ip_dr3_fbl','ea8_yum_lvj','oho_r3f_c6y','ddb_l4j_4j2','8jz_o3s_obt','jqy_1fv_u7v']:
            self.assertEqual(people[pid]['historicity'], 'legendary_tradition')
        self.assertIn('yqp_nlb_p1p_ACAG', people)
        p = next(p for p in read('corpus/shiji/117.json')['paragraphs'] if p['id'].endswith('p053'))
        self.assertEqual(next(m['person_id'] for m in p['mentions'] if m['surface']=='虞舜'), 'ddb_l4j_4j2')

    def test_ershi_is_huhai_and_fictional_roles_remain_unlinked(self):
        c = read('corpus/shiji/117.json')
        for n in [48,49]:
            p = next(p for p in c['paragraphs'] if p['id'].endswith(f'p{n:03}'))
            self.assertEqual(next(m['person_id'] for m in p['mentions'] if m['surface']=='二世'), 'ao3_0fy_d45_AAAA')
        p = next(p for p in c['paragraphs'] if p['id'].endswith('p004'))
        self.assertTrue(all(m['person_id'] is None for m in p['mentions']))

    def test_retired_duplicates_have_no_registry_references_or_person_files(self):
        people = {p['id'] for p in read('registry/persons.json')['persons']}
        self.assertFalse(set(MAPPING) & people)
        for path in reference_files(ROOT):
            for old in MAPPING:
                self.assertNotIn(old, path.read_text(), str(path))
        for old in MAPPING:
            for directory in ['exports/persons','data/corpus/profiles']:
                self.assertFalse((ROOT / directory / f'{old}.json').exists())

if __name__ == '__main__':
    unittest.main()
