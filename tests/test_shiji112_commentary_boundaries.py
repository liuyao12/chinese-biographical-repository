# coding: utf-8
import json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def load(f):return json.loads((R/f).read_text())
def para(k):return next(p for p in load('corpus/shiji/112.json')['paragraphs']if p['id'].endswith(':p'+str(k).zfill(3)))
def decision(did):return next(d for d in load('corpus/shiji/112-identities.json')['decisions']if d['id']==did)
def cells():return {c['id']:c for f in load('data/historical-tables/shiji-020.json')['fragments']for r in f['rows']for c in r['cells']}
class CommentaryBoundaries(unittest.TestCase):
 def test_cheng_retains_identity_and_anchor_but_not_the_verb(self):
  p=para(13);m=next(m for m in p['mentions']if m['id']=='c-shiji-112-pingjin:m013-0030');self.assertEqual((m['start'],m['end'],m['surface'],m['person_id']),(30,31,'成','lve_fqh_8v6'));self.assertIn('御史成進諫曰',p['text']);self.assertFalse(any(m['start']<=31<m['end']for m in p['mentions']));who=next(p for p in load('registry/persons.json')['persons']if p['id']=='lve_fqh_8v6');self.assertFalse(any(a['surface']=='成進'for a in who['aliases']));self.assertIn('姓名未詳',who['label'])
 def test_parallel_han_reference_keeps_partial_extent_and_original_spelling(self):
  r=decision('d-shiji112-cheng-word-boundary')['references'][0];self.assertIn('成諌曰不可',r['raw_quote']);self.assertEqual(r['response_extent'],dict(first_line=320,last_line=440,partial_file=True));self.assertIn('683113d4baf6febecaf2ccb7913df87c4d68d454',r['url']);self.assertFalse(r['image_verified'])
 def test_bracketed_tuo_is_identified_without_swallowing_tusui(self):
  p=para(19);m=next(m for m in p['mentions']if m['surface']=='尉[佗]');t=next(m for m in p['mentions']if m['surface']=='屠睢');self.assertEqual((m['start'],m['end'],m['person_id']),(204,208,'bvb_d1z_fd0'));self.assertEqual(t['start'],208);self.assertNotEqual(m['person_id'],t['person_id']);d=decision('d-shiji112-tuo-bracket-reading');self.assertTrue(any('他趙他也'in r['quote']for r in d['references']));self.assertTrue(any(r['scope']=='received_parallel_without_tuo_at_first_campaign'for r in d['references']));self.assertIn('尉[佗]屠睢',p['text'])
 def test_yan_zhuang_is_only_a_reported_surname_substitution(self):
  v=next(v for v in load('corpus/shiji/112.json')['annotation']['reported_variants']if v['id']=='v-shiji112-yan-zhuang-surname');self.assertEqual((v['component'],v['received_reading'],v['reported_reading']),('surname','嚴','莊'));self.assertFalse(v['adopted']);self.assertIn('本姓莊避明帝諱',v['quote']);self.assertIn('齊人嚴安',para(14)['text'])
 def test_qing_and_du_share_heir_identity_but_preserve_both_spellings(self):
  cc=cells();mid=next(m['person_id']for m in para(9)['mentions']if m['surface']=='度');self.assertEqual(mid,'q69_35n_f3h_A')
  for cid,start in [('shiji-020-t1-r008-c04',8),('shiji-020-t1-r008-c06',6)]:
   m=cc[cid]['person_mentions'][0];self.assertEqual((m['start'],m['end'],m['surface'],m['person_id']),(start,start+1,'慶',mid));self.assertTrue(any(e['person_id']==mid and '度為山陽太守'in e['quote']for e in m['identity_evidence']))
  self.assertIn('三年，侯慶元年',cc['shiji-020-t1-r008-c04']['text']);self.assertIn('元狩二年，弘病',para(9)['text']);self.assertNotIn('9s1_kcw_h0h',{p['id']for p in load('data/historical-tables/person-candidates.json')['persons']})
  for folder in ['exports/persons','data/corpus/profiles']:self.assertFalse((R/folder/'9s1_kcw_h0h.json').exists())
 def test_degree_heading_has_sourced_title_and_ming_without_invented_surname(self):
  n=next(n for n in load('data/corpus/profile-names.json')['records']if n['person_id']=='q69_35n_f3h_A');self.assertEqual((n['title'],n['surname'],n['ming']),('平津侯',None,'度'));self.assertEqual(n['additional_names'],['慶']);self.assertIn(n['quote'],para(9)['text']);self.assertEqual({r['table_cell_id']for r in n['references']},{'shiji-020-t1-r008-c04','shiji-020-t1-r008-c06'})
