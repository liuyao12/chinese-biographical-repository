import json,unittest,copy
from pathlib import Path
from scripts.person_bundle import bundle,load_catalog
from scripts.life_event_dates import date_decision_errors,date_record_scope_errors
ROOT=Path(__file__).resolve().parents[1]
def read(f):return json.loads((ROOT/f).read_text())
class WeiqiDeathChoices(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.catalog=load_catalog(ROOT)
 def test_four_deaths_keep_subjects_and_literal_years(self):
  es=read('corpus/shiji/107-life-events.json')['events'];self.assertEqual([e['person_id']for e in es],['ixk_6fg_v6f_A','h1w_44g_vef','nuf_tb9_fjs_A','7mz_d13_9ka_A']);self.assertEqual([e['normalized_date_range']['latest']['era_year']for e in es],[135,154,130,130]);self.assertEqual(es[1]['source_term'],'遂死吳軍中');self.assertEqual(es[3]['source_term'],'竟死')
 def test_preferred_range_does_not_choose_an_endpoint_or_hide_alternative(self):
  for pid,preferred in [('nuf_tb9_fjs_A','le-hanshu006-003'),('7mz_d13_9ka_A','le-hanshu006-004')]:
   b=bundle(pid,catalog=self.catalog);d=next(d for d in b['life_event_date_decisions']if d['id'].startswith('ld-shiji107-'));self.assertEqual(d['preferred_event_id'],preferred);s=next(s for s in b['selected_life_event_dates']if s['selection_decision_id']==d['id']);self.assertNotIn('year',s);self.assertEqual((s['earliest']['era_year'],s['latest']['era_year']),(132,131));self.assertTrue(any(e['normalized_date_range']['latest']['era_year']==130 for e in b['life_events']if e['id'].startswith('le-shiji107-')))
 def test_hypothetical_suicide_and_successor_not_death_subjects(self):
  es=read('corpus/shiji/107-life-events.json')['events'];self.assertFalse(any(e['person_id']=='7mz_d13_9ka_AA'for e in es));self.assertFalse(any('齰舌自殺'in e['source_term']for e in es));self.assertFalse(any(e['person_id']=='h1w_44g_vef_A'for e in es))
 def test_commentary_is_reported_without_editing_received_five(self):
  c=read('corpus/shiji/107.json');self.assertIn('五年十月',c['paragraphs'][23]['text']);v=next(v for v in c['annotation']['reported_variants']if v['id']=='rv-shiji107-death-year');self.assertIn('元光四年十月，灌夫弃市。',v['quote']);self.assertIn('h1w_44g_vef_A',v['person_ids']);self.assertFalse(v['adopted']);self.assertFalse(v['image_verified'])
 def test_choice_keeps_two_source_works_and_commentary_citations(self):
  r=read('corpus/shiji/107-date-decisions.json');self.assertEqual(set(r['work_ids']),{'w-shiji','w-hanshu'})
  for d in r['decisions']:self.assertEqual({e['work_id']for e in d['evidence']},{'w-shiji','w-hanshu'});self.assertTrue(d['references']);self.assertTrue(all(not x['image_verified']for x in d['references']))
 def test_machine_profile_preserves_preferred_range_and_references(self):
  p=read('data/corpus/profiles/nuf_tb9_fjs_A.json');d=next(d for d in p['life_event_date_decisions']if d['id']=='ld-shiji107-death-001');self.assertIn('按：五年者，誤也。',[r['quote']for r in d['references']]);s=next(s for s in p['selected_life_event_dates']if s['selection_decision_id']==d['id']);self.assertEqual(s['precision'],'year_range');self.assertEqual(s['record_id'],'le-hanshu006-003')
