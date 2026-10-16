# coding: utf-8
import json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def load(f):return json.loads((R/f).read_text())
def cells():return {c['id']:c for f in load('data/historical-tables/shiji-020.json')['fragments']for r in f['rows']for c in r['cells']}
class HeqiChangleVariants(unittest.TestCase):
 def test_different_written_names_join_only_with_context(self):
  cs=cells()
  for cid,s,pid in [('r032-c04','烏犁','2xh_q5y_5zo'),('r033-c04','稠雕','ltc_bon_w6p')]:
   c=cs['shiji-020-t1-'+cid];m=c['person_mentions'][0];self.assertEqual((m['surface'],m['person_id']),(s,pid));self.assertEqual(c['text'][m['start']:m['end']],s);self.assertIn('三年七月壬午',c['text']);self.assertTrue(m['identity_evidence']);self.assertIn('差異分存',m['interpretation_note'])
 def test_native_short_name_and_text_remain_literal(self):
  p=next(p for p in load('corpus/shiji/111.json')['paragraphs']if p['id'].endswith(':p013'));self.assertIn('禽為河綦侯，大當戶銅離為常樂侯',p['text']);m=next(m for m in p['mentions']if m['id'].endswith('m013-0244'));self.assertEqual((m['surface'],m['start'],m['end']),('禽',244,245))
 def test_each_person_has_three_fixed_references(self):
  ds=load('corpus/shiji/111-identities.json')['decisions']
  for slug in ['heqi','changle']:
   d=next(d for d in ds if d['id']=='d-shiji111-'+slug+'-variants');self.assertFalse(d['human_reviewed']);self.assertEqual(len(d['references']),3)
   for ref in d['references']:self.assertFalse(ref['image_verified']);self.assertIn('/blob/',ref['url']);self.assertTrue(ref['raw_quote']);self.assertEqual(len(ref['source_blob_sha']),40)
  d=next(d for d in ds if d['id']=='d-shiji111-changle-variants');ref=next(r for r in d['references']if '前漢書'in r['title']);self.assertIn('<pb:',ref['raw_quote']);self.assertIn('稠睢',ref['quote'])
 def test_successor_is_independent_candidate_without_invented_father(self):
  c=cells()['shiji-020-t1-r032-c05'];m=c['person_mentions'][0];self.assertEqual(m['surface'],'餘利鞮');self.assertEqual(c['text'][m['start']:m['end']],'餘利鞮');p=next(p for p in load('data/historical-tables/person-candidates.json')['persons']if p['id']==m['person_id']);self.assertNotIn('family_path',p);self.assertNotEqual(p['id'],'2xh_q5y_5zo');self.assertIn('不由同列繼侯推父子',p['identity_note'])
 def test_hunye_and_retirement(self):
  cs=cells()
  for cid in ['r032-c01','r033-c01']:self.assertEqual(cs['shiji-020-t1-'+cid]['person_mentions'][0]['person_id'],'164_wmw_9ck')
  for pid in ['ylo_qcd_loq','m2d_ww2_297']:
   self.assertNotIn(pid,{p['id']for p in load('data/historical-tables/person-candidates.json')['persons']});self.assertFalse((R/'data/corpus/profiles'/(pid+'.json')).exists())
