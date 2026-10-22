# coding: utf-8
import hashlib,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class LangyeKingReference(unittest.TestCase):
 def test_title_is_not_the_wang_surname(self):
  c=json.loads((ROOT/'corpus/nanshi/020-xiehongwei.json').read_text());ms=[m for p in c['paragraphs']for m in p['mentions']];m=next(m for m in ms if m['id']=='c-nanshi-020-xiehongwei:p005:m0029')
  self.assertEqual((m['surface'],m['person_id']),('琅邪王','ije_ngm_cmj'))
  self.assertTrue(all(x['person_id']!=m['person_id']for x in ms if x['surface']in('王練','王球')))
 def test_fixed_external_full_quotes_and_year_context(self):
  x=json.loads((ROOT/'source-evidence/nanshi020-langye-king-reading/reading.json').read_text());s=x['external_source'];raw=(ROOT/s['raw_path']).read_bytes();self.assertEqual(hashlib.sha256(raw).hexdigest(),s['raw_sha256']);self.assertEqual(s['revision_id'],2567072)
  for e in x['raw_excerpts']:self.assertEqual(raw.decode()[e['raw_start']:e['raw_end']],e['quote'])
  self.assertIn('以琅邪王德文爲大司馬',x['raw_excerpts'][0]['quote']);self.assertIn('義熙元年',x['year_context_quote'])
 def test_reverse_reference_and_qualified_decision(self):
  m='c-nanshi-020-xiehongwei:p005:m0029';reg=json.loads((ROOT/'registry/persons.json').read_text())['persons'];p=next(p for p in reg if p['id']=='ije_ngm_cmj');self.assertTrue(any(e.get('mention_id')==m for e in p['evidence']))
  ds=json.loads((ROOT/'corpus/nanshi/020-xiehongwei-identities.json').read_text())['decisions'];d=next(d for d in ds if d['id']=='d-nanshi020-langye-king');self.assertFalse(d['human_reviewed']);self.assertEqual(d['status'],'contextual_provisional');self.assertIn('不能由府主任命年推出弘微參軍始年',d['rationale'])
