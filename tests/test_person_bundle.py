import unittest
from scripts.person_bundle import bundle


class PersonBundleTests(unittest.TestCase):
    def test_real_person_has_reverse_relations_and_source_text(self):
        result = bundle('cbr-p004938')
        self.assertTrue(any(a['object_person_id'] == 'cbr-p004938' for a in result['relations']))
        self.assertTrue(result['title_holdings'])
        passages = {p['id']: p for p in result['passages']}
        for title in result['title_holdings']:
            for evidence in title['evidence']:
                self.assertEqual(evidence['quote'], passages[evidence['paragraph_id']]['text'])
        self.assertTrue(result['time_policy']['unknown_is_not_unbounded'])

    def test_provisional_equivalence_is_explicit(self):
        exact = bundle('cbr-p000537')
        combined = bundle('cbr-p000537', include_provisional=True)
        self.assertEqual(exact['person_ids'], ['cbr-p000537'])
        self.assertIn('cbr-p004868', combined['person_ids'])
        self.assertTrue(combined['equivalence_decisions'])
        self.assertGreater(len(combined['mentions']), len(exact['mentions']))

    def test_unknown_person_rejected(self):
        with self.assertRaises(ValueError):
            bundle('missing')

    def test_birth_order_is_structured_and_keeps_uncertainty(self):
        result = bundle('cbr-p000533')
        constraints = {c['assertion_id']: c for c in result['birth_order_constraints']}
        eldest = constraints['a-shiji006-005']
        self.assertEqual(eldest['ordinal'], 1)
        self.assertEqual(eldest['scope'], 'sons_of_parent')
        self.assertEqual(eldest['parent_person_id'], 'cbr-p000533')
        younger = constraints['a-shiji006-006']
        self.assertIsNone(younger['ordinal'])
        self.assertEqual(younger['interpretation_status'], 'ambiguous')
        relative = constraints['a-shiji006-004']
        self.assertEqual(relative['older_person_id'], 'cbr-p000533')
        self.assertEqual(relative['younger_person_id'], 'cbr-p000543')
        self.assertIsNone(relative['older_ordinal'])
        self.assertIsNone(relative['younger_ordinal'])
        self.assertTrue(relative['evidence'])

    def test_native_place_keeps_source_and_unknown_geography(self):
        result = bundle('cbr-p005166')
        address = result['address_assertions'][0]
        self.assertEqual(address['relation'], 'biographical_origin')
        self.assertEqual(address['place']['source_name'], '豐')
        self.assertIsNone(address['place']['place_id'])
        self.assertIsNone(address['place']['modern_identification'])
        passages = {p['id']: p for p in result['passages']}
        evidence = address['evidence'][0]
        self.assertEqual(evidence['quote'], passages[evidence['paragraph_id']]['text'])

    def test_birth_death_and_burial_places_are_separate(self):
        result = bundle('cbr-p000533')
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
        result = bundle('cbr-p000533')
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
        result = bundle('cbr-p005225')
        relations = [a for a in result['relations'] if a.get('discrepancy_group_id') == 'kin-shiji094-tianrong']
        self.assertEqual({a['predicate'] for a in relations}, {'brother', 'agnatic_cousin'})
        cousin = next(a for a in relations if a['predicate'] == 'agnatic_cousin')
        structure = cousin['qualifiers']['kinship_structure']
        self.assertEqual(structure['generation_difference'], 0)
        self.assertEqual(structure['lineage'], 'paternal')
        self.assertIsNone(structure['distance'])
        self.assertIsNone(structure['common_ancestor_person_id'])
        self.assertEqual(cousin['qualifiers']['relative_birth_order']['older_person_id'], 'cbr-p005225')

    def test_source_frequency_counts_only_focus_mentions_and_preserves_ties(self):
        result = bundle('cbr-p000533', include_provisional=True)
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
        result = bundle('w8j_vnd_rs4-AAA')
        path = result['family_paths'][0]
        self.assertEqual(path['parent_person_id'], 'w8j_vnd_rs4-AA')
        self.assertEqual(path['connection'], 'father')
        self.assertFalse(path['human_reviewed'])
        self.assertTrue(any(a['predicate'] == 'father' and a['object_person_id'] == path['parent_person_id'] for a in result['relations']))
        self.assertEqual(path['evidence'][0]['source_term'], '子侯偃立')
        self.assertFalse(result['birth_order_constraints'])

    def test_fujin_substitution_is_not_a_dai_office_title(self):
        result = bundle('w8j_vnd_rs4-')
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
