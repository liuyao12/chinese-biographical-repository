import json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
MAPPING={'ykt_rg0_cl9':'jjl_irg_zke_A','m6a_2rx_afc':'yqp_nlb_p1p_AA','26o_acg_bzw':'i30_mjq_6q8_A','5w8_533_9xk':'yqp_nlb_p1p_ACAA','3zz_xwh_g2j':'pme_eis_xqi_*A*AAAAA'}
def read(p):return json.loads((R/p).read_text())
class ChaoxianCoreIdentities(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=read('corpus/shiji/115.json');cls.people={p['id']:p for p in read('registry/persons.json')['persons']};cls.ds=[d for d in read('corpus/shiji/115-equivalences.json')['decisions']if d['id'].startswith('eq-shiji115-core-')]
 def test_five_materialized_decisions_retain_distinct_source_anchors(self):
  self.assertEqual(len(self.ds),5);self.assertEqual({d['canonical_person_id']for d in self.ds},set(MAPPING.values()))
  for d in self.ds:self.assertTrue(d['identity_materialized']);self.assertEqual(d['person_ids'],[d['canonical_person_id']]);self.assertGreaterEqual(len(d['chapter_ids']),2);self.assertGreaterEqual(len({m for e in d['evidence']for m in e['mention_ids']}),2)
 def test_old_ids_have_no_registry_reader_or_bundle_files(self):
  for old in MAPPING:self.assertNotIn(old,self.people);self.assertFalse((R/'exports/persons'/f'{old}.json').exists());self.assertFalse((R/'data/corpus/profiles'/f'{old}.json').exists())
 def test_all_editable_reference_layers_retire_old_ids(self):
  paths=list((R/'registry').glob('*.json'))+list((R/'corpus').glob('*/*.json'))+list((R/'data/historical-tables').glob('*.json'))
  for p in paths:
   s=p.read_text()
   for old in MAPPING:self.assertNotIn(old,s,str(p))
 def test_huihou_period_two_ruler_anchors_stay_unresolved(self):
  p=next(p for p in self.c['paragraphs']if p['id'].endswith('p002'));ms=[m for m in p['mentions']if m['surface']in ['天子','上']];self.assertEqual(len(ms),2)
  for m in ms:self.assertEqual(m['kind'],'unresolved');self.assertIsNone(m['person_id'])
 def test_ten_yuanfeng_ruler_mentions_use_wudi_and_preserve_surfaces(self):
  ds=next(d for d in self.ds if d['id']=='eq-shiji115-core-wudi');mids={mid for e in ds['evidence']if e['chapter_id']==self.c['id']for mid in e['mention_ids']};ms=[m for p in self.c['paragraphs']for m in p['mentions']if m['id']in mids];self.assertEqual(len(ms),10);self.assertEqual({m['person_id']for m in ms},{'yqp_nlb_p1p_ACAA'});self.assertEqual({m['surface']for m in ms},{'天子','上'})
 def test_luwan_keeps_existing_attested_father(self):self.assertEqual(self.people['jjl_irg_zke_A']['family_path']['parent_person_id'],'jjl_irg_zke')
 def test_author_has_specific_self_preface_authorship_reference(self):
  d=next(d for d in self.ds if d['id']=='eq-shiji115-core-qian');self.assertTrue(any('作朝鮮列傳第五十五'in x['quote']for x in d['references']));self.assertTrue(any(e['paragraph_id']=='c-shiji-130-taishigong:p007'and '遷為太史令'in e['quote']for e in d['evidence']))
 def test_unreviewed_name_variants_and_other_people_stay_separate(self):
  p=next(p for p in self.c['paragraphs']if p['id'].endswith('p008'));self.assertIn('長［降］',p['text']);self.assertIn('f41_ulg_3u1_*AA',self.people);self.assertIn('fa5_rxi_3t4',self.people);self.assertNotEqual(next(m['person_id']for m in p['mentions']if m['surface']=='長降'),'fa5_rxi_3t4');self.assertEqual(self.c['source']['revision_id'],439220);self.assertEqual(len(self.c['paragraphs']),10)
if __name__=='__main__':unittest.main()
