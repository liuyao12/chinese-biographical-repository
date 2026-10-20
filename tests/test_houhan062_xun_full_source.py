"""Portable source invariants; no private packet or temporary directory inputs."""
from pathlib import Path
import json,hashlib,unittest
from scripts.reading_layout import validate_chapter
from scripts.occurrence_concordance import occurrence_catalog
ROOT=Path(__file__).resolve().parents[1]
FIX=json.loads((ROOT/'tests/fixtures/houhan062-xun-full-source.json').read_text())
class Houhan062XunFullSource(unittest.TestCase):
 def chapter(self):return json.loads((ROOT/'corpus/houhanshu/062.json').read_text())
 def test_all_70_complete_fixed_units(self):
  c=self.chapter();by={p['id']:p for p in c['paragraphs']}
  for pid,sha in FIX['text_sha256'].items():self.assertEqual(hashlib.sha256(by[pid]['text'].encode()).hexdigest(),sha)
 def test_three_historical_objects_exact(self):
  c=self.chapter()
  for p in FIX['old_three']:self.assertIn(p,c['paragraphs'])
 def test_dynamic_full_partition_and_archival_ranges(self):
  c=self.chapter();validate_chapter(c,ROOT);layout=c['reading_layout'];self.assertTrue(set(FIX['text_sha256'])<=set(layout['primary_paragraph_ids']));self.assertTrue({p['id']for p in FIX['old_three']}<={a['paragraph_id']for a in layout['archival_excerpts']})
 def test_30_old_anchors_same_fixed_occurrences(self):
  c=self.chapter();con=json.loads((ROOT/c['reading_layout']['concordance_path']).read_text());aliases,_=occurrence_catalog(ROOT,[c,con]);self.assertEqual(set(aliases),{m['id']for p in FIX['old_three']for m in p['mentions']})
 def test_all_recorded_mentions_survive(self):
  c=self.chapter();actual={m['id']:m for p in c['paragraphs']for m in p['mentions']}
  for m in FIX['mentions']:
   self.assertIn(m['id'],actual)
   for key in ('start','end','surface','kind'):self.assertEqual(actual[m['id']][key],m[key])
 def test_prior_native_annotations_preserved(self):
  c=self.chapter()
  for key,rows in FIX['prior_annotation_lists'].items():
   self.assertTrue(all(row in c['annotation'].get(key,[])for row in rows),key)
if __name__=='__main__':unittest.main()
