import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class CoreFamilyNames(unittest.TestCase):
 def test_opening_persons_and_king_former_title(self):
  c=json.loads((ROOT/'corpus/shiji/105.json').read_text());ms=[m for p in c['paragraphs']for m in p['mentions']]
  for surface,pid in [('趙簡子','p4b_qf7_603_AA'),('董安于','t2m_90g_lng'),('秦穆公','y97_huh_vuz_AAAAA'),('公孫支','1ku_2ry_mri')]:self.assertTrue(any(m['surface']==surface and m.get('person_id')==pid for m in ms))
  p=next(p for p in c['paragraphs']if p['id'].endswith('p037'));self.assertEqual(next(m['person_id']for m in p['mentions']if m['surface']=='齊王'),'jc7_nxq_532')
 def test_jin_family_chain_and_direct_daogong_are_shared(self):
  reg=json.loads((ROOT/'registry/persons.json').read_text());people={p['id']:p for p in reg['persons']}
  for child,parent in [('6di_ywz_ju4_AAAD','6di_ywz_ju4_AAA'),('6di_ywz_ju4_AAADA','6di_ywz_ju4_AAAD'),('6di_ywz_ju4_AAADAA','6di_ywz_ju4_AAADA'),('6di_ywz_ju4_AAADAAA','6di_ywz_ju4_AAADAA')]:self.assertEqual(people[child]['family_path']['parent_person_id'],parent)
  self.assertNotIn('6di_ywz_ju4_AAAD**A',people);self.assertFalse(any(pid.startswith('kat_48c_thr')for pid in people))
  c=json.loads((ROOT/'corpus/shiji/043.json').read_text());p=next(p for p in c['paragraphs']if p['id'].endswith('p019'));self.assertEqual(next(m['person_id']for m in p['mentions']if m['surface']=='曾孫周'),'6di_ywz_ju4_AAADAAA')
 def test_explicit_name_components_and_source_conflicts(self):
  names=json.loads((ROOT/'data/corpus/profile-names.json').read_text())['records']
  for pid,surname,ming in [('6hq_bb2_3rb','秦','越人'),('opr_t0a_l8g','淳于','意')]:
   r=next(r for r in names if r['person_id']==pid);self.assertEqual((r['surname'],r['ming']),(surname,ming));self.assertFalse(r['human_reviewed'])
  c=json.loads((ROOT/'corpus/shiji/105.json').read_text());p=next(p for p in c['paragraphs']if p['id'].endswith('p002'));self.assertTrue(p['text'].startswith('當晉昭公時'))
  d=json.loads((ROOT/'corpus/shiji/105-equivalences.json').read_text());rows=[r for r in d['decisions']if r['id'].startswith('eq-shiji105-core-')];self.assertEqual(len(rows),13)
  self.assertTrue(any('是時齊無桓侯' in ref['quote']for r in rows for ref in r.get('references',[])))
