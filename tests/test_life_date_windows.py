# Synthetic fixtures only; no historical assertion is written to the corpus.
import copy,unittest
from scripts.life_event_dates import date_window,date_decision_errors,selected_dates,date_record_scope_errors

def event(eid,year):
 evidence=[dict(paragraph_id='synthetic:'+eid,quote='甲年某卒')]
 refs=[dict(url='https://example.invalid/fixture',quote='synthetic',scope=s)for s in ['received_regnal_year_attestation','digital_editorial_regnal_year_equivalence_only','received_calendar_rule']]
 w=dict(earliest=dict(era='BCE',era_year=year+1,year=-year),latest=dict(era='BCE',era_year=year,year=1-year),year_numbering='astronomical',precision='year_range',basis='regnal_year_crosses_ce_year',status='editorial_provisional',original_quote='甲年某卒',evidence=evidence,references=refs,rationale='synthetic fixture',reviewer='synthetic test',human_reviewed=False)
 return dict(id=eid,person_id='synthetic-person',event_type='death',date_expression='甲年',evidence=evidence,normalized_date_range=w)
def decision(events):return dict(id='synthetic-decision',person_ids=['synthetic-person'],event_type='death',candidate_event_ids=[e['id']for e in events],preferred_event_id=events[1]['id'],status='editorial_provisional',rationale='synthetic comparison',evidence=[x for e in events for x in e['evidence']],reviewer='synthetic test',human_reviewed=False,model=None)
class Ranges(unittest.TestCase):
 def setUp(self):self.es=[event('synthetic-a',200),event('synthetic-b',201)];self.d=decision(self.es)
 def errors(self):return date_decision_errors(self.d,{e['id']:e for e in self.es},[],{'synthetic-person':{}})
 def test_overlapping_ranges_can_preserve_recorded_choice(self):
  self.assertEqual(self.errors(),[]);s=selected_dates(self.es,[self.d])[0];self.assertNotIn('year',s);self.assertEqual((s['earliest']['year'],s['latest']['year']),(-201,-200));self.assertEqual(s['selection_decision_id'],'synthetic-decision');self.assertEqual(s['record_id'],'synthetic-b')
 def test_point_and_range_are_distinct_recorded_precisions(self):
  e=self.es[0];e.pop('normalized_date_range');e['normalized_date']=dict(year=-200);self.assertEqual(self.errors(),[])
 def test_equal_bounds_not_a_new_year_conflict(self):
  self.es[1]['normalized_date_range']=copy.deepcopy(self.es[0]['normalized_date_range']);self.es[1]['normalized_date_range']['evidence']=self.es[1]['evidence'];self.assertTrue(self.errors())
 def test_unknown_year_cannot_be_ranked(self):self.es[0].pop('normalized_date_range');self.assertTrue(self.errors())
 def test_range_with_reversed_bounds_rejected(self):
  w=self.es[0]['normalized_date_range'];w['earliest'],w['latest']=w['latest'],w['earliest'];self.assertTrue(self.errors())
 def test_two_date_forms_rejected(self):self.es[0]['normalized_date']=dict(year=-200);self.assertTrue(self.errors())
 def test_selected_nested_range_is_detached_from_source(self):
  s=selected_dates(self.es,[self.d])[0];s['earliest']['year']=0;self.assertEqual(self.es[1]['normalized_date_range']['earliest']['year'],-201)
 def test_unresolved_has_no_selected_range(self):self.d.update(status='unresolved',preferred_event_id=None);self.assertEqual(selected_dates(self.es,[self.d]),[])
 def test_range_cannot_omit_provenance(self):self.es[0]['normalized_date_range']['references']=[];self.assertTrue(self.errors())
 def test_invalid_selected_range_fails_instead_of_guessing(self):
  self.es[1].pop('normalized_date_range')
  with self.assertRaises(ValueError):selected_dates(self.es,[self.d])
 def test_optional_interpretation_reference_is_recorded(self):
  self.d['references']=[dict(title='Synthetic commentary',url='https://example.invalid/commentary',quote='synthetic date interpretation',scope='ancient_commentary_date_interpretation',image_verified=False)];self.assertEqual(self.errors(),[])
 def test_interpretation_reference_requires_safe_url_and_quote(self):
  self.d['references']=[dict(title='Synthetic commentary',url='javascript:alert(1)',quote='',scope='ancient_commentary_date_interpretation',image_verified=False)];self.assertTrue(self.errors())
 def parallel(self):
  e=self.es[1];e['date_expression']=None;w=e['normalized_date_range'];url='https://example.invalid/parallel';w['parallel_event']=dict(kind='parallel_event',source_event_quote='某卒',reference_url=url,reference_event_quote='synthetic parallel death',reference_year_quote='201');w['references'] += [dict(url=url,quote='synthetic parallel death',scope='received_parallel_event'),dict(url=url,quote='201',scope='digital_editorial_regnal_year_equivalence_only')];return e
 def test_parallel_event_range_keeps_two_bounds(self):
  e=self.parallel();self.assertEqual(date_window(e),(-201,-200));self.assertEqual(self.errors(),[]);self.assertNotIn('year',selected_dates(self.es,[self.d])[0])
 def test_parallel_event_cannot_drop_correspondence_reference(self):
  e=self.parallel();e['normalized_date_range']['references']=[r for r in e['normalized_date_range']['references']if r['scope']!='received_parallel_event'];self.assertIsNone(date_window(e));self.assertTrue(self.errors())

class DateWorkScope(unittest.TestCase):
 def setUp(self):
  self.chapters={'synthetic-a':{'work_id':'synthetic-work-a'},'synthetic-b':{'work_id':'synthetic-work-b'}};self.works={'synthetic-work-a','synthetic-work-b'};self.record=dict(work_id='synthetic-work-a',work_ids=['synthetic-work-a','synthetic-work-b'],decisions=[dict(evidence=[dict(chapter_id='synthetic-a',work_id='synthetic-work-a'),dict(chapter_id='synthetic-b',work_id='synthetic-work-b')])])
 def test_cross_work_scope_requires_both_declared_sources(self):self.assertEqual(date_record_scope_errors(self.record,self.chapters,self.works),[])
 def test_missing_or_unrepresented_work_rejected(self):
  self.record.pop('work_ids');self.assertTrue(date_record_scope_errors(self.record,self.chapters,self.works));self.record['work_ids']=['synthetic-work-a','synthetic-unknown'];self.assertTrue(date_record_scope_errors(self.record,self.chapters,self.works))
 def test_evidence_cannot_spoof_its_work(self):
  self.record['decisions'][0]['evidence'][0]['work_id']='synthetic-work-b';self.assertTrue(date_record_scope_errors(self.record,self.chapters,self.works))
if __name__=='__main__':unittest.main(verbosity=2)
