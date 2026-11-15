import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text())
def marks(ch):return {m['id']:m for p in read(ch)['paragraphs'] for m in p['mentions']}
class EarlyCrossChapterIdentity(unittest.TestCase):
 def test_cuo_keeps_the_existing_sima_root_and_descendants(self):
  people={p['id']:p for p in read('registry/persons.json')['persons']};self.assertNotIn('rec_qtq_9ve',people);self.assertEqual(people['pme_eis_xqi']['label'],'司馬錯')
  expected={'pme_eis_xqi','pme_eis_xqi_*A','pme_eis_xqi_*A*A','pme_eis_xqi_*A*AA','pme_eis_xqi_*A*AAA','pme_eis_xqi_*A*AAAA','pme_eis_xqi_*A*AAAAA'};self.assertEqual({p for p in people if p.startswith('pme_eis_xqi')},expected)
  for ch,mid in [('corpus/shiji/005.json','c-shiji-005-qin:m066-0119'),('corpus/shiji/070.json','c-shiji-070-zhang:m006-0072'),('corpus/shiji/130.json','c-shiji-130-taishigong:m002-0053')]:self.assertEqual(marks(ch)[mid]['person_id'],'pme_eis_xqi')
 def test_wuxinjun_is_resolved_by_the_zhao_event(self):
  m=marks('corpus/shiji/130.json')['c-shiji-130-taishigong:m002-0148'];self.assertEqual(m['person_id'],'yu4_0gm_gje');self.assertEqual(m['surface'],'武信君');other=[m for m in marks('corpus/shiji/007.json').values() if m['surface']=='武信君' and m['person_id']=='5xt_rg8_7zs_A'];self.assertTrue(other);self.assertNotEqual(m['person_id'],other[0]['person_id'])
 def test_qing_is_songyi_without_altering_the_received_character(self):
  m=marks('corpus/shiji/130.json')['c-shiji-130-taishigong:m019-0021'];self.assertEqual((m['surface'],m['person_id']),('慶','uj9_x5q_yir'));self.assertIn('宋義',str(read('source-evidence/shiji130-early-identity/context-reading.json')['annotation_reference']))
 def test_mutilated_sunzi_is_sunbin_and_not_sunwu(self):
  source=marks('corpus/shiji/130.json')['c-shiji-130-taishigong:m012-0115'];self.assertEqual(source['person_id'],'u7n_hyp_nqf');self.assertEqual(marks('corpus/shiji/065.json')['c-shiji-065-sun:m002-0000']['person_id'],'vax_w2r_0za');self.assertNotEqual(source['person_id'],'vax_w2r_0za')
 def test_weiguai_does_not_collapse_the_other_sima_ancestor(self):
  source=marks('corpus/shiji/130.json');self.assertEqual(source['c-shiji-130-taishigong:m049-0033']['person_id'],'n0i_g82_0n2');others=[m for mid,m in source.items() if ':m002-' in mid and m['surface']=='蒯聵'];self.assertTrue(others);self.assertTrue(all(m['person_id']!='n0i_g82_0n2' for m in others))
 def test_all_retired_profiles_are_absent_and_decisions_preserve_uncertainty(self):
  people={p['id'] for p in read('registry/persons.json')['persons']};decisions={d['id']:d for d in read('corpus/shiji/130-identities.json')['decisions']};mids=[]
  for i in range(1,28):
   did=f'd-shiji130-early-cross-chapter-{i:02}';receipt=read(f'source-evidence/shiji130-early-identity/retirement-{i:02}.json');self.assertFalse(people&set(receipt['retired_person_ids']));self.assertFalse(receipt['person_aliases_created']);d=decisions[did];self.assertFalse(d['human_reviewed']);self.assertEqual(d['status'],'contextual_provisional');mids+=d['identification_basis']['target_mention_ids']
  self.assertEqual(len(set(mids)),58);self.assertEqual(decisions['d-shiji130-early-cross-chapter-06']['confidence_level'],'medium')
