"""Source identity regressions: same people across chapters, homonyms distinct."""
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(path):return json.loads((ROOT/path).read_text())
class MinistersIdentity(unittest.TestCase):
 def setUp(self):
  self.base=read('source-evidence/shiji130-ministers-identity/context-reading.json')
  self.extra=read('source-evidence/shiji130-ministers-identity/expanded-context-reading.json')
  self.rows=self.base['decisions']+self.extra['decisions']
 def test_fourteen_source_local_records_reuse_eight_existing_people(self):
  people={p['id']:p for p in read('registry/persons.json')['persons']}
  self.assertEqual(len(self.rows),14);self.assertEqual(len({r['person_id'] for r in self.rows}),8)
  for row in self.rows:self.assertIn(row['person_id'],people)
  for i in range(1,15):
   receipt=read(f'source-evidence/shiji130-ministers-identity/retirement-{i:02}.json')
   self.assertEqual(receipt['identity_decision_id'],f'd-shiji130-ministers-cross-chapter-{i:02}')
   self.assertFalse(receipt['person_aliases_created'])
   self.assertEqual(len(receipt['retired_person_ids']),1)
   self.assertNotIn(receipt['retired_person_ids'][0],people)
 def test_twenty_nine_source_occurrences_keep_full_text_and_positions(self):
  chapters={d['id']:d for f in (ROOT/'corpus').glob('*/*.json') if (d:=json.loads(f.read_text())).get('record_type')=='marked_chapter'}
  bymid={m['id']:(p,m) for c in chapters.values() for p in c['paragraphs'] for m in p['mentions']}
  mids=[mid for r in self.rows for mid in r['target_mention_ids']];self.assertEqual(len(mids),29);self.assertEqual(len(set(mids)),29)
  for row in self.rows:
   for mid in row['target_mention_ids']:
    p,m=bymid[mid];self.assertEqual(m['person_id'],row['person_id']);self.assertEqual(p['text'][m['start']:m['end']],m['surface'])
  for unit in self.base['complete_units']+self.extra['complete_units']:
   c=chapters[unit['chapter_id']];p=next(p for p in c['paragraphs'] if p['id']==unit['paragraph']['id']);self.assertEqual(p['text'],unit['paragraph']['text'])
   actual={m['id']:m for m in p['mentions']}
   for expected in unit['paragraph']['mentions']:self.assertEqual(actual[expected['id']],expected)
 def test_two_hanxins_are_distinguished_by_their_biographies(self):
  ch=read('corpus/shiji/130.json');p104=next(p for p in ch['paragraphs'] if p['id'].endswith(':p104'));p105=next(p for p in ch['paragraphs'] if p['id'].endswith(':p105'))
  self.assertTrue(all(m['person_id']=='ofc_8ei_jb7' for m in p104['mentions'] if m['surface'] in ('信','淮陰侯')))
  self.assertTrue(all(m['person_id']=='l9e_fbr_36a_*A' for m in p105['mentions'] if m['surface']=='韓信'))
  self.assertNotEqual('ofc_8ei_jb7','l9e_fbr_36a_*A')
 def test_late_han_chenping_clerk_is_not_the_early_han_chancellor(self):
  ch=read('corpus/shiji/096.json');p=next(p for p in ch['paragraphs'] if p['id'].endswith(':p023'));self.assertEqual(next(m['person_id'] for m in p['mentions'] if m['surface']=='陳平'),'rwg_skp_gbq')
  people={p['id'] for p in read('registry/persons.json')['persons']};self.assertTrue({'rwg_skp_gbq','i3f_9l9_g53'}<=people)
 def test_existing_jin_reference_has_no_self_candidate_after_identification(self):
  row=next(v for v in read('source-evidence/jin043-wangrong-source/identity-review.json') if v['key']=='liang');self.assertEqual(row['person_id'],'ea5_zvr_hlp');self.assertEqual(row['same_surface_candidates'],[])
 def test_cross_chapter_decisions_preserve_ai_review_qualification(self):
  by={d['id']:d for d in read('corpus/shiji/130-identities.json')['decisions']}
  for row in self.rows:
   d=by[row['identity_decision_id']];self.assertEqual(d['person_id'],row['person_id']);self.assertEqual(d['scope'],'cross_chapter');self.assertFalse(d['human_reviewed']);self.assertEqual(d['status'],'contextual_provisional');self.assertGreater(len(d['chapter_ids']),1)
if __name__=='__main__':unittest.main(verbosity=2)
