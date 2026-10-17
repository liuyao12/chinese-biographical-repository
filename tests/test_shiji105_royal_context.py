import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class RoyalContext(unittest.TestCase):
 def test_yangxu_person_references_do_not_split_place(self):
  c=json.loads((ROOT/'corpus/shiji/105.json').read_text());ps={p['id']:p for p in c['paragraphs']};p=ps['c-shiji-105-bianque:p043'];h=[m for m in p['mentions']if m.get('person_id')=='yqp_nlb_p1p_ABI'];self.assertEqual([m['surface']for m in h],['侯','侯']);self.assertTrue(all(p['text'][m['end']:m['end']+1]!='國'for m in h));q=ps['c-shiji-105-bianque:p037'];self.assertTrue(any(m['surface']=='陽虛侯'and m.get('person_id')=='yqp_nlb_p1p_ABI'for m in q['mentions']))
 def test_wu_king_is_resolved_only_for_scoped_candidate(self):
  c=json.loads((ROOT/'corpus/shiji/105.json').read_text());m=next(m for p in c['paragraphs']for m in p['mentions']if m['id']=='c-shiji-105-bianque:m043-0062');self.assertEqual(m['person_id'],'yqp_nlb_p1p_CA');persons=json.loads((ROOT/'registry/persons.json').read_text())['persons'];self.assertFalse(any(p['id']=='vhq_7q6_k1o'for p in persons));self.assertFalse((ROOT/'data/corpus/profiles/vhq_7q6_k1o.json').exists());self.assertFalse((ROOT/'exports/persons/vhq_7q6_k1o.json').exists())
 def test_six_persons_table_names_and_old_titles_are_individually_marked(self):
  d=json.loads((ROOT/'data/historical-tables/shiji-017.json').read_text());r=next(r for f in d['fragments']for r in f['rows']if r['id']=='shiji-017-t1-r043');expected={5:('將閭','陽虛侯'),7:('志','安都侯'),8:('辟光','扐侯'),9:('賢','武城侯'),10:('卬','平昌侯'),11:('雄渠','白石侯')}
  for col,terms in expected.items():
   c=next(c for c in r['cells']if c['column']==col)
   ms=[m for m in c['person_mentions']if m['surface']in terms];self.assertEqual({m['surface']for m in ms},set(terms));self.assertEqual(len({m['person_id']for m in ms}),1)
   for m in ms:self.assertEqual(c['text'][m['start']:m['end']],m['surface']);self.assertLess(m['end']-m['start'],len(c['text']))
  self.assertEqual(r['year']['status'],'digital_editorial_equivalence');self.assertIn('平昌侯',next(c['text']for c in r['cells']if c['column']==10))
