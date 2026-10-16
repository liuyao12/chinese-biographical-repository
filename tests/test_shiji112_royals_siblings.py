# coding: utf-8
import json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def load(f):return json.loads((R/f).read_text())
def para(n,k):return next(p for p in load('corpus/shiji/'+n+'.json')['paragraphs']if p['id'].endswith(':p'+str(k).zfill(3)))
def pid(n,k,s):return next(m['person_id']for m in para(n,k)['mentions']if m['surface']==s)
def assertion(n,aid):return next(a for a in load('corpus/shiji/'+n+'-assertions.json')['assertions']if a['id']==aid)
class RoyalSiblings(unittest.TestCase):
 def test_qi_case_keeps_received_name(self):
  self.assertEqual(pid('112',25,'齊王'),'qok_ik2_99j_A');self.assertEqual(pid('052',26,'次景'),'qok_ik2_99j_A');self.assertIn('子次景立',para('052',26)['text']);self.assertNotEqual(pid('112',25,'齊王'),pid('052',25,'齊王'))
 def test_yan_same_case_and_zhao_regnal_context(self):
  self.assertEqual(pid('112',23,'燕王定國'),'jo4_4bf_0ra_AA');self.assertEqual(pid('052',28,'燕王'),'jo4_4bf_0ra_AA');self.assertEqual(pid('112',26,'趙王'),'yqp_nlb_p1p_ACAF');self.assertEqual(pid('052',30,'趙王'),'yqp_nlb_p1p_ACAF');d=next(d for d in load('corpus/shiji/112-equivalences.json')['decisions']if d['id']=='eq-shiji112-royals-zhao');self.assertTrue(any(r['quote']=='二十九'for r in d['references']));self.assertTrue(any(r['scope']=='preceding_source_chronological_context_only'for r in d['references']));self.assertFalse(any(e['paragraph_id']=='c-shiji-112-pingjin:p025'for e in d['evidence']))
 def test_sister_anaphors_resolved_without_new_spans(self):
  p=para('052',29)
  for mid,start in [('m029-0090',90),('m029-0131',131)]:
   m=next(m for m in p['mentions']if m['id'].endswith(mid));self.assertEqual((m['start'],m['end'],m['surface'],m['person_id']),(start,start+1,'姊','er5_u4u_i79'))
  self.assertEqual(pid('112',25,'姊'),'er5_u4u_i79')
 def test_sister_predicate_subject_is_female_sibling(self):
  for n,aid,subject,obj in [('111','a-shiji111-008','l5c_h8i_d5q','5dd_l1c_6g8'),('112','a-shiji112-003','er5_u4u_i79','qok_ik2_99j_A')]:
   a=assertion(n,aid);self.assertEqual((a['subject_person_id'],a['predicate'],a['object_person_id']),(subject,'sister',obj));r=a['qualifiers']['relative_birth_order'];self.assertEqual((r['older_person_id'],r['younger_person_id']),(subject,obj));self.assertIsNone(r['older_ordinal']);self.assertIsNone(r['younger_ordinal'])
 def test_conflicting_wei_age_order_stays_literal(self):
  a=assertion('111','a-shiji111-008');b=assertion('126','a-shiji126-005');self.assertEqual(a['qualifiers']['relative_birth_order']['older_person_id'],'l5c_h8i_d5q');self.assertEqual(b['qualifiers']['relative_birth_order']['older_person_id'],'5dd_l1c_6g8');self.assertIn('而姊衛子夫',para('111',1)['text']);self.assertIn('衛后兄也',para('126',19)['text'])
 def test_sister_not_spouse_or_invented_father(self):
  for n in ['052','112']:
   claims=load('corpus/shiji/'+n+'-assertions.json')['assertions'];self.assertFalse(any(a['predicate']=='spouse'and {a['subject_person_id'],a['object_person_id']}=={'er5_u4u_i79','qok_ik2_99j_A'}for a in claims));self.assertFalse(any(a['predicate']=='father'and a['subject_person_id']=='er5_u4u_i79'for a in claims))
 def test_retired_ids_removed(self):
  for p in ['7q5_0n4_mjt','40o_6pe_hvm','2t5_tp3_6ti','mm9_vf1_7o8','4lf_9lg_slx','hb2_xk3_z67']:
   self.assertNotIn(p,{x['id']for x in load('registry/persons.json')['persons']})
   for folder in ['exports/persons','data/corpus/profiles']:self.assertFalse((R/folder/(p+'.json')).exists())
