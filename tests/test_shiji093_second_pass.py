# coding: utf-8
import json
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

class HanLuIdentityTests(unittest.TestCase):
    def paragraph(self, book, suffix):
        c = json.loads((ROOT / f'corpus/shiji/{book}.json').read_text())
        return next(p for p in c['paragraphs'] if p['id'].endswith(':' + suffix))
    def ids(self, p, surface):
        return {m['person_id'] for m in p['mentions'] if m['surface'] == surface}
    def test_kings_and_two_hanxin_people_stay_distinct(self):
        p = self.paragraph('093', 'p001')
        self.assertEqual(self.ids(p, '韓王信'), {'l9e_fbr_36a_*A'})
        self.assertEqual(self.ids(p, '橫陽君成'), {'8i3_5vf_iu9'})
        q = self.paragraph('093', 'p003')
        self.assertEqual(self.ids(q, '鄭昌'), {'vxt_uj1_8ym'})
        self.assertEqual(self.ids(q, '韓王昌'), {'vxt_uj1_8ym'})
        self.assertEqual(self.ids(self.paragraph('092', 'p001'), '淮陰侯韓信'), {'ofc_8ei_jb7'})
        self.assertIn('故吳令鄭昌', self.paragraph('007', 'p024')['text'])
    def test_new_huaiwang_is_not_earlier_captive_king(self):
        p = self.paragraph('093', 'p001')
        self.assertEqual(self.ids(p, '項梁'), {'5xt_rg8_7zs_A'})
        self.assertEqual(self.ids(p, '懷王'), {'c2w_s7g_en0_*A'})
        q = self.paragraph('007', 'p006')
        self.assertIn('自懷王入秦不反', q['text'])
        self.assertIn('求楚懷王孫心', q['text'])
        self.assertEqual(self.ids(q, '懷王'), {'c2w_s7g_en0', 'c2w_s7g_en0_*A'})
    def test_baideng_people_and_short_names_use_scoped_evidence(self):
        p = self.paragraph('093', 'p005')
        self.assertEqual(self.ids(p, '冒頓'), {'wjt_htu_081_A'})
        self.assertEqual(self.ids(p, '陳平'), {'i3f_9l9_g53'})
        self.assertIn('白登', self.paragraph('110', 'p012')['text'])
        self.assertIn('高帝用陳平奇計', self.paragraph('056', 'p012')['text'])
        p = self.paragraph('093', 'p008')
        self.assertEqual(self.ids(p, '蕭'), {'xd8_uww_5ok'})
        self.assertEqual(self.ids(p, '曹'), {'37j_16p_7n8'})
        rows = json.loads((ROOT / 'corpus/shiji/093-equivalences.json').read_text())['decisions']
        for key in ['xiao', 'cao']:
            row = next(x for x in rows if x['id'] == 'eq-shiji093-review-' + key)
            self.assertIn('較弱', row['rationale'])
            self.assertFalse(row['human_reviewed'])

    def test_gongwei_uses_the_same_liu_jia_lu_wan_campaign(self):
        p = self.paragraph('093', 'p009')
        self.assertEqual(self.ids(p, '共尉'), {'bwv_ob8_6xi_A'})
        q = self.paragraph('051', 'p003')
        self.assertIn('太尉盧綰', q['text'])
        self.assertIn('臨江王共尉', q['text'])
        self.assertEqual(self.ids(q, '臨江王共尉'), {'bwv_ob8_6xi_A'})
    def test_zhao_officers_and_zhoubo_do_not_merge_same_office(self):
        self.assertEqual(self.ids(self.paragraph('093', 'p015'), '周昌'), {'gfr_55l_72s'})
        p = self.paragraph('093', 'p011')
        self.assertEqual(self.ids(p, '審食其'), {'qg7_n12_fne'})
        self.assertEqual(self.ids(p, '趙堯'), {'afb_ahe_sqp'})
        self.assertEqual(self.ids(self.paragraph('093', 'p017'), '勃'), {'koy_6jg_gcc'})
        self.assertIn('徙御史大夫周昌為趙相', self.paragraph('096', 'p006')['text'])
        self.assertIn('遂拜趙堯為御史大夫', self.paragraph('096', 'p007')['text'])
        self.assertIn('勃遷為太尉', self.paragraph('057', 'p004')['text'])

    def test_han_and_lu_direct_paths_keep_unknown_generations(self):
        people = {p['id']: p for p in json.loads((ROOT / 'registry/persons.json').read_text())['persons']}
        han = people['l9e_fbr_36a_*A']['family_path']
        self.assertEqual(han['ancestor_person_id'], 'l9e_fbr_36a')
        self.assertEqual(han['connection'], 'grandfather')
        self.assertIsNone(han['parent_person_id'])
        self.assertEqual(han['intermediate_person_ids'], [None])
        self.assertEqual(han['source_assertion_id'], 'a-shiji093-001')
        self.assertEqual(people['l9e_fbr_36a_*AB']['family_path']['parent_person_id'], 'l9e_fbr_36a_*A')
        self.assertEqual(people['l9e_fbr_36a_*AB*A']['family_path']['ancestor_person_id'], 'l9e_fbr_36a_*AB')
        self.assertEqual(people['jjl_irg_zke_A']['family_path']['parent_person_id'], 'jjl_irg_zke')
        self.assertEqual(people['jjl_irg_zke_A*A']['family_path']['intermediate_person_ids'], [None])
        self.assertFalse(any(p['id'].endswith('_*') for p in people.values()))

    def test_gonggao_and_hanyan_endpoints_match_in_both_chapters(self):
        p = self.paragraph('093', 'p007')
        q = self.paragraph('125', 'p003')
        self.assertEqual(self.ids(p, '韓嫣'), {'l9e_fbr_36a_*AB*A'})
        self.assertEqual(self.ids(q, '韓嫣'), {'l9e_fbr_36a_*AB*A'})
        self.assertEqual(self.ids(q, '弓高侯'), {'l9e_fbr_36a_*AB'})
        self.assertEqual(self.ids(q, '韓說'), {'l9e_fbr_36a_*AB*B'})
        self.assertEqual(self.ids(p, '說'), {'l9e_fbr_36a_*AB*B'})
        self.assertEqual(self.ids(self.paragraph('093', 'p001'), '韓襄王'), {'l9e_fbr_36a'})

    def test_sibling_grandfather_is_not_fabricated_as_direct_assertion(self):
        rows = json.loads((ROOT / 'corpus/shiji/093-assertions.json').read_text())['assertions']
        brother = next(x for x in rows if x['id'] == 'a-shiji093-006')
        self.assertEqual((brother['subject_person_id'], brother['object_person_id']),
                         ('l9e_fbr_36a_*AB*B', 'l9e_fbr_36a_*AB*A'))
        self.assertFalse(any(x['subject_person_id'] == 'l9e_fbr_36a_*AB*B' and x['predicate'] in ['father', 'grandfather'] for x in rows))

    def test_zi_dai_is_an_unnamed_son_and_succession_verb(self):
        p = self.paragraph('093', 'p007')
        m = next(x for x in p['mentions'] if x['id'] == 'c-shiji-093-hanlu:m007-0137')
        self.assertEqual(m['surface'], '子')
        self.assertEqual(p['text'][m['end']], '代')
        self.assertEqual(m['person_id'], 'l9e_fbr_36a_*AB*BA')
        people = json.loads((ROOT / 'registry/persons.json').read_text())['persons']
        child = next(x for x in people if x['id'] == m['person_id'])
        self.assertIn('子未名', child['label'])
        self.assertEqual(child['family_path']['parent_person_id'], 'l9e_fbr_36a_*AB*B')
        self.assertFalse(any(a['surface'] in ['子代', '代', '長君'] for a in child['aliases']))
        rows = json.loads((ROOT / 'corpus/shiji/093-identities.json').read_text())['decisions']
        ref = next(x for x in rows if x['id'] == 'd-shiji093-032')['references'][0]
        self.assertEqual(ref['reported_name'], '長君')
        self.assertFalse(ref['adopted_as_received_name'])

    def test_han_emperor_short_names_follow_their_reigns(self):
        self.assertEqual(self.ids(self.paragraph('093', 'p007'), '孝文'), {'yqp_nlb_p1p_AC'})
        self.assertEqual(self.ids(self.paragraph('093', 'p013'), '孝景'), {'yqp_nlb_p1p_ACA'})
        self.assertIn('孝文皇帝，高祖中子', self.paragraph('010', 'p001')['text'])
        self.assertIn('孝景皇帝者，孝文之中子', self.paragraph('011', 'p001')['text'])
    def test_quoted_yue_and_wu_people_keep_departure_and_death_accounts(self):
        p = self.paragraph('093', 'p006')
        self.assertEqual(self.ids(p, '種'), {'gu2_fde_5bw'})
        self.assertEqual(self.ids(p, '蠡'), {'yhm_h9f_8p0'})
        self.assertEqual(self.ids(p, '伍子胥'), {'g9h_5ih_ug1_A'})
        self.assertIn('種、蠡無一罪，身死亡', p['text'])
        self.assertIn('范蠡浮海出齊', self.paragraph('041', 'p020')['text'])
        self.assertIn('種遂自殺', self.paragraph('041', 'p013')['text'])
        self.assertIn('乃自剄死', self.paragraph('066', 'p019')['text'])

    def test_life_events_keep_two_hanxin_and_relative_dates_distinct(self):
        x = json.loads((ROOT / 'corpus/shiji/093-life-events.json').read_text())
        deaths = {e['person_id']: e for e in x['events'] if e['event_type'] == 'death'}
        self.assertEqual(len(deaths), 6)
        self.assertNotIn('ofc_8ei_jb7', deaths)
        self.assertEqual(deaths['l9e_fbr_36a_*A']['normalized_date']['era_year'], 196)
        self.assertEqual(deaths['l9e_fbr_36a_*A']['normalized_date']['year'], -195)
        for pid in ('jjl_irg_zke_A', 'eav_dh2_8o8', 'l9e_fbr_36a_*AB*BA', '1xx_s1v_svn'):
            self.assertNotIn('normalized_date', deaths[pid])
        child = deaths['l9e_fbr_36a_*AB*BA']
        self.assertEqual(child['evidence'][0]['person_mention_id'], 'c-shiji-093-hanlu:m007-0137')
        self.assertEqual(deaths['1xx_s1v_svn']['date_expression'], '高祖十二年冬')

    def test_tuidang_birth_and_hanxin_death_places_have_original_quotes(self):
        x = json.loads((ROOT / 'corpus/shiji/093-life-events.json').read_text())
        birth = next(e for e in x['events'] if e['event_type'] == 'birth')
        self.assertEqual(birth['person_id'], 'l9e_fbr_36a_*AB')
        self.assertNotIn('normalized_date', birth)
        addresses = json.loads((ROOT / 'corpus/shiji/093-addresses.json').read_text())['assertions']
        b = next(a for a in addresses if a['relation'] == 'birth_place')
        self.assertEqual(b['person_id'], birth['person_id'])
        self.assertEqual(b['place']['source_name'], '穨當城')
        self.assertIsNone(b['place']['modern_identification'])
        d = next(a for a in addresses if a['place']['source_name'] == '參合')
        self.assertEqual(d['person_id'], 'l9e_fbr_36a_*A')
        self.assertEqual(d['relation'], 'death_place')

    def test_zangtu_variant_and_later_campaign_references_share_identity(self):
        self.assertEqual(self.ids(self.paragraph('093', 'p010'), '臧茶'), {'xaa_ewn_4ro'})
        for suffix in ('p006', 'p013', 'p020', 'p028'):
            self.assertEqual(self.ids(self.paragraph('095', suffix), '臧荼'), {'xaa_ewn_4ro'})
        self.assertIn('故燕王臧茶子衍出亡在胡', self.paragraph('093', 'p010')['text'])
        d = json.loads((ROOT / 'corpus/shiji/093-equivalences.json').read_text())['decisions']
        d = next(d for d in d if d['id'] == 'eq-shiji093-zangtu-context')
        self.assertTrue(d['identity_materialized'])
        self.assertEqual(len(d['chapter_ids']), 3)

    def test_zangtu_child_retains_sourced_father_and_no_old_json(self):
        people = {p['id']: p for p in json.loads((ROOT / 'registry/persons.json').read_text())['persons']}
        child = people['xaa_ewn_4ro_A']
        self.assertEqual(child['family_path']['parent_person_id'], 'xaa_ewn_4ro')
        self.assertEqual(child['family_path']['source_assertion_id'], 'a-shiji093-011')
        self.assertNotIn('候選', child['label'])
        for pid in ('awy_adj_c0u', 'awy_adj_c0u_A', 'un2_jcz_dkt'):
            self.assertNotIn(pid, people)
            self.assertFalse((ROOT / f'exports/persons/{pid}.json').exists())
            self.assertFalse((ROOT / f'data/corpus/profiles/{pid}.json').exists())

    def test_lvhou_gaohou_and_weigong_have_contextual_identities(self):
        self.assertEqual(self.ids(self.paragraph('093', 'p011'), '呂后'), {'i30_mjq_6q8_A'})
        self.assertEqual(self.ids(self.paragraph('093', 'p012'), '高后'), {'i30_mjq_6q8_A'})
        self.assertEqual(self.ids(self.paragraph('093', 'p020'), '魏公子'), {'h8u_hld_5su'})
        decisions = json.loads((ROOT / 'corpus/shiji/093-equivalences.json').read_text())['decisions']
        for key in ('lvhou', 'gaohou', 'weigong'):
            d = next(d for d in decisions if d['id'] == 'eq-shiji093-lvhou-weigong-' + key)
            self.assertTrue(d['identity_materialized'])
            self.assertEqual(d['status'], 'contextual_provisional')
            self.assertGreaterEqual(len(d['chapter_ids']), 2)
        # Preserve received glyphs while recording the preferred referent.
        self.assertIn('高祖竟崩', self.paragraph('093', 'p012')['text'])
        self.assertEqual(self.ids(self.paragraph('093', 'p012'), '高祖'), {'i30_mjq_6q8_A'})

    def test_lvhou_weigong_retired_candidates_have_no_json_or_aliases(self):
        persons = json.loads((ROOT / 'registry/persons.json').read_text())['persons']
        ids = {p['id'] for p in persons}
        aliases = {a for p in persons for a in p.get('id_aliases', [])}
        for pid in ('smi_qcr_wtg', '4xv_p1u_vn2', 'xlt_9ml_n9i'):
            self.assertNotIn(pid, ids)
            self.assertNotIn(pid, aliases)
            self.assertFalse((ROOT / f'exports/persons/{pid}.json').exists())
            self.assertFalse((ROOT / f'data/corpus/profiles/{pid}.json').exists())

    def test_gaohou_editorial_reading_does_not_become_false_alias(self):
        p = json.loads((ROOT / 'data/corpus/profiles/i30_mjq_6q8_A.json').read_text())
        self.assertNotIn('高祖', p['names'])
        v = next(v for v in p['reported_variants'] if v['id'] == 'rv-shiji093-gaohou')
        self.assertFalse(v['adopted'])
        self.assertFalse(v['image_verified'])
        self.assertIn('高后竟崩', v['quote'])
        r = next(r for r in p['preferred_readings'] if r['person_mention_id'] == 'c-shiji-093-hanlu:m012-0032')
        self.assertEqual(r['preferred_surface'], '高后')
        self.assertTrue(r['source_spelling_is_not_alias'])

    def test_preferred_reading_rejects_unreported_surface(self):
        import tempfile, shutil
        from scripts.validate_corpus import validate
        with tempfile.TemporaryDirectory() as folder:
            target = (Path(folder) / 'repo').resolve()
            # Native validation reads these inputs; public bundles, reader imports
            # and other generated outputs do not participate in this operation.
            for name in ('registry', 'corpus', 'source-evidence', 'sources'):
                shutil.copytree(ROOT / name, target / name)
            shutil.copytree(ROOT / 'data/historical-tables', target / 'data/historical-tables')
            (target / 'data/corpus').mkdir(parents=True)
            shutil.copy2(ROOT / 'data/corpus/profile-names.json', target / 'data/corpus/profile-names.json')
            # Complete source validation also consumes trusted recipe/pin JSON and work records.
            shutil.copytree(ROOT / 'data/works', target / 'data/works')
            (target / 'scripts').mkdir()
            for config in (ROOT / 'scripts').glob('*.json'):
                shutil.copy2(config, target / 'scripts' / config.name)
            self.assertEqual(validate(target), [])
            p = target / 'corpus/shiji/093-identities.json'
            x = json.loads(p.read_text())
            d = next(d for d in x['decisions'] if d['id'] == 'd-shiji093-preferred-gaohou')
            d['preferred_reading']['preferred_surface'] = '高帝'
            p.write_text(json.dumps(x, ensure_ascii=False))
            self.assertTrue(any('首選校讀' in e for e in validate(target)))

    def test_preferred_reading_rejects_another_paragraph_anchor(self):
        import tempfile, shutil
        from scripts.validate_corpus import validate
        with tempfile.TemporaryDirectory() as folder:
            target = (Path(folder) / 'repo').resolve()
            # Native validation reads these inputs; public bundles, reader imports
            # and other generated outputs do not participate in this operation.
            for name in ('registry', 'corpus', 'source-evidence', 'sources'):
                shutil.copytree(ROOT / name, target / name)
            shutil.copytree(ROOT / 'data/historical-tables', target / 'data/historical-tables')
            (target / 'data/corpus').mkdir(parents=True)
            shutil.copy2(ROOT / 'data/corpus/profile-names.json', target / 'data/corpus/profile-names.json')
            # Complete source validation also consumes trusted recipe/pin JSON and work records.
            shutil.copytree(ROOT / 'data/works', target / 'data/works')
            (target / 'scripts').mkdir()
            for config in (ROOT / 'scripts').glob('*.json'):
                shutil.copy2(config, target / 'scripts' / config.name)
            self.assertEqual(validate(target), [])
            p = target / 'corpus/shiji/093-identities.json'
            x = json.loads(p.read_text())
            d = next(d for d in x['decisions'] if d['id'] == 'd-shiji093-preferred-gaohou')
            d['preferred_reading']['person_mention_id'] = 'c-shiji-093-hanlu:m012-0000'
            p.write_text(json.dumps(x, ensure_ascii=False))
            self.assertTrue(any('首選校讀' in e for e in validate(target)))

    def test_chai_general_preferred_identity_keeps_son_distinct(self):
        self.assertEqual(self.ids(self.paragraph('093', 'p006'), '柴將軍'), {'4yg_ete_09a'})
        self.assertEqual(self.ids(self.paragraph('101', 'p004'), '柴武'), {'4yg_ete_09a'})
        self.assertEqual(self.ids(self.paragraph('118', 'p003'), '棘蒲侯柴武'), {'4yg_ete_09a'})
        self.assertEqual(self.ids(self.paragraph('118', 'p003'), '太子奇'), {'4yg_ete_09a_A'})
        people = {p['id']: p for p in json.loads((ROOT / 'registry/persons.json').read_text())['persons']}
        child = people['4yg_ete_09a_A']
        self.assertEqual(child['family_path']['parent_person_id'], '4yg_ete_09a')
        self.assertEqual(child['family_path']['source_assertion_id'], 'a-shiji101-003')
        self.assertNotIn('候選', people['4yg_ete_09a']['label'])
        a = json.loads((ROOT / 'corpus/shiji/101-assertions.json').read_text())['assertions']
        a = next(a for a in a if a['id'] == 'a-shiji101-003')
        self.assertIsNone(a['qualifiers']['birth_ordinal'])

    def test_chai_general_alternative_is_preserved_not_a_false_name(self):
        p = json.loads((ROOT / 'data/corpus/profiles/4yg_ete_09a.json').read_text())
        v = next(v for v in p['reported_variants'] if v['id'] == 'rv-shiji093-chai-general')
        self.assertIn('柴武', v['quote'])
        self.assertIn('柴奇', v['quote'])
        self.assertFalse(v['adopted'])
        self.assertFalse(v['image_verified'])
        self.assertNotIn('柴奇', p['names'])
        ids = {p['id'] for p in json.loads((ROOT / 'registry/persons.json').read_text())['persons']}
        for pid in ('8r5_zyc_5dx', 'tqe_7o9_t4k', 'qbh_lsz_ipx'):
            self.assertNotIn(pid, ids)
            self.assertFalse((ROOT / f'exports/persons/{pid}.json').exists())

    def test_remaining_court_people_match_events_not_generic_titles(self):
        p=self.paragraph('093','p011')
        self.assertEqual(self.ids(p,'黥布'),{'zxd_afr_2xg'})
        self.assertEqual(self.ids(p,'淮陰'),{'ofc_8ei_jb7'})
        self.assertEqual(self.ids(p,'彭越'),{'9qt_orl_5f2'})
        self.assertEqual(self.ids(self.paragraph('093','p003'),'周苛'),{'7tm_3ss_4on'})
        self.assertEqual(self.ids(self.paragraph('093','p003'),'韓王信'),{'l9e_fbr_36a_*A'})
        self.assertIn('三年',self.paragraph('093','p003')['text'])
        self.assertIn('漢王四年',self.paragraph('096','p004')['text'])
        self.assertIn('往年殺彭越，前年殺韓信',self.paragraph('091','p015')['text'])

    def test_remaining_court_candidates_retired_after_references_updated(self):
        people={p['id'] for p in json.loads((ROOT/'registry/persons.json').read_text())['persons']}
        for pid in ('ehh_a65_95j','7mw_nab_5z6','ova_rch_fa4','nu6_2qe_oza'):
            self.assertNotIn(pid,people)
            self.assertFalse((ROOT/f'exports/persons/{pid}.json').exists())
            self.assertFalse((ROOT/f'data/corpus/profiles/{pid}.json').exists())
