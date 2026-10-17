import json,unittest
from pathlib import Path
from scripts.consolidate_person_ids import reference_files
from scripts.person_bundle import bundle
R=Path(__file__).resolve().parents[1]
MAPPING={'pc2_4ah_30v':'42z_cse_1ka_A','pd6_bus_9va':'q8m_d0c_kq3','nvi_c32_k29':'yqp_nlb_p1p_ACAA','fd5_bpe_y1p':'dzl_mvt_l93','os8_nvr_8zp':'y4i_pjk_4gn_A'}
def read(p):return json.loads((R/p).read_text())
class XinanyiCoreIdentities(unittest.TestCase):
 def test_five_decisions_keep_both_source_chapters_and_actual_quotes(self):
  ds=[d for d in read('corpus/shiji/116-equivalences.json')['decisions']if d['id'].startswith('eq-shiji116-core-')];self.assertEqual(len(ds),5)
  for d in ds:self.assertTrue(d['identity_materialized']);self.assertIn(d['canonical_person_id'],MAPPING.values());self.assertGreaterEqual(len(d['chapter_ids']),2);self.assertTrue(all(e['quote']and e['mention_ids']for e in d['evidence']));self.assertFalse(d['human_reviewed'])
 def test_all_fourteen_source_mentions_use_canonical_people(self):
  c=read('corpus/shiji/116.json');ms=[m for p in c['paragraphs']for m in p['mentions']if m.get('person_id')in MAPPING.values()];self.assertEqual(len(ms),14);self.assertEqual(sum(m['person_id']=='yqp_nlb_p1p_ACAA'for m in ms),10)
 def test_old_registry_ids_aliases_and_editable_references_are_retired(self):
  pids={p['id']for p in read('registry/persons.json')['persons']};self.assertFalse(set(MAPPING)&pids)
  for p in reference_files(R):
   text=p.read_text()
   for old in MAPPING:self.assertNotIn(old,text,str(p))
 def test_unresolved_rulers_and_ancestor_scope_remain_unresolved(self):
  c=read('corpus/shiji/116.json');actual=[m['id']for p in c['paragraphs']for m in p['mentions']if m.get('person_id')is None];decisions=read('corpus/shiji/116-identities.json')['decisions'];resolved={mid for decision in decisions for mid in decision['identification_basis']['target_mention_ids']};self.assertEqual(len(resolved),6);self.assertEqual(actual,[mid for mid in UNKNOWN if mid not in resolved])
 def test_received_words_and_chronology_are_unchanged(self):
  c=read('corpus/shiji/116.json');self.assertEqual(c['text_sha256'],SOURCE_HASH);p=next(p for p in c['paragraphs']if p['id'].endswith('p002'));self.assertIn('始楚威王時',p['text']);self.assertIn('楚莊王苗裔',p['text'])
 def test_person_bundle_connects_specific_chiyi_campaign_across_chapters(self):
  p=bundle('dzl_mvt_l93',R);chapters={m['chapter_id']for m in p['mentions']};self.assertIn('c-shiji-113-nanyue',chapters);self.assertIn('c-shiji-116-xinanyi',chapters);self.assertTrue(any(d['id']=='eq-shiji116-core-chiyi'for d in p['equivalence_decisions']))
UNKNOWN=['c-shiji-116-xinanyi:m001-0003', 'c-shiji-116-xinanyi:m001-0032', 'c-shiji-116-xinanyi:m001-0090', 'c-shiji-116-xinanyi:m001-0106', 'c-shiji-116-xinanyi:m001-0125', 'c-shiji-116-xinanyi:m001-0158', 'c-shiji-116-xinanyi:m003-0156', 'c-shiji-116-xinanyi:m006-0018', 'c-shiji-116-xinanyi:m007-0113', 'c-shiji-116-xinanyi:m007-0132', 'c-shiji-116-xinanyi:m009-0016', 'c-shiji-116-xinanyi:m009-0021', 'c-shiji-116-xinanyi:m009-0089', 'c-shiji-116-xinanyi:m009-0100', 'c-shiji-116-xinanyi:m009-0127', 'c-shiji-116-xinanyi:m010-0003', 'c-shiji-116-xinanyi:m011-0000', 'c-shiji-116-xinanyi:m011-0041']
SOURCE_HASH='d043ccd2b62c440d41ac0e05afa9c4a8bea5c7c08938d24992d8fdfab8192247'
if __name__=='__main__':unittest.main()
