# coding: utf-8
"""固定022兩完整單元的可攜原生測試；只讀ROOT下來源，不依賴/tmp包。"""
from pathlib import Path
import json,hashlib,copy,unittest
from scripts.uncle_parentage import explicit_maternal_uncle_valid
ROOT=Path(__file__).resolve().parents[1];J=lambda p:json.loads(p.read_text());H=lambda b:hashlib.sha256(b).hexdigest();C=J(ROOT/'corpus/sanguozhi/022-chenqun-chentai.json');A=J(ROOT/'corpus/sanguozhi/022-chenqun-chentai-assertions.json')['assertions'];PR=J(ROOT/'source-evidence/sanguozhi022-chenqun-chentai-projection.json');RAW=(ROOT/'sources/sanguozhi/022-kr214fcafa-fixed.txt').read_bytes();LS=RAW.decode().splitlines();PS={p['id']:p for p in C['paragraphs']};U={p['source_position']['unit_key']:p for p in C['paragraphs']}
def who(k,s):return next(m['person_id'] for m in U[k]['mentions'] if m['surface']==s)
def projected(c,proof):
 try:return c['source']['source_commit']=='214fcafa79894355909c9d8c2c1533089e7791c6' and len(c['paragraphs'])==16 and all(''.join(LS[r['raw_line']-1][r['raw_start']:r['raw_end']] for r in u['raw_runs'])==u['text']==next(p['text'] for p in c['paragraphs'] if p['id']==u['paragraph_id']) for u in proof['units'])
 except (KeyError,IndexError,StopIteration):return False
class ChenQunTaiSource(unittest.TestCase):
 def test_fixed_raw_hash(self):self.assertEqual(H(RAW),'3bac47f1f63c9556bc3b4087fda3cfb04f3470a267595521d236e22e58b00a3b')
 def test_complete_boundaries(self):
  self.assertTrue(LS[59].startswith('陳羣字長文'));self.assertTrue(LS[180].startswith('泰字玄伯'));self.assertTrue(LS[276].startswith('陳矯字季弼'));self.assertNotIn('陳矯字季弼',''.join(p['text'] for p in C['paragraphs']))
 def test_two_body_fourteen_note_layers(self):self.assertEqual(sum(p['text_layer']=='received_chapter' for p in C['paragraphs']),2);self.assertEqual(sum(p['text_layer']=='witness_appended_pei_songzhi_note' for p in C['paragraphs']),14)
 def test_all_projection_exact(self):self.assertTrue(projected(C,PR))
 def test_reject_revision_change(self):
  c=copy.deepcopy(C);c['source']['source_commit']='0'*40;self.assertFalse(projected(c,PR))
 def test_reject_skipped_raw_line(self):
  p=copy.deepcopy(PR);p['units'][0]['raw_runs'][0]['raw_line']+=1;self.assertFalse(projected(C,p))
 def test_reject_silent_glyph_change(self):
  c=copy.deepcopy(C);p=next(p for p in c['paragraphs'] if p['source_position']['unit_key']=='quoted_chenshi_pu');p['text']=p['text'].replace('凖','準');self.assertFalse(projected(c,PR))
 def test_reject_regnal_word_change(self):
  c=copy.deepcopy(C);c['paragraphs'][0]['text']=c['paragraphs'][0]['text'].replace('青龍','景元');self.assertFalse(projected(c,PR))
 def test_all_mention_slices(self):
  for p in C['paragraphs']:
   for m in p['mentions']:self.assertEqual(p['text'][m['start']:m['end']],m['surface'])
 def test_human_image_false(self):self.assertFalse(C['source']['image_verified']);self.assertFalse(C['annotation']['human_reviewed']);self.assertTrue(all(not a['human_reviewed'] for a in A))
 def test_chenqun_existing_identity(self):self.assertEqual(who('qun_received_body','陳羣'),'9w8_tqh_ysn_AA');self.assertEqual(who('quoted_bowuji','司空羣'),'9w8_tqh_ysn_AA')
 def test_chentai_existing_identity_and_zi(self):self.assertEqual(who('received_body','泰'),'9w8_tqh_ysn_AAA');self.assertEqual(who('received_body','玄伯'),'9w8_tqh_ysn_AAA')
 def test_sima_titles_reuse(self):self.assertEqual(who('received_body','司馬文王'),'dkn_ge4_286_AAAAI');self.assertEqual(who('received_body','司馬景王'),'dkn_ge4_286_AAAAH');self.assertEqual(who('quoted_weishi_chunqiu','司馬孚'),'dkn_ge4_286_AAAC')
 def test_wei_and_han_monarchs_distinct(self):
  self.assertEqual(who('qun_received_body','文帝'),'tix_jqk_w1o');self.assertEqual(who('qun_received_body','明帝'),'932_46f_026');self.assertNotEqual(who('qun_received_body','漢明帝'),'932_46f_026');self.assertEqual(who('sunsheng_criticism','武帝'),'yqp_nlb_p1p_ACAA')
 def test_poem_wen_not_sima(self):self.assertEqual(who('qun_received_body','文王'),'y4i_pjk_4gn_A')
 def test_zhugeliang_existing_kongming(self):self.assertEqual(who('received_body','諸葛亮'),'11e_f2d_5d2')
 def test_gaogui_emperor_same_event(self):self.assertEqual(who('quoted_ganbao_jinji','高貴鄉公'),'d6b_ea7_928');self.assertEqual(who('quoted_weishi_chunqiu','帝'),'d6b_ea7_928')
 def test_qun_tai_parent_explicit(self):self.assertTrue(any(a['subject_person_id']=='9w8_tqh_ysn_AAA' and a['predicate']=='father' and a['object_person_id']=='9w8_tqh_ysn_AA' and a['qualifiers']['source_term']=='子泰嗣' for a in A))
 def test_xun_after_note_remains_tai_son(self):
  x=who('received_body','恂');self.assertTrue(any(a['subject_person_id']==x and a['predicate']=='father' and a['object_person_id']=='9w8_tqh_ysn_AAA' for a in A));self.assertFalse(any(a['subject_person_id']==x and a['object_person_id']=='9w8_tqh_ysn_AA' for a in A))
 def test_wen_only_brother_no_fake_father(self):
  w=who('received_body','溫');self.assertTrue(any(a['subject_person_id']==w and a['predicate']=='brother' for a in A));self.assertFalse(any(a['subject_person_id']==w and a['predicate']=='father' for a in A))
 def test_uncle_existing_model_positive(self):
  a=next(a for a in A if a['predicate']=='maternal_uncle');self.assertTrue(explicit_maternal_uncle_valid(a,{p['id']:(C['id'],p) for p in C['paragraphs']}));self.assertIsNone(a['qualifiers']['mother_person_id'])
 def test_uncle_wrong_endpoint_rejected(self):
  a=copy.deepcopy(next(a for a in A if a['predicate']=='maternal_uncle'));a['object_person_id']='9w8_tqh_ysn_AA';self.assertFalse(explicit_maternal_uncle_valid(a,{p['id']:(C['id'],p) for p in C['paragraphs']}))
 def test_uncle_mother_filled_rejected(self):
  a=copy.deepcopy(next(a for a in A if a['predicate']=='maternal_uncle'));a['qualifiers']['mother_person_id']='yoo_ox0_545_BAF';self.assertFalse(explicit_maternal_uncle_valid(a,{p['id']:(C['id'],p) for p in C['paragraphs']}))
 def test_no_chentai_birthmother_invented(self):self.assertFalse(any(a['subject_person_id']=='9w8_tqh_ysn_AAA' and a['predicate']=='mother' for a in A))
 def test_grandsons_do_not_gain_unknown_fathers(self):
  for k,s in [('quoted_chenshi_pu','佐'),('quoted_chenshi_pu','逵')]:
   pid=who(k,s);self.assertTrue(any(a['subject_person_id']==pid and a['predicate']=='grandfather' for a in A));self.assertFalse(any(a['subject_person_id']==pid and a['predicate']=='father' for a in A))
 def test_dai_zheng_unresolved_no_ids(self):
  m=next(m for m in U['quoted_chenshi_pu']['mentions'] if m['surface']=='戴徵');self.assertEqual(m['kind'],'unresolved');self.assertIsNone(m['person_id'])
 def test_sunzi_two_candidates(self):
  m=next(m for m in U['received_body']['mentions'] if m['surface']=='孫子');self.assertEqual(set(m['candidate_person_ids']),{'vax_w2r_0za'});self.assertIsNone(m['person_id'])
 def test_no_generic_false_people(self):
  for p in C['paragraphs']:
   for m in p['mentions']:
    if m['kind']!='person':continue
    self.assertFalse(m['surface']=='羣' and p['text'][m['end']:m['end']+1]=='臣');self.assertFalse(m['surface']=='淮' and p['text'][m['end']:m['end']+1] in ['泗','北']);self.assertFalse(m['surface']=='安' and p['text'][max(0,m['start']-1):m['start']]=='南');self.assertFalse(m['surface']=='峻' and p['text'][m['end']:m['end']+1]=='城')
 def test_office_dispute_retained(self):
  self.assertIn('本傳泰不為太常未詳干寶所由知之',U['pei_critical_b']['text']);self.assertIn('太常陳泰',U['quoted_ganbao_jinji']['text']);self.assertNotIn('title_proposals',C['annotation'])
 def test_separate_death_reports(self):self.assertIn('景元元年薨',U['received_body']['text']);self.assertNotIn('歐血',U['received_body']['text']);self.assertIn('歐血薨',U['quoted_weishi_chunqiu']['text'])
 def test_life_age_facts_deferred(self):self.assertNotIn('age_assertions',C['annotation']);self.assertNotIn('life_events',C['annotation'])
 def test_all_relation_anchors_and_layers(self):
  for a in A:
   for e in a['evidence']:
    p=PS[e['paragraph_id']];r=e['relationship_anchor'];self.assertEqual(p['text'][r['start']:r['end']],r['surface']);self.assertEqual(e['quote'],p['text']);self.assertEqual(a['qualifiers']['source_layer'],'received_body' if p['text_layer']=='received_chapter' else 'ancient_commentary')
if __name__=='__main__':unittest.main()
