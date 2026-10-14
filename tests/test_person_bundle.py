import unittest
from scripts.person_bundle import bundle


class PersonBundleTests(unittest.TestCase):
    def test_zhangyi_dated_tenures_do_not_turn_point_duration_into_total(self):
        result = bundle('uq6_74z_vtv', include_provisional=True)
        holdings = {h['id']:h for h in result['title_holdings']}
        h = holdings['th-shiji070-004']
        self.assertEqual(h['reported_duration']['value'], 4)
        self.assertEqual(h['reported_duration']['source_term'], '儀相秦四歲')
        self.assertEqual(h['reported_duration']['counting'], 'unspecified_source_years')
        self.assertEqual((h['effective_period']['start']['normalized_date']['era_year'], h['effective_period']['end']['normalized_date']['era_year']), (328,322))
        self.assertEqual(holdings['th-shiji070-016']['reported_duration']['value'], 1)
        self.assertNotIn('reported_duration', holdings['th-shiji070-007'])
        self.assertEqual(holdings['th-shiji070-007']['effective_period']['end']['status'], 'unknown')
    def test_zhangyi_death_year_and_death_place_keep_exact_sources(self):
        result = bundle('uq6_74z_vtv', include_provisional=True)
        death = next(e for e in result['life_events'] if e['id']=='le-shiji070-006')
        date = death['normalized_date']
        self.assertEqual((date['era_year'],date['year']), (309,-308))
        self.assertEqual(date['references'][0]['quote'], '十。張儀死。')
        self.assertEqual(date['references'][1]['quote'], '309')
        self.assertEqual(len(death['evidence']), 2)
        self.assertTrue(any(a['relation']=='death_place' and a['place']['source_name']=='魏' for a in result['address_assertions']))
    def test_qugai_identity_does_not_erase_killed_and_captured_difference(self):
        result = bundle('c38_dzq_0o4', include_provisional=True)
        death = next(e for e in result['life_events'] if e['id']=='le-shiji070-002')
        self.assertEqual(death['source_term'], '殺屈丐')
        self.assertIn('虜其將屈丐', death['interpretation_note'])
        self.assertNotIn('normalized_date', death)
    def test_zhangyi_north_to_yan_is_not_dai_king_journey(self):
        result = bundle('uq6_74z_vtv', include_provisional=True)
        journey = next(a for a in result['address_assertions'] if a['id']=='pa-shiji070-010')
        self.assertEqual(journey['evidence'][0]['context']['paragraph_id'], 'c-shiji-070-zhang:p045')
        self.assertEqual(journey['source_term'], '北之燕')
        self.assertEqual(journey['place']['source_name'], '燕')
    def test_suqin_journeys_include_complete_carried_subject_passages(self):
        result = bundle('422_9v5_g9x', include_provisional=True)
        journey = next(a for a in result['address_assertions'] if a['id']=='pa-shiji069-004')
        context = journey['evidence'][0]['context']
        self.assertEqual(context['intervening_paragraph_ids'], ['c-shiji-069-su:p003','c-shiji-069-su:p004'])
        passages = {p['id']:p for p in result['passages']}
        for pid in [context['paragraph_id']] + context['intervening_paragraph_ids'] + [journey['evidence'][0]['paragraph_id']]:
            self.assertIn(pid, passages)
        self.assertEqual(journey['place']['source_name'], '燕')
        self.assertEqual(passages['c-shiji-069-su:p005']['text'][:3], '去游燕')
    def test_sudai_affinity_is_not_a_spouse_or_invented_generation(self):
        result = bundle('phx_4fq_fnx', include_provisional=True)
        relation = next(a for a in result['relations'] if a['id']=='a-shiji069-011')
        self.assertEqual(relation['predicate'], 'affinity_unspecified')
        self.assertEqual(relation['qualifiers']['source_term'], '子之與蘇代婚')
        for key in ('spouse_person_ids','connecting_person_ids','generation_difference'):
            self.assertIsNone(relation['qualifiers'][key])
        self.assertFalse(any(a['predicate']=='spouse' and {a['subject_person_id'],a['object_person_id']}=={'nfi_mir_dew','phx_4fq_fnx'} for a in result['relations']))
    def test_suqin_unknown_office_actions_and_no_false_death_or_duration(self):
        result = bundle('422_9v5_g9x', include_provisional=True)
        events = [e for e in result['person_events'] if e['id'].startswith('pe-shiji069-')]
        self.assertEqual([e['event_type'] for e in events], ['office_non_reinstatement','office_restoration'])
        for e in events:
            self.assertIsNone(e['office_title'])
            self.assertIsNone(e['title_holding_id'])
        deaths = [e for e in result['life_events'] if e['id'].startswith('le-shiji069-')]
        self.assertEqual(len(deaths), 1)
        self.assertEqual(deaths[0]['source_term'], '蘇秦既死')
        self.assertFalse(any('reported_duration' in h for h in result['title_holdings'] if h['id'].startswith('th-shiji069-')))
    def test_su_brothers_keep_relative_order_without_absolute_ordinals(self):
        result = bundle('phx_4fq_fnx', include_provisional=True)
        order = next(a for a in result['relations'] if a['id']=='a-shiji069-008')['qualifiers']['relative_birth_order']
        self.assertEqual((order['older_person_id'],order['younger_person_id'],order['operator']), ('422_9v5_g9x','phx_4fq_fnx','lt'))
        self.assertIsNone(order['older_ordinal'])
        self.assertIsNone(order['younger_ordinal'])
    def test_shang_wei_lineage_affiliation_is_not_a_birthplace(self):
        result = bundle('2wp_usr_ncd', include_provisional=True)
        place = next(a for a in result['address_assertions'] if a['id']=='pa-shiji068-007')
        self.assertEqual(place['relation'], 'polity_lineage_affiliation')
        self.assertEqual(place['place']['source_name'], '衛')
        self.assertEqual(place['qualifiers']['affiliation_kind'], 'royal_lineage')
        self.assertEqual(place['source_term'], '衛之諸庶孽公子')
        self.assertIsNone(place['place']['modern_identification'])
    def test_shang_title_years_do_not_resolve_ambiguous_left_shuzhang_or_tenure_ends(self):
        result = bundle('2wp_usr_ncd', include_provisional=True)
        holdings = {h['id']:h for h in result['title_holdings']}
        for hid, year in [('th-shiji068-009',352),('th-shiji068-017',340)]:
            period = holdings[hid]['effective_period']
            date = period['start']['normalized_date']
            self.assertEqual(date['era_year'], year)
            self.assertEqual(date['basis']['reference_year_quote'], str(year))
            self.assertEqual(date['status'], 'editorial_provisional')
            self.assertEqual(period['end']['status'], 'unknown')
            self.assertNotIn('normalized_date', period['end'])
        self.assertNotIn('normalized_date', holdings['th-shiji068-005']['effective_period']['start'])
    def test_bailixi_approximate_title_years_keep_unknown_dates(self):
        result = bundle('ws3_3yb_yzp', include_provisional=True)
        holding = next(h for h in result['title_holdings'] if h['id']=='th-shiji068-020')
        duration = holding['reported_duration']
        self.assertIsNone(duration['value'])
        self.assertEqual(duration['approximation'], {'kind':'adjacent_year_numbers','numbers':[6,7]})
        self.assertEqual(duration['source_number'], '六七')
        self.assertEqual(duration['source_term'], '相秦六七年')
        self.assertNotIn('bounds', duration)
        for boundary in holding['effective_period'].values():
            self.assertEqual(boundary['status'], 'unknown')
            self.assertNotIn('normalized_date', boundary)
        self.assertIn(duration['evidence'][0]['paragraph_id'], {p['id'] for p in result['passages']})
    def test_shang_death_year_preserves_separate_event_and_editorial_year_citations(self):
        result = bundle('2wp_usr_ncd', include_provisional=True)
        event = next(e for e in result['life_events'] if e['id']=='le-shiji068-006')
        date = event['normalized_date']
        self.assertEqual((date['era_year'], date['year']), (338,-337))
        self.assertEqual(date['basis']['reference_year_quote'], '338')
        self.assertIn('死彤地', date['basis']['reference_event_quote'])
        self.assertIn('殺之於鄭黽池', date['original_quote'])
        self.assertEqual(date['references'][1]['table_cell_id'], 'shiji-015-r139-c00')
        self.assertTrue(all(r['image_verified'] is False for r in date['references']))
    def test_wei_default_lineage_keeps_three_sons_and_retains_fourth_source_claim(self):
        result = bundle('5dd_l1c_6g8', include_provisional=True)
        self.assertIn('a-shiji049-045', {a['id'] for a in result['relations']})
        self.assertNotIn('a-shiji049-045', {a['id'] for a in result['preferred_relations']})
        children = {a['subject_person_id'] for a in result['preferred_relations']
                    if a['predicate'] == 'father' and a['object_person_id'] in result['person_ids']}
        identities = {frozenset(bundle(child, include_provisional=True)['person_ids']) for child in children}
        self.assertEqual(len(identities), 3)
        kang = bundle('5dd_l1c_6g8_D', include_provisional=True)
        self.assertIn('5dd_l1c_6g8_D', kang['person_ids'])
        self.assertNotIn('5dd_l1c_6g8_C', kang['person_ids'])
        father = next(a for a in kang['relations'] if a['id'] == 'a-shiji111-012')
        self.assertEqual(father['qualifiers']['birth_order']['ordinal'], 1)
        self.assertEqual(father['qualifiers']['birth_order']['scope'], 'sons_of_parent')
        younger = [a['qualifiers']['relative_birth_order'] for a in kang['relations']
                   if 'relative_birth_order' in a.get('qualifiers', {})]
        self.assertEqual(len(younger), 2)
        self.assertTrue(all(a['older_person_id'] == '5dd_l1c_6g8_D' and a['younger_ordinal'] is None for a in younger))
        succession = next(h for h in kang['title_holdings'] if h['mode'] == 'accession' and h['title'] == '長平侯')
        self.assertEqual(succession['effective_period']['start']['normalized_date']['era_year'], 104)
        self.assertNotIn('normalized_date', succession['effective_period']['end'])
        self.assertEqual(succession['reported_duration']['value'], 6)
    def test_shan_accession_does_not_copy_fathers_death_year(self):
        result = bundle('3tw_nq2_gyn_A', include_provisional=True)
        holding = next(h for h in result['title_holdings'] if 'inheritance' in h)
        self.assertIsNone(holding['effective_period']['start']['date_expression'])
        self.assertEqual(holding['effective_period']['start']['normalized_date']['era_year'], 116)
        self.assertEqual(holding['reported_duration']['value'], 6)
    def test_inherited_rank_is_parseable_without_expanding_source_text(self):
        result = bundle('3tw_nq2_gyn_A', include_provisional=True)
        holding = next(h for h in result['title_holdings'] if 'inheritance' in h)
        self.assertEqual(holding['title'], '侯')
        self.assertEqual(holding['inheritance']['resolved_title'], '冠軍侯')
        self.assertEqual(holding['inheritance']['predecessor_person_id'], '3tw_nq2_gyn')
        self.assertEqual(holding['reported_duration']['value'], 6)
        self.assertEqual(holding['effective_period']['end']['event_type'], 'abolition')
        self.assertEqual(holding['effective_period']['end']['normalized_date']['era_year'], 110)
        self.assertEqual(next(e for e in result['life_events'] if e['event_type'] == 'death')['normalized_date']['era_year'], 110)
    def test_huo_reported_title_years_do_not_set_tenure_end(self):
        result = bundle('3tw_nq2_gyn', include_provisional=True)
        holding = next(h for h in result['title_holdings'] if h.get('reported_duration', {}).get('unit') == 'title_year')
        self.assertEqual(holding['reported_duration']['value'], 3)
        self.assertEqual(holding['reported_duration']['source_term'], '既侯三歲')
        self.assertEqual(holding['effective_period']['end']['status'], 'unknown')
    def test_huo_age_is_exported_without_inferred_birth(self):
        result = bundle('3tw_nq2_gyn', include_provisional=True)
        age = result['age_assertions'][0]
        self.assertEqual((age['value'], age['source_term']), (18, '年十八'))
        self.assertIsNone(age['birth_year'])
        self.assertEqual(age['counting'], 'unspecified_source_age')
        self.assertEqual(age['normalized_date']['era_year'], 123)
        self.assertIn(age['evidence'][0]['paragraph_id'], {p['id'] for p in result['passages']})
        births = [e for e in result.get('life_events', []) if e['event_type'] == 'birth']
        self.assertTrue(births)
        for event in births:
            self.assertIsNone(event['date_expression'])
            self.assertNotIn('normalized_date', event)
            self.assertEqual(event['source_term'], '\u5c11\u5152\u751f\u5b50\u970d\u53bb\u75c5')
            self.assertTrue(any(event['source_term'] in e['quote'] for e in event['evidence']))
    def test_yuan_ang_cross_chapter_bundle_keeps_sourced_death_place(self):
        result = bundle('j32_wtj_khz_A', include_provisional=True)
        self.assertTrue({'j32_wtj_khz_A', 'j32_wtj_khz_A', 'j32_wtj_khz_A'}.issubset(result['person_ids']))
        place = next(a for a in result['address_assertions'] if a['id'] == 'pa-shiji101-005')
        self.assertEqual(place['place']['source_name'], '安陵郭門外')
        self.assertIn('刺殺盎安陵郭門外', place['evidence'][0]['quote'])

    def test_liang_retainer_equivalences_keep_two_people_separate(self):
        gui = bundle('2bl_b4d_kfg', include_provisional=True)
        yang = bundle('fo7_9ev_cht', include_provisional=True)
        self.assertIn('2bl_b4d_kfg', gui['person_ids'])
        self.assertIn('fo7_9ev_cht', yang['person_ids'])
        self.assertFalse(set(gui['person_ids']).intersection(yang['person_ids']))
        self.assertIn('le-shiji108-gui', {e['id'] for e in gui['life_events']})
        self.assertIn('le-shiji108-yang', {e['id'] for e in yang['life_events']})

    def test_han_death_year_is_a_life_event_not_title_endpoint(self):
        result = bundle('6hy_i1z_hu2', include_provisional=True)
        event = next(e for e in result['life_events'] if e['id'] == 'le-shiji108-han')
        self.assertEqual(event['normalized_date']['era_year'], 127)
        self.assertEqual(event['normalized_date']['original_quote'], '安國以元朔二年中卒。')
        date = next(d for d in result['date_normalizations'] if d['record_id'] == event['id'])
        self.assertEqual(date['date_role'], 'life_event')
        self.assertNotIn('endpoint', date)
        title = next(h for h in result['title_holdings'] if h['id'] == 'th-shiji108-031')
        self.assertEqual(title['effective_period']['end']['status'], 'unknown')
    def test_unknown_life_event_date_stays_unresolved(self):
        result = bundle('z2v_oh4_mhm')
        event = next(e for e in result['life_events'] if e['id'] == 'le-shiji108-hui')
        self.assertIsNone(event['date_expression'])
        self.assertNotIn('normalized_date', event)
    def test_real_person_has_reverse_relations_and_source_text(self):
        result = bundle('k2p_5ol_dwh')
        self.assertTrue(any(a['object_person_id'] == 'k2p_5ol_dwh' for a in result['relations']))
        self.assertTrue(result['title_holdings'])
        passages = {p['id']: p for p in result['passages']}
        for title in result['title_holdings']:
            for evidence in title['evidence']:
                self.assertEqual(evidence['quote'], passages[evidence['paragraph_id']]['text'])
        self.assertTrue(result['time_policy']['unknown_is_not_unbounded'])

    def test_provisional_equivalence_is_explicit(self):
        exact = bundle('49g_7az_e4i')
        combined = bundle('49g_7az_e4i', include_provisional=True)
        self.assertEqual(exact['person_ids'], ['49g_7az_e4i'])
        self.assertIn('49g_7az_e4i', combined['person_ids'])
        self.assertTrue(combined['equivalence_decisions'])
        self.assertEqual(combined['mentions'], exact['mentions'])
        self.assertTrue(all(d.get('identity_materialized') for d in combined['equivalence_decisions']))
        self.assertGreaterEqual(len({m['chapter_id'] for m in combined['mentions']}), 2)

    def test_materialized_case_keeps_identity_evidence_and_original_passages(self):
        result = bundle('li9_cmb_8ci')
        case = next(c for c in result['resolved_identity_cases'] if c['id'].startswith('u-shiji007-'))
        self.assertEqual(case['person_id'], 'li9_cmb_8ci')
        self.assertEqual(case['status'], 'contextual_provisional')
        self.assertTrue(case['identity_equivalence_decision_ids'])
        self.assertTrue(set(case['paragraph_ids']).issubset({p['id'] for p in result['passages']}))
        self.assertTrue(set(case['identity_equivalence_decision_ids']).issubset({d['id'] for d in result['equivalence_decisions']}))

    def test_unknown_person_rejected(self):
        with self.assertRaises(ValueError):
            bundle('missing')

    def test_birth_order_is_structured_and_keeps_uncertainty(self):
        result = bundle('ao3_0fy_d45_AAA')
        constraints = {c['assertion_id']: c for c in result['birth_order_constraints']}
        eldest = constraints['a-shiji006-005']
        self.assertEqual(eldest['ordinal'], 1)
        self.assertEqual(eldest['scope'], 'sons_of_parent')
        self.assertEqual(eldest['parent_person_id'], 'ao3_0fy_d45_AAA')
        younger = constraints['a-shiji006-006']
        self.assertIsNone(younger['ordinal'])
        self.assertEqual(younger['interpretation_status'], 'ambiguous')
        relative = constraints['a-shiji006-004']
        self.assertEqual(relative['older_person_id'], 'ao3_0fy_d45_AAA')
        self.assertEqual(relative['younger_person_id'], 'r5h_mrk_rov')
        self.assertIsNone(relative['older_ordinal'])
        self.assertIsNone(relative['younger_ordinal'])
        self.assertTrue(relative['evidence'])

    def test_native_place_keeps_source_and_unknown_geography(self):
        result = bundle('cc2_r4q_j5y')
        address = next(a for a in result['address_assertions'] if a['id'] == 'pa-shiji093-001')
        self.assertEqual(address['relation'], 'biographical_origin')
        self.assertEqual(address['place']['source_name'], '豐')
        self.assertIsNone(address['place']['place_id'])
        self.assertIsNone(address['place']['modern_identification'])
        passages = {p['id']: p for p in result['passages']}
        evidence = address['evidence'][0]
        self.assertEqual(evidence['quote'], passages[evidence['paragraph_id']]['text'])

    def test_birth_death_and_burial_places_are_separate(self):
        result = bundle('ao3_0fy_d45_AAA')
        addresses = result['address_assertions']
        received = [a for a in addresses if a['evidence'][0]['chapter_id'] == 'c-shiji-006-shihuang']
        def places(relation):
            return {a['place']['source_name'] for a in received if a['relation'] == relation}
        self.assertEqual(places('birth_place'), {'邯鄲'})
        self.assertEqual(places('death_place'), {'沙丘平臺'})
        self.assertEqual(places('burial_place'), {'酈邑', '酈山'})
        self.assertFalse(places('biographical_origin'))
        other_deaths = [a for a in addresses if a['relation'] == 'death_place'
                        and a['evidence'][0]['chapter_id'] == 'c-shiji-087-lisi']
        self.assertEqual({a['place']['source_name'] for a in other_deaths}, {'沙丘'})
        burials = [a for a in received if a['relation'] == 'burial_place']
        self.assertEqual({e['paragraph_id'] for a in burials for e in a['evidence']},
                         {'c-shiji-006-shihuang:p052', 'c-shiji-006-shihuang:p104'})
        for a in addresses:
            self.assertIsNone(a['place']['modern_identification'])
            self.assertTrue(a['evidence'])

    def test_numeric_year_keeps_source_and_numbering(self):
        from scripts.validate_corpus import normalized_date_errors
        result = bundle('ao3_0fy_d45_AAA')
        dates = result['date_normalizations']
        birth = next(d for d in dates if d['original_quote'] == '以秦昭王四十八年正月生於邯鄲。')
        self.assertEqual(birth['era_year'], 259)
        self.assertEqual(birth['year'], -258)
        deaths = [d for d in dates if d['era_year'] == 210]
        self.assertGreaterEqual(len(deaths), 2)
        self.assertTrue(all(d['year'] == -209 for d in deaths))
        old_death = next(d for d in deaths if d['original_quote'] == '七月丙寅，始皇崩於沙丘平臺。')
        self.assertEqual(len(old_death['evidence']), 2)
        self.assertTrue(any(e['chapter_id'] == 'c-shiji-087-lisi' for d in deaths for e in d['evidence']))
        for date in dates:
            self.assertEqual(normalized_date_errors(date), [])
        wrong = dict(birth, year=-259)
        self.assertTrue(normalized_date_errors(wrong))
        self.assertTrue(normalized_date_errors(dict(birth, year=True)))
        burial = next(a for a in result['address_assertions'] if a['relation'] == 'burial_place')
        self.assertNotIn('normalized_date', burial)

    def test_agnatic_relation_preserves_unknown_distance(self):
        result = bundle('u87_cc1_7vm')
        relations = [a for a in result['relations'] if a.get('discrepancy_group_id') == 'kin-shiji094-tianrong']
        self.assertEqual({a['predicate'] for a in relations}, {'brother', 'agnatic_cousin'})
        cousin = next(a for a in relations if a['predicate'] == 'agnatic_cousin')
        structure = cousin['qualifiers']['kinship_structure']
        self.assertEqual(structure['generation_difference'], 0)
        self.assertEqual(structure['lineage'], 'paternal')
        self.assertIsNone(structure['distance'])
        self.assertIsNone(structure['common_ancestor_person_id'])
        self.assertEqual(cousin['qualifiers']['relative_birth_order']['older_person_id'], 'u87_cc1_7vm')

    def test_source_frequency_counts_only_focus_mentions_and_preserves_ties(self):
        result = bundle('ao3_0fy_d45_AAA', include_provisional=True)
        rows = result['source_mention_summary']
        self.assertEqual(sum(r['mention_count'] for r in rows), len(result['mentions']))
        indexed = {m['id']: m for m in result['mentions']}
        for row in rows:
            self.assertEqual(row['mention_count'], len(row['mention_ids']))
            self.assertEqual(row['passage_count'], len(row['paragraph_ids']))
            self.assertTrue(all(indexed[mid]['chapter_id'] == row['chapter_id'] for mid in row['mention_ids']))
        maximum = max(r['mention_count'] for r in rows)
        self.assertEqual(set(result['most_mentioned_source_ids']), {r['source_id'] for r in rows if r['mention_count'] == maximum})
        self.assertTrue(result['mention_count_policy']['frequency_is_not_authority'])

    def test_family_path_has_direct_source_relation_and_does_not_claim_order(self):
        result = bundle('w8j_vnd_rs4_AAA')
        path = result['family_paths'][0]
        self.assertEqual(path['parent_person_id'], 'w8j_vnd_rs4_AA')
        self.assertEqual(path['connection'], 'father')
        self.assertFalse(path['human_reviewed'])
        self.assertTrue(any(a['predicate'] == 'father' and a['object_person_id'] == path['parent_person_id'] for a in result['relations']))
        self.assertEqual(path['evidence'][0]['source_term'], '子侯偃立')
        self.assertFalse(result['birth_order_constraints'])

    def test_fujin_substitution_is_not_a_dai_office_title(self):
        result = bundle('w8j_vnd_rs4')
        paragraph = next(p for p in result['passages'] if p['id'].endswith(':p003'))
        verb_start = paragraph['text'].index('代丞相')
        self.assertFalse(any(m['start'] == verb_start and m['surface'] == '代丞相' for m in paragraph['mentions']))
        self.assertTrue(any(m['surface'] == '代丞相' and m['start'] > verb_start for m in paragraph['mentions']))

    def test_heqin_proposal_is_not_actual_birth_or_marriage(self):
        from scripts.person_bundle import load_catalog
        catalog = load_catalog()
        people = catalog[0]
        def pid(label):
            return next(k for k, v in people.items() if v['label'] == label + '（劉敬叔孫通列傳候選）')
        modu = '2ev_182_3gg'
        princess = 'yqp_nlb_p1p_AI'
        sent = pid('實遣家人子未名')
        result = bundle(modu, catalog=catalog)
        self.assertNotEqual(princess, sent)
        self.assertTrue(any(a['predicate'] == 'spouse' and a['subject_person_id'] == sent for a in result['relations']))
        self.assertFalse(any(a['predicate'] == 'spouse' and a['subject_person_id'] == princess for a in result['relations']))
        self.assertFalse(any(a['predicate'] == 'father' and a['object_person_id'] == modu for a in result['relations']))
        hypothetical = next(p for p in result['passages'] if p['id'].endswith(':p006'))
        start = hypothetical['text'].index('生子必為太子') + len('生子必為')
        mention = next(m for m in hypothetical['mentions'] if m['start'] == start)
        self.assertEqual(mention['kind'], 'unresolved')
        self.assertIsNone(mention['person_id'])

    def test_ding_mudi_keeps_conflicting_commentaries_with_editorial_default(self):
        from scripts.person_bundle import load_catalog
        catalog = load_catalog()
        ding = next(k for k, v in catalog[0].items() if v['label'] == '丁公（季布欒布列傳候選）')
        result = bundle(ding, catalog=catalog)
        case = result['kinship_interpretation_cases'][0]
        self.assertEqual(case['default_alternative_id'], 'shigu-maternal-half-brother')
        self.assertEqual(case['selection']['confidence_level'], 'moderate')
        self.assertTrue(any(a['predicate'] == 'brother' and a['status'] == 'editorial_preferred' for a in result['preferred_relations']))
        order = result['preferred_birth_order_constraints'][0]
        self.assertEqual(order['younger_person_id'], ding)
        self.assertIsNone(order['younger_ordinal'])
        alternatives = {a['predicate']: a for a in case['alternatives']}
        self.assertEqual(set(alternatives), {'maternal_uncle', 'brother'})
        self.assertEqual(alternatives['maternal_uncle']['qualifiers']['object_generation_relative_to_subject'], -1)
        self.assertFalse(alternatives['brother']['qualifiers']['shared_father'])
        self.assertFalse(result['family_paths'])
        self.assertFalse(result['relations'])

    def test_jibu_direct_children_use_paths_without_inventing_sibling_parent(self):
        from scripts.person_bundle import load_catalog
        catalog = load_catalog()
        for child in ('766_5dq_zws_A', 'jx9_cov_qe0_A'):
            result = bundle(child, catalog=catalog)
            path = result['family_paths'][0]
            self.assertEqual(path['parent_person_id'], child[:11])
            self.assertTrue(any(a['predicate'] == 'father' and a['subject_person_id'] == child
                                and a['object_person_id'] == child[:11] for a in result['relations']))
            self.assertFalse(result['birth_order_constraints'])
        xin = next(k for k, v in catalog[0].items() if v['label'] == '季心（季布欒布列傳候選）')
        result = bundle(xin, catalog=catalog)
        self.assertFalse(result['family_paths'])
        self.assertFalse(any(a['predicate'] == 'father' for a in result['relations']))
        self.assertEqual(result['reported_variants'][0]['reported_reading'], '子')
        self.assertFalse(result['reported_variants'][0]['adopted'])

    def test_retired_hyphen_id_is_rejected_and_current_family_id_remains(self):
        with self.assertRaises(ValueError):
            bundle('w8j_vnd_rs4-AAA')
        new = bundle('w8j_vnd_rs4_AAA')
        self.assertEqual(new['family_paths'][0]['parent_person_id'], 'w8j_vnd_rs4_AA')

    def test_missing_generation_bundle_keeps_source_without_father_person(self):
        from scripts.person_bundle import load_catalog
        catalog = load_catalog()
        person = next(p for p in catalog[0].values() if p.get('family_path', {}).get('generation_distance') == 2)
        result = bundle(person['id'], catalog=catalog)
        path = result['family_paths'][0]
        self.assertIn('*', person['id'])
        self.assertIsNone(path['parent_person_id'])
        self.assertEqual(path['intermediate_person_ids'], [None])
        self.assertNotIn(person['id'][:-1], catalog[0])
        self.assertTrue(any(a['predicate'] == 'grandfather' and a['object_person_id'] == path['ancestor_person_id']
                            for a in result['relations']))

    def test_retired_sequential_id_is_rejected_without_losing_current_person(self):
        with self.assertRaises(ValueError):
            bundle('cbr-p000533')
        result = bundle('ao3_0fy_d45_AAA')
        self.assertTrue(any(p['label'] == '秦始皇帝' for p in result['persons']))

    def test_export_retires_legacy_urls_and_keeps_collapsible_monospace_index(self):
        import json
        import re
        from scripts.person_bundle import ROOT, load_catalog
        catalog = load_catalog()
        folder = ROOT / 'exports/persons'
        index = json.loads((folder / 'index.json').read_text())
        ids = [p['person_id'] for p in index['persons']]
        from scripts.family_assemblies import load_assemblies
        source_map, assembled = load_assemblies(ROOT, catalog)
        self.assertEqual(set(ids), (set(catalog[0]) - set(source_map)) | set(assembled))
        self.assertEqual(len(ids), len(set(ids)))
        self.assertFalse(set(ids).intersection(index['id_aliases']))
        self.assertTrue(all((folder / (old + '.json')).exists() for old in index['id_aliases']))
        self.assertFalse((folder / 'cbr-p000533.json').exists())
        self.assertFalse((folder / 'w8j_vnd_rs4-AAA.json').exists())
        self.assertTrue((folder / 'ao3_0fy_d45_AAA.json').exists())
        family_text = (folder / 'README.md').read_text()
        self.assertIn('[獨立人物索引](unconnected.md)', family_text)
        single_text = (folder / 'unconnected.md').read_text()
        self.assertIn('[可展開家族索引](README.md)', single_text)
        pages = index['reading_indexes']['family_pages'] + index['reading_indexes']['unconnected_pages']
        self.assertEqual(pages[0], 'README.md')
        self.assertEqual(index['reading_indexes']['unconnected_pages'][0], 'unconnected.md')
        self.assertEqual(len(pages), len(set(pages)))
        page_texts = [(folder / filename).read_text() for filename in pages]
        for page in page_texts:
            self.assertLess(len(page.encode('utf-8')), 500_000)
            source_refs = set(re.findall(r'\[《[^]]+》\]\[(\d+)\]', page))
            definitions = set(re.findall(r'^\[(\d+)\]: https://', page, re.M))
            self.assertTrue(source_refs.issubset(definitions))
        text = '\n'.join(page_texts)
        extra = next(row for row in index['persons'] if row['person_id'] == '5dd_l1c_6g8_C')
        self.assertEqual(extra['preferred_parent_status'], 'unresolved')
        self.assertIn('ft-shiji-wei-extra-son', extra['parent_decision_ids'])
        self.assertIn('衛青子宜春侯（來源候選；預設不接父系）', text)
        from urllib.parse import unquote
        table_ids = [unquote(filename) for filename in re.findall(r'\[JSON\]\(([^)]+)\.json\)', text)]
        self.assertEqual(set(table_ids), set(ids))
        self.assertEqual(len(table_ids), len(ids))
        self.assertGreater(text.count('<details>'), 0)
        self.assertEqual(text.count('<details>'), text.count('</details>'))
        self.assertIn('%2A', text)
        source_refs = set(re.findall(r'\[《[^]]+》\]\[(\d+)\]', text))
        definitions = set(re.findall(r'^\[(\d+)\]: https://', text, re.M))
        self.assertTrue(source_refs)
        self.assertTrue(source_refs.issubset(definitions))

    def test_reading_pagination_preserves_multibyte_rows_sources_and_removes_stale_pages(self):
        import tempfile
        from pathlib import Path
        from scripts.export_person_bundles import table_blocks, write_reading_pages
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            rows = [f'| `test_{i}` | 測試人物 | [《測試來源》][1] | [JSON](test_{i}.json) |' for i in range(7000)]
            references = ['[1]: https://example.org/source', '[2]: https://example.org/unused']
            pages = write_reading_pages(folder, 'unconnected.md', 'unconnected', '# 測試', '合成人物，並非史料。', table_blocks(rows), references)
            self.assertGreater(len(pages), 1)
            text = '\n'.join((folder / filename).read_text() for filename in pages)
            for row in rows:
                self.assertEqual(text.count(row + '\n'), 1)
            for filename in pages:
                page = (folder / filename).read_text()
                self.assertLess(len(page.encode('utf-8')), 500_000)
                self.assertIn('[1]: https://example.org/source', page)
                self.assertNotIn('[2]: https://example.org/unused', page)
                for other in pages:
                    self.assertIn(f']({other})', page)
            (folder / 'unconnected-notes.md').write_text('保留手寫檔案')
            write_reading_pages(folder, 'unconnected.md', 'unconnected', '# 測試', '', table_blocks(rows[:1]), references)
            self.assertTrue((folder / 'unconnected-notes.md').exists())
            self.assertTrue(all(not (folder / filename).exists() for filename in pages[1:]))

    def test_preferred_tree_selects_zhaozis_son_without_discarding_other_sources(self):
        from scripts.person_bundle import load_catalog
        catalog = load_catalog()
        pid = 'y97_huh_vuz_AAAAAAAAAAAAABAAA'
        result = bundle(pid, catalog=catalog)
        fathers = [a for a in result['relations'] if a['subject_person_id'] == pid and a['predicate'] == 'father']
        self.assertEqual(len(fathers), 2)
        selected = [a for a in result['preferred_relations'] if a['subject_person_id'] == pid and a['predicate'] == 'father']
        self.assertEqual([a['id'] for a in selected], ['a-shiji006-029'])
        self.assertEqual(result['family_paths'][0]['parent_person_id'], selected[0]['object_person_id'])
        self.assertTrue(result['family_tree_decisions'])

    def test_preferred_tree_does_not_treat_taguang_allegation_as_verified_birth(self):
        from scripts.person_bundle import load_catalog
        catalog = load_catalog()
        decision = next(d for record in catalog[1] if record.get('record_type') == 'family_tree_decision_set'
                        for d in record['decisions'] if d['id'] == 'ft-shiji-parent-taguang')
        result = bundle(decision['subject_person_id'], catalog=catalog)
        self.assertTrue(any(a['predicate'] == 'father' for a in result['relations']))
        self.assertFalse(any(a['predicate'] == 'father' and a['subject_person_id'] == decision['subject_person_id']
                             for a in result['preferred_relations']))
        self.assertIsNone(decision['preferred_parent_person_id'])

    def test_chuyou_preferred_royal_parentage_is_not_asserted_biological_birth(self):
        from scripts.person_bundle import load_catalog
        catalog = load_catalog()
        result = bundle('k5z_d58_n7p_A', catalog=catalog, include_provisional=True)
        royal = next(a for a in result['preferred_relations'] if a['id'] == 'a-shiji040-080')
        self.assertEqual(royal['qualifiers']['parentage_role'], 'legal_or_dynastic')
        self.assertEqual(royal['qualifiers']['biological_parent_status'], 'unknown')
        self.assertFalse(any(a['id'] == 'a-shiji078-004' for a in result['preferred_relations']))
        self.assertTrue(any(a['id'] == 'a-shiji078-004' for a in result['relations']))
    def test_yuan_si_brings_biography_titles_and_source_dates(self):
        result = bundle('j32_wtj_khz_A', include_provisional=True)
        self.assertTrue(any(m['surface'] == '絲' and m['chapter_id'] == 'c-shiji-101-yuanchao' for m in result['mentions']))
        dates = [d for d in result['date_normalizations'] if d.get('title') in ('太常', '楚相')]
        self.assertEqual({d['title'] for d in dates}, {'太常', '楚相'})
        self.assertTrue(all(d['era'] == 'BCE' and d['era_year'] == 154 and d['year'] == -153 for d in dates))
        passages = {p['id'] for p in result['passages']}
        self.assertTrue(all(e['paragraph_id'] in passages for d in dates for e in d['evidence']))
        self.assertTrue(all(d['endpoint'] == 'start' for d in dates))
        self.assertTrue(all(h['effective_period']['end']['status'] == 'unknown' for h in result['title_holdings'] if h['title'] == '太常'))

    def test_yuanchao_nephew_and_heir_do_not_invent_birth_order(self):
        from scripts.person_bundle import load_catalog
        catalog = load_catalog()
        people = {p['label']: p for p in catalog[0].values()}
        nephew = people['種（袁盎兄子）（袁盎鼂錯列傳候選）']
        result = bundle(nephew['id'], catalog=catalog)
        relation = next(a for a in result['relations'] if a['subject_person_id'] == nephew['id'])
        self.assertEqual(relation['predicate'], 'paternal_uncle')
        self.assertIsNone(relation['qualifiers']['intermediate_father_person_id'])
        self.assertFalse(any(a['predicate'] == 'father' for a in result['relations']))
        heir = catalog[0]['qbh_lsz_ipx']
        child = bundle(heir['id'], catalog=catalog)
        relation = next(a for a in child['relations'] if a['subject_person_id'] == heir['id'] and a['predicate'] == 'father')
        self.assertEqual(relation['qualifiers']['heir_status'], '太子')
        self.assertIsNone(relation['qualifiers']['birth_ordinal'])
        self.assertNotIn('birth_order', relation['qualifiers'])
        chapter = next(p for p in result['sources'] if p['chapter_id'] == 'c-shiji-101-yuanchao')
        self.assertFalse(chapter['source']['image_verified'])

    def test_zhangfeng_denied_appointment_and_rank_loss_do_not_create_tenure(self):
        from scripts.person_bundle import load_catalog
        catalog = load_catalog()
        people = {p['label']: p for p in catalog[0].values()}
        keeper = people['虎圈嗇夫未名（張釋之馮唐列傳候選）']
        result = bundle(keeper['id'], catalog=catalog)
        self.assertFalse(any(h['title'] == '上林令' for h in result['title_holdings']))
        wei = people['魏尚（張釋之馮唐列傳候選）']
        result = bundle(wei['id'], catalog=catalog)
        holdings = [h for h in result['title_holdings'] if h['title'] == '雲中守']
        self.assertEqual({h['mode'] for h in holdings}, {'attestation', 'grant'})
        self.assertTrue(all(h['effective_period']['end']['status'] == 'unknown' for h in holdings))

    def test_feng_family_origin_and_accession_date_keep_source_subjects(self):
        from scripts.person_bundle import load_catalog
        catalog = load_catalog()
        people = {p['label']: p for p in catalog[0].values()}
        tang = people['馮唐（張釋之馮唐列傳候選）']
        father = people['馮唐父未名（張釋之馮唐列傳候選）']
        grandfather = people['馮唐祖父未名（張釋之馮唐列傳候選）']
        self.assertEqual(tang['family_path']['parent_person_id'], father['id'])
        self.assertEqual(father['family_path']['parent_person_id'], grandfather['id'])
        result = bundle(tang['id'], catalog=catalog)
        self.assertFalse(any(a['place']['source_name'] == '趙' for a in result['address_assertions']))
        dates = [d for d in result['date_normalizations'] if d.get('title') == '楚相']
        self.assertEqual(len(dates), 1)
        self.assertEqual((dates[0]['era_year'], dates[0]['year']), (157, -156))
        self.assertIn('七年，景帝立', dates[0]['original_quote'])
        holding = next(h for h in result['title_holdings'] if h['title'] == '楚相')
        self.assertNotIn('normalized_date', holding['effective_period']['end'])

    def test_zhang_hui_honorific_is_separate_and_received_text_is_preserved(self):
        result = bundle('epn_7nx_g1b')
        self.assertEqual([m['surface'] for m in result['mentions']], ['張恢'])
        holding = next(h for h in result['title_holdings'] if h['title'] == '先')
        self.assertEqual(holding['kind'], 'honorific')
        self.assertTrue(any('張恢先所' in p['text'] for p in result['passages']))

    def test_zhou_ren_ancestral_place_is_not_personal_origin(self):
        from scripts.person_bundle import load_catalog
        catalog = load_catalog()
        person = next(p for p in catalog[0].values() if p['label'] == '周仁（萬石張叔列傳候選）')
        result = bundle(person['id'], catalog=catalog)
        ancestral = next(a for a in result['address_assertions'] if a['place']['source_name'] == '任城')
        self.assertEqual(ancestral['relation'], 'ancestral_origin')
        self.assertEqual(ancestral['qualifiers']['subject_scope'], 'ancestors_unspecified')
        self.assertIsNone(ancestral['qualifiers']['ancestor_person_id'])
        self.assertFalse(any(a['relation'] in ('native_place', 'biographical_origin') and a['place']['source_name'] == '任城' for a in result['address_assertions']))

    def test_tian_ren_younger_son_does_not_invent_ordinal_or_death_endpoint(self):
        from scripts.person_bundle import load_catalog
        catalog = load_catalog()
        people = {p['label']: p for p in catalog[0].values()}
        ren = people['田仁（田叔列傳候選）']
        shu = catalog[0]['6bn_yfc_lzi']
        result = bundle(ren['id'], catalog=catalog)
        self.assertEqual(ren['family_path']['parent_person_id'], shu['id'])
        order = next(c for c in result['birth_order_constraints'] if c['assertion_id'] == 'a-shiji104-001')
        self.assertIsNone(order['ordinal'])
        self.assertEqual(order['position'], 'younger_or_youngest')
        self.assertTrue(all(h['effective_period']['end']['status'] == 'unknown' for h in result['title_holdings'] if h['title'] in ('司直', '丞相司直')))
        layers = {p['text_layer'] for p in result['passages']}
        self.assertIn('received_chapter', layers)
        self.assertIn('witness_appended_chu_note', layers)

    def test_ren_an_short_name_excludes_changan_and_origin_remains_sourced(self):
        from scripts.person_bundle import load_catalog
        catalog = load_catalog()
        person = next(p for p in catalog[0].values() if p['label'] == '任安（田叔列傳候選）')
        result = bundle(person['id'], catalog=catalog)
        self.assertFalse(any(m['paragraph_id'].endswith(':p010') and m['start'] == 41 for m in result['mentions']))
        origin = next(a for a in result['address_assertions'] if a['relation'] == 'native_place')
        self.assertEqual(origin['place']['source_name'], '滎陽')
        self.assertIsNone(origin['place']['modern_identification'])

    def test_usage_year_includes_earlier_chronological_context(self):
        result = bundle('284_zc9_6fx')
        passages = {p['id']: p for p in result['passages']}
        self.assertIn('c-shiji-107-weiqi:p019', passages)
        h = next(h for h in result['title_holdings'] if h['title'] == '主爵都尉')
        for evidence in h['attestations'][0]['normalized_date']['evidence']:
            self.assertEqual(evidence['quote'], passages[evidence['paragraph_id']]['text'])
        self.assertEqual(h['effective_period']['start']['status'], 'unknown')

    def test_unresolved_dowager_is_available_without_identity_merge(self):
        for pid in ('6d6_eg1_o3a_A', 'l26_mjw_rwe'):
            result = bundle(pid, include_provisional=True)
            case = next(c for c in result['unresolved_identity_cases'] if c['id'].startswith('u-shiji107-'))
            self.assertEqual(set(case['candidate_person_ids']), {'6d6_eg1_o3a_A', 'l26_mjw_rwe'})
            self.assertIn(pid, result['person_ids'])
            other = 'l26_mjw_rwe' if pid == '6d6_eg1_o3a_A' else '6d6_eg1_o3a_A'
            self.assertNotIn(other, result['person_ids'])
            passages = {p['id']: p for p in result['passages']}
            self.assertTrue(all(p in passages for p in case['paragraph_ids']))
            self.assertTrue(any(m['kind'] == 'unresolved' for m in passages['c-shiji-107-weiqi:p007']['mentions']))

    def test_usage_date_summary_does_not_claim_accession(self):
        result = bundle('7mz_d13_9ka_AA')
        date = next(d for d in result['date_normalizations'] if d.get('date_role') == 'attestation')
        self.assertEqual(date['era_year'], 126)
        self.assertNotIn('endpoint', date)
        self.assertEqual(result['title_holdings'][0]['effective_period']['start']['date_expression'], '其春')
