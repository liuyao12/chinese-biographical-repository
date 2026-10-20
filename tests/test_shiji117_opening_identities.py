import json,unittest
from pathlib import Path
from scripts.consolidate_person_ids import reference_files
R=Path(__file__).resolve().parents[1]
MAPPING={'dmr_myf_9k4':'yqp_nlb_p1p_ACA','pfb_62k_tz3':'yqp_nlb_p1p_ACG','wz9_alv_i3k':'06n_ttw_xgt','3a1_wug_71s':'sfa_wwl_tt2','n89_ouw_0ix':'g8d_9kf_uqg','gnf_v23_0ks':'e1m_xt0_8w7'}
def read(p):return json.loads((R/p).read_text())
class XiangruOpeningIdentities(unittest.TestCase):
 def test_six_materialized_decisions_keep_exact_cross_chapter_evidence(self):
  ds=[d for d in read('corpus/shiji/117-equivalences.json')['decisions']if d['id'].startswith('eq-shiji117-opening-')];self.assertEqual(len(ds),6)
  for d in ds:self.assertTrue(d['identity_materialized']);self.assertEqual(d['person_ids'],[d['canonical_person_id']]);self.assertIn(d['canonical_person_id'],MAPPING.values());self.assertEqual(len(d['chapter_ids']),2);self.assertTrue(all(e['quote']and e['mention_ids']for e in d['evidence']));self.assertFalse(d['human_reviewed'])
 def test_opening_references_use_named_context_not_new_candidates(self):
  p=read('corpus/shiji/117.json')['paragraphs'][0];ms={m['surface']:m['person_id']for m in p['mentions']};self.assertEqual({k:ms[k]for k in ['孝景帝','景帝','梁孝王','鄒陽','莊忌','枚乘','藺相如']},{'孝景帝':'yqp_nlb_p1p_ACA','景帝':'yqp_nlb_p1p_ACA','梁孝王':'yqp_nlb_p1p_ACG','鄒陽':'06n_ttw_xgt','莊忌':'g8d_9kf_uqg','枚乘':'e1m_xt0_8w7','藺相如':'sfa_wwl_tt2'})
 def test_meisheng_and_meicheng_share_huaiyin_and_liang_companions(self):
  c=read('corpus/shiji/083.json');p=next(p for p in c['paragraphs']if p['id'].endswith('p015'));self.assertIn('淮陰枚生',p['text']);self.assertEqual(next(m['person_id']for m in p['mentions']if m['surface']=='枚生'),'e1m_xt0_8w7');self.assertEqual(next(m['person_id']for m in p['mentions']if m['surface']=='莊忌夫子'),'g8d_9kf_uqg')
 def test_old_ids_have_no_live_registry_files_or_editable_references(self):
  people={p['id']for p in read('registry/persons.json')['persons']};self.assertFalse(set(MAPPING)&people)
  for old in MAPPING:
   self.assertFalse((R/f'exports/persons/{old}.json').exists());self.assertFalse((R/f'data/corpus/profiles/{old}.json').exists())
  for p in reference_files(R):
   for old in MAPPING:self.assertNotIn(old,p.read_text(),str(p))
 def test_linxiangru_is_not_sima_xiangru_and_confidence_is_not_overstated(self):
  p=read('corpus/shiji/117.json')['paragraphs'][0];self.assertEqual(next(m['person_id']for m in p['mentions']if m['surface']=='司馬相如'),'usb_lgr_ksa');self.assertEqual(next(m['person_id']for m in p['mentions']if m['surface']=='藺相如'),'sfa_wwl_tt2');d=next(d for d in read('corpus/shiji/117-equivalences.json')['decisions']if d['id']=='eq-shiji117-opening-linxiangru');self.assertEqual(d['confidence_level'],'moderate');self.assertIn('未重敘',d['rationale'])
 def test_emperor_candidate_is_not_blindly_merged_into_wudi(self):
  c=read('corpus/shiji/117.json');p=next(p for p in c['paragraphs']if p['id'].endswith('p003'));ms=[m for m in p['mentions']if m['surface']in ['上','天子']];self.assertEqual(len(ms),9);self.assertEqual(sum(m['person_id']=='yqp_nlb_p1p_ACAA' for m in ms),7);self.assertEqual(sum(m['person_id'] is None for m in ms),2)
 def test_resolved_display_labels_drop_candidate_scaffolding(self):
  people={p['id']:p for p in read('registry/persons.json')['persons']}
  for pid in MAPPING.values():
   p=people[pid];self.assertNotIn('候選',p['label']);self.assertNotIn('本卷未名',p['label']);self.assertTrue(any(p['label']in a['surface']for a in p['aliases']))
 def test_fictional_fu_speakers_and_qi_king_are_not_historical_people(self):
  c=read('corpus/shiji/117.json');p=next(p for p in c['paragraphs']if p['id'].endswith('p004'));self.assertEqual(len(p['mentions']),8);self.assertTrue(all(m['person_id']is None for m in p['mentions']));self.assertIn('故空藉此三人為辭',c['paragraphs'][2]['text'])
if __name__=='__main__':unittest.main()
