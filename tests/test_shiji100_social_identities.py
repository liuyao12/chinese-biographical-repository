# coding: utf-8
import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OLD={'m0d_n8x_pj8','fjt_yam_bfq','o7j_zzq_frd','52e_gh9_em4','j9f_i2u_283'}
def read(p):return json.loads((ROOT/p).read_text())
def para(n,key):return next(p for p in read('corpus/shiji/'+n+'.json')['paragraphs'] if p['id'].endswith(':'+key))
def eq(key):return next(d for d in read('corpus/shiji/100-equivalences.json')['decisions'] if d['id']=='eq-shiji100-social-'+key)
class JibuSocialIdentityTests(unittest.TestCase):
 def test_zhao_tong_is_same_han_eunuch_across_three_chapters(self):
  for n,key in [('100','p004'),('101','p006'),('125','p001')]:self.assertEqual({m['person_id'] for m in para(n,key)['mentions'] if m['surface']=='趙同'},{'qyn_07y_0gt'})
  for n,key in [('039','p107'),('043','p010')]:self.assertNotEqual(next(m['person_id'] for m in para(n,key)['mentions'] if m['surface']=='趙同'),'qyn_07y_0gt')
 def test_li_qi_commentary_is_a_scoped_digital_witness(self):
  r=next(r for r in eq('zhaotong')['references'] if r.get('commentator')=='李奇')
  self.assertEqual(r['quote'],'宦者趙談也');self.assertEqual(r['page_id'],'KR2a0007_WYG_037-3b');self.assertEqual(len(r['witness_sha256']),64);self.assertFalse(r['image_verified']);self.assertEqual(r['verification_scope'],'specified_digital_quote_only')
  self.assertIn('趙同',para('100','p004')['text']);self.assertNotIn('趙談',para('100','p004')['text'])
 def test_social_network_inference_is_not_source_explicit_identity(self):
  for key in ['guanfu','jifu']:
   d=eq(key);self.assertEqual(d['status'],'contextual_provisional');self.assertFalse(d['human_reviewed'])
  for pid in ['h1w_44g_vef_A','lp5_fix_eqs']:
   row=next(d for d in read('data/corpus/profiles/'+pid+'.json')['reading_decisions'] if d['id'].startswith('d-shiji100'))
   self.assertTrue(any(r.get('scope')=='social_network_context_not_direct_identity_statement' for r in row['references']))
  self.assertEqual(next(m['person_id'] for m in para('120','p002')['mentions'] if m['surface']=='灌夫'),'h1w_44g_vef_A')
  self.assertEqual(next(m['person_id'] for m in para('100','p005')['mentions'] if m['surface']=='籍福'),'lp5_fix_eqs')
 def test_reader_profiles_include_human_readable_evidence(self):
  for pid in ['qyn_07y_0gt','h1w_44g_vef_A','lp5_fix_eqs']:
   p=read('data/corpus/profiles/'+pid+'.json');ds=[d for d in p.get('reading_decisions',[]) if d['id'].startswith('d-shiji100')]
   self.assertEqual(len(ds),1);self.assertTrue(ds[0]['references']);self.assertGreaterEqual(len(ds[0]['chapter_ids']),2)
  p=read('data/corpus/profiles/qyn_07y_0gt.json');self.assertIn('李奇',json.dumps(p['reading_decisions'],ensure_ascii=False))
 def test_no_blood_kinship_or_life_date_is_added_for_social_metaphor(self):
  social={'cte_yao_v47','j32_wtj_khz_A','h1w_44g_vef_A','lp5_fix_eqs'}
  self.assertFalse(any(a['subject_person_id'] in social and a['object_person_id'] in social for a in read('corpus/shiji/100-assertions.json')['assertions']))
  self.assertFalse(any(e['person_id'] in social for e in read('corpus/shiji/100-life-events.json')['events']))
 def test_all_five_retired_ids_and_json_files_are_removed(self):
  ids={p['id'] for p in read('registry/persons.json')['persons']};self.assertFalse(ids & OLD)
  for pid in OLD:
   for folder in ['data/corpus/profiles','exports/persons']:self.assertFalse((ROOT/folder/(pid+'.json')).exists())
