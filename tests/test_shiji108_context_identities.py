# coding: utf-8
import json
import unittest
from pathlib import Path
from scripts.person_bundle import bundle, load_catalog
ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text())
class HanContextIdentities(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.catalog=load_catalog(ROOT)
 def test_four_groups_materialized_with_own_chapter_and_sources(self):
  ds=[d for d in load('corpus/shiji/108-equivalences.json')['decisions']if d['id'].startswith('eq-shiji108-context-')]
  self.assertEqual([d['canonical_person_id']for d in ds],['z2v_oh4_mhm','xp5_39k_w5w','zuf_oll_649','yqp_nlb_p1p_ACF'])
  for d in ds:
   self.assertEqual(d['person_ids'],[d['canonical_person_id']]);self.assertTrue(d['identity_materialized']);self.assertFalse(d['human_reviewed']);self.assertIn('c-shiji-108-han',d['chapter_ids']);self.assertTrue(all(e['mention_ids']for e in d['evidence']))
 def test_king_identity_preserves_conflicting_polity_wording(self):
  c=load('corpus/shiji/108.json');p=next(p for p in c['paragraphs']if p['id'].endswith('p006'))
  self.assertIn('閩越、東越相攻',p['text']);self.assertEqual(next(m['person_id']for m in p['mentions']if m['surface']=='王'),'xp5_39k_w5w')
  c=load('corpus/shiji/114.json');p=next(p for p in c['paragraphs']if p['id'].endswith('p004'));self.assertIn('閩越擊南越',p['text'])
 def test_gongsun_ao_office_difference_not_silently_reconciled(self):
  d=next(d for d in load('corpus/shiji/108-equivalences.json')['decisions']if d['id']=='eq-shiji108-context-gongsunao')
  self.assertTrue(any('爲中將軍從大將軍'in e['quote']for e in d['evidence']));self.assertTrue(any('後二歲，以校尉從大將軍'in e['quote']for e in d['evidence']))
  self.assertIn('官稱',d['rationale'])
 def test_princess_keeps_recorded_son_without_inventing_father(self):
  c=load('corpus/shiji/011.json');p=next(p for p in c['paragraphs']if p['id'].endswith('p006'));self.assertEqual(next(m['person_id']for m in p['mentions']if m['surface']=='長公主'),'yqp_nlb_p1p_ACF')
  assertions=load('corpus/shiji/011-assertions.json')['assertions'];a=next(a for a in assertions if a['subject_person_id']=='dep_bjj_vwe'and a['predicate']=='mother');self.assertEqual(a['object_person_id'],'yqp_nlb_p1p_ACF')
 def test_six_old_ids_have_no_registry_or_json_replacements(self):
  ids={p['id']for p in load('registry/persons.json')['persons']}
  for pid in ['4gs_22r_d9a','px6_0om_awh','kha_4p3_834','suw_tds_nwl','kvm_6zv_6ez','9v3_xea_50v']:
   self.assertNotIn(pid,ids)
   for directory in ['exports/persons','data/corpus/profiles']:self.assertFalse((ROOT/directory/(pid+'.json')).exists())
 def test_table_min_yue_king_uses_biographical_evidence(self):
  t=load('data/historical-tables/shiji-022.json');c=next(c for f in t['fragments']for r in f['rows']for c in r['cells']if c['id']=='shiji-022-t1-r072-c02');m=next(m for m in c['person_mentions']if m['surface']=='閩越王');self.assertEqual(m['person_id'],'xp5_39k_w5w');self.assertEqual(m['identity_evidence'][0]['chapter_id'],'c-shiji-114-dongyue');self.assertIn('孝景太后崩。。',c['text'])
 def test_distinction_exports_evidence_without_merging_people(self):
  for pid,other in [('z2v_oh4_mhm','4qp_wu1_qhe'),('4qp_wu1_qhe','z2v_oh4_mhm')]:
   b=bundle(pid,catalog=self.catalog);d=next(d for d in b['identity_distinctions']if d['id']=='distinct-shiji108-wanghui');self.assertEqual(b['person_ids'],[pid]);self.assertIn(other,{p['id']for p in b['persons']});self.assertTrue(all(m['person_id']==pid for m in b['mentions']));self.assertTrue(all(t['person_id']==pid for t in b['title_holdings']))
   for e in d['evidence']:
    p=next(p for p in b['passages']if p['id']==e['paragraph_id']);self.assertEqual(e['work_id'],p['work_id']);self.assertEqual(e['book_id'],p['book_id']);self.assertIn(e['quote'],p['text'])
  self.assertNotIn('identity_distinctions',bundle('z6u_kf1_554',catalog=self.catalog))
