# coding: utf-8
import json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def load(f):return json.loads((R/f).read_text())
def para(n,k):return next(p for p in load('corpus/shiji/'+n+'.json')['paragraphs']if p['id'].endswith(':p'+str(k).zfill(3)))
class HouTableIdentities(unittest.TestCase):
 def test_document_signature_refers_to_huo(self):
  for k in [1,2,7]:
   self.assertTrue(all(m['person_id']=='3tw_nq2_gyn'for m in para('060',k)['mentions']if m['surface']=='去病'))
  d=next(d for d in load('corpus/shiji/111-equivalences.json')['decisions']if d['id']=='eq-shiji111-houlinks-huo');self.assertIn('不等於已證親撰',d['rationale'])
 def test_hunye_same_surrender_not_hereditary_name(self):
  for n,k in [('123',16),('111',13),('110',37)]:
   ms=[m for m in para(n,k)['mentions']if m['surface']=='渾邪王'];self.assertTrue(ms);self.assertEqual({m['person_id']for m in ms},{'164_wmw_9ck'})
 def test_table_short_forms_and_commanders_exact(self):
  cells={c['id']:c for f in load('data/historical-tables/shiji-020.json')['fragments']for row in f['rows']for c in row['cells']}
  for cid,s,pid in [('r022-c04','騫','gqj_xdu_8rf'),('r024-c04','賢','ldw_cby_hek'),('r026-c04','不識','1fa_jx6_oun'),('r028-c07','破奴','z0l_1wp_de1'),('r030-c01','渾邪王','164_wmw_9ck')]:
   c=cells['shiji-020-t1-'+cid];ms=[m for m in c['person_mentions']if m['surface']==s];self.assertTrue(ms);self.assertEqual({m['person_id']for m in ms},{pid})
   for m in ms:self.assertEqual(c['text'][m['start']:m['end']],s);self.assertTrue(m['identity_evidence'])
 def test_distinct_juwang_and_gaobushi(self):
  p=para('111',12);a=next(m for m in p['mentions']if m['id'].endswith('m012-0356'));b=next(m for m in p['mentions']if m['id'].endswith('m012-0356-juwang'));self.assertEqual(a['person_id'],'1fa_jx6_oun');self.assertEqual(b['person_id'],'qcc_x7d_rqk');self.assertEqual(b['end'],a['start'])
 def test_retired_ids_absent_and_profiles_join_sources(self):
  old=['kgo_dqk_ti0','20n_l53_kkr','lqs_y56_2ws','j6d_o09_36i','ley_h0n_2ex','qd5_pe6_fde','717_0mk_i1a','svx_gml_av2','zdy_xdv_xic','z6k_c47_hl0','q43_8vs_cxd','045_eb8_rg7']
  for pid in old:
   self.assertNotIn(pid,{p['id']for p in load('registry/persons.json')['persons']});self.assertNotIn(pid,{p['id']for p in load('data/historical-tables/person-candidates.json')['persons']})
   for folder in ['exports/persons','data/corpus/profiles']:self.assertFalse((R/folder/(pid+'.json')).exists())
  p=load('data/corpus/profiles/3tw_nq2_gyn.json');self.assertTrue({60,111}<={o['number']for o in p['occurrences']});self.assertTrue(any(o['cell_id']=='shiji-020-t1-r023-c03'for o in p['table_occurrences']))
