# coding: utf-8
"""年表人物介面的來源覆蓋及機讀約束。"""
import json
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
class TablePersonProfilesTests(unittest.TestCase):
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
