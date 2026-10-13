# coding: utf-8
"""年表人物介面的來源覆蓋及機讀約束。"""
import json
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
class TablePersonProfilesTests(unittest.TestCase):
    def test_profiles_follow_current_registry_and_index_not_stale_export_files(self):
        registry = json.loads((ROOT/'data/corpus/persons.json').read_text())
        bundles = json.loads((ROOT/'exports/persons/index.json').read_text())
        candidates = json.loads((ROOT/'data/historical-tables/person-candidates.json').read_text())['persons']
        expected = set(registry) | {p['person_id'] for p in bundles['persons']} | {p['id'] for p in candidates}
        profiles = {p.stem for p in (ROOT/'data/corpus/profiles').glob('*.json') if p.stem != 'index'}
        self.assertEqual(profiles, expected)
        for pid in registry:
            profile = json.loads((ROOT/'data/corpus/profiles'/f'{pid}.json').read_text())
            for relation in profile.get('preferred_relations', []):
                if relation['predicate'] in {'father','mother','spouse','son','daughter','grandfather','great_grandfather'}:
                    self.assertIn(relation['subject_person_id'], profiles)
                    self.assertIn(relation['object_person_id'], profiles)
    def test_every_marked_person_has_a_local_profile_and_index_entry(self):
        index=json.loads((ROOT/'data/corpus/profiles/index.json').read_text())
        profiles={p['id']:p for p in index['profiles']}
        table=json.loads((ROOT/'data/historical-tables/shiji-015.json').read_text())
        for fragment in table['fragments']:
            for row in fragment['rows']:
                for cell in row['cells']:
                    for m in cell['person_mentions']:
                        record=json.loads((ROOT/profiles[m['person_id']]['path']).read_text())
                        self.assertEqual(record['id'],m['person_id'])
                        self.assertTrue(any(x['cell_id']==cell['id'] and x['quote']==cell['text'] for x in record['table_occurrences']))
    def test_source_local_candidates_preserve_evidence_and_do_not_invent_cross_chapter_matches(self):
        candidates=json.loads((ROOT/'data/historical-tables/person-candidates.json').read_text())['persons']
        for p in candidates:
            record=json.loads((ROOT/'data/corpus/profiles'/f'{p["id"]}.json').read_text())
            self.assertEqual(record['review'],'source_local_candidate')
            self.assertEqual(record['occurrences'],[])
            self.assertEqual(record['titles'],[])
            self.assertEqual(record['relations'],[])
            self.assertTrue(record['table_occurrences'])
    def test_zhang_yi_links_actual_cross_chapter_passages(self):
        profile=json.loads((ROOT/'data/corpus/profiles/uq6_74z_vtv.json').read_text())
        occurrences=profile['occurrences'];self.assertTrue({5,40,70}.issubset({p['number'] for p in occurrences}))
        for entry in occurrences:
            chapter=json.loads((ROOT/'data/corpus/shiji'/f'{entry["number"]:03}.json').read_text())
            paragraph=next(p for p in chapter['paragraphs'] if p['id']==entry['paragraph_id'])
            self.assertIn(entry['quote'],paragraph['text'])

    def test_reader_retains_commentary_provenance_without_adopting_readings(self):
        for pid in ('jb2_tak_5p8', 'lap_qc0_yqm', 'puu_6hs_m4f'):
            bundle=json.loads((ROOT/'exports/persons'/f'{pid}.json').read_text())
            profile=json.loads((ROOT/'data/corpus/profiles'/f'{pid}.json').read_text())
            self.assertTrue(bundle['reported_variants'])
            self.assertEqual(profile['reported_variants'],bundle['reported_variants'])
            for variant in profile['reported_variants']:
                self.assertFalse(variant['adopted'])
                self.assertEqual(variant['status'],'reported_not_collated')
                self.assertIn('oldid=2514755',variant['url'])
                self.assertTrue(variant['commentator'])
