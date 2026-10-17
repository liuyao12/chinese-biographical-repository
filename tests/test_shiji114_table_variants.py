# coding:utf-8
import copy,json,re,unittest
from pathlib import Path
from scripts.person_bundle import bundle,validate_name_component_alternatives
from scripts.historical_tables import validate_identity_evidence
R=Path(__file__).resolve().parents[1]
TARGETS={'r057':('0j7_7f9_87r','bxw_vv0_1t3','吳陽'),'r060':('bc9_mt7_eye','08e_bwz_ync','轅終古'),'r061':('orj_n7c_wx6','43i_62q_gf6','建成'),'r063':('gzx_hby_fdp','1bh_uew_js1','居服'),'r064':('bft_z34_73i','7ty_ab1_ab9','多軍')}
NEW={'r057-c01':[('東越衍侯','bxw_vv0_1t3'),('繇王','1bh_uew_js1'),('餘善','ub3_zen_skw')],'r060-c01':[('徇北將軍','u5g_scl_2bs')],'r060-c07':[('終古','08e_bwz_ync')],'r061-c01':[('東越建成侯','43i_62q_gf6'),('繇王','1bh_uew_js1'),('餘善','ub3_zen_skw')],'r063-c01':[('東越繇王','1bh_uew_js1'),('餘善','ub3_zen_skw')],'r064-c01':[('東越將軍','7ty_ab1_ab9')]}
def load(f):return json.loads((R/f).read_text())
class DongyueTableVariants(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.t=load('data/historical-tables/shiji-020.json');cls.cells={c['id']:c for f in cls.t['fragments']for r in f['rows']for c in r['cells']};cls.names={n['person_id']:n for n in load('data/corpus/profile-names.json')['records']};cls.ds={d['id']:d for d in load('corpus/shiji/114-identities.json')['decisions']}
 def cell(self,suffix):return self.cells['shiji-020-t1-'+suffix]
 def test_five_old_table_candidates_link_to_sourced_canonical_people(self):
  candidates={p['id']for p in load('data/historical-tables/person-candidates.json')['persons']};people={p['id']for p in load('registry/persons.json')['persons']}
  for row,(old,pid,surface)in TARGETS.items():
   self.assertNotIn(old,candidates);self.assertIn(pid,people);m=self.cell(row+'-c06')['person_mentions'][0];self.assertEqual((m['person_id'],m['surface']),(pid,surface));self.assertEqual(m['id'],self.cell(row+'-c06')['id']+'-m000');self.assertEqual(m['identity_evidence'][0]['person_id'],pid);validate_identity_evidence(m,R)
 def test_eleven_new_role_or_short_name_anchors_are_exact_and_sourced(self):
  found=0
  for suffix,expected in NEW.items():
   c=self.cell(suffix);self.assertEqual([(m['surface'],m['person_id'])for m in c['person_mentions']],expected)
   for m in c['person_mentions']:self.assertEqual(c['text'][m['start']:m['end']],m['surface']);validate_identity_evidence(m,R);found+=1
  self.assertEqual(found,11)
 def test_received_words_and_fixed_revisions_are_not_silently_corrected(self):
  self.assertEqual(self.t['source']['revision'],'2607036');self.assertEqual(self.t['source']['response_sha256'],'f3fb3f9b7ead59e58f522014810ad9faf46b4723ba0b65f6175d72422aa6e0f8');self.assertEqual(self.cell('r060-c00')['text'],'蘌兒。');self.assertIn('侯建成元年',self.cell('r061-c06')['text']);self.assertIn('侯居服元年',self.cell('r063-c06')['text']);c=load('corpus/shiji/114.json');self.assertEqual(c['text_sha256'],'b38ea0d040864a0368385740200d92755990ada0d0d3676e768cff945a22fc6f');self.assertTrue(any('繇王居股'in p['text']for p in c['paragraphs']))
 def test_chengcheng_reading_does_not_replace_aos_preferred_name(self):
  n=self.names['43i_62q_gf6'];self.assertEqual((n['surname'],n['ming']),(None,'敖'));self.assertIn('建成侯',n['additional_names']);d=self.ds['d-shiji114-table-r061'];self.assertIn('不將它當敖的確證本名',d['rationale']);self.assertTrue(any('疑表誤'in ref['quote']for ref in d['references']))
 def test_jufu_jugu_identity_keeps_source_difference_and_chou_distinct(self):
  d=self.ds['d-shiji114-table-r063'];self.assertIn('居服',d['rationale']);self.assertIn('居股',d['rationale']);b=bundle('1bh_uew_js1',R,include_provisional=True);self.assertEqual(b['person_ids'],['1bh_uew_js1']);self.assertNotIn('e00_pe1_zri_*A',b['person_ids'])
 def test_next_beishi_holder_shou_is_not_wuyang_or_automatically_his_son(self):
  m=self.cell('r057-c07')['person_mentions'][0];self.assertEqual((m['surface'],m['person_id']),('首','76z_zdc_38o'));self.assertIn(m['person_id'],{p['id']for p in load('data/historical-tables/person-candidates.json')['persons']});self.assertNotEqual(m['person_id'],TARGETS['r057'][1])
 def test_yuans_surname_segmentation_has_explicit_commentary_not_character_count(self):
  n=self.names['08e_bwz_ync'];self.assertEqual((n['surname'],n['ming']),('轅','終古'));self.assertTrue(any(r['quote']=='榬姓終古名也'for r in n['references']));self.assertIn('榬',n['note']);self.assertIn('御兒侯',n['title'])
 def test_wuyang_and_jugu_are_not_mechanically_split_into_surnames(self):
  self.assertNotIn('bxw_vv0_1t3',self.names);self.assertNotIn('1bh_uew_js1',self.names)
 def test_multichar_name_default_and_other_scholars_split_are_both_parseable(self):
  n=self.names['7ty_ab1_ab9'];validate_name_component_alternatives(n);self.assertEqual((n['surname'],n['ming']),(None,'多軍'));alt=n['component_alternatives'][0];self.assertEqual(alt['components'],dict(surname='多',ming='軍',zi=None));self.assertEqual(alt['source_terms'],dict(surname='多姓',ming='軍名也'));self.assertEqual(alt['status'],'source_claim_not_selected')
 def test_split_name_grammar_requires_one_exact_explicit_source_phrase(self):
  for kind in ['wrong_surname','separate_clauses','wrong_ming','wrong_term','source_commit','raw_quote']:
   n=copy.deepcopy(self.names['7ty_ab1_ab9']);a=n['component_alternatives'][0]
   if kind=='wrong_surname':a['components']['surname']='居'
   elif kind=='separate_clauses':a['reference'].update(quote='多姓，軍名也',raw_quote='多姓，軍名也')
   elif kind=='wrong_ming':a['components']['ming']='多軍'
   elif kind=='wrong_term':a['source_terms']['surname']='多姓也'
   elif kind=='source_commit':a['reference']['source_commit']='0'*40
   else:a['reference']['raw_quote']='synthetic unrelated text'
   with self.assertRaises(ValueError,msg=kind):validate_name_component_alternatives(n)
 def test_primary_commentary_quotes_are_present_in_fixed_raw_quotes(self):
  for d in self.ds.values():
   if not d['id'].startswith('d-shiji114-table-'):continue
   for ref in d['references']:
    if 'raw_quote'in ref:
     normalized=re.sub(r'<pb:[^>]*>','',ref['raw_quote']);normalized=re.sub(r'[()/¶\s]','',normalized);self.assertIn(ref['quote'],normalized);self.assertIn(ref['source_commit'],ref['url']);self.assertFalse(ref['image_verified'])
 def test_every_table_judgment_has_full_cell_and_received_paragraph(self):
  for row,(old,pid,surface)in TARGETS.items():
   d=self.ds['d-shiji114-table-'+row];ref=d['references'][0];self.assertEqual(d['person_id'],pid);self.assertFalse(d['human_reviewed']);self.assertEqual(ref['quote'],self.cell(row+'-c06')['text']);self.assertEqual(ref['source_revision'],'2607036');self.assertTrue(d['evidence'][0]['quote'])
 def test_existing_wang_and_chengyang_families_remain_parseable(self):
  self.assertEqual(bundle('r5s_lra_wfi',R)['person_ids'],['r5s_lra_wfi']);self.assertEqual(bundle('yqp_nlb_p1p_ABFAC',R)['family_paths'][0]['parent_person_id'],'yqp_nlb_p1p_ABFA')
if __name__=='__main__':unittest.main()
