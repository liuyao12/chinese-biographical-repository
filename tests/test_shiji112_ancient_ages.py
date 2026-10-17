# coding: utf-8
import json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def load(f):return json.loads((R/f).read_text())
def para(k):return next(p for p in load('corpus/shiji/112.json')['paragraphs']if p['id'].endswith(':p'+str(k).zfill(3)))
def pid(k,s):return next(m['person_id']for m in para(k)['mentions']if m['surface']==s)
class PingjinAncientAges(unittest.TestCase):
 def test_qi_ministers_and_kings_are_contextual(self):
  for s,p in [('管仲','h1v_8ap_b9y'),('晏嬰','jcn_rp4_qap'),('桓公','9w2_c77_53m'),('景公','wuz_yxe_b9k')]:self.assertEqual(pid(6,s),p)
  self.assertNotEqual(pid(6,'桓公'),'lmu_nbm_rzo_AAAAAAABAAAAA');self.assertEqual(pid(29,'齊桓'),'9w2_c77_53m')
 def test_qin_names_and_rebel_aliases(self):
  for k,s,p in [(12,'秦皇帝','ao3_0fy_d45_AAA'),(19,'秦王','ao3_0fy_d45_AAA'),(12,'李斯','49g_7az_e4i'),(24,'蒙恬','k2p_5ol_dwh_AA'),(15,'陳涉','pom_ycp_ha5'),(19,'陳勝','pom_ycp_ha5')]:self.assertEqual(pid(k,s),p)
 def test_nested_speaker_and_kongzi_aliases(self):
  ms=[m for m in para(13)['mentions']if m['surface']=='陛下'];self.assertEqual([m['person_id']for m in ms],['yqp_nlb_p1p_A','yqp_nlb_p1p_ACAA']);self.assertEqual(pid(29,'仲尼'),'fp6_ia6_7yw');self.assertEqual(pid(15,'孔'),'fp6_ia6_7yw');self.assertEqual(pid(29,'孔子'),'fp6_ia6_7yw')
 def test_ages_keep_open_lower_and_exact_report_not_birth(self):
  ages=load('corpus/shiji/112.json')['annotation']['age_assertions'];a,b=ages;self.assertIsNone(a['value']);self.assertEqual(a['bounds'],dict(lower=40,lower_inclusive=False,upper=None,upper_inclusive=None));self.assertEqual(a['source_term'],'年四十餘');self.assertEqual(b['value'],60);v=b['normalized_date_range'];self.assertEqual((v['earliest']['era_year'],v['latest']['era_year']),(141,140));self.assertEqual((v['earliest']['year'],v['latest']['year']),(-140,-139));self.assertNotIn('normalized_date',b)
  for age in ages:self.assertIsNone(age['birth_year']);self.assertEqual(age['counting'],'unspecified_source_age');self.assertIn(age['source_term'],age['evidence'][0]['quote'])
 def test_child_tenure_is_not_age_or_exact_dates(self):
  h=next(h for h in load('corpus/shiji/112-titles.json')['holdings']if h['id']=='th-shiji112-016');d=h['reported_duration'];self.assertEqual(h['person_id'],'q69_35n_f3h_A');self.assertEqual(d['unit'],'title_year');self.assertEqual(d['source_term'],'十餘歲');self.assertIsNone(d['value']);self.assertEqual(d['bounds'],dict(lower=10,lower_inclusive=False,upper=None,upper_inclusive=None));self.assertEqual(h['effective_period']['start']['status'],'unknown');self.assertEqual(h['effective_period']['end']['status'],'unknown')
 def test_old_ids_removed(self):
  for p in ['zgg_ncu_lxg','811_det_o9f','6ua_ti1_4bc','i8v_5et_i28','ny0_svo_ifn','62u_sdu_1e9','8kz_4ad_0fq','1c0_c3k_jno','b74_xpn_elo','wsh_uzd_aj3']:
   self.assertNotIn(p,{p['id']for p in load('registry/persons.json')['persons']})
   for folder in ['exports/persons','data/corpus/profiles']:self.assertFalse((R/folder/(p+'.json')).exists())
 def test_historical_references_do_not_receive_wudi_dates(self):
  for h in load('corpus/shiji/112-titles.json')['holdings']:
   if h['person_id']in ['h1v_8ap_b9y','jcn_rp4_qap','9w2_c77_53m','wuz_yxe_b9k']:
    for a in h['attestations']:self.assertNotIn('normalized_date',a)
