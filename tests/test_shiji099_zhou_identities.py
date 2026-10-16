# coding: utf-8
import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MAPPING={'6l4_h2o_qll':'jqy_1fv_u7v','46o_tfb_rlc':'ubt_idy_jr8','r4u_mw5_3u3':'5dm_e40_rqh','5va_k17_tk7':'y4i_pjk_4gn_A','81b_bpq_qcv':'y4i_pjk_4gn_AA','282_wxp_l9r':'y4i_pjk_4gn_AD','xv9_2k8_d07':'qna_m75_pj8','doa_gbf_ent':'nek_dsn_nih'}
def read(p):return json.loads((ROOT/p).read_text())
class ZhouQuotedIdentityTests(unittest.TestCase):
 def test_eight_identifications_have_both_quoted_story_and_zhou_context(self):
  c=read('corpus/shiji/099.json');z=read('corpus/shiji/004.json')
  ds=[d for d in read('corpus/shiji/099-equivalences.json')['decisions'] if d['id'].startswith('eq-shiji099-zhou-')]
  self.assertEqual(len(ds),8)
  for d in ds:
   self.assertIn(d['canonical_person_id'],MAPPING.values());self.assertTrue(d['identity_materialized'])
   self.assertEqual(set(d['chapter_ids']),{c['id'],z['id']})
   for e in d['evidence']:
    source=c if e['chapter_id']==c['id'] else z
    p=next(p for p in source['paragraphs'] if p['id']==e['paragraph_id'])
    self.assertEqual(e['quote'],p['text']);self.assertTrue(e['mention_ids'])
    self.assertTrue(all(any(m['id']==mid and m['person_id']==d['canonical_person_id'] for m in p['mentions']) for mid in e['mention_ids']))
 def test_cheng_kang_are_two_individual_characters(self):
  p=read('corpus/shiji/099.json')['paragraphs'][1]
  at=p['text'].index('成康')
  marks=[m for m in p['mentions'] if at<=m['start']<at+2]
  self.assertEqual([(m['surface'],m['person_id']) for m in marks],[('成','qna_m75_pj8'),('康','nek_dsn_nih')])
 def test_retired_candidates_have_no_person_files(self):
  ids={p['id'] for p in read('registry/persons.json')['persons']}
  for old in MAPPING:
   self.assertNotIn(old,ids)
   for folder in ['data/corpus/profiles','exports/persons']:self.assertFalse((ROOT/folder/(old+'.json')).exists())
 def test_hypothetical_and_actual_princesses_remain_separate(self):
  p=read('corpus/shiji/099.json')['paragraphs'][5]
  self.assertEqual({m['person_id'] for m in p['mentions'] if m['surface']=='長公主'},{'yqp_nlb_p1p_AI','g7g_fpv_oq5'})
  self.assertTrue(all(m.get('person_id') is None for m in p['mentions'] if m['surface']=='外孫'))
