import unittest
from scripts.person_bundle import bundle


class PersonBundleTests(unittest.TestCase):
    def test_real_person_has_reverse_relations_and_source_text(self):
        result = bundle('fd2_w60_h42')
        self.assertTrue(any(a['object_person_id'] == 'fd2_w60_h42' for a in result['relations']))
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
        self.assertIn('5ok_joj_etv', combined['person_ids'])
        self.assertTrue(combined['equivalence_decisions'])
        self.assertGreater(len(combined['mentions']), len(exact['mentions']))

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
        result = bundle('jjl_irg_zke_A')
        address = result['address_assertions'][0]
        self.assertEqual(address['relation'], 'biographical_origin')
        self.assertEqual(address['place']['source_name'], '豐')
        self.assertIsNone(address['place']['place_id'])
        self.assertIsNone(address['place']['modern_identification'])
        passages = {p['id']: p for p in result['passages']}
        evidence = address['evidence'][0]
        self.assertEqual(evidence['quote'], passages[evidence['paragraph_id']]['text'])

    def test_birth_death_and_burial_places_are_separate(self):
        result = bundle('ao3_0fy_d45_AAA')
        addresses = {a['relation']: a for a in result['address_assertions']}
        self.assertEqual(addresses['birth_place']['place']['source_name'], '邯鄲')
        self.assertEqual(addresses['death_place']['place']['source_name'], '沙丘平臺')
        self.assertEqual(addresses['burial_place']['place']['source_name'], '酈邑')
        self.assertNotIn('biographical_origin', addresses)
        for a in addresses.values():
            self.assertIsNone(a['place']['modern_identification'])
            self.assertTrue(a['evidence'])

    def test_numeric_year_keeps_source_and_numbering(self):
        from scripts.validate_corpus import normalized_date_errors
        result = bundle('ao3_0fy_d45_AAA')
        dates = {d['era_year']: d for d in result['date_normalizations']}
        self.assertEqual(dates[259]['year'], -258)
        self.assertEqual(dates[210]['year'], -209)
        self.assertEqual(dates[259]['original_quote'], '以秦昭王四十八年正月生於邯鄲。')
        self.assertEqual(len(dates[210]['evidence']), 2)
        for date in dates.values():
            self.assertEqual(normalized_date_errors(date), [])
        wrong = dict(dates[259], year=-259)
        self.assertTrue(normalized_date_errors(wrong))
        self.assertTrue(normalized_date_errors(dict(dates[259], year=True)))
        burial = next(a for a in result['address_assertions'] if a['relation'] == 'burial_place')
        self.assertNotIn('normalized_date', burial)

    def test_agnatic_relation_preserves_unknown_distance(self):
        result = bundle('j80_2bm_4af')
        relations = [a for a in result['relations'] if a.get('discrepancy_group_id') == 'kin-shiji094-tianrong']
        self.assertEqual({a['predicate'] for a in relations}, {'brother', 'agnatic_cousin'})
        cousin = next(a for a in relations if a['predicate'] == 'agnatic_cousin')
        structure = cousin['qualifiers']['kinship_structure']
        self.assertEqual(structure['generation_difference'], 0)
        self.assertEqual(structure['lineage'], 'paternal')
        self.assertIsNone(structure['distance'])
        self.assertIsNone(structure['common_ancestor_person_id'])
        self.assertEqual(cousin['qualifiers']['relative_birth_order']['older_person_id'], 'j80_2bm_4af')

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
        modu = pid('冒頓')
        princess = pid('呂后女未名')
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

    def test_published_hyphen_id_resolves_without_duplicate_person(self):
        from scripts.person_bundle import load_catalog
        catalog = load_catalog()
        old = bundle('w8j_vnd_rs4-AAA', catalog=catalog)
        new = bundle('w8j_vnd_rs4_AAA', catalog=catalog)
        self.assertEqual(old['requested_person_id'], 'w8j_vnd_rs4-AAA')
        self.assertEqual(old['canonical_person_id'], 'w8j_vnd_rs4_AAA')
        self.assertEqual(old['person_ids'], new['person_ids'])
        self.assertEqual(old['mentions'], new['mentions'])
        self.assertEqual(old['relations'], new['relations'])
        self.assertNotIn('w8j_vnd_rs4-AAA', catalog[0])
        self.assertEqual(old['family_paths'][0]['parent_person_id'], 'w8j_vnd_rs4_AA')

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

    def test_old_sequential_id_resolves_to_new_family_id(self):
        result = bundle('cbr-p000533')
        self.assertEqual(result['requested_person_id'], 'cbr-p000533')
        self.assertNotEqual(result['canonical_person_id'], 'cbr-p000533')
        self.assertIn('cbr-p000533', result['id_aliases'])
        self.assertTrue(any(p['label'] == '秦始皇帝' for p in result['persons']))

    def test_export_keeps_legacy_urls_and_collapsible_monospace_index(self):
        import json
        import re
        from scripts.person_bundle import ROOT, load_catalog
        catalog = load_catalog()
        folder = ROOT / 'exports/persons'
        index = json.loads((folder / 'index.json').read_text())
        ids = [p['person_id'] for p in index['persons']]
        self.assertEqual(set(ids), set(catalog[0]))
        self.assertEqual(len(ids), len(set(ids)))
        self.assertFalse(set(ids).intersection(index['id_aliases']))
        self.assertTrue(all((folder / (old + '.json')).exists() for old in index['id_aliases']))
        old = json.loads((folder / 'cbr-p000533.json').read_text())
        new = json.loads((folder / (old['canonical_person_id'] + '.json')).read_text())
        self.assertEqual(old['mentions'], new['mentions'])
        self.assertEqual(old['relations'], new['relations'])
        text = (folder / 'README.md').read_text()
        table_ids = re.findall(r'\| `([^`]+)` \|', text)
        self.assertEqual(set(table_ids), set(ids))
        self.assertEqual(len(table_ids), len(ids))
        self.assertGreater(text.count('<details>'), 0)
        self.assertEqual(text.count('<details>'), text.count('</details>'))
        self.assertIn('%2A', text)

    def test_preferred_tree_selects_zhaozis_son_without_discarding_other_sources(self):
        from scripts.person_bundle import load_catalog
        catalog = load_catalog()
        pid = next(p['id'] for p in catalog[0].values() if 'cbr-p000442' in p.get('id_aliases', []))
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
