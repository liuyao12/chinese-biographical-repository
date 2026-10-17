# coding:utf-8
import json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def load(f):return json.loads((R/f).read_text())
class NanyueOfficesAndCommentary(unittest.TestCase):
 def holdings(self):return {h['id']:h for h in load('corpus/shiji/113-titles.json')['holdings']}
 def test_acting_office_not_formal_grant(self):
  h=self.holdings()['th-shiji113-034'];self.assertEqual(h['person_id'],'bvb_d1z_fd0');self.assertEqual(h['title'],'行南海尉事');self.assertEqual(h['appointment_role'],'acting');self.assertEqual(h['mode'],'attestation');self.assertIn(h['source_term'],h['evidence'][0]['quote'])
  for b in h['effective_period'].values():self.assertEqual(b['status'],'unknown');self.assertIsNone(b['date_expression'])
 def test_ren_xiao_office_is_separate_person(self):
  h=self.holdings()['th-shiji113-003'];self.assertEqual(h['person_id'],'e8q_4ar_5bh');self.assertEqual(h['title'],'南海尉')
 def test_su_hong_old_office_is_not_surname_or_new_grant(self):
  h=self.holdings()['th-shiji113-035'];self.assertEqual(h['person_id'],'m08_4xt_opo');self.assertEqual(h['title'],'校尉司馬');self.assertEqual(h['attestations'][0]['usage'],'retrospective');self.assertEqual(h['source_term'],'故校尉司馬');self.assertEqual(h['mode'],'attestation');r=h['references'][0];self.assertIn('校之司馬',r['raw_quote']);self.assertIn('宏得建德',r['raw_quote']);self.assertFalse(r['image_verified'])
 def test_lao_hou_anchor_keeps_received_characters_and_id(self):
  c=load('corpus/shiji/113.json');p=next(p for p in c['paragraphs']if p['id'].endswith('p014'));m=next(m for m in p['mentions']if m['id']=='c-shiji-113-nanyue:m014-0030');self.assertEqual(p['text'][m['start']:m['end']],'嫪後');self.assertEqual(m['person_id'],'3q4_zsp_jwy');self.assertEqual(m['status'],'contextual_provisional');self.assertEqual(p['text_layer'],'witness_appended_suoyin_zan')
 def test_lao_hou_decision_is_contextual_not_claimed_collation(self):
  d=next(d for d in load('corpus/shiji/113-identities.json')['decisions']if d['id']=='d-shiji113-laohou-context');self.assertEqual({e['paragraph_id'].rsplit(':',1)[-1]for e in d['evidence']},{'p007','p008','p014'});self.assertFalse(d['human_reviewed']);self.assertIn('未有原刊',d['rationale']);self.assertIn('不認定歷史別名',d['rationale'])
 def test_death_year_keeps_civil_year_uncertainty_and_typed_row(self):
  e=next(e for e in load('corpus/shiji/113-life-events.json')['events']if e['person_id']=='bvb_d1z_fd0');self.assertEqual(e['date_expression'],'建元四年');self.assertNotIn('normalized_date',e);w=e['normalized_date_range'];self.assertEqual((w['earliest']['era_year'],w['latest']['era_year']),(138,137));self.assertEqual(w['regnal_year_table']['regnal_year_cell_id'],'shiji-022-t1-r070-c01');self.assertEqual(w['regnal_year_table']['calendar_rule'],'han_tenth_month_before_taichu')
 def test_explicit_autumn_preserved_for_two_appointments(self):
  for hid in ['th-shiji113-022','th-shiji113-024']:
   h=self.holdings()[hid];self.assertEqual(h['effective_period']['start']['date_expression'],'元鼎五年秋');self.assertEqual(h['effective_period']['start']['normalized_date']['era_year'],112);self.assertEqual(h['attestations'][0]['date_expression'],'元鼎五年秋')
 def test_death_does_not_supply_all_zhao_tuo_title_ends(self):
  for h in self.holdings().values():
   if h['person_id']=='bvb_d1z_fd0':self.assertEqual(h['effective_period']['end']['status'],'unknown')
if __name__=='__main__':unittest.main()
