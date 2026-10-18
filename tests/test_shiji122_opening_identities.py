# coding: utf-8
import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class OpeningIdentityTests(unittest.TestCase):
 def test_all_35_original_spans_target_the_reviewed_identity(self):
  fixture=json.loads((ROOT/'tests/fixtures/shiji122-opening-identities.json').read_text());chapter=json.loads((ROOT/'corpus/shiji/122.json').read_text());ps={p['id']:p for p in chapter['paragraphs']}
  self.assertEqual(len(fixture['mentions']),35)
  for row in fixture['mentions']:
   p=ps[row['paragraph_id']];m=next(m for m in p['mentions'] if m['id']==row['marker']['id']);self.assertEqual(p['text'],row['text']);self.assertEqual(m,row['marker']);self.assertEqual(p['text'][m['start']:m['end']],m['surface'])
 def test_retired_candidates_have_no_live_source_references_or_public_files(self):
  fixture=json.loads((ROOT/'tests/fixtures/shiji122-opening-identities.json').read_text());ids=set(fixture['mapping'])
  people=json.loads((ROOT/'registry/persons.json').read_text())['persons'];self.assertFalse(ids&{p['id'] for p in people})
  for folder in ['corpus','registry','data/corpus','exports']:
   for p in (ROOT/folder).rglob('*'):
    if p.is_file() and p.suffix in ['.json','.xml','.md']:
     text=p.read_text();self.assertFalse(any(old in text for old in ids),str(p))
 def test_two_zhou_yafu_forms_share_source_preserving_office_records(self):
  titles=json.loads((ROOT/'corpus/shiji/122-titles.json').read_text())
  rows=[h for h in titles['holdings'] if h['person_id']=='koy_6jg_gcc_C'];self.assertGreaterEqual(len(rows),3)
