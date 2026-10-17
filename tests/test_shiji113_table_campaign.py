# coding: utf-8
import json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def load(f):return json.loads((R/f).read_text())
def cells():return {c['id']:c for f in load('data/historical-tables/shiji-020.json')['fragments']for r in f['rows']for c in r['cells']}
CASES={'r045':'tz9_dhl_ifo_A','r046':'8xz_mlj_r3c_A','r052':'jk8_8gt_vmi','r053':'xhk_b1m_hjb','r054':'b77_ulm_otk','r055':'h1o_o6t_3ru','r056':'m08_4xt_opo','r062':'6m0_ze7_hl0'}
OLD=['bdb_3b1_9u9','n6k_43g_m5z','10a_rgu_07z','7px_ip2_lbd','rnf_a5p_uxz','gx2_jb5_cj0','xgz_37t_knq','pt2_cpj_p1h']
class NanyueTableCampaign(unittest.TestCase):
 def test_eight_table_identities_have_native_event_evidence(self):
  cs=cells()
  for row,pid in CASES.items():
   hits=[m for cid,c in cs.items()if row in cid for m in c['person_mentions']if m['person_id']==pid];self.assertTrue(hits,row)
   for m in hits:
    for e in m['identity_evidence']:self.assertEqual(e['person_id'],pid);self.assertEqual(e['chapter_id'],'c-shiji-113-nanyue');self.assertEqual(e['source_revision'],8735632)
 def test_office_prefixes_are_not_underlined_as_names(self):
  cs=cells()
  for row,surface,start,end in [('r053','史定',13,15),('r055','居翁',11,13)]:
   c=cs['shiji-020-t1-'+row+'-c05'];m=c['person_mentions'][0];self.assertEqual((m['surface'],m['start'],m['end']),(surface,start,end));self.assertEqual(c['text'][start:end],surface);self.assertTrue(m['id'].endswith('-m000'))
 def test_four_added_anchors_identify_people_in_merit_or_short_forms(self):
  for cid,surface,pid in [('r045-c01','摎樂','tz9_dhl_ifo'),('r046-c01','韓千秋','8xz_mlj_r3c'),('r052-c06','僕','jk8_8gt_vmi'),('r056-c07','弘','m08_4xt_opo')]:
   c=cells()['shiji-020-t1-'+cid];m=c['person_mentions'][0];self.assertEqual((m['surface'],m['person_id']),(surface,pid));self.assertEqual(c['text'][m['start']:m['end']],surface)
 def test_merit_father_is_not_the_son_who_received_marquisate(self):
  cs=cells()
  for row,parent,son in [('r045','tz9_dhl_ifo','tz9_dhl_ifo_A'),('r046','8xz_mlj_r3c','8xz_mlj_r3c_A')]:
   self.assertEqual(cs['shiji-020-t1-'+row+'-c01']['person_mentions'][0]['person_id'],parent);self.assertEqual(cs['shiji-020-t1-'+row+'-c05']['person_mentions'][0]['person_id'],son)
 def test_same_fief_name_does_not_merge_unrelated_merits(self):
  cs=cells();self.assertEqual(cs['shiji-020-t1-r037-c00']['text'],'湘成。');self.assertEqual(cs['shiji-020-t1-r055-c00']['text'],'湘成。');self.assertEqual(cs['shiji-020-t1-r037-c04']['person_mentions'][0]['person_id'],'qbv_kgp_cd2');self.assertNotEqual(cs['shiji-020-t1-r037-c04']['person_mentions'][0]['person_id'],CASES['r055'])
 def test_duji_sundu_keeps_witness_names_and_explicit_ancient_note(self):
  c=load('corpus/shiji/113.json');p=next(p for p in c['paragraphs']if p['id'].endswith('p011'));self.assertIn('都稽得嘉',p['text']);self.assertEqual(cells()['shiji-020-t1-r062-c06']['person_mentions'][0]['surface'],'孫都');v=next(v for v in c['annotation']['reported_variants']if v['id']=='v-shiji113-duji-sundu');self.assertEqual(v['quote'],'徐廣曰表曰孫都');self.assertFalse(v['adopted']);self.assertFalse(v['image_verified']);self.assertIn('73c4d2ba067d99a6de924ac952fd6921a958c7e7',v['url']);self.assertEqual(len(v['response_sha256']),64)
 def test_jueweng_name_components_are_explicit_not_guessed_from_office(self):
  n=next(n for n in load('data/corpus/profile-names.json')['records']if n['person_id']=='h1o_o6t_3ru');self.assertEqual((n['title'],n['surname'],n['ming']),('桂林監','居','翁'));self.assertIn('姓居名翁',n['references'][0]['quote']);self.assertIn('監姓居名翁',n['references'][0]['raw_quote'].replace('/','').replace('\n','').replace('¶','').replace('(','').replace(')',''))
 def test_ancient_date_words_stay_in_their_own_source(self):
  cs=cells();self.assertIn('六年七月乙酉',cs['shiji-020-t1-r056-c05']['text']);self.assertIn('元年閏月癸卯',cs['shiji-020-t1-r062-c06']['text']);p=next(p for p in load('corpus/shiji/113.json')['paragraphs']if p['id'].endswith('p011'));self.assertTrue(p['text'].startswith('元鼎六年冬'));self.assertNotIn('七月乙酉',p['text'])
 def test_retired_table_candidates_have_no_active_refs_or_profile(self):
  paths=list((R/'data/historical-tables').glob('*.json'))
  for path in paths:
   text=path.read_text()
   for old in OLD:self.assertNotIn(old,text)
  for old in OLD:self.assertFalse((R/'data/corpus/profiles'/f'{old}.json').exists())
 def test_api_table_occurrences_match_persons_and_include_new_short_forms(self):
  for pid in CASES.values():self.assertTrue(any(x['table_id']=='shiji-020'for x in load('exports/persons/'+pid+'.json')['table_occurrences']))
  b=load('exports/persons/h1o_o6t_3ru.json');self.assertTrue(any(n['surname']=='居'and n['ming']=='翁'for n in b['name_components']));b=load('data/corpus/profiles/6m0_ze7_hl0.json');self.assertIn('孫都',b['names'])
if __name__=='__main__':unittest.main()
