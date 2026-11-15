"""Source-bound author identity regression; no inference from a label."""
import unittest,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class ChuAuthorIdentity(unittest.TestCase):
 def test_source_signatures_share_current_author(self):
  mids=[];pids=[]
  for n in ('048','049','058','060','104','126','127','128'):
   ch=json.loads((ROOT/f'corpus/shiji/{n}.json').read_text())
   for p in ch['paragraphs']:
    for m in p['mentions']:
     if m['surface']=='褚先生':self.assertEqual(m['kind'],'person');self.assertEqual(p['text'][m['start']:m['end']],'褚先生');mids.append(m['id']);pids.append(m['person_id'])
  self.assertEqual(len(mids),11);self.assertEqual(len(set(pids)),1)
  people={p['id']:p for p in json.loads((ROOT/'registry/persons.json').read_text())['persons']};p=people[pids[0]];self.assertTrue(set(mids)<=set(next(a for a in p['aliases'] if a['surface']=='褚先生')['mention_ids']));self.assertTrue(set(mids)<={e.get('mention_id') for e in p['evidence']})
 def test_identity_and_authenticity_are_separate(self):
  r=json.loads((ROOT/'source-evidence/shiji-chu-author-identity/context-reading.json').read_text());self.assertFalse(r['human_reviewed']);self.assertIn('不宣稱每篇每句均已證明為褚少孫親筆',r['scope_qualification']);self.assertEqual(r['editorial_name']['reference']['revision_id'],2432895);self.assertFalse(r['editorial_name']['reference']['image_verified'])
 def test_history_bytes_pinned_not_rewritten(self):
  r=json.loads((ROOT/'source-evidence/shiji-chu-author-identity/context-reading.json').read_text())['historical_snapshot'];self.assertEqual(hashlib.sha256((ROOT/r['path']).read_bytes()).hexdigest(),r['sha256']);self.assertEqual(r['current_projection'][0]['mention_id'],'c-shiji-048-chenshe:m021-0000')
 def test_retired_ids_are_reservations(self):
  r=json.loads((ROOT/'source-evidence/shiji-chu-author-identity/annotation-chain.json').read_text());self.assertFalse(r['person_aliases_created']);self.assertEqual(len(r['retired_person_ids']),7);people=json.loads((ROOT/'registry/persons.json').read_text())['persons'];self.assertFalse(set(r['retired_person_ids'])&{p['id'] for p in people})
if __name__=='__main__':unittest.main()
