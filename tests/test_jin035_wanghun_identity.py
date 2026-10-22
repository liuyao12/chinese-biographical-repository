# coding: utf-8
"""Cross-history Wang Hun identity and marriage evidence boundaries."""
import json
import unittest
from pathlib import Path
from scripts.retired_person_ids import retired_person_ids
ROOT=Path(__file__).resolve().parents[1]
class WangHunIdentity(unittest.TestCase):
 def test_four_source_references_use_taiyuan_identity(self):
  c=json.loads((ROOT/'corpus/jinshu/035-pei-family.json').read_text())
  wanted={'p006:m0100':'父','p006:m0101':'王渾','p007:m0011':'王渾','p007:m0118':'臣'}
  actual={m['id'].split('family:')[1]:m for p in c['paragraphs']for m in p['mentions']if m['id'].split('family:')[1]in wanted}
  self.assertEqual(set(actual),set(wanted))
  for k,m in actual.items():self.assertEqual(m['person_id'],'a8f_ec8_e74_AB');self.assertEqual(m['surface'],wanted[k])
 def test_marriage_clause_remains_qualified_support(self):
  d=json.loads((ROOT/'corpus/jinshu/035-pei-identities.json').read_text())['decisions'][0]
  self.assertEqual(d['status'],'contextual_provisional');self.assertFalse(d['human_reviewed'])
  r=json.loads((ROOT/d['external_reference_file']).read_text())
  self.assertIn('姊夫僅修和嶠',r['alternative_reading'])
  self.assertIn('與姊夫和嶠及裴楷齊名',r['supporting_marriage_clause']['quote'])
  self.assertFalse(any(e['paragraph_id'].endswith('line028')for e in d['evidence']))
 def test_old_identity_retired_and_wifes_father_updated(self):
  reg=json.loads((ROOT/'registry/persons.json').read_text())['persons']
  self.assertNotIn('wqv_0yh_new',{p['id']for p in reg});self.assertIn('wqv_0yh_new',retired_person_ids(ROOT))
  aa=json.loads((ROOT/'corpus/jinshu/035-pei-family-assertions.json').read_text())['assertions']
  a=next(a for a in aa if a['id']=='a-jin035-pei-kai-wife-father')
  self.assertEqual((a['subject_person_id'],a['predicate'],a['object_person_id']),('5mr_fbg_vop','father','a8f_ec8_e74_AB'))
