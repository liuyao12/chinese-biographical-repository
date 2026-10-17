import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class ChuMinister(unittest.TestCase):
 def test_same_office_event_and_explicit_ancient_identification(self):
  eq=json.loads((ROOT/'corpus/shiji/106-equivalences.json').read_text())['decisions'];e=next(e for e in eq if e['id']=='eq-shiji106-chu-minister-001');self.assertEqual(e['person_ids'],['i8p_f0y_kea']);self.assertEqual(len(e['evidence']),2);self.assertEqual([r['quote']for r in e['references']],['楚相張尚諫王而死。','按：羽，尚弟也。']);self.assertTrue(all(not r['image_verified']for r in e['references']))
 def test_brother_order_preserved_without_invented_father(self):
  a=next(a for a in json.loads((ROOT/'corpus/shiji/106-assertions.json').read_text())['assertions']if a['id']=='a-shiji106-010');self.assertEqual((a['subject_person_id'],a['predicate'],a['object_person_id']),('o6h_ba5_gno','brother','i8p_f0y_kea'));q=a['qualifiers']['relative_birth_order'];self.assertEqual(q['older_person_id'],'i8p_f0y_kea');self.assertEqual(q['younger_person_id'],'o6h_ba5_gno');self.assertIsNone(q['older_ordinal']);self.assertIsNone(q['younger_ordinal'])
 def test_thin_identity_uses_same_robes_punishment_event(self):
  c=json.loads((ROOT/'corpus/shiji/050.json').read_text());p=next(p for p in c['paragraphs']if '其相張尚'in p['text']);m=next(m for m in p['mentions']if m['surface']=='薄太后');self.assertEqual(m['person_id'],'9zj_vf7_86a_A');self.assertIn('削東海郡',p['text'])
 def test_old_candidates_removed(self):
  reg=json.loads((ROOT/'registry/persons.json').read_text());ids={p['id']for p in reg['persons']}
  for pid in ['tae_3uh_xsc','jko_7a4_o8v']:
   self.assertNotIn(pid,ids);self.assertFalse((ROOT/'exports/persons'/f'{pid}.json').exists());self.assertFalse((ROOT/'data/corpus/profiles'/f'{pid}.json').exists())
