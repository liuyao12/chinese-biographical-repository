"""Permanent data regression; canonical follows stable source MID after future rekeys."""
import unittest,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class CaoRenCrossIdentity(unittest.TestCase):
 def read(self,p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
 def test_source_mids_and_reverse_evidence(self):
  k=self.read('corpus/sanguozhi/015-wenhui.json');c=self.read('corpus/sanguozhi/023-qing-collation.json');km='c-sanguozhi-015-wenhui:p003:m0046';tm=['c-sanguozhi-023-qing-collation:p001:'+s for s in ('m0528','m0562','m0585')];lookup={m['id']:(p,m)for ch in(k,c)for p in ch['paragraphs']for m in p['mentions']};pid=lookup[km][1]['person_id'];rows={p['id']:p for p in self.read('registry/persons.json')['persons']}
  for mid in [km]+tm:
   p,m=lookup[mid];self.assertEqual(m['person_id'],pid);self.assertEqual(p['text'][m['start']:m['end']],m['surface']);self.assertTrue(any(e['mention_id']==mid for e in rows[pid]['evidence']))
  p,m=lookup[tm[1]];self.assertIn('監本作　曹仁',p['text']);other=next(x for x in p['mentions']if x['id'].endswith(':m0549'));self.assertEqual(other['surface'],'曹休');self.assertNotEqual(other['person_id'],pid)
 def test_primary_complete_units_and_anchor_bytes(self):
  d=self.read('source-evidence/caoren-zixiao-identity/primary-proof.json')
  for u in d['complete_units']:
   b=(ROOT/u['raw_file']).read_bytes();self.assertEqual(hashlib.sha256(b).hexdigest(),u['raw_sha256']);self.assertEqual(b.decode()[u['raw_start']:u['raw_end']],u['raw_quote'])
  for a in d['anchors']:
   s=(ROOT/a['raw_file']).read_text(encoding='utf-8');self.assertEqual(''.join(s[i]for i in a['raw_codepoint_positions']),a['quote'])
 def test_retirement_has_no_current_person_or_alias(self):
  d=self.read('source-evidence/caoren-zixiao-identity/annotation-chain.json');rows=self.read('registry/persons.json')['persons'];self.assertIs(d['person_aliases_created'],False)
  for old in d['retired_person_ids']:
   self.assertFalse(any(r['id']==old or any(a.get('surface')==old for a in r.get('aliases',[]))for r in rows));self.assertFalse((ROOT/'exports/persons'/f'{old}.json').exists());self.assertFalse((ROOT/'data/corpus/profiles'/f'{old}.json').exists())
if __name__=='__main__':unittest.main()
