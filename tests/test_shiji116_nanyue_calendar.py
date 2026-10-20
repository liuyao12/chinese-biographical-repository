import json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
PID='bvb_d1z_fd0_*A'
def read(p):return json.loads((R/p).read_text())
class NanyueCalendar(unittest.TestCase):
 def test_three_received_references_share_hu_without_new_identity(self):
  for ch,mid in [('116','c-shiji-116-xinanyi:m003-0156'),('113','c-shiji-113-nanyue:m004-0004'),('113','c-shiji-113-nanyue:m005-0008')]:
   c=read(f'corpus/shiji/{ch}.json');p,m=next((p,m)for p in c['paragraphs']for m in p['mentions']if m['id']==mid);self.assertEqual(m['person_id'],PID);self.assertEqual(p['text'][m['start']:m['end']],'南越王')
 def test_profile_name_components_preserve_received_hu_and_posthumous_title(self):
  n=next(n for n in read('data/corpus/profile-names.json')['records']if n['person_id']==PID);self.assertEqual((n['title'],n['surname'],n['ming']),('南越王',None,'胡'));self.assertEqual(n['additional_names'],['文王']);self.assertIn('佗孫胡為南越王',n['quote']);self.assertEqual(n['references'][0]['quote'],'胡薨，謚為文王。')
 def test_decision_identifies_parallel_campaign_and_excludes_other_kings(self):
  d=next(d for d in read('corpus/shiji/116-identities.json')['decisions']if d['id']=='d-shiji116-nanyue-king-hu');self.assertEqual(d['scope'],'cross_chapter');self.assertEqual(set(d['chapter_ids']),{'c-shiji-113-nanyue','c-shiji-116-xinanyi'});self.assertIn('餘善殺郢',d['identification_basis']['same_event']);self.assertEqual(d['references'][0]['quote'],'至建元四年卒。');self.assertEqual(set(d['identification_basis']['excluded_person_ids']),{'bvb_d1z_fd0','bvb_d1z_fd0_*AA'});self.assertFalse(d['human_reviewed'])
 def test_ying_death_keeps_unspecified_month_as_two_ce_years(self):
  e=next(e for e in read('corpus/shiji/116-life-events.json')['events']if e['person_id']=='xp5_39k_w5w');self.assertNotIn('normalized_date',e);d=e['normalized_date_range'];self.assertEqual([d[k]['era_year']for k in ['earliest','latest']],[136,135]);self.assertEqual([d[k]['year']for k in ['earliest','latest']],[-135,-134]);self.assertEqual(d['regnal_year_table']['calendar_rule'],'han_tenth_month_before_taichu');self.assertIn('東越殺王郢',d['original_quote']);self.assertEqual(d['evidence'],e['evidence'])
 def test_three_opening_titles_have_usage_windows_but_no_accession(self):
  hs={h['id']:h for h in read('corpus/shiji/116-titles.json')['holdings']}
  for hid in ['th-shiji116-004','th-shiji116-005','th-shiji116-006']:
   h=hs[hid];a=h['attestations'][0];self.assertEqual(a['date_expression'],'建元六年');self.assertEqual([a['normalized_date_range'][k]['era_year']for k in ['earliest','latest']],[136,135]);self.assertEqual(h['effective_period']['start']['status'],'unknown');self.assertEqual(h['effective_period']['end']['status'],'unknown')
  h=hs['th-shiji116-021'];self.assertEqual(h['person_id'],PID);self.assertEqual(h['mode'],'attestation');self.assertIsNone(h['attestations'][0]['date_expression']);self.assertTrue(all(x['status']=='unknown'for x in h['effective_period'].values()))
 def test_later_unknown_event_dates_are_not_filled_from_opening_year(self):
  events=read('corpus/shiji/116-life-events.json')['events']
  for e in events:
   if e['person_id']=='xp5_39k_w5w':continue
   self.assertIsNone(e['date_expression']);self.assertNotIn('normalized_date_range',e);self.assertNotIn('normalized_date',e)
if __name__=='__main__':unittest.main()
