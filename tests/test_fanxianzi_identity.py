import unittest,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1]
class FanXianIdentity(unittest.TestCase):
 def load(self,p):return json.loads((R/p).read_text())
 def mark(self,rel,mid):return next((q,m)for q in self.load(rel)['paragraphs']for m in q['mentions']if m['id']==mid)
 def test_early_and_late_are_distinct(self):
  q,a=self.mark('corpus/shiji/039.json','c-shiji-039-jin:m119-0065');_,b=self.mark('corpus/shiji/039.json','c-shiji-039-jin:m126-0038');self.assertNotEqual(a['person_id'],b['person_id']);self.assertEqual(q['text'][a['start']:a['end']],'范獻子');self.assertIn('首選',a['interpretation_note'])
 def test_late_two_sources_and_hhs_same(self):
  _,a=self.mark('corpus/shiji/039.json','c-shiji-039-jin:m126-0038');_,b=self.mark('corpus/shiji/044.json','c-shiji-044-wei:m008-0068');q,c=self.mark('corpus/houhanshu/064-luzhi.json','c-houhanshu-064-luzhi:note002:u0003');self.assertEqual(a['person_id'],b['person_id']);self.assertEqual(a['person_id'],c['person_id']);self.assertTrue(q['text'].startswith('左傳曰范獻子曰'));self.assertIn('主客差異',c['interpretation_note'])
 def test_raw_units_exact(self):
  base=R/'source-evidence/fanxianzi-identity-audit'
  for u in json.loads((base/'units.json').read_text()):
   s=(base/u['path']).read_text()[u['start']:u['end']];self.assertEqual(s,u['raw']);self.assertEqual(hashlib.sha256(s.encode()).hexdigest(),u['sha256'])
 def test_retirement_not_alias(self):
  from scripts.retired_person_ids import retired_person_ids
  rec=self.load('source-evidence/fanxianzi-identity-audit/annotation-chain.json');ps=self.load('registry/persons.json')['persons'];self.assertFalse(rec['person_aliases_created'])
  for old in rec['retired_person_ids']:
   self.assertIn(old,retired_person_ids(R));self.assertFalse(any(old==p['id']or old in p.get('id_aliases',[])for p in ps))
 def test_full_event_father_son_and_self_names(self):
  units={u['id']:u['visible']for u in self.load('source-evidence/fanxianzi-identity-audit/units.json')};self.assertIn('鞅之父與二三子在君所矣',units['B9.23.3']);self.assertIn('匄也',units['B9.8.8']);self.assertIn('故鞅以為難',units['B10.27.4']);self.assertIn('嫠不恤其緯',units['B10.24.6'])
