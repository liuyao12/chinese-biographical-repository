"""Contextual identity regressions for shared courtesy names and noble ranks."""
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(path):return json.loads((ROOT/path).read_text())
def paragraph(number,suffix):return next(p for p in read(f'corpus/shiji/{number:03}.json')['paragraphs'] if p['id'].endswith(':'+suffix))
class CourtCourtesyIdentity(unittest.TestCase):
 def test_fifteen_mentions_are_source_bound_and_preserve_entire_units(self):
  r=read('source-evidence/shiji-court-courtesy-identity/context-reading.json');chapters={d['id']:d for f in (ROOT/'corpus').glob('*/*.json') if (d:=json.loads(f.read_text())).get('record_type')=='marked_chapter'};mids={m['id']:m for c in chapters.values() for p in c['paragraphs'] for m in p['mentions']};expected=[m for d in r['identity_decisions'] for m in d['target_mention_ids']];self.assertEqual(len(expected),15);self.assertEqual(len(set(expected)),15)
  for d in r['identity_decisions']:
   for mid in d['target_mention_ids']:self.assertEqual(mids[mid]['person_id'],d['person_id'])
  for unit in r['complete_units']:
   p=next(p for p in chapters[unit['chapter_id']]['paragraphs'] if p['id']==unit['paragraph']['id']);self.assertEqual(p,unit['paragraph'])
 def test_eleven_retired_candidates_have_no_active_registry_alias(self):
  people=read('registry/persons.json')['persons'];active={p['id'] for p in people};retired=[]
  for i in range(1,12):
   r=read(f'source-evidence/shiji-court-courtesy-identity/retirement-{i:02}.json');self.assertEqual(r['identity_decision_id'],f'd-shiji-court-courtesy-cross-chapter-{i:02}');retired+=r['retired_person_ids'];self.assertFalse(r['person_aliases_created'])
  self.assertEqual(len(set(retired)),11);self.assertFalse(active&set(retired))
  for p in people:self.assertFalse(set(p.get('id_aliases',[]))&set(retired))
 def test_shared_changru_does_not_merge_hananguo_and_jian(self):
  p=paragraph(108,'p014');self.assertEqual(next(m['person_id'] for m in p['mentions'] if m['surface']=='韓長孺'),'6hy_i1z_hu2')
  p=paragraph(130,'p132');self.assertEqual(next(m['person_id'] for m in p['mentions'] if m['surface']=='長孺'),'fmh_dmt_cql')
  p=paragraph(120,'p001');self.assertEqual(next(m['person_id'] for m in p['mentions'] if m['surface']=='長孺'),'fmh_dmt_cql')
 def test_wuan_in_weiqi_summary_is_tianfen_not_baiqi(self):
  p=paragraph(130,'p119');self.assertEqual(next(m['person_id'] for m in p['mentions'] if m['surface']=='武安'),'7mz_d13_9ka_A')
  p=paragraph(73,'p001');self.assertEqual({m['person_id'] for m in p['mentions'] if m['surface']=='武安君'},{'2bk_fz6_icl'})
 def test_wuan_successor_is_not_backfilled_to_father(self):
  p=paragraph(107,'p025');marks=[m for m in p['mentions'] if m['surface']=='武安侯'];self.assertEqual([m['person_id'] for m in marks],['7mz_d13_9ka_A','7mz_d13_9ka_AA'])
 def test_recommended_counsellors_are_not_turned_into_appointments(self):
  p=paragraph(58,'p025');self.assertIn('如汲黯、韓長孺',p['text']);self.assertEqual({m['person_id'] for m in p['mentions'] if m['surface'] in ('汲黯','韓長孺')},{'fmh_dmt_cql','6hy_i1z_hu2'})
  for f in (ROOT/'corpus').glob('*/*-titles.json'):
   for h in json.loads(f.read_text())['holdings']:
    if h['person_id'] in ('fmh_dmt_cql','6hy_i1z_hu2'):self.assertFalse(any(e['paragraph_id']==p['id'] for e in h['evidence']))
 def test_zhuang_variant_is_local_and_received_characters_survive(self):
  p=paragraph(130,'p132');self.assertIn('壯有溉',p['text']);self.assertEqual(next(m['person_id'] for m in p['mentions'] if m['surface']=='壯'),'jws_b08_hob')
  p=paragraph(120,'p015');self.assertIn('字莊',p['text']);self.assertEqual(next(m['person_id'] for m in p['mentions'] if m['surface']=='莊'),'jws_b08_hob')
 def test_royal_brother_relation_keeps_both_current_endpoints(self):
  a=next(a for a in read('corpus/shiji/011-assertions.json')['assertions'] if a['id']=='a-shiji011-012');self.assertEqual((a['subject_person_id'],a['predicate'],a['object_person_id']),('7mz_d13_9ka_A','brother','6d6_eg1_o3a_A'));self.assertEqual(a['qualifiers']['source_term'],'弟')
 def test_candidate_pool_dedup_does_not_identify_chenying_as_douying(self):
  row=next(r for r in read('source-evidence/xintang071xia-chen-preface/identities.json')['identities'] if r['source_local_identity_key']=='xts071xia-chen-ying');self.assertEqual(row['person_id'],'6us_ibm_u05');hits=row['candidate_hits_are_not_decisions'];self.assertEqual(len(hits),11);self.assertEqual(len({h['person_id'] for h in hits}),11);self.assertEqual(next(h['label'] for h in hits if h['person_id']=='nuf_tb9_fjs_A'),'竇嬰')
 def test_existing_cross_chapter_decision_and_normalized_name_survive(self):
  d=next(d for d in read('corpus/shiji/012-identities.json')['decisions'] if d['id']=='d-shiji012-007');self.assertEqual(d['person_id'],'7mz_d13_9ka_A');self.assertEqual(d['scope'],'cross_chapter');self.assertEqual(len(d['chapter_ids']),2);self.assertTrue(d['prior_contextual_rationale'])
  self.assertEqual(next(p['label'] for p in read('registry/persons.json')['persons'] if p['id']=='7mz_d13_9ka_A'),'田蚡')
if __name__=='__main__':unittest.main(verbosity=2)
