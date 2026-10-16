# coding: utf-8
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text())
def paragraph(book,n):return next(p for p in load('corpus/shiji/'+book+'.json')['paragraphs']if p['id'].endswith(':p'+str(n).zfill(3)))
class LiGuangQinYanIdentities(unittest.TestCase):
 def test_lixin_ancestor_stays_unspecified(self):
  a=next(a for a in load('corpus/shiji/109-assertions.json')['assertions']if a['id']=='a-shiji109-001')
  self.assertEqual((a['subject_person_id'],a['predicate'],a['object_person_id']),('27j_f4p_jwp','ancestor','k7j_gr6_8nz'));self.assertIsNone(a['qualifiers']['generation_distance'])
  for assembly in load('registry/family-assemblies.json')['assemblies']:
   self.assertFalse({'27j_f4p_jwp','k7j_gr6_8nz'}<={m['person_id']for m in assembly['members']})
 def test_specific_chase_identifies_both_people(self):
  p=paragraph('109',1);self.assertEqual(next(m['person_id']for m in p['mentions']if m['surface']=='李信'),'k7j_gr6_8nz');self.assertEqual(next(m['person_id']for m in p['mentions']if m['surface']=='丹'),'e3o_2bk_lhm')
  for book,n in [('073',10),('086',35)]:
   ids={m.get('person_id')for m in paragraph(book,n)['mentions']};self.assertTrue({'k7j_gr6_8nz','e3o_2bk_lhm'}<=ids)
 def test_hostage_dan_keeps_its_narrative(self):
  for n in [17,18]:
   ms=[m for m in paragraph('071',n)['mentions']if '太子'in m['surface']];self.assertTrue(ms);self.assertEqual({m['person_id']for m in ms},{'e3o_2bk_lhm'})
  self.assertIn('三年而燕王喜使太子丹入質於秦',paragraph('071',17)['text']);self.assertIn('秦歸燕太子',paragraph('071',18)['text'])
 def test_conflicting_capture_and_death_wording_survives(self):
  self.assertIn('卒破得丹',paragraph('073',10)['text']);self.assertIn('燕王乃使使斬太子丹',paragraph('086',35)['text'])
  d=next(d for d in load('corpus/shiji/109-equivalences.json')['decisions']if d['id']=='eq-shiji109-qinyan-lixin');self.assertIn('不判定殺丹者',d['rationale']);self.assertFalse(d['human_reviewed'])
 def test_retired_candidates_have_no_public_files(self):
  people={p['id']for p in load('registry/persons.json')['persons']}
  for pid in ['vm4_pus_oa9','t6o_4u4_qj2','yqm_g1b_g6u']:
   self.assertNotIn(pid,people)
   for folder in ['exports/persons','data/corpus/profiles']:self.assertFalse((ROOT/folder/(pid+'.json')).exists())
 def test_decisions_keep_exact_native_evidence(self):
  for d in load('corpus/shiji/109-equivalences.json')['decisions']:
   if not d['id'].startswith('eq-shiji109-qinyan-'):continue
   self.assertEqual(d['person_ids'],[d['canonical_person_id']]);self.assertTrue(d['identity_materialized'])
   for e in d['evidence']:
    book=e['chapter_id'].split('-')[2];p=next(p for p in load('corpus/shiji/'+book+'.json')['paragraphs']if p['id']==e['paragraph_id']);self.assertEqual(e['quote'],p['text']);self.assertTrue(set(e['mention_ids'])<={m['id']for m in p['mentions']})
