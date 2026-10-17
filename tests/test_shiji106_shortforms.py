import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def chapter():return json.loads((ROOT/'corpus/shiji/106.json').read_text())
def para(key):return next(p for p in chapter()['paragraphs']if p['id'].endswith(':'+key))
def people(key,surface):return {m['person_id']for m in para(key)['mentions']if m['surface']==surface}
class Shortforms(unittest.TestCase):
 def test_court_prince_is_jingdi_not_wu_prince(self):
  p=para('p004');first=[m for m in p['mentions']if m['surface']=='太子'];self.assertEqual(len(first),2);self.assertEqual({m['person_id']for m in first},{'yqp_nlb_p1p_ACA'});at=p['text'].index('太子之郄');self.assertFalse(any(m['start']==at for m in p['mentions']))
 def test_dialogue_addressee_is_jiaoxi(self):
  self.assertEqual(people('p005','大王'),{'yqp_nlb_p1p_ABB'});self.assertEqual(people('p005','王'),{'yqp_nlb_p1p_ABB'});self.assertEqual(people('p005','主上'),{'yqp_nlb_p1p_ACA'})
 def test_chu_sui_xi_does_not_name_zhao_king_sui(self):
  p=para('p017');at=p['text'].index('楚王遂西');m=next(m for m in p['mentions']if m['start']==at);self.assertEqual((m['surface'],m['person_id']),('楚王','yqp_nlb_p1p_DCA'));self.assertFalse(any(m['start']==at+2 for m in p['mentions']))
 def test_jiaoxi_dowager_is_not_assumed_birth_mother(self):
  self.assertEqual(people('p006','太后'),{'pxm_dwu_afr'});a=json.loads((ROOT/'corpus/shiji/106-assertions.json').read_text())['assertions'];self.assertFalse(any(a['subject_person_id']=='yqp_nlb_p1p_ABB'and a['predicate']=='mother'for a in a))
 def test_final_prince_is_de_and_taiwei_is_zhou_yafu(self):
  self.assertEqual(people('p018','太子'),{'yqp_nlb_p1p_ABBA'});self.assertEqual(people('p017','太尉'),{'koy_6jg_gcc_C'})
