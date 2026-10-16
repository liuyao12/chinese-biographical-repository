# coding: utf-8
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(f):return json.loads((ROOT/f).read_text())
def para(n):return next(p for p in load('corpus/shiji/111.json')['paragraphs']if p['id'].endswith(':p'+str(n).zfill(3)))
def cell(cid):return next(c for f in load('data/historical-tables/shiji-020.json')['fragments']for r in f['rows']for c in r['cells']if c['id']==cid)
class JuWangTables(unittest.TestCase):
 def test_literal_text_preserved_two_nonoverlapping_persons(self):
  p=para(12);self.assertIn('校尉句王高不識',p['text']);a=next(m for m in p['mentions']if m['id']=='c-shiji-111-wei-huo:m012-0356');b=next(m for m in p['mentions']if m['id']=='c-shiji-111-wei-huo:m012-0356-juwang');self.assertEqual((a['start'],a['end'],a['surface'],a['person_id']),(358,361,'高不識','1fa_jx6_oun'));self.assertEqual((b['start'],b['end'],b['surface'],b['person_id']),(356,358,'句王','qcc_x7d_rqk'));self.assertEqual(b['end'],a['start'])
 def test_new_person_is_not_fabricated_family_or_gaos_alias(self):
  ps={p['id']:p for p in load('registry/persons.json')['persons']};self.assertNotIn('family_path',ps['qcc_x7d_rqk']);self.assertNotIn('句王高不識',[a['surface']for a in ps['1fa_jx6_oun']['aliases']]);self.assertEqual(ps['1fa_jx6_oun']['label'],'高不識');self.assertEqual(len(ps['qcc_x7d_rqk']['evidence']),1)
 def test_only_gao_gets_yiguan_ju_has_unknown_endpoints(self):
  hs=load('corpus/shiji/111-titles.json')['holdings'];self.assertTrue(any(h['title']=='宜冠侯'and h['person_id']=='1fa_jx6_oun'for h in hs));ju=[h for h in hs if h['person_id']=='qcc_x7d_rqk'];self.assertEqual({h['title']for h in ju},{'句王','校尉'})
  for h in ju:
   self.assertEqual(h['mode'],'attestation');self.assertEqual(h['effective_period']['start']['status'],'unknown');self.assertEqual(h['effective_period']['end']['status'],'unknown');self.assertEqual(h['attestations'][0]['normalized_date']['year'],-120)
 def test_fixed_raw_commentary_references_and_distinction(self):
  ds=load('corpus/shiji/111-identities.json')['decisions'];d=next(d for d in ds if d['id']=='d-shiji111-juwang-split');self.assertTrue(any('按二人並匈奴人也'==r['quote']for r in d['references']))
  for r in d['references']:self.assertIn('/blob/',r['url']);self.assertFalse(r['image_verified']);self.assertTrue(r['raw_quote']);self.assertEqual(len(r['source_blob_sha']),40)
  self.assertFalse(d['human_reviewed']);self.assertTrue(any(set(d['person_ids'])=={'qcc_x7d_rqk','1fa_jx6_oun'}for d in load('corpus/shiji/111-distinctions.json')['distinctions']))
 def test_two_reported_puduo_spellings_are_not_adopted(self):
  vs=[v for v in load('corpus/shiji/111.json')['annotation']['reported_variants']if v.get('id')in ['rv-shiji111-puming','rv-shiji111-pupeng']];self.assertEqual({v['reported_reading']for v in vs},{'僕明','僕朋'})
  for v in vs:self.assertFalse(v['adopted']);self.assertFalse(v['image_verified']);self.assertIn('轉引',v['commentator'])
  self.assertTrue(any(m['surface']=='僕多'and m.get('person_id')=='zqj_u2i_r5y'for m in para(12)['mentions']))
 def test_table_puduo_and_yingbi_not_collapsed_by_same_title(self):
  a=cell('shiji-020-t1-r027-c04');b=cell('shiji-020-t1-r031-c04');c=cell('shiji-020-t1-r031-c05');self.assertEqual(a['person_mentions'][0]['person_id'],'zqj_u2i_r5y');self.assertEqual(b['person_mentions'][0]['person_id'],'dy9_czc_11p');self.assertEqual(c['person_mentions'][0]['person_id'],'dy9_czc_11p');self.assertNotEqual(a['person_mentions'][0]['person_id'],b['person_mentions'][0]['person_id']);self.assertIn('僕多。。',a['text']);self.assertIn('三年七月壬午',b['text']);self.assertIn('扁訾死',c['text'])
 def test_retired_table_candidate_is_removed_without_redirect(self):
  self.assertNotIn('2xp_j46_zr3',{p['id']for p in load('data/historical-tables/person-candidates.json')['persons']});self.assertFalse((ROOT/'data/corpus/profiles/2xp_j46_zr3.json').exists())
 def test_profile_exposes_readable_sources_and_precise_occurrences(self):
  ju=load('data/corpus/profiles/qcc_x7d_rqk.json');high=load('data/corpus/profiles/1fa_jx6_oun.json');self.assertNotIn('句王高不識',high['names']);self.assertIn('句王',ju['names']);self.assertTrue(any(o['number']==111for o in ju['occurrences']));y=load('data/corpus/profiles/dy9_czc_11p.json');self.assertEqual(len([o for o in y['table_occurrences']if o['cell_id'].startswith('shiji-020-t1-r031')]),2)
