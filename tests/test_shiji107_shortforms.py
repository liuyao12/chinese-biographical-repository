import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(name):return json.loads((ROOT/'corpus/shiji'/name).read_text())
def para(n):return read('107.json')['paragraphs'][n-1]
def matches(n,s):return [m for m in para(n)['mentions']if m['surface']==s]
class WeiqiShortforms(unittest.TestCase):
 def test_dialogue_addressee_switches_inside_one_paragraph(self):
  self.assertEqual({m['person_id']for m in matches(7,'將軍')},{'7mz_d13_9ka_A'});self.assertEqual({m['person_id']for m in matches(7,'君侯')},{'nuf_tb9_fjs_A'});self.assertEqual(len(matches(7,'將軍')),3);self.assertEqual(len(matches(7,'君侯')),5)
 def test_taizi_fu_is_a_title_but_actual_prince_is_marked(self):
  p=para(4);at=p['text'].index('太子傅');self.assertFalse(any(m['start']<=at<m['end']for m in p['mentions']));ms=matches(4,'太子');self.assertEqual(len(ms),2);self.assertEqual({m['person_id']for m in ms},{'yqp_nlb_p1p_ACAH'})
 def test_cheng_li_compound_has_two_adjacent_persons(self):
  p=para(20);chars=[m for m in p['mentions']if m['surface']in ['程','李']];self.assertEqual(len(chars),4)
  for a,b in zip(chars[::2],chars[1::2]):self.assertEqual(a['end'],b['start']);self.assertEqual((a['surface'],b['surface']),('程','李'));self.assertEqual((a['person_id'],b['person_id']),('y6f_9v5_dqg','27j_f4p_jwp'))
 def test_enemy_general_is_not_guan_he(self):
  p=para(12);at=p['text'].index('若將軍頭')+1;self.assertFalse(any(m['start']==at for m in p['mentions']));ms=matches(12,'將軍');self.assertEqual(len(ms),2);self.assertEqual({m['person_id']for m in ms},{'d4q_icw_co6'});self.assertEqual({m['person_id']for m in matches(12,'太尉')},{'koy_6jg_gcc_C'});self.assertEqual({m['person_id']for m in matches(12,'吳王')},{'yqp_nlb_p1p_CA'})
 def test_embedded_edict_keeps_jingdi_outer_narrative_wudi(self):
  p=para(24);at=p['text'].index('論上')+1;ms=matches(24,'上');self.assertEqual(next(m['person_id']for m in ms if m['start']==at),'yqp_nlb_p1p_ACA');self.assertEqual({m['person_id']for m in ms if m['start']!=at},{'yqp_nlb_p1p_ACAA'})
 def test_queen_and_king_contexts_remain_separate(self):
  self.assertEqual({m['person_id']for m in matches(2,'太后')},{'ixk_6fg_v6f_A'});self.assertEqual({m['person_id']for m in matches(6,'太后')},{'6d6_eg1_o3a_A'});self.assertIsNone(matches(7,'太后')[0]['person_id']);self.assertEqual({m['person_id']for m in matches(26,'大王')+matches(26,'王')},{'yqp_nlb_p1p_AFA'})
 def test_thirteen_decisions_keep_source_anchors_and_no_new_tenures(self):
  ds=[d for d in read('107-identities.json')['decisions']if d['id'].startswith('d-shiji107-shortforms-')];self.assertEqual(len(ds),13)
  for d in ds:self.assertFalse(d['human_reviewed']);self.assertTrue(all(e['mention_ids']for e in d['evidence']))
  self.assertEqual(len(read('107-titles.json')['holdings']),44)
